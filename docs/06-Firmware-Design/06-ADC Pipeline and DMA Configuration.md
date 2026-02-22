---
tags: [PDU, firmware, ADC, DMA, oversampling, filter, STM32G474, HRTIM]
created: 2026-02-22
---

# 06 – ADC Pipeline and DMA Configuration

> [!note] Scope
> This document covers **ADC DMA buffer layout, hardware oversampling configuration, software filter chains, FMAC co-processor offload, and trigger routing**. For the ADC signal list, channel allocation, and sampling rate requirements, see [[06-Firmware Architecture]] §2. For ADC errata workarounds, see §2.3 of the same document.

---

## 1. Two-Path ADC Architecture

The STM32G474 ADC subsystem is split into two distinct paths to satisfy the conflicting requirements of high-speed control feedback and low-speed monitoring.

```
┌────────────────────────────────────────────────────────────────────┐
│                     HIGH-SPEED PATH                                │
│                   (Injected Groups)                                │
│                                                                    │
│  HRTIM CMP/PER event ──→ ADC1..5 Injected Trigger                │
│                            │                                       │
│                            ▼                                       │
│                    Injected conversion (1–4 channels)              │
│                            │                                       │
│                            ▼                                       │
│                    JDRx register ──→ ISR direct read (~200 ns)    │
│                    (no DMA)                                        │
│                            │                                       │
│                            ▼                                       │
│                    Control ISR (PFC current loop, LLC voltage)      │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│                      LOW-SPEED PATH                                │
│                    (Regular Groups)                                 │
│                                                                    │
│  HRTIM Master rate-div ──→ ADC1..5 Regular Trigger                │
│                              │                                     │
│                              ▼                                     │
│                    Regular scan (multi-channel)                    │
│                              │                                     │
│                              ▼                                     │
│                    DMA circular double-buffer ──→ RAM              │
│                              │                                     │
│                              ▼                                     │
│                    Background task (1 kHz) reads DMA buffer       │
│                    Applies SW filters (EMA, biquad IIR)            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Injected Group (High-Speed, No DMA)

### 2.1 Rationale

Injected conversions are read directly from `JDRx` registers inside the HRTIM ISR. DMA is not used because:
- ISR execution is deterministic (< 3 us)
- JDR registers are double-buffered in hardware (no race condition)
- DMA interrupt latency would add ~500 ns jitter

### 2.2 ISR Read Sequence

```c
/* PFC Current Control ISR — triggered by HRTIM Timer A CMP2 (center of PWM) */
void PFC_CurrentControl_ISR(void)
{
    /* Direct register reads — ~200 ns total for 7 channels */
    float ia = (float)LL_ADC_INJ_ReadConversionData12(ADC1, LL_ADC_INJ_RANK_1) * ADC_TO_AMPS;
    float ib = (float)LL_ADC_INJ_ReadConversionData12(ADC2, LL_ADC_INJ_RANK_1) * ADC_TO_AMPS;
    float ic = (float)LL_ADC_INJ_ReadConversionData12(ADC3, LL_ADC_INJ_RANK_1) * ADC_TO_AMPS;

    float vbus = (float)LL_ADC_INJ_ReadConversionData12(ADC1, LL_ADC_INJ_RANK_2) * ADC_TO_VBUS;
    float va   = (float)LL_ADC_INJ_ReadConversionData12(ADC2, LL_ADC_INJ_RANK_2) * ADC_TO_VGRID;
    float vb   = (float)LL_ADC_INJ_ReadConversionData12(ADC3, LL_ADC_INJ_RANK_2) * ADC_TO_VGRID;
    float vc   = (float)LL_ADC_INJ_ReadConversionData12(ADC4, LL_ADC_INJ_RANK_1) * ADC_TO_VGRID;

    /* Clarke → Park → PI → Inverse Park → SVM → HRTIM update */
    PFC_dq_Control(ia, ib, ic, va, vb, vc, vbus);
}
```

### 2.3 Injected Channel Summary

| ADC Instance | INJ Rank 1 | INJ Rank 2 | Trigger Source |
|-------------|-----------|-----------|---------------|
| ADC1 | I_A (phase current) | V_DC_bus | HRTIM TRG1 (Timer A CMP2) |
| ADC2 | I_B | V_A (grid) | HRTIM TRG1 (simultaneous with ADC1) |
| ADC3 | I_C | V_B (grid) | HRTIM TRG2 (Timer B CMP2) |
| ADC4 | V_C (grid) | V_out | HRTIM TRG3 (Timer D PER) |
| ADC5 | I_out | — | HRTIM TRG3 (simultaneous with ADC4) |

---

## 3. Regular Group (Low-Speed, DMA)

### 3.1 DMA Channel Mapping

| ADC | DMA Controller | DMA Channel | Stream | Priority |
|-----|---------------|-------------|--------|----------|
| ADC1 REG | DMA1 | CH1 | — | Medium |
| ADC2 REG | DMA1 | CH2 | — | Medium |
| ADC3 REG | DMA2 | CH1 | — | Low |
| ADC4 REG | DMA2 | CH2 | — | Low |
| ADC5 REG | DMA2 | CH3 | — | Low |

### 3.2 Circular Double-Buffer Configuration

Each ADC regular group uses a circular DMA buffer with double-buffering (half-transfer + transfer-complete interrupts) to allow the background task to process one half while DMA fills the other.

```c
#define ADC_REG_CHANNELS_PER_INST  4    /* max regular channels per ADC */
#define ADC_REG_OVERSAMPLE_DEPTH   16   /* hardware oversampling ratio */
#define ADC_DMA_HALF_DEPTH         8    /* samples per half-buffer */
#define ADC_DMA_BUFFER_DEPTH       (ADC_DMA_HALF_DEPTH * 2)  /* 16 samples */

/* Buffer sizing per ADC instance:
 * 4 channels × 16 samples × 2 bytes (uint16_t) = 128 bytes per instance
 * Total across 5 instances: 640 bytes
 * With oversampling: effective data is 16-bit, stored as uint16_t */

static uint16_t adc1_dma_buf[ADC_REG_CHANNELS_PER_INST * ADC_DMA_BUFFER_DEPTH];
static uint16_t adc2_dma_buf[ADC_REG_CHANNELS_PER_INST * ADC_DMA_BUFFER_DEPTH];
/* ... same for ADC3, ADC4, ADC5 */
```

**Total DMA buffer: 5 × 128 = 640 bytes** (negligible RAM usage on 128 kB SRAM)

### 3.3 Regular Channel Assignment

| ADC | REG Channel | Signal | Oversample | Effective Rate |
|-----|------------|--------|-----------|---------------|
| ADC1 | CH_A | V_cap_top | 16× | 1 kHz |
| ADC2 | CH_A | V_cap_bot | 16× | 1 kHz |
| ADC3 | CH_A | V_aux_12V | 16× | 100 Hz |
| ADC4 | CH_A | T_SiC_PFC | 16× | 100 Hz |
| ADC4 | CH_B | T_magnetics | 16× | 100 Hz |
| ADC5 | CH_A | T_SiC_LLC | 16× | 100 Hz |
| ADC5 | CH_B | T_ambient | 16× | 10 Hz |

---

## 4. Hardware Oversampling

The STM32G474 ADC hardware oversampler accumulates N conversions and right-shifts the result, providing effective resolution beyond 12 bits without CPU overhead.

### 4.1 Configuration

| Parameter | Value | Register |
|-----------|-------|----------|
| Oversampling ratio | 16× | `ADCx_CFGR2.OVSR` = 0b0011 |
| Right shift | 4 bits | `ADCx_CFGR2.OVSS` = 0b0100 |
| Effective resolution | 16-bit (12 + 4 from averaging) | — |
| Triggered mode | Single trigger starts all 16 accumulations | `ADCx_CFGR2.TROVS` = 0 |

### 4.2 Effective ENOB Improvement

| Oversampling Ratio | Additional Bits | Effective ENOB | Conversion Time (at 4 MHz ADC clock) |
|-------------------|----------------|----------------|--------------------------------------|
| 1× (none) | 0 | ~10.5 | 0.25 us |
| 4× | 1 | ~11.5 | 1.0 us |
| 16× | 2 | ~12.5 | 4.0 us |
| 256× | 4 | ~14.5 | 64 us |

16× is the best trade-off for NTC and auxiliary signals: 4 us conversion time at 100 Hz rate is negligible, and 12.5 ENOB provides ±0.3°C temperature resolution with typical NTC divider.

### 4.3 Configuration Code

```c
void ADC_Oversampling_Config(ADC_TypeDef *adc, uint32_t ratio, uint32_t shift)
{
    /* Disable ADC before configuration */
    LL_ADC_Disable(adc);
    while (LL_ADC_IsEnabled(adc)) {}

    /* Enable oversampling on regular group only (not injected) */
    MODIFY_REG(adc->CFGR2,
        ADC_CFGR2_ROVSE | ADC_CFGR2_OVSR | ADC_CFGR2_OVSS | ADC_CFGR2_TROVS,
        ADC_CFGR2_ROVSE |                  /* Enable regular oversampling */
        (ratio << ADC_CFGR2_OVSR_Pos) |    /* Ratio: 0b0011 = 16× */
        (shift << ADC_CFGR2_OVSS_Pos) |    /* Shift: 4 bits right */
        0);                                 /* TROVS=0: all in one trigger */
}
```

---

## 5. Software Filter Chains

### 5.1 Bus Voltage Biquad IIR (100 Hz Butterworth)

Applied to V_DC_bus in the 1 kHz bus voltage ISR to reject 300 Hz ripple (6-pulse rectifier ripple at 3× grid frequency).

**Design:**
- Type: 2nd-order Butterworth low-pass
- Cutoff: 100 Hz
- Sample rate: 1 kHz (bus voltage ISR)
- 300 Hz attenuation: −18 dB

**Coefficients** (Direct Form II Transposed):

```
Transfer function: H(z) = (b0 + b1*z^-1 + b2*z^-2) / (1 + a1*z^-1 + a2*z^-2)

  b0 =  0.06745527f
  b1 =  0.13491055f
  b2 =  0.06745527f
  a1 = -1.14298050f
  a2 =  0.41280160f
```

```c
typedef struct {
    float b0, b1, b2;
    float a1, a2;
    float z1, z2;    /* state variables (Direct Form II Transposed) */
} Biquad_t;

float Biquad_Update(Biquad_t *f, float x)
{
    float y = f->b0 * x + f->z1;
    f->z1 = f->b1 * x - f->a1 * y + f->z2;
    f->z2 = f->b2 * x - f->a2 * y;
    return y;
}

/* Initialization */
static Biquad_t g_vbus_filter = {
    .b0 =  0.06745527f,
    .b1 =  0.13491055f,
    .b2 =  0.06745527f,
    .a1 = -1.14298050f,
    .a2 =  0.41280160f,
    .z1 = 0.0f, .z2 = 0.0f,
};
```

### 5.2 Temperature EMA (Exponential Moving Average)

Applied to all NTC temperature readings in the 100 Hz background task.

```c
#define TEMP_EMA_ALPHA  0.01f   /* tau ≈ 1/alpha × T_s = 1 s at 100 Hz */

float Temp_EMA_Update(float *state, float new_sample)
{
    *state = TEMP_EMA_ALPHA * new_sample + (1.0f - TEMP_EMA_ALPHA) * (*state);
    return *state;
}
```

| Parameter | Value |
|-----------|-------|
| Alpha | 0.01 |
| Sample rate | 100 Hz |
| Time constant | ~1 s |
| Settling time (2%) | ~4 s |

This is appropriate for NTC thermal response (thermal time constant of heatsink is 10–30 s).

### 5.3 LLC Output Voltage 1st-Order IIR

Applied to V_out in the LLC voltage ISR at 20 kHz. Faster than the bus voltage filter because the LLC CV loop bandwidth is 500 Hz–2 kHz.

```c
#define VOUT_IIR_ALPHA   0.3f   /* fc ≈ alpha × fs / (2*pi) ≈ 955 Hz */

float Vout_IIR_Update(float *state, float x)
{
    *state = VOUT_IIR_ALPHA * x + (1.0f - VOUT_IIR_ALPHA) * (*state);
    return *state;
}
```

| Parameter | Value |
|-----------|-------|
| Alpha | 0.3 |
| Sample rate | 20 kHz |
| Effective cutoff | ~955 Hz |
| 10 kHz attenuation | −20 dB |

---

## 6. FMAC Co-Processor Offload

The STM32G474 **FMAC (Filter Mathematical Accelerator)** can run IIR/FIR filters autonomously, freeing the CPU. It is used for the bus voltage biquad filter.

### 6.1 FMAC Configuration

| Parameter | Value |
|-----------|-------|
| Filter type | IIR (biquad, order 2) |
| Input buffer | X1 (8 entries, DMA-fed from ADC1 regular group) |
| Coefficient buffer | X2 (5 entries: b0, b1, b2, a1, a2) |
| Output buffer | Y (8 entries, DMA to RAM) |
| Trigger | Software (called from 1 kHz ISR) |

### 6.2 FMAC vs. CPU Comparison

| Method | Execution Time | CPU Cycles |
|--------|---------------|------------|
| CPU biquad (float32) | ~150 ns | ~25 cycles |
| FMAC (q1.15 fixed-point) | ~60 ns | 0 (DMA) |

The saving is modest for a single biquad, but scales if multiple filters are chained or if the CPU is near its ISR budget limit.

---

## 7. ADC Trigger Routing Map

Complete mapping of HRTIM ADC trigger events to ADC instances and conversion groups.

| HRTIM Trigger | Source Event | ADC Target | Group | Purpose |
|--------------|-------------|-----------|-------|---------|
| ADC1TRG1 | Timer A CMP2 (PER/2) | ADC1, ADC2 | Injected | PFC phase A/B currents, V_bus, V_A |
| ADC1TRG2 | Timer B CMP2 (PER/2) | ADC3 | Injected | PFC phase C current, V_B |
| ADC1TRG3 | Timer C CMP2 (PER/2) | ADC4 | Injected | V_C (grid voltage) |
| ADC2TRG1 | Timer D PER (LLC period) | ADC4, ADC5 | Injected | V_out, I_out |
| ADC2TRG2 | Timer D CMP2 | ADC1, ADC2, ADC3 | Injected | I_LLC_ph1/2/3 (resonant currents) |
| ADC2TRG3 | Master CMP4 (rate-divided) | ADC3, ADC4, ADC5 | Regular | Temperatures, V_aux (DMA) |

### 7.1 Trigger Routing Initialization

```c
void ADC_TriggerRouting_Init(void)
{
    /* PFC current sampling: Timer A CMP2 triggers ADC1/ADC2 injected */
    LL_ADC_INJ_SetTriggerSource(ADC1, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG1);
    LL_ADC_INJ_SetTriggerSource(ADC2, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG1);
    LL_ADC_INJ_SetTriggerEdge(ADC1, LL_ADC_INJ_TRIG_EXT_RISING);
    LL_ADC_INJ_SetTriggerEdge(ADC2, LL_ADC_INJ_TRIG_EXT_RISING);

    /* PFC phase C: Timer B CMP2 triggers ADC3 injected */
    LL_ADC_INJ_SetTriggerSource(ADC3, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG2);
    LL_ADC_INJ_SetTriggerEdge(ADC3, LL_ADC_INJ_TRIG_EXT_RISING);

    /* Grid V_C: Timer C CMP2 triggers ADC4 injected */
    LL_ADC_INJ_SetTriggerSource(ADC4, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG3);
    LL_ADC_INJ_SetTriggerEdge(ADC4, LL_ADC_INJ_TRIG_EXT_RISING);

    /* LLC output: Timer D PER triggers ADC4/ADC5 injected */
    LL_ADC_INJ_SetTriggerSource(ADC4, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG4);
    LL_ADC_INJ_SetTriggerSource(ADC5, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG4);

    /* Slow signals: Master CMP4 triggers ADC3/4/5 regular (DMA) */
    LL_ADC_REG_SetTriggerSource(ADC3, LL_ADC_REG_TRIG_EXT_HRTIM_TRG5);
    LL_ADC_REG_SetTriggerSource(ADC4, LL_ADC_REG_TRIG_EXT_HRTIM_TRG5);
    LL_ADC_REG_SetTriggerSource(ADC5, LL_ADC_REG_TRIG_EXT_HRTIM_TRG5);
}
```

---

## 8. ES0430 Errata Workaround

STM32G4 errata **ES0430** (section 2.5.x) documents an issue where **intermixing regular and injected conversions on the same ADC instance with DMA can cause data corruption**.

### 8.1 Workaround Strategy

The allocation in [[06-Firmware Architecture]] §2.2 already separates concerns:
- **ADC1/ADC2**: Both injected (PFC currents, V_bus, V_grid) and regular (V_cap_top/bot) are used, but regular uses DMA while injected does not
- **Mitigation**: Regular group conversions are triggered at a much lower rate (1 kHz) than injected (48–65 kHz), and the DMA transfer completes well before the next injected trigger

Additional safeguard in firmware:

```c
/* Disable regular group during injected burst to avoid overlap */
void ADC_SafeRegularStart(ADC_TypeDef *adc)
{
    /* Wait for any pending injected conversion to complete */
    while (LL_ADC_IsActiveFlag_JEOS(adc) == 0 && LL_ADC_INJ_IsConversionOngoing(adc)) {}

    /* Start regular group conversion (DMA will handle the rest) */
    LL_ADC_REG_StartConversion(adc);
}
```

### 8.2 Alternative: Dedicated ADC Instances

For maximum robustness, a future revision could dedicate ADC instances:
- ADC1, ADC2, ADC3: Injected only (control feedback)
- ADC4, ADC5: Regular + DMA only (monitoring)

This eliminates the errata risk entirely but requires remapping some channels.

---

## 9. DMA Initialization Pseudocode

```c
void ADC_DMA_Init(void)
{
    /* --- DMA1 Channel 1: ADC1 Regular Group --- */
    LL_DMA_SetDataTransferDirection(DMA1, LL_DMA_CHANNEL_1,
                                    LL_DMA_DIRECTION_PERIPH_TO_MEMORY);
    LL_DMA_SetMode(DMA1, LL_DMA_CHANNEL_1, LL_DMA_MODE_CIRCULAR);
    LL_DMA_SetPeriphAddress(DMA1, LL_DMA_CHANNEL_1, (uint32_t)&ADC1->DR);
    LL_DMA_SetMemoryAddress(DMA1, LL_DMA_CHANNEL_1, (uint32_t)adc1_dma_buf);
    LL_DMA_SetDataLength(DMA1, LL_DMA_CHANNEL_1,
                         ADC_REG_CHANNELS_PER_INST * ADC_DMA_BUFFER_DEPTH);
    LL_DMA_SetPeriphSize(DMA1, LL_DMA_CHANNEL_1, LL_DMA_PDATAALIGN_HALFWORD);
    LL_DMA_SetMemorySize(DMA1, LL_DMA_CHANNEL_1, LL_DMA_MDATAALIGN_HALFWORD);
    LL_DMA_EnableIT_HT(DMA1, LL_DMA_CHANNEL_1);  /* Half-transfer interrupt */
    LL_DMA_EnableIT_TC(DMA1, LL_DMA_CHANNEL_1);  /* Transfer-complete interrupt */
    LL_DMA_EnableChannel(DMA1, LL_DMA_CHANNEL_1);

    /* --- DMA1 Channel 2: ADC2 Regular Group --- */
    /* (Same pattern as above, different addresses) */

    /* --- DMA2 Channels 1-3: ADC3, ADC4, ADC5 Regular Groups --- */
    /* (Same pattern) */

    /* Enable DMA request on each ADC regular group */
    LL_ADC_REG_SetDMATransfer(ADC1, LL_ADC_REG_DMA_TRANSFER_UNLIMITED);
    LL_ADC_REG_SetDMATransfer(ADC2, LL_ADC_REG_DMA_TRANSFER_UNLIMITED);
    LL_ADC_REG_SetDMATransfer(ADC3, LL_ADC_REG_DMA_TRANSFER_UNLIMITED);
    LL_ADC_REG_SetDMATransfer(ADC4, LL_ADC_REG_DMA_TRANSFER_UNLIMITED);
    LL_ADC_REG_SetDMATransfer(ADC5, LL_ADC_REG_DMA_TRANSFER_UNLIMITED);
}
```

---

## References

- [[06-Firmware Architecture]] — ADC signal list (§2.2), ADC triggering (§2.3), errata note (§2.3), ISR timing budget (§3.2)
- ST AN5346 — STM32G4 ADC Use Tips and Recommendations
- ST ES0430 — STM32G474 Errata Sheet
- ST RM0440 — STM32G4 Reference Manual, ADC and DMA chapters

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
