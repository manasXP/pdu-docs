---
tags: [pdu, pcb-layout, dc-dc, llc, creepage, clearance, isolation, safety, ipc-2221b]
created: 2026-02-22
status: draft
---

# 06 — Creepage and Clearance

## Purpose

This document specifies the creepage (surface distance) and clearance (air gap) requirements for the DC-DC LLC resonant converter board. The DC-DC board has the most demanding isolation requirements in the PDU due to the **primary-secondary isolation barrier** (4 kV hipot, reinforced insulation) and the presence of **two independent high-voltage domains** (920V primary, up to 1000V secondary).

## Applicable Standards

| Standard | Scope | Key Requirements |
|----------|-------|-----------------|
| **IPC-2221B** | PCB design (general) | Internal/external clearances for working voltage |
| **IEC 62368-1** | IT/AV/communication equipment safety | Creepage/clearance for insulation types |
| **IEC 61851-23** | EV charging — DC requirements | 4 kV hipot between primary and secondary |
| **UL 2202** | EV charging equipment (North America) | Reinforced insulation requirements |
| **IEC 60664-1** | Insulation coordination | Pollution degree, overvoltage category |
| **EN 61000-series** | EMC | Not directly creepage, but influences layout |

### Design Environment Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Pollution degree | PD2 (normal industrial) | Enclosed equipment, non-condensing |
| Overvoltage category | OVC III (primary), OVC II (secondary) | Mains-connected primary, battery secondary |
| Material group | IIIb (FR-4, CTI 175–399 V) | Standard FR-4 laminate |
| Altitude | ≤2000 m | Standard; above 2000 m requires derating |
| Operating temperature | −20°C to +75°C | PDU specification |
| Conformal coating | Yes (Humiseal 1A33 or equivalent) | Applied to isolation-critical areas |

## Voltage Domains and Boundaries

The DC-DC board has four distinct voltage domains:

```
  ┌────────────────────────────────────────────────────────┐
  │                                                         │
  │  DOMAIN 1: DC BUS PRIMARY                              │
  │  Voltage: 920 VDC nominal (up to 1060V transient)      │
  │  Referenced to: Primary GND / PE                        │
  │  Components: Bus caps, primary MOSFETs,                │
  │              resonant tank, TX primary                  │
  │                                                         │
  ├════════════ ISOLATION BARRIER (4 kV) ══════════════════┤
  │                                                         │
  │  DOMAIN 2: DC OUTPUT SECONDARY                          │
  │  Voltage: 150–1000 VDC (output to EV battery)          │
  │  Referenced to: Secondary GND (floating)                │
  │  Components: Secondary rectifiers, output caps,         │
  │              TX secondary, output connector              │
  │                                                         │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  DOMAIN 3: PRIMARY CONTROL (LOW VOLTAGE)                │
  │  Voltage: 15V / 5V / 3.3V                              │
  │  Referenced to: Primary GND                              │
  │  Components: Primary gate drivers (input side),          │
  │              control MCU, CAN transceiver (primary)      │
  │                                                         │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  DOMAIN 4: SECONDARY CONTROL (LOW VOLTAGE)               │
  │  Voltage: 15V / 5V / 3.3V                                │
  │  Referenced to: Secondary GND                              │
  │  Components: Secondary gate drivers (input side),          │
  │              output voltage/current sense                   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

## Clearance and Creepage Requirements

### External (PCB Surface) Requirements

| Boundary | Working Voltage | Insulation Type | Clearance (mm) | Creepage (mm) | Notes |
|----------|----------------|-----------------|----------------|---------------|-------|
| DC bus (920V) → PE/GND | 920V + transients | Basic | 8.0 | 14.0 | OVC III, PD2 |
| DC bus + → DC bus − | 920 VDC | Functional | 4.0 | 7.0 | Within same domain |
| Output (1000V) → PE/GND | 1000 VDC | Basic | 8.5 | 15.0 | OVC II, PD2 |
| Output + → Output − | 1000 VDC | Functional | 4.5 | 8.0 | Within same domain |
| **Primary → Secondary** | **4000V test** | **Reinforced** | **10.0** | **20.0** | **IEC 61851-23** |
| Primary HV → Primary LV | 920V | Basic | 8.0 | 14.0 | Driver input to output side |
| Secondary HV → Secondary LV | 1000V | Basic | 8.5 | 15.0 | Driver input to output side |
| Switching node → adjacent trace | 920V (primary) | Functional | 4.0 | 7.0 | Same domain |
| Any HV → mounting hole (PE) | 920V / 1000V | Basic | 8.0–8.5 | 14.0–15.0 | Screw = PE potential |

### Internal (Between PCB Layers) Requirements — IPC-2221B

Internal clearances are significantly smaller than external because the insulating material (FR-4) has a much higher dielectric strength than air:

| Boundary | Working Voltage | Min Internal Clearance (mm) | Notes |
|----------|----------------|-----------------------------|-------|
| DC bus traces on L5 → L2 GND | 920V | 0.6 | FR-4 dielectric strength ~40 kV/mm |
| Output traces on L5 → L2 GND | 1000V | 0.7 | Same FR-4 |
| Primary → Secondary (internal) | 4000V test | **N/A — no internal crossing** | Isolation barrier extends through all layers |
| Signal (L3) → L2 GND | <50V | 0.1 | Standard signal clearance |

> [!warning] No Internal Primary-Secondary Crossing
> Unlike external clearances that can be satisfied with adequate spacing, the primary-secondary isolation **cannot** be achieved by merely spacing internal layer copper. The barrier must be a **physical slot** through the full PCB stack-up, removing all FR-4 and copper between the primary and secondary domains. No copper on L2, L3, L4, or L5 may bridge the isolation barrier.

## Primary-Secondary Isolation Barrier — Detailed Design

### Physical Implementation

The isolation barrier is implemented as a **routed slot** through the entire PCB:

```
  Cross-section at isolation barrier:

  L1 ──[Primary copper]──  ≥2mm  │←4mm slot→│  ≥2mm  ──[Secondary copper]──
  L2 ──[Primary GND]─────  ≥2mm  │          │  ≥2mm  ──[Secondary GND]────
  L3 ──[Primary signal]──  ≥2mm  │  AIR /   │  ≥2mm  ──[Secondary signal]─
  L4 ──[Primary sig/pwr]─  ≥2mm  │ CONFORMAL│  ≥2mm  ──[Secondary sig/pwr]
  L5 ──[Primary power]───  ≥2mm  │ COATING  │  ≥2mm  ──[Secondary power]──
  L6 ──[Primary copper]──  ≥2mm  │          │  ≥2mm  ──[Secondary copper]──

  Total keep-out zone: 4mm slot + 2×2mm clearance = 8mm minimum
```

### Barrier Specifications

| Parameter | Value | Standard Reference |
|-----------|-------|--------------------|
| Slot width | ≥4 mm | IPC-2221B for reinforced insulation at 4 kV |
| Slot length | Full board width (250 mm) | End-to-end isolation |
| Copper clearance from slot edge | ≥2 mm (all layers) | Additional safety margin |
| Slot routing method | CNC routed, 2 mm end mill | Smooth edges, no burrs |
| Conformal coating at slot | Both sides, extending 5 mm from slot edge | Prevents contamination ingress |
| Total effective separation | 8 mm (4 mm slot + 2×2 mm clearance) | Exceeds 10 mm clearance requirement with coating credit |

> [!note] Conformal Coating Creepage Credit
> Per IEC 60664-1 and IPC-2221B, conformal coating (Type AR per IPC-CC-830) can reduce creepage requirements by providing a sealed surface resistant to contamination. With coating applied, the effective creepage is measured along the **coated surface** rather than the bare PCB surface. However, for reinforced insulation, many certification bodies do not grant full coating credit. Design for the uncoated requirement (20 mm creepage) and use coating as additional margin.

### Slots at Transformer Interface

The isolation barrier must pass through or around each transformer. Since the transformer physically bridges the primary and secondary domains, special attention is needed:

#### Option 1: Barrier Passes Around Transformers

```
  Primary Domain
  ────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────
              │    │              │    │              │    │
  ════════════╡    ╞══════════════╡    ╞══════════════╡    ╞════════
              │    │              │    │              │    │
  ────────────┘    └──────────────┘    └──────────────┘    └────────
  Secondary Domain  [TX_A cutout]     [TX_B cutout]     [TX_C cutout]

  The barrier slot routes around each transformer cutout, maintaining
  isolation continuity while allowing the transformer to bridge the gap.
```

#### Option 2: Barrier Is Integral with Transformer Cutouts

```
  Primary Domain
  ────────────────────────────────────────────────────
  ════╤════════════════╤════════════════╤════════════
      │  TX_A cutout   │  TX_B cutout   │  TX_C cutout
      │  (extends slot)│  (extends slot)│  (extends slot)
  ════╧════════════════╧════════════════╧════════════
  ────────────────────────────────────────────────────
  Secondary Domain

  The transformer cutouts are part of the isolation barrier.
  Slot width at cutout ≥4mm on each side of transformer pins.
```

> [!tip] Preferred: Option 2
> Making the transformer cutouts part of the isolation barrier simplifies the board design and saves PCB area. The transformer's own insulation system (per its safety certification) handles the isolation between its primary and secondary pins. The PCB only needs to ensure adequate creepage around the transformer landing pads.

### Creepage Around Transformer Pins

The transformer primary pins and secondary pins land on opposite sides of the isolation barrier. The creepage path between the closest primary pin and the closest secondary pin must satisfy the reinforced insulation requirement:

```
Creepage path: Primary pin pad → PCB surface → around cutout edge →
               PCB surface → Secondary pin pad

Minimum required: 20 mm (reinforced insulation, 4 kV)

Design approach:
  - Primary pin pad to cutout edge: ≥3 mm
  - Cutout edge to cutout edge (through air): not counted as creepage
  - Cutout edge to secondary pin pad: ≥3 mm
  - Around cutout perimeter (PCB surface): ≥14 mm
  - Total surface path: ≥20 mm ✓
```

## STGAP2SiC Driver Isolation

Each of the 12 STGAP2SiC gate drivers has its own internal isolation barrier between input and output pins. The PCB must support this isolation:

### Driver PCB Slot

| Parameter | Value |
|-----------|-------|
| Slot width | 3 mm (centered between input and output pin rows) |
| Slot length | 12 mm (spanning the IC body width + 1 mm each side) |
| Copper clearance from slot edge | 1 mm (all layers) |
| Total input-to-output distance on PCB | 3 mm slot + 2×1 mm = 5 mm |
| IC package creepage (SO-16W) | 8 mm (per datasheet — meets IEC 60664-1) |

```
  Top View of STGAP2SiC on PCB:

  Input pins (1-8)     │ 3mm PCB slot │     Output pins (9-16)
  ─────────────────────│              │─────────────────────
  │ VDD GND IN  EN     │              │     OUT+ OUT- VCC GND │
  │ 1   2   3   4      │              │     16   15   14  13  │
  │                     │              │                       │
  │ 5   6   7   8      │              │     12   11   10  9   │
  │ DESAT CLAMP NC NC  │              │     NC   NC  UVLO NC  │
  ─────────────────────│              │─────────────────────
                        │              │
                        │ (no copper   │
                        │  any layer)  │
```

### Creepage Verification per Driver

| Path | Distance | Requirement | Status |
|------|----------|-------------|--------|
| Input pin 1 → Output pin 16 (across IC) | 8 mm (IC package) | Per STGAP2SiC datasheet | Meets |
| Input pad → Output pad (on PCB) | ≥5 mm (slot + clearance) | Supplemented by IC package | Meets |
| Input trace → Output trace (nearest approach) | ≥3 mm (slot enforces) | Basic insulation for driver supply voltage | Meets |

## DRC Net Class Table

Configure the KiCad DRC (Design Rule Check) with the following net classes to automatically enforce clearance and creepage rules:

### Net Class Definitions

| Net Class | Nets Included | Min Clearance to Others | Min Trace Width | Notes |
|-----------|--------------|------------------------|-----------------|-------|
| `DC_BUS_PRI` | DC_BUS_P, DC_BUS_N, SW_A, SW_B, SW_C | See matrix below | 5.5 mm (pour) | 920V primary |
| `OUTPUT_SEC` | OUT_P, OUT_N, SEC_SW_A/B/C | See matrix below | 7.0 mm (pour) | Up to 1000V secondary |
| `PRI_CTRL` | PRI_15V, PRI_5V, PRI_3V3, PRI_GND | See matrix below | 0.15 mm | Primary low-voltage control |
| `SEC_CTRL` | SEC_15V, SEC_5V, SEC_3V3, SEC_GND | See matrix below | 0.15 mm | Secondary low-voltage control |
| `GATE_PRI` | GATE_Q1A-C, GATE_Q2A-C, KELSRC_Q1A-C, KELSRC_Q2A-C | See matrix below | 0.20 mm | Primary gate drive |
| `GATE_SEC` | GATE_Q3A-C, GATE_Q4A-C, KELSRC_Q3A-C, KELSRC_Q4A-C | See matrix below | 0.20 mm | Secondary gate drive |
| `PE` | PE, CHASSIS, MOUNTING | See matrix below | 1.0 mm | Protective earth |
| `DEFAULT` | All other nets | 0.15 mm | 0.15 mm | Standard signal |

### Clearance Matrix (mm) — External Layers (L1, L6)

| | DC_BUS_PRI | OUTPUT_SEC | PRI_CTRL | SEC_CTRL | GATE_PRI | GATE_SEC | PE |
|---|-----------|-----------|----------|----------|----------|----------|-----|
| **DC_BUS_PRI** | 4.0 | **10.0** | 8.0 | **10.0** | 4.0 | **10.0** | 8.0 |
| **OUTPUT_SEC** | **10.0** | 4.5 | **10.0** | 8.5 | **10.0** | 4.5 | 8.5 |
| **PRI_CTRL** | 8.0 | **10.0** | 0.15 | **10.0** | 0.15 | **10.0** | 0.5 |
| **SEC_CTRL** | **10.0** | 8.5 | **10.0** | 0.15 | **10.0** | 0.15 | 0.5 |
| **GATE_PRI** | 4.0 | **10.0** | 0.15 | **10.0** | 0.15 | **10.0** | 8.0 |
| **GATE_SEC** | **10.0** | 4.5 | **10.0** | 0.15 | **10.0** | 0.15 | 8.5 |
| **PE** | 8.0 | 8.5 | 0.5 | 0.5 | 8.0 | 8.5 | — |

> [!warning] 10 mm Entries Are Isolation Barrier
> All entries showing **10.0 mm** in the matrix represent the primary-secondary isolation barrier. These clearances are enforced by the **physical PCB slot**, not by copper spacing alone. The DRC net class system prevents any routing tool from bridging the barrier, but the slot must be drawn manually in the board outline / keep-out layer.

### Clearance Matrix (mm) — Internal Layers (L2–L5)

| Boundary | Internal Clearance | Notes |
|----------|--------------------|-------|
| DC_BUS_PRI → same class | 0.3 mm | FR-4 dielectric between L1 and L5 |
| OUTPUT_SEC → same class | 0.3 mm | Same |
| DC_BUS_PRI → PRI_CTRL | 0.6 mm | 920V across FR-4 |
| OUTPUT_SEC → SEC_CTRL | 0.7 mm | 1000V across FR-4 |
| **Primary → Secondary** | **N/A** | **No internal crossing permitted** |
| Any HV → PE (via/pad) | 0.6 mm | Around mounting holes |

## IPC-2221B Internal Clearance Reference

For reference, IPC-2221B Table 6-1 (Internal Conductors, B1 class):

| Working Voltage (DC) | Minimum Spacing (mm) |
|----------------------|---------------------|
| 0–100 V | 0.10 |
| 101–300 V | 0.25 |
| 301–500 V | 0.40 |
| 501–700 V | 0.50 |
| 701–1000 V | 0.63 |
| 1001–1500 V | 0.80 |
| >1500 V | Calculated per formula |

> [!note] Internal vs. External
> Internal clearances in IPC-2221B are much smaller than external because FR-4 has a dielectric strength of ~40 kV/mm (at 1.6 mm thickness). Even at 920V working voltage, the 0.63 mm internal clearance provides a safety factor of ~100. However, this assumes no voids, delamination, or contamination in the FR-4 — which is why IPC Class 2 fabrication quality is specified.

## Special Creepage Zones

### Zone 1: DC Bus Input (Bus Bar to Capacitors)

| Boundary | Clearance | Creepage |
|----------|-----------|---------|
| P2 bus bar pad (920V) → board edge | 8 mm | 14 mm |
| P2 bus bar pad → nearest mounting hole (PE) | 8 mm | 14 mm |
| DC bus + pad → DC bus − pad | 4 mm | 7 mm |
| Bus capacitor pads → adjacent signal trace | 8 mm | 14 mm |

### Zone 2: Primary Half-Bridge (Switching Nodes)

| Boundary | Clearance | Creepage |
|----------|-----------|---------|
| Switching node pour → primary GND pour | 4 mm | 7 mm |
| Q1 drain pad (DC bus +) → Q2 source pad (DC bus −) | 4 mm | 7 mm |
| Q1/Q2 pads → gate driver IC input pins | 8 mm | 14 mm |
| Snubber pad → adjacent low-voltage component | 8 mm | 14 mm |

### Zone 3: Isolation Barrier (Transformer Area)

| Boundary | Clearance | Creepage |
|----------|-----------|---------|
| Primary copper → Secondary copper (across barrier) | 10 mm | 20 mm |
| TX primary pin → TX secondary pin (around cutout) | 10 mm | 20 mm |
| Y-capacitor pad (primary side) → Y-cap pad (secondary side) | 10 mm | 20 mm |
| Driver IC input pin → driver IC output pin (across slot) | Per STGAP2SiC spec (8 mm) | Per STGAP2SiC spec |

### Zone 4: Secondary Rectifiers

| Boundary | Clearance | Creepage |
|----------|-----------|---------|
| Secondary switching node → secondary GND | 4.5 mm | 8 mm |
| Q3/Q4 pads → gate driver IC input pins | 8.5 mm | 15 mm |
| Output + pad → Output − pad | 4.5 mm | 8 mm |

### Zone 5: Output Connector (P3)

| Boundary | Clearance | Creepage |
|----------|-----------|---------|
| P3 output pad (1000V) → board edge | 8.5 mm | 15 mm |
| P3 output pad → nearest mounting hole (PE) | 8.5 mm | 15 mm |
| Output bus bar → PE copper | 8.5 mm | 15 mm |

## Conformal Coating Strategy

### Coating Application Map

| Area | Coating Required? | Reason |
|------|------------------|--------|
| Isolation barrier (slot + 5 mm each side) | **Yes** | Prevents contamination bridging the barrier |
| STGAP2SiC driver slots + 3 mm each side | **Yes** | Prevents tracking across driver isolation |
| Transformer mounting area | **Yes** | High-voltage, exposed area |
| DC bus input zone | Optional | Indoor equipment; helps with humidity |
| Output zone | Optional | Same |
| Control/signal zone | No | Low voltage, not safety-critical |
| Component pads requiring rework | **Selective mask** | Leave test points and adjustment pots uncoated |

### Coating Specification

| Parameter | Specification |
|-----------|--------------|
| Material | Humiseal 1A33 (acrylic) or equivalent per IPC-CC-830 Type AR |
| Thickness | 25–75 µm (1–3 mils) |
| Application | Selective spray or brush, avoiding connectors and test points |
| Dielectric strength | >50 kV/mm (acrylic) |
| Temperature range | −55°C to +130°C |
| Cure | Air dry 24h or UV cure per material datasheet |

> [!tip] Coating Does Not Replace Distance
> Conformal coating adds margin but does not replace the required creepage/clearance distances. Design the PCB to meet all requirements **without** coating, then apply coating as an additional layer of protection. Certification bodies may not accept coating as a substitute for physical distance in reinforced insulation applications.

## Hipot Test Requirements

### Factory Test Specification

| Test | Voltage | Duration | Pass Criteria | Reference |
|------|---------|----------|---------------|-----------|
| Primary-to-Secondary | 4000 VAC (or 5660 VDC) | 60 seconds | Leakage <10 mA | IEC 61851-23 |
| Primary-to-PE | 2500 VAC (or 3535 VDC) | 60 seconds | Leakage <10 mA | IEC 62368-1 |
| Secondary-to-PE | 2500 VAC (or 3535 VDC) | 60 seconds | Leakage <10 mA | IEC 62368-1 |

### Design for Hipot Survival

| Factor | Requirement |
|--------|-------------|
| No sharp copper edges at isolation barrier | Smooth pour edges, no acute angles pointing across barrier |
| No solder bridges across barrier | Solder mask extends over barrier; slot prevents bridging |
| Conformal coating at barrier | Prevents surface flashover during hipot |
| No flux residue at barrier | Clean with IPA after soldering; specify no-clean flux |
| PCB quality | IPC Class 2 minimum; no delamination, no voids near barrier |
| Test point isolation | All test points on one side of barrier only |

## Layout Checklist — Creepage and Clearance

- [ ] KiCad DRC net classes configured per the matrix in this document
- [ ] Isolation barrier slot drawn in board outline (4 mm wide, full board width)
- [ ] Copper clearance ≥2 mm from slot edge on all 6 layers verified
- [ ] No copper on any layer crosses the isolation barrier
- [ ] STGAP2SiC PCB slots drawn (3 mm wide × 12 mm long, ×12 ICs)
- [ ] Transformer cutout creepage verified (≥20 mm surface path primary to secondary)
- [ ] DC bus to PE clearance ≥8 mm verified at all mounting holes
- [ ] Output to PE clearance ≥8.5 mm verified at all mounting holes
- [ ] Internal layer clearances per IPC-2221B verified
- [ ] DRC run with zero violations
- [ ] Conformal coating mask layer created for selective application
- [ ] Y-capacitor placement at barrier verified (primary GND to secondary GND)
- [ ] No sharp copper points aimed across any high-voltage gap
- [ ] Solder mask covers isolation barrier area (prevents solder bridging)
- [ ] Hipot test procedure documented for factory acceptance testing

## Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board-level isolation requirements
- [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment|Stack-Up and Layer Assignment]] — Internal layer clearances
- [[07-PCB-Layout/DC-DC/03-Gate Driver Layout|Gate Driver Layout]] — STGAP2SiC isolation slots, barrier signal crossing
- [[07-PCB-Layout/DC-DC/05-EMI-Aware Layout|EMI-Aware Layout]] — Y-capacitors at barrier, CM current path
- [[07-PCB-Layout/AC-DC/06-Creepage and Clearance|AC-DC Creepage and Clearance]] — Companion board creepage (simpler — no isolation barrier)
- [[09-Protection and Safety]] — System-level safety requirements, hipot test specifications
