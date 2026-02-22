---
tags: [PDU, project-management, epic, phase-1, prototype, assembly]
created: 2026-02-22
---

# EP-02 — Rev A Prototype Build

> **Phase 1 | Duration: 8 weeks | Lead: PE**
> Gate exit: 5 units assembled and inspected. MCU boots on a custom board. All power rails verified. Gate driver waveforms captured—no assembly defects blocking bring-up.

---

## Epic Summary

This epic covers receiving bare PCBs and components, assembling 5 Rev A prototype units across 5 boards each, performing board-level verification (smoke test, rail checks, MCU boot), and preparing units for firmware bring-up. Power devices and custom magnetics are hand-soldered; SMT passives are placed by PCBA service.

**Entry criteria:** Gerbers sent, component POs placed (EP-01 complete).
**Exit criteria:** 5 units pass board-level test checklist; MCU runs blinky on target board.

---

## Stories

### Board Assembly

#### EP-02-001: Receive and Inspect Bare PCBs
| Field | Value |
|-------|-------|
| **Assignee** | PCB |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-012 |
| **Blocks** | EP-02-002 |

**Description:** Receive bare boards from fabricator. Perform incoming inspection: verify layer count, copper weight, surface finish (ENIG), board thickness, drill accuracy, impedance coupon test results (if ordered).

**Acceptance criteria:**
- [ ] All 5 board types received (6 sets each)
- [ ] Visual inspection: no delamination, scratches, or solder mask defects
- [ ] Impedance test coupon within ±10% of target (Controller board: 50 ohm single-ended)
- [ ] Stack-up cross-section matches specification (if ordered)

---

#### EP-02-002: SMT Assembly — Passive Components and ICs
| Field | Value |
|-------|-------|
| **Assignee** | PROC (coordinate PCBA vendor), PCB |
| **Size** | M (8 days including vendor turnaround) |
| **Status** | Backlog |
| **Depends on** | EP-02-001, EP-01-008 |
| **Blocks** | EP-02-003 |

**Description:** Send bare boards + component kits to PCBA service for SMT placement of passives (resistors, capacitors, inductors) and ICs (STM32G474RE, gate driver support ICs, CAN transceiver, LDOs, op-amps). Exclude power semiconductors (hand-solder) and through-hole magnetics.

**Acceptance criteria:**
- [ ] PCBA vendor confirms component placement matches centroid file
- [ ] X-ray inspection of QFP/QFN packages (MCU, gate drivers) — no bridging or voids
- [ ] AOI (Automated Optical Inspection) report clean
- [ ] 6 sets of each board returned

---

#### EP-02-003: Hand-Solder Power Semiconductors and Magnetics
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | L (15 days — 3 days per unit × 5 units) |
| **Status** | Backlog |
| **Depends on** | EP-02-002, EP-01-004, EP-01-005 |
| **Blocks** | EP-02-006 |

**Description:** Hand-solder SiC MOSFETs (D2PAK-7L package), SiC Schottky diodes, gate driver ICs (STGAP2SiC), EMI filter chokes, LLC transformer, resonant inductors, and bus bar connections. Apply thermal interface material under power devices.

**Per unit (5 boards):**
| Board | Hand-solder items |
|-------|-------------------|
| AC-DC | 6× SiC MOSFETs, 12× SiC diodes, EMI chokes, boost inductors |
| DC-DC | 6× SiC MOSFETs, 12× SiC diodes, 3× LLC transformers, 3× resonant inductors |
| Power Entry | NTC thermistors, bypass relay, output contactor |
| Aux PSU | Flyback transformer, optocouplers |
| Controller | CAN transceiver (if through-hole), test headers |

**Acceptance criteria:**
- [ ] Solder joints inspected under microscope (no cold joints, bridging, or lifted pads)
- [ ] TIM applied to all power device thermal pads (verified by slight squeeze-out)
- [ ] Magnetics mounted with correct polarity (dot convention verified)
- [ ] 5 complete units assembled

---

### Mechanical Assembly

#### EP-02-004: Assemble Bus Bars and Inter-Board Connections
| Field | Value |
|-------|-------|
| **Assignee** | ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-003 |
| **Blocks** | EP-02-006 |

**Description:** Install laminated bus bars (P2 DC bus, 920 V rated, 40 A) and output bus bars (100 A, M8 studs). Connect inter-board signal harnesses (gate drive, ADC sense, CAN, control). Torque all power connections per [[10-Mechanical Integration]] specifications.

**Acceptance criteria:**
- [ ] Bus bar torque values documented (M6: 4.5 Nm, M8: 10 Nm)
- [ ] Inter-board connector pinout verified against schematic
- [ ] Hi-pot pre-test between bus bar and chassis (1000 VDC, 1 s) — no breakdown
- [ ] 5 units wired

---

#### EP-02-005: Mount Boards to Heatsink and Enclosure
| Field | Value |
|-------|-------|
| **Assignee** | ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-004, EP-01-006 |
| **Blocks** | EP-02-006 |

**Description:** Mount AC-DC and DC-DC boards to heatsink using thermal pads and mounting screws. Install Controller and Aux PSU boards on standoffs. Mount fans. Route airflow ducting. Install AC input and DC output connectors on enclosure panel.

**Acceptance criteria:**
- [ ] All boards mechanically secured (screw torque: 0.5 Nm for PCB, 1.0 Nm for heatsink)
- [ ] TIM compression verified (0.25 mm target, measured at 3 points per board)
- [ ] Fans spin freely, airflow direction correct (intake → heatsink → exhaust)
- [ ] Connector panel accessible (AC input terminal, DC output studs, CAN connector)

---

### Board-Level Verification

#### EP-02-006: Board-Level Smoke Test — All 5 Boards
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-005, EP-01-013, EP-01-014 |
| **Blocks** | EP-02-007, EP-02-008 |

**Description:** First power-on with current-limited bench supply. Verify all power rails (3.3 V, 5 V, 12 V, 18 V gate drive, −5 V gate drive) within tolerance. Check quiescent current draw. Inspect for thermal anomalies with thermal camera.

**Per board checklist:**
| Board | Tests |
|-------|-------|
| Aux PSU | 12 V input → all isolated outputs; measure ripple |
| Controller | 3.3 V rail, MCU current draw, LED blink, JTAG connect |
| Power Entry | NTC resistance, relay coil drive, contactor coil drive |
| AC-DC | Gate driver supply rails (18 V / −5 V), bootstrap cap charge |
| DC-DC | Gate driver supply rails, LLC half-bridge midpoint (no ringing) |

**Acceptance criteria:**
- [ ] All rails within ±5% of nominal
- [ ] No components exceed 50 degC above ambient at idle
- [ ] Total quiescent current < 8 W (per project spec)
- [ ] No magic smoke released on any of 5 units

---

#### EP-02-007: MCU Boot and JTAG Verification
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-006 |
| **Blocks** | EP-03-001 |

**Description:** Connect JTAG/SWD probe to Controller board. Verify MCU device ID (STM32G474RE). Flash basic firmware (LED blink, UART printf). Verify clock configuration (170 MHz from HSE). Test GPIO toggling speed.

**Acceptance criteria:**
- [ ] SWD connection established on all 5 units
- [ ] Device ID matches STM32G474RET6 (0x469)
- [ ] LED blink at 1 Hz confirmed
- [ ] UART debug output at 115200 baud confirmed
- [ ] HSE crystal oscillator running (verify with scope on MCO pin)

---

#### EP-02-008: Gate Driver Waveform Capture
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-006, EP-02-007 |
| **Blocks** | EP-03-004, EP-03-006 |

**Description:** With HRTIM generating test PWM (50% duty, 65 kHz for PFC, 150 kHz for LLC), capture gate driver output waveforms on all 12 channels (6 PFC + 6 LLC). Verify rise time, fall time, dead-time, and ringing.

**Measurement targets:**
| Parameter | PFC (65 kHz) | LLC (150 kHz) | Tool |
|-----------|-------------|--------------|------|
| Rise time (10–90%) | < 30 ns | < 20 ns | 500 MHz scope + diff probe |
| Fall time | < 30 ns | < 20 ns | Same |
| Dead-time | 300 ± 50 ns | 100 ± 30 ns | Same |
| Gate voltage (+) | 18 ± 1 V | 18 ± 1 V | Same |
| Gate voltage (−) | −5 ± 0.5 V | −5 ± 0.5 V | Same |
| Ringing pk-pk | < 3 V | < 3 V | Same |

**Acceptance criteria:**
- [ ] All 12 channels waveform-captured and saved
- [ ] Dead-time within spec on all channels
- [ ] No DESAT false trips during test PWM
- [ ] Gate ringing < 3 V pk-pk (if not, gate resistor adjustment noted)

---

#### EP-02-009: ADC Channel Verification
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-007 |
| **Blocks** | EP-03-003 |

**Description:** Apply known voltages/currents to each ADC input channel and verify firmware readings. Test all 5 ADC instances, injected and regular groups. Verify HRTIM ADC trigger routing per [[06-Firmware-Design/06-ADC Pipeline and DMA Configuration]].

| Test | Method | Expected |
|------|--------|----------|
| V_bus sense | Apply 700 VDC via divider test point | ADC reads 700 ± 5 V |
| Phase current | Inject 10 A via current probe | ADC reads 10 ± 0.2 A |
| NTC temperature | Apply 10k resistor (simulates 25 degC) | ADC reads 25 ± 2 degC |
| V_aux_12V | Measure rail directly | ADC reads 12.0 ± 0.2 V |

**Acceptance criteria:**
- [ ] All ADC channels respond to stimulus
- [ ] Calibration offsets recorded for each unit (stored in flash)
- [ ] DMA circular buffer operating correctly (regular group)
- [ ] HRTIM trigger routing verified (injected conversions sync to PWM center)

---

#### EP-02-010: CAN Bus Communication Test
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-007 |
| **Blocks** | EP-03-014 |

**Description:** Connect 2 prototype units via CAN bus (120 ohm termination). Verify basic CAN communication: send/receive test frames at 500 kbps. Test FDCAN Rx FIFO, Tx mailbox, and error counters.

**Acceptance criteria:**
- [ ] Loopback test passes on each unit individually
- [ ] Two-node communication verified (ping-pong at 10 ms interval)
- [ ] Bus-off recovery tested (short bus, verify auto-recovery)
- [ ] DIP switch node ID read correctly

---

### Documentation and Issue Tracking

#### EP-02-011: Create Rev A Issue Tracker
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (0.5 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-006 |
| **Blocks** | EP-05-001 |

**Description:** Create a structured issue log for all Rev A findings: schematic errors, layout issues, assembly difficulties, thermal anomalies, and firmware bring-up blockers. Each issue gets severity (critical/major/minor), owner, and target resolution phase.

**Acceptance criteria:**
- [ ] Issue tracker template created (Markdown table or spreadsheet)
- [ ] All board-level test findings logged
- [ ] Issues categorized by board and severity

---

#### EP-02-012: Photograph and Document Assembly Process
| Field | Value |
|-------|-------|
| **Assignee** | ME |
| **Size** | XS (1 day) |
| **Status** | Backlog |
| **Depends on** | EP-02-005 |
| **Blocks** | EP-09-007 |

**Description:** Photograph each assembly step for future manufacturing documentation. Document torque values, TIM application, bus bar routing, and connector crimping. This becomes the basis for production assembly instructions.

**Acceptance criteria:**
- [ ] Photo set covering all assembly steps
- [ ] Notes on any assembly difficulties or recommended sequence changes

---

#### EP-02-013: Transformer First-Article Inspection
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-005 |
| **Blocks** | EP-02-003 |

**Description:** Receive custom LLC transformers from vendor. Perform incoming inspection: measure magnetizing inductance (target 258 uH ± 10%), leakage inductance (target 10 uH ± 20%), DCR (both windings), turns ratio (n=2), and hipot (4 kVAC, 60 s primary-to-secondary).

**Acceptance criteria:**
- [ ] Lm within 232–284 uH
- [ ] Leakage inductance within 8–12 uH
- [ ] Hipot passed at 4 kVAC for 60 s (no breakdown, leakage < 1 mA)
- [ ] DCR within ±15% of design value
- [ ] First-article inspection report filed

---

#### EP-02-014: Resonant Tank Parameter Measurement
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-013 |
| **Blocks** | EP-03-006 |

**Description:** Measure actual resonant frequency of assembled LLC tank on each unit. Use impedance analyzer or frequency sweep to determine fr = 1/(2*pi*sqrt(Lr*Cr)). Compare with design target of 150.5 kHz. Record per-unit variation.

**Acceptance criteria:**
- [ ] Resonant frequency measured on all 5 units
- [ ] fr within 140–160 kHz (±7% of design center)
- [ ] Lr, Cr values back-calculated and compared with design
- [ ] Unit-to-unit variation documented (target < 3%)

---

## References

- [[12-Project-Management/__init|Project Management]] — Phase 1 entry/exit criteria
- [[10-Mechanical Integration]] — Assembly sequence and torque specifications
- [[07-PCB-Layout/__init|07-PCB Layout]] — Board design documentation
- [[02-Magnetics Design]] — Transformer and inductor specifications

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 14 stories |
