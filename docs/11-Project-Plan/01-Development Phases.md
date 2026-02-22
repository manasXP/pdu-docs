---
tags: [pdu, project-plan, schedule, phases]
created: 2026-02-22
---

# 01 — Development Phases

This document defines the 9 development phases for the 30 kW PDU, covering hardware, firmware, and certification tracks. Each phase includes scope, deliverables, entry/exit criteria, and key activities.

> [!note] See [[11-Project-Plan/__init|11-Project Plan]] for the Gantt timeline and milestone schedule.

## Phase Overview

```
Ph 0: Design Review & Procurement ─────── 6 wk
Ph 1: Rev A Prototype Build ───────────── 8 wk
Ph 2: Firmware Bring-Up ───────────────── 7 wk  (overlaps Ph 1)
Ph 3: System Integration ──────────────── 8 wk
Ph 4: Rev B Prototype ─────────────────── 8 wk
Ph 5: Firmware Maturation ─────────────── 10 wk (overlaps Ph 4)
Ph 6: Certification Prep ──────────────── 8 wk  (overlaps Ph 5)
Ph 7: Pre-Production Validation ────────── 8 wk
Ph 8: Production Release ──────────────── 6 wk
```

### Parallel Tracks

| Track | Phases | Focus |
|-------|--------|-------|
| **Hardware** | 0, 1, 3, 4, 7, 8 | Schematics, PCB, mechanical, prototypes |
| **Firmware** | 2, 3, 5 | BSP, control loops, protocols, protection |
| **Certification** | 6, 7, 8 | EMC, safety, documentation, lab testing |

---

## Phase 0 — Design Review & Procurement (6 weeks)

### Objective
Finalize all design documents, complete peer reviews, and place orders for long-lead components.

### Entry Criteria
- All design documents at draft status (topology, magnetics, thermal, EMI, firmware, PCB layout, BOM, mechanical, protection)
- Project plan approved

### Key Activities

#### Week 1–2: Design Reviews
- Schematic review (power stage, control, auxiliary)
- [[07-PCB-Layout/__init|PCB layout]] review (power loop, creepage/clearance, thermal)
- [[02-Magnetics Design]] review (LLC transformer, PFC inductor)
- [[05-EMI Filter Design]] review (filter component selection, placement)

#### Week 2–3: Design Fixes
- Address all review findings (categorized as critical/major/minor)
- Update schematics, layout, BOM
- Re-verify [[03-LLC Gain Curve Verification|LLC gain curves]] if tank values changed

#### Week 3–4: Procurement
- Identify long-lead items (SiC MOSFETs, gate drivers, custom magnetics, connectors)
- Place orders for Rev A quantities (5 sets + spares)
- Confirm lead times; escalate items >6 weeks
- Order PCB fabrication (bare boards)

#### Week 4–6: Manufacturing Prep
- Finalize assembly drawings and pick-and-place files
- Prepare stencil files
- [[10-Mechanical Integration|Mechanical]] fabrication release (enclosure, heatsinks, bus bars)
- Prepare test fixtures and jigs

### Deliverables
- [ ] Signed-off schematics (all 4 boards)
- [ ] PCB fabrication package released
- [ ] Purchase orders for all components
- [ ] Mechanical fabrication released
- [ ] Updated BOM with confirmed suppliers and lead times

### Exit Criteria (Gate 0)
- All design reviews closed; no open critical findings
- All long-lead components on order with confirmed delivery dates
- PCB and mechanical fabrication in progress
- Test fixtures designed

---

## Phase 1 — Rev A Prototype Build (8 weeks)

### Objective
Fabricate, assemble, and inspect the first prototype hardware set (5 units).

### Entry Criteria
- Gate 0 passed
- Bare PCBs and components received
- Mechanical parts received

### Key Activities

#### Week 1–2: PCB Assembly
- Solder paste stencil printing
- Component placement (manual or PCBA service for 5 units)
- Reflow soldering (leaded or lead-free per BOM)
- Hand-solder through-hole components (connectors, large caps, bus bar lugs)

#### Week 2–3: Board Inspection
- Visual inspection under magnification
- AOI (Automated Optical Inspection) if using PCBA service
- X-ray inspection for QFN/BGA packages (gate drivers, MCU)
- Record and disposition any defects

#### Week 3–5: Board-Level Smoke Test
- Apply auxiliary power only; verify all rails per [[08-Power-On Sequence and Inrush Management]]
- Check 3.3 V, 5 V, 12 V, 15 V rails
- Verify MCU boot (JTAG/SWD connection)
- Gate driver supply verification
- Current consumption check (quiescent)

#### Week 5–6: Mechanical Assembly
- Heatsink preparation (thermal interface material application)
- Board mounting to heatsink assemblies
- Bus bar installation
- Fan mounting and wiring
- Enclosure assembly per [[10-Mechanical Integration]]

#### Week 6–8: Integration Assembly
- 4-board interconnection (power buses, signal harnesses)
- Input/output connector installation
- Cooling duct and airflow path verification
- Label and serialize units

### Deliverables
- [ ] 5 assembled and inspected PCB sets (4 boards each)
- [ ] 5 mechanically complete prototype units
- [ ] Inspection reports (visual, AOI, X-ray)
- [ ] Board-level smoke test results
- [ ] Assembly photos and build log

### Exit Criteria (Gate 1)
- All 5 units assembled; no critical assembly defects
- Auxiliary power rails verified on all units
- MCU boots and connects via debugger
- Mechanical assembly complete and passes dimensional check

---

## Phase 2 — Firmware Bring-Up (7 weeks)

### Objective
Develop and validate the board support package (BSP) and achieve open-loop PWM on the bench. Overlaps with Phase 1 using development boards initially, then transitions to Rev A hardware.

### Entry Criteria
- [[06-Firmware Architecture]] document approved
- STM32G474RE Nucleo board available (for early development)
- Rev A board available by Week 3 (from Phase 1)

### Key Activities

#### Week 1–2: BSP Development (on Nucleo)
- Clock tree configuration (170 MHz, PLL)
- GPIO initialization for all signals
- UART/debug console bring-up
- Watchdog timer configuration
- Flash/SRAM memory map

#### Week 2–3: HRTIM Configuration
- Timer A–F allocation per [[06-Firmware Architecture]] resource map
- PWM output configuration (complementary, dead-time)
- Dead-time calibration (target: 80–120 ns for SiC)
- ADC trigger synchronization
- Fault input configuration (hardware OCP trip)

#### Week 3–4: ADC Bring-Up
- ADC1/ADC2 channel configuration
- DMA transfer setup
- Calibration and offset correction
- Sampling time optimization for current/voltage sensing
- Verify all analog channels: phase currents (×3), DC bus voltage, output current, output voltage, NTC temperatures

#### Week 4–5: Open-Loop PWM (on Rev A board)
- Vienna PFC open-loop switching at 65 kHz
  - Verify gate signals on all 6 SiC MOSFETs
  - Dead-time verification with oscilloscope
  - Gate driver dV/dt stress test
- LLC open-loop switching at ~100–300 kHz
  - Verify resonant waveforms
  - Confirm ZVS indication via drain waveforms
  - Sweep frequency range

#### Week 5–6: Communication Peripherals
- CAN-FD initialization and loopback test
- SPI (for isolated ADC if applicable)
- I2C (for temperature sensors, EEPROM)
- UART (debug console, OCPP bridge)

#### Week 6–7: Basic Protection Implementation
- Hardware OCP via HRTIM fault inputs (< 1 us response)
- Software OVP/OCP/OTP with configurable thresholds
- Watchdog and fault state machine
- Soft-start sequence (basic, per [[08-Power-On Sequence and Inrush Management]])

### Deliverables
- [ ] BSP validated on Nucleo and Rev A hardware
- [ ] HRTIM resource map verified (PWM outputs, dead-times, triggers)
- [ ] All ADC channels calibrated and reading correctly
- [ ] Open-loop PFC switching verified (gate waveforms captured)
- [ ] Open-loop LLC switching verified (resonant waveforms captured)
- [ ] CAN/SPI/I2C/UART peripherals functional
- [ ] Basic protection functional (OCP trip verified)

### Exit Criteria (Gate 2)
- All peripherals functional on Rev A board
- Open-loop PWM verified on both PFC and LLC stages
- No silicon or layout errors preventing closed-loop development
- Protection trips verified at bench level

---

## Phase 3 — System Integration (8 weeks)

### Objective
Close control loops and achieve rated 30 kW operation with full thermal and efficiency characterization.

### Entry Criteria
- Gate 1 (hardware) and Gate 2 (firmware) passed
- Programmable AC source available (3-phase, 30+ kW)
- Electronic load available (1000 V, 100 A capable)
- Power analyzer connected

### Key Activities

#### Week 1–2: PFC Closed-Loop
- Implement dq-frame current control per [[06-Firmware Architecture]]
- DC bus voltage loop closure
- PFC bring-up sequence:
  1. Single-phase operation first (for debug)
  2. Three-phase balanced operation
  3. Voltage loop closure (800 VDC bus target)
- Measure: PF, THDi, efficiency at 25/50/75/100% load
- Target: PF ≥ 0.99, THDi ≤ 5% at full load

#### Week 2–4: LLC Closed-Loop
- Implement PFM (Pulse Frequency Modulation) control
- Output voltage regulation (CC/CV modes)
- LLC bring-up sequence:
  1. No-load start-up with voltage ramp
  2. Light load (1 kW) — verify ZVS
  3. Stepped load to 30 kW
- Verify gain curve matches [[03-LLC Gain Curve Verification]]
- Measure: efficiency, output ripple, transient response

#### Week 4–5: Full Power Operation
- Combined PFC + LLC at 30 kW continuous
- Input voltage sweep: 260 VAC → 530 VAC
- Output voltage sweep: 150 VDC → 1000 VDC
- Constant-power region verification (300–1000 V)
- Efficiency mapping (>96% target; >98% with SiC target)

#### Week 5–7: Thermal Characterization
- Thermocouple placement per [[04-Thermal Budget]]
- 30 kW continuous at 25°C ambient — record steady state temperatures
- 30 kW continuous at 45°C ambient (chamber) — verify derating curve
- Identify hot spots; compare to thermal model predictions
- Fan speed vs. temperature profile tuning

#### Week 7–8: Transient Testing
- Load step response (0→100%, 100%→0%)
- Input voltage step (brownout/overvoltage)
- CC→CV transition characterization
- Soft-start verification under load
- Output short circuit and recovery

### Deliverables
- [ ] Closed-loop PFC: PF, THDi, efficiency data across load range
- [ ] Closed-loop LLC: efficiency, ripple, transient data
- [ ] Full-power 30 kW steady-state test report
- [ ] Thermal characterization report with thermocouple data
- [ ] Efficiency map (input voltage × output voltage × load)
- [ ] Issue list for Rev B (categorized: critical/major/minor)

### Exit Criteria (Gate 3)
- 30 kW continuous operation demonstrated (≥1 hour)
- Efficiency >95% (target >96%) at rated conditions
- All junction temperatures within limits at 45°C ambient
- CC/CV modes functional with smooth transitions
- Rev B issue list finalized and prioritized

---

## Phase 4 — Rev B Prototype (8 weeks)

### Objective
Incorporate all Rev A fixes, re-spin PCBs, and build 10 units for certification and extended testing.

### Entry Criteria
- Gate 3 passed
- Rev B issue list approved
- Updated BOM reviewed

### Key Activities

#### Week 1–2: Design Updates
- Schematic changes per Rev A issue list
- PCB layout updates:
  - Power loop optimization (if needed)
  - Thermal relief improvements
  - EMI fixes (guard traces, stitching vias, filter component changes)
  - Creepage/clearance corrections (if any)
- Updated [[07-BOM and Cost Analysis|BOM]] with component changes
- Updated [[10-Mechanical Integration|mechanical]] design (if enclosure changes needed)

#### Week 2–3: Review & Release
- Focused design review on changed areas only
- DRC/ERC clean
- Fabrication release (PCB + mechanical)
- Component procurement for 10 units + spares

#### Week 3–6: Fabrication & Assembly
- PCB fabrication (expedite if schedule-critical)
- PCBA service for 10-unit build (SMT + through-hole)
- Mechanical fabrication and surface treatment
- Assembly and inspection (same process as Phase 1)

#### Week 6–7: Board-Level Verification
- Smoke test all 10 units
- Spot-check functional test on 3 units
- Verify all Rev A issues are resolved
- Regression: re-run Phase 2 key tests on Rev B

#### Week 7–8: System Verification
- Full-power test on 3 units (regression)
- Unit-to-unit variation assessment
- Select golden units for EMC and safety testing
- Reserve units: 2 for EMC, 2 for safety, 2 for HALT, 4 for integration/stacking

### Deliverables
- [ ] Updated schematics and layout (Rev B)
- [ ] 10 assembled and inspected Rev B units
- [ ] Board-level verification results
- [ ] Full-power regression test results (3 units)
- [ ] Unit allocation plan for Phase 5–7

### Exit Criteria (Gate 4)
- All 10 units assembled; no critical defects
- All Rev A issues verified resolved
- Full-power regression pass on ≥3 units
- Units allocated and labeled for downstream phases

---

## Phase 5 — Firmware Maturation (10 weeks)

### Objective
Complete all firmware features: CAN bus stacking, full protection suite, OCPP 1.6, and ISO 15118 interface.

### Entry Criteria
- Gate 3 (minimum) or Gate 4 passed
- Rev B units available for CAN stacking tests (≥5 units)

### Key Activities

#### Week 1–3: CAN Bus Stacking Protocol
- CAN-FD message set implementation per [[06-Firmware Architecture]]
- Master/slave arbitration and ID assignment
- Current sharing algorithm (proportional, droop-based)
- 2-module stacking test → 5-module stacking test
- Target: current imbalance < 5%
- Hot-plug / hot-unplug handling
- Fault propagation between modules (cascade shutdown)

#### Week 3–5: Protection Suite Completion
- Full protection matrix per [[09-Protection and Safety]]:
  - OVP (input and output)
  - OCP (input, DC bus, output) — hardware + software
  - OTP (heatsink, ambient, magnetics, SiC junction estimate)
  - Short-circuit protection (< 10 us trip)
  - Ground fault detection
  - Surge event response (per [[05-EMI Filter Design]])
- Protection coordination: priority, masking, recovery
- Fault logging (non-volatile, with timestamp)
- Configurable thresholds via CAN

#### Week 5–7: OCPP 1.6 Interface
- OCPP 1.6 JSON/WebSocket client implementation
- Core profile messages: BootNotification, Heartbeat, StatusNotification
- Smart charging profile: SetChargingProfile, GetCompositeSchedule
- Firmware update profile: UpdateFirmware, GetDiagnostics
- Integration with charge controller (via UART or CAN bridge)
- Test against OCPP 1.6 compliance test suite

#### Week 7–9: ISO 15118 Interface
- ISO 15118-2 (PLC-based) communication stack integration
- SLAC (Signal Level Attenuation Characterization)
- V2G message handling: SessionSetup, ChargeParameterDiscovery, PowerDelivery
- Plug & Charge (PnC) certificate handling
- Integration with external EVCC (Electric Vehicle Communication Controller)
- Test against ISO 15118 conformance test cases

#### Week 9–10: Integration & Hardening
- Full firmware integration test
- Stress testing: rapid start/stop, fault injection, communication dropout
- Code review and static analysis (MISRA-C subset)
- Flash memory management (firmware update, configuration storage)
- Firmware version management and release tagging

### Deliverables
- [ ] CAN stacking protocol — 5-module 150 kW demonstrated
- [ ] Full protection suite — all fault types tested and logged
- [ ] OCPP 1.6 — compliance test report
- [ ] ISO 15118 — conformance test report
- [ ] Firmware release candidate (RC1) with version tag
- [ ] Static analysis report (no critical/high findings)

### Exit Criteria (Gate 5)
- 5-module 150 kW stacking stable for ≥4 hours
- All protection faults trip correctly and recover (where applicable)
- OCPP 1.6 core + smart charging profiles pass compliance
- ISO 15118 basic session flow demonstrated
- Firmware RC1 tagged; no critical bugs open

---

## Phase 6 — Certification Preparation (8 weeks)

### Objective
Conduct EMC and safety pre-compliance testing; prepare all documentation for formal lab submission.

### Entry Criteria
- Gate 4 (hardware) and Gate 5 (firmware) passed
- Pre-compliance test equipment available (or rented)
- Dedicated test units identified (2 EMC, 2 safety)

### Key Activities

#### Week 1–3: EMC Pre-Compliance
- Conducted emissions (150 kHz – 30 MHz) per CISPR 32 / EN 55032
  - Measure at 25%, 50%, 75%, 100% load
  - Compare to Class B limits with 6 dB margin target
  - Iterate on [[05-EMI Filter Design]] if needed
- Radiated emissions (30 MHz – 1 GHz) per CISPR 32 / EN 55032
  - Measure in pre-compliance chamber or open area
  - Identify any peaks; correlate with switching frequencies
- Harmonics (IEC 61000-3-2) and flicker (IEC 61000-3-3)

#### Week 3–4: EMC Immunity Pre-Test
- Surge (IEC 61000-4-5): ±2 kV L-L, ±4 kV L-PE
- ESD (IEC 61000-4-2): ±8 kV contact, ±15 kV air
- EFT/Burst (IEC 61000-4-4): ±2 kV
- Conducted immunity (IEC 61000-4-6): 10 V
- Radiated immunity (IEC 61000-4-3): 10 V/m
- Voltage dips/interruptions (IEC 61000-4-11)
- Criteria: Performance A (no degradation during test)

#### Week 4–6: Safety Pre-Test
- Hipot test: 3.0 kVAC for 60 s (input to output per [[09-Protection and Safety]])
- Insulation resistance: >10 MΩ at 500 VDC
- Earth leakage current: <3.5 mA
- PE continuity: <0.1 Ω at 25 A
- Touch current measurement
- Temperature rise test at full load (thermocouples on critical components)
- Abnormal conditions: fan failure, single fault, overload

#### Week 6–8: Documentation Preparation
- Technical construction file (TCF):
  - Circuit description and theory of operation
  - Component list with safety certifications (UL/IEC)
  - PCB material certifications (UL 94 V-0)
  - Creepage/clearance analysis per IEC 62368-1
  - Thermal test report
- EMC test report (pre-compliance results + analysis)
- Safety test report (pre-test results)
- Risk assessment per ISO 14971 (if applicable)
- User manual draft (installation, operation, maintenance)

### Deliverables
- [ ] EMC pre-compliance report (emissions + immunity)
- [ ] Safety pre-test report (hipot, insulation, leakage, temperature rise)
- [ ] Technical construction file (TCF) complete
- [ ] Pre-compliance fix list (if any EMC/safety issues found)
- [ ] Lab submission package ready

### Exit Criteria (Gate 6)
- Conducted emissions within Class B limits (6 dB margin)
- Radiated emissions within Class B limits (3 dB margin minimum)
- All immunity tests pass at Performance Criteria A
- Hipot pass at 3.0 kVAC / 60 s
- No safety pre-test failures
- TCF complete and reviewed

---

## Phase 7 — Pre-Production Validation (8 weeks)

### Objective
Complete formal EMC and safety certification at accredited labs, plus HALT and burn-in testing.

### Entry Criteria
- Gate 6 passed
- Lab submission package complete
- Test units shipped to accredited labs

### Key Activities

#### Week 1–4: Formal EMC Testing (Accredited Lab)
- Full EMC test suite per EN 61000-6-1 / EN 61000-6-2 (or product standard)
- Conducted and radiated emissions
- Full immunity suite
- Harmonics and flicker
- Lab issues test report → CB test certificate
- Timeline: typically 2–3 weeks for testing + 1–2 weeks for report

#### Week 1–4: Formal Safety Testing (Accredited Lab)
- Full safety evaluation per IEC 62368-1 (or IEC 61851-23 for EVSE)
- UL 2202 evaluation (parallel with CB scheme)
- Construction evaluation, hipot, leakage, temperature rise, abnormal
- Lab issues test report → CB test certificate + UL listing
- Timeline: typically 4–6 weeks (may extend to 8–12 weeks)

#### Week 3–6: HALT (Highly Accelerated Life Test)
- Thermal step stress: -40°C to +85°C in 10°C steps, 10 min dwell
- Vibration step stress: 5 Grms to 50 Grms
- Combined thermal + vibration
- Identify operating limits and destruct limits
- Root cause analysis on any failures
- Design fixes if failure margin too small

#### Week 5–8: Burn-In
- 500-hour continuous operation at 30 kW, 45°C ambient
- 10 units under test simultaneously
- Monitor: efficiency, temperatures, output ripple
- Log any anomalies or parameter drift
- Target: 0 failures in 500 hours
- Calculate field MTBF estimate from burn-in data

#### Week 6–8: Certification Follow-Up
- Address any lab findings or non-conformances
- Re-test if required (EMC or safety)
- Obtain final certificates
- Update TCF with final test data

### Deliverables
- [ ] EMC test certificate (CB scheme)
- [ ] Safety test certificate (CB scheme + UL 2202)
- [ ] HALT report with operating and destruct limits
- [ ] 500-hour burn-in report
- [ ] Updated TCF with final certification data
- [ ] Field MTBF estimate

### Exit Criteria (Gate 7)
- EMC and safety certificates obtained (no open non-conformances)
- HALT destruct limit >20% above operating limit
- 0 failures in 500-hour burn-in
- MTBF estimate ≥120,000 hours (per spec)

---

## Phase 8 — Production Release (6 weeks)

### Objective
Freeze the BOM, prepare the complete manufacturing package, and complete pilot production.

### Entry Criteria
- Gate 7 passed
- All certifications obtained
- Final firmware release tagged

### Key Activities

#### Week 1–2: BOM Freeze
- Final BOM review: verify all components available, no EOL issues
- Approved alternate components listed (per [[07-BOM and Cost Analysis]])
- Preferred suppliers and distributors confirmed
- Target cost verified at production quantities (100, 500, 1000 units)

#### Week 2–3: Manufacturing Documentation
- Assembly drawings (top/bottom, each board)
- Pick-and-place files (centroid, rotation)
- Stencil files (paste layer)
- Reflow profile specification
- Through-hole assembly instructions
- Mechanical assembly procedure (exploded view, torque specs)
- Wiring harness drawings
- Label and marking specifications

#### Week 3–4: Test Documentation
- Production test procedure (functional test at end of line)
- Test fixture design and fabrication
- Calibration procedure (voltage/current sensing)
- Burn-in procedure (production: 24-hour screen)
- Quality inspection criteria (visual, electrical)
- Shipping test (drop, vibration — if applicable)

#### Week 4–5: Pilot Production Run
- Build 5–10 units using production process
- Verify assembly yield
- Run production test procedure
- Timing study (cycle time per unit)
- Identify process improvements

#### Week 5–6: Handoff
- Manufacturing package review with contract manufacturer
- Training session for production team
- Quality agreement (IPC class, acceptance criteria)
- First article inspection (FAI) process defined
- Post-production support plan

### Deliverables
- [ ] Frozen BOM with alternates
- [ ] Complete manufacturing package (Gerbers, assembly docs, BOMs, test procedures)
- [ ] Production test fixture
- [ ] Pilot production results
- [ ] Quality agreement with manufacturer
- [ ] Firmware production image (signed, versioned)

### Exit Criteria (Gate 8 — Production Release)
- BOM frozen; all components available at target cost
- Manufacturing package reviewed and accepted by CM
- Pilot production yield >95%
- Production test catches all known fault modes
- Firmware production image signed and locked
- All documentation archived

---

## Phase Dependencies and Parallel Execution

```
Phase 0 ──→ Phase 1 ──→ Phase 3 ──→ Phase 4 ──→ Phase 7 ──→ Phase 8
                ↓              ↓           ↓           ↑
             Phase 2 ────→ Phase 3    Phase 5 ──→ Phase 6 ──→ Phase 7
```

### Critical Path
The critical path runs through: **Ph 0 → Ph 1 → Ph 3 → Ph 4 → Ph 6 → Ph 7 → Ph 8**

Schedule compression opportunities:
- Start Phase 2 (FW) before Phase 1 completes (using Nucleo boards)
- Start Phase 5 (FW maturation) before Phase 4 completes (using Rev A units)
- Overlap Phase 6 (cert prep) with late Phase 5
- Run EMC and safety lab tests in parallel (Phase 7)

### Resource Contention Points
- Phase 3 requires both HW and FW teams full-time
- Phase 7 requires 4+ test units (EMC: 2, safety: 2, HALT: 2, burn-in: 10)
- Lab scheduling (external) is a long-lead item — book 8–12 weeks ahead

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
