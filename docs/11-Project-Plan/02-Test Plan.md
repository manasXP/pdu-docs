---
tags: [pdu, project-plan, testing, verification]
created: 2026-02-22
---

# 02 — Test Plan

This document defines the test strategy and procedures for the 30 kW PDU, covering board-level verification through formal EMC and safety certification testing.

> [!note] See [[01-Development Phases]] for when each test stage is executed.

## Test Strategy Overview

Testing follows a progressive approach — from individual board tests to full system certification:

```
Board-Level → Sub-System → System → Environmental → EMC → Safety
```

| Stage | Phase | Units | Environment |
|-------|-------|-------|-------------|
| Board-Level | 1, 2 | Rev A (5 units) | Bench |
| Sub-System | 2, 3 | Rev A | Lab (3-phase source + load) |
| System | 3 | Rev A | Lab (full power) |
| Environmental | 7 | Rev B (2 units) | Environmental chamber |
| EMC | 6 (pre), 7 (formal) | Rev B (2 units) | EMC chamber / accredited lab |
| Safety | 6 (pre), 7 (formal) | Rev B (2 units) | Safety lab / accredited lab |

## Test Equipment Required

| Equipment | Specification | Use |
|-----------|--------------|-----|
| Programmable AC source | 3-phase, 0–530 VAC, 30+ kW | PFC input |
| Electronic DC load | 0–1000 V, 0–100 A, 30 kW | Output loading |
| Power analyzer | 3-phase, 0.1% accuracy (e.g., Yokogawa WT5000) | Efficiency, PF, THD |
| Oscilloscope | 4-ch, ≥500 MHz, isolated probes | Waveform capture |
| Thermal camera | -20 to +250°C | Hot spot identification |
| Multimeter (calibrated) | 6.5 digit | DC measurements |
| Current probes | AC/DC, 100 A, ≥50 MHz BW | Current waveforms |
| HV differential probes | 1000 V, ≥100 MHz BW | Voltage waveforms |
| Insulation tester | 5 kV DC, >100 GΩ range | Insulation resistance |
| Hipot tester | 5 kVAC, leakage measurement | Dielectric strength |
| Earth bond tester | 25 A, 0–1 Ω | PE continuity |
| Environmental chamber | -40 to +85°C, humidity control | Thermal/humidity testing |

---

## Stage 1 — Board-Level Tests

### BLT-01: Smoke Test (Per Board)

| Step | Action | Pass Criteria |
|------|--------|---------------|
| 1 | Visual inspection (magnification) | No solder bridges, missing components, polarity errors |
| 2 | Check resistance between power rails and GND | >10 kΩ (no shorts) |
| 3 | Apply auxiliary 12 V (current limited to 500 mA) | No excess current draw; no smoke or heat |
| 4 | Measure all voltage rails | Within ±5% of nominal |
| 5 | Check quiescent current | Within expected range per design |
| 6 | Touch test — feel for hot components | No unexpected heating |

### BLT-02: Rail Verification

| Rail | Nominal | Tolerance | Load (mA) | Regulator |
|------|---------|-----------|-----------|-----------|
| +3.3 V (digital) | 3.30 V | ±3% | 200 | LDO |
| +5.0 V (logic) | 5.00 V | ±3% | 300 | Buck |
| +12 V (fan, relay) | 12.0 V | ±5% | 1000 | Flyback |
| +15 V (gate driver) | 15.0 V | ±3% | 100 per driver | Isolated DC-DC |
| −5 V (gate driver) | −5.0 V | ±5% | 50 per driver | Isolated DC-DC |

### BLT-03: MCU Functional Test

| Step | Action | Pass Criteria |
|------|--------|---------------|
| 1 | Connect SWD debugger | Device ID reads correctly |
| 2 | Flash test firmware | Programming successful, CRC match |
| 3 | Toggle GPIO outputs | All outputs verified with scope/LED |
| 4 | Read GPIO inputs | All inputs respond correctly |
| 5 | UART echo test | Bidirectional communication at 115200 baud |
| 6 | LED/indicator test | All indicators functional |

### BLT-04: Gate Driver Verification

| Step | Action | Pass Criteria |
|------|--------|---------------|
| 1 | Verify isolated supply voltages (+15 V / −5 V) | Within ±3% |
| 2 | Apply PWM input (1 kHz, 50%) with no power stage | Output follows input; propagation delay <100 ns |
| 3 | Verify DESAT / fault output | Trips correctly when simulated |
| 4 | Measure dead-time | Within 80–120 ns target |
| 5 | CMTI test (if possible at board level) | No false triggering at 50 V/ns |

---

## Stage 2 — Sub-System Tests

### SST-01: PFC Stage Characterization

| Test | Conditions | Pass Criteria |
|------|-----------|---------------|
| PFC efficiency | 400 VAC, 25/50/75/100% load | >97% at 50–100% load |
| Power factor | 400 VAC, 25/50/75/100% load | ≥0.99 at 100% load; ≥0.97 at 25% load |
| THDi | 400 VAC, 25/50/75/100% load | ≤5% at full load; ≤8% at 25% load |
| DC bus regulation | 400 VAC, load step 0→100% | Bus voltage within ±5% during transient; settles in <20 ms |
| DC bus ripple | 400 VAC, 100% load | <10 Vpp at 800 VDC |
| Input voltage range | 260/400/480/530 VAC, 75% load | Stable operation across range |
| Inrush current | Cold start at 400 VAC | <25 A peak per [[08-Power-On Sequence and Inrush Management]] |
| PFC startup time | 400 VAC, no load | DC bus reaches 800 V within 6 s |

### SST-02: LLC Stage Characterization

| Test | Conditions | Pass Criteria |
|------|-----------|---------------|
| LLC efficiency | 800 VDC input, 25/50/75/100% load, 400 V out | >98% at 50–100% load |
| Output voltage regulation | Load step 25→100% | ±0.5% steady-state; <2% transient |
| Output ripple | 100% load | <0.5% RMS of output voltage |
| ZVS verification | 25/50/75/100% load | Drain waveform shows ZVS at all loads |
| Gain curve | Sweep V_out 150–1000 V at 50% load | Matches [[03-LLC Gain Curve Verification]] within 5% |
| Frequency range | Min/max load across output range | Within 100–300 kHz design range |
| Soft start | From 0 to rated output | Monotonic rise, no overshoot >5% |
| Short circuit response | Apply short at output | Trip in <10 us; no damage |

### SST-03: Thermal Pre-Characterization

| Test | Measurement Points | Pass Criteria |
|------|-------------------|---------------|
| SiC MOSFET case temp | PFC and LLC switches | Per [[04-Thermal Budget]] derating curve |
| Transformer hot spot | LLC transformer core/winding | <130°C (Class F insulation) |
| PFC inductor temp | Core surface | <120°C |
| Capacitor temp | DC bus electrolytics, output film | <85°C (electrolytic); <105°C (film) |
| Heatsink temp | Base near mounting points | <80°C at 45°C ambient |
| PCB temp | Near power traces | <110°C |
| Ambient exhaust | Fan outlet | <70°C above ambient |

---

## Stage 3 — System-Level Tests

### SYS-01: Full Power 30 kW Steady State

| Parameter | Condition | Pass Criteria |
|-----------|----------|---------------|
| Output power | 30 kW continuous, 1 hour | Stable, no trips or derating |
| System efficiency | 400 VAC in, 400 VDC out, 30 kW | >96% (target >98%) |
| Thermal equilibrium | 30 kW, 25°C ambient | All temps per [[04-Thermal Budget]] |
| Output ripple | 30 kW, 400 VDC | <0.5% RMS |
| Input PF | 30 kW, 400 VAC | ≥0.99 |
| Input THDi | 30 kW, 400 VAC | ≤5% |
| Acoustic noise | 30 kW, 1 m distance | ≤65 dB(A) |

### SYS-02: CC/CV Charging Profile

| Test | Conditions | Pass Criteria |
|------|-----------|---------------|
| CC mode accuracy | Set 75 A, measure at load | ±1% of set point |
| CV mode accuracy | Set 400 V, measure at output | ±0.5% of set point |
| CC→CV transition | Ramp voltage at 75 A until CV limit | Smooth transition, no overshoot >1% |
| Dynamic load response | 50%→100% step in CC mode | Recovery <5 ms, overshoot <3% |
| Zero-cross response | 0 A → 75 A step | Output current within 10 ms |
| Minimum load | 100 W (1 A at 100 V) | Stable regulation |

### SYS-03: Input Voltage Transients

| Test | Conditions | Pass Criteria |
|------|-----------|---------------|
| Low line | 260 VAC, 75% load | Stable operation; no trip |
| High line | 530 VAC, 75% load | Stable operation; no OVP trip |
| Brownout | 400→200→400 VAC in 100 ms | Graceful shutdown and auto-restart |
| Phase loss | Remove 1 phase at 50% load | Controlled shutdown; no damage |
| Frequency sweep | 45–65 Hz at 400 VAC, 50% load | Stable operation |

### SYS-04: 5-Module CAN Stacking

| Test | Conditions | Pass Criteria |
|------|-----------|---------------|
| 2-module power sharing | 60 kW total | Current imbalance <5% |
| 5-module power sharing | 150 kW total | Current imbalance <5% |
| Module hot-plug | Add module at 120 kW | Seamless integration, no transient >5% |
| Module hot-unplug | Remove module at 150 kW | Remaining modules absorb load; no trip |
| Master failover | Kill master at 150 kW | New master elected; <100 ms recovery |
| CAN bus fault | Disconnect CAN on 1 module | Module drops off; others continue |
| Mixed firmware | Units with v1.0 and v1.1 | Compatible operation |

### SYS-05: Protection Verification

| Test | Expected Response | Recovery |
|------|------------------|----------|
| Output overvoltage (>1050 V) | OVP trip in <100 us | Manual reset |
| Output overcurrent (>110 A) | OCP trip in <10 us | Auto-retry ×3, then latch |
| DC bus overvoltage (>900 V) | Bus OVP trip | Auto-restart after 5 s |
| Overtemperature (heatsink >95°C) | OTP derate, then trip at 105°C | Auto-restart when <85°C |
| Short circuit (output) | SCF trip in <5 us | Manual reset |
| Ground fault (>30 mA) | GFI trip | Manual reset |
| Fan failure | Derate to 50%, then OTP | Auto-restart when fan restored |
| Watchdog timeout | Safe state (all PWM off) | Auto-restart |

---

## Stage 4 — Environmental Tests

### ENV-01: Thermal Cycling

| Parameter | Value |
|-----------|-------|
| Temperature range | −30°C to +70°C |
| Ramp rate | 10°C/min |
| Dwell time | 30 min at each extreme |
| Cycles | 100 |
| During test | Unit powered, 50% load |
| Pass criteria | No performance degradation; no physical damage |

### ENV-02: Vibration

| Parameter | Value |
|-----------|-------|
| Type | Random vibration |
| Spectrum | 5–500 Hz, 2 Grms |
| Duration | 30 min per axis (X, Y, Z) |
| Condition | Powered, no load |
| Pass criteria | No loose connections; functional after |

### ENV-03: Humidity

| Parameter | Value |
|-----------|-------|
| Conditions | 40°C, 93% RH |
| Duration | 96 hours (4 days) |
| Post-test | Insulation resistance >1 MΩ; hipot pass |
| Pass criteria | No corrosion; full functionality |

### ENV-04: HALT (Highly Accelerated Life Test)

| Step | Stress | Dwell | Goal |
|------|--------|-------|------|
| Cold step | −10°C, −20°C, −30°C, −40°C, −50°C, −60°C | 10 min each | Find lower operating limit |
| Hot step | +55°C, +65°C, +75°C, +85°C, +95°C, +105°C | 10 min each | Find upper operating limit |
| Vibration step | 5, 10, 15, 20, 30, 40, 50 Grms | 10 min each | Find vibration operating limit |
| Combined | Thermal extremes + vibration | 10 min each | Find combined operating limit |
| Destruct | Beyond operating limits | Until failure | Find destruct limits |

> [!warning] HALT is a qualitative test — no formal pass/fail. Goal is to discover failure modes and verify adequate margin. Target: operating limits ≥20% beyond specification.

### ENV-05: Burn-In

| Parameter | Value |
|-----------|-------|
| Units | 10 |
| Load | 30 kW continuous |
| Ambient | 45°C |
| Duration | 500 hours |
| Monitoring | Efficiency, temperatures, output ripple (logged every 60 s) |
| Pass criteria | 0 failures; no parameter drift >2% |

---

## Stage 5 — EMC Tests

Reference standards: EN 55032, EN 61000-series, IEC 61851-23 (Annex AA)

### EMC-01: Conducted Emissions

| Parameter | Value |
|-----------|-------|
| Standard | CISPR 32 / EN 55032 Class B |
| Frequency range | 150 kHz – 30 MHz |
| Detector | Quasi-peak and average |
| LISN | 50 Ω / 50 uH, V-network |
| Conditions | 400 VAC in, 100% load, 400 VDC out |
| Margin target | 6 dB below limit (pre-compliance) |

### EMC-02: Radiated Emissions

| Parameter | Value |
|-----------|-------|
| Standard | CISPR 32 / EN 55032 Class B |
| Frequency range | 30 MHz – 1 GHz (6 GHz if required) |
| Distance | 10 m (or 3 m with correction) |
| Antenna | Bilog / horn |
| Conditions | 400 VAC in, 100% load |
| Margin target | 3 dB below limit (pre-compliance) |

### EMC-03: Harmonics

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-3-2 Class A |
| Measurement | Harmonic currents up to 40th order |
| Conditions | 400 VAC, 25/50/75/100% load |
| Pass criteria | All harmonics within Class A limits |

### EMC-04: Surge Immunity

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-5 |
| Level | ±2 kV line-to-line, ±4 kV line-to-earth |
| Coupling | 12/50 us combination wave |
| Criteria | Performance Criterion B (temporary degradation OK, self-recoverable) |

### EMC-05: ESD Immunity

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-2 |
| Level | ±8 kV contact, ±15 kV air discharge |
| Application | All accessible metal surfaces, connectors |
| Criteria | Performance Criterion B |

### EMC-06: EFT/Burst Immunity

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-4 |
| Level | ±2 kV on power lines, ±1 kV on signal lines |
| Repetition rate | 5 kHz |
| Criteria | Performance Criterion B |

### EMC-07: Conducted RF Immunity

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-6 |
| Level | 10 Vrms (150 kHz – 80 MHz) |
| Modulation | 80% AM, 1 kHz |
| Criteria | Performance Criterion A |

### EMC-08: Radiated RF Immunity

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-3 |
| Level | 10 V/m (80 MHz – 2.7 GHz) |
| Modulation | 80% AM, 1 kHz |
| Criteria | Performance Criterion A |

### EMC-09: Voltage Dips and Interruptions

| Parameter | Value |
|-----------|-------|
| Standard | IEC 61000-4-11 |
| Dips | 0%, 40%, 70% of nominal; 0.5, 1, 5, 10, 25, 50 cycles |
| Interruption | 0% for 250 cycles (5 s at 50 Hz) |
| Criteria | Performance Criterion B for dips; C for interruptions |

---

## Stage 6 — Safety Tests

Reference standards: IEC 62368-1, IEC 61851-23, UL 2202

### SAF-01: Hipot (Dielectric Strength)

| Insulation Barrier | Test Voltage | Duration | Pass Criteria |
|--------------------|-------------|----------|---------------|
| Input (AC) → Output (DC) | 3.0 kVAC | 60 s | No breakdown; leakage <10 mA |
| Input (AC) → Earth | 2.5 kVAC | 60 s | No breakdown; leakage <10 mA |
| Output (DC) → Earth | 2.5 kVAC | 60 s | No breakdown; leakage <10 mA |
| Primary → Secondary (within) | 1.5 kVAC | 60 s | No breakdown |

> [!note] Per [[09-Protection and Safety]] insulation coordination. Production test may use 120% voltage for 1 s as alternative.

### SAF-02: Insulation Resistance

| Barrier | Voltage | Pass Criteria |
|---------|---------|---------------|
| Input → Output | 500 VDC | >10 MΩ |
| Input → Earth | 500 VDC | >10 MΩ |
| Output → Earth | 500 VDC | >10 MΩ |
| Post-humidity | 500 VDC | >1 MΩ |

### SAF-03: Earth Leakage Current

| Condition | Limit |
|-----------|-------|
| Normal condition | <3.5 mA |
| Single fault condition | <7.0 mA |
| Measurement method | IEC 62368-1 Annex B |

### SAF-04: PE Continuity

| Parameter | Value |
|-----------|-------|
| Test current | 25 A (or 2× rated earth current, whichever greater) |
| Duration | 60 s |
| Pass criteria | <0.1 Ω between any accessible metal and PE terminal |

### SAF-05: Temperature Rise

| Component | Max Rise Above Ambient | Method |
|-----------|----------------------|--------|
| SiC MOSFET case | Per datasheet Tc_max − ambient | Thermocouple |
| Transformer winding | 100 K (Class F) | Resistance method |
| PCB traces (power) | 50 K | Thermocouple |
| Enclosure surface (touchable) | 40 K | Thermocouple |
| Terminal connections | 50 K | Thermocouple |
| Electrolytic capacitors | 40 K | Thermocouple |
| Wire insulation | Per rating − ambient | Thermocouple |

### SAF-06: Abnormal Conditions

| Condition | Expected Behavior |
|-----------|------------------|
| Fan failure (single) | Derate to 50%; shutdown if temp exceeds limit |
| Fan failure (all) | Shutdown within 30 s |
| Output short circuit | Trip within 10 us; no fire/explosion |
| Single semiconductor failure | No propagation; safe shutdown |
| Overload (150%) | Trip within 1 s |
| Mains overvoltage (530 V + 10%) | OVP trip or continued safe operation |

### SAF-07: Ground Fault Detection

| Parameter | Value |
|-----------|-------|
| Trip threshold | 30 mA (adjustable) |
| Trip time | <100 ms |
| Test method | Inject current via test resistor |
| Pass criteria | Trip occurs within threshold; latch and report |

---

## Test Matrix Summary

| ID | Test Name | Stage | Standard | Phase | Units |
|----|-----------|-------|----------|-------|-------|
| BLT-01 | Smoke Test | Board | — | 1 | All |
| BLT-02 | Rail Verification | Board | — | 1 | All |
| BLT-03 | MCU Functional | Board | — | 1 | All |
| BLT-04 | Gate Driver Verification | Board | — | 1 | All |
| SST-01 | PFC Characterization | Sub-System | — | 3 | 3 |
| SST-02 | LLC Characterization | Sub-System | — | 3 | 3 |
| SST-03 | Thermal Pre-Characterization | Sub-System | — | 3 | 3 |
| SYS-01 | 30 kW Steady State | System | — | 3 | 3 |
| SYS-02 | CC/CV Profile | System | IEC 61851 | 3 | 2 |
| SYS-03 | Input Voltage Transients | System | — | 3 | 2 |
| SYS-04 | 5-Module Stacking | System | — | 5 | 5 |
| SYS-05 | Protection Verification | System | — | 3, 5 | 3 |
| ENV-01 | Thermal Cycling | Environmental | IEC 60068-2-14 | 7 | 2 |
| ENV-02 | Vibration | Environmental | IEC 60068-2-64 | 7 | 2 |
| ENV-03 | Humidity | Environmental | IEC 60068-2-78 | 7 | 2 |
| ENV-04 | HALT | Environmental | — | 7 | 2 |
| ENV-05 | Burn-In | Environmental | — | 7 | 10 |
| EMC-01 | Conducted Emissions | EMC | CISPR 32 | 6, 7 | 2 |
| EMC-02 | Radiated Emissions | EMC | CISPR 32 | 6, 7 | 2 |
| EMC-03 | Harmonics | EMC | IEC 61000-3-2 | 6, 7 | 2 |
| EMC-04 | Surge | EMC | IEC 61000-4-5 | 6, 7 | 2 |
| EMC-05 | ESD | EMC | IEC 61000-4-2 | 6, 7 | 2 |
| EMC-06 | EFT/Burst | EMC | IEC 61000-4-4 | 6, 7 | 2 |
| EMC-07 | Conducted RF Immunity | EMC | IEC 61000-4-6 | 6, 7 | 2 |
| EMC-08 | Radiated RF Immunity | EMC | IEC 61000-4-3 | 6, 7 | 2 |
| EMC-09 | Voltage Dips | EMC | IEC 61000-4-11 | 6, 7 | 2 |
| SAF-01 | Hipot | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-02 | Insulation Resistance | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-03 | Earth Leakage | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-04 | PE Continuity | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-05 | Temperature Rise | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-06 | Abnormal Conditions | Safety | IEC 62368-1 | 6, 7 | 2 |
| SAF-07 | Ground Fault | Safety | IEC 61851-23 | 6, 7 | 2 |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
