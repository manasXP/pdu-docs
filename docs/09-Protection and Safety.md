---
tags: [PDU, protection, safety, OVP, OCP, OTP, ground-fault, insulation, surge, compliance]
created: 2026-02-22
status: draft
---

# Protection and Safety Design — 30 kW PDU

> [!summary] Key Numbers
> 14 distinct protection functions spanning voltage, current, thermal, ground fault, and surge domains. Hardware OVP response: <1 us (comparator-latched). DESAT short-circuit turn-off: <2 us. Ground fault trip: <6 mA DC residual per IEC 62955. Hipot: up to 4000 VAC primary-to-secondary. All protections mapped to IEC 61851-23, IEC 62368-1, UL 2202, and EN 61000 series.

---

## 1. Overview

### 1.1 Purpose

This document defines every protection function in the 30 kW PDU, specifying detection method, trip threshold, response time, recovery behavior, and the applicable safety standard clause. It serves as the single reference for:

- Hardware protection circuit design (comparators, gate driver DESAT, MOVs/TVS)
- Firmware protection state machine and fault handling (cross-reference [[06-Firmware Architecture]])
- Safety certification test plan (IEC 61851-23, UL 2202, IEC 62368-1)
- Production test specification (hipot, insulation resistance, functional protection verification)

### 1.2 Reference Standards

| Standard | Edition | Scope | Relevance to PDU |
|----------|---------|-------|-------------------|
| **IEC 61851-23** | Ed. 2.0 (2023) | DC EV charging station requirements | Primary product standard — output protection, insulation, ground fault |
| **IEC 62368-1** | Ed. 3.0 (2023) | Audio/video, IT, and communication equipment safety | Equipment-level safety: energy hazard classes, insulation, touch current |
| **UL 2202** | Ed. 3 (2022) | EV charging system equipment (North America) | UL listing for US/Canada market — parallels IEC 61851-23 |
| **IEC 60664-1** | Ed. 2.0 (2007) | Insulation coordination for low-voltage systems | Creepage, clearance, pollution degree, overvoltage category |
| **EN 61000-4-2** | (2009) | Electrostatic discharge immunity | ESD on accessible surfaces |
| **EN 61000-4-4** | (2012) | Electrical fast transient / burst immunity | EFT on AC input and signal lines |
| **EN 61000-4-5** | (2014+A1:2017) | Surge immunity | AC input and DC output surge protection |
| **IEC 62955** | Ed. 1.0 (2018) | Residual direct current detecting device (RDC-DD) | DC ground fault detection for mode 3/4 charging |
| **EN 55032** | (2015+A1:2020) | Conducted and radiated emissions | EMC compliance (see [[05-EMI Filter Design]]) |

---

## 2. Voltage Protection

### 2.1 Output Over-Voltage Protection (OVP)

The output voltage range is 150–1000 VDC. Over-voltage on the output cable directly endangers the vehicle battery and occupant safety.

> [!warning] Critical Safety Function
> Output OVP is a **safety-critical** protection per IEC 61851-23 clause 6.3.1. Both software and hardware OVP are mandatory — neither alone is sufficient for certification.

#### 2.1.1 Software OVP

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | ADC sampling of output voltage divider | 12-bit ADC, 1 MSPS, HRTIM-triggered |
| Trip threshold | 105% of current setpoint | e.g., at 800 V setpoint: trip at 840 V |
| Response time | <100 us | ADC conversion + comparison + PWM disable |
| Action | Disable LLC PWM via HRTIM output disable | HRTIM FLT input or software SET/RST |
| Secondary action | Open output contactor after 10 ms | Allows current decay through freewheeling path |
| Recovery | Auto-retry after 1 s cooldown | Up to 3 retries, then latch to FAULT |

#### 2.1.2 Hardware OVP

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | Analog comparator (STM32 internal or external LM339) | Dedicated resistor divider, separate from ADC divider |
| Trip threshold | 110% of maximum output (1100 VDC) | Fixed threshold — absolute maximum |
| Response time | <1 us | Comparator propagation + HRTIM fault blanking |
| Action | Latch HRTIM FLT input → all PWM forced low | Hardware-latched, firmware cannot override |
| Secondary action | Open output contactor via GPIO | Contactor coil de-energized by fault latch |
| Recovery | Manual reset (power cycle or CAN command) | Latching fault — requires operator intervention |

#### 2.1.3 Output Clamp

- **TVS diodes:** Bidirectional TVS array rated for V_WM = 1000 VDC, V_BR = 1100 VDC, clamping at 1200 V for 10/1000 us pulse
- **Energy absorption:** Sized for stored energy in output filter capacitors plus cable inductance energy (L_cable x I^2 / 2)
- **Coordination:** TVS clamps transiently while hardware OVP opens the contactor within 10 ms

### 2.2 Input Over-Voltage Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | ADC sampling of AC input voltage (after rectification or via isolated amplifier) | Per-phase monitoring |
| Trip threshold | 583 VAC (530 VAC + 10%) | Corresponds to ~825 Vpk line-to-line |
| Response time | <10 ms (within one AC cycle) | Software-based, sampled at line frequency |
| Action | Disable PFC PWM, open input contactor | Prevents DC bus overshoot |
| Recovery | Auto-retry when V_in returns below 550 VAC for >5 s | Hysteresis prevents chattering |

### 2.3 DC Bus Over-Voltage Protection

The DC bus is rated for 920 VDC nominal (Vienna PFC boost output). Bus capacitors are rated at 450 V per rail (900 V total series) with 1000 V rated film caps across the full bus.

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | Hardware comparator on DC bus voltage divider | Separate from PFC control ADC path |
| Trip threshold | 960 VDC | 4.3% margin to 1000 V film cap rating |
| Response time | <5 us | Analog comparator to HRTIM FLT |
| Action | Disable PFC PWM immediately | LLC continues briefly to discharge bus |
| Recovery | Auto-retry after 5 s if bus voltage < 900 V | Up to 3 retries |

> [!tip] Design Margin
> The 960 V trip point provides 40 V margin to the 1000 V film capacitor rating and 80 V margin to the 450 V + 450 V series electrolytic rating (effective 900 V with voltage balancing). This accounts for measurement tolerance (±1%) and comparator offset.

### 2.4 Under-Voltage Protection

| Condition | Threshold | Action | Recovery |
|-----------|-----------|--------|----------|
| DC bus UV | <600 VDC | Disable LLC (insufficient headroom for resonant gain) | Auto when bus > 650 V |
| AC input UV (brownout) | <230 VAC sustained >1 s | Graceful shutdown: ramp output to 0, open contactors | Auto when V_in > 250 VAC for 5 s |
| AC input UV (sag) | <200 VAC for <100 ms | Ride through using DC bus energy (55 J at 800 V) | Transparent to output |
| Output UV | Per CAN setpoint | Managed by CC/CV control loop — not a fault | N/A |

---

## 3. Current Protection

### 3.1 Output Over-Current Protection (OCP)

#### 3.1.1 Cycle-by-Cycle Current Limiting

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | HRTIM built-in comparator (CMP1 on each LLC timer) | Shunt resistor + current sense amplifier → comparator |
| Trip threshold | 110 A (110% of 100 A rated) | Per-phase threshold: 36.7 A (3-phase interleaved) |
| Response time | Within current switching period (<10 us at 100 kHz) | Pulse-by-pulse skip |
| Action | Truncate current pulse (pulse skip) | Maintains soft-switching; output voltage droops naturally |
| Recovery | Immediate — next switching cycle resumes normally | Self-recovering |

#### 3.1.2 Hardware OCP

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | External fast comparator (e.g., TLV3501, 4.5 ns propagation) | Blanking circuit: RC filter or digital blanking via HRTIM |
| Trip threshold | 120 A | Absolute maximum, above cycle-by-cycle limit |
| Response time | <500 ns | Comparator + gate driver disable |
| Action | Disable all LLC PWM outputs via HRTIM FLT | Latching for 1 s |
| Recovery | Auto-retry after 1 s | Up to 3 retries, then latch |

#### 3.1.3 Constant Power Foldback

At the current limit boundary, the control loop implements constant-power foldback:

$$P_{out} = V_{out} \times I_{limit} = V_{out} \times 100\text{ A}$$

As output current hits 100 A, the voltage setpoint is reduced to maintain 30 kW:

| Output Voltage (V) | Maximum Current (A) | Power (kW) |
|--------------------:|--------------------:|-----------:|
| 1000 | 30 | 30 |
| 500 | 60 | 30 |
| 300 | 100 | 30 |
| 200 | 100 | 20 (current-limited) |
| 150 | 100 | 15 (current-limited) |

### 3.2 Input Over-Current Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | Per-phase current sensor (shunt + INA240 or Hall effect) | ADC-sampled at PFC switching rate |
| Trip threshold | 66 A peak (110% of 60 A rated) | Per-phase measurement |
| Response time | <1 ms (software, within PFC control loop) | Hardware backup via upstream MCB (63 A Type D) |
| Action | Reduce PFC duty cycle; if sustained >100 ms, disable PFC | Soft current limiting first, hard trip second |
| Recovery | Auto after 5 s | Ramp PFC back to setpoint |

### 3.3 DC Bus Over-Current

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | Shunt resistor on DC bus (high-side or low-side) + isolated amplifier | Hall sensor (e.g., LEM HTFS 200-P) as alternative |
| Trip threshold | 44 A | At 920 VDC bus: 44 A x 920 V = 40.5 kW (135% of rated) |
| Response time | <100 us (ADC-based) | Hardware comparator backup at 50 A |
| Action | Disable PFC and LLC simultaneously | Full shutdown |
| Recovery | Auto-retry after 5 s | Single retry, then latch |

### 3.4 Short-Circuit Protection

> [!warning] Critical Fast-Response Protection
> Short-circuit faults can destroy SiC MOSFETs within 2–5 us due to their low short-circuit withstand time (typ. 3 us for 1200 V SiC). Hardware DESAT detection is mandatory.

#### 3.4.1 Output Short-Circuit Detection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | dI/dt sensing (di/dt transformer or rate-of-rise on shunt) | Threshold: >50 A/us |
| Response time | <10 us | Faster than cycle-by-cycle OCP |
| Action | Disable all PWM, open output contactor | Hard shutdown |
| Recovery | Latch — manual reset required | Inspect for damage before restart |

#### 3.4.2 DESAT Detection (SiC MOSFETs)

The STGAP2SiC isolated gate drivers include integrated desaturation detection:

| Parameter | Value | Notes |
|-----------|-------|-------|
| DESAT threshold | V_DS > 8 V (configurable via external resistor) | SiC on-state at 100 A: V_DS = R_DS(on) x I = 0.022 x 100 = 2.2 V |
| Blanking time | 2.5 us (configurable, 2–3 us range) | Must exceed turn-on dV/dt transient + reverse recovery |
| Detection method | High-voltage diode from drain to DESAT pin | Internal current source charges blanking capacitor |
| Turn-off method | Soft turn-off (2-level gate drive: fast to 0 V, then slow to -5 V) | Limits dV/dt to prevent drain voltage overshoot |
| Response time | <2 us from DESAT detection to gate low | Including soft turn-off ramp |
| Fault output | Open-drain FAULT pin → HRTIM FLT input | Active-low, latching until cleared |

> [!note] Blanking Time Selection
> The 2.5 us blanking time is chosen to be longer than the SiC MOSFET turn-on transient (typ. 30–80 ns) plus the resonant commutation interval in LLC operation. At 300 kHz LLC (3.33 us period), the blanking time consumes 75% of a half-period — for very high frequency operation, consider reducing blanking to 2 us and accepting slightly higher false-trip risk at the boundary.

---

## 4. Thermal Protection (OTP)

### 4.1 Temperature Sensing Locations

| Sensor | Location | Sensor Type | ADC Channel | Purpose |
|--------|----------|-------------|-------------|---------|
| NTC1 | PFC heatsink (near MOSFET cluster) | 10 kOhm NTC B=3950 | ADC1_IN5 | PFC MOSFET junction estimation |
| NTC2 | LLC primary heatsink | 10 kOhm NTC B=3950 | ADC1_IN6 | LLC primary MOSFET Tj estimation |
| NTC3 | LLC secondary heatsink | 10 kOhm NTC B=3950 | ADC1_IN7 | Secondary diode Tj estimation |
| NTC4 | LLC transformer (on core or winding) | 10 kOhm NTC B=3950 | ADC1_IN8 | Transformer hot-spot |
| NTC5 | AC-DC board (near boost inductors) | 10 kOhm NTC B=3950 | ADC2_IN1 | Inductor temperature |
| NTC6 | Ambient / fan inlet | 10 kOhm NTC B=3950 | ADC2_IN2 | Inlet air for derating calculation |

### 4.2 MOSFET Junction Temperature Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Estimated Tj from heatsink NTC | T_j = T_heatsink + P_device x R_th(j-hs) | R_th(j-hs) from [[04-Thermal Budget]] |
| Warning threshold | T_j(est) = 125 deg C | Trigger fan speed increase, CAN warning |
| Trip threshold | T_j(est) = 140 deg C | Immediate power reduction to 50%, shutdown if no recovery |
| Hysteresis | 15 deg C | Resume full power below 125 deg C |
| Absolute maximum | T_j = 175 deg C (datasheet) | 35 deg C margin from trip to max |

### 4.3 Transformer Temperature Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Trip threshold | 130 deg C | Class F insulation limit = 155 deg C; 25 deg C margin |
| Warning threshold | 115 deg C | Increase fan speed, reduce power |
| Hysteresis | 10 deg C | Resume normal operation below 120 deg C |

### 4.4 Ambient Temperature Derating

Per [[04-Thermal Budget]] and [[__init]] specifications:

| Ambient Temperature | Maximum Output Power | Fan Speed | Notes |
|--------------------:|---------------------:|----------:|-------|
| -30 deg C to +45 deg C | 30 kW (100%) | Variable (PID) | Full-rated operation |
| 45 deg C to 50 deg C | 30 kW to 22.5 kW (linear) | 100% | Linear derating begins |
| 50 deg C to 55 deg C | 22.5 kW to 15 kW (linear) | 100% | Continued derating |
| 55 deg C to 65 deg C | 15 kW to 0 kW (linear) | 100% | Final derating to shutdown |
| >65 deg C inlet | 0 kW — shutdown | 100% | Thermal fault latch |

> [!tip] Cold Start Consideration
> At -30 deg C, electrolytic capacitor ESR increases significantly (typ. 5–10x). The pre-charge sequence ([[08-Power-On Sequence and Inrush Management]]) includes a warm-up hold of 30 s at reduced power to bring capacitor temperature above -10 deg C before ramping to full load.

### 4.5 Fan Failure Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| Detection | Tachometer output from each fan (3 x 92 mm fans) | Hall-effect tach, 2 pulses per revolution |
| Normal RPM | 2000–5000 RPM (PWM controlled) | PID loop maintains heatsink temperature |
| Warning threshold | RPM < 50% of setpoint for >2 s | CAN warning, increase remaining fan speed |
| Trip threshold | RPM < 50% of setpoint for >5 s | Reduce power to 50%, shutdown if heatsink T rises |
| Total fan loss | All fans <500 RPM | Immediate shutdown (thermal runaway risk) |
| Recovery | Auto when fan RPM recovers above 75% of setpoint | 10 s stabilization delay |

---

## 5. Earth Leakage and Ground Fault

### 5.1 Touch Current Limits

Per IEC 62368-1 for Class I equipment (protective earthing):

| Parameter | Limit | Test Condition |
|-----------|-------|---------------|
| Steady-state touch current | <3.5 mA | Normal operation, rated voltage |
| Protective earth continuity | <0.1 ohm | 25 A test current for 60 s |
| Earth bond current | >2x rated input current | Verify PE conductor sizing |

### 5.2 Earth Leakage Current Budget

| Source | Leakage Current (mA) | Notes |
|--------|----------------------:|-------|
| Y-capacitors (EMI filter) | <1.0 | 3 x 22 nF Y2 caps at 530 VAC, 50 Hz: I = 2 pi f C V = 2 x 3.14 x 50 x 22e-9 x 530 x 3 = 0.55 mA |
| Parasitic capacitance (heatsink-to-chassis) | <0.5 | Depends on isolation pad (Kapton/SilPad) |
| CM noise at switching frequency | <0.5 | CM choke attenuates by >40 dB (see [[05-EMI Filter Design]]) |
| Transformer interwinding capacitance | <0.3 | Faraday shield reduces coupling |
| DC-DC board parasitic | <0.2 | Via heatsink-to-secondary ground |
| **Total (worst case)** | **<2.5** | **Margin of 1.0 mA to 3.5 mA limit** |

> [!warning] Y-Capacitor Selection
> Y-capacitor values are constrained by the 3.5 mA touch current limit. Maximum total Y-capacitance per line-to-PE: C_max = I_max / (2 pi f V) = 3.5e-3 / (2 x 3.14 x 50 x 530) = 21 nF. The 22 nF Y2 caps per phase are at the limit — verify with parasitic contributions during EMC qualification testing.

### 5.3 Ground Fault Detection

#### 5.3.1 DC Residual Current Monitoring (RCM)

Per IEC 62955, DC charging stations must detect DC residual (fault) currents that bypass the upstream AC RCD:

| Parameter | Value | Standard |
|-----------|-------|----------|
| DC fault current trip | >6 mA DC | IEC 62955, IEC 61851-23 clause 9.4 |
| Response time | <1 s for >6 mA DC | IEC 62955 |
| Smooth DC detection | Required | Standard RCDs (Type A) are blind to DC — RDC-DD required |
| Implementation | Dedicated RCM module (e.g., Bender RCMB300 or integrated IC) | Or fluxgate-based DC CT |

#### 5.3.2 AC Residual Current Protection

| Parameter | Value | Notes |
|-----------|-------|-------|
| AC fault current trip | 30 mA (Type A RCD upstream) | Provided by installation, not PDU-internal |
| PDU responsibility | Signal the system controller to open AC contactor if RCM detects fault | CAN message to charger controller |

### 5.4 Insulation Monitoring

| Test | Threshold | When | Standard |
|------|-----------|------|----------|
| Pre-charge insulation resistance | >500 kohm (output-to-PE) | Before closing output contactor, every startup | IEC 61851-23 clause 8.2 |
| Continuous insulation monitoring | >100 kohm during operation | Periodic (every 10 s) | IEC 61851-23 clause 8.2 |
| Method | Insulation monitoring device (IMD) injecting low-frequency AC test signal | DC-safe measurement, does not interfere with charging | IEC 61557-8 |

> [!note] Implementation
> The IMD function can be integrated into the controller board using a dedicated IC (e.g., Bender iso685-D or ADI ADUM4190-based isolated measurement). The test signal is injected between output positive and PE, measuring leakage through the cable and vehicle chassis. See [[00-Board Partitioning]] for signal routing between controller and DC-DC boards.

---

## 6. Surge and Transient Protection

### 6.1 AC Input Surge Protection (IEC 61000-4-5)

| Test | Waveform | Level | PDU Requirement |
|------|----------|-------|-----------------|
| Line-to-line (L-L) | 1.2/50 us voltage, 8/20 us current | 2 kV / installation class III | Criterion B (temporary degradation, self-recovery) |
| Line-to-earth (L-PE) | 1.2/50 us voltage, 8/20 us current | 4 kV / installation class III | Criterion B |

#### 6.1.1 Protection Components

| Component | Type | Rating | Location | Purpose |
|-----------|------|--------|----------|---------|
| MOV (L-L) | EPCOS B72220S0271K101 | 275 VAC, 20 kA 8/20 us | AC input, before EMI filter | Clamp L-L surge to <900 Vpk |
| MOV (L-PE) | EPCOS B72220S0271K101 | 275 VAC, 20 kA 8/20 us | AC input, L to PE | Clamp L-PE surge |
| GDT (L-PE) | Bourns 2038-xx-SM | 600 V sparkover, 20 kA | AC input, L to PE (after MOV) | Secondary clamp for fast transients |
| TVS (DC bus) | Littelfuse SMDJ440CA | 440 V working, 710 V clamp | Across each bus cap rail | Absorb residual transients past MOV |

> [!tip] MOV Coordination
> Place MOVs at the AC input terminals (before the EMI filter X/Y capacitors). The MOV clamping voltage (~700–900 V at 20 kA) must be below the EMI filter component voltage ratings. GDTs are placed after MOVs as a secondary barrier — the GDT's higher sparkover voltage means it only fires for very fast transients that exceed the MOV's response time. See [[05-EMI Filter Design]] for filter component placement.

#### 6.1.2 MOV Degradation Monitoring

MOVs degrade with repeated surges. Monitor via:
- **Leakage current increase:** measure MOV current at rated voltage during periodic self-test
- **Thermal fuse:** MOVs with integrated thermal disconnector (prevents fire from shorted MOV)
- **Visual indicator:** optional LED indicator on AC input board for field service

### 6.2 DC Output Transient Protection

| Component | Rating | Location | Purpose |
|-----------|--------|----------|---------|
| TVS array | V_WM = 1000 V, I_PP = 600 A (10/1000 us) | Output terminals, after contactor | Lightning transient on DC cable |
| Output filter capacitor | 10 uF film, 1200 V rated | Output bus | Absorb high-frequency transients |

### 6.3 ESD Protection (IEC 61000-4-2)

| Test | Level | Applicable Surfaces |
|------|-------|-------------------|
| Contact discharge | ±8 kV | Metal enclosure, connectors, touchscreen bezel |
| Air discharge | ±15 kV | All accessible surfaces |
| Protection | TVS diodes on exposed signal lines (CAN, Ethernet, USB) | ESD-rated TVS: PESD3V3S2UT or equivalent |

---

## 7. Insulation and Hipot Testing

### 7.1 Insulation Coordination (IEC 60664-1)

| Parameter | Selection | Rationale |
|-----------|-----------|-----------|
| Pollution degree | 2 | Indoor equipment, non-conductive pollution may occur |
| Material group | IIIb | Standard FR4 PCB (CTI 175–249) |
| Overvoltage category — AC input | III | Direct connection to building mains |
| Overvoltage category — DC output | II | Downstream of isolation transformer |
| Working voltage (AC input) | 530 VAC (L-L) = 750 Vpk | Highest rated input |
| Working voltage (DC bus) | 920 VDC | Vienna PFC boost output |
| Working voltage (DC output) | 1000 VDC | Maximum output specification |
| Insulation type (primary-secondary) | Reinforced | Single-fault safe, no accessible hazardous voltage |

#### 7.1.1 Creepage and Clearance Requirements

Per IEC 60664-1 and IEC 62368-1, at PD 2, Material Group IIIb:

| Boundary | Working Voltage | Insulation | Min Clearance (mm) | Min Creepage (mm) |
|----------|---------------:|------------|--------------------:|------------------:|
| AC input to PE | 750 Vpk | Basic | 5.5 | 8.0 |
| DC bus to PE | 920 VDC | Basic | 6.0 | 8.0 |
| DC output to PE | 1000 VDC | Reinforced | 10.0 | 16.0 |
| Primary to secondary (transformer) | 920 + 1000 = 1920 V | Reinforced | 14.0 | 25.0 |
| CAN bus / signal to mains | 750 Vpk | Reinforced | 10.0 | 16.0 |

> [!warning] PCB Layout Requirement
> The primary-to-secondary clearance of 14 mm and creepage of 25 mm dictate the transformer bobbin design and the isolation barrier on the DC-DC board. This cannot be achieved with standard PCB routing — a physical slot or board edge cutout is required. See [[07-PCB-Layout/__init|07-PCB Layout]] for implementation details.

### 7.2 Hipot (Dielectric Withstand) Test Requirements

| Test | Voltage | Duration | Standard | Notes |
|------|---------|----------|----------|-------|
| AC input to PE | 3000 VAC (50/60 Hz) | 60 s | IEC 62368-1 clause 5.4.1 | Basic insulation, OVC III |
| DC bus to PE | 3500 VAC (50/60 Hz) | 60 s | IEC 62368-1 clause 5.4.1 | Reinforced if bus accessible |
| DC output to PE | 3750 VAC (50/60 Hz) | 60 s | IEC 62368-1 clause 5.4.1 | Reinforced insulation |
| Primary to secondary (transformer) | 4000 VAC (50/60 Hz) | 60 s | IEC 62368-1 clause 5.4.1 | Reinforced, highest working voltage |
| Output to chassis | 2500 VDC | 60 s | IEC 61851-23 clause 8.2 | DC test per EV charging standard |

### 7.3 Partial Discharge Testing

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| Threshold | <10 pC | At 1.5x working voltage |
| Test voltage (primary-secondary) | 1.5 x 1920 V = 2880 Vpk | Reinforced insulation boundary |
| Significance | Verifies insulation integrity without breakdown | Detects voids, contamination in bobbin/insulation tape |

### 7.4 Production (Routine) Test

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| Voltage | 80% of type-test voltage | e.g., 3200 VAC for primary-to-secondary |
| Duration | 1–2 s | Flash test for production throughput |
| Leakage limit | <5 mA at test voltage | Pass/fail criterion per unit |
| Frequency | Every unit | 100% production test |

---

## 8. Protection Response Hierarchy

The following table defines the complete protection response matrix, ordered from fastest (hardware) to slowest (thermal):

| # | Protection | Detection Method | Response Time | Immediate Action | Secondary Action | Recovery Mode |
|:-:|------------|-----------------|--------------|------------------|------------------|---------------|
| 1 | DESAT (short circuit) | Gate driver VDS monitor | <2 us | Soft turn-off of faulted MOSFET | Disable all PWM, open contactor | Latch — manual reset |
| 2 | Output OCP (HW) | External comparator | <500 ns | Disable LLC PWM via HRTIM FLT | — | Auto-retry after 1 s (3x) |
| 3 | Output OVP (HW) | Comparator (1100 V) | <1 us | Latch PWM off | Open output contactor | Latch — manual reset |
| 4 | DC bus OVP | Comparator (960 V) | <5 us | Disable PFC PWM | LLC discharges bus | Auto-retry after 5 s |
| 5 | Output OCP (cycle) | HRTIM comparator | <1 switching period | Pulse skip | Foldback to constant power | Immediate (self-recovering) |
| 6 | Input surge | MOV + GDT | <1 us | Passive clamping | — | Self-recovering |
| 7 | Output OVP (SW) | ADC + firmware | <100 us | Disable LLC PWM | Open contactor after 10 ms | Auto-retry after 1 s (3x) |
| 8 | Output short circuit | dI/dt sensor | <10 us | Disable all PWM | Open contactor | Latch — manual reset |
| 9 | Input OCP | ADC + firmware | <1 ms | Reduce PFC duty | Disable PFC if sustained | Auto after 5 s |
| 10 | DC bus OC | ADC + comparator | <100 us | Disable PFC + LLC | Full shutdown | Auto-retry after 5 s (1x) |
| 11 | Ground fault (DC) | RCM / IMD | <1 s | Open output contactor | Disable all power stages | Latch — manual reset |
| 12 | OTP (heatsink) | NTC + ADC | <1 s | Reduce power / shutdown | Open contactors | Auto when T < (trip - hysteresis) |
| 13 | Fan failure | Tachometer | 5 s | Reduce power to 50% | Shutdown if T rises | Auto when fan resumes |
| 14 | Insulation fault | IMD periodic test | 10 s (test interval) | Open output contactor | Disable all power stages | Latch — manual reset |

> [!warning] Fault Priority
> When multiple faults occur simultaneously, the hardware-latched faults (DESAT, HW OVP, HW OCP) take precedence — they act independently of firmware. The firmware state machine processes remaining faults in priority order (lowest number = highest priority) and reports the highest-priority active fault via CAN.

---

## 9. Firmware Protection Implementation

### 9.1 Protection State Machine

The firmware protection engine operates as a hierarchical state machine within the main control loop (cross-reference [[06-Firmware Architecture]]):

```
IDLE ──► PRECHARGE ──► SOFT_START ──► RUNNING ──► SHUTDOWN
  │          │              │             │            │
  │          ▼              ▼             ▼            │
  │       FAULT ◄────── FAULT ◄────── FAULT            │
  │          │                            │            │
  │          ▼                            │            │
  │      RECOVERY ────────────────────────┘            │
  │          │                                         │
  └──────────┴─────────────────────────────────────────┘
```

| State | Entry Condition | Active Protections | Exit Condition |
|-------|----------------|-------------------|----------------|
| IDLE | Power-on, CAN "standby" command | Input UV/OV monitoring only | CAN "start" command |
| PRECHARGE | Start command received | Input OV, DC bus OV, OTP, insulation test | Bus voltage within 5% of expected |
| SOFT_START | Pre-charge complete, insulation OK | All protections active | Output voltage at setpoint |
| RUNNING | Soft-start complete | All protections active | CAN "stop" or fault |
| FAULT | Any protection trip | Hardware protections remain active | Recovery timer expired or manual reset |
| RECOVERY | Fault cleared, recovery conditions met | All protections active | Transition to PRECHARGE or IDLE |
| SHUTDOWN | CAN "stop" or graceful exit | Input monitoring, OTP | Output current = 0, contactors open |

### 9.2 Fault Logging

| Field | Size | Description |
|-------|------|-------------|
| Fault code | 16 bits | Unique ID per protection (see §8 numbering) |
| Timestamp | 32 bits | System tick counter (1 ms resolution) |
| V_out at fault | 16 bits | Output voltage ADC reading |
| I_out at fault | 16 bits | Output current ADC reading |
| V_bus at fault | 16 bits | DC bus voltage |
| T_heatsink at fault | 8 bits | Hottest NTC reading (deg C) |
| T_ambient at fault | 8 bits | Inlet air temperature (deg C) |
| Operating state | 8 bits | State machine state before fault |
| Retry count | 8 bits | Number of auto-retries for this fault type |
| **Total per entry** | **16 bytes** | Stored in STM32 flash (last 4 kB sector) |

- **Capacity:** 256 fault entries in 4 kB flash sector (ring buffer, oldest overwritten)
- **Persistence:** survives power cycle; accessible via CAN diagnostic command
- **Real-time reporting:** fault code + operating data broadcast on CAN within 10 ms of fault

### 9.3 CAN Fault Reporting

| CAN ID | Message | Content | Rate |
|--------|---------|---------|------|
| 0x180 + node_id | Module Status | State, fault code, V_out, I_out, T_max | 100 ms periodic |
| 0x080 + node_id | Fault Event | Fault code, timestamp, snapshot data | On fault (event-triggered) |
| 0x580 + node_id | Fault Log Read | Response to diagnostic query | On request |

### 9.4 Watchdog and MCU Health

| Mechanism | Configuration | Action on Timeout |
|-----------|--------------|-------------------|
| Independent watchdog (IWDG) | 100 ms timeout | Full MCU reset → re-enters IDLE state |
| Window watchdog (WWDG) | 10 ms window, must refresh in 6–10 ms | Triggers NMI → can attempt graceful shutdown |
| HRTIM fault input from WWDG | Connected to FLT5 | Hardware disables all PWM if MCU hangs |
| External watchdog (optional) | TPS3823 or MAX6369 | Asserts RESET if MCU fails to toggle GPIO within 1.6 s |

> [!note] Defense in Depth
> The triple-watchdog architecture ensures that even a firmware hang or MCU lockup results in safe shutdown. The HRTIM FLT5 connection is the most critical — it ensures PWM outputs are forced to safe state (all low) within one switching period, regardless of CPU status.

---

## 10. Safety Compliance Matrix

This table maps each protection function to the applicable clause in each relevant standard:

| Protection Function | IEC 61851-23 | IEC 62368-1 | UL 2202 | EN 61000 Series |
|--------------------|-------------|-------------|---------|-----------------|
| Output OVP | §6.3.1 (voltage limits) | §5.4.2 (ES2 energy source) | §28 (overvoltage) | — |
| Output OCP | §6.3.2 (current limits) | §5.4.3 (PS2 power source) | §29 (overcurrent) | — |
| Short-circuit (DESAT) | §6.3.3 (short-circuit) | §5.4.6 (abnormal operation) | §30 (short circuit) | — |
| DC bus OVP | — (internal) | §5.4.2 | — | — |
| Input OVP/OCP | — | §5.4.2, §5.4.3 | §28, §29 | — |
| OTP (all sensors) | §6.4 (thermal) | §5.4.7 (temperature) | §36 (temperature) | — |
| Touch current / earth leakage | §6.5 (leakage) | §5.4.9 (touch current) | §27 (leakage) | — |
| Ground fault (DC RCM) | §9.4, IEC 62955 | — | §31 (ground fault) | — |
| Insulation monitoring (IMD) | §8.2 (insulation) | §5.4.1 (insulation) | §26 (insulation) | — |
| Insulation / hipot | §8.2 | §5.4.1 | §26 | — |
| Creepage / clearance | §8.3 | §5.4.1, IEC 60664-1 | §26 | — |
| Surge immunity (AC input) | — | — | — | IEC 61000-4-5 (§5.6) |
| ESD immunity | — | — | — | IEC 61000-4-2 (§5.1) |
| EFT/burst immunity | — | — | — | IEC 61000-4-4 (§5.3) |
| Conducted immunity | — | — | — | IEC 61000-4-6 (§5.7) |
| EMC emissions (conducted) | — | — | — | EN 55032 Class B |
| EMC emissions (radiated) | — | — | — | EN 55032 Class B |
| Voltage dips / interruptions | — | — | — | IEC 61000-4-11 (§5.9) |
| Harmonics | — | — | — | EN 61000-3-12 |

> [!tip] Certification Strategy
> For CE marking: self-declare to EN 61000 series (EMC directive) + have a Notified Body test to IEC 62368-1 (LVD) and IEC 61851-23 (EV charging). For UL listing: submit to UL 2202 with CB scheme test report to IEC 62368-1. Parallel submission saves 4–6 months vs. sequential testing.

---

## 11. Cross-References

| Document | Relevance to Protection Design |
|----------|-------------------------------|
| [[01-Topology Selection]] | SiC device ratings, switching parameters, DESAT thresholds |
| [[04-Thermal Budget]] | Loss allocation per device, junction-to-ambient thermal resistance, derating curves |
| [[05-EMI Filter Design]] | Surge protection components (MOV, GDT), Y-capacitor leakage current, filter placement |
| [[06-Firmware Architecture]] | HRTIM fault inputs (FLT1–FLT5), ADC trigger configuration, ISR priorities, CAN protocol |
| [[07-PCB-Layout/__init\|07-PCB Layout]] | Creepage/clearance implementation, isolation barriers, slot placement, copper pours |
| [[08-Power-On Sequence and Inrush Management]] | Pre-charge sequence, contactor control timing, insulation test before startup |
| [[00-Board Partitioning]] | Inter-board fault signal routing, isolated interface definitions |
| [[SiC Device Thermal Parameters]] | Device SOA curves, DESAT voltage characteristics, short-circuit withstand time |
| [[07-BOM and Cost Analysis]] | Protection component selection, MOV/TVS/NTC part numbers, cost impact |
