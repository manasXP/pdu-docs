---
tags: [PDU, project-management, epic, phase-6, EMC, safety, pre-compliance, certification]
created: 2026-02-22
---

# EP-07 — Certification Prep

> **Phase 6 | Duration: 8 weeks | Lead: QA**
> Gate exit: Pre-compliance EMC scan passes Class B limits with margin. Safety pre-test passes hipot/insulation. Test documentation package prepared for formal lab submission.

---

## Epic Summary

This epic prepares the product for formal certification testing. Pre-compliance scans identify any EMC or safety issues while corrections are still cost-effective. Test documentation is prepared for the accredited lab. This is the **gate decision** for committing to formal certification spend (~$50–80k).

**Entry criteria:** Rev B units available and functionally verified (EP-05-007). Firmware RC tagged (EP-06-012).
**Exit criteria:** Pre-compliance pass. Test plan approved by lab. Budget authorized for formal testing.

---

## Stories

### EMC Pre-Compliance

#### EP-07-001: Prepare EMC Test Plan
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-007, EP-06-011 |
| **Blocks** | EP-07-002, EP-07-003 |

**Description:** Draft EMC test plan per EN 55032 (emissions) and EN 61000-4 series (immunity). Define test configurations: input voltage (400 VAC), load (30 kW, 50% load, and no-load), cable routing, grounding, and EUT orientation. Identify test lab and confirm equipment availability.

**Standards coverage:**
| Standard | Test | Level |
|----------|------|-------|
| EN 55032 | Conducted emissions (150 kHz – 30 MHz) | Class B |
| EN 55032 | Radiated emissions (30 MHz – 1 GHz) | Class B |
| EN 61000-4-2 | ESD | Level 3 (±6 kV contact, ±8 kV air) |
| EN 61000-4-4 | EFT/Burst | Level 3 (2 kV) |
| EN 61000-4-5 | Surge | Level 3 (1.2/50 us, 2 kV L-N, 4 kV L-PE) |
| EN 61000-4-6 | Conducted immunity | Level 3 (10 V) |
| EN 61000-4-8 | Magnetic field | Level 4 (30 A/m) |
| EN 61000-4-11 | Voltage dips | Per standard |

**Acceptance criteria:**
- [ ] Test plan document completed with all configurations
- [ ] Lab booked with confirmed dates (8–12 wk out typically)
- [ ] Budget estimate for formal testing obtained

---

#### EP-07-002: Build EMC Test Configuration
| Field | Value |
|-------|-------|
| **Assignee** | PE, QA |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-001 |
| **Blocks** | EP-07-003 |

**Description:** Prepare 2 Rev B units for EMC testing: install in final enclosure, route cables per production intent, install EMI filter, apply ferrites (if needed), connect LISN. Prepare test fixture for load simulation.

**Acceptance criteria:**
- [ ] 2 units in production-representative enclosures
- [ ] Cable routing documented (length, shielding, ferrite locations)
- [ ] LISN connected and verified operational
- [ ] Ground plane and bonding straps installed per production intent

---

#### EP-07-003: Conducted Emissions Pre-Compliance Scan
| Field | Value |
|-------|-------|
| **Assignee** | QA, PE |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-002 |
| **Blocks** | EP-07-004, EP-08-002 |

**Description:** Perform conducted emissions scan (150 kHz – 30 MHz) using in-house spectrum analyzer or near-field probe. Test at 30 kW, 15 kW, and no-load. Compare against EN 55032 Class B quasi-peak and average limits. Identify any frequency bands exceeding limit.

**Acceptance criteria:**
- [ ] Conducted emissions below Class B limits with >=6 dB margin at all operating points
- [ ] If margin < 6 dB at any frequency: root cause identified and fix proposed
- [ ] Scan results saved (CSV and screenshot)
- [ ] Report with pass/fail per frequency band

---

#### EP-07-004: Radiated Emissions Pre-Compliance Scan
| Field | Value |
|-------|-------|
| **Assignee** | QA, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-003 |
| **Blocks** | EP-08-002 |

**Description:** Perform radiated emissions scan (30 MHz – 1 GHz) using near-field probes or in-house anechoic measurement. Focus on harmonics of switching frequencies: PFC (65 kHz × harmonics), LLC (150 kHz × harmonics). Identify any frequencies requiring additional shielding or filtering.

**Acceptance criteria:**
- [ ] Radiated emissions below Class B limits with >=6 dB margin
- [ ] If issues found: shielding or layout fix proposed
- [ ] Test documented with probe positions and orientations

---

### Safety Pre-Compliance

#### EP-07-005: Safety Pre-Test — Hipot and Insulation
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-012 |
| **Blocks** | EP-08-003 |

**Description:** Perform full type-test level hipot per [[09-Protection and Safety]]:

| Test | Voltage | Duration | Limit |
|------|---------|----------|-------|
| Primary-to-secondary | 4000 VAC | 60 s | No breakdown, leakage < 5 mA |
| AC input-to-PE | 3000 VAC | 60 s | No breakdown |
| DC output-to-PE | 3750 VAC | 60 s | No breakdown |
| Insulation resistance (all pairs) | 500 VDC | — | > 10 Mohm |

Additionally measure partial discharge at 1.5× working voltage (< 10 pC).

**Acceptance criteria:**
- [ ] All hipot tests pass on 2 Rev B units
- [ ] Insulation resistance > 10 Mohm on all isolation barriers
- [ ] Partial discharge < 10 pC (if PD measurement available)
- [ ] Test results documented per unit serial number

---

#### EP-07-006: Safety Pre-Test — Earth Continuity and Leakage
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-005 |
| **Blocks** | EP-08-003 |

**Description:** Measure earth continuity between PE terminal and all exposed metalwork (< 0.1 ohm at 25 A). Measure touch current / leakage current at rated input voltage (< 3.5 mA per IEC 62368-1).

**Acceptance criteria:**
- [ ] Earth continuity < 0.1 ohm at all accessible metal parts
- [ ] Leakage current < 3.5 mA at 530 VAC / 60 Hz (worst case)
- [ ] Y-cap leakage contribution measured and budgeted

---

#### EP-07-007: Ground Fault / RCD Functional Test
| Field | Value |
|-------|-------|
| **Assignee** | QA, FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-008 |
| **Blocks** | EP-08-003 |

**Description:** Test DC residual current monitoring (RCM) per IEC 62955. Inject known DC fault current and verify detection threshold (> 6 mA) and shutdown response time (< 1 s). Test with both AC and DC fault components.

**Acceptance criteria:**
- [ ] RCM detects 6 mA DC fault current within 300 ms
- [ ] System shuts down within 1 s of RCM trip
- [ ] AC component rejection verified (no false trip at rated load)
- [ ] Test documented for certification submission

---

### Documentation

#### EP-07-008: Compile Certification Documentation Package
| Field | Value |
|-------|-------|
| **Assignee** | QA, PM |
| **Size** | L (15 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-003, EP-07-005 |
| **Blocks** | EP-08-001 |

**Description:** Prepare complete documentation package for accredited test lab:
- Circuit descriptions (all 5 boards)
- Safety critical component list (insulation, Y-caps, fuses, MOVs)
- Creepage/clearance analysis
- Thermal derating analysis
- Risk assessment (IEC 62368-1 energy source classification)
- EMC filter design rationale
- Protection function description

**Acceptance criteria:**
- [ ] Documentation package reviewed by lab (pre-submission review)
- [ ] All safety-critical components have certification marks (UL, VDE, etc.)
- [ ] Creepage/clearance analysis matches actual PCB measurements
- [ ] Lab confirms package is sufficient for test program start

---

#### EP-07-009: EMC Fix Implementation (If Needed)
| Field | Value |
|-------|-------|
| **Assignee** | PE, PCB |
| **Size** | M (5 days) — conditional |
| **Status** | Backlog |
| **Depends on** | EP-07-003, EP-07-004 |
| **Blocks** | EP-08-002 |

**Description:** If pre-compliance scans reveal emissions exceeding limits: implement fixes (additional filtering, shielding, ferrite beads, layout changes). Re-test after fix. This story is conditional — may not be needed.

**Acceptance criteria:**
- [ ] Root cause identified for each failing frequency
- [ ] Fix implemented and re-tested
- [ ] Post-fix emissions within Class B with >=6 dB margin

---

#### EP-07-010: Safety Fix Implementation (If Needed)
| Field | Value |
|-------|-------|
| **Assignee** | PE, PCB |
| **Size** | M (5 days) — conditional |
| **Status** | Backlog |
| **Depends on** | EP-07-005, EP-07-006, EP-07-007 |
| **Blocks** | EP-08-003 |

**Description:** If safety pre-tests reveal issues (hipot failure, excessive leakage, creepage violation): implement fixes (increased isolation distance, different Y-caps, additional conformal coating). Re-test after fix.

**Acceptance criteria:**
- [ ] Root cause identified for each failure
- [ ] Fix implemented and re-tested to pass

---

#### EP-07-011: Surge Immunity Pre-Test
| Field | Value |
|-------|-------|
| **Assignee** | QA, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-002 |
| **Blocks** | EP-08-004 |

**Description:** Test surge immunity per EN 61000-4-5 Level 3: 1.2/50 us combined wave, 2 kV line-to-neutral, 4 kV line-to-PE. Apply ±5 surges on each line/phase. Verify MOV clamping and no damage to downstream components.

**Acceptance criteria:**
- [ ] EUT survives all surges without damage
- [ ] MOV clamping voltage measured (should not exceed 1200 V peak)
- [ ] No protection trips during surge (MOV absorbs energy)
- [ ] EUT operates normally after each surge

---

#### EP-07-012: ESD and EFT/Burst Pre-Test
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-002 |
| **Blocks** | EP-08-004 |

**Description:** Test ESD per EN 61000-4-2 Level 3 (±6 kV contact, ±8 kV air) on all accessible surfaces and connectors. Test EFT/Burst per EN 61000-4-4 Level 3 (2 kV) on AC input and CAN bus.

**Acceptance criteria:**
- [ ] No permanent damage from ESD
- [ ] Temporary upset acceptable (criterion B) — system recovers within 5 s
- [ ] EFT/Burst: no communication errors on CAN, no protection trips
- [ ] Results documented per test point

---

#### EP-07-013: Formal Lab Engagement and Schedule
| Field | Value |
|-------|-------|
| **Assignee** | PM, QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-008 |
| **Blocks** | EP-08-001 |

**Description:** Finalize contract with accredited test lab (TUV, UL, Intertek, etc.) for formal EMC + safety testing. Confirm test dates, sample requirements, documentation submission deadline, and budget.

**Acceptance criteria:**
- [ ] Lab contract signed
- [ ] Test dates confirmed (typically 4–6 weeks of testing)
- [ ] Budget authorized (~$50–80k for EMC + safety + CB report)
- [ ] Sample shipping coordinated (2 units for EMC, 2 for safety)

---

## References

- [[09-Protection and Safety]] — Protection thresholds, insulation requirements, compliance matrix
- [[05-EMI Filter Design]] — EMI filter design and insertion loss
- [[12-Project-Management/01-Budget Estimate|Budget Estimate]] — Certification budget

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 13 stories |
