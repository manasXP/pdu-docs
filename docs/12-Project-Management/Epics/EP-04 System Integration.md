---
tags: [PDU, project-management, epic, phase-3, integration, closed-loop, thermal]
created: 2026-02-22
---

# EP-04 — System Integration

> **Phase 3 | Duration: 8 weeks | Lead: PE**
> Gate exit: 30 kW continuous output achieved. Efficiency > 95% at rated load. Thermal steady-state characterized. CC/CV charging profiles validated. All protection functions tested. Rev A issues documented.

---

## Epic Summary

This epic closes the control loops and validates the complete power conversion chain at full power. PFC dq-frame current control locks to grid, LLC voltage/current loops regulate output, and the system sustains 30 kW continuously. Thermal characterization maps junction and heatsink temperatures. Protection functions are stress-tested. All findings feed into the Rev B design fix list.

**Entry criteria:** Open-loop PFC and LLC verified (EP-03 complete).
**Exit criteria:** 30 kW sustained for 1 hour. Efficiency > 95%. Thermal steady-state < limits. Rev A issue list prioritized.

---

## Stories

### PFC Closed-Loop

#### EP-04-001: Close PFC dq-Frame Current Loop
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | L (12 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-005, EP-03-010, EP-03-011, EP-03-012 |
| **Blocks** | EP-04-002, EP-04-003 |

**Description:** Enable closed-loop PFC current control: Clarke → Park (using PLL theta) → d/q PI controllers → inverse Park → SVM → HRTIM duty update. Tune d-axis and q-axis PI gains starting from calculated values (Kp ≈ 0.94, Ki ≈ 1776 rad/s for L=200 uH, BW=1.5 kHz). Add decoupling terms (omega*L cross-coupling).

**Test progression:**
1. 260 VAC / 50 Hz, resistive load, 5 kW → tune current PI
2. 400 VAC / 50 Hz, 15 kW → verify stability
3. 530 VAC / 50 Hz, 30 kW (PFC only, LLC off — bus capacitor load)

**Acceptance criteria:**
- [ ] I_d tracks setpoint within 2% steady-state error
- [ ] I_q < 2 A (PF > 0.99)
- [ ] THDi < 5% at rated load (measured with power analyzer)
- [ ] Bus voltage stable within ±10 V of target
- [ ] Transient response: 50% load step, Vbus deviation < 30 V, recovery < 50 ms

---

#### EP-04-002: Close Bus Voltage Outer Loop
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-001, EP-03-013 |
| **Blocks** | EP-04-006 |

**Description:** Enable bus voltage PI loop (20–50 Hz bandwidth). Output = I_d* reference for inner current loop. Tune Kp and Ki for stable bus voltage at 700–920 VDC. Verify anti-windup during soft-start. Verify neutral point balancing under load (|V_NP_err| < 5 V at balanced grid).

**Acceptance criteria:**
- [ ] Bus voltage regulates to setpoint within ±5 V steady-state
- [ ] Voltage loop bandwidth measured (step response): 20–50 Hz
- [ ] NP imbalance < 5 V at balanced 400 VAC, < 15 V at 5% grid unbalance
- [ ] Anti-windup prevents overshoot during soft-start ramp

---

#### EP-04-003: PFC Efficiency and THD Characterization
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-001 |
| **Blocks** | EP-04-006 |

**Description:** Systematic efficiency and power quality measurement of PFC stage at 10/25/50/75/100% load, 3 input voltages (260/400/530 VAC), and 2 frequencies (50/60 Hz). Record: efficiency, PF, THDi, Vbus ripple, switching waveforms.

**Acceptance criteria:**
- [ ] Efficiency > 98% at 50–100% load (SiC Vienna, per [[04-Thermal Budget]] prediction)
- [ ] PF > 0.99 at 25–100% load
- [ ] THDi < 5% at rated load, < 8% at 25% load
- [ ] Data captured in spreadsheet for design verification

---

### LLC Closed-Loop

#### EP-04-004: Close LLC CC/CV Voltage and Current Loops
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | L (12 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-007, EP-03-012 |
| **Blocks** | EP-04-005, EP-04-006 |

**Description:** Enable LLC closed-loop voltage/current control per [[06-Firmware Architecture]] §5.2. CV mode: V_out PI → frequency command. CC mode: I_out PI → frequency command. Mode switching logic: I_out > I_limit → CC; V_out > V_limit → CV. Tune PI gains starting from Kp=0.005 Hz/V, Ki=5 rad/s.

**Test progression:**
1. Fixed Vbus=800 V (bench supply), resistive load, 5 kW → tune voltage PI
2. 15 kW → verify CC/CV crossover
3. Full PFC+LLC chain, 30 kW → validate complete system

**Acceptance criteria:**
- [ ] CV mode: V_out within ±0.5% of setpoint (e.g., ±3.75 V at 750 V)
- [ ] CC mode: I_out within ±1% of setpoint
- [ ] CC → CV transition smooth (no voltage spike > 2%)
- [ ] Load step response: 25 → 75% load, V_out deviation < 20 V, recovery < 100 ms

---

#### EP-04-005: LLC Efficiency Characterization
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-004 |
| **Blocks** | EP-04-006 |

**Description:** Measure LLC stage efficiency at multiple operating points: V_out = 200/400/600/800/1000 VDC, load = 10/25/50/75/100%. Record switching frequency, resonant current waveforms, and ZVS margin.

**Acceptance criteria:**
- [ ] LLC efficiency > 97% at rated power (800 V, 37.5 A)
- [ ] ZVS confirmed at all operating points above resonance
- [ ] No ZCS risk at any tested condition
- [ ] Efficiency vs. load curve plotted for each V_out

---

### Full System Test

#### EP-04-006: Achieve 30 kW Continuous Operation
| Field | Value |
|-------|-------|
| **Assignee** | PE, FW |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-002, EP-04-003, EP-04-004, EP-04-005 |
| **Blocks** | EP-04-007, EP-04-008, EP-05-002 |

**Description:** Run complete system (PFC + LLC) at 30 kW continuous for 1 hour. Input: 400 VAC, 3-phase. Output: 750 VDC, 40 A (30 kW). Measure overall efficiency, thermal steady-state, acoustic noise, and power quality.

**Acceptance criteria:**
- [ ] 30 kW sustained for 60 minutes without fault or derate
- [ ] System efficiency > 96% (measured AC input to DC output)
- [ ] No component exceeds temperature limit (T_SiC < 100°C, T_mag < 120°C)
- [ ] Acoustic noise < 65 dB at 1 m
- [ ] Input current balanced across 3 phases (< 5% imbalance)
- [ ] Output ripple < 0.5% RMS of V_out

---

#### EP-04-007: Thermal Characterization — Full Temperature Map
| Field | Value |
|-------|-------|
| **Assignee** | TH, PE |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-006 |
| **Blocks** | EP-05-002 |

**Description:** Full thermal characterization at 30 kW steady-state: thermocouple measurements on all power devices, magnetics, heatsink surface, inlet/outlet air. Thermal camera imaging. Map actual thermal resistance chain against [[04-Thermal Budget]] predictions.

**Measurement points (per unit):**
| Location | Sensor | Expected |
|----------|--------|----------|
| SiC MOSFET case (PFC, hottest) | TC type-K | < 85°C |
| SiC MOSFET case (LLC primary) | TC type-K | < 90°C |
| SiC diode case (LLC secondary, hottest) | TC type-K | < 100°C |
| LLC transformer core | TC type-K | < 110°C |
| Heatsink surface (center) | TC type-K | < 75°C |
| Inlet air | TC type-K | Ambient |
| Outlet air | TC type-K | Ambient + 15–25°C |

**Acceptance criteria:**
- [ ] All components below derate threshold at 25°C ambient
- [ ] Thermal resistance values match budget within ±20%
- [ ] Derating curve validated at 45°C and 55°C ambient (thermal chamber)
- [ ] Thermal camera images captured for documentation
- [ ] Hot spots identified for Rev B layout improvement (if any)

---

#### EP-04-008: Protection Function Stress Test
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE, QA |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-009, EP-04-006 |
| **Blocks** | EP-05-002 |

**Description:** Systematically test all 14 protection functions from [[09-Protection and Safety]] under controlled conditions. Each test injects a fault condition and verifies the response latency, output behavior, and fault logging.

| Test | Fault Injected | Expected Response | Pass Criteria |
|------|---------------|-------------------|--------------|
| OCP PFC (HW) | Increase load suddenly to 130% | HRTIM idle < 200 ns | Scope capture |
| OVP bus (HW) | Disconnect load suddenly | HRTIM idle < 1 us | Scope capture |
| OVP output (HW) | Raise V_ref above limit | HRTIM idle < 1 us | Scope capture |
| OTP SiC | Block airflow (thermal) | Derate at 100°C, shutdown at 115°C | Temp log |
| Phase loss | Disconnect one AC phase | FAULT within 20 ms | State log |
| CAN timeout | Disconnect CAN cable | Derate at 50 ms, shutdown at 200 ms | State log |
| Short circuit | Apply dead short on output | OCP trip < 500 ns | Scope capture |

**Acceptance criteria:**
- [ ] All 14 protection functions tested and documented
- [ ] No destructive failure during any test
- [ ] Fault log entries match expected fault IDs and severities
- [ ] Auto-retry logic tested for major faults (3 retries, then latch)
- [ ] Test report suitable for pre-compliance documentation

---

### CC/CV Profile and EV Charging Simulation

#### EP-04-009: Validate CC/CV Charging Profile
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-004, EP-03-014 |
| **Blocks** | EP-06-004 |

**Description:** Simulate an EV charging session: ramp from 0 → 100 A CC, transition to CV at 800 V, taper to 5 A cutoff. Use programmable DC load in CC/CV mode to emulate vehicle battery. Verify smooth CC→CV transition, setpoint tracking, and CAN status reporting.

**Acceptance criteria:**
- [ ] CC mode holds current within ±1 A at all points
- [ ] CV mode holds voltage within ±2 V
- [ ] CC→CV crossover: no overshoot > 5 V, no undershoot > 5 A
- [ ] Full profile completes without fault
- [ ] CAN status frames report correct V_out, I_out, state throughout

---

#### EP-04-010: Characterize Startup at Voltage Extremes
| Field | Value |
|-------|-------|
| **Assignee** | PE, FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-006 |
| **Blocks** | EP-05-002 |

**Description:** Test full power-on sequence at input voltage extremes (260 VAC and 530 VAC) and frequency extremes (45 Hz and 65 Hz). Verify PLL lock time, soft-start timing, and bus voltage regulation.

**Acceptance criteria:**
- [ ] PLL locks at all 4 corner cases within 2 s
- [ ] Total startup <=6 s at worst case (260 VAC / 45 Hz)
- [ ] No inrush current exceeds NTC rating at 530 VAC
- [ ] Bus voltage stable at all operating points

---

### Parallel Activities

#### EP-04-011: CFD Simulation of Enclosure Airflow
| Field | Value |
|-------|-------|
| **Assignee** | TH |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-005 |
| **Blocks** | EP-05-003 |

**Description:** CFD simulation of complete enclosure: fan placement, heatsink fin geometry, board obstruction, inlet/outlet apertures. Validate 2.5 m/s target airflow across heatsink. Identify dead zones and potential improvements for Rev B.

**Acceptance criteria:**
- [ ] CFD model matches enclosure geometry from [[10-Mechanical Integration]]
- [ ] Simulated airflow velocity across heatsink fins: 2.0–3.0 m/s at 55 CFM
- [ ] System pressure drop < 7.1 mm H2O (fan operating point)
- [ ] No dead zones causing hotspot > 10°C above average
- [ ] Recommendations for Rev B (fin spacing, inlet size) documented

---

#### EP-04-012: Fan Speed Control Algorithm Implementation
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-003 |
| **Blocks** | EP-04-007 |

**Description:** Implement PWM fan speed control (25 kHz PWM, 20–100% duty). PID control based on hottest NTC reading. Minimum speed = 20% (audible noise reduction at light load). Boost to 100% if any temperature exceeds derate threshold. Fan failure detection: tachometer feedback timeout (5 s).

**Acceptance criteria:**
- [ ] Fan speed ramps linearly with heatsink temperature
- [ ] Min speed 20% at T < 50°C ambient
- [ ] Max speed 100% at T > 70°C or any component in derate zone
- [ ] Tachometer feedback reads correct RPM (within ±10%)
- [ ] Fan failure fault triggers within 5 s of fan stop

---

#### EP-04-013: Efficiency Optimization Investigation
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-003, EP-04-005 |
| **Blocks** | EP-05-002 |

**Description:** Analyze measured losses vs. [[04-Thermal Budget]] predictions. Identify top 3 loss contributors. Investigate optimization opportunities: dead-time tuning (adaptive dead-time), PFC switching frequency selection (48 vs 65 kHz), LLC magnetizing inductance adjustment, gate drive voltage optimization.

**Acceptance criteria:**
- [ ] Loss breakdown table: predicted vs. measured for top 10 components
- [ ] Top 3 optimization opportunities quantified (expected efficiency gain)
- [ ] Recommendations documented for Rev B implementation

---

#### EP-04-014: Rev A Issue List Consolidation
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (1 day) |
| **Status** | Backlog |
| **Depends on** | EP-04-006, EP-04-007, EP-04-008 |
| **Blocks** | EP-05-001 |

**Description:** Consolidate all Rev A issues from board bring-up, system integration, thermal characterization, and protection testing. Prioritize by severity. Assign to Rev B fix or defer.

**Acceptance criteria:**
- [ ] All issues logged with severity, root cause, and proposed fix
- [ ] Critical and major issues assigned to EP-05 stories
- [ ] Minor issues triaged (fix in Rev B or defer to Rev C)

---

#### EP-04-015: Update Design Documents with Measured Data
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-003, EP-04-005, EP-04-007 |
| **Blocks** | — |

**Description:** Update [[04-Thermal Budget]] with measured thermal data. Update [[03-LLC Gain Curve Verification]] with actual resonant frequency measurements. Update [[02-Magnetics Design]] with measured transformer parameters. Update [[06-Firmware Architecture]] with tuned PI gains.

**Acceptance criteria:**
- [ ] Design documents updated with "Measured" columns alongside "Calculated" columns
- [ ] Any discrepancies > 20% flagged with root cause analysis

---

## References

- [[12-Project-Management/__init|Project Management]] — Phase 3 entry/exit criteria
- [[04-Thermal Budget]] — Predicted thermal performance
- [[09-Protection and Safety]] — Protection function specifications

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 15 stories |
