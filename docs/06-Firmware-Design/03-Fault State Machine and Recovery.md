---
tags: [PDU, firmware, fault-handling, protection, thermal-derate, STM32G474]
created: 2026-02-22
---

# 03 – Fault State Machine and Recovery

> [!note] Scope
> This document covers **firmware fault classification, detection, recovery logic, thermal derating, and fault logging**. For hardware protection thresholds and comparator-to-HRTIM fault routing, see [[06-Firmware Architecture]] §7. For insulation coordination, hipot, surge immunity, and safety compliance, see [[09-Protection and Safety]]. For thermal budget and junction temperature limits, see [[04-Thermal Budget]].

---

## 1. Fault Severity Classification

| Level | Name | Response | Recovery | Example |
|-------|------|----------|----------|---------|
| 0 | **Critical** | Immediate HRTIM idle (HW latch) | No auto-recovery; power cycle or diagnostic clear | DC bus OVP, output OVP, destructive OCP, ground fault |
| 1 | **Major** | HRTIM idle, enter FAULT state | Auto-retry up to 3 times with 10 s cooldown | PLL lock timeout, soft-start timeout, phase loss, CAN bus-off |
| 2 | **Warning** | Reduce output power (derate) | Auto-clear when condition resolves + hysteresis | Over-temperature, CAN 50 ms timeout, input undervoltage |

---

## 2. Fault Source Registry

| ID | Fault Name | Source | Severity | Detection Latency | HRTIM Fault Input | Notes |
|----|-----------|--------|----------|-------------------|-------------------|-------|
| 0x01 | PFC_OCP_HW | COMP1/2/3 → shunt | Critical | < 200 ns | FLT1 | Cycle-by-cycle in normal, latch if persistent |
| 0x02 | LLC_OCP_HW | COMP4/5 → CT | Critical | < 200 ns | FLT2 | Resonant current exceeds 2× rated peak |
| 0x03 | VBUS_OVP_HW | COMP6 → divider | Critical | < 1 us | FLT3 | V_bus > 966 V (920 × 1.05) |
| 0x04 | VOUT_OVP_HW | COMP7 → divider | Critical | < 1 us | FLT4 | V_out > 1050 V |
| 0x05 | GROUND_FAULT | External RCD relay | Critical | 10 ms | FLT5 | Residual current > 30 mA |
| 0x06 | PFC_OCP_SW | ISR: I_phase > 70 A | Major | 1 PWM period | — | Software current limit exceeded |
| 0x07 | LLC_OCP_SW | ISR: I_out > 105 A | Major | 1 sample | — | Output current limit exceeded |
| 0x08 | VBUS_OVP_SW | ISR: V_bus > 940 V | Major | 1 ms | — | Below HW threshold but above FW limit |
| 0x09 | VBUS_UVP | ISR: V_bus < 600 V | Major | 1 ms | — | Bus collapsed — LLC disabled |
| 0x0A | VOUT_UVP | ISR: V_out < V_ref − 50 V | Warning | 20 ms | — | Output voltage droop |
| 0x0B | PLL_TIMEOUT | Main: t > 2 s in PLL_LOCK | Major | 2 s | — | Grid absent or distorted |
| 0x0C | PFC_START_TIMEOUT | Main: t > 5 s in SOFT_START_PFC | Major | 5 s | — | PFC failed to reach V_bus target |
| 0x0D | LLC_START_TIMEOUT | Main: t > 5 s in SOFT_START_LLC | Major | 5 s | — | LLC failed to reach V_out target |
| 0x0E | SHUTDOWN_TIMEOUT | Main: t > 3 s in SHUTDOWN | Critical | 3 s | — | Controlled shutdown failed |
| 0x0F | OTP_SIC | ADC: T_SiC > 115°C | Critical | 10 ms | — | SiC junction over-temperature shutdown |
| 0x10 | OTP_MAG | ADC: T_mag > 140°C | Critical | 10 ms | — | Magnetics over-temperature shutdown |
| 0x11 | OTP_SIC_WARN | ADC: T_SiC > 100°C | Warning | 10 ms | — | Thermal derate begins |
| 0x12 | OTP_MAG_WARN | ADC: T_mag > 120°C | Warning | 10 ms | — | Thermal derate begins |
| 0x13 | OTP_AMB_WARN | ADC: T_amb > 55°C | Warning | 100 ms | — | Ambient thermal derate |
| 0x14 | CAN_TIMEOUT_50 | Main: no cmd > 50 ms | Warning | 50 ms | — | Derate to 50% |
| 0x15 | CAN_TIMEOUT_200 | Main: no cmd > 200 ms | Major | 200 ms | — | → SHUTDOWN |
| 0x16 | CAN_BUSOFF | FDCAN error state | Major | Immediate | — | CAN bus-off recovery |
| 0x17 | AUX_RAIL_UV | ADC: V_aux < 11.4 V | Critical | 100 ms | — | Gate driver supply lost |
| 0x18 | PHASE_LOSS | PLL: freq deviation > 5 Hz | Major | 20 ms | — | Grid phase lost |

---

## 3. Fault State Diagram

```
                                ┌───────────────┐
                                │    NORMAL     │  (RUN, DERATE, SOFT_START states)
                                │               │
                                └───────┬───────┘
                                        │
                            fault detected (any severity)
                                        │
                                        v
                          ┌─────────────────────────────┐
                          │        FAULT_ACTIVE         │
                          │                             │
                          │  1. HRTIM outputs → idle    │
                          │  2. Log fault to ring buffer│
                          │  3. Broadcast on CAN        │
                          │  4. Classify severity       │
                          └─────┬───────────────┬───────┘
                                │               │
                     severity=0 │               │ severity=1
                     (Critical) │               │ (Major)
                                │               │
                                v               v
                    ┌───────────────┐  ┌─────────────────────┐
                    │ FAULT_LATCHED │  │    FAULT_RETRY      │
                    │               │  │                     │
                    │ Permanent off │  │ Wait 10 s cooldown  │
                    │ LED red-solid │  │ retry_count < 3?    │
                    │               │  │                     │
                    └───────┬───────┘  └──┬──────────┬───────┘
                            │             │          │
                    diag_clear_cmd  retry_ok    retry_count >= 3
                            │             │          │
                            v             v          v
                    ┌───────────┐  ┌───────────┐  ┌───────────────┐
                    │  STANDBY  │  │ PLL_LOCK  │  │ FAULT_LATCHED │
                    │ (cleared) │  │ (restart) │  │ (exhausted)   │
                    └───────────┘  └───────────┘  └───────────────┘


              severity=2 (Warning):
              ┌───────────────────────────────────────────┐
              │ Does NOT enter FAULT state.               │
              │ Transitions RUN → DERATE with reduced     │
              │ I_ref per thermal derate curve.            │
              │ Auto-clears when condition resolves        │
              │ with hysteresis.                           │
              └───────────────────────────────────────────┘
```

---

## 4. Thermal Derate Curves

Thermal derating reduces output power linearly to prevent shutdown. Three independent derate calculations run in parallel; the most restrictive one wins.

### 4.1 SiC Junction Temperature Derate

```
Power (%)
  100 |────────────┐
      |            │
      |             \
      |              \
      |               \
   0  |────────────────\────
      80   90   100  115  °C
                ↑     ↑
          derate  shutdown
          start   threshold
```

| T_SiC (°C) | Output Power (%) |
|------------|-----------------|
| < 100 | 100% |
| 100 – 115 | Linear: 100% → 0% |
| > 115 | 0% (shutdown, fault 0x0F) |

### 4.2 Magnetics Temperature Derate

```
Power (%)
  100 |────────────────┐
      |                │
      |                 \
      |                  \
   0  |──────────────────\────
      100  110  120   140  °C
                 ↑      ↑
           derate  shutdown
```

| T_mag (°C) | Output Power (%) |
|-----------|-----------------|
| < 120 | 100% |
| 120 – 140 | Linear: 100% → 0% |
| > 140 | 0% (shutdown, fault 0x10) |

### 4.3 Ambient Temperature Derate

```
Power (%)
  100 |──────────┐
      |          │
      |           \
      |            \
   50 |             \──────
      |
   0  |────────────────────
      40   50   55    70  °C
              ↑     ↑
        derate  max derate
        start   (50%)
```

| T_amb (°C) | Output Power (%) |
|-----------|-----------------|
| < 55 | 100% |
| 55 – 70 | Linear: 100% → 50% |
| > 70 | 50% (sustained; no shutdown from ambient alone) |

### 4.4 Derate Hysteresis

To prevent oscillation at the derate boundary, a **5°C hysteresis** is applied:
- Enter derate at T_threshold (e.g., 100°C for SiC)
- Exit derate at T_threshold − 5°C (e.g., 95°C for SiC)

---

## 5. Fault Log Structure

### 5.1 Fault Entry

```c
typedef struct __attribute__((packed)) {
    uint32_t timestamp_ms;   /* System tick at fault time (4 bytes) */
    uint8_t  fault_id;       /* Fault ID from registry (1 byte) */
    uint8_t  severity;       /* 0=Critical, 1=Major, 2=Warning (1 byte) */
    uint16_t v_bus_x10;      /* V_bus × 10 at fault time (2 bytes) */
    uint16_t i_out_x10;      /* I_out × 10 at fault time (2 bytes) */
    uint8_t  t_sic;          /* SiC temperature °C (1 byte) */
    uint8_t  retry_count;    /* Retry attempt number (1 byte) */
} FaultLogEntry_t;           /* Total: 12 bytes */
```

### 5.2 Ring Buffer in Flash

| Parameter | Value |
|-----------|-------|
| Entry size | 12 bytes |
| Buffer depth | 256 entries |
| Total flash | 3,072 bytes (3 kB) |
| Flash page | Dedicated 2 kB page × 2 (double-buffered for wear leveling) |
| Write endurance | ~10,000 cycles per page → 2.56 M fault entries lifetime |
| Read-out | CAN diagnostic frame (see [[05-CAN Master and Module Stacking]]) |

```c
#define FAULT_LOG_DEPTH     256
#define FAULT_LOG_FLASH_ADDR  0x0807F000  /* Last 4 kB of 512 kB flash */

typedef struct {
    uint8_t  write_idx;                          /* Next write position */
    uint8_t  count;                              /* Total entries (saturates at 256) */
    FaultLogEntry_t entries[FAULT_LOG_DEPTH];    /* Ring buffer */
} FaultLog_t;

static FaultLog_t g_fault_log;  /* RAM shadow; flushed to flash on write */
```

---

## 6. Pseudocode

### 6.1 `Fault_Enter()`

Called from `App_SM_Run()` when a fault flag is detected.

```c
void Fault_Enter(uint8_t fault_id)
{
    /* 1. Immediate output disable */
    HRTIM_DisableAllOutputs();

    /* 2. Classify severity */
    uint8_t severity = Fault_GetSeverity(fault_id);

    /* 3. Log to ring buffer */
    FaultLogEntry_t entry = {
        .timestamp_ms = HAL_GetTick(),
        .fault_id     = fault_id,
        .severity     = severity,
        .v_bus_x10    = (uint16_t)(ADC_Read_VbusFilt() * 10.0f),
        .i_out_x10    = (uint16_t)(ADC_Read_IoutFilt() * 10.0f),
        .t_sic        = (uint8_t)ADC_Read_TSiC(),
        .retry_count  = g_retry_count,
    };
    FaultLog_Write(&entry);

    /* 4. Broadcast fault on CAN */
    CAN_SendFault(fault_id, severity);

    /* 5. Set state */
    if (severity == 0) {
        /* Critical: latch — no auto-recovery */
        g_fault_latched = true;
        State_Transition(APP_FAULT);
    } else if (severity == 1) {
        /* Major: auto-retry possible */
        g_fault_latched = false;
        g_retry_count++;
        g_fault_cooldown_start = HAL_GetTick();
        State_Transition(APP_FAULT);
    }
    /* severity == 2 (Warning) handled in DERATE, not here */
}
```

### 6.2 `Fault_Recovery_Check()`

Called every 1 kHz tick while in `APP_FAULT` state.

```c
#define FAULT_RETRY_MAX      3
#define FAULT_COOLDOWN_MS    10000   /* 10 seconds */

void Fault_Recovery_Check(void)
{
    /* Latched fault: wait for diagnostic clear command */
    if (g_fault_latched) {
        if (g_can_cmd_pending & CMD_DIAG_CLEAR) {
            g_can_cmd_pending &= ~CMD_DIAG_CLEAR;
            g_fault_latched = false;
            g_retry_count = 0;
            State_Transition(APP_STANDBY);
        }
        return;
    }

    /* Major fault: auto-retry with cooldown */
    uint32_t elapsed = HAL_GetTick() - g_fault_cooldown_start;
    if (elapsed >= FAULT_COOLDOWN_MS) {
        if (g_retry_count <= FAULT_RETRY_MAX) {
            /* Attempt restart from PLL_LOCK */
            PLL_Start();
            State_Transition(APP_PLL_LOCK);
        } else {
            /* Exhausted retries: latch */
            g_fault_latched = true;
            State_Transition(APP_DISABLED);
        }
    }
}
```

### 6.3 `Thermal_Derate_Calc()`

Called every 1 kHz tick while in `APP_DERATE` (or `APP_RUN` to check entry condition).

```c
#define DERATE_HYSTERESIS  5.0f   /* °C hysteresis for exit */

typedef struct {
    float power_limit_pct;     /* 0.0 to 1.0 */
    bool  active;
} DerateState_t;

static DerateState_t g_derate;

float Thermal_Derate_Calc(void)
{
    float t_sic = ADC_Read_TSiC();
    float t_mag = ADC_Read_TMag();
    float t_amb = ADC_Read_TAmb();

    /* SiC derate: 100% at 100°C, 0% at 115°C */
    float pwr_sic = 1.0f;
    if (t_sic > 100.0f) {
        pwr_sic = 1.0f - (t_sic - 100.0f) / 15.0f;
        if (pwr_sic < 0.0f) pwr_sic = 0.0f;
    }

    /* Magnetics derate: 100% at 120°C, 0% at 140°C */
    float pwr_mag = 1.0f;
    if (t_mag > 120.0f) {
        pwr_mag = 1.0f - (t_mag - 120.0f) / 20.0f;
        if (pwr_mag < 0.0f) pwr_mag = 0.0f;
    }

    /* Ambient derate: 100% at 55°C, 50% at 70°C */
    float pwr_amb = 1.0f;
    if (t_amb > 55.0f) {
        pwr_amb = 1.0f - 0.5f * (t_amb - 55.0f) / 15.0f;
        if (pwr_amb < 0.5f) pwr_amb = 0.5f;
    }

    /* Most restrictive wins */
    float power_limit = fminf(pwr_sic, fminf(pwr_mag, pwr_amb));

    /* Check for shutdown conditions */
    if (t_sic > 115.0f) Fault_Enter(FAULT_OTP_SIC);
    if (t_mag > 140.0f) Fault_Enter(FAULT_OTP_MAG);

    g_derate.power_limit_pct = power_limit;
    return power_limit;
}

bool Thermal_Derate_Required(void)
{
    float limit = Thermal_Derate_Calc();
    return (limit < 1.0f);
}

bool Thermal_Derate_Cleared(void)
{
    /* All temperatures below threshold minus hysteresis */
    float t_sic = ADC_Read_TSiC();
    float t_mag = ADC_Read_TMag();
    float t_amb = ADC_Read_TAmb();
    return (t_sic < (100.0f - DERATE_HYSTERESIS)) &&
           (t_mag < (120.0f - DERATE_HYSTERESIS)) &&
           (t_amb < (55.0f  - DERATE_HYSTERESIS));
}

void Thermal_Derate_Apply(void)
{
    float limit = g_derate.power_limit_pct;
    /* Scale current references */
    float i_derated = I_RATED_D * limit;
    __atomic_store_float(&g_id_ref, i_derated);

    float iout_derated = I_OUT_RATED * limit;
    __atomic_store_float(&g_iout_ref, iout_derated);
}
```

---

## 7. Fault Severity Lookup

```c
static const uint8_t fault_severity_table[] = {
    [FAULT_NONE]             = 0xFF,  /* invalid */
    [FAULT_PFC_OCP_HW]       = 0,     /* Critical */
    [FAULT_LLC_OCP_HW]       = 0,
    [FAULT_VBUS_OVP_HW]      = 0,
    [FAULT_VOUT_OVP_HW]      = 0,
    [FAULT_GROUND_FAULT]      = 0,
    [FAULT_PFC_OCP_SW]        = 1,     /* Major */
    [FAULT_LLC_OCP_SW]        = 1,
    [FAULT_VBUS_OVP_SW]       = 1,
    [FAULT_VBUS_UVP]          = 1,
    [FAULT_VOUT_UVP]          = 2,     /* Warning */
    [FAULT_PLL_TIMEOUT]       = 1,
    [FAULT_PFC_START_TIMEOUT] = 1,
    [FAULT_LLC_START_TIMEOUT] = 1,
    [FAULT_SHUTDOWN_TIMEOUT]  = 0,
    [FAULT_OTP_SIC]           = 0,
    [FAULT_OTP_MAG]           = 0,
    [FAULT_OTP_SIC_WARN]      = 2,
    [FAULT_OTP_MAG_WARN]      = 2,
    [FAULT_OTP_AMB_WARN]      = 2,
    [FAULT_CAN_TIMEOUT_50]    = 2,
    [FAULT_CAN_TIMEOUT_200]   = 1,
    [FAULT_CAN_BUSOFF]        = 1,
    [FAULT_AUX_RAIL_UV]       = 0,
    [FAULT_PHASE_LOSS]        = 1,
};

uint8_t Fault_GetSeverity(uint8_t fault_id)
{
    if (fault_id >= sizeof(fault_severity_table)) return 0;  /* default: Critical */
    return fault_severity_table[fault_id];
}
```

---

## 8. CAN Fault Diagnostic Read-Out

The fault log can be read out over CAN using diagnostic frames. See [[05-CAN Master and Module Stacking]] §6 for the full diagnostic frame specification.

**Summary:**
- Request: Master sends `DIAG_READ_FAULT_LOG` with start index
- Response: Module sends 4 entries per frame (48 bytes) until buffer exhausted
- Clear: Master sends `DIAG_CLEAR_FAULTS` to reset the fault log write index

---

## References

- [[06-Firmware Architecture]] — Hardware protection (§7.1), firmware protection (§7.2), ISR timing budget (§3.2)
- [[09-Protection and Safety]] — OVP/OCP/OTP thresholds, insulation coordination, safety compliance
- [[04-Thermal Budget]] — SiC junction temperatures, magnetics temperatures, cooling system design
- [[01-Application State Machine]] — FAULT and DERATE state transitions (this sub-folder)
- [[05-CAN Master and Module Stacking]] — Diagnostic CAN frames (this sub-folder)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 18 faults, 3 derate curves |
