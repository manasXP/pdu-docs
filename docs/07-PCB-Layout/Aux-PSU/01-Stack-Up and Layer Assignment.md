---
tags: [pdu, pcb-layout, aux-psu, stack-up, isolation, 4-layer]
created: 2026-02-22
status: draft
---

# 01 — Stack-Up and Layer Assignment

## Purpose

This document defines the 4-layer PCB stack-up for the Aux PSU board. Unlike the power boards (AC-DC and DC-DC) where the stack-up is optimized for minimal power loop inductance, the Aux PSU stack-up is primarily driven by **isolation barrier management** — the board must physically separate 920 VDC primary-side circuitry from all secondary-side outputs with reinforced insulation per IEC 62368-1.

The 4-layer stack-up provides adequate routing density for the low-complexity Aux PSU circuit while maintaining a continuous ground reference on L2 within each isolation domain.

## Stack-Up Definition

### Layer Table

| Layer | Name | Cu Weight | Thickness (um) | Function | Notes |
|-------|------|-----------|-----------------|----------|-------|
| L1 | TOP | 1 oz (2 oz local) | 35 (70 local) | Component placement, power traces | Primary and secondary components; 2 oz pours on input and output power paths |
| — | Prepreg 1 | — | 200 (target) | L1–L2 dielectric | Standard prepreg; 200 um adequate for Aux PSU frequencies |
| L2 | GND | 1 oz | 35 | Split ground plane | Primary GND and secondary GND(s), split at isolation barrier |
| — | Core | — | 1000 | L2–L3 dielectric | Standard FR-4 core; thick core for structural rigidity |
| L3 | PWR/SIG | 1 oz | 35 | Power distribution + signal routing | Secondary output pours, feedback signals, PWM controller routing |
| — | Prepreg 2 | — | 200 (target) | L3–L4 dielectric | Standard prepreg |
| L4 | BOT | 1 oz (2 oz local) | 35 (70 local) | Component placement, power traces | Bottom-side components, additional power routing |

**Total board thickness:** ~1.6 mm (adjust core thickness to achieve target)

> [!tip] Why 4 Layers (Not 6)?
> The Aux PSU carries a maximum of 2 A per rail — far less than the 40–60 A on the power boards. Four layers provide sufficient copper area for 25 W total power delivery. The cost, complexity, and lead time of a 4-layer board are substantially lower than 6-layer, making it appropriate for this low-power auxiliary board. The 100 x 80 mm footprint also limits routing congestion.

### Selective 2 oz Copper

The board uses 1 oz copper as the baseline, with **2 oz copper pours selectively applied** on L1 and L4 for power-carrying paths:

| Path | Layer | Current | 1 oz Width Required | 2 oz Width Required | Implementation |
|------|-------|---------|--------------------|--------------------|----------------|
| DC bus input (+920 V) | L1 | 0.05 A (avg) | 0.15 mm | 0.1 mm | 2 oz pour (for voltage handling, not current) |
| Flyback primary loop | L1 | 0.5 A (pk) | 0.3 mm | 0.2 mm | 2 oz pour for low inductance |
| +18 V output (per channel) | L1/L4 | 0.5 A | 0.3 mm | 0.2 mm | 2 oz pour recommended |
| +12 V fan output | L1/L4 | 2.0 A | 1.5 mm | 0.8 mm | 2 oz pour |
| +5 V output | L1/L4 | 1.0 A | 0.6 mm | 0.4 mm | 2 oz pour |

> [!warning] Selective Copper Weight
> Not all fabricators support selective copper weight on the same layer. If selective 2 oz is unavailable, use full 2 oz on L1 and L4, or use 1 oz throughout with wider pours. Confirm with the fabricator during stack-up review.

## Board Zone Map

The board is divided into two primary zones by the isolation barrier, with the secondary side further subdivided by function:

```
        ←——————————— 100 mm ———————————————→
   ┌──────────────────╥──────────────────────┐  ↑
   │                  ║                      │  │
   │   PRIMARY SIDE   ║    SECONDARY SIDE    │  │
   │    (~35 mm)      ║     (~61 mm)         │  │
   │                  ║                      │  │
   │  DC bus input    ║  ┌─────┬─────┬─────┐ │ 80
   │  Input caps      ║  │Gate │Gate │Logic│ │  mm
   │  Flyback MOSFET  ║  │Drv A│Drv B│+Fan │ │  │
   │  Clamp circuit   ║  │18/−5│18/−5│5/3.3│ │  │
   │  PWM controller  ║  │     │     │/12V │ │  │
   │  Bias winding    ║  └─────┴─────┴─────┘ │  │
   │                  ║   ~20mm ~20mm ~21mm   │  │
   │                  ║                      │  ↓
   └──────────────────╨──────────────────────┘
                      ↑
               4 mm PCB slot
          (isolation barrier)
```

**Slot specification:**
- Width: 4 mm minimum (see [[05-Safety and Isolation]])
- Extends the full 80 mm board height
- Only the flyback transformer footprint and Y1 safety capacitor bridge the slot
- No copper, solder mask, or silkscreen may cross the slot except at designated bridge points

## Layer Assignments by Zone

### Primary Side (35 mm width)

| Layer | Function | Key Nets |
|-------|----------|----------|
| L1 (TOP) | Flyback primary MOSFET, input filter caps, clamp components | HV_BUS+, HV_BUS−, SW_NODE, CLAMP |
| L2 (GND) | Primary ground plane (HV_BUS− reference) | PRI_GND |
| L3 (PWR/SIG) | PWM controller routing, auxiliary bias winding return, feedback optocoupler | VCC_PRI, FB, COMP, RT/CT |
| L4 (BOT) | Additional primary routing, input capacitor return, clamp return | HV_BUS−, PRI_GND |

> [!warning] Primary Side Net Classification
> All nets on the primary side carry hazardous voltage potential (referenced to the 920 VDC bus). The primary ground (PRI_GND) is **not** the same as secondary/logic GND. In the schematic and layout, these must be clearly differentiated with distinct net names and net classes.

### Secondary Side — Gate Drive Domain A (AC-DC)

| Layer | Function | Key Nets |
|-------|----------|----------|
| L1 | +18 V rectifier diode, output inductor, output caps | VDRV_AC+, VNEG_AC, RTN_AC |
| L2 | Gate drive A ground plane (RTN_AC) | RTN_AC |
| L3 | −5 V regulator routing, filter components | VNEG_AC, RTN_AC |
| L4 | Connector P4 pins 1–4 routing, additional output filtering | VDRV_AC+, VNEG_AC, RTN_AC |

### Secondary Side — Gate Drive Domain B (DC-DC)

| Layer | Function | Key Nets |
|-------|----------|----------|
| L1 | +18 V rectifier diode, output inductor, output caps | VDRV_DC+, VNEG_DC, RTN_DC |
| L2 | Gate drive B ground plane (RTN_DC) | RTN_DC |
| L3 | −5 V regulator routing, filter components | VNEG_DC, RTN_DC |
| L4 | Connector P4 pins 5–8 routing, additional output filtering | VDRV_DC+, VNEG_DC, RTN_DC |

### Secondary Side — Logic + Fan Domain C

| Layer | Function | Key Nets |
|-------|----------|----------|
| L1 | +12 V rectifier, +5 V LDO, +3.3 V LDO, output caps | V12V, V5V, V3V3, SEC_GND |
| L2 | Logic/fan ground plane (SEC_GND) | SEC_GND |
| L3 | Standby regulator, feedback divider routing | STBY, V5V, SEC_GND |
| L4 | Connector P5 routing, fan output, additional filtering | V12V, V5V, V3V3, SEC_GND |

## L2 Ground Plane — Split Configuration

Unlike the power boards where L2 is a single continuous ground plane, the Aux PSU L2 is **intentionally split** into four isolated ground zones:

```
L2 Ground Plane (view from top):

┌──────────────╥─────────┬─────────┬──────────┐
│              ║         │         │          │
│   PRI_GND   ║  RTN_AC │  RTN_DC │ SEC_GND  │
│              ║  (GD-A) │  (GD-B) │ (Logic)  │
│   920 VDC   ║  +18/−5 │  +18/−5 │ +5/3.3/  │
│   reference  ║  domain │  domain │  12V     │
│              ║         │         │          │
└──────────────╨─────────┴─────────┴──────────┘
     ~35 mm   slot  ~20 mm   ~20 mm   ~21 mm
```

### Ground Plane Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| PRI_GND to any secondary | 4 mm slot + 14 mm creepage | Reinforced insulation per IEC 62368-1 |
| RTN_AC to RTN_DC gap | 1.0 mm minimum | Functional isolation between gate drive domains |
| RTN_AC/RTN_DC to SEC_GND gap | 1.0 mm minimum | Functional isolation; different return paths |
| No copper bridges across slot | Absolute rule | Only transformer pads and Y-cap pads cross the barrier |
| Each ground zone fully filled | >90% copper fill | Minimize impedance within each domain |
| Stitching vias within each zone | 0.3 mm vias, 3 mm pitch | Connect L2 ground zone to L1/L4 ground pours |

> [!tip] DRC Net Class Configuration
> Set up distinct net classes in the EDA tool for each ground domain:
> - `NC_PRI` — primary-side nets, 14 mm clearance to all secondary classes
> - `NC_GDA` — gate drive A nets, 1 mm clearance to NC_GDB and NC_SEC
> - `NC_GDB` — gate drive B nets, 1 mm clearance to NC_GDA and NC_SEC
> - `NC_SEC` — logic/fan secondary nets, 1 mm clearance to NC_GDA and NC_GDB
>
> This enforces isolation distances automatically during layout.

## Via Strategy

### Power Vias (L1 ↔ L4)

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.4 mm |
| Pad diameter | 0.8 mm |
| Finished hole | 0.3 mm |
| Current per via | ~1.0 A (IPC-2152, 30°C rise, 1 oz plating) |
| Array for 2 A fan rail | 3 vias minimum (use 4+) |
| Array for 0.5 A gate drive | 2 vias minimum |

### Signal Vias (L1/L4 ↔ L3)

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.3 mm |
| Pad diameter | 0.6 mm |
| Finished hole | 0.2 mm |
| Usage | PWM controller, feedback, optocoupler |

### Thermal Vias

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.3 mm |
| Pad diameter | 0.6 mm |
| Pitch | 1.27 mm |
| Array | 3x3 under MOSFET, 2x2 under rectifier diodes |
| Fill | Tented or plugged |

See [[03-Thermal Layout]] for thermal via placement under dissipative components.

### Stitching Vias

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.3 mm |
| Pad diameter | 0.6 mm |
| Pitch | 3 mm along zone boundaries |
| Usage | Connect L1/L4 ground pours to L2 ground zone within each domain |

> [!warning] No Stitching Vias Across Isolation Barrier
> Stitching vias must only connect copper within the **same isolation domain**. A via that connects primary-side L1 copper through L2 PRI_GND to L4 primary copper is correct. A via that connects any primary copper to any secondary copper is a catastrophic isolation failure. Verify via assignments against net classes after placement.

## Impedance Considerations

The Aux PSU has minimal controlled-impedance requirements. All signals are low-frequency (PWM controller at 65–130 kHz, feedback loop bandwidth <10 kHz):

| Signal | Target Z0 | Layer | Notes |
|--------|-----------|-------|-------|
| PWM controller to MOSFET gate | Not controlled | L1 | Short (<10 mm), series gate resistor dominates |
| Optocoupler feedback | Not controlled | L3 | Low bandwidth, <5 kHz loop |
| Bias winding sense | Not controlled | L3 | Low current, shield with ground pour |

## Design for Manufacturing (DFM) Notes

| Parameter | Value | Standard |
|-----------|-------|----------|
| Minimum trace width (signal) | 0.15 mm | IPC Class 2 |
| Minimum trace spacing (signal) | 0.15 mm | IPC Class 2 |
| Minimum trace spacing (primary-secondary) | 4 mm slot + creepage | IEC 62368-1 |
| Minimum via-to-via spacing | 0.5 mm | Fab-dependent |
| Minimum annular ring | 0.125 mm | IPC Class 2 |
| Board thickness tolerance | +/- 10% | IPC-6012 Class 2 |
| Surface finish | ENIG | Reliable soldering |
| PCB slot | 4 mm wide, full board height, routed (not V-scored) | Isolation barrier |
| Solder mask | LPI, both sides | Standard |
| Silkscreen | White, both sides | Zone labels + safety markings |

> [!tip] PCB Slot Fabrication
> The 4 mm isolation slot must be **routed** (milled) by the fabricator, not V-scored. Specify the slot on the board outline layer (Edge.Cuts in KiCad) or as a routed cutout on the mechanical layer. The slot walls should be smooth and free of copper burrs to prevent tracking. Confirm with the fabricator that the slot meets the specified width tolerance (+/- 0.1 mm).

## Cross-References

- [[__init]] — Board overview, rail summary, isolation domain map
- [[02-Isolated Converter Layout]] — Transformer placement across isolation barrier
- [[03-Thermal Layout]] — Thermal via strategy
- [[05-Safety and Isolation]] — Creepage, clearance, PCB slot specifications
- [[00-Board Partitioning]] — Multi-board architecture, connector definitions

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: 4-layer stack-up, split ground plane, zone map, via strategy |
