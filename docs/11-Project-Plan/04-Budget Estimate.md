---
tags: [pdu, project-plan, budget, cost]
created: 2026-02-22
---

# 04 — Budget Estimate

This document provides both a high-level budget summary and detailed line-item estimates for the 30 kW PDU development programme.

> [!note] Component costs reference [[07-BOM and Cost Analysis]]. Resource requirements reference [[03-Resource Plan]]. Mechanical costs reference [[10-Mechanical Integration]].

## High-Level Budget Summary

| Category | Estimated Cost (USD) | % of Total | Phases |
|----------|---------------------|-----------|--------|
| Design & Engineering Labor | $120,000–160,000 | 30–35% | 0–8 |
| Prototype Components (Rev A + Rev B) | $40,000–60,000 | 12–15% | 0–4 |
| PCB Fabrication & Assembly | $15,000–25,000 | 4–6% | 1, 4 |
| Mechanical Fabrication | $20,000–35,000 | 5–8% | 1, 4, 8 |
| Custom Magnetics | $8,000–15,000 | 2–4% | 0–1, 4 |
| Test Equipment (buy) | $80,000–130,000 | 20–28% | 1–3 |
| Test Equipment (rental) | $10,000–20,000 | 3–5% | 6–7 |
| EMC Certification (lab fees) | $15,000–30,000 | 4–7% | 7 |
| Safety Certification (lab + listing) | $20,000–40,000 | 5–9% | 7 |
| Production Tooling (NRE) | $10,000–20,000 | 3–5% | 8 |
| Contingency (15%) | $50,000–80,000 | 15% | — |
| **Total (excl. labor)** | **$270,000–455,000** | — | — |
| **Total (incl. labor)** | **$390,000–615,000** | — | — |

> [!warning] Labor costs are highly variable depending on geography and employment model (in-house vs. contract). The range above assumes a mix of senior and mid-level engineers in a developed-market cost base.

### Budget by Phase

| Phase | Duration | Labor | Materials & Services | Total |
|-------|----------|-------|---------------------|-------|
| 0 — Design Review | 6 wk | $15,000–20,000 | $5,000–10,000 | $20,000–30,000 |
| 1 — Rev A Build | 8 wk | $18,000–24,000 | $30,000–45,000 | $48,000–69,000 |
| 2 — FW Bring-Up | 7 wk | $14,000–18,000 | $2,000–5,000 | $16,000–23,000 |
| 3 — Integration | 8 wk | $20,000–26,000 | $5,000–10,000 | $25,000–36,000 |
| 4 — Rev B Build | 8 wk | $18,000–24,000 | $40,000–60,000 | $58,000–84,000 |
| 5 — FW Maturation | 10 wk | $16,000–22,000 | $3,000–5,000 | $19,000–27,000 |
| 6 — Cert Prep | 8 wk | $14,000–18,000 | $15,000–25,000 | $29,000–43,000 |
| 7 — Pre-Prod | 8 wk | $12,000–16,000 | $45,000–80,000 | $57,000–96,000 |
| 8 — Release | 6 wk | $8,000–12,000 | $15,000–25,000 | $23,000–37,000 |
| **Contingency** | — | — | — | $50,000–80,000 |
| **Total** | ~18 mo | $135,000–180,000 | $210,000–345,000 | $390,000–615,000 |

---

## Detailed Line Items

### 1. Prototype Components — Rev A (5 units)

| Item | Qty | Unit Cost | Extended | Notes |
|------|-----|-----------|----------|-------|
| SiC MOSFET (C3M0065100K or equiv.) | 48 | $18–25 | $864–1,200 | 6 per PFC × 5 units + spares; see [[07-BOM and Cost Analysis]] |
| SiC MOSFET (LLC, C3M0025065D or equiv.) | 48 | $12–18 | $576–864 | 8 per LLC × 5 units + spares |
| Gate drivers (Si8271 / UCC21710 or equiv.) | 36 | $5–8 | $180–288 | Isolated, per switch |
| LLC transformer (custom wound) | 8 | $80–150 | $640–1,200 | 5 units + 3 spares |
| PFC inductor (custom wound) | 8 | $60–100 | $480–800 | 5 units + 3 spares |
| DC bus capacitors (electrolytic, 450 V) | 40 | $8–15 | $320–600 | Per module × 5 + spares |
| Resonant capacitor (film, C_r) | 20 | $3–6 | $60–120 | |
| Output filter capacitors (film) | 20 | $10–20 | $200–400 | |
| Current sensors (LEM or shunt + amp) | 20 | $8–15 | $160–300 | |
| STM32G474RE MCU | 8 | $8–12 | $64–96 | |
| CAN transceiver (TCAN4550 or equiv.) | 8 | $4–6 | $32–48 | |
| Isolated DC-DC (gate driver supply) | 36 | $6–10 | $216–360 | Per gate driver |
| Connectors (AC input, DC output, CAN, aux) | 5 sets | $30–50 | $150–250 | |
| Passives (resistors, caps, ferrites) | 5 sets | $50–80 | $250–400 | |
| Miscellaneous (fuses, relays, thermistors) | 5 sets | $30–50 | $150–250 | |
| **Rev A Components Subtotal** | | | **$4,340–7,176** | |
| **Spares / contingency (+20%)** | | | **$870–1,435** | |
| **Rev A Total** | | | **$5,210–8,610** | |

### 2. Prototype Components — Rev B (10 units)

| Item | Notes | Extended |
|------|-------|----------|
| Same BOM as Rev A, ×10 units + 20% spares | Updated components per Rev A findings | $10,400–17,200 |
| Additional components for design changes | Layout/schematic mods | $1,000–3,000 |
| **Rev B Total** | | **$11,400–20,200** |

### 3. PCB Fabrication

| Item | Qty | Unit Cost | Extended | Notes |
|------|-----|-----------|----------|-------|
| **Rev A — Power board** (6-layer, 2 oz, 200×150 mm) | 8 | $80–150 | $640–1,200 | 5 + 3 spares; prototype pricing |
| **Rev A — Control board** (4-layer, 1 oz, 100×80 mm) | 8 | $30–60 | $240–480 | |
| **Rev A — Gate driver boards** (4-layer, 100×60 mm) | 16 | $20–40 | $320–640 | 2 boards × 5 + spares |
| **Rev A — Auxiliary PSU board** (4-layer, 80×60 mm) | 8 | $20–35 | $160–280 | |
| Solder paste stencils (Rev A) | 4 | $50–80 | $200–320 | 1 per board type |
| **Rev B — Same board set** (10 units) | — | — | $2,500–5,000 | 10 units + spares, all 4 boards |
| Solder paste stencils (Rev B) | 4 | $50–80 | $200–320 | |
| **PCB Fabrication Total** | | | **$4,260–8,240** | |

### 4. PCB Assembly Services

| Item | Qty | Cost | Notes |
|------|-----|------|-------|
| Rev A hand assembly (in-house) | 5 units | $0 (labor) | Technician time included in labor |
| Rev A PCBA service (if outsourced) | 5 units | $3,000–5,000 | Setup + placement + reflow |
| Rev B PCBA service | 10 units | $5,000–10,000 | SMT + through-hole |
| **Assembly Total** | | **$5,000–10,000** | Assumes Rev A in-house, Rev B outsourced |

### 5. Mechanical Fabrication

| Item | Qty | Unit Cost | Extended | Notes |
|------|-----|-----------|----------|-------|
| Enclosure (sheet metal, laser cut + bend) — Rev A | 5 | $150–300 | $750–1,500 | Prototype, no powder coat |
| Enclosure — Rev B (powder coated) | 10 | $200–400 | $2,000–4,000 | |
| Heatsink extrusion — NRE (die) | 1 | $3,000–6,000 | $3,000–6,000 | One-time tooling |
| Heatsink extrusion — units | 15 | $40–80 | $600–1,200 | Rev A (5) + Rev B (10) |
| CNC machining (heatsink pocketing) | 15 | $30–60 | $450–900 | |
| Bus bars (copper, tin plated) | 15 sets | $20–40 | $300–600 | |
| Fan assemblies | 15 | $15–30 | $225–450 | |
| Thermal interface material | 15 sets | $5–10 | $75–150 | Pads + paste |
| Fasteners and hardware | 15 sets | $10–20 | $150–300 | |
| **Mechanical Total** | | | **$7,550–15,100** | |

### 6. Test Equipment

| Item | Buy Cost | Amortized/Project | Decision |
|------|----------|-------------------|----------|
| Programmable AC source (3-ph, 45 kVA) | $30,000–40,000 | $30,000–40,000 | Buy (ongoing use) |
| Electronic DC load (30 kW) | $18,000–25,000 | $18,000–25,000 | Buy |
| Power analyzer (Yokogawa WT5000 equiv.) | $25,000–35,000 | $25,000–35,000 | Buy |
| Oscilloscope (4-ch, 500 MHz) | $10,000–15,000 | $10,000–15,000 | Buy |
| HV differential probes (×4) | $6,000–12,000 | $6,000–12,000 | Buy |
| Current probes (×4) | $4,000–8,000 | $4,000–8,000 | Buy |
| Thermal camera | $4,000–8,000 | $4,000–8,000 | Buy |
| Hipot tester | $3,000–5,000 | $3,000–5,000 | Buy |
| Insulation resistance tester | $1,000–2,000 | $1,000–2,000 | Buy |
| Earth bond tester | $2,000–4,000 | $2,000–4,000 | Buy |
| Dev tools (debugger, CAN analyzer, etc.) | $1,000–3,000 | $1,000–3,000 | Buy |
| **Test Equipment (Buy) Total** | | **$104,000–170,000** | |

| Item | Rental Rate | Duration | Total |
|------|------------|----------|-------|
| EMC pre-compliance receiver + LISN | $3,000/mo | 2 months | $6,000 |
| Environmental chamber | $4,000/mo | 2 months | $8,000 |
| Vibration table | $3,000/mo | 1 month | $3,000 |
| **Test Equipment (Rental) Total** | | | **$10,000–17,000** |

### 7. Certification Costs

| Service | Cost | Duration | Notes |
|---------|------|----------|-------|
| **EMC Testing (Accredited Lab)** | | | |
| Full EMC test suite (emissions + immunity) | $10,000–20,000 | 2–3 weeks | EN 55032 + EN 61000-series |
| Re-test (if needed, emissions only) | $3,000–5,000 | 3–5 days | Common first time |
| CB test certificate (EMC) | $2,000–3,000 | 1–2 weeks | |
| **EMC Subtotal** | **$15,000–28,000** | | |
| **Safety Certification** | | | |
| IEC 62368-1 evaluation | $12,000–20,000 | 4–8 weeks | Full construction evaluation |
| UL 2202 listing (parallel) | $8,000–15,000 | 6–12 weeks | Concurrent with CB |
| CB test certificate (safety) | Included | | With IEC 62368-1 |
| Factory inspection (initial) | $2,000–3,000 | 1 day | Required for UL listing |
| Annual maintenance (UL listing) | $3,000–5,000/yr | Ongoing | First year included |
| **Safety Subtotal** | **$22,000–38,000** | | |
| **Certification Total** | **$37,000–66,000** | | |

### 8. Production Tooling & NRE

| Item | Cost | Notes |
|------|------|-------|
| Heatsink extrusion die | $3,000–6,000 | Already counted in mechanical (above) |
| Magnetics tooling (bobbin, winding fixture) | $2,000–4,000 | For automated winding |
| Production test fixture | $3,000–8,000 | Bed-of-nails or pogo-pin |
| Enclosure stamping die (if volume >500) | $5,000–10,000 | Only needed at volume |
| Label printing setup | $500–1,000 | |
| **Tooling NRE Total** | **$10,500–23,000** | Some overlap with mechanical section |

---

## Cash Flow Timeline

| Month | Cumulative Spend | Major Expenses |
|-------|-----------------|----------------|
| M1 | $15,000–25,000 | Long-lead component orders, PCB fab |
| M2 | $30,000–50,000 | PCBA service, mechanical fab, magnetics |
| M3 | $50,000–80,000 | Test equipment purchases begin |
| M4 | $80,000–130,000 | Remaining test equipment; Rev A assembly |
| M5 | $95,000–150,000 | Steady-state: lab consumables, debug parts |
| M6 | $100,000–160,000 | Steady-state |
| M7 | $105,000–170,000 | Steady-state |
| M8 | $110,000–180,000 | Steady-state |
| M9 | $130,000–210,000 | Rev B component orders |
| M10 | $150,000–250,000 | Rev B PCBA, mechanical fab |
| M11 | $165,000–275,000 | EMC equipment rental begins |
| M12 | $180,000–300,000 | Pre-compliance testing |
| M13 | $200,000–340,000 | EMC lab deposit; safety lab deposit |
| M14 | $230,000–390,000 | EMC + safety lab fees; environmental rental |
| M15 | $255,000–430,000 | Remaining certification fees |
| M16 | $270,000–455,000 | Tooling NRE; pilot production |
| M17 | $280,000–470,000 | Pilot production completion |
| M18 | $285,000–480,000 | Final documentation; handoff |

> [!note] Labor costs ($120,000–160,000) are distributed roughly evenly across 18 months and are not included in the above cash flow. Add ~$7,000–9,000/month for loaded labor cost.

---

## Cost Optimization Opportunities

| Opportunity | Savings Estimate | Trade-Off |
|-------------|-----------------|-----------|
| Hand-assemble Rev A in-house | $3,000–5,000 | Slower; requires skilled technician |
| Rent AC source instead of buying | $10,000–20,000 | Limited availability; scheduling risk |
| Share EMC chamber with another project | $5,000–10,000 | Scheduling dependency |
| Use CB scheme for international (skip UL initially) | $8,000–15,000 | Delays US market entry |
| Combine EMC and safety at same lab | $3,000–5,000 | Reduces shipping and coordination |
| Off-the-shelf heatsink (skip extrusion NRE) | $3,000–6,000 | May not optimize thermal performance |

---

## Budget Tracking

| Category | Budget (Mid-Range) | Actual | Variance | Notes |
|----------|-------------------|--------|----------|-------|
| Components (Rev A) | $6,900 | — | — | |
| Components (Rev B) | $15,800 | — | — | |
| PCB Fab & Assembly | $11,100 | — | — | |
| Mechanical | $11,300 | — | — | |
| Custom Magnetics | $3,500 | — | — | |
| Test Equipment (Buy) | $137,000 | — | — | |
| Test Equipment (Rent) | $13,500 | — | — | |
| Certification | $51,500 | — | — | |
| Tooling NRE | $16,750 | — | — | |
| Contingency (15%) | $40,000 | — | — | |
| **Total (excl. labor)** | **$307,350** | — | — | |
| Labor (18 mo) | $150,000 | — | — | |
| **Grand Total** | **$457,350** | — | — | |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
