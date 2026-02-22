---
tags: [PDU, firmware, STM32G474, HRTIM, Vienna-PFC, LLC, control]
created: 2026-02-22
---

# 06 – Firmware Architecture: STM32G474RE Control of Vienna PFC + 3-Phase Interleaved LLC

This document covers the complete firmware design for the 30 kW PDU using the STM32G474RE MCU to control a Vienna rectifier PFC front-end followed by a 3-phase interleaved LLC DC-DC stage.

---

## 1. STM32G474RE HRTIM Resource Map

### 1.1 HRTIM Architecture

The STM32G474RE includes **HRTIM v2**, running at 170 MHz system clock with an internal DLL at **5.44 GHz**, providing a minimum resolution of **184 ps**.

| Parameter | Value |
|---|---|
| System clock | 170 MHz |
| HRTIM DLL clock | 5.44 GHz |
| Minimum resolution | 184 ps |
| Timer units | 1 Master + 6 Slave (A, B, C, D, E, F) |
| Total PWM outputs | 12 (2 per slave timer: Tx1, Tx2) |
| Fault inputs | 5 (FLT1–FLT5) |
| ADC trigger events | 10 (ADC1TRGx, configurable per timer event) |

> [!note] Resolution calculation
> At 170 MHz PLL input, HRTIM DLL = 32 × 170 MHz = 5.44 GHz → period = 184 ps. Compare to a standard 16-bit timer at 170 MHz (5.88 ns resolution) — HRTIM is ~32× finer.

### 1.2 HRTIM Output Allocation

With 12 outputs (TA1/TA2 through TF1/TF2), the full 30 kW converter requires exactly **12 complementary outputs**: 6 for Vienna PFC + 6 for LLC.

#### Vienna PFC — 3 Switch Cells (Timers A, B, C)

The Vienna rectifier has 3 bidirectional switch cells, one per phase leg. Each cell requires one complementary PWM pair (top switch + bottom switch) with programmable dead-time.

| HRTIM Timer | Output Pair | Function | Switching Freq |
|---|---|---|---|
| Timer A | TA1 / TA2 | Phase A switch cell (S_A+, S_A−) | 48–65 kHz |
| Timer B | TB1 / TB2 | Phase B switch cell (S_B+, S_B−) | 48–65 kHz |
| Timer C | TC1 / TC2 | Phase C switch cell (S_C+, S_C−) | 48–65 kHz |

- Dead-time insertion: ~300 ns (SiC MOSFET, SCTWA90N65G2V-4 per [[01-Topology Selection]] §3.3)
- Phase interleaving: Timers A/B/C synchronized to Master, with compare registers in Master setting 120° offsets for PFC current ripple cancellation (effective ripple frequency 96–130 kHz)
- Duty cycle updated each PWM period by current-loop ISR

#### 3-Phase Interleaved LLC — 3 Half-Bridges (Timers D, E, F)

Each LLC phase is a half-bridge. Each half-bridge needs complementary drive with dead-time to ensure ZVS.

| HRTIM Timer | Output Pair | Function | Switching Freq |
|---|---|---|---|
| Timer D | TD1 / TD2 | LLC Phase 1 half-bridge (Q1_H, Q1_L) | 100–300 kHz |
| Timer E | TE1 / TE2 | LLC Phase 2 half-bridge (Q2_H, Q2_L) | 100–300 kHz |
| Timer F | TF1 / TF2 | LLC Phase 3 half-bridge (Q3_H, Q3_L) | 100–300 kHz |

- Dead-time: 80–150 ns (adjusted vs. operating frequency and ZVS condition)
- Variable frequency: period register (PERxR) updated each cycle via LLC voltage/current loop
- 120° phase interleaving maintained by master timer compare registers D/E/F (see Section 5.3)

> [!tip] Half-mode operation
> HRTIM "half mode" (HALF bit in TIMxCR = 1) automatically sets CMP1 = PER/2, guaranteeing 50% duty cycle at variable frequency — ideal for LLC half-bridges.

---

## 2. ADC Requirements

### 2.1 STM32G474RE ADC Instances

The G474RE has **5 × 12-bit ADC instances** (ADC1–ADC5), each capable of 4 Msps, with up to 42 total channels and 16-bit resolution via hardware oversampling. ADC1/ADC2 and ADC3/ADC4 are interleaved pairs sharing a common clock.

### 2.2 Signal List and ADC Allocation

#### Vienna PFC Signals

| Signal | Description | Sample Rate | ADC | Channel | Notes |
|---|---|---|---|---|---|
| I_A | Phase A input current | 48–65 kHz (every PWM period) | ADC1 | INJ group | Shunt or LEM HAL sensor |
| I_B | Phase B input current | 48–65 kHz | ADC2 | INJ group | Simultaneous with ADC1 |
| I_C | Phase C input current | 48–65 kHz | ADC3 | INJ group | Can derive from I_A + I_B |
| V_DC_bus | PFC output bus voltage | 48–65 kHz | ADC1 | INJ group | Resistor divider, ×½ |
| V_A | Grid phase A voltage | 48–65 kHz | ADC2 | INJ group | For PLL and feed-forward |
| V_B | Grid phase B voltage | 48–65 kHz | ADC3 | INJ group | |
| V_C | Grid phase C voltage | 48–65 kHz | ADC4 | INJ group | Derive Vγ or use all 3 |
| V_cap_top | Upper DC-link cap voltage | 1 kHz | ADC1 | REG group | Neutral point balance |
| V_cap_bot | Lower DC-link cap voltage | 1 kHz | ADC2 | REG group | Neutral point balance |

#### LLC DC-DC Signals

| Signal | Description | Sample Rate | ADC | Channel | Notes |
|---|---|---|---|---|---|
| V_out | Output DC voltage | 20 kHz | ADC4 | INJ group | Primary feedback for CV |
| I_out | Output DC current | 20 kHz | ADC5 | INJ group | Hall sensor, primary feedback for CC |
| I_LLC_ph1 | LLC phase 1 resonant current | 100 kHz | ADC1 | INJ group | Peak current / OCP sensing |
| I_LLC_ph2 | LLC phase 2 resonant current | 100 kHz | ADC2 | INJ group | |
| I_LLC_ph3 | LLC phase 3 resonant current | 100 kHz | ADC3 | INJ group | |

#### Temperature and Auxiliary Signals

| Signal | Description | Sample Rate | ADC | Notes |
|---|---|---|---|---|
| T_SiC_PFC | PFC SiC MOSFET heatsink NTC | 100 Hz | ADC4 | REG group, slow background scan |
| T_SiC_LLC | LLC SiC MOSFET heatsink NTC | 100 Hz | ADC5 | REG group |
| T_magnetics | Transformer / inductor NTC | 100 Hz | ADC4 | REG group |
| T_ambient | Inlet air temperature | 10 Hz | ADC5 | REG group |
| V_aux_12V | Auxiliary 12 V rail monitor | 100 Hz | ADC3 | REG group |

### 2.3 ADC Triggering and Synchronization

The G474 HRTIM generates 10 programmable ADC trigger events (ADC1TRG1–ADC1TRG5, ADC2TRG1–ADC2TRG5) that can be routed to any timer's reset, compare, or period event.

**PFC current sampling (center-of-PWM):**
- HRTIM Timer A, B, C each fire an ADC trigger at their CMP2 register, set to PER/2 (midpoint of on-time)
- This samples phase currents at the valley/midpoint where ripple is minimal (equivalent to average current sensing)
- `LL_ADC_INJ_SetTriggerSource(ADC1, LL_ADC_INJ_TRIG_EXT_HRTIM_TRG1)` → Timer A CMP2

**LLC output voltage/current sampling:**
- HRTIM Timer D fires ADC4/ADC5 injected trigger at its period event (resonant peak)
- Sampling at switching frequency (up to 300 kHz for LLC) requires ADC1–3 injected mode at 100 kHz minimum

**Slow background signals (temperatures, auxiliary rails):**
- ADC3/ADC4/ADC5 regular group in DMA scan mode, postscaler set to reduce effective rate to 100 Hz
- Triggered by HRTIM Master timer at rate-divided compare event

> [!warning] G474 ADC errata
> STM32G4 errata ES0430 notes issues when intermixing regular and injected channels with the same ADC instance and using DMA. Prefer dedicated ADC instances per group or use the oversampler on regular channels only.

---

## 3. STSW-30KWVRECT Reference Firmware Architecture

ST's **STSW-30KWVRECT** is the official reference firmware for the STDES-30KWVRECT 30 kW Vienna rectifier board using the STM32G474RE.

### 3.1 Software Layer Structure

```
Application Layer
├── State Machine (Init → Soft-Start → Run → Fault → Shutdown)
├── OCPP / Communication Interface (CAN to charger controller)
└── Supervisory (OTP, derating, fan speed, LED/status)

Control Layer (ISR-driven)
├── PFC Current Control ISR  [48–65 kHz, ~3 µs budget]
│   ├── ADC readback (phase currents, bus voltage, grid voltages)
│   ├── Clarke / Park transforms (abc → αβ → dq)
│   ├── SRF-PLL update (grid angle θ)
│   ├── d-axis and q-axis current PI controllers
│   ├── Inverse Park + SVM (Space Vector Modulation)
│   └── HRTIM duty-cycle update (TA1/TA2, TB1/TB2, TC1/TC2)
│
├── Bus Voltage Loop  [1 kHz, outer loop]
│   ├── V_DC filtered (2nd-order IIR)
│   ├── Voltage PI → I_d* reference
│   └── Anti-windup (back-calculation)
│
└── Neutral Point Balance  [1 kHz]
    └── V_cap differential PI → modulation index offset

Peripheral Drivers
├── HRTIM HAL/LL (6 timers, fault inputs)
├── ADC LL (5 instances, injected + regular)
├── CAN FD (FDCAN1 peripheral)
├── UART (debug, OCPP passthrough)
└── DMA (ADC, UART)
```

### 3.2 ISR Timing Budget

| ISR | Trigger | Period | Estimated execution |
|---|---|---|---|
| PFC_CurrentControl_ISR | HRTIM Master period event | 15–21 µs (48–65 kHz) | 2.5–3 µs |
| BusVoltage_ISR | TIM6 or HRTIM Master/64 | 1 ms | 0.5 µs |
| LLC_VoltageControl_ISR | HRTIM Timer D period event | Varies (2.5–10 µs) | 1 µs |
| CAN_Rx_ISR | FDCAN Rx FIFO | On demand | 0.3 µs |
| Fault_ISR | HRTIM FLT event | On demand | 0.1 µs (HW) |

At 170 MHz Cortex-M4, a 65 kHz ISR with 3 µs execution consumes **19.5%** of CPU — within budget for dual-loop control. The STM32G474's CORDIC and FMAC co-processors offload Park/Clarke transforms to reduce ISR execution time.

---

## 4. Vienna PFC Digital Control

### 4.1 dq-Frame Current Control

The Vienna rectifier is controlled in the synchronous (dq) reference frame, aligning the d-axis with the grid voltage vector so that:
- **I_d** controls active power (and DC bus voltage indirectly)
- **I_q** controls reactive power (set to 0 for unity PF)

**Control signal path:**

```
Grid voltages (V_abc) ──→ Clarke (αβ) ──→ Park (dq, using θ from PLL)
Phase currents (I_abc) ──→ Clarke ──→ Park → I_d_meas, I_q_meas

I_d* (from V_bus loop) ──→ [PI] ──→ V_d*
I_q* = 0              ──→ [PI] ──→ V_q*
                      + decoupling (ωL feedforward)

(V_d*, V_q*) ──→ Inverse Park ──→ (V_α*, V_β*) ──→ SVM ──→ HRTIM duty cycles
```

**Decoupling terms** (cross-coupling compensation):
```
V_d* = V_d_PI - ω·L·I_q + V_d_grid
V_q* = V_q_PI + ω·L·I_d + V_q_grid
```

**Typical PI gains (48–65 kHz sampling, L_boost ≈ 200 µH per phase, 700–920 V bus):**

| Loop | Bandwidth | K_p | K_i | Notes |
|---|---|---|---|---|
| d-axis current | 1–2 kHz | 0.8–1.5 Ω | 1,000–3,000 rad/s | Tuned for L/R time constant |
| q-axis current | 1–2 kHz | 0.8–1.5 Ω | 1,000–3,000 rad/s | Same structure as d-axis |
| DC bus voltage | 20–50 Hz | 0.01–0.05 | 5–20 rad/s | Outer loop, slow relative to current |

> [!note] Gain tuning method
> Use K_p = 2ζω_c·L and K_i = ω_c²·L/R, where ω_c = 2π × bandwidth. For L = 200 µH, R_winding = 20 mΩ, target bandwidth 1.5 kHz: K_p ≈ 0.94, K_i ≈ 1,776 rad/s.

### 4.2 Software PLL for Grid Synchronization

**Recommended PLL type: SRF-PLL (Synchronous Reference Frame PLL)**

The ST reference firmware (UM2975, STSW-VIENNARECT) uses an SRF-PLL. DSOGI-PLL is the preferred alternative for weak or distorted grids.

**SRF-PLL structure:**
```
V_abc ──→ Clarke (V_αβ) ──→ Park (V_dq using θ̂)
V_q ──→ PI (force V_q → 0) ──→ ω̂ ──→ integrator ──→ θ̂
```

| Parameter | Value | Notes |
|---|---|---|
| PLL type | SRF-PLL (DSOGI-PLL for distorted grid) | |
| Tracking range | 45–65 Hz | Per project spec |
| Bandwidth | 20–50 Hz (fast: up to 100 Hz) | Balance between noise rejection and tracking speed |
| Damping ζ | 0.707 (critically damped) | Standard choice |
| K_p (PLL PI) | 2ζω_n | ω_n = 2π × bandwidth |
| K_i (PLL PI) | ω_n² | |
| Sample rate | 48–65 kHz | Same as current-loop ISR |
| Frequency output | ω̂ → used for decoupling terms | |
| Angle output | θ̂ → used for Park transforms | |

**DSOGI-PLL** (recommended for noisy industrial grid or weak grid):
- Uses Second-Order Generalized Integrator (SOGI) as pre-filter to extract fundamental component
- Rejects harmonics before PLL, allows higher PLL bandwidth (500 rad/s vs. ~200 rad/s for SRF-PLL)
- Slightly higher computational cost; well within G474 budget

### 4.3 Bus Voltage Loop

| Parameter | Value |
|---|---|
| Target bus voltage | 700–920 VDC (active adjustment per output demand, see [[01-Topology Selection]] §4.4) |
| Control bandwidth | 20–50 Hz (1/10th of grid frequency) |
| Output | I_d* reference (active current demand) |
| Anti-windup | Back-calculation with tracking time constant T_t = √(T_i/T_p) |
| Voltage filter | 2nd-order Butterworth IIR, fc = 100 Hz (rejects 300 Hz ripple) |
| Soft-start | Ramp I_d* from 0 → rated over 200 ms (6 s total including LLC ramp) |
| Neutral-point balance | Separate P controller on (V_cap_top − V_cap_bot); adds offset to zero-sequence modulation |

---

## 5. LLC Frequency Control

### 5.1 Variable-Frequency Control via HRTIM Period Register

The LLC resonant converter is controlled by **PFM (Pulse Frequency Modulation)**. In HRTIM, switching frequency is set by writing the period register `PERxR` of each LLC timer (D, E, F).

**HRTIM period vs. frequency relationship:**
```
f_sw = f_HRTIM_DLL / PERxR
PERxR = f_HRTIM_DLL / f_sw
      = 5.44 × 10⁹ / f_sw

Example:
  f_sw = 200 kHz → PERxR = 27,200 ticks (5 ns resolution at this count)
  f_sw = 100 kHz → PERxR = 54,400 ticks
  f_sw = 300 kHz → PERxR = 18,133 ticks
```

**With HALF mode enabled** (HALF = 1 in TIMxCR):
- CMP1 auto-computed as PERxR/2 → 50% duty cycle guaranteed
- Dead-time registers (DTRx) set independently of duty cycle
- On each LLC control update: write new PERxR → HRTIM applies at next period boundary

**Period register update sequence** (to avoid glitches):
1. Preload enable: set PREEN bit (updates take effect at period boundary, not immediately)
2. Write new PERxR to shadow register
3. HRTIM automatically transfers shadow → active at next timer reset
4. If preload is disabled, write must be done after CMP event to avoid half-period glitch

### 5.2 CC/CV Outer Loop

The LLC operates in two modes:
- **CC mode** (constant current): I_out controlled by varying frequency
- **CV mode** (constant voltage): V_out controlled by varying frequency

**Control structure:**
```
CV mode:  V_out* ──→ [PI] ──→ Δf ──→ f_sw = f_nom + Δf ──→ PERxR update
CC mode:  I_out* ──→ [PI] ──→ Δf ──→ f_sw = f_nom + Δf ──→ PERxR update
Mode select: I_out > I_limit → switch to CC; V_out > V_limit → switch to CV
```

**Frequency-to-gain relationship:**
- Below resonance (f < f_r): gain increases as f decreases (ZCS risk)
- Above resonance (f > f_r): gain decreases as f increases (ZVS maintained)
- Operating range: f_r to 2×f_r (always above resonance in normal regulation)
- f_r ≈ 150.5 kHz = 1/(2π√(L_r·C_r)) — see [[02-Magnetics Design]] and [[03-LLC Gain Curve Verification]]

| Parameter | Value |
|---|---|
| Outer loop bandwidth | 500 Hz – 2 kHz (much slower than switching) |
| Frequency range | 100 kHz to 300 kHz (per [[01-Topology Selection]] §4.3) |
| K_p (voltage loop) | 0.001–0.01 (units: Hz/V) |
| K_i | 1–10 rad/s |
| Anti-windup | Clamp integrator when f_sw hits min/max limit |
| Sample rate for V_out / I_out | 20 kHz (LLC timer period event) |

### 5.3 Phase Interleaving at Variable Frequency

Maintaining 120° phase offset between the three LLC phases requires that the HRTIM master timer manages phase references, not just absolute timing.

**Implementation using HRTIM Master timer:**
```
Master timer: runs at same period as LLC slaves (PERxR_M = PERxR_D = PERxR_E = PERxR_F)

Master CMP1 ──→ resets Timer D (Phase 1, offset = 0°)
Master CMP2 ──→ resets Timer E (Phase 2, offset = PERxR/3)
Master CMP3 ──→ resets Timer F (Phase 3, offset = 2×PERxR/3)

On frequency update:
  new_PERxR = f_HRTIM_DLL / f_sw_new
  Master_CMP1 = 0
  Master_CMP2 = new_PERxR / 3
  Master_CMP3 = 2 × new_PERxR / 3
  Write all registers simultaneously using HRTIM burst mode or preload
```

> [!important] Simultaneous register update
> All period and compare registers must be updated atomically (in the same PWM cycle) to avoid transient phase imbalance during frequency steps. Enable preload on Master and all slave timers; write all values before the next Master period event triggers shadow transfer.

**TI C2000 application note SPRAD15** documents a similar approach for 3-phase interleaved LLC where CMPA/CMPB values for phase shift must be loaded simultaneously to prevent PWM ordering errors during frequency transitions.

### 5.4 Burst Mode for Light Load (< 3 kW, ~10%)

Below 10% load, variable frequency alone cannot maintain regulation efficiently (very high frequency → high switching losses, low gain). Burst mode is implemented:

**HRTIM Burst Mode Controller:**
- Hardware block within HRTIM that alternates between RUN and IDLE states
- In IDLE state: HRTIM outputs are forced to idle level (low for LLC switches)
- Burst period and duty cycle set by `HRTIM_BMPER` and `HRTIM_BMCMPR` registers
- Trigger: software sets burst mode active when LLC voltage PI output falls below threshold

**Burst mode activation threshold:**
```
Enter burst mode: f_sw demand > f_burst_threshold (e.g., 280 kHz)
Exit burst mode:  f_sw demand < f_run_threshold (e.g., 270 kHz) [hysteresis]
```

**During burst IDLE period:**
- LLC resonant tank rings down naturally (ZVS preserved for first post-burst cycle)
- Output capacitor supplies load
- ADC continues sampling; voltage loop integrator freezes (or decays slowly)

**Light-load efficiency improvement:**
- At 5% load, burst mode reduces switching events by 70–90%
- Core losses in LLC transformer proportional to switching frequency × duty of activity
- Burst frequency ~10–50 kHz; burst duty cycle adjusted by outer voltage loop

---

## 6. Inter-Module CAN Protocol for 5-Module Stacking

### 6.1 Physical Layer

| Parameter | Value |
|---|---|
| Interface | FDCAN1 (STM32G474 FDCAN peripheral) |
| Bit rate | 500 kbps nominal (data phase 2 Mbps for CAN FD) |
| Topology | Daisy-chain bus, 120 Ω termination at each end |
| Frame format | CAN 2.0B (29-bit extended ID) or CAN FD |
| Bus length | Up to 5 m within charger cabinet |

### 6.2 CAN Frame Structure

**Module address scheme:** Each module has a 4-bit node ID (0x0–0xF), configured via DIP switches or resistor-coded GPIO.

#### Status Frame (Module → Master, broadcast, 10 ms period)

| Bits | Field | Resolution | Range |
|---|---|---|---|
| 28:24 | Node ID [4:0] | — | 0–15 |
| 23:16 | Message type = 0x01 | — | Status |
| 15:4 | I_out measured [11:0] | 0.1 A/LSB | 0–100 A |
| 3:0 | Fault flags [3:0] | — | OVP, OCP, OTP, COM |
| +16 bits | V_out measured [15:0] | 0.1 V/LSB | 0–1000 V |
| +8 bits | Temperature [7:0] | 1°C/LSB | −40–215°C |
| +8 bits | Module state [7:0] | — | INIT/RUN/FAULT/IDLE |

#### Command Frame (Master → All modules, 10 ms period)

| Bits | Field | Resolution | Range |
|---|---|---|---|
| 28:24 | Destination (0x1F = broadcast) | — | |
| 23:16 | Message type = 0x02 | — | Command |
| 47:32 | V_ref [15:0] | 0.1 V/LSB | 150–1000 V |
| 63:48 | I_ref [15:0] | 0.1 A/LSB | 0–100 A |
| +8 bits | Enable flags | — | EN, CC_mode, CV_mode |

### 6.3 Current-Sharing Strategy

**Active current sharing with droop:**
```
I_ref_module_n = I_total_ref / N_active + K_droop × (I_avg − I_n_meas)

Where:
  N_active = number of enabled modules (1–5)
  K_droop  = droop gain (~0.05 A/A)
  I_avg    = mean of all modules' I_out (computed by master from status frames)
  I_n_meas = this module's measured output current
```

**Master module responsibilities:**
- Receives status frames from all slaves every 10 ms
- Computes I_avg and checks for imbalance (> 5% → log event)
- Broadcasts updated I_ref and V_ref every 10 ms
- Module selection: activates/deactivates modules based on total power demand
- Fault arbitration: if any module reports fault, master re-allocates current

**Slave module behavior on CAN timeout:**
- If no command frame received within 50 ms → reduce output to 50% rated
- If no command frame within 200 ms → shutdown (safety fail-safe)

---

## 7. Protection Implementation

### 7.1 Hardware Protection (< 1 µs response)

These protections use the STM32G474 analog comparators (COMP1–COMP7) routed directly to HRTIM fault inputs, bypassing firmware entirely.

| Protection | Mechanism | Threshold | Response | HRTIM Fault |
|---|---|---|---|---|
| OCP — PFC phase | COMP1/2/3 on shunt resistor | 1.3× rated (78 A peak) | < 200 ns | FLT1 → all PFC outputs → idle |
| OCP — LLC resonant | COMP4/5 on LLC current transformer | 2× rated peak | < 200 ns | FLT2 → LLC outputs → idle |
| OVP — DC bus | COMP6 on resistor divider | 966 V (920 V × 1.05) | < 1 µs | FLT3 → all outputs → idle |
| OVP — LLC output | COMP7 on output divider | 1050 V (Vout_max × 1.05) | < 1 µs | FLT4 → LLC outputs → idle |

**HRTIM fault response modes:**
- **CBC (Cycle-by-Cycle):** output forced idle for one period, auto-resets; used for soft current limiting
- **Latch:** output forced idle permanently until firmware clears; used for hard faults (OVP, destructive OCP)

### 7.2 Firmware Protection (1–10 ms response)

These protections are implemented in the control ISR or background task.

| Protection | Mechanism | Threshold | Response Time | Action |
|---|---|---|---|---|
| OTP — SiC junction | NTC ADC reading | > 100°C | 10 ms (background loop) | Derate output power, then shutdown at 115°C |
| OTP — magnetics | NTC ADC reading | > 120°C | 10 ms | Reduce switching frequency, then shutdown |
| OTP — ambient | NTC ADC reading | > 65°C | 100 ms | Enable fan boost, derate at 55°C |
| UVP — DC bus | Software threshold in voltage loop | < 600 V (min operating) | 1 ms (voltage ISR) | Disable LLC, hold PFC |
| Phase loss | SRF-PLL frequency deviation | ±5 Hz from nominal | 20 ms | Fault state |
| CAN timeout | Missing master frame counter | > 50 ms | — | Reduce to 50% rated |

### 7.3 Soft-Start and Inrush

- **Pre-charge relay**: closes via NTC thermistor circuit before main contactor to limit inrush to DC bus caps
- **Software soft-start**: ramp I_d* from 0 in PFC current loop over 200 ms; LLC V_ref ramp from V_initial to V_target over further 1–2 s
- **Total startup time**: ≤ 6 s (per project spec in [[__init]])

> [!info] For the complete power-on/off sequence including inrush calculations, NTC/relay/contactor specifications, timing diagrams, fault shutdown sequences, and cold-start analysis, see [[08-Power-On Sequence and Inrush Management]].

---

## 8. OCPP 1.6 and ISO 15118 Interface

### 8.1 Architecture Overview

The STM32G474RE power module does **not** run OCPP or ISO 15118 directly — these are handled by a higher-level **SECC (Supply Equipment Communication Controller)** or charger management module (typically an embedded Linux or RTOS-based board with Ethernet/Wi-Fi).

The power module interfaces to this controller via a simple **internal CAN or UART protocol**.

```
[EV Vehicle BMS] ←──── ISO 15118 (PLC on pilot line) ────→ [SECC / Charger Controller]
                                                                     │
                                                              OCPP 1.6 (Ethernet/4G)
                                                                     │
                                                           [Cloud / CSMS Backend]
                                                                     │
                                                      CAN bus or RS-485 (internal)
                                                                     │
                                                      ┌──────────────┴──────────────┐
                                                [PDU Module 1] ... [PDU Module 5]
                                                (STM32G474RE)      (STM32G474RE)
```

### 8.2 Internal CAN Messages from Charger Controller to PDU Modules

The charger controller translates ISO 15118/OCPP session parameters into simple setpoints sent to PDU modules:

| Message | Direction | Fields | Rate |
|---|---|---|---|
| Charger_Setpoint | Controller → PDU | V_target (V), I_target (A), mode (CC/CV/OFF), session_id | 100 ms |
| PDU_Status | PDU → Controller | V_out (V), I_out (A), P_out (W), T_max (°C), fault_code, state | 100 ms |
| PDU_Fault | PDU → Controller | fault_type, fault_severity (warn/shutdn), timestamp | On event |

### 8.3 OCPP 1.6 Relevant Actions (Charger Controller Level)

The power module firmware responds indirectly to these OCPP actions via the setpoint messages above:

| OCPP Action | Effect on PDU |
|---|---|
| `RemoteStartTransaction` | Controller sends Charger_Setpoint with I_target, V_target |
| `RemoteStopTransaction` | Controller sends I_target = 0, then OFF |
| `ChangeConfiguration` (max current) | Controller updates I_target in Charger_Setpoint |
| `MeterValues` | PDU_Status aggregated and uploaded as meter reading |
| `StatusNotification` | PDU fault_code mapped to OCPP status (Faulted, Available) |

### 8.4 ISO 15118 Interaction (Plug & Charge, V2G)

ISO 15118-2 (AC/DC charging) defines `CurrentDemand` and `PowerDelivery` messages. The SECC translates:

| ISO 15118 Parameter | Mapped to PDU |
|---|---|
| `EVTargetVoltage` | V_target in Charger_Setpoint |
| `EVTargetCurrent` | I_target in Charger_Setpoint |
| `EVMaximumVoltageLimit` | V_max clamp in PDU firmware |
| `EVMaximumCurrentLimit` | I_max clamp in PDU firmware |
| `ChargingComplete` | Controller sends OFF setpoint |

> [!note] OCPP 1.6 + ISO 15118 tunneling
> OCPP 1.6 does not natively carry ISO 15118 data. OCA's "Using ISO 15118 Plug & Charge with OCPP 1.6" spec defines a `DataTransfer` tunneling mechanism. For new designs, prefer OCPP 2.0.1 which has native ISO 15118 support.

---

## 9. Firmware Implementation Checklist

- [ ] HRTIM DLL calibration at startup (ST HAL: `HAL_HRTIM_DLLCalibrationStart`)
- [ ] ADC calibration (self-calibration on startup for all 5 instances)
- [ ] SRF-PLL pre-lock sequence on startup (ramp ω̂ from 0 to grid frequency before enabling current loop)
- [ ] LLC soft-start: begin at f_max (maximum attenuation) and ramp down toward f_r
- [ ] Preload enable on all LLC HRTIM timers before variable-frequency operation
- [ ] HRTIM fault inputs tested in hardware (inject fault signal via test point)
- [ ] CAN baud rate configuration (500 kbps) and node ID DIP switch read at init
- [ ] NTC thermistor lookup table (Steinhart-Hart coefficients for specific NTC part)
- [ ] State machine fault logging (fault code + timestamp to internal flash or EEPROM emulation)

---

## References

- [[01-Topology Selection]] — Vienna PFC + LLC topology rationale
- [[02-Magnetics Design]] — L_r, C_r, transformer design
- [[03-LLC Gain Curve Verification]] — Gain curve and ZVS boundary
- [[04-Thermal Budget]] — SiC junction temperatures and derating curves
- [[Commercial Reference Designs Survey]] — ST STDES-30KWVRECT, Wolfspeed CRD30DD12N-K

**Implementation detail sub-documents** (see [[06-Firmware-Design/__init|06-Firmware Design]]):
- [[06-Firmware-Design/01-Application State Machine|01-Application State Machine]] — 10-state FSM, transition table, pseudocode
- [[06-Firmware-Design/02-Power-On Sequence and Ramp Control|02-Power-On Sequence and Ramp Control]] — Init steps, PLL lock, PFC/LLC ramps
- [[06-Firmware-Design/03-Fault State Machine and Recovery|03-Fault State Machine and Recovery]] — Fault classification, derate curves, logging
- [[06-Firmware-Design/04-LLC Burst Mode|04-LLC Burst Mode]] — Light-load burst algorithm, HRTIM registers
- [[06-Firmware-Design/05-CAN Master and Module Stacking|05-CAN Master and Module Stacking]] — Master FSM, enable sequencing, failover
- [[06-Firmware-Design/06-ADC Pipeline and DMA Configuration|06-ADC Pipeline and DMA Configuration]] — DMA buffers, oversampling, filters
- [[06-Firmware-Design/07-Neutral Point Balancing|07-Neutral Point Balancing]] — P-controller, zero-sequence injection

**External references:**
- ST AN4539 Rev 5 — [HRTIM Cookbook](https://www.st.com/resource/en/application_note/an4539-hrtim-cookbook-stmicroelectronics.pdf)
- ST UM3011 — [STDES-30KWVRECT Getting Started](https://www.st.com/resource/en/user_manual/um3011-getting-started-with-the-stdes30kwvrect-30-kw-vienna-pfc-rectifier-reference-design-stmicroelectronics.pdf)
- ST STSW-30KWVRECT — [Firmware package](https://www.st.com/en/embedded-software/stsw-30kwvrect.html)
- Imperix — [SRF-PLL](https://imperix.com/doc/implementation/synchronous-reference-frame-pll) and [Vector current control](https://imperix.com/doc/implementation/vector-current-control)
- TI SPRAD15 — Three-Phase Interleaved LLC on C2000 Type-4 PWM
- Infineon EVAL-5K5W-3PH-LLC — [5.5 kW 3-Phase Interleaved LLC App Note](https://www.infineon.com/assets/row/public/documents/24/42/infineon-evaluation-board-eval-5k5w-3ph-llc-sic2-applicationnotes-en.pdf)
- ST STM32G4 HRTIM Training — [Product Training PDF](https://www.st.com/resource/en/product_training/STM32G4-WDG_TIMERS-High_Resolution_Timer_HRTIM.pdf)
- ST AN5346 — [STM32G4 ADC Use Tips](https://www.st.com/resource/en/application_note/an5346-stm32g4-adc-use-tips-and-recommendations-stmicroelectronics.pdf)
- OCA — [Using ISO 15118 Plug & Charge with OCPP 1.6](https://openchargealliance.org/wp-content/uploads/2023/11/ocpp_1_6_ISO_15118_v10.pdf)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
