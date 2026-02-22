---
tags: [PDU, project-management, epics, stories, planning]
created: 2026-02-22
---

# 12 – Project Management: Epics and Stories

This folder contains the complete work breakdown for the 30 kW PDU development programme, organized as **9 epics** aligned with the development phases. Each epic contains user stories spanning all disciplines. Supporting documents include the [[12-Project-Management/01-Budget Estimate|Budget Estimate]], [[12-Project-Management/02-Risk Register|Risk Register]], and [[12-Project-Management/03-Commissioning Procedure|Commissioning Procedure]].

---

## 1. Resource Roles

| Abbreviation | Role | Responsibility |
|-------------|------|----------------|
| **PE** | Power Electronics Engineer | Topology, magnetics, gate drive, control loop design |
| **PCB** | PCB Layout Engineer | Schematic capture, multi-board layout, DFM |
| **FW** | Firmware Engineer | STM32G474 embedded C, HRTIM, ADC, control algorithms |
| **FW-COM** | Firmware Engineer (Comms) | CAN protocol, OCPP/ISO 15118 integration |
| **ME** | Mechanical Engineer | Enclosure, heatsink, fans, bus bars, assembly |
| **TH** | Thermal Engineer | CFD simulation, thermal characterization, derating |
| **QA** | Quality / Compliance Engineer | EMC pre-compliance, safety testing, certification |
| **PM** | Programme Manager | Scheduling, procurement, vendor management, risk |
| **PROC** | Procurement Specialist | Component sourcing, vendor qualification, cost reduction |

> [!note] Team sizing
> Baseline team: 2 PE, 1 PCB, 2 FW (one control, one comms), 1 ME/TH (dual-hat), 1 QA, 1 PM/PROC (dual-hat). Total: 8 headcount.

---

## 2. Epic Overview

| Epic | Name | Phase | Duration | Lead | Key Deliverable |
|------|------|-------|----------|------|-----------------|
| [[12-Project-Management/Epics/EP-01 Design Review and Procurement|EP-01 Design Review and Procurement]] | Design Review & Procurement | 0 | 6 weeks | PM | Long-lead orders placed, design sign-off |
| [[12-Project-Management/Epics/EP-02 Rev A Prototype Build|EP-02 Rev A Prototype Build]] | Rev A Prototype Build | 1 | 8 weeks | PE | 5 assembled units, MCU boots |
| [[12-Project-Management/Epics/EP-03 Firmware Bring-Up|EP-03 Firmware Bring-Up]] | Firmware Bring-Up | 2 | 7 weeks | FW | Open-loop PFC + LLC verified on HW |
| [[12-Project-Management/Epics/EP-04 System Integration|EP-04 System Integration]] | System Integration | 3 | 8 weeks | PE | 30 kW achieved, efficiency >95% |
| [[12-Project-Management/Epics/EP-05 Rev B Prototype|EP-05 Rev B Prototype]] | Rev B Prototype | 4 | 8 weeks | PCB | 10 units built, Rev A issues resolved |
| [[12-Project-Management/Epics/EP-06 Firmware Maturation|EP-06 Firmware Maturation]] | Firmware Maturation | 5 | 10 weeks | FW-COM | CAN stacking, OCPP, ISO 15118 working |
| [[12-Project-Management/Epics/EP-07 Certification Prep|EP-07 Certification Prep]] | Certification Prep | 6 | 8 weeks | QA | Pre-compliance pass, test docs ready |
| [[12-Project-Management/Epics/EP-08 Pre-Production Validation|EP-08 Pre-Production Validation]] | Pre-Production Validation | 7 | 8 weeks | QA | Formal EMC + safety certs, HALT pass |
| [[12-Project-Management/Epics/EP-09 Production Release|EP-09 Production Release]] | Production Release | 8 | 6 weeks | PM | BOM frozen, manufacturing package |

**Total programme: 14–18 months** (phases overlap; see Gantt timeline below).

---

## 3. Gantt Timeline (Baseline)

The following month-by-month timeline shows the baseline schedule with 3 parallel tracks. Phases overlap where work streams are independent.

```
Month:     1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
          ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤

HW Track:
  Ph 0    ██████████████                                                        Design Review
  Ph 1              ████████████████████                                         Rev A Build
  Ph 3                                  ████████████████████                     Integration
  Ph 4                                                      ████████████████████ Rev B Build
  Ph 7                                                                          ████████████████  Pre-Prod

FW Track:
  Ph 2                    ██████████████████                                     FW Bring-Up
  Ph 3                                  ████████████████████                     Integration
  Ph 5                                            ██████████████████████████     FW Maturation

Cert Track:
  Ph 6                                                            ████████████████████  Cert Prep
  Ph 7                                                                          ████████████████  Validation
  Ph 8                                                                                    ██████████████  Release
```

### 3.1 Milestone Schedule

| ID | Milestone | Target Month | Phase | Go/No-Go |
|----|-----------|-------------|-------|----------|
| M1 | Schematic review complete | M1.5 | 0 | Design review board approval |
| M2 | Long-lead components received | M2.5 | 0 | All critical parts in stock |
| M3 | Rev A boards received & inspected | M4 | 1 | Visual + AOI inspection pass |
| M4 | First power-on (PFC stage) | M5 | 2 | Open-loop PFC verified on bench |
| M5 | First 30 kW achieved | M8 | 3 | Full power, closed-loop, efficiency >95% |
| M6 | Thermal characterization complete | M9 | 3 | All junctions within limits per [[04-Thermal Budget]] |
| M7 | Rev B boards received | M11 | 4 | All Rev A issues resolved in layout |
| M8 | 5-module CAN stacking verified | M12 | 5 | 150 kW, current imbalance <5% |
| M9 | EMC pre-compliance pass | M13 | 6 | Conducted + radiated within Class B limits |
| M10 | Safety pre-test pass | M14 | 6 | Hipot, insulation, earth leakage pass |
| M11 | Formal EMC certification | M16 | 7 | Accredited lab report issued |
| M12 | Safety certification (CB + UL) | M16 | 7 | CB scheme + UL 2202 certificates |
| M13 | HALT/burn-in complete | M17 | 7 | No failures in 500-hr burn-in |
| M14 | BOM freeze | M17 | 8 | Production BOM locked; alternates approved |
| M15 | Manufacturing package handoff | M18 | 8 | Gerbers, assembly docs, test procedures delivered |

---

## 4. Phase Gate Review Process

Each phase ends with a formal gate review. The review board (project lead + engineering lead + quality) evaluates:

1. **Deliverable completeness** — All phase deliverables submitted and reviewed
2. **Test results** — All required tests passed per the relevant epic stories
3. **Issue closure** — No open critical/high issues; medium issues have mitigation plans
4. **Risk assessment** — Updated [[12-Project-Management/02-Risk Register|Risk Register]]
5. **Budget status** — Actual spend vs. plan per [[12-Project-Management/01-Budget Estimate|Budget Estimate]]
6. **Schedule status** — Variance analysis; recovery plan if behind

### 4.1 Gate Decisions

| Decision | Meaning |
|----------|---------|
| **Go** | All criteria met; proceed to next phase |
| **Conditional Go** | Minor issues; proceed with action items (tracked, time-boxed) |
| **Hold** | Significant issues; repeat gate in 2 weeks after resolution |
| **No-Go** | Critical issues; return to prior phase or re-scope |

---

## 5. Story Tracking Conventions

### 5.1 Story ID Format

```
EP-XX-YYY
  │    │
  │    └── Story number within epic (001–999)
  └──────── Epic number (01–09)
```

### 5.2 Story Status

| Status | Meaning |
|--------|---------|
| `Backlog` | Defined but not started |
| `Ready` | All prerequisites met, can be picked up |
| `In Progress` | Actively being worked |
| `In Review` | Deliverable produced, awaiting peer review |
| `Done` | Accepted and verified |
| `Blocked` | Cannot proceed — blocker identified |

### 5.3 Story Size (T-Shirt)

| Size | Person-Days | Complexity |
|------|------------|-----------|
| **XS** | 0.5–1 | Trivial, single deliverable |
| **S** | 2–3 | Straightforward, minimal unknowns |
| **M** | 5–8 | Multi-step, some design decisions |
| **L** | 10–15 | Significant effort, cross-discipline |
| **XL** | 15–25 | Complex, high uncertainty, long lead |

---

## 6. Story Count Summary

| Epic | Stories | XS | S | M | L | XL | Total Effort (person-days) |
|------|---------|----|---|---|---|----|-----------------------------|
| EP-01 | 18 | 3 | 5 | 5 | 3 | 2 | ~110 |
| EP-02 | 14 | 2 | 4 | 4 | 3 | 1 | ~90 |
| EP-03 | 16 | 2 | 4 | 6 | 3 | 1 | ~105 |
| EP-04 | 15 | 1 | 3 | 5 | 4 | 2 | ~120 |
| EP-05 | 12 | 2 | 3 | 4 | 2 | 1 | ~75 |
| EP-06 | 14 | 1 | 3 | 5 | 4 | 1 | ~100 |
| EP-07 | 13 | 2 | 3 | 4 | 3 | 1 | ~85 |
| EP-08 | 11 | 1 | 3 | 3 | 3 | 1 | ~80 |
| EP-09 | 10 | 2 | 3 | 3 | 1 | 1 | ~60 |
| **Total** | **123** | **16** | **31** | **39** | **26** | **11** | **~825** |

---

## 7. Critical Path

The following story chains determine the minimum programme duration:

```
SiC MOSFET procurement (EP-01-004, 12–16 wk lead)
  → Rev A assembly (EP-02-003)
    → PFC open-loop bring-up (EP-03-004)
      → PFC closed-loop (EP-04-002)
        → Full 30 kW test (EP-04-006)
          → Rev B fixes (EP-05-002)
            → CAN 5-module stacking (EP-06-004)
              → Pre-compliance EMC (EP-07-003)
                → Formal EMC test (EP-08-002)
                  → BOM freeze (EP-09-001)
```

---

## 8. Sprint Breakdown

The programme uses **2-week sprints** (10 working days) to time-box work across all epics. Sprint capacity is 56 person-days (8 people × 10 days × 0.7 utilization). Sprints run sequentially from SP-01 to SP-27, with phase overlaps handled by assigning stories from multiple active epics to the same sprint.

See [[12-Project-Management/Sprints/__init|Sprints]] for the full sprint index, cadence definition, and ceremony schedule.

### 8.1 Sprint-to-Phase Summary

| Sprints | Phase | Epic(s) | Focus |
|---------|-------|---------|-------|
| SP-01 – SP-03 | 0 | EP-01 | Design review & procurement |
| SP-04 – SP-07 | 1 | EP-02 | Rev A prototype build |
| SP-07 – SP-10 | 2 | EP-03 | Firmware bring-up |
| SP-08 – SP-11 | 3 | EP-04 | System integration |
| SP-12 – SP-15 | 4 | EP-05 | Rev B prototype |
| SP-13 – SP-18 | 5 | EP-06 | Firmware maturation |
| SP-17 – SP-20 | 6 | EP-07 | Certification prep |
| SP-21 – SP-24 | 7 | EP-08 | Pre-production validation |
| SP-25 – SP-27 | 8 | EP-09 | Production release |

> [!tip] Phase overlaps
> Phases 2/3, 4/5, and 5/6 overlap because the HW, FW, and Cert tracks run in parallel. Each sprint file lists stories from all active epics in that time window.

---

## 9. Cross-References

| Document | Relevance |
|----------|-----------|
| [[12-Project-Management/Sprints/__init\|Sprints]] | 27 two-week sprints mapping stories to time-boxed iterations |
| [[__init]] | Project specifications and design document index |
| [[12-Project-Management/01-Budget Estimate|Budget Estimate]] | High-level and detailed budget, cash flow, cost tracking |
| [[12-Project-Management/02-Risk Register|Risk Register]] | 21 risks scored on 5×5 matrix with mitigations |
| [[12-Project-Management/03-Commissioning Procedure|Commissioning Procedure]] | 7-stage field deployment and handoff procedure |
| [[06-Firmware Architecture]] | Firmware scope definition |
| [[06-Firmware-Design/__init\|06-Firmware Design]] | Firmware implementation detail |
| [[07-BOM and Cost Analysis]] | BOM baseline for procurement stories |
| [[09-Protection and Safety]] | Compliance requirements for certification stories |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 9 epics, 123 stories |
