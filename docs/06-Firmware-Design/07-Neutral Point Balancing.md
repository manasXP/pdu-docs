---
tags: [PDU, firmware, Vienna-PFC, neutral-point, balancing, STM32G474]
created: 2026-02-22
---

# 07 – Neutral Point Balancing

> [!note] Scope
> This document covers the **neutral point (NP) voltage balancing algorithm** for the Vienna rectifier DC-link midpoint. For the bus voltage loop structure and NP balance overview, see [[06-Firmware Architecture]] §4.3. For the ADC channels used (V_cap_top, V_cap_bot), see §2.2 of the same document.

---

## 1. Problem Statement

The Vienna rectifier splits the DC bus into two series capacitors (C_top and C_bot), forming a **neutral point (NP)** at their junction. Ideally, V_cap_top = V_cap_bot = V_bus/2. In practice, the midpoint drifts due to:

- **Asymmetric switching**: Unequal duty cycles across phases (manufacturing tolerance, gate driver mismatch)
- **Grid voltage unbalance**: Different phase voltages cause asymmetric current draw
- **Load transients**: Uneven energy extraction from top/bottom halves
- **Capacitor tolerance**: ±20% ESR and capacitance variation between top and bottom caps

**Consequences of NP drift:**
- Increased voltage stress on one capacitor bank (risk of exceeding V_rated)
- Asymmetric device stress (SiC MOSFETs see different blocking voltages)
- Increased even-harmonic distortion in line currents
- Potential saturation of input inductors under heavy unbalance

---

## 2. Sensing

| Signal | ADC | Group | Sample Rate | Resolution |
|--------|-----|-------|-------------|-----------|
| V_cap_top | ADC1 | Regular (DMA) | 1 kHz | 16-bit (HW 16× oversample) |
| V_cap_bot | ADC2 | Regular (DMA) | 1 kHz | 16-bit (HW 16× oversample) |

**Error signal:**

```
V_NP_err = V_cap_top − V_cap_bot
```

- `V_NP_err > 0`: Top capacitor overvoltaged → need to reduce top half charging
- `V_NP_err < 0`: Bottom capacitor overvoltaged → need to reduce bottom half charging

---

## 3. P-Controller Design

A simple proportional controller is sufficient because:
- The plant (capacitor voltage integrator) provides inherent integral action
- PI would risk oscillation at the 300 Hz ripple frequency
- The required bandwidth is low (< 10 Hz)

### 3.1 Control Law

```
d_offset = K_NP × V_NP_err
```

Where:
- `d_offset` is a duty cycle offset added to the zero-sequence component of the SVM modulation
- `K_NP` is the proportional gain (dimensionless: modulation index per volt)

### 3.2 Gain Selection

| Parameter | Minimum | Typical | Maximum |
|-----------|---------|---------|---------|
| K_NP | 0.001 | 0.005 | 0.01 |
| Bandwidth | ~1 Hz | ~5 Hz | ~10 Hz |
| Steady-state error | < 1 V | < 1 V | < 1 V |

**Tuning rationale:**
- K_NP = 0.005: at V_NP_err = 10 V → d_offset = 0.05 (5% modulation adjustment)
- Settling time: ~200 ms for a 20 V step disturbance
- Higher K_NP gives faster response but risks injecting audible harmonics (> 5 Hz bandwidth overlaps with grid frequency harmonics)

---

## 4. Integration with SVM Zero-Sequence Injection

The Space Vector Modulation (SVM) already produces three-phase duty cycles (d_a, d_b, d_c) from the inverse Park transform output. The NP balance offset is added as a **common-mode (zero-sequence) component**:

```
d_a' = d_a + d_offset
d_b' = d_b + d_offset
d_c' = d_c + d_offset
```

This shifts all three phases equally, which:
- Does not affect the differential-mode (line-to-line) output voltages
- Biases the NP current to rebalance the capacitor voltages
- Is equivalent to injecting a zero-sequence voltage

### 4.1 Why Zero-Sequence Works

In a 3-wire system (Vienna rectifier has no neutral return), the zero-sequence component does not flow as line current. Instead, it redistributes charge between C_top and C_bot by biasing which capacitor is charged during each switching interval.

---

## 5. Saturation and Limiting

### 5.1 Modulation Index Clamp

The zero-sequence offset is clamped to prevent over-modulation:

```
d_offset = CLAMP(d_offset, -0.05, +0.05)
```

**±5% of modulation index** is sufficient to correct typical imbalances without affecting THD.

### 5.2 Warning Condition

If the imbalance persists despite maximum correction effort:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| |V_NP_err| > 20 V for > 1 s | Warning | Log event, set LED amber |
| |V_NP_err| > 50 V for > 100 ms | Major fault | → FAULT state (capacitor overstress risk) |

---

## 6. Expected Performance

| Grid Condition | Expected |V_NP_err| | Notes |
|---------------|----------------------|-------|
| Balanced grid (< 2% unbalance) | < 5 V | Well within limits |
| 5% grid voltage unbalance | < 10 V | Normal industrial environment |
| 10% grid voltage unbalance | < 15 V | Weak grid, rural installation |
| Phase loss (one phase missing) | — | Not correctable; PLL detects phase loss → FAULT |
| Capacitor 20% mismatch | < 8 V | Worst-case component tolerance |

---

## 7. Pseudocode: `NP_Balance_Update()`

Called at 1 kHz from the bus voltage background loop (or main loop within `APP_RUN` / `APP_DERATE`).

```c
#define KNP_GAIN           0.005f   /* modulation index per volt */
#define NP_OFFSET_MAX      0.05f    /* ±5% clamp */
#define NP_WARN_THRESHOLD  20.0f    /* V */
#define NP_WARN_TIME_MS    1000     /* 1 s sustained */
#define NP_FAULT_THRESHOLD 50.0f    /* V */
#define NP_FAULT_TIME_MS   100      /* 100 ms sustained */

typedef struct {
    float    d_offset;        /* zero-sequence duty offset */
    float    v_np_err;        /* V_cap_top - V_cap_bot */
    uint32_t warn_timer;      /* timestamp when warning condition started */
    uint32_t fault_timer;     /* timestamp when fault condition started */
} NP_Balance_t;

static NP_Balance_t g_np;

void NP_Balance_Update(void)
{
    /* Read capacitor voltages from DMA buffer (already oversampled) */
    float v_top = ADC_Read_VcapTop();
    float v_bot = ADC_Read_VcapBot();

    /* Compute error */
    g_np.v_np_err = v_top - v_bot;

    /* P-controller */
    g_np.d_offset = KNP_GAIN * g_np.v_np_err;

    /* Clamp */
    if (g_np.d_offset > NP_OFFSET_MAX)  g_np.d_offset = NP_OFFSET_MAX;
    if (g_np.d_offset < -NP_OFFSET_MAX) g_np.d_offset = -NP_OFFSET_MAX;

    /* Export to PFC current ISR (read atomically in SVM) */
    __atomic_store_float(&g_svm_zs_offset, g_np.d_offset);

    /* --- Warning / Fault monitoring --- */
    uint32_t now = HAL_GetTick();
    float abs_err = fabsf(g_np.v_np_err);

    /* Warning: |err| > 20 V for > 1 s */
    if (abs_err > NP_WARN_THRESHOLD) {
        if (g_np.warn_timer == 0) g_np.warn_timer = now;
        if ((now - g_np.warn_timer) > NP_WARN_TIME_MS) {
            EventLog_Write(EVT_NP_IMBALANCE_WARN, (uint16_t)(g_np.v_np_err * 10.0f));
            LED_SetAmber();
        }
    } else {
        g_np.warn_timer = 0;
    }

    /* Fault: |err| > 50 V for > 100 ms */
    if (abs_err > NP_FAULT_THRESHOLD) {
        if (g_np.fault_timer == 0) g_np.fault_timer = now;
        if ((now - g_np.fault_timer) > NP_FAULT_TIME_MS) {
            Fault_Enter(FAULT_NP_IMBALANCE);  /* → FAULT state */
        }
    } else {
        g_np.fault_timer = 0;
    }
}
```

### 7.1 Integration in PFC Current ISR

The zero-sequence offset is applied inside the SVM calculation:

```c
/* Inside PFC_dq_Control(), after inverse Park transform: */
void SVM_ApplyZeroSequence(float *da, float *db, float *dc)
{
    float zs = __atomic_load_float(&g_svm_zs_offset);
    *da += zs;
    *db += zs;
    *dc += zs;

    /* Clamp individual duties to [0, 1] */
    *da = CLAMP(*da, 0.0f, 1.0f);
    *db = CLAMP(*db, 0.0f, 1.0f);
    *dc = CLAMP(*dc, 0.0f, 1.0f);
}
```

---

## References

- [[06-Firmware Architecture]] — Bus voltage loop and NP balance overview (§4.3), ADC allocation for V_cap_top/V_cap_bot (§2.2)
- [[01-Topology Selection]] — Vienna rectifier midpoint topology
- [[04-Thermal Budget]] — Capacitor temperature and ESR derating
- [[01-Application State Machine]] — APP_RUN state where NP balance runs (this sub-folder)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
