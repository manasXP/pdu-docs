---
tags: [pdu, project-plan, management]
created: 2026-02-22
aliases: [Project Plan, 11-Project Plan]
---

# 11 — Project Development Plan

This document provides the master project plan for the **30 kW PDU** development programme. It defines the phased development approach, key milestones, and phase gate criteria from design review through production release.

> [!tip] Navigation
> This is the index for the Project Plan section. See [[__init]] for the overall PDU specification.

## Sub-Documents

| # | Document | Purpose |
|---|----------|---------|
| 01 | [[01-Development Phases]] | 9-phase schedule with 3 parallel tracks (HW / FW / Cert) |
| 02 | [[02-Test Plan]] | Board-level through certification test procedures |
| 03 | [[03-Resource Plan]] | Team, equipment, facilities, external services |
| 04 | [[04-Budget Estimate]] | High-level summary + detailed line-item budget |
| 05 | [[05-Risk Register]] | Technical, supply chain, schedule, and certification risks |
| 06 | [[06-Commissioning Procedure]] | 7-stage field deployment and handoff procedure |

## Phase Summary

| Phase | Name | Duration | Key Deliverables | Gate Criteria |
|-------|------|----------|-----------------|---------------|
| 0 | Design Review & Procurement | 6 wk | Approved schematics, long-lead orders placed | Peer review sign-off; all critical components on order |
| 1 | Rev A Prototype Build | 8 wk | Populated PCBs, assembled mechanical unit | All 4 boards fabricated and inspected; enclosure complete |
| 2 | Firmware Bring-Up | 7 wk | BSP validated, open-loop PWM on bench | All peripherals functional; HRTIM/ADC verified |
| 3 | System Integration | 8 wk | Closed-loop PFC + LLC at 30 kW | Full power achieved; efficiency >95%; thermal OK |
| 4 | Rev B Prototype | 8 wk | Design-fixed boards, 10-unit build | All Rev A issues resolved; 10 units assembled |
| 5 | Firmware Maturation | 10 wk | CAN stacking, protection, OCPP, ISO 15118 | 5-module stacking demonstrated; all protocols passing |
| 6 | Certification Prep | 8 wk | Pre-scan pass, test documentation complete | EMC pre-compliance pass; safety pre-test pass |
| 7 | Pre-Production Validation | 8 wk | Formal EMC/safety certificates, HALT data | All certifications obtained; HALT/burn-in complete |
| 8 | Production Release | 6 wk | Frozen BOM, manufacturing package | Manufacturing docs reviewed; pilot run complete |

> [!note] Total programme duration is approximately **14–18 months** depending on overlap between phases. See the Gantt timeline below for the baseline schedule.

## Gantt Timeline (Baseline)

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

### Milestone Schedule

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

## Phase Gate Definitions

Each phase ends with a formal gate review. The review board (project lead + engineering lead + quality) evaluates the following:

### Gate Review Process

1. **Deliverable completeness** — All phase deliverables submitted and reviewed
2. **Test results** — All required tests passed per [[02-Test Plan]]
3. **Issue closure** — No open critical/high issues; medium issues have mitigation plans
4. **Risk assessment** — Updated risk register per [[05-Risk Register]]
5. **Budget status** — Actual spend vs. plan per [[04-Budget Estimate]]
6. **Schedule status** — Variance analysis; recovery plan if behind

### Gate Decisions

| Decision | Meaning |
|----------|---------|
| **Go** | All criteria met; proceed to next phase |
| **Conditional Go** | Minor issues; proceed with action items (tracked, time-boxed) |
| **Hold** | Significant issues; repeat gate in 2 weeks after resolution |
| **No-Go** | Critical issues; return to prior phase or re-scope |

## Cross-References

- [[__init]] — PDU specification (input/output, efficiency, stacking, standards)
- [[01-Topology Selection]] — Approved topology: Vienna PFC + 3-Phase Interleaved LLC
- [[06-Firmware Architecture]] — STM32G474RE firmware architecture
- [[07-BOM and Cost Analysis]] — Component costs feeding into budget
- [[07-PCB-Layout/__init|07-PCB Layout]] — Board design feeding into Rev A/B builds
- [[09-Protection and Safety]] — Protection design feeding into safety certification
- [[10-Mechanical Integration]] — Enclosure design feeding into prototype builds

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
