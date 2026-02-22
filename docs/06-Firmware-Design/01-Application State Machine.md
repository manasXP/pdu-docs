---
tags: [PDU, firmware, state-machine, STM32G474, implementation]
created: 2026-02-22
---

# 01 – Application State Machine

> [!note] Scope
> This document defines the top-level application state machine for the 30 kW PDU firmware. For HRTIM resource mapping, ADC allocation, and control loop structures, see [[06-Firmware Architecture]]. For HW-side power-on sequencing (NTC, relay, contactor), see [[08-Power-On Sequence and Inrush Management]].

---

## 1. State Enumeration

The application runs a single top-level state machine (`AppState_t`) in the main loop at 1 kHz. All ISR-level control loops (PFC current, LLC voltage) check `g_app_state` to decide whether to produce active PWM output.

```c
typedef enum {
    APP_POWER_ON       = 0,   // HW init, peripheral config
    APP_STANDBY        = 1,   // Waiting for enable command (CAN or local)
    APP_PLL_LOCK       = 2,   // SRF-PLL acquiring grid angle
    APP_SOFT_START_PFC = 3,  // PFC bus voltage ramp
    APP_SOFT_START_LLC = 4,  // LLC output voltage ramp
    APP_RUN            = 5,   // Normal CC/CV charging
    APP_DERATE         = 6,   // Thermal or input derate active
    APP_FAULT          = 7,   // Fault condition — outputs disabled
    APP_SHUTDOWN       = 8,   // Controlled ramp-down
    APP_DISABLED       = 9,   // Outputs permanently off until power cycle
} AppState_t;
```

---

## 2. ASCII State Diagram

```
                          ┌─────────────────────────────────────────────┐
                          │                                             │
                          v                                             │
                    ┌──────────┐    init_ok      ┌──────────┐          │
     Power ──────>  │ POWER_ON │ ──────────────> │ STANDBY  │          │
                    └──────────┘                 └──────────┘          │
                          │                        │    ^              │
                          │ init_fail              │    │ stop_cmd     │
                          v                        │    │              │
                    ┌──────────┐                   │    │              │
                    │ DISABLED │ <─────────────────┼────┼──────────┐   │
                    └──────────┘  unrecoverable    │    │          │   │
                                                   │ enable_cmd    │   │
                                                   v               │   │
                                             ┌──────────┐          │   │
                                             │ PLL_LOCK │          │   │
                                             └──────────┘          │   │
                                               │    │              │   │
                                    pll_locked │    │ timeout      │   │
                                               v    v              │   │
                                        ┌───────────────┐          │   │
                                        │ SOFT_START_PFC│          │   │
                                        └───────────────┘          │   │
                                               │    │              │   │
                                    vbus_ok    │    │ fault        │   │
                                               v    │              │   │
                                        ┌───────────────┐          │   │
                                        │ SOFT_START_LLC│          │   │
                                        └───────────────┘          │   │
                                               │    │              │   │
                                    vout_ok    │    │ fault        │   │
                                               v    │              │   │
                                         ┌─────────┐               │   │
                                ┌──────> │   RUN   │ ───────┐      │   │
                                │        └─────────┘        │      │   │
                                │          │    │           │      │   │
                                │  thermal │    │ fault     │      │   │
                                │  clear   │    │           │      │   │
                                │          v    │           │      │   │
                                │       ┌────────┐          │      │   │
                                └────── │ DERATE │          │      │   │
                                        └────────┘          │      │   │
                                           │                │      │   │
                                      fault│                │      │   │
                                           v                v      │   │
                                        ┌─────────────────────┐    │
                                        │       FAULT         │    │
                                        └─────────────────────┘    │
                                           │          │            │
                                  retry_ok │          │ latch      │
                                           │          v            │
                                           │     ┌──────────┐      │
                                           │     │ DISABLED │      │
                                           │     └──────────┘      │
                                           v                       │
                                        ┌──────────┐               │
                              ┌──────── │ SHUTDOWN │ <─────────────┘
                              │         └──────────┘   stop_cmd
                              │ done
                              v
                         ┌──────────┐
                         │ STANDBY  │
                         └──────────┘
```

---

## 3. State Transition Table

| # | Source State | Event / Trigger | Guard Condition | Target State | Action |
|---|-------------|----------------|-----------------|--------------|--------|
| 1 | POWER_ON | Peripheral init complete | All self-tests pass | STANDBY | Set status LED green-blink |
| 2 | POWER_ON | Init failure | HRTIM DLL cal fail OR ADC self-cal fail | DISABLED | Log fault, set LED red-solid |
| 3 | STANDBY | Enable command (CAN or local) | V_aux_12V within range | PLL_LOCK | Start SRF-PLL, enable ADC injected |
| 4 | STANDBY | Stop command | — | STANDBY | No-op (already idle) |
| 5 | PLL_LOCK | PLL locked | V_q < 5 V for 20 consecutive samples | SOFT_START_PFC | Enable HRTIM PFC outputs |
| 6 | PLL_LOCK | Timeout | t > 2 s | FAULT | Log PLL_LOCK_TIMEOUT |
| 7 | PLL_LOCK | Grid absent | V_grid_rms < 100 V | FAULT | Log GRID_ABSENT |
| 8 | SOFT_START_PFC | V_bus reached target | V_bus > V_target − 10 V, stable for 50 ms | SOFT_START_LLC | Begin LLC soft-start |
| 9 | SOFT_START_PFC | Timeout | t > 5 s | FAULT | Log PFC_START_TIMEOUT |
| 10 | SOFT_START_PFC | Fault (OVP/OCP) | HW comparator trip | FAULT | HRTIM auto-idle, log fault |
| 11 | SOFT_START_LLC | V_out reached target | V_out within ±2% of V_ref for 100 ms | RUN | Enable CAN status broadcast |
| 12 | SOFT_START_LLC | Timeout | t > 5 s | FAULT | Log LLC_START_TIMEOUT |
| 13 | SOFT_START_LLC | Fault (OVP/OCP) | HW comparator trip | FAULT | HRTIM auto-idle, log fault |
| 14 | RUN | Thermal warning | T_SiC > 100°C OR T_mag > 120°C OR T_amb > 55°C | DERATE | Reduce I_ref per derate curve |
| 15 | RUN | Critical fault | HW fault input OR SW OVP/OCP | FAULT | Immediate HRTIM idle, log |
| 16 | RUN | Stop command (CAN) | — | SHUTDOWN | Begin controlled ramp-down |
| 17 | RUN | CAN timeout (50 ms) | No master cmd for 50 ms | DERATE | Reduce to 50% rated |
| 18 | RUN | CAN timeout (200 ms) | No master cmd for 200 ms | SHUTDOWN | Controlled shutdown |
| 19 | DERATE | Thermal cleared | All temps below warning − hysteresis | RUN | Restore full I_ref |
| 20 | DERATE | Critical fault | HW fault OR temp exceeds shutdown | FAULT | Immediate idle, log |
| 21 | DERATE | Stop command | — | SHUTDOWN | Begin ramp-down |
| 22 | FAULT | Retry OK (major fault) | retry_count < 3, cooldown elapsed | PLL_LOCK | Increment retry, restart sequence |
| 23 | FAULT | Latch (critical fault) | Unrecoverable fault type | DISABLED | Permanent off, log to flash |
| 24 | FAULT | Clear command (diagnostic) | Operator clears via CAN diag | STANDBY | Reset fault flags |
| 25 | SHUTDOWN | Ramp complete | I_out < 0.5 A, contactors open | STANDBY | Disable HRTIM outputs |
| 26 | SHUTDOWN | Fault during ramp | HW fault input | FAULT | Immediate idle |
| 27 | DISABLED | Power cycle only | — | POWER_ON | Full HW reset |

---

## 4. Timeout Table

| State | Timeout | Action on Timeout |
|-------|---------|-------------------|
| PLL_LOCK | 2 s | → FAULT (PLL_LOCK_TIMEOUT) |
| SOFT_START_PFC | 5 s | → FAULT (PFC_START_TIMEOUT) |
| SOFT_START_LLC | 5 s | → FAULT (LLC_START_TIMEOUT) |
| SHUTDOWN | 3 s | → FAULT (SHUTDOWN_TIMEOUT) — force idle |
| FAULT (retry cooldown) | 10 s | Allow retry attempt |
| DERATE (CAN watchdog) | 200 ms from last 50 ms warning | → SHUTDOWN |

**CAN watchdog (slave mode):**

| Threshold | Action |
|-----------|--------|
| 50 ms without master command | → DERATE (50% rated) |
| 200 ms without master command | → SHUTDOWN |

---

## 5. ISR Priority vs. Main-Loop Transitions

State transitions are **requested** by ISRs via atomic flags but **executed** in the main loop to avoid priority inversion and complex critical sections.

```
ISR context (cannot change state directly):
  ├── HW fault ISR (HRTIM FLT)    → sets g_fault_pending = FAULT_OVP / FAULT_OCP
  ├── PFC current ISR              → sets g_pfc_vbus_ok flag
  ├── LLC voltage ISR              → sets g_llc_vout_ok flag
  └── CAN Rx ISR                   → sets g_can_cmd_pending

Main loop (1 kHz, executes transitions):
  └── App_SM_Run()
      ├── Reads atomic flags
      ├── Evaluates guards
      ├── Executes transition actions
      └── Clears flags
```

**Priority order (highest first):**

| Priority | ISR | NVIC Level |
|----------|-----|------------|
| 0 (highest) | HRTIM Fault | 0 |
| 1 | PFC Current Control | 1 |
| 2 | LLC Voltage Control | 2 |
| 3 | CAN Rx | 5 |
| 4 | TIM6 (1 kHz background) | 7 |
| — | Main loop (state machine) | Thread mode |

---

## 6. Pseudocode: `App_SM_Run()`

Called from `main()` at 1 kHz (TIM6 tick or SysTick).

```c
void App_SM_Run(void)
{
    uint32_t now = HAL_GetTick();

    /* Check for pending fault flag from ISR (highest priority) */
    uint32_t fault = __atomic_exchange_n(&g_fault_pending, 0, __ATOMIC_SEQ_CST);
    if (fault != FAULT_NONE && g_app_state != APP_FAULT && g_app_state != APP_DISABLED) {
        Fault_Enter(fault);  /* see [[03-Fault State Machine and Recovery]] */
        return;
    }

    switch (g_app_state) {

    case APP_POWER_ON:
        /* Peripheral init done in main() before this loop starts.
         * We arrive here once; transition immediately.                */
        if (g_init_ok) {
            State_Transition(APP_STANDBY);
        } else {
            State_Transition(APP_DISABLED);
        }
        break;

    case APP_STANDBY:
        /* Waiting for enable command via CAN or local pushbutton */
        if (g_can_cmd_pending & CMD_ENABLE) {
            g_can_cmd_pending &= ~CMD_ENABLE;
            if (AuxRail_OK()) {
                g_state_timer = now;
                PLL_Start();
                State_Transition(APP_PLL_LOCK);
            }
        }
        break;

    case APP_PLL_LOCK:
        if (PLL_IsLocked()) {
            g_state_timer = now;
            PFC_SoftStart_Begin();
            State_Transition(APP_SOFT_START_PFC);
        } else if ((now - g_state_timer) > PLL_LOCK_TIMEOUT_MS) {
            Fault_Enter(FAULT_PLL_TIMEOUT);
        }
        break;

    case APP_SOFT_START_PFC:
        PFC_SoftStart_Tick();  /* see [[02-Power-On Sequence and Ramp Control]] */
        if (g_pfc_vbus_ok && (now - g_vbus_stable_since) > 50) {
            g_state_timer = now;
            LLC_SoftStart_Begin();
            State_Transition(APP_SOFT_START_LLC);
        } else if ((now - g_state_timer) > SOFT_START_TIMEOUT_MS) {
            Fault_Enter(FAULT_PFC_START_TIMEOUT);
        }
        break;

    case APP_SOFT_START_LLC:
        LLC_SoftStart_Tick();  /* see [[02-Power-On Sequence and Ramp Control]] */
        if (g_llc_vout_ok && (now - g_vout_stable_since) > 100) {
            CAN_EnableStatusBroadcast();
            State_Transition(APP_RUN);
        } else if ((now - g_state_timer) > SOFT_START_TIMEOUT_MS) {
            Fault_Enter(FAULT_LLC_START_TIMEOUT);
        }
        break;

    case APP_RUN:
        Burst_Mode_Tick();  /* see [[04-LLC Burst Mode]] */
        NP_Balance_Update();  /* see [[07-Neutral Point Balancing]] */

        if (Thermal_Derate_Required()) {
            Thermal_Derate_Apply();
            State_Transition(APP_DERATE);
        }
        if (g_can_cmd_pending & CMD_STOP) {
            g_can_cmd_pending &= ~CMD_STOP;
            Shutdown_Begin();
            State_Transition(APP_SHUTDOWN);
        }
        if (CAN_Watchdog_Expired(50)) {
            Thermal_Derate_Apply();  /* 50% reduction */
            State_Transition(APP_DERATE);
        }
        break;

    case APP_DERATE:
        Thermal_Derate_Calc();  /* see [[03-Fault State Machine and Recovery]] */
        if (Thermal_Derate_Cleared()) {
            State_Transition(APP_RUN);
        }
        if (CAN_Watchdog_Expired(200)) {
            Shutdown_Begin();
            State_Transition(APP_SHUTDOWN);
        }
        if (g_can_cmd_pending & CMD_STOP) {
            Shutdown_Begin();
            State_Transition(APP_SHUTDOWN);
        }
        break;

    case APP_FAULT:
        Fault_Recovery_Check();  /* see [[03-Fault State Machine and Recovery]] */
        break;

    case APP_SHUTDOWN:
        Shutdown_Tick();
        if (Shutdown_Complete()) {
            HRTIM_DisableAllOutputs();
            Contactor_Open();
            State_Transition(APP_STANDBY);
        } else if ((now - g_state_timer) > SHUTDOWN_TIMEOUT_MS) {
            Fault_Enter(FAULT_SHUTDOWN_TIMEOUT);
        }
        break;

    case APP_DISABLED:
        /* Dead state — only exit is power cycle */
        __WFI();  /* Sleep until interrupt (watchdog will keep running) */
        break;
    }
}
```

---

## 7. `State_Transition()` Helper

```c
static inline void State_Transition(AppState_t new_state)
{
    AppState_t old = g_app_state;
    g_app_state = new_state;
    g_state_timer = HAL_GetTick();

    /* Telemetry: log state change to ring buffer */
    StateLog_Append(old, new_state, g_state_timer);

    /* CAN: broadcast state change immediately (don't wait for 10 ms cycle) */
    CAN_SendStateChange(new_state);
}
```

---

## References

- [[06-Firmware Architecture]] — HRTIM resource map, ISR timing budget (§3.2), protection implementation (§7)
- [[08-Power-On Sequence and Inrush Management]] — HW-side startup sequence
- [[02-Power-On Sequence and Ramp Control]] — FW-side ramp profiles (this sub-folder)
- [[03-Fault State Machine and Recovery]] — Fault classification and recovery logic (this sub-folder)
- [[04-LLC Burst Mode]] — Burst mode sub-states within RUN (this sub-folder)
- [[07-Neutral Point Balancing]] — NP balance within RUN (this sub-folder)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 10 states, 27 transitions |
