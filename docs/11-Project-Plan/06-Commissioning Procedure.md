---
tags: [pdu, project-plan, commissioning, deployment]
created: 2026-02-22
---

# 06 — Commissioning Procedure

This document defines the 7-stage field commissioning procedure for deploying a 30 kW PDU module (or 5-module 150 kW stack) at a charging site.

> [!note] This procedure references the power-on sequence from [[08-Power-On Sequence and Inrush Management]] and thermal limits from [[04-Thermal Budget]].

## Prerequisites

Before starting commissioning:

- [ ] Unit(s) received and unpacked; verify shipping damage inspection
- [ ] Site 3-phase AC supply verified: 400/480 VAC, 63 A breaker, PE connected
- [ ] Environmental conditions within spec: -30°C to +55°C, <95% RH non-condensing
- [ ] Required tools available: multimeter, insulation tester, torque wrench, laptop with CAN interface
- [ ] Commissioning engineer trained on this procedure
- [ ] Safety PPE: insulated gloves (1 kV), safety glasses, arc-flash rated clothing

> [!warning] **Hazardous voltages present.** The DC bus operates at up to 900 VDC. The output can reach 1000 VDC. Only qualified personnel may perform this procedure. Follow all site-specific lockout/tagout procedures.

---

## Stage 1 — Receiving Inspection

### Purpose
Verify physical condition and completeness of the delivered unit.

### Procedure

| Step | Action | Accept Criteria | Record |
|------|--------|----------------|--------|
| 1.1 | Inspect shipping container for damage | No dents, punctures, water intrusion | Photo |
| 1.2 | Unpack unit; verify serial number against packing list | Serial matches; all items present | Serial # |
| 1.3 | Visual inspection of enclosure | No dents, scratches exposing bare metal, loose fasteners | Photo |
| 1.4 | Check fan rotation by hand | Spins freely; no rubbing | Pass/Fail |
| 1.5 | Verify connector integrity (AC input, DC output, CAN, aux) | No bent pins, cracked housings | Pass/Fail |
| 1.6 | Check accessory kit | Mounting hardware, manual, cert docs, CAN termination | Checklist |
| 1.7 | Record firmware version (label or CAN query) | Matches expected version | Version # |

---

## Stage 2 — Pre-Power Checks

### Purpose
Verify insulation integrity and wiring correctness before applying power.

### Procedure

| Step | Action | Accept Criteria | Instrument |
|------|--------|----------------|------------|
| 2.1 | Measure insulation resistance: L1–PE | >10 MΩ at 500 VDC | Insulation tester |
| 2.2 | Measure insulation resistance: L2–PE | >10 MΩ at 500 VDC | Insulation tester |
| 2.3 | Measure insulation resistance: L3–PE | >10 MΩ at 500 VDC | Insulation tester |
| 2.4 | Measure insulation resistance: DC+–PE | >10 MΩ at 500 VDC | Insulation tester |
| 2.5 | Measure insulation resistance: DC−–PE | >10 MΩ at 500 VDC | Insulation tester |
| 2.6 | Measure insulation resistance: AC–DC | >10 MΩ at 500 VDC | Insulation tester |
| 2.7 | PE continuity: enclosure to PE terminal | <0.1 Ω | Multimeter (low-Ω) |
| 2.8 | PE continuity: heatsink to PE terminal | <0.1 Ω | Multimeter (low-Ω) |
| 2.9 | Verify AC input wiring: phase sequence | L1-L2-L3 correct (120° rotation) | Phase rotation meter |
| 2.10 | Verify DC output wiring: polarity | DC+ and DC− correct | Multimeter |
| 2.11 | Verify CAN bus wiring: Hi/Lo, shield, termination | Correct per wiring diagram | Visual + multimeter |
| 2.12 | Check all mechanical connections: torque | Per torque spec on data plate | Torque wrench |

> [!warning] If any insulation resistance measurement is below 10 MΩ, **do not apply power**. Investigate and resolve before proceeding.

---

## Stage 3 — First Power-On Sequence

### Purpose
Apply power in a controlled sequence and verify basic operation per [[08-Power-On Sequence and Inrush Management]].

### Procedure

| Step | Action | Expected Result | Verify |
|------|--------|----------------|--------|
| 3.1 | Ensure DC output is disconnected (no load, no vehicle) | Open circuit at output | Visual |
| 3.2 | Close AC input breaker | Standby LED illuminates | LED |
| 3.3 | Monitor inrush current (if clamp meter available) | <25 A peak; NTC pre-charge active | Clamp meter |
| 3.4 | Wait for auxiliary PSU to stabilize (5–10 s) | Fan starts; status LED changes to ready | LED, fan |
| 3.5 | Query unit via CAN: status register | Status = READY, no faults | CAN tool |
| 3.6 | Query unit via CAN: firmware version | Matches expected | CAN tool |
| 3.7 | Query unit via CAN: temperature readings | Ambient ±5°C; no sensor faults | CAN tool |
| 3.8 | Query unit via CAN: DC bus voltage | ~0 V (PFC not yet enabled) or pre-charge voltage | CAN tool |
| 3.9 | Enable PFC via CAN command | DC bus ramps to ~800 VDC within 6 s | CAN tool |
| 3.10 | Monitor DC bus voltage for 60 s | Stable within ±5 V; no oscillation | CAN tool |
| 3.11 | Verify PFC input current (CAN or clamp) | Small magnetizing current only (no load) | CAN / clamp |
| 3.12 | Disable PFC; verify DC bus discharge | Bus discharges through bleed resistors; <50 V in 60 s | CAN tool |

---

## Stage 4 — Functional Verification

### Purpose
Verify output regulation, CC/CV modes, and protection functions at reduced load.

### Equipment Needed
- Resistive load bank or electronic load (≥10 kW)
- DC voltmeter (calibrated)
- DC ammeter or current clamp

### Procedure

#### 4A — No-Load Verification

| Step | Action | Expected Result |
|------|--------|----------------|
| 4A.1 | Enable PFC + LLC; set output to 400 V, 0 A (CV, no load) | Output voltage 400 V ±0.5% |
| 4A.2 | Step output voltage: 200 V, 400 V, 600 V, 800 V, 1000 V | Each step within ±0.5% |
| 4A.3 | Measure output ripple at 400 V no-load | <2 Vpp |
| 4A.4 | Verify no audible abnormalities | No buzzing, clicking, or excessive fan noise |

#### 4B — Stepped Load Verification

| Step | Load | Output | Verify |
|------|------|--------|--------|
| 4B.1 | 1 kW (2.5 A @ 400 V) | CC mode, 2.5 A set | Current ±1% |
| 4B.2 | 5 kW (12.5 A @ 400 V) | CC mode, 12.5 A set | Current ±1% |
| 4B.3 | 10 kW (25 A @ 400 V) | CC mode, 25 A set | Current ±1% |
| 4B.4 | Measure efficiency at 10 kW | >96% (400 V in / 400 V out) | Power analyzer or input/output meters |
| 4B.5 | Observe thermal camera or CAN temps | No abnormal hot spots | Thermal camera |

#### 4C — CC/CV Mode Verification

| Step | Action | Expected Result |
|------|--------|----------------|
| 4C.1 | Set CC = 25 A, CV = 400 V; apply 10 Ω load | Operates in CC at 25 A, ~250 V |
| 4C.2 | Reduce load to 20 Ω | Transitions to CV at 400 V, ~20 A |
| 4C.3 | Verify smooth CC→CV transition | No oscillation or overshoot >1% |

#### 4D — Protection Spot-Check

| Step | Action | Expected Result |
|------|--------|----------------|
| 4D.1 | Simulate OTP: set threshold to current temp + 5°C via CAN | OTP trips; output disabled |
| 4D.2 | Clear OTP; verify auto-recovery | Unit restarts after cool-down |
| 4D.3 | Set OVP to test value (e.g., 410 V); increase voltage setpoint | OVP trips at threshold |
| 4D.4 | Reset to normal thresholds | All protections back to default |

---

## Stage 5 — Full Load Commissioning

### Purpose
Operate at rated 30 kW for 30 minutes and verify thermal equilibrium.

### Equipment Needed
- Full-rated load (30 kW electronic load or resistor bank)
- Power analyzer (3-phase input + DC output)
- Temperature logging (CAN + optional thermal camera)

### Procedure

| Step | Action | Accept Criteria |
|------|--------|----------------|
| 5.1 | Set output: 75 A @ 400 V (30 kW) | Stable output within 10 s |
| 5.2 | Record input power (3-phase) | <31.25 kW (>96% efficiency) |
| 5.3 | Record power factor | ≥0.99 |
| 5.4 | Record THDi | ≤5% |
| 5.5 | Record output ripple | <0.5% RMS (2 V at 400 V) |
| 5.6 | Monitor temperatures every 5 min for 30 min | All temps stabilizing; no runaway |
| 5.7 | After 30 min: record final temperatures | All within [[04-Thermal Budget]] limits |
| 5.8 | Record acoustic noise (1 m distance) | ≤65 dB(A) |
| 5.9 | Reduce to 0 load; observe shutdown | Clean shutdown; DC bus discharges |
| 5.10 | Check for any new fault codes | No fault codes logged during test |

### Thermal Limits (Reference)

| Location | Max Temperature |
|----------|----------------|
| Heatsink (SiC MOSFET region) | Per [[04-Thermal Budget]] + ambient |
| Transformer | <130°C |
| Electrolytic capacitors | <85°C |
| Enclosure surface (touchable) | <65°C (40 K above 25°C ambient) |
| Fan exhaust | <70°C above ambient |

---

## Stage 6 — CAN Stacking Verification

### Purpose
Verify multi-module operation for installations with 2 or 5 PDU modules.

> [!note] Skip this stage for single-module installations.

### 6A — 2-Module Test

| Step | Action | Accept Criteria |
|------|--------|----------------|
| 6A.1 | Connect 2 modules on CAN bus with termination | CAN communication established |
| 6A.2 | Power on both; verify master election | One module becomes master |
| 6A.3 | Set 60 kW total (150 A @ 400 V or 60 A @ 1000 V) | Both modules share load |
| 6A.4 | Verify current imbalance | <5% difference between modules |
| 6A.5 | Run for 10 min | Stable operation; no faults |

### 6B — 5-Module Test (150 kW)

| Step | Action | Accept Criteria |
|------|--------|----------------|
| 6B.1 | Connect 5 modules on CAN bus with termination | All 5 modules on bus |
| 6B.2 | Power on all; verify master election and ID assignment | IDs 1–5 assigned; master elected |
| 6B.3 | Ramp to 150 kW total | All 5 modules sharing load evenly |
| 6B.4 | Verify current imbalance across all modules | <5% max deviation from average |
| 6B.5 | Run for 15 min at 150 kW | Stable operation |
| 6B.6 | Verify efficiency (system-level) | >95.5% (accounting for bus bar losses) |

### 6C — Hot-Plug Test

| Step | Action | Accept Criteria |
|------|--------|----------------|
| 6C.1 | Running at 120 kW (4 modules); add 5th module | 5th module joins seamlessly; ramp to 150 kW |
| 6C.2 | Running at 150 kW; remove 1 module | Remaining 4 absorb load (120 kW); no trip |
| 6C.3 | Running at 150 kW; kill master module | New master elected in <100 ms; no output dropout |

---

## Stage 7 — Handoff

### Purpose
Complete commissioning documentation and hand off to site operator.

### Procedure

| Step | Action | Deliverable |
|------|--------|------------|
| 7.1 | Complete commissioning report (fill all data from Stages 1–6) | Signed commissioning report |
| 7.2 | Record all serial numbers and firmware versions | Asset register entry |
| 7.3 | Record site-specific configuration (CAN ID, voltage limits, current limits) | Configuration record |
| 7.4 | Provide operator training: power on/off, fault codes, basic troubleshooting | Training sign-off |
| 7.5 | Provide documentation package: manual, certs, wiring diagram, contact info | Handover package |
| 7.6 | Verify OCPP connection to backend (if applicable) | Backend receives heartbeat |
| 7.7 | Customer sign-off | Signed acceptance form |

### Commissioning Report Template

```
COMMISSIONING REPORT — 30 kW PDU MODULE
========================================
Date: _______________
Site: _______________
Commissioning Engineer: _______________

UNIT INFORMATION
  Serial Number: _______________
  Firmware Version: _______________
  Hardware Revision: _______________
  CAN ID: _______________

STAGE 1 — RECEIVING INSPECTION
  Condition: [ ] Pass  [ ] Fail
  Notes: _______________

STAGE 2 — PRE-POWER CHECKS
  Insulation L1-PE: _______ MΩ
  Insulation L2-PE: _______ MΩ
  Insulation L3-PE: _______ MΩ
  Insulation DC+-PE: _______ MΩ
  Insulation DC--PE: _______ MΩ
  Insulation AC-DC: _______ MΩ
  PE Continuity (enclosure): _______ Ω
  PE Continuity (heatsink): _______ Ω
  Phase Sequence: [ ] Correct  [ ] Incorrect

STAGE 3 — FIRST POWER-ON
  Inrush Current: _______ A peak
  DC Bus Voltage: _______ V (after PFC enable)
  Status: [ ] Pass  [ ] Fail

STAGE 4 — FUNCTIONAL VERIFICATION
  No-load voltage accuracy: _______ V at 400 V set (error: _____%)
  10 kW efficiency: _______%
  CC/CV transition: [ ] Smooth  [ ] Issue
  Protection spot-check: [ ] Pass  [ ] Fail

STAGE 5 — FULL LOAD (30 kW, 30 min)
  Input Power: _______ kW
  Output Power: _______ kW
  Efficiency: _______%
  Power Factor: _______
  THDi: _______%
  Output Ripple: _______ mV RMS
  Max Heatsink Temp: _______°C
  Max Transformer Temp: _______°C
  Acoustic Noise: _______ dB(A)
  Result: [ ] Pass  [ ] Fail

STAGE 6 — STACKING (if applicable)
  Modules tested: _______
  Max current imbalance: _______%
  Hot-plug: [ ] Pass  [ ] N/A
  Result: [ ] Pass  [ ] Fail  [ ] N/A

OVERALL RESULT: [ ] PASS  [ ] FAIL  [ ] CONDITIONAL

Notes / Punch List:
_______________________________________________
_______________________________________________

Commissioning Engineer: _______________ Date: _______________
Customer Representative: _______________ Date: _______________
```

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
