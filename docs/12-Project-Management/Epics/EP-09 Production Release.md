---
tags: [PDU, project-management, epic, phase-8, production, manufacturing, release]
created: 2026-02-22
---

# EP-09 — Production Release

> **Phase 8 | Duration: 6 weeks | Lead: PM**
> Gate exit: BOM frozen. Manufacturing package complete (Gerbers, assembly procedures, test procedures, firmware binary). Pilot run of 10 units shipped and accepted. Product released for volume production.

---

## Epic Summary

This epic finalizes all deliverables for volume manufacturing. The BOM is frozen, manufacturing documentation is completed, a pilot production run validates the process, and the product is formally released. This is the last phase before handoff to manufacturing.

**Entry criteria:** Certifications obtained (EP-08 complete). Firmware v1.0 tagged. No open critical issues.
**Exit criteria:** Manufacturing package delivered. Pilot run accepted. Product released.

---

## Stories

#### EP-09-001: Freeze BOM for Production
| Field | Value |
|-------|-------|
| **Assignee** | PM, PROC |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-007, EP-05-008 |
| **Blocks** | EP-09-002, EP-09-003 |

**Description:** Lock BOM at final revision. Confirm all components are in active production (no EOL or NRND). Verify minimum 2 approved alternates for all critical parts (SiC MOSFETs, gate drivers, custom magnetics). Set target cost for qty 500 production.

**Acceptance criteria:**
- [ ] BOM locked with revision number (e.g., BOM Rev C)
- [ ] No EOL or NRND components (or approved alternates identified)
- [ ] At least 2 approved sources for all >$10 components
- [ ] Production cost target confirmed: < $1,400 per unit at qty 500

---

#### EP-09-002: Finalize Manufacturing Gerbers and Fab Spec
| Field | Value |
|-------|-------|
| **Assignee** | PCB |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-09-001 |
| **Blocks** | EP-09-004 |

**Description:** Generate final production Gerbers for all 5 boards. Include: panelization for volume production (if applicable), fiducial marks for automated placement, impedance-controlled traces (Controller board), and V-score / tab routing specifications.

**Acceptance criteria:**
- [ ] Gerbers generated from frozen schematic/layout
- [ ] Panelization defined (if needed by volume assembler)
- [ ] Fab specification document: stack-up, copper weight, surface finish, impedance requirements
- [ ] Final Gerber review by PE lead

---

#### EP-09-003: Secure Volume Component Supply
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-09-001 |
| **Blocks** | EP-09-004 |

**Description:** Place blanket orders for first production batch (qty 100 or 500 depending on demand forecast). Negotiate pricing for volume breaks. Secure long-lead items (SiC MOSFETs: schedule 6-month rolling forecast with distributor). Establish safety stock for critical single-source parts (VITROPERM choke).

**Acceptance criteria:**
- [ ] Volume pricing confirmed from at least 2 distributors
- [ ] SiC MOSFET rolling forecast placed (6-month visibility)
- [ ] VITROPERM safety stock ordered (3-month buffer)
- [ ] Custom magnetics vendor confirmed for volume (lead time and MOQ)
- [ ] Total supply chain risk assessment documented

---

#### EP-09-004: Pilot Production Run (10 Units)
| Field | Value |
|-------|-------|
| **Assignee** | PM, ME, PE |
| **Size** | XL (15 days) |
| **Status** | Backlog |
| **Depends on** | EP-09-002, EP-09-003, EP-09-007 |
| **Blocks** | EP-09-005 |

**Description:** Build 10 units using production-intent process: PCBA service for all SMT components, controlled hand-solder for power devices (or automated reflow if process validated), assembly per production procedure. This validates the manufacturing process.

**Acceptance criteria:**
- [ ] 10 units assembled by production-intent process
- [ ] Assembly time tracked (target: < 4 hours per unit)
- [ ] Yield: >=9/10 units pass first-time (90% first-pass yield)
- [ ] Any assembly issues documented as process improvements

---

#### EP-09-005: Pilot Unit Functional Acceptance Test
| Field | Value |
|-------|-------|
| **Assignee** | PE, QA |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-09-004 |
| **Blocks** | EP-09-010 |

**Description:** Run production acceptance test on all 10 pilot units:

| Test | Pass Criteria |
|------|--------------|
| Hipot (production level: 80% of type-test) | No breakdown, leakage < 5 mA |
| Insulation resistance | > 500 kohm |
| Earth continuity | < 0.1 ohm |
| Power-on and self-test | All rails OK, MCU boots |
| 30 kW rated power (10 min) | Efficiency > 95%, no fault |
| CC/CV profile | V within ±0.5%, I within ±1% |
| Thermal spot check | No component > limits |

**Acceptance criteria:**
- [ ] All 10 units pass all tests
- [ ] Test data logged per serial number
- [ ] Production test procedure validated (time per unit: < 30 min)

---

#### EP-09-006: Production Test Fixture Design
| Field | Value |
|-------|-------|
| **Assignee** | PE |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-006, EP-06-014 |
| **Blocks** | EP-09-005 |

**Description:** Design production test fixture with: power connections (AC input, DC output), hipot test jacks, CAN bus connection for automated firmware flash and calibration, NTC simulation resistors, pass/fail indicator LEDs, and test script (Python or similar) for automated acceptance test.

**Acceptance criteria:**
- [ ] Test fixture built and validated
- [ ] Automated test script runs all production tests
- [ ] Firmware flash and calibration automated (< 2 min per unit)
- [ ] Test report auto-generated (PDF with serial number, date, results)

---

#### EP-09-007: Finalize Production Assembly Procedure
| Field | Value |
|-------|-------|
| **Assignee** | ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-010, EP-02-012 |
| **Blocks** | EP-09-004 |

**Description:** Finalize production assembly procedure based on Rev A/B experience and pilot run feedback. Include: step-by-step work instructions with photos, torque specifications, solder temperature profiles, in-process inspection points, and ESD handling requirements.

**Acceptance criteria:**
- [ ] Assembly procedure document finalized (version-controlled)
- [ ] Photos for every critical step
- [ ] Quality checkpoints defined (after SMT, after hand-solder, after mechanical)
- [ ] Procedure validated during pilot run (EP-09-004)

---

#### EP-09-008: Product Labeling and Marking
| Field | Value |
|-------|-------|
| **Assignee** | ME, QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-011 |
| **Blocks** | EP-09-004 |

**Description:** Design product label with: model number, serial number (barcode), electrical ratings (input: 260–530 VAC, output: 150–1000 VDC, 30 kW), certification marks (CE, UL), safety warnings, and manufacturing date code. Design enclosure nameplate.

**Acceptance criteria:**
- [ ] Label layout approved by QA (all required markings present)
- [ ] Certification marks correctly sized per brand guidelines
- [ ] Barcode scannable and linked to production database
- [ ] Label material rated for operating environment (IP20, −30 to +55°C)

---

#### EP-09-009: Create Product Datasheet
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-008, EP-08-010 |
| **Blocks** | — |

**Description:** Create 2-page product datasheet with: key specifications, efficiency curves, derating curves, mechanical drawing, block diagram, ordering information, and certification logos. Based on measured data from EP-04 and EP-08.

**Acceptance criteria:**
- [ ] Datasheet reviewed by PE and QA
- [ ] All specifications from measured data (not design predictions)
- [ ] Efficiency curve from power analyzer data
- [ ] Derating curve from thermal chamber data
- [ ] PDF and editable source file archived

---

#### EP-09-010: Production Release Sign-Off
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (1 day) |
| **Status** | Backlog |
| **Depends on** | EP-09-005 |
| **Blocks** | — |

**Description:** Formal production release meeting. All stakeholders sign off:
- PE: design verified, performance meets spec
- FW: firmware v1.0 released, no critical bugs
- QA: certifications obtained, reliability validated
- PROC: supply chain secured, cost targets met
- PM: schedule and budget closed

**Acceptance criteria:**
- [ ] Release sign-off document signed by all stakeholders
- [ ] Manufacturing package delivered to production:
  - Gerbers (all 5 boards)
  - BOM (frozen, with alternates)
  - Assembly procedure
  - Test procedure and fixture
  - Firmware binary (.hex) with checksum
  - Calibration procedure
  - Product label artwork
- [ ] Project closeout report drafted

---

## References

- [[12-Project-Management/__init|Project Management]] — Phase 8 entry/exit criteria
- [[12-Project-Management/01-Budget Estimate|Budget Estimate]] — Production cost targets
- [[07-BOM and Cost Analysis]] — BOM and cost reduction roadmap
- [[10-Mechanical Integration]] — Assembly specifications and enclosure design

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 10 stories |
