---
tags: [PDU, project-management, epic, phase-0, procurement, design-review]
created: 2026-02-22
---

# EP-01 — Design Review and Procurement

> **Phase 0 | Duration: 6 weeks | Lead: PM**
> Gate exit: All design documents peer-reviewed and signed off. Long-lead component orders placed. Test equipment availability confirmed.

---

## Epic Summary

This epic closes the design phase and initiates procurement of long-lead items. Every design document is formally reviewed, critical decisions are locked, and purchase orders are placed for SiC MOSFETs (12–16 week lead), custom magnetics (6–8 week lead), and mechanical parts (heatsinks, enclosures). The firmware BSP can begin on a Nucleo development board in parallel.

**Entry criteria:** All 10 design documents at draft status or better.
**Exit criteria:** Design review minutes signed, BOM locked (Rev A), POs placed for critical-path items.

---

## Stories

### Design Reviews

#### EP-01-001: Conduct Topology and Magnetics Design Review
| Field | Value |
|-------|-------|
| **Assignee** | PE (lead), all |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-01-004, EP-01-005 |

**Description:** Formal peer review of [[01-Topology Selection]] and [[02-Magnetics Design]]. Verify Vienna PFC + 3-phase interleaved LLC selection rationale, resonant tank parameters (Lr=43 uH, Cr=26 nF, Lm=258 uH), transformer design (E65/32/27, 3C97, Np=21/Ns=42), and resonant inductor (Kool Mu 77439, 33 uH).

**Acceptance criteria:**
- [ ] Review meeting held with minutes documented
- [ ] All open action items assigned with due dates
- [ ] Transformer winding specification signed off
- [ ] Resonant tank tolerance analysis reviewed (Monte Carlo from [[03-LLC Gain Curve Verification]])
- [ ] ZVS boundary at Vbus=920V confirmed acceptable (3% margin above fr2)

---

#### EP-01-002: Conduct Thermal and EMI Design Review
| Field | Value |
|-------|-------|
| **Assignee** | PE (lead), ME, TH |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-01-006, EP-01-007 |

**Description:** Review [[04-Thermal Budget]] and [[05-EMI Filter Design]]. Verify 941 W total loss budget (399 W PFC + 497 W LLC + 45 W aux), heatsink sizing (Rth_sa = 0.07–0.10 degC/W), derating schedule (30 kW at 45 degC, 0 kW at 65 degC), EMI filter design (2-stage CM/DM, VITROPERM W914 + MnZn R42), and surge protection (MOV 680 VAC, 20 kA).

**Acceptance criteria:**
- [ ] Thermal resistance network reviewed and approved
- [ ] Derating curve shape agreed (linear vs. step)
- [ ] EMI filter insertion loss calculations checked
- [ ] Y-cap leakage current budget verified (< 3.5 mA per IEC 62368-1)
- [ ] Surge protection MOV energy rating confirmed for IEC 61000-4-5 Level 3

---

#### EP-01-003: Conduct Firmware Architecture and Protection Review
| Field | Value |
|-------|-------|
| **Assignee** | FW (lead), PE, QA |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-03-001 |

**Description:** Review [[06-Firmware Architecture]], [[06-Firmware-Design/__init|06-Firmware Design]] sub-documents, [[08-Power-On Sequence and Inrush Management]], and [[09-Protection and Safety]]. Verify HRTIM resource map, ADC allocation, state machine design, fault classification, protection thresholds, and startup timing budget (<=6 s).

**Acceptance criteria:**
- [ ] HRTIM timer allocation (A–C PFC, D–F LLC) confirmed feasible
- [ ] ADC channel mapping verified against PCB schematic net names
- [ ] 10-state application state machine approved
- [ ] 24 fault sources reviewed with severity assignments agreed
- [ ] Hardware protection latencies verified (< 200 ns OCP, < 1 us OVP)
- [ ] Startup timing budget walkthrough completed (<=6 s total)

---

### Procurement

#### EP-01-004: Place SiC MOSFET and Diode Orders
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-001 |
| **Blocks** | EP-02-003 |

**Description:** Order SiC semiconductors for Rev A build (5 units + 20% spares). This is the **critical-path long-lead item** (12–16 week lead time).

| Part | Quantity (5 units + spares) | Vendor | Lead Time |
|------|---------------------------|--------|-----------|
| SCTWA90N65G2V-4 (650 V, PFC) | 6 × 6 = 36 | ST Micro | 12–16 wk |
| STPSC40H12C (1200 V diode, PFC) | 12 × 6 = 72 | ST Micro | 12 wk |
| SCTW100N120G2AG (1200 V, LLC primary) | 6 × 6 = 36 | ST Micro | 12–16 wk |
| STPSC20H065CW (650 V diode, LLC secondary) | 12 × 6 = 72 | ST Micro | 10 wk |
| STGAP2SiC (gate driver) | 6 × 6 = 36 | ST Micro | 8 wk |

**Acceptance criteria:**
- [ ] PO placed with confirmed delivery date
- [ ] At least one alternate source identified per part (Wolfspeed C3M, onsemi NTHL)
- [ ] Broker market checked for immediate availability (eval qty)
- [ ] Budget: ~$600 × 6 = $3,600 semiconductor cost

---

#### EP-01-005: Order Custom Magnetics
| Field | Value |
|-------|-------|
| **Assignee** | PROC, PE |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-001 |
| **Blocks** | EP-02-003 |

**Description:** Engage magnetics vendor for LLC transformer (E65/32/27, 3C97, P-S-P-S interleaved), resonant inductor (Kool Mu 77439), and PFC boost inductors. Provide winding specification, creepage requirements (25 mm primary-secondary), and thermal class (Class F, 155 degC).

**Acceptance criteria:**
- [ ] Transformer winding specification document sent to vendor
- [ ] Vendor quote received (target: < $45/unit at qty 30)
- [ ] PO placed with 6–8 week delivery confirmed
- [ ] First-article inspection criteria defined (leakage inductance, magnetizing inductance, DCR)

---

#### EP-01-006: Order Mechanical Parts (Heatsink, Enclosure, Fans)
| Field | Value |
|-------|-------|
| **Assignee** | PROC, ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-002 |
| **Blocks** | EP-02-005 |

**Description:** Order heatsink extrusion (455 x 180 mm, 50 fins), enclosure sheet metal (6061-T6, powder coat RAL 7016), fans (2x Sanyo Denki 9GA0812P4G01, 80 mm, 67.9 CFM), and thermal interface material (Bergquist GP3000S, 0.25 mm).

**Acceptance criteria:**
- [ ] Heatsink vendor quote (custom extrusion NRE if needed)
- [ ] Enclosure fabrication quote (laser cut, bend, powder coat)
- [ ] Fan and TIM ordered (standard distribution, 2–4 wk)
- [ ] Total mechanical cost per unit confirmed (target < $264)

---

#### EP-01-007: Order EMI Filter Components
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-002 |
| **Blocks** | EP-02-003 |

**Description:** Order VITROPERM W914 nanocrystalline CM choke (3.3 mH, single-source from VAC/Vacuumschmelze), MnZn R42 ferrite CM choke (1.0 mH), X-capacitors (2.2 uF + 1.0 uF), Y-capacitors (22 nF), and MOVs (680 VAC rated).

**Acceptance criteria:**
- [ ] VITROPERM W914 availability confirmed (single-source risk acknowledged)
- [ ] Alternate identified: Magnetec M-403-A (if lead time > 8 wk)
- [ ] All passives ordered from distribution (Mouser/DigiKey)

---

#### EP-01-008: Finalize Rev A BOM and Generate Purchase Orders
| Field | Value |
|-------|-------|
| **Assignee** | PM, PROC |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-001, EP-01-002 |
| **Blocks** | EP-02-001 |

**Description:** Consolidate complete BOM across all 5 boards (Power Entry, AC-DC, DC-DC, Controller, Aux PSU) per [[07-BOM and Cost Analysis]]. Verify all line items have part numbers, quantities for 5+1 units, and at least one alternate for critical parts. Generate POs for remaining components (passives, connectors, MCU, misc).

**Acceptance criteria:**
- [ ] BOM exported as CSV with columns: RefDes, MPN, Qty, Unit Cost, Vendor, Lead Time, Alternate
- [ ] Total Rev A build cost calculated (target: 6 × $1,726 = ~$10,350)
- [ ] All POs placed or distribution cart submitted
- [ ] Long-lead items flagged and tracked on procurement dashboard

---

### PCB and Schematic Finalization

#### EP-01-009: Schematic Peer Review — All 5 Boards
| Field | Value |
|-------|-------|
| **Assignee** | PCB (lead), PE, FW |
| **Size** | L (12 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-001, EP-01-002, EP-01-003 |
| **Blocks** | EP-01-011 |

**Description:** Formal schematic review for all 5 PCBs. Check net naming consistency, power rail decoupling, gate driver bootstrap circuits, analog signal conditioning (ADC input filters, voltage dividers), protection circuits (comparator thresholds match [[09-Protection and Safety]]), and inter-board connector pinouts.

**Acceptance criteria:**
- [ ] Each board reviewed by at least 2 engineers (PE + FW for Controller, PE + PE for power boards)
- [ ] ERC (Electrical Rules Check) clean for all boards
- [ ] Net names match firmware ADC channel mapping from [[06-Firmware Architecture]] §2.2
- [ ] Gate driver decoupling matches STGAP2SiC datasheet recommendations
- [ ] Review action items tracked and closed

---

#### EP-01-010: PCB Layout Final Review — Creepage, Clearance, Thermal
| Field | Value |
|-------|-------|
| **Assignee** | PCB (lead), PE, QA |
| **Size** | L (12 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-009 |
| **Blocks** | EP-01-012 |

**Description:** Final layout review per [[07-PCB-Layout/__init|07-PCB Layout]] documentation. Verify creepage/clearance (25 mm primary-secondary, 16 mm output-PE), power loop inductance (PFC < 10 nH, LLC < 8 nH), thermal pad placement, copper pour connectivity, and DFM rules.

**Acceptance criteria:**
- [ ] Creepage/clearance measurement report for AC-DC and DC-DC boards
- [ ] Power loop inductance estimated (field solver or Q3D extraction)
- [ ] Thermal via arrays verified under all power devices
- [ ] DFM check passed (min trace width, drill sizes, solder mask expansion)
- [ ] Gerber review sign-off by PE lead

---

#### EP-01-011: Generate Manufacturing Outputs — All 5 Boards
| Field | Value |
|-------|-------|
| **Assignee** | PCB |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-010 |
| **Blocks** | EP-02-001 |

**Description:** Generate Gerber files (RS-274X), drill files (Excellon), pick-and-place centroid files, assembly drawings, and fabrication notes for all 5 boards. Include stack-up specifications per board documentation.

**Acceptance criteria:**
- [ ] Gerber output verified in CAM viewer (no missing layers, correct layer mapping)
- [ ] Fab notes include stack-up, impedance control, surface finish (ENIG), and board thickness
- [ ] Assembly drawings include polarity markings, keep-out zones, and heatsink mounting holes

---

#### EP-01-012: Place PCB Fabrication and Assembly Orders
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-011 |
| **Blocks** | EP-02-002 |

**Description:** Submit Gerbers to PCB fabricator. Order bare boards (6 sets, 5+1 spare) and arrange PCBA service for passive/IC placement. Power devices and custom magnetics will be hand-soldered.

**Acceptance criteria:**
- [ ] Fab quote received (target: 2–3 wk lead for prototype qty)
- [ ] PCBA service confirmed for SMT passives and ICs
- [ ] Stencil ordered for hand assembly of power boards

---

### Test Equipment and Lab Setup

#### EP-01-013: Secure Test Equipment Access
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-02-006 |

**Description:** Confirm availability of required test equipment for Phase 1–3 testing.

| Equipment | Specification | Purpose |
|-----------|--------------|---------|
| 3-phase AC source | 30 kW, 260–530 VAC, programmable | PFC input |
| DC electronic load | 30 kW, 0–1000 VDC, 0–100 A, CC/CV/CP modes | LLC output |
| Power analyzer | Yokogawa WT3000 or equivalent, 6 channels | Efficiency measurement |
| Oscilloscope | 4-ch, >=500 MHz, isolated probes | Waveform capture |
| Thermal camera | FLIR or equivalent, resolution <=0.1 degC | Thermal characterization |
| Safety analyzer | Hipot tester, insulation resistance meter | Safety pre-test |

**Acceptance criteria:**
- [ ] All equipment available in-house or rental contract signed
- [ ] Calibration certificates current for power analyzer and safety analyzer
- [ ] Lab bench provisioned with 3-phase power, cooling air, safety barriers

---

#### EP-01-014: Design Test Fixture for Board-Level Verification
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-009 |
| **Blocks** | EP-02-006 |

**Description:** Design a test jig with banana-jack breakouts for power rails, SMA connectors for gate drive signals, and NTC simulator resistors. Include a test procedure checklist per [[12-Project-Management/Epics/EP-02 Rev A Prototype Build|EP-02 Rev A Prototype Build]] board-level tests.

**Acceptance criteria:**
- [ ] Test jig schematic and layout complete
- [ ] Test procedure checklist created (smoke test, rail verification, MCU boot, gate driver waveform)

---

### Firmware Preparation

#### EP-01-015: Set Up Firmware Repository and Toolchain
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-01-016 |

**Description:** Create git repository, configure STM32CubeIDE project for G474RE, set up CI (build + static analysis), establish coding standard (MISRA-C subset), and configure JTAG/SWD debug probe.

**Acceptance criteria:**
- [ ] Repository created with `.gitignore`, `Makefile`, and CubeIDE project
- [ ] CI pipeline builds successfully (ARM GCC toolchain)
- [ ] MISRA-C checker configured (PC-lint or cppcheck with MISRA rules)
- [ ] Debug probe tested with Nucleo-G474RE board

---

#### EP-01-016: Generate CubeMX Baseline Configuration
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-015, EP-01-003 |
| **Blocks** | EP-03-001 |

**Description:** Configure STM32CubeMX for G474RE: clock tree (170 MHz PLL from HSE), HRTIM (6 timers, fault inputs, DLL), ADC1–5 (injected + regular groups), DMA channels, FDCAN1 (500 kbps), TIM6 (1 kHz tick), GPIO pinout. Generate HAL/LL initialization code.

**Acceptance criteria:**
- [ ] CubeMX `.ioc` file committed
- [ ] Generated code compiles cleanly
- [ ] Clock tree verified: 170 MHz SYSCLK, HRTIM DLL 5.44 GHz
- [ ] Pin assignments match Controller board schematic

---

### Risk and Schedule

#### EP-01-017: Update Risk Register with Procurement Status
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (1 day) |
| **Status** | Backlog |
| **Depends on** | EP-01-004, EP-01-005 |
| **Blocks** | — |

**Description:** Update [[12-Project-Management/02-Risk Register|Risk Register]] with actual lead times from vendor quotes. Adjust risk scores for S1 (SiC availability), S3 (single-source VITROPERM), and SC2 (integration debug overrun).

**Acceptance criteria:**
- [ ] Risk register updated with confirmed lead times
- [ ] Mitigation actions assigned for any red-flag items

---

#### EP-01-018: Create Detailed Phase 1–2 Schedule
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (1 day) |
| **Status** | Backlog |
| **Depends on** | EP-01-004, EP-01-012 |
| **Blocks** | — |

**Description:** Create week-by-week Gantt chart for Phases 1–2 based on actual vendor lead times. Identify float and critical path. Schedule key milestones: boards received, first power-on, PFC open-loop, LLC open-loop.

**Acceptance criteria:**
- [ ] Gantt chart exported (Markdown table or Mermaid diagram)
- [ ] Critical path identified and shared with team
- [ ] Milestone dates committed

---

## References

- [[12-Project-Management/__init|Project Management]] — Phase 0 entry/exit criteria
- [[07-BOM and Cost Analysis]] — BOM baseline and cost targets
- [[07-PCB-Layout/__init|07-PCB Layout]] — PCB design documentation
- [[09-Protection and Safety]] — Compliance requirements
- [[12-Project-Management/02-Risk Register|Risk Register]] — Programme risks

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 18 stories |
