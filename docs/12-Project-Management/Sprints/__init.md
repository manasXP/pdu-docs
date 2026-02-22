---
tags: [PDU, project-management, sprints, agile]
created: 2026-02-22
---

# Sprints — 30 kW PDU Programme

This folder contains the sprint-level work breakdown for the 30 kW PDU development programme. Sprints map stories from the [[12-Project-Management/__init|9 epics]] into time-boxed 2-week iterations across 3 parallel work tracks: Hardware, Firmware, and Certification.

---

## 1. Sprint Cadence

| Parameter | Value |
|-----------|-------|
| Sprint duration | 2 weeks (10 working days) |
| Team size | 8 headcount |
| Utilization factor | 0.7 (meetings, admin, unplanned work) |
| Sprint capacity | 8 × 10 × 0.7 = **56 person-days** |
| Total sprints | 27 (SP-01 to SP-27) |
| Programme duration | ~54 weeks (~13.5 months active) |

---

## 2. Sprint Ceremonies

| Ceremony | When | Duration | Purpose |
|----------|------|----------|---------|
| Sprint Planning | Day 1, AM | 2 hours | Select stories, define sprint goals, assign owners |
| Daily Standup | Every day, AM | 15 min | Blockers, progress, coordination |
| Sprint Review | Day 10, AM | 1 hour | Demo completed work, stakeholder feedback |
| Retrospective | Day 10, PM | 1 hour | Process improvement, lessons learned |

---

## 3. Sprint-to-Phase Mapping

| Sprints | Phase | Epic(s) | Duration | Focus |
|---------|-------|---------|----------|-------|
| SP-01 to SP-03 | 0 | [[12-Project-Management/Epics/EP-01 Design Review and Procurement\|EP-01]] | 6 weeks | Design review & procurement |
| SP-04 to SP-07 | 1 | [[12-Project-Management/Epics/EP-02 Rev A Prototype Build\|EP-02]] | 8 weeks | Rev A prototype build |
| SP-07 to SP-10 | 2 | [[12-Project-Management/Epics/EP-03 Firmware Bring-Up\|EP-03]] | 7 weeks | Firmware bring-up (overlaps Ph 1) |
| SP-08 to SP-11 | 3 | [[12-Project-Management/Epics/EP-04 System Integration\|EP-04]] | 8 weeks | System integration |
| SP-12 to SP-15 | 4 | [[12-Project-Management/Epics/EP-05 Rev B Prototype\|EP-05]] | 8 weeks | Rev B prototype |
| SP-13 to SP-18 | 5 | [[12-Project-Management/Epics/EP-06 Firmware Maturation\|EP-06]] | 10 weeks | Firmware maturation (overlaps Ph 4) |
| SP-17 to SP-20 | 6 | [[12-Project-Management/Epics/EP-07 Certification Prep\|EP-07]] | 8 weeks | Certification prep |
| SP-21 to SP-24 | 7 | [[12-Project-Management/Epics/EP-08 Pre-Production Validation\|EP-08]] | 8 weeks | Pre-production validation |
| SP-25 to SP-27 | 8 | [[12-Project-Management/Epics/EP-09 Production Release\|EP-09]] | 6 weeks | Production release |

> [!note] Phase overlaps
> Sprint numbers overlap between phases because the 3 work tracks (HW, FW, Cert) run in parallel. Each sprint file lists stories from ALL active epics in that time window.

---

## 4. Burndown Tracking

Each sprint tracks:
- **Committed person-days** vs. **capacity** (56 pd)
- **Stories completed** vs. **stories committed**
- **Velocity** — rolling 3-sprint average of completed person-days

Burndown is updated at each daily standup. Sprint review notes capture actuals vs. plan.

---

## 5. Sprint Index

### Phase 0 — Design Review & Procurement (EP-01)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-01\|SP-01]] | Design Reviews & Long-Lead Procurement | 38 pd | M1 |
| [[12-Project-Management/Sprints/SP-02\|SP-02]] | Procurement Completion & PCB Finalization | 36 pd | M2 |
| [[12-Project-Management/Sprints/SP-03\|SP-03]] | Manufacturing Outputs & Firmware Prep | 36 pd | — |

### Phase 1 — Rev A Prototype Build (EP-02)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-04\|SP-04]] | Board Receipt & SMT Assembly | 24 pd | M3 |
| [[12-Project-Management/Sprints/SP-05\|SP-05]] | Power Device Assembly & Mechanical Integration | 24 pd | — |
| [[12-Project-Management/Sprints/SP-06\|SP-06]] | Board-Level Verification & Gate Driver Test | 22 pd | — |
| [[12-Project-Management/Sprints/SP-07\|SP-07]] | Documentation, Resonant Tank & FW Peripheral Init | 20 pd | — |

### Phase 2/3 — Firmware Bring-Up & System Integration (EP-03 + EP-04)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-08\|SP-08]] | PFC & LLC Open-Loop Bring-Up | 28 pd | M4 |
| [[12-Project-Management/Sprints/SP-09\|SP-09]] | Protection, ADC Pipeline & Control Foundations | 30 pd | — |
| [[12-Project-Management/Sprints/SP-10\|SP-10]] | CAN Protocol, Burst Mode & Closed-Loop PFC | 26 pd | — |
| [[12-Project-Management/Sprints/SP-11\|SP-11]] | LLC Closed-Loop, Full 30 kW & Thermal | 32 pd | M5, M6 |

### Phase 3 contd. — Integration Wrap-Up (EP-04)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-12\|SP-12]] | Efficiency Optimization, CFD & Issue Consolidation | 30 pd | — |

### Phase 4/5 — Rev B & Firmware Maturation (EP-05 + EP-06)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-13\|SP-13]] | Rev B Design & Layout Update | 26 pd | — |
| [[12-Project-Management/Sprints/SP-14\|SP-14]] | Rev B PCB Order & 5-Module Test Bench | 20 pd | M7 |
| [[12-Project-Management/Sprints/SP-15\|SP-15]] | Rev B Verification & CAN Stacking | 33 pd | M8 |
| [[12-Project-Management/Sprints/SP-16\|SP-16]] | Rev B Acceptance & Fault Redistribution | 33 pd | — |

### Phase 5/6 — FW Maturation & Cert Prep (EP-06 + EP-07)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-17\|SP-17]] | OCPP Interface, Burst Mode & EMC Test Plan | 36 pd | — |
| [[12-Project-Management/Sprints/SP-18\|SP-18]] | FW Code Review, RC Tag & EMC Pre-Compliance | 34 pd | M9 |

### Phase 6 — Certification Prep (EP-07)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-19\|SP-19]] | Safety Pre-Test & Cert Documentation | 20 pd | M10 |
| [[12-Project-Management/Sprints/SP-20\|SP-20]] | Compliance Fixes & Lab Engagement | 16 pd | — |

### Phase 7 — Pre-Production Validation (EP-08)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-21\|SP-21]] | Formal EMC & Safety Testing Start | 22 pd | — |
| [[12-Project-Management/Sprints/SP-22\|SP-22]] | HALT/Burn-In & Environmental Testing | 22 pd | M11, M12 |
| [[12-Project-Management/Sprints/SP-23\|SP-23]] | Certification Closure & Fix Cycles | 20 pd | M13 |
| [[12-Project-Management/Sprints/SP-24\|SP-24]] | Reliability Analysis & Design Doc Updates | 16 pd | — |

### Phase 8 — Production Release (EP-09)

| Sprint | Name | Committed | Milestone(s) |
|--------|------|-----------|-------------|
| [[12-Project-Management/Sprints/SP-25\|SP-25]] | BOM Freeze & Manufacturing Docs | 22 pd | M14 |
| [[12-Project-Management/Sprints/SP-26\|SP-26]] | Pilot Production Run | 20 pd | — |
| [[12-Project-Management/Sprints/SP-27\|SP-27]] | Acceptance Test & Production Release | 18 pd | M15 |

---

## 6. Cross-References

| Document | Relevance |
|----------|-----------|
| [[12-Project-Management/__init\|Project Management]] | Epics, milestones, phase gates |
| [[12-Project-Management/01-Budget Estimate\|Budget Estimate]] | Sprint-level spend tracking |
| [[12-Project-Management/02-Risk Register\|Risk Register]] | Risk review at sprint retrospectives |
| [[12-Project-Management/03-Commissioning Procedure\|Commissioning Procedure]] | Field deployment after production release |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 27 sprints across 9 epics |
