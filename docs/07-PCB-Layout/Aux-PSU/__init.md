---
tags: [pdu, pcb-layout, aux-psu, flyback, isolated-supply, power-electronics]
created: 2026-02-22
status: draft
aliases: [Aux PSU Board, Auxiliary Power Supply]
---

# Aux PSU Board — Isolated Auxiliary Power Supply

## 1 Overview

This subfolder documents the PCB layout design for the **Auxiliary Power Supply (Aux PSU)** board of the 30 kW Power Delivery Unit. The Aux PSU provides all low-voltage power rails required by the system — isolated gate drive supplies for the two power boards, logic power for the controller, and fan drive voltage — all derived from the high-voltage DC bus (920 VDC) or an auxiliary AC winding.

The Aux PSU must start up autonomously from the DC bus or AC input before the main converter begins switching, providing a stable standby rail to the controller so it can initialize, perform safety checks, and command the main power stage.

## 2 Board Summary

| Parameter | Value |
|-----------|-------|
| Board designation | AUX-PSU-01 |
| Function | Multi-output isolated auxiliary power supply |
| Board dimensions | 100 mm x 80 mm |
| Layer count | 4 |
| Copper weight | L1/L4: 1 oz (2 oz for power traces); L2/L3: 1 oz |
| Minimum trace/space | 0.15 mm / 0.15 mm (signal); power per IPC-2152 |
| Minimum via drill | 0.3 mm |
| Surface finish | ENIG |
| Solder mask | LPI, both sides |
| Board thickness | 1.6 mm nominal |
| Material | FR-4 Tg 170°C minimum |
| Total output power | 15–25 W across all rails |
| On-board dissipation | 5–10 W (topology-dependent) |

## 3 Output Rail Summary

| Rail | Voltage | Current | Ripple (max) | Load | Isolation | Connector |
|------|---------|---------|-------------|------|-----------|-----------|
| VDRV_AC | +18 V | 0.5 A | <100 mV pp | AC-DC board gate drivers | Reinforced from DC bus; functional from other secondaries | P4 pin 1 |
| VNEG_AC | −5 V | 0.2 A | <50 mV pp | AC-DC board negative gate bias | Same domain as VDRV_AC | P4 pin 2 |
| VDRV_DC | +18 V | 0.5 A | <100 mV pp | DC-DC board gate drivers | Reinforced from DC bus; functional from other secondaries | P4 pin 5 |
| VNEG_DC | −5 V | 0.2 A | <50 mV pp | DC-DC board negative gate bias | Same domain as VDRV_DC | P4 pin 6 |
| +5 V | 5 V | 1.0 A | <50 mV pp | CAN transceiver, digital I/O | Reinforced from DC bus | P5 pin 1 |
| +3.3 V | 3.3 V | 0.5 A | <30 mV pp | MCU logic, ADC reference | Derived from +5 V via LDO | P5 pin 2 |
| +12 V_FAN | 12 V | 2.0 A | <200 mV pp | Enclosure fan(s) | Reinforced from DC bus | P5 pin 4 |
| STBY | 3.3 V | 50 mA | <50 mV pp | Standby controller, wake logic | Reinforced from DC bus | Internal |

**Total output power budget:**

$$P_{out} = (18 \times 0.5 + 5 \times 0.2) \times 2 + 5 \times 1.0 + 3.3 \times 0.5 + 12 \times 2.0 + 3.3 \times 0.05 \approx 23 + 5 + 1.65 + 24 + 0.17 \approx 22.8 \text{ W}$$

At 80% converter efficiency: $P_{in} \approx 28.5$ W, dissipation $\approx 5.7$ W on-board.

## 4 Isolation Domains

The Aux PSU contains **four distinct isolation domains** separated by reinforced or functional insulation barriers:

```
                          ISOLATION BARRIER (4mm PCB slot)
                          ═══════════════════════════════

    PRIMARY SIDE                    SECONDARY SIDE
    ─────────────                   ──────────────

    DC Bus Input          ┌─── Domain A: Gate Drive AC-DC ───┐
    (920 VDC)             │  +18 V / −5 V / RTN_AC           │
    Flyback Primary       │  → P4 pins 1–4                   │
    Clamp Circuit         └──────────────────────────────────┘
    Input Caps
                          ┌─── Domain B: Gate Drive DC-DC ───┐
                          │  +18 V / −5 V / RTN_DC           │
                          │  → P4 pins 5–8                   │
                          └──────────────────────────────────┘

                          ┌─── Domain C: Logic + Fan ────────┐
                          │  +5 V / +3.3 V / +12 V / GND     │
                          │  → P5 pins 1–4                   │
                          │  Standby rail (internal)         │
                          └──────────────────────────────────┘
```

| Boundary | Insulation Class | Working Voltage | Creepage | Clearance |
|----------|-----------------|-----------------|----------|-----------|
| Primary → any secondary | Reinforced (IEC 62368-1) | 920 VDC | 14 mm | 8 mm |
| Domain A ↔ Domain B | Functional | 50 V (gate drive differential) | 1.6 mm | 0.5 mm |
| Domain A/B ↔ Domain C | Functional | 18 V | 1.6 mm | 0.5 mm |

> [!warning] Reinforced Insulation Requirement
> The 920 VDC bus is classified as a hazardous voltage source. All insulation between the primary side and any secondary output must meet **reinforced insulation** per IEC 62368-1. This drives the 4 mm PCB slot, 14 mm creepage, 8 mm clearance, and hipot test requirements detailed in [[05-Safety and Isolation]].

## 5 Functional Block Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│  AUX-PSU-01  (100 mm × 80 mm)                                    │
│                                                                   │
│  PRIMARY SIDE              │ BARRIER │  SECONDARY SIDE            │
│                            │  (slot) │                            │
│  ┌─────────┐  ┌─────────┐ │         │  ┌──────────┐ → +18V/−5V  │
│  │ Input   │→ │ Flyback │ │  XFMR   │  │ Rect +   │   (AC-DC)   │
│  │ Filter  │  │ Primary │─│─────────│─ │ Filter A │ → P4:1-4    │
│  │ + Caps  │  │ + Clamp │ │         │  ├──────────┤             │
│  └─────────┘  └─────────┘ │         │  │ Rect +   │ → +18V/−5V  │
│       ↑                   │         │  │ Filter B │   (DC-DC)   │
│  DC Bus In                │         │  ├──────────┤ → P4:5-8    │
│  (920 VDC)                │         │  │ Rect +   │             │
│                            │         │  │ Filter C │ → +12V/+5V  │
│  ┌─────────┐              │         │  └────┬─────┘ → P5:1-4    │
│  │ PWM     │              │    Y1   │       │                    │
│  │ Control │──────────────│─ ─ ─ ─ │───────┘ Feedback           │
│  │ IC      │  Optocoupler │  cap    │                            │
│  └─────────┘              │         │  ┌──────┐                  │
│                            │         │  │ LDO  │ → +3.3V         │
│                            │         │  └──────┘                  │
│                            │         │  ┌──────┐                  │
│                            │         │  │STBY  │ → 3.3V standby  │
│                            │         │  └──────┘                  │
└───────────────────────────────────────────────────────────────────┘
```

## 6 Key Design Parameters

| Parameter | Target | Reference |
|-----------|--------|-----------|
| Input voltage range | 400–920 VDC (from DC bus) | [[__init]] |
| Total output power | 15–25 W | This document |
| Converter topology | Multi-output flyback | [[02-Isolated Converter Layout]] |
| Switching frequency | 65–130 kHz | [[02-Isolated Converter Layout]] |
| Peak efficiency | >80% | [[03-Thermal Layout]] |
| Primary loop inductance | <15 nH | [[02-Isolated Converter Layout]] |
| Creepage primary-secondary | 14 mm (reinforced) | [[05-Safety and Isolation]] |
| PCB slot width | 4 mm minimum | [[05-Safety and Isolation]] |
| Hipot test | 4000 VAC, 60 s | [[05-Safety and Isolation]] |
| Output ripple (+18 V rail) | <100 mV pp | [[04-Output Filtering and Regulation]] |
| Output ripple (+3.3 V rail) | <30 mV pp | [[04-Output Filtering and Regulation]] |

## 7 Document Index

This subfolder contains the following detailed layout design notes:

1. **[[07-PCB-Layout/Aux-PSU/01-Stack-Up and Layer Assignment]]** — 4-layer stack-up definition, copper weights, isolation barrier zoning, primary/secondary side layer assignments, and via strategy.

2. **[[02-Isolated Converter Layout]]** — Flyback converter primary circuit placement, transformer positioning across the isolation barrier, primary loop optimization, clamp snubber layout, and secondary rectifier routing.

3. **[[03-Thermal Layout]]** — Power dissipation budget, natural convection + conduction thermal design, thermal via arrays, copper pour heat spreading, and component derating at 55°C ambient.

4. **[[04-Output Filtering and Regulation]]** — Post-regulator placement for each rail, LC filter and LDO design, ripple specifications, load transient response, and output connector decoupling.

5. **[[05-Safety and Isolation]]** — Reinforced insulation design per IEC 62368-1, creepage and clearance analysis, PCB slot specification, conformal coating, hipot testing, Y-capacitor selection, and leakage current budget.

## 8 Design Constraints Summary

> [!warning] Critical Layout Constraints
> - The **4 mm PCB slot** across the full board width is the primary isolation barrier. No copper, solder mask bridges, or silkscreen may cross this slot except the flyback transformer footprint and Y-class safety capacitor.
> - The **L2 ground plane is split** into primary-side and secondary-side zones by the isolation barrier. This is fundamentally different from the power board layouts where L2 is continuous.
> - All gate drive output rails (+18 V/−5 V) must maintain **functional isolation** from each other — separate windings, separate rectifiers, separate ground returns.
> - The standby rail must be operational within **50 ms** of DC bus voltage appearing, before any main converter switching begins.

## 9 Related Documents

- [[__init]] — PDU top-level specifications
- [[00-Board Partitioning]] — Multi-board architecture, P4/P5 connector definitions
- [[04-Thermal Budget]] — System-level loss allocation and cooling
- [[07-PCB-Layout/AC-DC/__init]] — AC-DC board (consumer of +18 V/−5 V gate drive supply)
- [[07-PCB-Layout/DC-DC/__init]] — DC-DC board (consumer of +18 V/−5 V gate drive supply)
- [[07-PCB-Layout/Controller/__init]] — Controller board (consumer of +5 V/+3.3 V/+12 V)

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
