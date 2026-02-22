---
tags: [pdu, pcb-layout, dc-dc, llc, power-electronics]
created: 2026-02-22
status: draft
aliases: [DC-DC Board Layout, LLC Board]
---

# DC-DC Converter Board — LLC Resonant Converter

## Overview

This subfolder documents the PCB layout design for the **DC-DC stage** of the 30 kW PDU. The board implements a **3-phase interleaved LLC resonant converter** that converts the 920 VDC bus (from the [[07-PCB-Layout/AC-DC/__init|AC-DC board]]) down to the 150–1000 VDC output required for EV battery charging.

The DC-DC board is the most layout-critical board in the PDU due to:
- **Extremely tight voltage margins** on the LLC primary half-bridge (8V margin without snubber)
- **High-frequency transformer mounting** with 4 kV isolation requirements
- **Three interleaved phases** requiring symmetric layout for current sharing
- **Dual high-voltage domains** (920V primary, up to 1000V secondary) with reinforced insulation between them

> [!warning] Critical Design Risk
> The LLC primary half-bridge overshoot analysis shows only **8V margin** to the 1200V MOSFET rating without RC snubbers. The snubber (10 Ω + 1 nF per MOSFET) is **mandatory** and reduces peak voltage to ~1061V, providing 139V margin. This is still tighter than the AC-DC board's PFC stage and demands the most aggressive loop minimization possible.

## Board Summary

| Parameter | Value |
|-----------|-------|
| **Board Dimensions** | 250 mm × 180 mm |
| **Layer Count** | 6 layers |
| **Copper Weights** | L1/L2/L5/L6: 2 oz; L3/L4: 1 oz |
| **Topology** | 3-phase interleaved LLC resonant converter |
| **DC Bus Input** | 920 VDC (from AC-DC via bus bar, P2 connector) |
| **Output** | 150–1000 VDC, 0–100 A (33 A per phase) |
| **Primary Switches** | 6× 1200V SiC MOSFETs (TO-247), half-bridge per phase |
| **Secondary Rectifiers** | 6× 650V SiC MOSFETs (TO-247), sync rectifier per phase |
| **Gate Drivers** | STGAP2SiC (both primary and secondary) |
| **Transformers** | 3× planar/wound, mounted through PCB cutout or on-board |
| **Switching Frequency** | ~100–200 kHz (variable, LLC resonant control) |
| **Peak Efficiency Target** | >98% (SiC-based) |

## Key Design Targets

| Metric | Target | Criticality |
|--------|--------|-------------|
| Primary half-bridge loop inductance | ≤8 nH (PCB contribution) | **CRITICAL** |
| Total primary loop inductance | ~34 nH (incl. package + cap) | **CRITICAL** |
| Primary overshoot (with snubber) | ≤141V (1061V peak) | **CRITICAL** |
| Secondary rectifier loop inductance | ≤12 nH (PCB contribution) | High |
| Secondary overshoot | ≤110V (610V peak) | High |
| Switching node area | ≤1.5 cm² per phase | High |
| Gate loop inductance | <5 nH | High |
| Primary–secondary creepage | Per 4 kV reinforced insulation | **CRITICAL** |
| DC bus to PE clearance | 8 mm clearance, 14 mm creepage | High |
| Output to PE clearance | 8.5 mm clearance, 15 mm creepage | High |
| Phase current symmetry | ≤2% imbalance at full load | Medium |
| Board temperature rise | ≤40°C above ambient (forced air) | Medium |

## 6-Layer Stack-Up

The DC-DC board uses the **same standardized stack-up** as the [[07-PCB-Layout/AC-DC/__init|AC-DC board]] to simplify fabrication and reduce cost:

| Layer | Function | Weight | Notes |
|-------|----------|--------|-------|
| L1 | Top Power | 2 oz | Primary H-bridge, secondary rectifier, bus bars |
| L2 | Continuous GND | 2 oz | Unbroken ground reference plane |
| L3 | Signal | 1 oz | Gate drive signals, control, sensing |
| L4 | Signal / Power Return | 1 oz | Auxiliary power, additional signal routing |
| L5 | Power Plane | 2 oz | DC bus distribution, output power |
| L6 | Bottom Power | 2 oz | Return current paths, additional power |

> [!tip] Stack-Up Standardization
> Using the identical 6-layer stack-up across both AC-DC and DC-DC boards enables a single PCB fabrication order with shared layer specifications, reducing lead time and cost.

## Board Zone Map (Top View)

```
┌───────────────────────────────────────────────────────────┐
│  DC Bus Input Zone (~40mm)                                 │
│  [P2 Bus Bar] [C_bus ×N] [C_bus ×N] [C_bus ×N]           │
│              Phase A     Phase B     Phase C               │
├───────────────────────────────────────────────────────────┤
│  LLC Primary Bridge Zone (~80mm)                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │ Q1A/Q2A │  │ Q1B/Q2B │  │ Q1C/Q2C │                   │
│  │ Driver A│  │ Driver B│  │ Driver C│                   │
│  │ Lr_A Cr_A│ │ Lr_B Cr_B│ │ Lr_C Cr_C│                  │
│  └─────────┘  └─────────┘  └─────────┘                   │
│  ═══════════ ISOLATION BARRIER (PCB SLOT) ════════════════ │
├───────────────────────────────────────────────────────────┤
│  Transformer Mounting Zone (~60mm)                         │
│  ┌─────┐      ┌─────┐      ┌─────┐                       │
│  │ TX_A│      │ TX_B│      │ TX_C│                       │
│  │[cut]│      │[cut]│      │[cut]│                       │
│  └─────┘      └─────┘      └─────┘                       │
├───────────────────────────────────────────────────────────┤
│  Secondary Rectifier Zone (~50mm)                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │ Q3A/Q4A │  │ Q3B/Q4B │  │ Q3C/Q4C │                   │
│  │ Driver A│  │ Driver B│  │ Driver C│                   │
│  │ C_out_A │  │ C_out_B │  │ C_out_C │                   │
│  └─────────┘  └─────────┘  └─────────┘                   │
├───────────────────────────────────────────────────────────┤
│  Output Zone (~30mm)                                       │
│  [C_out combined] [Output Bus Bar / P3a] [Sense/Ctrl]     │
│  DC output → P3a → Power Entry board (contactor) → P3b    │
└───────────────────────────────────────────────────────────┘
```

> [!note] DC Output Routing
> The DC-DC board output connects to the [[07-PCB-Layout/Power-Entry/__init|Power Entry board]] via P3a (internal bus bar / cable). The output contactor (TE EV200) resides on the Power Entry board and isolates the vehicle-facing DC output connector (P3b). See [[07-PCB-Layout/00-Board Partitioning]] for the complete power interface chain.

## Design Document Index

| # | Document | Description |
|---|----------|-------------|
| 1 | [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment|Stack-Up and Layer Assignment]] | 6-layer stack-up details, zone map, IPC-2152 trace sizing |
| 2 | [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] | Primary and secondary loop inductance analysis, snubber design |
| 3 | [[07-PCB-Layout/DC-DC/03-Gate Driver Layout|Gate Driver Layout]] | STGAP2SiC placement, gate loop optimization, isolation barrier |
| 4 | [[07-PCB-Layout/DC-DC/04-Thermal Layout|Thermal Layout]] | Heatsinking, thermal vias, airflow path, transformer thermal |
| 5 | [[07-PCB-Layout/DC-DC/05-EMI-Aware Layout|EMI-Aware Layout]] | Switching node area, resonant tank symmetry, CM current |
| 6 | [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] | Isolation barrier design, DRC net classes, IPC-2221B |

## Cross-References

### Topology and Component Selection
- [[01-Topology Selection]] — LLC resonant converter topology rationale and trade-offs
- [[02-Magnetics Design]] — Transformer and resonant inductor (Lr) design parameters
- [[SiC Device Thermal Parameters]] — MOSFET Rth_jc, power loss budgets

### Companion Board Layout
- [[07-PCB-Layout/AC-DC/__init|AC-DC Board Layout]] — Shares same 6-layer stack-up, similar gate driver approach

### System-Level
- [[10-Mechanical Integration]] — Enclosure, heatsink mounting, bus bar routing between boards
- [[09-Protection and Safety]] — OVP, OCP, OTP requirements that influence layout

## Open Issues

- [ ] Transformer mounting method: through-board cutout vs. surface-mount planar — affects zone sizing
- [ ] Resonant inductor (Lr) integration: discrete inductor vs. integrated into transformer leakage
- [ ] Output bus bar routing: direct to connector or through current sensor first
- [ ] Exact switching frequency range affects EMI filter component sizing on output

## Revision History

| Date | Rev | Author | Changes |
|------|-----|--------|---------|
| 2026-02-22 | 0.1 | — | Initial draft structure |
