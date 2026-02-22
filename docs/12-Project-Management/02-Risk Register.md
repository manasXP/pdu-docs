---
tags: [PDU, project-management, risk, management]
created: 2026-02-22
aliases: [Risk Register, 05-Risk Register]
---

# Risk Register

This document identifies and tracks risks for the 30 kW PDU development programme, categorized by type with likelihood, impact, and mitigation strategies.

> [!note] See [[09-Protection and Safety]] for safety-related design mitigations. Phase references align with the epics in [[12-Project-Management/__init|Project Management]].

## Risk Matrix

Risks are scored on a 5×5 matrix:

| | Impact 1 (Negligible) | Impact 2 (Minor) | Impact 3 (Moderate) | Impact 4 (Major) | Impact 5 (Critical) |
|---|---|---|---|---|---|
| **Likelihood 5 (Almost Certain)** | 5 | 10 | 15 | 20 | 25 |
| **Likelihood 4 (Likely)** | 4 | 8 | 12 | 16 | 20 |
| **Likelihood 3 (Possible)** | 3 | 6 | 9 | 12 | 15 |
| **Likelihood 2 (Unlikely)** | 2 | 4 | 6 | 8 | 10 |
| **Likelihood 1 (Rare)** | 1 | 2 | 3 | 4 | 5 |

### Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 15–25 | **Critical** | Immediate mitigation required; escalate to project lead |
| 10–14 | **High** | Mitigation plan required; review weekly |
| 5–9 | **Medium** | Monitor; mitigation plan recommended |
| 1–4 | **Low** | Accept; review monthly |

---

## Technical Risks

### T1: LLC ZVS Loss at Light Load

| Field | Value |
|-------|-------|
| **Description** | LLC converter may lose ZVS (Zero Voltage Switching) below 10–15% load, causing hard switching, increased losses, and EMI |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — reduced efficiency and increased EMI at light load |
| **Score** | **9 (Medium)** |
| **Phase** | 3 (Integration) |
| **Mitigation** | Burst mode at very light load; verify gain curve per [[03-LLC Gain Curve Verification]]; optimize magnetizing inductance (Lm) for wide ZVS range |
| **Owner** | PE Lead |

### T2: PFC THD Exceeds 5% Limit

| Field | Value |
|-------|-------|
| **Description** | Vienna rectifier THDi may exceed IEC 61000-3-2 Class A limits at partial load, especially with unbalanced input |
| **Likelihood** | 2 (Unlikely) |
| **Impact** | 4 (Major) — certification failure |
| **Score** | **8 (Medium)** |
| **Phase** | 3, 6 |
| **Mitigation** | dq-frame control with feedforward per [[06-Firmware Architecture]]; tune current loop bandwidth; verify at 25% load points |
| **Owner** | FW Engineer |

### T3: Thermal Runaway or Hotspot

| Field | Value |
|-------|-------|
| **Description** | Junction temperatures exceed limits under worst-case conditions (55°C ambient, 30 kW, reduced airflow) |
| **Likelihood** | 3 (Possible) |
| **Impact** | 4 (Major) — field failure or forced derating below spec |
| **Score** | **12 (High)** |
| **Phase** | 3, 7 |
| **Mitigation** | Conservative thermal design per [[04-Thermal Budget]]; multiple NTC sensors; firmware thermal derating curve; HALT testing to find margin |
| **Owner** | PE Lead |

### T4: Gate Driver Noise Causing False Triggering

| Field | Value |
|-------|-------|
| **Description** | High dV/dt (50+ V/ns with SiC) causes common-mode noise coupling into gate driver, causing shoot-through |
| **Likelihood** | 3 (Possible) |
| **Impact** | 5 (Critical) — immediate device destruction |
| **Score** | **15 (Critical)** |
| **Phase** | 1, 2 |
| **Mitigation** | Select gate drivers with CMTI >200 V/ns; negative turn-off bias (−5 V); Kelvin source connection; tight gate loop per [[07-PCB-Layout/__init|07-PCB Layout]]; verify with fast dV/dt on bench |
| **Owner** | PE Lead |

### T5: Resonant Component Tolerance Shifting Gain Curve

| Field | Value |
|-------|-------|
| **Description** | Lr, Lm, Cr tolerance stackup (±10–15%) shifts LLC gain curve, narrowing operating range |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — may not cover full 150–1000 V output range |
| **Score** | **9 (Medium)** |
| **Phase** | 1, 3 |
| **Mitigation** | Specify tight tolerances on Cr (±5%); characterize actual Lr/Lm on received transformers; Monte Carlo analysis per [[03-LLC Gain Curve Verification]]; design with margin |
| **Owner** | PE Lead |

### T6: Firmware Control Loop Instability

| Field | Value |
|-------|-------|
| **Description** | PFC voltage loop or LLC frequency loop becomes unstable at certain operating points (e.g., mode transitions, load steps) |
| **Likelihood** | 2 (Unlikely) |
| **Impact** | 4 (Major) — OVP/OCP trip, potential hardware damage |
| **Score** | **8 (Medium)** |
| **Phase** | 3, 5 |
| **Mitigation** | Model-based loop design with adequate phase margin (>45°); extensive transient testing across operating envelope; anti-windup on integrators; slew rate limits |
| **Owner** | FW Engineer |

### T7: CAN Bus Current Sharing Instability

| Field | Value |
|-------|-------|
| **Description** | 5-module parallel operation shows oscillating current distribution or one module consistently overloaded |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — thermal stress on overloaded module |
| **Score** | **9 (Medium)** |
| **Phase** | 5 |
| **Mitigation** | Droop sharing with CAN-based trim; test with intentionally mismatched modules; configurable droop gain; monitor imbalance threshold and alarm |
| **Owner** | FW Engineer |

---

## Supply Chain Risks

### S1: SiC MOSFET Long Lead Time

| Field | Value |
|-------|-------|
| **Description** | SiC MOSFETs (Wolfspeed, Infineon, onsemi) have lead times of 16–30+ weeks; risk of allocation during shortage |
| **Likelihood** | 4 (Likely) |
| **Impact** | 4 (Major) — schedule slip of 2–4 months |
| **Score** | **16 (Critical)** |
| **Phase** | 0, 4 |
| **Mitigation** | Order early in Phase 0; qualify 2 alternate sources per [[07-BOM and Cost Analysis]]; maintain safety stock for Rev B; consider broker market for prototype qty |
| **Owner** | Project Manager |

### S2: Custom Magnetics Vendor Delay

| Field | Value |
|-------|-------|
| **Description** | Custom-wound LLC transformer and PFC inductor depend on specialist magnetics vendor with limited capacity |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — 2–4 week schedule slip |
| **Score** | **9 (Medium)** |
| **Phase** | 0–1 |
| **Mitigation** | Engage vendor in Phase 0; provide final specs early; qualify backup vendor; consider hand-winding prototypes in-house for Phase 1 |
| **Owner** | PE Lead |

### S3: Single-Source Component

| Field | Value |
|-------|-------|
| **Description** | Key components (specific gate driver, CAN transceiver, current sensor) may be single-source with no drop-in alternative |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — re-design if component becomes unavailable |
| **Score** | **9 (Medium)** |
| **Phase** | 0, 4, 8 |
| **Mitigation** | BOM review with alternates column per [[07-BOM and Cost Analysis]]; footprint-compatible alternates where possible; qualification testing of alternates during Phase 4 |
| **Owner** | PE Lead |

### S4: Connector or Enclosure Vendor EOL

| Field | Value |
|-------|-------|
| **Description** | Mechanical components (connectors, enclosure hardware) may go EOL between prototype and production |
| **Likelihood** | 2 (Unlikely) |
| **Impact** | 2 (Minor) — re-source with minimal design change |
| **Score** | **4 (Low)** |
| **Phase** | 8 |
| **Mitigation** | Select components from established product lines; verify lifecycle status at BOM freeze |
| **Owner** | Mech Engineer |

---

## Schedule Risks

### SC1: PCB Fabrication Delay

| Field | Value |
|-------|-------|
| **Description** | PCB fabrication (6-layer, 2 oz Cu) takes longer than quoted due to fab capacity or quality issues |
| **Likelihood** | 3 (Possible) |
| **Impact** | 2 (Minor) — 1–2 week slip |
| **Score** | **6 (Medium)** |
| **Phase** | 1, 4 |
| **Mitigation** | Use established fab with track record; order 2–3 spares; consider expedite option; have backup fab identified |
| **Owner** | PCB Designer |

### SC2: Integration Debug Overrun

| Field | Value |
|-------|-------|
| **Description** | System integration (Phase 3) reveals unexpected issues requiring extensive debug, exceeding 8-week allocation |
| **Likelihood** | 4 (Likely) |
| **Impact** | 3 (Moderate) — 2–4 week schedule extension |
| **Score** | **12 (High)** |
| **Phase** | 3 |
| **Mitigation** | Phase 3 has 2-week buffer built into 8-week estimate; prioritize critical path items; daily debug standups; pre-validate sub-systems thoroughly in Phase 2 |
| **Owner** | PE Lead |

### SC3: EMC Test Failure Requiring Re-Design

| Field | Value |
|-------|-------|
| **Description** | Formal EMC test fails (conducted or radiated emissions), requiring filter re-design and re-test |
| **Likelihood** | 3 (Possible) |
| **Impact** | 4 (Major) — 4–8 week delay + $5,000–15,000 re-test cost |
| **Score** | **12 (High)** |
| **Phase** | 6, 7 |
| **Mitigation** | Thorough pre-compliance testing in Phase 6 with 6 dB margin target; iterative [[05-EMI Filter Design|EMI filter]] tuning before formal test; budget for one re-test; select lab with quick turnaround |
| **Owner** | EMC Specialist |

### SC4: Safety Certification Extended Review

| Field | Value |
|-------|-------|
| **Description** | Safety certification body raises additional questions or requires design modifications, extending 8-week timeline |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — 4–8 week delay |
| **Score** | **9 (Medium)** |
| **Phase** | 7 |
| **Mitigation** | Engage certification body early (Phase 6) for pre-review; ensure TCF is complete before submission; design for compliance from Phase 0 per [[09-Protection and Safety]] |
| **Owner** | PE Lead |

### SC5: Lab Scheduling Conflict

| Field | Value |
|-------|-------|
| **Description** | Accredited EMC or safety lab has no availability when needed, pushing formal test by 4–8 weeks |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — direct schedule delay |
| **Score** | **9 (Medium)** |
| **Phase** | 7 |
| **Mitigation** | Book lab slots 8–12 weeks in advance; maintain relationship with 2 accredited labs; flexible schedule to accommodate lab availability |
| **Owner** | Project Manager |

---

## Certification Risks

### C1: Emissions Above Class B at Switching Harmonics

| Field | Value |
|-------|-------|
| **Description** | Conducted emissions at PFC or LLC switching frequency harmonics (65 kHz, 100–300 kHz fundamental + harmonics) exceed Class B limits |
| **Likelihood** | 4 (Likely) |
| **Impact** | 3 (Moderate) — filter redesign needed |
| **Score** | **12 (High)** |
| **Phase** | 6 |
| **Mitigation** | Design EMI filter per [[05-EMI Filter Design]] with margin; CM choke + DM filter staged; near-field probing during integration to identify leakage paths; grounding optimization |
| **Owner** | EMC Specialist |

### C2: Safety Standard Revision During Project

| Field | Value |
|-------|-------|
| **Description** | IEC 62368-1 or IEC 61851-23 issues revised edition during project, changing requirements |
| **Likelihood** | 1 (Rare) |
| **Impact** | 4 (Major) — potential re-design for new requirements |
| **Score** | **4 (Low)** |
| **Phase** | 6–7 |
| **Mitigation** | Monitor IEC TC108 and TC69 publication schedules; design with margin beyond current edition requirements; confirm applicable edition with certification body at project start |
| **Owner** | PE Lead |

### C3: Surge Test Failure (IEC 61000-4-5)

| Field | Value |
|-------|-------|
| **Description** | Surge test at ±4 kV L-PE causes component damage or functional failure |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — requires surge protection re-design |
| **Score** | **9 (Medium)** |
| **Phase** | 6 |
| **Mitigation** | MOV + GDT coordination per [[05-EMI Filter Design]]; pre-test with surge generator in Phase 6; adequate creepage on input filter stage |
| **Owner** | PE Lead |

---

## Financial Risks

### F1: Test Equipment Budget Overrun

| Field | Value |
|-------|-------|
| **Description** | Test equipment costs exceed estimate due to price increases or additional equipment needs discovered during testing |
| **Likelihood** | 3 (Possible) |
| **Impact** | 2 (Minor) — budget overrun 10–20% in equipment category |
| **Score** | **6 (Medium)** |
| **Phase** | 3 |
| **Mitigation** | Get firm quotes before Phase 3; consider rental for non-critical items; 15% contingency in budget per [[12-Project-Management/01-Budget Estimate|Budget Estimate]] |
| **Owner** | Project Manager |

### F2: Certification Cost Overrun Due to Re-Testing

| Field | Value |
|-------|-------|
| **Description** | Multiple EMC or safety re-tests required, each adding $5,000–15,000 |
| **Likelihood** | 3 (Possible) |
| **Impact** | 3 (Moderate) — $15,000–30,000 overrun |
| **Score** | **9 (Medium)** |
| **Phase** | 7 |
| **Mitigation** | Thorough pre-compliance in Phase 6; budget for one re-test in baseline; fix root cause before re-submission |
| **Owner** | PE Lead |

---

## Risk Summary Dashboard

| ID | Risk | L | I | Score | Level | Status |
|----|------|---|---|-------|-------|--------|
| T4 | Gate driver noise / shoot-through | 3 | 5 | 15 | Critical | Open |
| S1 | SiC MOSFET lead time | 4 | 4 | 16 | Critical | Open |
| T3 | Thermal runaway / hotspot | 3 | 4 | 12 | High | Open |
| SC2 | Integration debug overrun | 4 | 3 | 12 | High | Open |
| SC3 | EMC test failure | 3 | 4 | 12 | High | Open |
| C1 | Emissions at switching harmonics | 4 | 3 | 12 | High | Open |
| T1 | LLC ZVS loss at light load | 3 | 3 | 9 | Medium | Open |
| T2 | PFC THD exceeds limit | 2 | 4 | 8 | Medium | Open |
| T5 | Resonant component tolerance | 3 | 3 | 9 | Medium | Open |
| T6 | Control loop instability | 2 | 4 | 8 | Medium | Open |
| T7 | CAN current sharing instability | 3 | 3 | 9 | Medium | Open |
| S2 | Magnetics vendor delay | 3 | 3 | 9 | Medium | Open |
| S3 | Single-source component | 3 | 3 | 9 | Medium | Open |
| SC1 | PCB fab delay | 3 | 2 | 6 | Medium | Open |
| SC4 | Safety cert extended review | 3 | 3 | 9 | Medium | Open |
| SC5 | Lab scheduling conflict | 3 | 3 | 9 | Medium | Open |
| C3 | Surge test failure | 3 | 3 | 9 | Medium | Open |
| F1 | Test equipment budget overrun | 3 | 2 | 6 | Medium | Open |
| F2 | Certification cost overrun | 3 | 3 | 9 | Medium | Open |
| S4 | Connector/enclosure vendor EOL | 2 | 2 | 4 | Low | Open |
| C2 | Safety standard revision | 1 | 4 | 4 | Low | Open |

**Summary:** 2 Critical, 4 High, 13 Medium, 2 Low — **21 total risks identified**

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 21 risks identified |
| 0.2 | 2026-02-22 | Manas Pradhan | Moved from 11-Project-Plan to 12-Project-Management |
