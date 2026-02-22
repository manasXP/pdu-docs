---
tags: [pdu, pcb-layout, aux-psu, safety, isolation, iec-62368, creepage, clearance, hipot]
created: 2026-02-22
status: draft
---

# 05 — Safety and Isolation

## Purpose

This document specifies the safety and isolation design for the Aux PSU board. The board bridges the most dangerous voltage boundary in the entire PDU: the 920 VDC bus (hazardous energy source) to all low-voltage secondary outputs that are accessible through connectors and harnesses. This makes the Aux PSU the **most safety-critical PCB** in the system — a single insulation failure here can expose operators or downstream boards to lethal voltage.

All isolation requirements are derived from **IEC 62368-1** (Audio/video, information and technology equipment — Safety requirements), which is the harmonized standard for IT/telecom power supplies and is accepted by UL (UL 62368-1) and CE (EN 62368-1).

## Applicable Safety Standards

| Standard | Scope | Key Requirements for Aux PSU |
|----------|-------|------------------------------|
| IEC 62368-1 (Ed. 3.0) | Equipment safety | Reinforced insulation between PS2 (920V DC bus) and PS1 (SELV outputs) |
| IEC 60664-1 | Insulation coordination | Creepage/clearance tables based on pollution degree and material group |
| IEC 61558-2-16 | Transformers for SMPS | Flyback transformer construction, hipot, creepage |
| UL 2202 | EV charging equipment | Additional requirements for EV DCFC safety |
| IEC 60112 | CTI testing | Material group classification for creepage calculation |

## Voltage Classification

### Primary Side

| Parameter | Value |
|-----------|-------|
| Working voltage | 920 VDC (continuous) |
| Transient voltage | 1200 V (bus overshoot during load transients) |
| Pollution degree | PD2 (normally non-conductive pollution; condensation expected) |
| Material group | IIIb (FR-4, CTI 100–174 V) |
| Overvoltage category | OVC II (equipment level) |
| Energy class | PS2 (hazardous energy: V > 60 VDC and available energy > 20 J from bus caps) |

### Secondary Side (All Outputs)

| Parameter | Value |
|-----------|-------|
| Working voltage | ≤18 VDC (highest secondary rail) |
| Classification | SELV (Safety Extra-Low Voltage) — PS1 |
| Accessible | Yes — through connectors P4 and P5 to other boards |

### Insulation Requirement

| Boundary | From | To | Insulation Type | Rationale |
|----------|------|----|----|-----------|
| Primary → any secondary | PS2 (920 V) | PS1 (SELV) | **Reinforced** | Single fault must not expose SELV to hazardous voltage |
| Gate drive A ↔ Gate drive B | PS1 | PS1 | Functional | Different isolated returns, max 50 V differential |
| Gate drive ↔ Logic | PS1 | PS1 | Functional | Different returns, max 18 V differential |

## Creepage and Clearance Requirements

### Primary to Secondary (Reinforced Insulation)

Creepage and clearance are calculated per IEC 62368-1, Table 28 and Table G.9:

**Input parameters:**
- Working voltage: 920 VDC
- Equivalent RMS: 920 V (DC = peak = RMS for creepage tables)
- Pollution degree: PD2
- Material group: IIIb (FR-4, CTI 100–174 V)
- Altitude: ≤2000 m (no altitude correction)
- Insulation type: Reinforced (2x basic)

**Creepage calculation:**

| Step | Value | Reference |
|------|-------|-----------|
| Basic creepage for 920 V, PD2, IIIb | 7.0 mm | IEC 62368-1 Table G.9, interpolated |
| Reinforced factor | 2.0x | IEC 62368-1 clause 5.4.2 |
| **Required creepage** | **14.0 mm** | Minimum across any primary-to-secondary path |

**Clearance calculation:**

| Step | Value | Reference |
|------|-------|-----------|
| Basic clearance for 920 V + transient (1200 V), PD2 | 4.0 mm | IEC 62368-1 Table 28 |
| Reinforced factor | 2.0x | IEC 62368-1 clause 5.4.2 |
| **Required clearance** | **8.0 mm** | Minimum through-air distance |

### Functional Isolation (Between Secondary Domains)

| Boundary | Working Voltage | Creepage | Clearance |
|----------|----------------|----------|-----------|
| Gate drive A ↔ Gate drive B | 50 V (max differential) | 1.6 mm | 0.5 mm |
| Gate drive ↔ Logic domain | 18 V | 1.6 mm | 0.5 mm |

> [!warning] Creepage Measurement Rules
> Creepage is measured along the **shortest path across any surface** between two conductors. This includes:
> - PCB surface (top, bottom, and internal layer edges exposed by slots)
> - Component body surfaces
> - Solder fillet surfaces
> - Conformal coating surfaces (coating reduces effective creepage by only ~1 mm credit per IEC 60664-5)
>
> When measuring creepage across the PCB slot, the path goes: primary copper edge → down the slot wall → across the slot bottom (if any) → up the opposite wall → to secondary copper edge. The 4 mm slot width contributes approximately 4 + 1.6 + 1.6 = 7.2 mm of path (slot width + two wall descents of ~0.8 mm each for 1.6 mm board).

## PCB Slot Specification

The primary isolation barrier is a **routed PCB slot** that spans the full board height (80 mm):

### Slot Geometry

| Parameter | Value | Notes |
|-----------|-------|-------|
| Slot width | 4.0 mm minimum (4.5 mm recommended) | Measured between nearest copper edges |
| Slot length | 80 mm (full board height) | End-to-end; slot terminates at board edges |
| Slot depth | Through all layers (1.6 mm) | Full board thickness |
| Slot wall finish | No copper, no solder mask on slot walls | Bare FR-4 substrate exposed |
| Copper setback from slot edge | 1.0 mm minimum on all layers | No copper within 1 mm of slot wall |
| Solder mask setback from slot | 0.5 mm minimum | Prevent mask bridging |

### Slot Location on Board

```
        ←——————————— 100 mm ———————————————→
   ┌────────────────╥════╥─────────────────────┐  ↑
   │                ║    ║                     │  │
   │  PRIMARY       ║SLOT║    SECONDARY        │ 80
   │  SIDE          ║4mm ║    SIDE             │  mm
   │  (~33 mm)      ║    ║    (~63 mm)         │  │
   │                ║    ║                     │  │
   └────────────────╨════╨─────────────────────┘  ↓
                    ↑    ↑
               33 mm    37 mm from left edge
```

### Components Crossing the Slot

Only two component types are permitted to physically bridge the PCB slot:

| Component | Requirement | Verification |
|-----------|-------------|-------------|
| Flyback transformer T1 | Safety-rated per IEC 61558-2-16; ≥14 mm creepage between primary and secondary winding terminals on bobbin | Transformer test report from manufacturer |
| Y1 safety capacitor | Y1 class per IEC 60384-14; rated for 500 VAC or equivalent DC | Component safety certification |
| Optocoupler (if wide-body) | Safety-rated package; ≥8 mm creepage between input and output pins | Component datasheet + safety file |

> [!tip] Slot Bridging Verification
> After layout, generate a DRC report with a custom rule that flags any copper, solder mask, or silkscreen crossing the defined slot zone (33–37 mm from left edge, all layers). Only the transformer pads, Y-capacitor pads, and optocoupler pads should appear as intentional violations.

## Conformal Coating

### Coating Specification

| Parameter | Value |
|-----------|-------|
| Coating type | Acrylic or polyurethane per IEC 61086-1 |
| Application | Both sides of PCB |
| Thickness | 25–75 um (per IPC-CC-830) |
| Coverage | All copper traces, solder joints, and component leads within 5 mm of the isolation barrier |
| Exclusion zones | Connector pins, test points, mounting holes, transformer core |

### Coating Benefits for Isolation

Conformal coating provides several safety benefits:

1. **Contamination resistance** — Prevents conductive dust or moisture films from bridging the isolation gap
2. **Partial discharge suppression** — Fills micro-gaps between solder mask and copper that can initiate partial discharge
3. **Creepage improvement** — IEC 60664-5 allows a limited creepage credit (~1 mm) for coated surfaces with CTI > 600 V
4. **Corrosion protection** — Prevents tin whisker growth and copper migration across the isolation gap

> [!warning] Conformal Coating is Not a Substitute for Creepage
> The conformal coating provides a secondary safety benefit but must NOT be relied upon as the primary insulation means. The 14 mm creepage and 8 mm clearance must be met on the **bare PCB** without coating. The coating is an additional layer of protection.

### Application Process

1. Clean the board thoroughly (IPA wash + DI water rinse) before coating
2. Mask connector pins, test points, and transformer core
3. Apply coating by selective spray or dipping
4. Cure per manufacturer specifications
5. Inspect under UV light (acrylic coatings fluoresce under UV for inspection)

## Hipot (Dielectric Withstand) Testing

### Test Specification

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Test voltage | 4000 VAC (5656 V peak) | IEC 62368-1 clause 5.4.11, reinforced: 2x basic |
| Duration | 60 seconds | Production test |
| Test points | Between all primary-side copper (shorted together) and all secondary-side copper (shorted together) | Each secondary domain tested independently |
| Leakage current limit | <5 mA during test | Test equipment threshold |
| Test frequency | 50/60 Hz | Line frequency AC |
| Pass criteria | No breakdown, no flashover, leakage <5 mA | |

### Test Matrix

| Test # | From (shorted together) | To (shorted together) | Voltage | Duration |
|--------|------------------------|----------------------|---------|----------|
| 1 | HV_BUS+, HV_BUS−, PRI_GND, SW_NODE, CLAMP | VDRV_AC+, VNEG_AC, RTN_AC | 4000 VAC | 60 s |
| 2 | HV_BUS+, HV_BUS−, PRI_GND, SW_NODE, CLAMP | VDRV_DC+, VNEG_DC, RTN_DC | 4000 VAC | 60 s |
| 3 | HV_BUS+, HV_BUS−, PRI_GND, SW_NODE, CLAMP | V12V, V5V, V3V3, SEC_GND | 4000 VAC | 60 s |
| 4 | VDRV_AC+, RTN_AC | VDRV_DC+, RTN_DC | 500 VAC | 60 s |
| 5 | VDRV_AC+, RTN_AC | V5V, SEC_GND | 500 VAC | 60 s |

> [!warning] Hipot Test Sequence
> Always perform hipot tests **before** conformal coating, so any defects are caught. Then coat, cure, and re-test at the same voltage as a post-coating verification. A hipot failure after coating indicates a coating defect or contamination under the coating.

### Test Point Design

Provide dedicated test pads for hipot testing:

| Test Pad | Location | Net | Purpose |
|----------|----------|-----|---------|
| TP1 | Primary side, board edge | HV_BUS+ | Primary high-voltage access |
| TP2 | Primary side, board edge | PRI_GND | Primary ground access |
| TP3 | Secondary side, near P4 | RTN_AC | Gate drive A return access |
| TP4 | Secondary side, near P4 | RTN_DC | Gate drive B return access |
| TP5 | Secondary side, near P5 | SEC_GND | Logic ground access |

Test pads: 2 mm diameter, ENIG finish, not covered by solder mask. Place at board edges for probe access.

## Y1 Safety Capacitor

### Purpose

A Y1-class capacitor is placed across the isolation barrier (from PRI_GND to SEC_GND) to provide a return path for common-mode noise current. Without this capacitor, CM noise current has no low-impedance path back to the primary side, resulting in high conducted EMI.

### Specification

| Parameter | Value | Notes |
|-----------|-------|-------|
| Capacitor class | Y1 per IEC 60384-14 | Reinforced insulation rated; fail-open |
| Capacitance | 2.2 nF (typical) | Trade-off: lower = less CM filtering; higher = more leakage current |
| Voltage rating | 500 VAC (or 1500 VDC) | Must withstand working voltage + safety margin |
| Package | Radial through-hole, 7.5–10 mm lead spacing | Provides sufficient creepage on PCB |
| Placement | Bridges the PCB slot, one pad on primary side, one on secondary side |
| Creepage (component body) | ≥14 mm (verified on datasheet) | Must meet reinforced insulation distance |

### Placement Rules

1. Y1 capacitor placed within 10 mm of the flyback transformer (shares the CM noise loop)
2. Primary pad connects to PRI_GND copper pour
3. Secondary pad connects to SEC_GND copper pour
4. The capacitor body overhangs the PCB slot — the component physically bridges the gap
5. No other components within 5 mm of the Y1 capacitor (creepage preservation)
6. Silkscreen safety marking: triangle with "Y1" designation

```
    Y1 capacitor placement across slot (top view):

    PRIMARY SIDE          SLOT           SECONDARY SIDE
    ─────────────   ╔═══════════╗   ──────────────────
                    ║           ║
    PRI_GND pad ────╫── Y1 cap ─╫──── SEC_GND pad
         ○         ║   2.2nF   ║         ○
                    ║           ║
    ─────────────   ╚═══════════╝   ──────────────────
                    ←── 4mm ──→
```

## Leakage Current Budget

### Requirement

Per IEC 62368-1 clause 5.7.2, the total touch current (leakage current) must not exceed:

| Condition | Limit |
|-----------|-------|
| Normal operation | 3.5 mA (for permanently connected equipment) |
| Single fault | 3.5 mA |

### Leakage Current Sources

| Source | Estimated Current | Calculation |
|--------|------------------|-------------|
| Y1 capacitor (2.2 nF at 60 Hz, 920 V) | $I = 2\pi \times 60 \times 2.2 \times 10^{-9} \times 920 = 0.76$ mA | Dominates leakage budget |
| Transformer interwinding capacitance (~20 pF) | $I = 2\pi \times 65000 \times 20 \times 10^{-12} \times 920 = 7.5$ mA | At switching frequency — this is CM noise, not touch current |
| PCB parasitic capacitance (~5 pF across slot) | Negligible at 60 Hz | |
| **Total touch current (60 Hz)** | **~0.76 mA** | Well within 3.5 mA limit |

> [!tip] Touch Current vs. CM Noise Current
> The IEC 62368-1 leakage current limit applies at **mains frequency** (50/60 Hz) and is measured with a specified body impedance network. The high-frequency CM current through the transformer interwinding capacitance (~7.5 mA at 65 kHz) is an EMI concern, not a safety concern per the leakage current test. The Y1 capacitor and the EMI filter together manage the high-frequency CM current.

### Y1 Capacitor Value Selection

The Y1 capacitor value is limited by the leakage current budget:

$$C_{Y1\_max} = \frac{I_{leak\_max}}{2\pi \times f \times V_{bus}} = \frac{3.5 \times 10^{-3}}{2\pi \times 60 \times 920} = 10.1 \text{ nF}$$

The selected 2.2 nF provides a 4.6x margin to the leakage limit. Increasing to 4.7 nF would improve CM filtering but reduce margin to 2.1x.

## Isolation Between Gate Drive Domains

### Functional Isolation (Domain A ↔ Domain B)

The two gate drive supply channels (AC-DC and DC-DC) must be isolated from each other because they have independent return paths that may operate at different potentials (the MOSFET source of each power board is at a different switching potential).

| Parameter | Requirement |
|-----------|-------------|
| Insulation type | Functional |
| Working voltage | 50 V (worst-case differential between gate drive returns) |
| Creepage | 1.6 mm minimum |
| Clearance | 0.5 mm minimum |
| PCB implementation | 1 mm gap between Domain A and Domain B ground pours on L2; no shared copper |
| Hipot test | 500 VAC for 60 s between domains |

### Layout Rules for Domain Separation

1. Each gate drive domain (A, B) has its own ground pour on L2, L1, and L4 — never merged
2. Output inductors and capacitors for Domain A and Domain B maintain 1.6 mm edge-to-edge spacing
3. The transformer has separate secondary winding pins for each domain — pins must maintain 1.6 mm spacing
4. Connector P4 has dedicated return pins for each domain (pin 3 = RTN_AC, pin 7 = RTN_DC)
5. No component straddles the boundary between domains A and B

## Safety Marking and Silkscreen

### Required Markings

| Marking | Location | Symbol |
|---------|----------|--------|
| Isolation barrier | Along PCB slot, both sides | Dashed line with "ISOLATION BARRIER — DO NOT BRIDGE" text |
| Primary side | Primary zone, both sides | "PRIMARY — HAZARDOUS VOLTAGE" |
| Safety ground | Near mounting holes | IEC 60417-5019 earth ground symbol |
| Y1 capacitor | Adjacent to Y1 | "Y1" with safety capacitor symbol |
| Hipot test points | Near TP1–TP5 | "HIPOT TEST" labels |
| Creepage boundaries | Along 14 mm paths | Hatched keepout zone markings |

## Design Verification Checklist

- [ ] Creepage ≥14 mm measured across every primary-to-secondary path (PCB surface, component bodies)
- [ ] Clearance ≥8 mm measured through air across every primary-to-secondary gap
- [ ] PCB slot width ≥4 mm across full 80 mm board height
- [ ] Copper setback from slot edge ≥1 mm on all layers
- [ ] Only transformer, Y1 cap, and optocoupler bridge the slot
- [ ] Y1 capacitor rated Y1 class with ≥500 VAC rating
- [ ] Leakage current <3.5 mA at 60 Hz (calculated and verified by test)
- [ ] Hipot test points accessible on all isolation domains
- [ ] Transformer safety certification (IEC 61558-2-16) obtained
- [ ] Conformal coating specification documented and applied both sides
- [ ] Functional isolation (1.6 mm creepage) maintained between gate drive domains
- [ ] Safety silkscreen markings present on both sides of PCB
- [ ] DRC configured with net classes enforcing creepage/clearance per domain

## Cross-References

- [[__init]] — Board overview, isolation domain map
- [[01-Stack-Up and Layer Assignment]] — Split ground plane, slot location
- [[02-Isolated Converter Layout]] — Transformer placement across barrier, optocoupler
- [[03-Thermal Layout]] — Conformal coating interaction with thermal dissipation
- [[04-Output Filtering and Regulation]] — Y-capacitor role in CM filtering
- [[00-Board Partitioning]] — System-level grounding strategy
- [[06-Creepage and Clearance]] — AC-DC board creepage analysis (reference methodology)

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: IEC 62368-1 analysis, creepage/clearance, PCB slot, hipot, Y-cap, leakage budget |
