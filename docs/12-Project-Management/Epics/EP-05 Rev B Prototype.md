---
tags: [PDU, project-management, epic, phase-4, rev-B, prototype, re-spin]
created: 2026-02-22
---

# EP-05 — Rev B Prototype

> **Phase 4 | Duration: 8 weeks | Lead: PCB**
> Gate exit: 10 Rev B units built and functionally tested. All critical/major Rev A issues resolved. Layout optimized per thermal and EMI findings.

---

## Epic Summary

This epic incorporates all Rev A lessons into a revised PCB design, orders new boards and components, assembles 10 units for certification and extended testing, and validates that Rev A issues are resolved.

**Entry criteria:** Rev A issue list prioritized (EP-04-014 complete). Design fixes agreed.
**Exit criteria:** 10 Rev B units pass functional test. No critical open issues.

---

## Stories

#### EP-05-001: Prioritize Rev A Issues and Define Fixes
| Field | Value |
|-------|-------|
| **Assignee** | PE, PCB, FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-014, EP-02-011 |
| **Blocks** | EP-05-002 |

**Description:** Review consolidated Rev A issue list. Classify fixes into: schematic change, layout change, firmware workaround, BOM substitution. Assign owners and estimate effort per fix.

**Acceptance criteria:**
- [ ] All critical issues have a defined fix with owner
- [ ] Fixes categorized (schematic/layout/FW/BOM)
- [ ] Change requests documented in design review format

---

#### EP-05-002: Rev B Schematic and Layout Update
| Field | Value |
|-------|-------|
| **Assignee** | PCB, PE |
| **Size** | XL (20 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-001, EP-04-006, EP-04-007, EP-04-013 |
| **Blocks** | EP-05-003 |

**Description:** Implement schematic fixes. Update PCB layout for all 5 boards. Incorporate thermal improvements (if any: larger copper pours, additional thermal vias, adjusted TIM pad area). Incorporate EMI layout improvements (if any from EP-04 observations). Re-run DRC and ERC. Regenerate manufacturing outputs.

**Acceptance criteria:**
- [ ] All critical and major Rev A fixes implemented
- [ ] Creepage/clearance verified on updated layout
- [ ] Power loop inductance re-estimated (target: no regression)
- [ ] Gerbers generated and verified in CAM viewer

---

#### EP-05-003: Incorporate CFD Thermal Findings
| Field | Value |
|-------|-------|
| **Assignee** | ME, PCB |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-011, EP-05-002 |
| **Blocks** | EP-05-004 |

**Description:** If CFD simulation (EP-04-011) identified airflow dead zones or inadequate cooling, update enclosure (inlet/outlet aperture size, fan ducting) and/or heatsink (fin spacing). Update mechanical drawings.

**Acceptance criteria:**
- [ ] CFD recommendations reviewed and accepted/rejected with rationale
- [ ] Mechanical drawings updated (if applicable)
- [ ] Fan selection confirmed or changed (if airflow insufficient)

---

#### EP-05-004: Order Rev B PCBs and Updated Components
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | M (5 days + 3 wk fab lead) |
| **Status** | Backlog |
| **Depends on** | EP-05-002, EP-05-003 |
| **Blocks** | EP-05-005 |

**Description:** Submit Rev B Gerbers to fabricator. Order 12 sets (10 + 2 spare). Order any new/changed components. Reuse remaining SiC inventory from Rev A (if undamaged).

**Acceptance criteria:**
- [ ] PCB fab order placed with confirmed delivery
- [ ] BOM delta identified (new/changed parts vs. Rev A)
- [ ] New component orders placed or confirmed from existing inventory

---

#### EP-05-005: Assemble 10 Rev B Units
| Field | Value |
|-------|-------|
| **Assignee** | PE, ME |
| **Size** | XL (20 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-004 |
| **Blocks** | EP-05-006 |

**Description:** Repeat assembly process from EP-02 for 10 units. Use updated assembly procedure based on EP-02-012 photos and lessons learned. PCBA service for SMT, hand-solder power devices and magnetics.

**Acceptance criteria:**
- [ ] 10 units fully assembled and mechanically integrated
- [ ] Assembly procedure updated with any new steps
- [ ] Visual inspection complete (no solder defects)

---

#### EP-05-006: Rev B Board-Level Verification
| Field | Value |
|-------|-------|
| **Assignee** | PE, FW |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-005 |
| **Blocks** | EP-05-007 |

**Description:** Repeat board-level tests from EP-02-006 through EP-02-010 on all 10 units. Verify Rev A fixes are effective. Flash latest firmware.

**Acceptance criteria:**
- [ ] All 10 units pass smoke test and rail verification
- [ ] MCU boots and runs on all 10 units
- [ ] Rev A issues confirmed resolved on spot-check (3 units minimum)

---

#### EP-05-007: Rev B Functional Test — Full Power
| Field | Value |
|-------|-------|
| **Assignee** | PE, FW |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-006 |
| **Blocks** | EP-06-001, EP-07-001, EP-08-001 |

**Description:** Run each Rev B unit at rated power (30 kW) for 30 minutes. Verify efficiency, thermal, and protection. This is the acceptance test before units are allocated to certification (EP-07/08) and firmware maturation (EP-06).

**Acceptance criteria:**
- [ ] All 10 units achieve 30 kW without fault
- [ ] Efficiency > 95% on all units (> 96% target on majority)
- [ ] No component exceeds temperature limit at 25°C ambient
- [ ] Units allocated: 2 for EMC, 2 for safety, 5 for stacking, 1 spare

---

#### EP-05-008: Update BOM with Rev B Changes
| Field | Value |
|-------|-------|
| **Assignee** | PROC |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-002 |
| **Blocks** | EP-09-001 |

**Description:** Update [[07-BOM and Cost Analysis]] with Rev B component changes. Recalculate per-unit cost. Identify cost reduction opportunities from Rev A experience (alternate parts, quantity breaks).

**Acceptance criteria:**
- [ ] BOM updated with Rev B part numbers and quantities
- [ ] Cost delta from Rev A calculated
- [ ] Cost reduction roadmap updated (target: -10% for production)

---

#### EP-05-009: Update Rev B Issue Tracker
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (0.5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-007 |
| **Blocks** | — |

**Description:** Log any new issues discovered during Rev B testing. Close Rev A issues confirmed fixed. Carry forward any remaining items to Rev C or production.

**Acceptance criteria:**
- [ ] Rev A issues marked closed or carried forward
- [ ] Rev B-specific issues logged (if any)

---

#### EP-05-010: Production Assembly Procedure Draft
| Field | Value |
|-------|-------|
| **Assignee** | ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-005, EP-02-012 |
| **Blocks** | EP-09-007 |

**Description:** Draft production assembly procedure based on Rev A/B experience. Include step-by-step instructions with photos, torque specifications, test checkpoints, and quality inspection criteria.

**Acceptance criteria:**
- [ ] Step-by-step procedure document created
- [ ] Photos from Rev A/B assembly incorporated
- [ ] Critical dimensions and torque values specified
- [ ] In-process test points identified (rail check, hipot)

---

#### EP-05-011: Allocate Units for Downstream Phases
| Field | Value |
|-------|-------|
| **Assignee** | PM |
| **Size** | XS (0.5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-007 |
| **Blocks** | EP-06-001, EP-07-001 |

**Description:** Allocate 10 Rev B units across downstream activities:

| Allocation | Units | Purpose |
|-----------|-------|---------|
| CAN stacking development | 5 | EP-06: 5-module parallel test |
| EMC pre-compliance | 2 | EP-07: conducted/radiated emissions |
| Safety pre-test | 2 | EP-07: hipot, insulation |
| Spare / burn-in | 1 | Buffer for failures |

**Acceptance criteria:**
- [ ] Units labeled and assigned
- [ ] Serial numbers tracked in test log

---

#### EP-05-012: Hipot Pre-Test on Rev B Units
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-006 |
| **Blocks** | EP-07-005 |

**Description:** Perform hipot pre-test on all 10 Rev B units per [[09-Protection and Safety]] production test limits: primary-to-secondary 3200 VAC (80% of type-test), 1 s duration, leakage < 5 mA. Verify earth continuity < 0.1 ohm.

**Acceptance criteria:**
- [ ] All 10 units pass hipot without breakdown
- [ ] Leakage current recorded per unit (target < 3 mA)
- [ ] Earth continuity < 0.1 ohm on all units
- [ ] Any failures investigated and root-caused

---

## References

- [[12-Project-Management/__init|Project Management]] — Phase 4 entry/exit criteria
- [[07-BOM and Cost Analysis]] — BOM baseline
- [[10-Mechanical Integration]] — Assembly specifications

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 12 stories |
