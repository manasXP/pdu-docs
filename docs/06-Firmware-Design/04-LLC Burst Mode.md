---
tags: [PDU, firmware, LLC, burst-mode, HRTIM, light-load, STM32G474]
created: 2026-02-22
---

# 04 – LLC Burst Mode

> [!note] Scope
> This document covers the **light-load burst mode algorithm** for the 3-phase interleaved LLC converter. For LLC variable-frequency control and HRTIM period register usage, see [[06-Firmware Architecture]] §5. For the overall application state machine (burst mode runs as a sub-state within `APP_RUN`), see [[01-Application State Machine]].

---

## 1. Problem Statement

Below ~10% load (< 3 kW), the LLC frequency must rise significantly above resonance to reduce gain. At very light loads:
- Switching frequency approaches the 300 kHz ceiling
- Switching losses dominate (no longer negligible vs. load)
- Efficiency drops from >96% to <80% at 1 kW without burst mode
- Gate drive and core losses become the primary loss contributors

Burst mode periodically disables switching, reducing average switching events by 70–90%.

---

## 2. Burst Mode Sub-States

Burst mode is a sub-state machine within `APP_RUN`. It does not change the top-level application state.

```
                      ┌─────────────────────────────────────────────┐
                      │                  APP_RUN                    │
                      │                                             │
                      │   ┌────────────────┐                        │
                      │   │ BURST_INACTIVE │  (normal PFM control)  │
                      │   └───────┬────────┘                        │
                      │           │ f_sw > 280 kHz for > 50 ms     │
                      │           v                                 │
                      │   ┌────────────────┐                        │
                      │   │   BURST_RUN    │  (HRTIM burst active)  │
                      │   │                │                        │
                      │   │  switching ON  │                        │
                      │   └───────┬────────┘                        │
                      │           │ V_out > V_target + 2 V         │
                      │           v                                 │
                      │   ┌────────────────┐                        │
                      │   │   BURST_IDLE   │  (outputs idle)        │
                      │   │                │                        │
                      │   │  V_out monitor │                        │
                      │   │  at 20 kHz     │                        │
                      │   └───────┬────────┘                        │
                      │           │ V_out < V_target − 5 V         │
                      │           │ OR dI/dt > 2 A/ms (load step)  │
                      │           v                                 │
                      │   ┌────────────────┐                        │
                      │   │   BURST_RUN    │                        │
                      │   └────────────────┘                        │
                      │                                             │
                      │   Exit burst: f_sw demand < 270 kHz        │
                      │   → back to BURST_INACTIVE                  │
                      └─────────────────────────────────────────────┘
```

### 2.1 State Transitions

| Source | Condition | Target | Action |
|--------|-----------|--------|--------|
| BURST_INACTIVE | f_sw > 280 kHz for > 50 ms | BURST_RUN | Enable HRTIM burst mode controller |
| BURST_RUN | V_out > V_target + 2 V | BURST_IDLE | HRTIM outputs → idle level |
| BURST_IDLE | V_out < V_target − 5 V | BURST_RUN | Resume switching |
| BURST_IDLE | dI/dt > 2 A/ms (load step) | BURST_RUN | Fast exit for load transient |
| BURST_RUN / BURST_IDLE | f_sw demand < 270 kHz | BURST_INACTIVE | Disable HRTIM burst, return to normal PFM |

### 2.2 Entry/Exit Hysteresis

| Parameter | Value |
|-----------|-------|
| Burst entry frequency | > 280 kHz sustained for 50 ms |
| Burst exit frequency | < 270 kHz (10 kHz hysteresis band) |
| V_out upper threshold (RUN → IDLE) | V_target + 2 V |
| V_out lower threshold (IDLE → RUN) | V_target − 5 V |
| Load transient detection | dI/dt > 2 A/ms |

---

## 3. HRTIM Burst Mode Register Configuration

The STM32G474 HRTIM includes a dedicated **Burst Mode Controller (BMC)** that can gate timer outputs without modifying the timer configuration.

### 3.1 Register Map

| Register | Field | Value | Description |
|----------|-------|-------|-------------|
| `HRTIM_BMCR` | `BME` | 1 | Burst Mode Enable |
| `HRTIM_BMCR` | `BMOM` | 0 | Single-shot mode (FW controls run/idle) |
| `HRTIM_BMCR` | `BMCLK` | 0b0000 | Master timer clock (prescaled) |
| `HRTIM_BMCR` | `BMPRSC` | 0b0100 | Prescaler /16 (master at 170 MHz/16 = 10.625 MHz) |
| `HRTIM_BMCR` | `BMPREN` | 1 | Preload enable for BMPER/BMCMPR |
| `HRTIM_BMPER` | `BMPER[15:0]` | Calculated | Burst period register |
| `HRTIM_BMCMPR` | `BMCMP[15:0]` | Calculated | Burst compare (on-time) |
| `HRTIM_BMTRGR` | `SW` | 1 | Software trigger to start burst |

### 3.2 Burst Period and Duty Cycle

The burst controller operates at a much lower frequency than the LLC switching:

```
Burst frequency: 10–50 kHz (adjustable by outer voltage loop)
  BMPER = f_burst_clk / f_burst
        = 10,625,000 / 20,000 = 531 (for 20 kHz burst)

Burst duty cycle: sets average power delivery
  BMCMPR = BMPER × duty_burst
         = 531 × 0.3 = 159 (for 30% burst duty)
```

During the **burst ON** window, all LLC timers (D, E, F) switch normally at their configured PFM frequency. During the **burst OFF** window, outputs are forced to their idle level (low).

### 3.3 Configuration Pseudocode

```c
void HRTIM_BurstMode_Config(float f_burst, float duty_burst)
{
    /* Burst mode clock: Master timer / 16 = 10.625 MHz */
    const uint32_t f_burst_clk = 170000000UL / 16;

    uint16_t bmper = (uint16_t)(f_burst_clk / f_burst);
    uint16_t bmcmpr = (uint16_t)(bmper * duty_burst);

    /* Clamp minimum on-time (at least 5 LLC switching cycles) */
    uint16_t min_on = (uint16_t)(f_burst_clk / g_llc_fsw * 5);
    if (bmcmpr < min_on) bmcmpr = min_on;

    /* Configure burst mode controller */
    HRTIM1->sCommonRegs.BMCR = 0;  /* Disable before config */
    HRTIM1->sCommonRegs.BMPER = bmper;
    HRTIM1->sCommonRegs.BMCMPR = bmcmpr;

    HRTIM1->sCommonRegs.BMCR =
        HRTIM_BMCR_BME       |   /* Enable */
        (0b0100 << HRTIM_BMCR_BMPRSC_Pos) |  /* /16 prescaler */
        HRTIM_BMCR_BMPREN;       /* Preload enable */

    /* Burst mode triggers Timer D, E, F outputs only */
    HRTIM1->sCommonRegs.BMTRGR = HRTIM_BMTRGR_SW;  /* Software trigger */
}
```

---

## 4. Integrator Freeze During Idle

During the burst IDLE window, the LLC voltage/current PI integrators must be frozen. Otherwise, the integrator winds up during the idle period (seeing error accumulate with no control action), causing an overshoot on the next burst RUN.

```c
/* In LLC voltage control ISR */
void LLC_VoltageControl_ISR(void)
{
    float vout = ADC_Read_Vout_Inj();
    float error = g_vout_ref - vout;

    if (g_burst_state == BURST_IDLE) {
        /* Freeze integrator — proportional path still active for
         * monitoring, but don't accumulate integral */
        /* Optionally: slow decay to prevent stale integrator
         *   pi.integrator *= 0.999f;  (tau ~ 1 s at 20 kHz)
         */
        return;  /* Don't update PERxR during idle */
    }

    /* Normal PI update */
    g_llc_pi.integrator += g_llc_pi.Ki * error * dt;
    float output = g_llc_pi.Kp * error + g_llc_pi.integrator;

    /* Clamp to frequency range */
    output = CLAMP(output, F_SW_MIN, F_SW_MAX);
    HRTIM_SetPeriod_Hz_AllLLC(output);
}
```

---

## 5. Load Detection During Idle

During burst IDLE, the output capacitor discharges into the load. The firmware monitors V_out at the LLC ISR rate (up to 20 kHz via ADC4 injected group) for fast load transient detection.

| Detection Method | Threshold | Response Time |
|-----------------|-----------|---------------|
| V_out absolute drop | V_out < V_target − 5 V | 1 sample (50 us at 20 kHz) |
| dI/dt estimation | dV_out/dt × C_out > 2 A/ms | 2 samples (differentiate V_out) |
| V_out large drop (10 V) | V_out < V_target − 10 V | 1 sample → immediate burst exit |

```c
void Burst_LoadDetect(float vout, float vout_prev)
{
    /* Absolute voltage drop */
    if (vout < g_vout_target - 5.0f) {
        g_burst_state = BURST_RUN;
        HRTIM_BurstMode_ForceRun();
        return;
    }

    /* dI/dt estimation: dV/dt * C_out */
    float dvdt = (vout - vout_prev) * g_llc_sample_rate;  /* V/s */
    float di_est = fabsf(dvdt) * C_OUT;                    /* A/s */
    if (di_est > 2.0f) {  /* 2 A/ms = 2000 A/s */
        g_burst_state = BURST_RUN;
        HRTIM_BurstMode_ForceRun();
    }
}
```

---

## 6. Efficiency vs. Ripple Trade-Off

| Load (kW) | Without Burst | With Burst (20 kHz, 30%) | Output Ripple (pk-pk) |
|-----------|--------------|--------------------------|----------------------|
| 1.0 (3%) | ~75% | ~88% | ~8 V (1.1% at 750 V) |
| 2.0 (7%) | ~82% | ~91% | ~5 V (0.7%) |
| 3.0 (10%) | ~88% | ~93% | ~3 V (0.4%) |

> [!tip] Ripple management
> At 1 kW burst mode, the 8 V peak-to-peak ripple is within the 0.5% RMS spec (≈2.3 V RMS at 750 V target). If ripple is too high, increase burst frequency (30–50 kHz) at the cost of slightly lower efficiency.

---

## 7. Pseudocode: `Burst_Mode_Tick()`

Called at 1 kHz from main loop while in `APP_RUN` state.

```c
typedef enum {
    BURST_INACTIVE = 0,
    BURST_RUN      = 1,
    BURST_IDLE     = 2,
} BurstState_t;

typedef struct {
    BurstState_t state;
    uint32_t     entry_timer;       /* ms timestamp for entry condition */
    float        f_burst;           /* burst repetition frequency (Hz) */
    float        duty_burst;        /* burst on-duty (0..1) */
} BurstMode_t;

static BurstMode_t g_burst;

#define BURST_ENTRY_FREQ     280000.0f   /* Hz */
#define BURST_EXIT_FREQ      270000.0f   /* Hz */
#define BURST_ENTRY_TIME_MS  50          /* sustained above threshold */
#define BURST_VOUT_UPPER     2.0f        /* V above target → go idle */
#define BURST_VOUT_LOWER     5.0f        /* V below target → resume */

void Burst_Mode_Tick(void)
{
    float f_sw = LLC_GetCurrentFreq();
    float vout = ADC_Read_VoutFilt();

    switch (g_burst.state) {

    case BURST_INACTIVE:
        /* Check entry condition: high frequency sustained */
        if (f_sw > BURST_ENTRY_FREQ) {
            if (g_burst.entry_timer == 0)
                g_burst.entry_timer = HAL_GetTick();
            else if ((HAL_GetTick() - g_burst.entry_timer) > BURST_ENTRY_TIME_MS) {
                /* Enter burst mode */
                g_burst.state = BURST_RUN;
                g_burst.f_burst = 20000.0f;   /* Start at 20 kHz burst */
                g_burst.duty_burst = 0.5f;     /* 50% initial duty */
                HRTIM_BurstMode_Config(g_burst.f_burst, g_burst.duty_burst);
            }
        } else {
            g_burst.entry_timer = 0;
        }
        break;

    case BURST_RUN:
        /* Check if output voltage has risen enough to idle */
        if (vout > g_vout_target + BURST_VOUT_UPPER) {
            g_burst.state = BURST_IDLE;
            HRTIM_BurstMode_ForceIdle();
            LLC_PI_Freeze();
        }
        /* Check exit condition: load increased */
        if (f_sw < BURST_EXIT_FREQ) {
            g_burst.state = BURST_INACTIVE;
            HRTIM_BurstMode_Disable();
            LLC_PI_Unfreeze();
        }
        break;

    case BURST_IDLE:
        /* Load detection runs in LLC ISR at 20 kHz (see §5) */
        /* Here we handle the slow exit path */
        if (vout < g_vout_target - BURST_VOUT_LOWER) {
            g_burst.state = BURST_RUN;
            HRTIM_BurstMode_ForceRun();
            LLC_PI_Unfreeze();
        }
        /* Adjust burst duty based on how long idle lasts */
        /* (outer regulation: more idle → reduce duty next cycle) */
        break;
    }
}
```

---

## References

- [[06-Firmware Architecture]] — LLC frequency control (§5.1), HRTIM period register (§5.1), burst mode overview (§5.4), HRTIM half mode (§1.2)
- [[01-Topology Selection]] — LLC resonant frequency (f_r ≈ 150.5 kHz), operating range (100–300 kHz)
- [[01-Application State Machine]] — APP_RUN state (this sub-folder)
- ST AN4539 — HRTIM Cookbook, burst mode controller section

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
