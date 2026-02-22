---
tags: [PDU, testing, V&V, certification, HALT, environmental, type-test, production-test]
created: 2026-02-22
status: draft
---

# End-to-End Test Plan — 30 kW PDU

> [!summary] Purpose
> This document defines the **full verification and validation (V&V) test plan** for the 30 kW PDU, covering the lifecycle from design verification through certification and production release. It fills the gap between the [[11-Test-Plan/01-Board-Level Test Procedure|Board-Level Test Procedure]] (prototype bring-up / DVT) and the [[12-Project-Management/03-Commissioning Procedure|Commissioning Procedure]] (field deployment). It provides the detailed test procedures, acceptance criteria, and test matrices referenced by [[12-Project-Management/Epics/EP-08 Pre-Production Validation|EP-08 Pre-Production Validation]] stories.

---

## 1. Test Strategy Overview

### 1.1 Test Phases

| Phase | Abbreviation | Purpose | Units | Primary Venue |
|-------|-------------|---------|-------|---------------|
| Design Verification Test | DVT | Prove the design meets specifications on prototype hardware | Rev A / early Rev B | In-house lab |
| Engineering Validation Test | EVT | Formal type testing, environmental qualification, reliability | Rev B (design-frozen) | In-house + accredited lab |
| Production Validation Test | PVT | Validate production test fixtures, process, and yield | Pilot production run | Factory / contract manufacturer |

### 1.2 Scope Mapping

| Test Category | DVT | EVT | PVT | Reference |
|---------------|:---:|:---:|:---:|-----------|
| Board-level bring-up (§3 of board-level procedure) | X | | | [[11-Test-Plan/01-Board-Level Test Procedure\|01-Board-Level Test Procedure]] §3 |
| System integration (§4 of board-level procedure) | X | | | [[11-Test-Plan/01-Board-Level Test Procedure\|01-Board-Level Test Procedure]] §4 |
| Efficiency sweep | X | X | | §2 below; board-level §4.2 |
| Type tests per standards (§3 below) | | X | | Accredited lab |
| Environmental qualification (§4 below) | | X | | Environmental test lab |
| HALT / burn-in (§5 below) | | X | | In-house or contract |
| Communication protocol validation (§6 below) | X | X | | In-house lab |
| Charging profile tests (§7 below) | X | X | | In-house + vehicle test |
| Production test (§8 below) | | | X | Factory |

### 1.3 Relationship to Other Documents

| Document | Role |
|----------|------|
| [[11-Test-Plan/01-Board-Level Test Procedure\|01-Board-Level Test Procedure]] | DVT-phase procedures — standalone board tests and first system integration |
| [[12-Project-Management/03-Commissioning Procedure\|Commissioning Procedure]] | PVT/field — site acceptance testing for deployed units |
| [[12-Project-Management/Epics/EP-08 Pre-Production Validation\|EP-08 Pre-Production Validation]] | Project management stories defining schedule, assignees, and gate criteria for EVT activities |
| [[09-Protection and Safety]] | Protection thresholds, hipot voltages, safety compliance matrix — normative reference for type tests |

---

## 2. Requirements Traceability Matrix

Every key specification from [[__init]] is mapped to one or more test cases. Test IDs prefixed **RTM-** are traced here; detailed procedures appear in subsequent sections.

| # | Specification | Value | Test ID(s) | Test Phase | Section |
|:-:|---------------|-------|-----------|:----------:|:-------:|
| 1 | Input voltage range | 260–530 VAC, 3-phase | RTM-01 | DVT, EVT | §3.1 |
| 2 | Input frequency range | 45–65 Hz | RTM-02 | DVT | §3.1 |
| 3 | Input current | ≤60 A per module | RTM-03 | DVT | §3.1 |
| 4 | Power factor | ≥0.99 at full load | RTM-04 | DVT, EVT | §3.1 |
| 5 | THDi | ≤5% at full load | RTM-05 | DVT, EVT | §3.1 |
| 6 | Rated output power | 30 kW (constant power) | RTM-06 | DVT, EVT | §3.1 |
| 7 | Output voltage range | 150–1000 VDC | RTM-07 | DVT, EVT | §3.1, §7 |
| 8 | Output current range | 0–100 A | RTM-08 | DVT, EVT | §3.1, §7 |
| 9 | Voltage accuracy | ±0.5% | RTM-09 | DVT | §3.1 |
| 10 | Current accuracy | ±1% | RTM-10 | DVT | §3.1 |
| 11 | Output ripple | <0.5% RMS | RTM-11 | DVT | §3.1 |
| 12 | Peak efficiency | >96% | RTM-12 | DVT, EVT | §3.1 |
| 13 | Standby power | <8 W | RTM-13 | DVT | §3.1 |
| 14 | Soft start time | ≤6 s | RTM-14 | DVT | §3.1 |
| 15 | MTBF | >120,000 hours | RTM-15 | EVT | §5 |
| 16 | CAN stacking — current imbalance | ≤5% | RTM-16 | DVT, EVT | §6.2 |
| 17 | Acoustic noise | ≤65 dB | RTM-17 | DVT, EVT | §3.1 |
| 18 | Operating temperature | −30°C to +55°C full load | RTM-18 | EVT | §4.1 |
| 19 | Storage temperature | −40°C to +85°C | RTM-19 | EVT | §4.2 |
| 20 | Protections (OVP/OCP/OTP/SC/surge) | Per [[09-Protection and Safety]] §8 | RTM-20 | DVT, EVT | §3.2, §3.3 |
| 21 | IEC 61851-23 compliance | DC EVSE requirements | RTM-21 | EVT | §3.2 |
| 22 | IEC 62368-1 compliance | Equipment safety | RTM-22 | EVT | §3.1 |
| 23 | UL 2202 compliance | North American listing | RTM-23 | EVT | §3.3 |
| 24 | CE marking (EMC) | EN 55032, EN 61000-4 series | RTM-24 | EVT | §3.4 |
| 25 | Dimensions | ~455 × 300 × 94 mm | RTM-25 | DVT | Mechanical inspection |
| 26 | Weight | ~17 kg | RTM-26 | DVT | Mechanical inspection |

---

## 3. Type Tests per Standards

### 3.1 IEC 62368-1 — Equipment Safety

| Test | Clause | Description | Level / Condition | Pass Criteria |
|------|--------|-------------|-------------------|---------------|
| Hipot: AC input → PE | 5.4.1 | Dielectric withstand | 3000 VAC, 60 s | No breakdown; leakage <5 mA |
| Hipot: DC bus → PE | 5.4.1 | Dielectric withstand | 3500 VAC, 60 s | No breakdown; leakage <5 mA |
| Hipot: DC output → PE | 5.4.1 | Dielectric withstand | 3750 VAC, 60 s | No breakdown; leakage <5 mA |
| Hipot: primary → secondary | 5.4.1 | Reinforced insulation | 4000 VAC, 60 s | No breakdown; leakage <5 mA |
| Partial discharge | 5.4.1 | Insulation integrity | 2880 Vpk (1.5× working) | <10 pC |
| Touch current | 5.4.9 | Normal operation | Rated voltage, MD network | <3.5 mA |
| Earth bond | 5.4.1 | Protective earth | 25 A for 60 s | <0.1 Ω |
| Temperature rise | 5.4.7 | All components | Rated load, max ambient | No component exceeds rated limit |
| Abnormal operation | 5.4.6 | Single-fault safety | Blocked fan, shorted output, open feedback | No fire, no hazardous voltage exposure |

> [!note] Hipot levels from [[09-Protection and Safety]] §7.2.

### 3.2 IEC 61851-23 — DC EV Charging

| Test | Clause | Description | Level / Condition | Pass Criteria |
|------|--------|-------------|-------------------|---------------|
| Output voltage limits | 6.3.1 | OVP response | 105% setpoint (SW), 1100 V (HW) | LLC off <100 µs (SW), <1 µs (HW); contactor opens |
| Output current limits | 6.3.2 | OCP response | 110 A cycle-by-cycle, 120 A hardware | Pulse skip / latch per [[09-Protection and Safety]] §3.1 |
| Short circuit | 6.3.3 | Output short-circuit | Bolted short at output terminals | DESAT <2 µs, all PWM off, contactor opens |
| Insulation monitoring | 8.2 | Pre-charge and continuous | >500 kΩ pre-charge, >100 kΩ operational | IMD trips and opens contactor if below threshold |
| DC residual current | 9.4 | Ground fault detection | >6 mA DC residual | RCM trips <1 s per IEC 62955 |
| Emergency stop | 6.3.1 | De-energization | E-stop activation at full load | V_bus <60 V within 5 s |
| Output de-energization | 6.3.1 | Normal shutdown | Shutdown command | V_bus <60 V within 5 s |

### 3.3 UL 2202 — EV Charging Equipment

| Test | Section | Description | Condition | Pass Criteria |
|------|---------|-------------|-----------|---------------|
| Overload | §29 | Sustained overcurrent | 120% rated current, 60 min | Protection operates; no fire or hazard |
| Short circuit | §30 | Bolted short | Output terminals shorted | Safe shutdown; no explosion or fire |
| Temperature | §36 | All accessible surfaces | Rated load, max ambient | Touchable surfaces <65°C at 25°C ambient |
| Abnormal operation | §28 | Blocked ventilation, component failure | Single-fault conditions | No hazard; protection operates correctly |
| Dielectric withstand | §26 | Hipot | Per IEC 62368-1 levels | No breakdown |
| Leakage current | §27 | Normal operation | Rated voltage | <3.5 mA |
| Ground fault | §31 | DC ground fault | >6 mA DC | RCM trips within 1 s |

### 3.4 EMC — EN 55032 + EN 61000-4 Series

#### 3.4.1 Emissions

| Test | Standard | Description | Limit | Condition |
|------|----------|-------------|-------|-----------|
| Conducted emissions | EN 55032 | 150 kHz – 30 MHz, QP + AVG | Class B | 30 kW, 530 VAC, LISN on each phase |
| Radiated emissions | EN 55032 | 30 MHz – 1 GHz, QP + AVG | Class B | 30 kW, 3 m distance (or 10 m) |
| Harmonics | EN 61000-3-12 | Current harmonics | Equipment >16 A: Table 4 limits | 30 kW, rated voltage |

#### 3.4.2 Immunity

| Test | Standard | Description | Level | Criterion |
|------|----------|-------------|-------|-----------|
| ESD | EN 61000-4-2 | Contact + air discharge | ±8 kV contact, ±15 kV air | B (temporary degradation, self-recovery) |
| EFT / Burst | EN 61000-4-4 | Fast transients on AC input + signal | Level 3 (2 kV AC, 1 kV signal) | B |
| Surge (L-L) | EN 61000-4-5 | AC input line-to-line | 2 kV, 1.2/50 µs | B |
| Surge (L-PE) | EN 61000-4-5 | AC input line-to-earth | 4 kV, 1.2/50 µs | B |
| Conducted immunity | EN 61000-4-6 | Injected RF on AC and signal lines | 10 V, 150 kHz – 80 MHz | A (no degradation) |
| Voltage dips | EN 61000-4-11 | Supply voltage dips/interruptions | 0% for 10 ms; 40% for 100 ms; 70% for 500 ms | B/C per depth |
| Power frequency magnetic | EN 61000-4-8 | External magnetic field | 30 A/m continuous | A |

---

## 4. Environmental Qualification

All environmental tests performed on Rev B units. Post-test functional verification: 30 kW for 10 minutes, all protections verified.

### 4.1 Temperature — Operating

| Test | Condition | Duration | Pass Criteria |
|------|-----------|----------|---------------|
| Low temperature | −30°C, full load (30 kW) | 2 hours at steady state | Operates within spec; startup ≤7 s (relaxed from 6 s per [[08-Power-On Sequence and Inrush Management]] §8.2); all protections functional |
| High temperature | +55°C, full load (30 kW) | 2 hours at steady state | Operates at rated power; thermal derating curve matches [[04-Thermal Budget]] §5.2; Tj_max ≤140°C (LLC diode, per §4.2) |
| Temperature sweep | −30°C → +55°C, 2°C/min ramp, at 15 kW | Full sweep (~45 min) | No fault, no loss of regulation, no audible anomaly |

### 4.2 Temperature — Storage

| Test | Condition | Duration | Pass Criteria |
|------|-----------|----------|---------------|
| Low storage | −40°C, unpowered | 24 hours | Post-test functional pass at 25°C; no cracked components or solder joints |
| High storage | +85°C, unpowered | 24 hours | Post-test functional pass at 25°C; capacitor ESR within 20% of pre-test |

### 4.3 Humidity

| Test | Condition | Duration | Pass Criteria |
|------|-----------|----------|---------------|
| Damp heat (steady-state) | 40°C, 93% RH, non-condensing | 96 hours | Hipot pass after (at type-test levels per §3.1); no corrosion; insulation resistance >10 MΩ; post-test functional pass |

### 4.4 Altitude

| Test | Condition | Pass Criteria |
|------|-----------|---------------|
| Standard | 2000 m (reduced air density → reduced cooling) | Full 30 kW at ≤45°C ambient; derating above 45°C acceptable |
| Extended (optional) | 3000 m | 25 kW at ≤40°C ambient; document derating curve |

> [!note] Altitude testing may be simulated by reducing fan airflow by the altitude correction factor (air density at 2000 m ≈ 80% of sea level).

### 4.5 Vibration — Operational

| Parameter | Value |
|-----------|-------|
| Frequency range | 5–500 Hz |
| Acceleration | 1g RMS |
| Axes | 3 (X, Y, Z) |
| Duration per axis | 2 hours |
| Condition | Powered, 15 kW load |
| Pass criteria | No fault, no loss of regulation, no mechanical failure; post-test visual: no cracked solder, no loose connectors |

### 4.6 Vibration — Transport

| Parameter | Value |
|-----------|-------|
| Frequency range | 5–500 Hz |
| Acceleration | 2g RMS |
| Axes | 3 (X, Y, Z) |
| Duration per axis | 1 hour |
| Condition | Unpowered, packaged |
| Pass criteria | Post-test functional pass; no mechanical damage |

### 4.7 Mechanical Shock

| Parameter | Value |
|-----------|-------|
| Acceleration | 15g |
| Pulse duration | 11 ms (half-sine) |
| Axes | 3 (X, Y, Z), both directions |
| Pulses per direction | 3 |
| Condition | Unpowered |
| Pass criteria | Post-test functional pass; no mechanical damage, no displaced components |

---

## 5. Reliability and Endurance

### 5.1 HALT Profile

Per [[12-Project-Management/Epics/EP-08 Pre-Production Validation|EP-08-005]]: 500 hours at rated power on 2 Rev B units.

| Segment | Duration | Conditions | Data Capture |
|---------|----------|-----------|--------------|
| Initial characterization | 4 hours | 30 kW at 25°C, full instrumentation | Efficiency, V_out, I_out, all NTC temps, waveform captures |
| Burn-in block 1 | 168 hours (1 week) | 30 kW at 45°C ambient | V_out, I_out, temps, fault events logged every 10 s |
| Thermal cycling | 100 hours | −30°C to +55°C, 2 hr/cycle, 50 cycles at 15 kW | Same as block 1 |
| Burn-in block 2 | 168 hours | 30 kW at 25°C ambient | Same |
| Final block | 64 hours | 30 kW at 55°C (derated per [[04-Thermal Budget]] §5.2) | Same |
| Final characterization | 4 hours | 30 kW at 25°C, full instrumentation | Same as initial — compare for degradation |

**Acceptance criteria:**
- Zero unplanned shutdowns (thermal derate at 55°C is expected, not a failure)
- Efficiency degradation <0.2% (initial vs. final characterization)
- No component temperature drift >5°C from initial characterization
- No fan RPM degradation >10%

### 5.2 MTBF Calculation Method

| Parameter | Value |
|-----------|-------|
| Method | Chi-squared, 90% confidence, zero-failure assumption |
| Formula | MTBF = 2T / χ²(2, 0.10) where T = total device-hours |
| Target | >120,000 hours |
| With 2 units × 500 hours = 1,000 device-hours and 0 failures | MTBF ≥ 2 × 1,000 / 4.61 = 434 hours (insufficient for claim) |

> [!warning] Statistical significance
> 1,000 device-hours with zero failures only demonstrates MTBF ≥434 hours at 90% confidence — far short of the 120,000-hour target. The 500-hour HALT is primarily a **design robustness** screen, not a statistical MTBF demonstration. The MTBF claim is supported by:
> 1. Component-level reliability data (datasheet MTBF / FIT rates)
> 2. Parts-count MTBF analysis per MIL-HDBK-217F or Telcordia SR-332
> 3. Thermal margin analysis ([[04-Thermal Budget]] §8) — all junctions well within derating
> 4. Capacitor life calculation ([[04-Thermal Budget]] §8.1) — Arrhenius model confirms >113,000 hours at 90°C

### 5.3 Capacitor Life Verification

| Parameter | Method | Acceptance |
|-----------|--------|------------|
| Electrolytic capacitor life | Arrhenius model: L = L₀ × 2^((T_rated − T_actual)/10) | Calculated life >120,000 hours at worst-case measured temperature |
| Cross-check | Compare measured capacitor temperature from HALT (§5.1) against [[04-Thermal Budget]] §8.1 prediction | Measured T_cap within 5°C of prediction |
| ESR drift | Measure ESR at initial and final characterization (LCR meter, 100 kHz) | ESR increase <20% |

### 5.4 Fan Life Verification

| Parameter | Method | Acceptance |
|-----------|--------|------------|
| Tachometer monitoring | Log fan RPM every 10 s throughout 500-hour burn-in | RPM within ±5% of initial at same PWM duty |
| Acoustic drift | Sound level measurement at initial and final characterization | Increase <3 dB |
| Bearing type | Verify dual ball bearing or FDB per [[04-Thermal Budget]] §8.2 | Datasheet MTBF >70,000 hours at rated speed |

---

## 6. Communication Protocol Validation

### 6.1 CAN Bus — Single Module

| Test ID | Test | Condition | Pass Criteria |
|---------|------|-----------|---------------|
| CAN-01 | Frame integrity | 100,000 frames at 500 kbps | 0 CRC errors, 0 frame errors |
| CAN-02 | Timing accuracy | Status frame (10 ms period) over 24 hours | Jitter <1 ms; no missed frames |
| CAN-03 | Error rate | 24-hour soak at 30 kW, noisy environment (near switching) | Error frame rate <0.001% |
| CAN-04 | Bus-off recovery | Force bus-off (inject dominant errors) | Auto-recovery within 1 s; module re-enters RUN |
| CAN-05 | Baud rate tolerance | ±2% oscillator drift (simulated) | Communication maintained |

### 6.2 CAN Stacking — Multi-Module

| Test ID | Test | Condition | Pass Criteria |
|---------|------|-----------|---------------|
| STK-01 | 2-module current sharing | 60 kW total, 400 V output | Imbalance ≤5% per [[06-Firmware Architecture]] §6.3 |
| STK-02 | 5-module current sharing | 150 kW total, 800 V output | Imbalance ≤5% across all modules |
| STK-03 | Hot-swap (add module) | Running at 120 kW (4 modules); add 5th | Seamless ramp to 150 kW; V_out transient <5% |
| STK-04 | Hot-swap (remove module) | Running at 150 kW; disconnect 1 module | Remaining 4 absorb load; V_out dip <5%; no fault |
| STK-05 | Master failover | Disconnect master CAN while 2+ modules run | Slave promotes to master within 200 ms; output maintained |
| STK-06 | Node ID assignment | 5 modules, random power-on order | Unique IDs assigned; no conflicts |
| STK-07 | CAN timeout (slave) | Remove command frames for 50 ms / 200 ms | Derate to 50% at 50 ms; full shutdown at 200 ms per [[06-Firmware Architecture]] §6.3 |

### 6.3 OCPP 1.6

Testing is performed at the charger controller level; the PDU module responds via internal CAN setpoints per [[06-Firmware Architecture]] §8.

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| OCPP-01 | Heartbeat | Controller sends Heartbeat every 30 s; backend acknowledges |
| OCPP-02 | RemoteStartTransaction | PDU receives V/I setpoint via CAN; output enables within 6 s |
| OCPP-03 | RemoteStopTransaction | PDU ramps to 0 A; contactor opens; controller reports StopTransaction |
| OCPP-04 | MeterValues | PDU_Status aggregated; kWh, V, I, T reported to backend every 60 s |
| OCPP-05 | StatusNotification | PDU fault code → OCPP Faulted status; clear → Available |
| OCPP-06 | FirmwareUpdate | DataTransfer with firmware image; PDU enters bootloader and updates |

### 6.4 ISO 15118

Testing requires a SECC (Supply Equipment Communication Controller) and optionally an EV simulator or real vehicle.

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| ISO-01 | CurrentDemand response | SECC sends EVTargetVoltage/Current; PDU regulates to setpoint within 500 ms |
| ISO-02 | PowerDelivery start/stop | Session start → output on; session stop → controlled shutdown |
| ISO-03 | Session establishment | SECC-EV handshake completes; CAN setpoint received by PDU |
| ISO-04 | Session teardown | Clean termination; contactor opens; PDU enters IDLE |
| ISO-05 | Plug & Charge (if SECC supports) | TLS authentication, contract certificate exchange, seamless session start |

---

## 7. Charging Profile Tests

### 7.1 CCS Combo Simulation

Simulate a standard CCS charging curve using an electronic load in CV/CC mode or a battery simulator.

| Phase | V_out (V) | I_out (A) | Duration | Verify |
|-------|-----------|-----------|----------|--------|
| Pre-charge | 0 → 400 | 0 | ≤6 s | Startup timing ≤6 s |
| CC ramp | 400 | 0 → 75 | ~10 s | Smooth ramp, no overshoot >5 A |
| CC hold | 400 | 75 | 10 min | V_out ±0.5%, I_out ±1%, efficiency >96% |
| CV transition | 400 → 420 | 75 → taper | ~30 s | Smooth CC→CV, no oscillation |
| CV taper | 420 | 75 → 5 | 5 min | Voltage regulation ±0.5% |
| Termination | 420 | <2 | — | PDU detects end-of-charge; shutdown clean |

### 7.2 CHAdeMO Simulation

| Phase | Test | Pass Criteria |
|-------|------|---------------|
| Handshake | Protocol handshake via CAN (simulated CHAdeMO controller) | Sequence completes within 5 s |
| Current demand | Step I_out 0 → 50 A → 100 A | PDU tracks demand within ±1 A |
| Voltage regulation | V_out at 200 V, 400 V, 500 V | Regulation ±0.5% |
| Session termination | Stop request from vehicle | Current ramps to 0; contactor opens |

### 7.3 Real Vehicle Test (If Available)

| Test | Setup | Pass Criteria |
|------|-------|---------------|
| End-to-end charge session | PDU + SECC + CCS cable + production EV | Complete charge session from plug-in to termination without fault |
| Multi-module session | 2+ PDU modules + SECC + EV | Load shared; vehicle charges normally |

### 7.4 Edge Cases

| Test ID | Test | Condition | Pass Criteria |
|---------|------|-----------|---------------|
| EDGE-01 | Maximum voltage | V_out = 1000 V, I_out = 30 A | Regulation ±0.5%; no OVP trip |
| EDGE-02 | Maximum current | V_out = 300 V, I_out = 100 A | Regulation ±1%; no OCP trip |
| EDGE-03 | Minimum voltage | V_out = 150 V, I_out = 100 A (15 kW) | Regulation ±1%; stable LLC operation |
| EDGE-04 | Minimum input voltage | 260 VAC, 30 kW | All specs met; PFC current ≤60 A/phase |
| EDGE-05 | Maximum input voltage | 530 VAC, 30 kW | All specs met; DC bus ≤920 V |
| EDGE-06 | Rapid start/stop cycling | 100 start/stop cycles, 30 s interval, 15 kW | No faults; NTC energy within rating; relay contacts OK |
| EDGE-07 | Load rejection | 30 kW → 0 kW step (load disconnect) | V_out overshoot <5% of setpoint; OVP does not trip |
| EDGE-08 | Load step | 0 → 30 kW step (CC mode) | Settling <500 ms; no undershoot below 90% of setpoint |

---

## 8. Production Test Specification

### 8.1 Flash Hipot

| Test | Voltage | Duration | Pass Criteria |
|------|---------|----------|---------------|
| AC input → PE | 2400 VAC (80% of 3000 V type-test) | 1–2 s | No breakdown; leakage <5 mA |
| DC bus → PE | 2800 VAC (80% of 3500 V) | 1–2 s | No breakdown; leakage <5 mA |
| DC output → PE | 3000 VAC (80% of 3750 V) | 1–2 s | No breakdown; leakage <5 mA |
| Primary → secondary | 3200 VAC (80% of 4000 V) | 1–2 s | No breakdown; leakage <5 mA |

> [!note] Flash hipot at 80% of type-test voltage per [[09-Protection and Safety]] §7.4.

### 8.2 Functional Test

| Step | Test | Condition | Pass Criteria | Time |
|------|------|-----------|---------------|------|
| 1 | Power-on | 400 VAC input | Startup ≤6 s; no faults | 10 s |
| 2 | Output regulation — point 1 | 400 V, 25 A (10 kW) | V_out ±0.5%, I_out ±1% | 30 s |
| 3 | Output regulation — point 2 | 800 V, 37.5 A (30 kW) | V_out ±0.5%, I_out ±1% | 30 s |
| 4 | Efficiency | 30 kW operating point | >96% | Included in step 3 |
| 5 | Protection verify | Inject OVP test signal (1100 V threshold) | PWM latches off <1 µs | 10 s |
| 6 | CAN check | Query status frame | Valid response with correct V/I readings | 5 s |
| 7 | Fan verify | Check tachometer on all 3 fans | RPM within ±10% of expected | 5 s |
| 8 | Shutdown | Normal shutdown command | Clean shutdown; V_bus <60 V within 5 s | 10 s |
| **Total functional test** | | | | **~2 min** |

### 8.3 Burn-In (Production)

| Parameter | Value |
|-----------|-------|
| Load | 80% of rated (24 kW) |
| Ambient | 45°C |
| Duration | 4 hours |
| Monitoring | V_out, I_out, all NTC temps, fault events logged |
| Pass criteria | No faults; no temperature anomaly; V_out within ±1% of setpoint throughout |

### 8.4 Test Time Budget

| Stage | Duration | Notes |
|-------|----------|-------|
| Visual inspection | 2 min | Automated optical inspection (AOI) on PCBs |
| Flash hipot (4 tests) | 2 min | Automated hipot tester with sequencer |
| Functional test | 2 min | Automated test fixture with electronic load |
| CAN + fan check | 1 min | Part of functional test |
| Data logging / labeling | 1 min | Serial number, test result archive |
| **Subtotal (excluding burn-in)** | **~8 min** | **Target <15 min met** |
| Production burn-in | 4 hours | Batch — multiple units in parallel on burn-in rack |

### 8.5 Test Fixture Requirements

| Item | Specification |
|------|---------------|
| AC source | Programmable, 0–530 VAC, 60 A, 30 kVA |
| DC electronic load | 30 kW, 0–1200 V, 0–100 A, CC/CV/CP modes |
| Hipot tester | Automated sequencer, 4 test programs, 5 kV AC, foot-switch interlock |
| CAN interface | PCAN-USB or custom fixture with automated query/verify |
| Temperature monitor | Read NTC channels via CAN or dedicated ADC fixture |
| Bed-of-nails fixture | Custom per PCB — contact pads for power, signal, and measurement |
| Software | Custom test executive with pass/fail logging, serial number tracking, database |

---

## 9. Certification Test Matrix

| Standard | Test Category | Accredited Lab | Est. Duration | EP-08 Story | Status |
|----------|--------------|----------------|---------------|-------------|--------|
| EN 55032 Class B | Conducted emissions | TBD | 3 days | EP-08-002 | Backlog |
| EN 55032 Class B | Radiated emissions | TBD | 3 days | EP-08-002 | Backlog |
| EN 61000-4-2 | ESD | TBD | 1 day | EP-08-002 | Backlog |
| EN 61000-4-4 | EFT / Burst | TBD | 1 day | EP-08-002 | Backlog |
| EN 61000-4-5 | Surge | TBD | 2 days | EP-08-004 | Backlog |
| EN 61000-4-6 | Conducted immunity | TBD | 1 day | EP-08-002 | Backlog |
| EN 61000-4-8 | Power frequency magnetic | TBD | 0.5 day | EP-08-002 | Backlog |
| EN 61000-4-11 | Voltage dips | TBD | 1 day | EP-08-002 | Backlog |
| EN 61000-3-12 | Harmonics | TBD | 1 day | EP-08-002 | Backlog |
| IEC 62368-1 | Hipot / insulation / touch current / temp rise | TBD | 5 days | EP-08-003 | Backlog |
| IEC 62368-1 | Abnormal operation / partial discharge | TBD | 3 days | EP-08-003 | Backlog |
| IEC 61851-23 | Output voltage/current limits, insulation monitoring, ground fault, RCM, e-stop | TBD | 5 days | EP-08-003 | Backlog |
| UL 2202 | Overload, short circuit, temperature, leakage, ground fault | TBD | 5 days | EP-08-003 | Backlog |
| — | Environmental (humidity, vibration, shock) | In-house or contract | 8 days | EP-08-006 | Backlog |
| — | HALT / 500-hour burn-in | In-house | 21+ days | EP-08-005 | Backlog |

---

## 10. Test Infrastructure and Lab Requirements

### 10.1 DVT Lab Equipment

Reference the equipment list in [[11-Test-Plan/01-Board-Level Test Procedure|01-Board-Level Test Procedure]] §1 for core lab instruments (AC source, electronic loads, oscilloscope, probes, power analyzer, DMMs, hipot tester, etc.).

### 10.2 Additional EVT/PVT Equipment

| # | Equipment | Specification | Purpose |
|:-:|-----------|---------------|---------|
| 1 | Thermal chamber | −40°C to +85°C, interior ≥0.5 m³, with power/signal feedthroughs | Temperature operating/storage, HALT thermal cycling |
| 2 | LISN (3×) | 50 µH / 50 Ω, 50 A per phase, 150 kHz – 30 MHz | Conducted emissions measurement |
| 3 | EMC receiver / spectrum analyzer | 9 kHz – 1 GHz, CISPR quasi-peak + average detectors | Emissions measurement |
| 4 | Near-field probe set | H-field and E-field probes, 30 MHz – 1 GHz | Pre-compliance radiated scan |
| 5 | Surge generator | 1.2/50 µs voltage, 8/20 µs current, up to 6 kV / 3 kA | IEC 61000-4-5 surge immunity |
| 6 | ESD simulator | ±15 kV air, ±8 kV contact | IEC 61000-4-2 |
| 7 | EFT/Burst generator | Up to 4 kV, 5/50 ns pulse | IEC 61000-4-4 |
| 8 | Vibration table | 5–500 Hz, 2g, 3-axis (or single-axis with repositioning) | Vibration and shock testing |
| 9 | Sound level meter | Class 2, A-weighted, 30–130 dB | Acoustic noise measurement |
| 10 | Battery simulator (optional) | 150–1000 VDC, 100 A sink, programmable V/I curve | Realistic EV charging simulation |
| 11 | SECC / charger controller | ISO 15118 + OCPP 1.6 capable | Communication protocol validation |
| 12 | CCS combo cable + connector | 1000 V, 200 A rated | Vehicle interface testing |
| 13 | CHAdeMO adapter (optional) | Standard CHAdeMO connector + protocol simulator | CHAdeMO protocol testing |

### 10.3 Production Test Fixtures

See §8.5 above for fixture specifications. Additional requirements:

- **Burn-in rack:** Accommodates 8–16 units simultaneously, with individual AC supply, shared electronic load (or individual resistive loads), temperature monitoring, and automated data logging
- **Test station integration:** Barcode scanner for serial number, automated test sequence, pass/fail database, label printer
- **Calibration:** All measurement instruments calibrated annually per ISO/IEC 17025; calibration certificates on file

---

## 11. Cross-References

| Document | Relevance |
|----------|-----------|
| [[__init]] | All PDU specifications — source for requirements traceability (§2) |
| [[11-Test-Plan/01-Board-Level Test Procedure\|01-Board-Level Test Procedure]] | DVT-phase procedures, equipment list, board-level pass/fail criteria |
| [[09-Protection and Safety]] | Protection thresholds (§8), hipot levels (§7.2), safety compliance matrix (§10), surge protection components (§6) |
| [[04-Thermal Budget]] | Thermal limits (§4.2), derating curve (§5.2), capacitor life (§8.1), fan life (§8.2) |
| [[06-Firmware Architecture]] | CAN protocol (§6), OCPP interface (§8), protection state machine (§7), HRTIM fault mapping (§7.1) |
| [[08-Power-On Sequence and Inrush Management]] | Startup timing (§5.2), cold-start analysis (§8), shutdown sequences (§6) |
| [[12-Project-Management/03-Commissioning Procedure\|Commissioning Procedure]] | Field commissioning — downstream of this test plan |
| [[12-Project-Management/Epics/EP-08 Pre-Production Validation\|EP-08 Pre-Production Validation]] | Project stories: EP-08-002 (EMC), EP-08-003 (safety), EP-08-005 (HALT), EP-08-006 (environmental) |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
