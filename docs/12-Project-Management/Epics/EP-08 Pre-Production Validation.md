---
tags: [PDU, project-management, epic, phase-7, certification, HALT, burn-in, validation]
created: 2026-02-22
---

# EP-08 — Pre-Production Validation

> **Phase 7 | Duration: 8 weeks | Lead: QA**
> Gate exit: Formal EMC and safety certifications obtained (CB scheme + UL mark). HALT/burn-in completed (500 hours). All test reports filed.

---

## Epic Summary

This epic executes formal certification testing at an accredited lab and performs reliability validation (HALT/burn-in). The product exits this phase with marketable certifications and validated reliability data. Any issues discovered require immediate resolution before production release.

**Entry criteria:** Pre-compliance pass (EP-07 complete). Lab contract signed (EP-07-013). Rev B units allocated.
**Exit criteria:** CB test report issued. UL certification mark authorized. 500-hour burn-in complete with zero failures.

---

## Stories

#### EP-08-001: Ship Samples and Documentation to Lab
| Field | Value |
|-------|-------|
| **Assignee** | PM, QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-07-008, EP-07-013, EP-05-007 |
| **Blocks** | EP-08-002, EP-08-003, EP-08-004 |

**Description:** Ship 4 Rev B units (2 EMC, 2 safety) and complete documentation package to accredited test lab. Include: test plan, circuit descriptions, safety component list, creepage/clearance analysis, operating manual.

**Acceptance criteria:**
- [ ] 4 units shipped with tracking
- [ ] Documentation package submitted (electronic and hard copy)
- [ ] Lab confirms receipt and test program kickoff date

---

#### EP-08-002: Formal EMC Testing (Emissions + Immunity)
| Field | Value |
|-------|-------|
| **Assignee** | QA (monitor), lab (execute) |
| **Size** | XL (25 days — lab calendar time) |
| **Status** | Backlog |
| **Depends on** | EP-08-001, EP-07-003, EP-07-004 |
| **Blocks** | EP-08-007 |

**Description:** Lab executes full EMC test program per EN 55032 (emissions) and EN 61000-4 series (immunity). Engineer on-site support for first 2 days to answer questions and assist with test setup.

| Test | Standard | Duration |
|------|----------|----------|
| Conducted emissions | EN 55032 Class B | 3 days |
| Radiated emissions | EN 55032 Class B | 3 days |
| ESD | EN 61000-4-2 Level 3 | 1 day |
| EFT/Burst | EN 61000-4-4 Level 3 | 1 day |
| Surge | EN 61000-4-5 Level 3 | 2 days |
| Conducted immunity | EN 61000-4-6 Level 3 | 1 day |
| Magnetic field | EN 61000-4-8 Level 4 | 0.5 day |
| Voltage dips | EN 61000-4-11 | 1 day |

**Acceptance criteria:**
- [ ] All emission tests pass Class B limits
- [ ] All immunity tests pass at specified levels (criterion A or B as applicable)
- [ ] Lab issues formal EMC test report
- [ ] If any test fails: immediate fix cycle (may add 2–4 weeks)

---

#### EP-08-003: Formal Safety Testing (IEC 62368-1 / IEC 61851-23 / UL 2202)
| Field | Value |
|-------|-------|
| **Assignee** | QA (monitor), lab (execute) |
| **Size** | XL (25 days — lab calendar time) |
| **Status** | Backlog |
| **Depends on** | EP-08-001, EP-07-005, EP-07-006, EP-07-007 |
| **Blocks** | EP-08-007 |

**Description:** Lab executes formal safety test program:

| Test | Standard | Criteria |
|------|----------|----------|
| Hipot (type-test levels) | IEC 62368-1 | 4000/3000/3750 VAC, 60 s |
| Insulation resistance | IEC 62368-1 | > 10 Mohm |
| Earth continuity | IEC 62368-1 | < 0.1 ohm at 25 A |
| Touch current | IEC 62368-1 | < 3.5 mA |
| Partial discharge | IEC 62368-1 | < 10 pC at 1.5× working V |
| Temperature rise | IEC 62368-1 | All components < rated limits |
| Abnormal operation | IEC 62368-1 | Single fault safety |
| Ground fault protection | IEC 61851-23, IEC 62955 | DC RCM, 6 mA threshold |
| Short circuit | UL 2202 | Safe shutdown, no fire |
| Overload | UL 2202 | Protection operates correctly |

**Acceptance criteria:**
- [ ] All safety tests pass
- [ ] Lab issues formal safety test report (CB scheme)
- [ ] UL certification mark authorized (or follow-up actions defined)
- [ ] If any test fails: root cause, fix, and re-test within 4 weeks

---

#### EP-08-004: Formal Surge and Transient Immunity Testing
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | M (5 days — part of lab test program) |
| **Status** | Backlog |
| **Depends on** | EP-08-001, EP-07-011, EP-07-012 |
| **Blocks** | EP-08-007 |

**Description:** Lab executes surge, ESD, and EFT/Burst at formal levels (may be higher than pre-compliance). Verify MOV degradation after repeated surges (measure clamping voltage before and after).

**Acceptance criteria:**
- [ ] All transient tests pass at formal levels
- [ ] MOV clamping voltage not degraded by > 5% after test series
- [ ] No component damage (visual inspection after testing)

---

#### EP-08-005: HALT Testing (500-Hour Burn-In)
| Field | Value |
|-------|-------|
| **Assignee** | QA, PE |
| **Size** | L (15 days active + 21 days continuous burn) |
| **Status** | Backlog |
| **Depends on** | EP-05-007 |
| **Blocks** | EP-08-008 |

**Description:** Run 2 Rev B units continuously at rated power (30 kW) for 500 hours. Include thermal cycling: −30°C to +55°C, 50 cycles during the 500 hours. Monitor: V_out, I_out, efficiency, temperatures, fault events. Log data every 10 s.

**Schedule:**
| Segment | Duration | Conditions |
|---------|----------|-----------|
| Initial characterization | 4 hours | 30 kW at 25°C, full data capture |
| Burn-in block 1 | 168 hours (1 week) | 30 kW at 45°C ambient |
| Thermal cycling | 100 hours | −30°C to +55°C, 2 hr/cycle, 50 cycles at 15 kW |
| Burn-in block 2 | 168 hours | 30 kW at 25°C ambient |
| Final block | 64 hours | 30 kW at 55°C (derated to ~20 kW at 55°C per curve) |
| Final characterization | 4 hours | 30 kW at 25°C, full data capture |

**Acceptance criteria:**
- [ ] 500 hours completed without interruption (except planned thermal cycles)
- [ ] Zero faults or shutdowns (excluding thermal derate at 55°C — expected)
- [ ] Efficiency degradation < 0.2% (initial vs. final characterization)
- [ ] No component temperature drift > 5°C from initial characterization
- [ ] Data log archived for reliability analysis

---

#### EP-08-006: Environmental Testing (Humidity, Vibration)
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-007 |
| **Blocks** | EP-08-008 |

**Description:** Environmental stress testing per product specification:

| Test | Condition | Duration | Pass Criteria |
|------|-----------|----------|--------------|
| Humidity | 40°C, 93% RH, non-condensing | 96 hours | Hipot pass after, no corrosion |
| Vibration (operational) | 5–500 Hz, 1g, 3 axes | 2 hours/axis | No mechanical failure, operational |
| Vibration (transport) | 5–500 Hz, 2g, 3 axes | 1 hour/axis | No mechanical failure |
| Shock | 15g, 11 ms, 3 axes, 3 pulses | — | No mechanical failure |

**Acceptance criteria:**
- [ ] All environmental tests pass
- [ ] Post-test functional verification passes (30 kW for 10 minutes)
- [ ] Visual inspection: no cracked solder, loose connectors, or displaced components

---

#### EP-08-007: Certification Report Review and Closure
| Field | Value |
|-------|-------|
| **Assignee** | QA, PM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-002, EP-08-003, EP-08-004 |
| **Blocks** | EP-09-001 |

**Description:** Review formal test reports from accredited lab. Address any non-conformances or observations. Obtain certification documents: CB test report, CB certificate, UL listing (or follow-up schedule).

**Acceptance criteria:**
- [ ] EMC test report received and filed
- [ ] Safety test report (CB scheme) received
- [ ] UL certification mark authorized (or timeline for listing confirmed)
- [ ] CE marking self-declaration prepared (based on CB + EMC reports)
- [ ] All non-conformances resolved or waived with justification

---

#### EP-08-008: Reliability Data Analysis
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-005, EP-08-006 |
| **Blocks** | EP-09-009 |

**Description:** Analyze HALT/burn-in and environmental test data. Calculate observed MTBF (target > 120,000 hours). Identify any degradation trends. Document reliability summary for product datasheet.

**Acceptance criteria:**
- [ ] Zero failures → MTBF estimate based on Chi-squared (90% confidence)
- [ ] Degradation trends documented (if any: efficiency, temperature)
- [ ] Reliability summary report created
- [ ] MTBF statement for product datasheet confirmed

---

#### EP-08-009: Fix and Re-Test Cycle (If Needed)
| Field | Value |
|-------|-------|
| **Assignee** | PE, PCB, FW |
| **Size** | L (15 days) — conditional |
| **Status** | Backlog |
| **Depends on** | EP-08-002, EP-08-003 |
| **Blocks** | EP-08-007 |

**Description:** If formal testing reveals failures: implement fix (hardware rework, firmware update, or component change), re-test at lab. Budget for 1–2 re-test cycles.

**Acceptance criteria:**
- [ ] Root cause documented for each failure
- [ ] Fix verified with pre-compliance re-test before sending back to lab
- [ ] Re-test passes at formal levels

---

#### EP-08-010: Update Design Documents with Certification Data
| Field | Value |
|-------|-------|
| **Assignee** | QA |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-007 |
| **Blocks** | — |

**Description:** Update [[09-Protection and Safety]] with formal test results. Add certification numbers, test report references, and compliance statement. Update product specification with certified ratings.

**Acceptance criteria:**
- [ ] Certification numbers added to documentation
- [ ] Compliance matrix updated with "Tested" and "Certified" columns
- [ ] Product spec sheet updated with certified voltage/current/power ratings

---

#### EP-08-011: Certification Mark Application
| Field | Value |
|-------|-------|
| **Assignee** | QA, PM |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-08-007 |
| **Blocks** | EP-09-008 |

**Description:** Apply for certification marks: CE (self-declaration based on CB + EMC), UL listing (through lab), and any regional marks required for target markets.

**Acceptance criteria:**
- [ ] CE Declaration of Conformity signed
- [ ] UL listing file opened (or listing confirmed)
- [ ] Certification marks approved for product labeling

---

## References

- [[09-Protection and Safety]] — Compliance matrix, hipot requirements, protection specifications
- [[05-EMI Filter Design]] — EMI filter design supporting emissions compliance
- [[12-Project-Management/01-Budget Estimate|Budget Estimate]] — Certification budget allocation

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 11 stories |
