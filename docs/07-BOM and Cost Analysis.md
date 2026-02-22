---
tags: [PDU, BOM, cost-analysis, procurement, SiC, EV-charging]
created: 2026-02-22
status: draft
---

# BOM and Cost Analysis — 30 kW PDU

> [!summary] Key Results
> Per-module BOM cost: **~$1,726 @qty 100** (production pilot), **~$1,383 @qty 500** (volume). Semiconductors (SiC + ICs) dominate at 35% of total. Five-module 150 kW system: ~$9,279 @100, ~$7,434 @500. Primary cost reduction levers: Chinese SiC alternates (-20-30%), nanocrystalline core sourcing (-40%), and resonant capacitor optimization (-50%).

## 1. Scope and Assumptions

This document consolidates every component specified across the six design documents ([[01-Topology Selection]], [[02-Magnetics Design]], [[03-LLC Gain Curve Verification]], [[04-Thermal Budget]], [[05-EMI Filter Design]], [[06-Firmware Architecture]]) into a single costed bill of materials.

| Assumption | Value |
|------------|-------|
| Pricing basis | Per-module (single 30 kW unit) |
| Quantity tiers | @100 modules (production pilot), @500 modules (volume) |
| Currency | USD, 2025-2026 distributor/contract pricing |
| Semiconductor sourcing | US/EU authorized distributors (Mouser, Digi-Key, Arrow) |
| Passive/mechanical sourcing | Mix of distributor and China-sourced mechanical |
| Excludes | Test fixtures, development tools, certification costs, NRE tooling (noted separately) |

## 2. Semiconductor BOM

### 2.1 Power Semiconductors

| Part Number | Function | Package | Qty | Unit @100 | Unit @500 | Extended @100 | Source Doc |
|-------------|----------|---------|-----|-----------|-----------|---------------|------------|
| SCTWA90N65G2V-4 | PFC SiC MOSFET, 650 V 22 mΩ | HiP247-4 | 6 | $24.00 | $20.00 | $144.00 | [[01-Topology Selection]] §3.3 |
| STPSC40H12C | PFC SiC Schottky diode, 1200 V 40 A | TO-247 LL | 12 | $11.00 | $9.00 | $132.00 | [[01-Topology Selection]] §3.3 |
| SCTW100N120G2AG | LLC primary SiC MOSFET, 1200 V 36 mΩ | HiP247 | 6 | $40.00 | $32.00 | $240.00 | [[01-Topology Selection]] §4.3, [[04-Thermal Budget]] §2.2 |
| STPSC20H065CW | LLC secondary SiC Schottky, 650 V 2×10 A | TO-247 | 9 | $6.50 | $5.00 | $58.50 | [[01-Topology Selection]] §4.3, [[04-Thermal Budget]] §2.2 |

**Power semiconductor subtotal: $574.50 @100, $462.00 @500**

> [!note] LLC secondary diode quantity
> 9 diodes: 3 per LLC phase (center-tapped secondary with 2 diodes + 1 spare position). Actual population depends on output voltage range requirement. At full output range (150–1000 V), all 9 positions populated.

### 2.2 Gate Drivers and ICs

| Part Number | Function | Package | Qty | Unit @100 | Unit @500 | Extended @100 | Source Doc |
|-------------|----------|---------|-----|-----------|-----------|---------------|------------|
| STGAP2SiC | Isolated gate driver, SiC-optimized | SO-8W | 6 | $3.00 | $2.60 | $18.00 | [[01-Topology Selection]] §5 |
| STM32G474RE | MCU, Cortex-M4F 170 MHz, HRTIM | LQFP-64 | 1 | $6.50 | $5.00 | $6.50 | [[06-Firmware Architecture]] §1 |
| SN65HVD230 | CAN 2.0 transceiver | SOIC-8 | 1 | $1.60 | $1.30 | $1.60 | [[06-Firmware Architecture]] §6.1 |

**IC subtotal: $26.10 @100, $21.30 @500**

### 2.3 Semiconductor Summary

| Category | @100 | @500 |
|----------|------|------|
| Power semiconductors | $574.50 | $462.00 |
| Gate drivers + ICs | $26.10 | $21.30 |
| **Semiconductor total** | **$600.60** | **$483.30** |

## 3. Magnetics BOM (×3 Phases)

All magnetics values from [[02-Magnetics Design]] §8.

### 3.1 Per-Phase Components

| Component | Part / Specification | Qty/Phase | Unit Cost @100 | Notes |
|-----------|---------------------|-----------|----------------|-------|
| Transformer core set | E65/32/27, 3C97 (Ferroxcube) | 1 set | $14.00 | Core pair + clamp |
| Transformer bobbin | B65/32 (Ferroxcube) with pin header | 1 | $3.00 | |
| Primary winding wire | Litz 44 AWG × 800 strands, 21 turns | ~8 m | $16.00 | ~$2.00/m |
| Secondary winding wire | Litz 44 AWG × 400 strands, 42 turns | ~12 m | $14.40 | ~$1.20/m |
| Kapton interlayer insulation | 0.05 mm × 25 mm, 3 layers | 1 set | $1.50 | 5 kV isolation class |
| Core clamp / mounting | Spring clip or adhesive bracket | 1 | $1.00 | |
| Resonant inductor core | Kool Mu 77439 toroid, µ=60 (Magnetics Inc.) | 1 | $7.50 | 33 µH discrete Lr |
| Resonant inductor winding | Litz 44 AWG × 400 strands, 24 turns | ~3 m | $3.60 | |
| Resonant capacitor | TDK CGA9N4C0G2J103J, 10 nF 630 V C0G 2220 | 24 | $24.00 | 8P × 3S = 26.7 nF, $1.00 each |

**Per-phase magnetics cost: ~$85.00 @100**

### 3.2 Magnetics Summary (3 Phases)

| Item | @100 | @500 | Notes |
|------|------|------|-------|
| Transformer assemblies (×3) | $148.80 | $126.00 | Core + bobbin + wire + insulation + clamp |
| Resonant inductors (×3) | $33.30 | $28.00 | Kool Mu toroid + winding |
| Resonant capacitors (72 total) | $72.00 | $58.00 | 24 per phase × 3 phases |
| **Magnetics total** | **$254.10** | **$212.00** |

> [!note] Volume pricing
> At qty 500, core sets drop ~15% via direct Ferroxcube/TDK order. Litz wire pricing improves ~10% on spool quantities (≥100 m). C0G MLCCs are stable at ~$0.80/pc in volume.

## 4. EMI Filter BOM

All components from [[05-EMI Filter Design]] §9.

| Component | Part / Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|---------------------|-----|-----------|---------------|-------|
| CM Choke 1 | VITROPERM W914, 3.3 mH, 60 A, 3-phase nanocrystalline | 1 | $60.00 | $60.00 | Dominant filter cost |
| CM Choke 2 | MnZn ferrite R42 stacked toroids, 1.0 mH, 60 A | 1 | $15.00 | $15.00 | TDK PC95 or 3E6 |
| X-capacitor (Cx1) | 2.2 µF, 310 VAC, X2 film (EPCOS B32924) | 3 | $2.50 | $7.50 | L-L delta |
| X-capacitor (Cx2) | 1.0 µF, 310 VAC, X2 film | 3 | $2.00 | $6.00 | L-L delta |
| Y-capacitor (Cy) | 10 nF, 250 VAC, Y2 ceramic disc | 6 | $0.50 | $3.00 | L-PE distributed |
| MOV (L-PE) | 680 VAC, EPCOS B72220S0681K101 | 3 | $3.00 | $9.00 | Surge, star to PE |
| MOV (L-L) | 680 VAC, 20 kA surge | 3 | $3.00 | $9.00 | Surge, delta |
| NTC thermistor | 10 Ω cold, 60 A rated | 3 | $2.00 | $6.00 | Inrush limiting; see [[08-Power-On Sequence and Inrush Management]] §3 for sizing |
| Bypass relay | 60 A, 600 VAC, normally open | 1 | $15.00 | $15.00 | Engages after soft-start; see [[08-Power-On Sequence and Inrush Management]] §3 for specs |
| Discharge resistors | 1 MΩ, 1 W, across each X-cap | 6 | $0.10 | $0.60 | IEC 60384-14 |
| **EMI filter total** | | | | **$131.10** | |

**EMI filter: $131.10 @100, $107.00 @500**

> [!tip] The VITROPERM nanocrystalline core at $60 is the single most expensive passive component. See §11 for Chinese alternates at $20–30.

## 5. DC Bus Capacitors

Split bus (700–920 VDC) requires high-voltage, high-ripple-current capacitors. From [[04-Thermal Budget]] §4.3 and [[01-Topology Selection]] §3.4.

| Component | Part / Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|---------------------|-----|-----------|---------------|-------|
| Electrolytic (main bus) | Nichicon UBY 450 V 470 µF 125°C | 4 | $12.00 | $48.00 | 2 per rail (series for 900 V) |
| Film (bus snubber) | EPCOS B32778 500 V 20 µF polypropylene | 2 | $15.00 | $30.00 | Ripple current handling |
| Bus midpoint balance | 2× 100 µF 450 V electrolytic 125°C | 2 | $6.00 | $12.00 | Neutral point balance |
| **DC bus total** | | | | **$90.00** | |

**DC bus capacitors: $90.00 @100, $72.00 @500** — see [[08-Power-On Sequence and Inrush Management]] §1.2 for capacitance analysis and stored energy calculations.

> [!warning] 125°C capacitor rating is mandatory
> Per [[04-Thermal Budget]] §4.3: PFC heatsink reaches 95°C at worst case. Standard 105°C electrolytics at 90°C give only 28,000 hours — far below the 120,000-hour MTBF target. 125°C-rated parts provide >113,000 hours.

## 6. Thermal and Mechanical BOM

From [[04-Thermal Budget]] §3.

### 6.1 Heatsinks

| Component | Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|--------------|-----|-----------|---------------|-------|
| PFC heatsink | Al 6063-T5 extrusion, 150 × 280 × 40 mm, 25 fins | 1 | $50.00 | $50.00 | 399 W load, Rth_sa = 0.10 °C/W |
| LLC heatsink | Al 6063-T5 extrusion, 280 × 280 × 40 mm, 45 fins | 1 | $75.00 | $75.00 | 497 W load, Rth_sa = 0.06 °C/W |

### 6.2 Thermal Interface Materials

| Component | Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|--------------|-----|-----------|---------------|-------|
| Thermal pads | Bergquist GP3000S, 0.25 mm, pre-cut | ~30 pcs | $0.80 | $24.00 | All power devices + drivers |
| Thermal grease | For heatsink-to-chassis (optional) | 1 tube | $2.00 | $2.00 | Amortized |

### 6.3 Fans and Sensors

| Component | Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|--------------|-----|-----------|---------------|-------|
| Axial fan | 92 × 92 × 25 mm, PWM, 24 V, ball bearing | 3 | $35.00 | $105.00 | ~65 CFM free air, <55 dB |
| NTC temperature sensor | 10 kΩ NTC + signal conditioning | 4 | $2.00 | $8.00 | PFC, LLC, magnetics, ambient |

### 6.4 Thermal Summary

| Category | @100 | @500 |
|----------|------|------|
| Heatsinks | $125.00 | $100.00 |
| Thermal pads + grease | $26.00 | $22.00 |
| Fans | $105.00 | $87.00 |
| NTC sensors | $8.00 | $6.00 |
| **Thermal total** | **$264.00** | **$215.00** |

## 7. PCB and Assembly

| Item | Specification | @100 | @500 | Notes |
|------|--------------|------|------|-------|
| Main power PCB (AC-DC + DC-DC) | 6-layer, 2 oz/4 oz mixed copper, ~300 × 450 mm, FR4 TG170 | $120.00 | $85.00 | Heavy copper for power loops |
| Power Entry PCB (PE-CONT-01) | 2-layer, 4 oz copper, 150 × 120 mm, FR4 TG170 | $18.00 | $14.00 | NTC, relay, contactor mounting; see [[07-PCB-Layout/Power-Entry/__init\|Power Entry Board]] |
| S4 signal harness | 8-pin Micro-Fit 3.0, ~150 mm, Controller → Power Entry | $3.00 | $2.50 | Relay/contactor coil drive + feedback |
| SMD assembly | Reflow + selective wave for through-hole | $45.00 | $35.00 | ~400 placements |
| Stencil (amortized) | Laser-cut stainless steel | $5.00 | $2.00 | NRE ~$500 amortized |
| Conformal coating | Selective spray, acrylic | $8.00 | $6.00 | IP20 environment |
| **PCB + assembly total** | | **$199.00** | **$144.50** | |

> [!note] Power Entry Board Cost Impact
> The Power Entry PCB ($18) and S4 harness ($3) add ~$21 per module at qty 100. NTC, relay, and contactor component costs are unchanged — they are simply relocated from the AC-DC board to the Power Entry board. The net benefit is improved serviceability and thermal isolation at minimal cost.

## 8. Enclosure and Mechanical

From [[__init]] physical specifications: 455 × 300 × 94 mm.

| Component | Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|--------------|-----|-----------|---------------|-------|
| Sheet metal enclosure | 1.5 mm steel, 455 × 300 × 94 mm, powder coat | 1 | $65.00 | $65.00 | Intake + exhaust mesh |
| AC input connector | 3P+N+PE, 60 A panel mount | 1 | $12.00 | $12.00 | |
| DC output connector | 2-pole, 100 A panel mount | 1 | $10.00 | $10.00 | |
| CAN connector | DB9 or M12 | 1 | $3.00 | $3.00 | |
| Signal connector | Auxiliary I/O, 10-pin | 1 | $2.00 | $2.00 | |
| Bus bars | Copper, tin-plated, DC bus + output | 1 set | $20.00 | $20.00 | |
| Hardware kit | Screws, standoffs, DIN clips, labels | 1 set | $10.00 | $10.00 | |
| **Enclosure + mechanical total** | | | | **$122.00** | |

**Enclosure + mechanical: $122.00 @100, $98.00 @500**

## 9. Auxiliary Power Supply and Sensors

| Component | Specification | Qty | Unit @100 | Extended @100 | Notes |
|-----------|--------------|-----|-----------|---------------|-------|
| Aux SMPS module | 12 V / 24 V, 30 W, enclosed | 1 | $15.00 | $15.00 | Fans, gate drivers, MCU |
| Current sensor (AC input) | LEM LTSR 25-NP or Allegro ACS770, Hall effect | 3 | $8.00 | $24.00 | PFC phase current sensing |
| Output current sensor | LEM HTFS 200-P or shunt + isolator | 1 | $10.00 | $10.00 | CC feedback for LLC |
| Miscellaneous passives | Decoupling caps, pull-ups, LEDs, crystal, etc. | 1 lot | $8.00 | $8.00 | |
| **Auxiliary total** | | | | **$57.00** | |

**Auxiliary: $57.00 @100, $45.00 @500**

## 10. Cost Summary

### 10.1 Per-Module Cost

| Category | @100 (USD) | @500 (USD) | % of Total (@100) |
|----------|------------|------------|-------------------|
| Semiconductors (SiC + ICs) | $600.60 | $483.30 | 35.2% |
| Magnetics (transformers + inductors + Cr) | $254.10 | $212.00 | 14.9% |
| EMI Filter | $131.10 | $107.00 | 7.7% |
| DC Bus Capacitors | $90.00 | $72.00 | 5.3% |
| Thermal + Fans | $264.00 | $215.00 | 15.5% |
| PCB + Assembly | $199.00 | $144.50 | 11.5% |
| Enclosure + Mechanical | $122.00 | $98.00 | 7.2% |
| Auxiliary + Sensors | $57.00 | $45.00 | 3.3% |
| Miscellaneous / margin (5%) | $8.00 | $6.00 | 0.5% |
| **Per-Module Total** | **$1,725.80** | **$1,382.80** | **100%** |

### 10.2 System-Level Cost (5-Module 150 kW Stack)

| Configuration | @100 | @500 |
|---------------|------|------|
| 5 × 30 kW modules | $8,629 | $6,914 |
| System CAN bus + wiring harness | ~$150 | ~$120 |
| System enclosure / rack | ~$500 | ~$400 |
| **150 kW system total** | **~$9,279** | **~$7,434** |

### 10.3 Cost Breakdown (Visual)

```
Semiconductors  ████████████████████████████████████  35%
Thermal + Fans  ████████████████                      16%
Magnetics       ███████████████                       15%
PCB + Assembly  ████████████                          12%
EMI Filter      ████████                               8%
Enclosure       ███████                                7%
DC Bus Caps     █████                                  5%
Auxiliary       ███                                    3%
Margin          █                                      1%
```

## 11. Cost Drivers and Optimization Opportunities

### 11.1 Top Cost Drivers

| Rank | Item | Extended @100 | % of BOM | Lever |
|------|------|---------------|----------|-------|
| 1 | SCTW100N120G2AG (LLC MOSFETs, 6×) | $240.00 | 14.1% | Chinese SiC alternates |
| 2 | SCTWA90N65G2V-4 (PFC MOSFETs, 6×) | $144.00 | 8.4% | Chinese SiC alternates |
| 3 | STPSC40H12C (PFC diodes, 12×) | $132.00 | 7.7% | Volume negotiation |
| 4 | PCB + assembly | $178.00 | 10.4% | Panel optimization |
| 5 | Fans (3 × 92 mm) | $105.00 | 6.2% | Chinese OEM fans |
| 6 | Heatsinks (PFC + LLC) | $125.00 | 7.3% | Custom extrusion tooling |
| 7 | C0G MLCC resonant caps (72 pcs) | $72.00 | 4.2% | Film cap alternative |
| 8 | VITROPERM nanocrystalline core | $60.00 | 3.5% | Chinese nanocrystalline |

### 11.2 Optimization Scenarios

| Optimization | Savings @100 | Savings @500 | Risk / Trade-off |
|-------------|-------------|-------------|------------------|
| Chinese SiC (BASiC Semi, SICC) for LLC MOSFETs | -$50 to -$70 | -$40 to -$55 | Qualification risk; no AEC-Q101 |
| Chinese SiC for PFC MOSFETs | -$30 to -$45 | -$25 to -$35 | Same qualification concern |
| Magnetec M-403-A vs. VITROPERM W914 | -$25 to -$35 | -$20 to -$28 | Equivalent performance, better availability |
| Film caps (WIMA FKP2) vs. C0G MLCC for Cr | -$30 to -$40 | -$25 to -$32 | Larger footprint, but higher ripple current capability |
| Chinese OEM fans (EBM-Papst equivalent) | -$25 to -$35 | -$20 to -$28 | Verify MTBF; qualification testing needed |
| Custom heatsink extrusion (NRE $2,500) | -$15/unit | -$30/unit | NRE amortizes to $25 @100, $5 @500 |
| **Total potential savings** | **-$175 to -$260** | **-$160 to -$208** | |
| **Optimized BOM** | **~$1,450–$1,530** | **~$1,160–$1,210** | |

### 11.3 Heatsink Tooling NRE

Custom extrusion die NRE is ~$2,500 one-time. Amortized per-unit cost:

| Qty | NRE per Unit | Extrusion Unit Cost | Total per Unit |
|-----|-------------|-------------------|---------------|
| 100 | $25.00 | $85.00 | $110.00 |
| 500 | $5.00 | $70.00 | $75.00 |
| 1000 | $2.50 | $65.00 | $67.50 |

At qty 100, custom tooling saves ~$15/unit vs. off-the-shelf extrusions. Breakeven at ~50 units.

## 12. Risk Items and Alternates

| Component | Risk | Alternate | Cost Impact | Status |
|-----------|------|-----------|-------------|--------|
| SCTW100N120G2AG | Lead time (12–16 wk), AEC-Q cost premium | C3M0030120K (Wolfspeed) | -15% per device | Validated in Wolfspeed CRD30DD12N-K |
| VITROPERM W914 | Single-source (Vacuumschmelze), opaque pricing | Magnetec M-403-A | -40% (-$25) | Equivalent µr, available ex-stock |
| TDK CGA9N4C0G2J103J (2220 C0G 630 V) | Specialty MLCC, allocation risk | WIMA FKP2 2.2 nF 630 V film | -50% (-$36) | Larger footprint; verify PCB space |
| Litz wire 44 AWG × 800 strands | Long lead specialty wire (8–12 wk) | 46 AWG × 1200 strands | Neutral | Equivalent cross-section, easier sourcing |
| Nichicon UBY 450 V 125°C | Supply chain (125°C grade is niche) | Nippon Chemi-con KMZ 450 V 125°C | Neutral | Pin-compatible, same life model |
| STPSC20H065CW (LLC diode) | Thermal bottleneck per [[04-Thermal Budget]] §4.2 | STPSC30H065CW (30 A, lower Vf) | +$3/pc (+$27 total) | Reduces Tj by ~15°C, worth the premium |

## 13. Procurement Notes

### 13.1 Long-Lead Items (Order First)

| Item | Typical Lead Time | Action |
|------|------------------|--------|
| SiC MOSFETs (SCTW100N120G2AG) | 12–16 weeks | Order immediately at prototype stage |
| Nanocrystalline CM choke core | 8–12 weeks | Request samples from Vacuumschmelze + Magnetec |
| Litz wire (800-strand, 44 AWG) | 8–12 weeks | Source from New England Wire or Rubadue |
| Custom heatsink extrusions | 6–8 weeks (with tooling) | Tooling NRE: ~$2,500 |
| E65/32/27 core sets (3C97) | 6–8 weeks | Ferroxcube or TDK equivalent (N97) |

### 13.2 Readily Available Items

- STM32G474RE, SN65HVD230, STGAP2SiC: stock at major distributors
- X/Y capacitors, MOVs, NTC thermistors: commodity parts, 2–4 week lead
- Sheet metal enclosure: 3–4 weeks from China fabricator
- Fans, connectors, hardware: stock items

## 14. Cross-Reference Verification

### 14.1 Semiconductor Quantity Check

| Device | Topology Requirement | BOM Qty | Match |
|--------|---------------------|---------|-------|
| PFC MOSFETs (650 V) | Vienna: 2 per phase × 3 phases | 6 | Yes |
| PFC Schottky diodes (1200 V) | Vienna: 4 per phase × 3 phases | 12 | Yes |
| LLC primary MOSFETs (1200 V) | Half-bridge: 2 per phase × 3 phases | 6 | Yes |
| LLC secondary diodes (650 V) | Rectifier: 3 per phase × 3 phases | 9 | Yes |
| Gate drivers | PFC (3 half-bridges) + LLC (3 half-bridges) | 6 | Yes |
| MCU | Single-controller architecture | 1 | Yes |
| CAN transceiver | Inter-module stacking bus | 1 | Yes |

### 14.2 Volume Discount Consistency

| Category | @100 | @500 | Discount | Expected Range |
|----------|------|------|----------|---------------|
| Semiconductors | $600.60 | $483.30 | 19.5% | 15–25% — Yes |
| Magnetics | $254.10 | $212.00 | 16.6% | 15–20% — Yes |
| EMI Filter | $131.10 | $107.00 | 18.4% | 15–25% — Yes |
| DC Bus Caps | $90.00 | $72.00 | 20.0% | 15–25% — Yes |
| Thermal | $264.00 | $215.00 | 18.6% | 15–25% — Yes |
| PCB + Assembly | $199.00 | $144.50 | 27.4% | 25–35% — Yes |
| Enclosure | $122.00 | $98.00 | 19.7% | 15–25% — Yes |
| Auxiliary | $57.00 | $45.00 | 21.1% | 15–25% — Yes |

All volume discounts fall within the expected 15–35% range for qty 100 → qty 500 scaling.

## 15. References

- [[01-Topology Selection]] — Architecture, semiconductor selection, design decisions
- [[02-Magnetics Design]] — Transformer, inductor, resonant capacitor specifications
- [[03-LLC Gain Curve Verification]] — LLC operating points validation
- [[04-Thermal Budget]] — Loss breakdown, heatsink sizing, component thermal data
- [[05-EMI Filter Design]] — EMI filter component selection and sizing
- [[06-Firmware Architecture]] — MCU, CAN transceiver, current sensors
- Mouser / Digi-Key — Distributor pricing reference (2025-2026)
- Ferroxcube E65/32/27 datasheet — Core pricing via authorized distributors
- Magnetics Inc. Kool Mu catalog — Powder core pricing
- Vacuumschmelze VITROPERM 500F — Nanocrystalline core pricing

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
