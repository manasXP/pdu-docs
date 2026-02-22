---
tags: [pdu, pcb-layout, vienna-pfc, ac-dc, power-electronics]
created: 2026-02-22
status: draft
aliases: [Vienna PFC Board, AC-DC Board]
---

# AC-DC Board — Vienna Rectifier PFC

## 1. Overview

This subfolder documents the PCB layout design for the **Vienna Rectifier PFC stage** of the 30 kW Power Delivery Unit. The AC-DC board converts 3-phase AC mains input into a regulated DC bus voltage suitable for the downstream [[07-PCB-Layout/DC-DC/__init|DC-DC]] converter (LLC or PSFB).

The Vienna PFC topology was selected based on the analysis in [[01-Topology Selection]] for its superior harmonic performance, bidirectional blocking capability, and high power density at the 30 kW level.

## 2. Board Summary

| Parameter | Value |
|-----------|-------|
| Board designation | AC-DC-VPFC-01 |
| Function | 3-phase Vienna rectifier PFC |
| Board dimensions | 250 mm × 180 mm |
| Layer count | 6 |
| Copper weight | L1/L2/L5/L6: 2 oz; L3/L4: 1 oz |
| Minimum trace/space | 0.15 mm / 0.15 mm (signal); power per IPC-2152 |
| Minimum via drill | 0.3 mm |
| Surface finish | ENIG (for SiC soldering reliability) |
| Solder mask | LPI, both sides |
| Board thickness | 1.6 mm nominal |
| Material | FR-4 Tg 170°C minimum |

## 3. Functional Zones

The board is organized into four functional zones arranged along the airflow axis (left-to-right when viewed from the component side):

```
┌────────────────────────────────────────────────────────────────┐
│  EMI Filter    │   Vienna Rectifier    │  DC Bus Caps  │ Conn  │
│   Zone         │      Power Stage      │    Zone       │ Zone  │
│  (~50 mm)      │     (~100 mm)         │  (~50 mm)     │(~50mm)│
│                │                       │               │       │
│ CM choke       │ 6× SiC MOSFETs        │ Bulk e-caps   │ DC out│
│ X-caps         │ 6× STGAP2SiC drivers  │ Film snubbers │ P1b   │
│ Y-caps         │ Snubber arrays        │               │ PE    │
│ (P1b input)    │ Current sensors       │               │ Aux   │
└────────────────────────────────────────────────────────────────┘
          ← Fan intake                          Exhaust →
```

> [!note] NTC and Bypass Relay Relocated
> The NTC inrush thermistors and bypass relay previously shown in the EMI Filter zone have been moved to the [[07-PCB-Layout/Power-Entry/__init|Power Entry board]] (PE-CONT-01). The AC-DC board now receives pre-conditioned AC input via the P1b internal connector from the Power Entry board. See [[07-PCB-Layout/00-Board Partitioning]] for the full 5-board architecture and interface definitions.

## 4. Key Design Parameters

| Parameter | Target | Reference |
|-----------|--------|-----------|
| AC input voltage | 260–530 VAC (750 Vpk) | [[__init]] |
| AC input current | Up to 60 A per phase | [[__init]] |
| DC bus voltage | Up to 920 VDC | [[__init]] |
| DC bus current | Up to 40 A | [[__init]] |
| Switching frequency | 48–65 kHz | [[01-Topology Selection]] |
| Power loop inductance | ≤10 nH PCB contribution | [[07-PCB-Layout/AC-DC/02-Power Loop Analysis|02-Power Loop Analysis]] |
| Gate loop inductance | <5 nH total | [[07-PCB-Layout/AC-DC/03-Gate Driver Layout|03-Gate Driver Layout]] |
| Switching node area | ≤1 cm² per phase | [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout|05-EMI-Aware Layout]] |
| Creepage AC→PE | 10 mm (reinforced, PD2, IIIb) | [[07-PCB-Layout/AC-DC/06-Creepage and Clearance|06-Creepage and Clearance]] |
| Creepage DC bus→PE | 14 mm | [[07-PCB-Layout/AC-DC/06-Creepage and Clearance|06-Creepage and Clearance]] |
| Efficiency target | >98% (SiC-based) | [[__init]] |

## 5. Key Components

### 5.1 Power Semiconductors

| Ref | Part | Package | Qty | Notes |
|-----|------|---------|-----|-------|
| Q1–Q6 | SiC MOSFET 650V/75A | HiP247 / TO-247-4 | 6 | Kelvin source pin; see [[SiC Device Thermal Parameters]] |
| D1–D6 | SiC Schottky 650V/20A | TO-247-2 | 6 | Boost diodes (if discrete) |

### 5.2 Gate Drivers

| Ref | Part | Package | Qty | Notes |
|-----|------|---------|-----|-------|
| U1–U6 | STGAP2SiC | SO-8W (wide body) | 6 | Isolated, 4A sink/source; see [[07-PCB-Layout/AC-DC/03-Gate Driver Layout|03-Gate Driver Layout]] |

### 5.3 Passive Power Components

| Ref | Part | Qty | Notes |
|-----|------|-----|-------|
| C_snub1 | 100 nF C0G 630V 1206/1210 | 24–48 (4–8 per MOSFET) | <5 mm from drain |
| C_snub2 | 1 µF X7R 630V 1812/2220 | 12 (2 per MOSFET) | <10 mm from drain |
| C_bus | 470 µF 450V electrolytic | 4–6 | Series pairs for 900V rating |
| L_boost | PFC inductor (external) | 3 | Board-mounted or chassis-mounted |

> [!tip] BOM Cross-References
> - Full topology rationale: [[01-Topology Selection]]
> - SiC MOSFET thermal characterization: [[SiC Device Thermal Parameters]]
> - Gate driver selection rationale: [[07-PCB-Layout/AC-DC/03-Gate Driver Layout|03-Gate Driver Layout]]
> - DC bus capacitor sizing: [[07-PCB-Layout/AC-DC/02-Power Loop Analysis|02-Power Loop Analysis]]

## 6. Document Index

This subfolder contains the following detailed layout design notes:

1. **[[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment|01-Stack-Up and Layer Assignment]]** — 6-layer stack-up definition, copper weights, zone mapping, and IPC-2152 trace width calculations for 60A AC and 40A DC bus currents.

2. **[[07-PCB-Layout/AC-DC/02-Power Loop Analysis|02-Power Loop Analysis]]** — Vienna PFC commutation loop analysis, parasitic inductance budget, decoupling capacitor placement strategy, and snubber array design.

3. **[[07-PCB-Layout/AC-DC/03-Gate Driver Layout|03-Gate Driver Layout]]** — STGAP2SiC placement rules, gate loop inductance budget, Kelvin source routing, Rg selection, decoupling, and dV/dt immunity measures.

4. **[[07-PCB-Layout/AC-DC/04-Thermal Layout|04-Thermal Layout]]** — TO-247 heatsink mounting, thermal interface materials, thermal via arrays, IPC-2152 bus bar sizing, airflow path optimization, and driver thermal management.

5. **[[07-PCB-Layout/AC-DC/05-EMI-Aware Layout|05-EMI-Aware Layout]]** — Common-mode current budget, switching node area minimization, EMI filter zone separation, stitching via fences, and sensitive signal routing strategy.

6. **[[07-PCB-Layout/AC-DC/06-Creepage and Clearance|06-Creepage and Clearance]]** — IEC 62368-1 creepage and clearance analysis for AC input, DC bus, and gate drive circuits; PCB slot strategy; DRC net class definitions.

## 7. Design Constraints Summary

> [!warning] Critical Layout Constraints
> - L2 (inner ground plane) must remain **continuous and unbroken** across the entire board — no routing, no splits, no thermal relief. This is the primary return path for both power loops and high-frequency signals.
> - EMI filter zone must be separated from the power stage by **≥20 mm** plus a **double-row stitching via fence**.
> - All switching node copper must be confined to **L1 only** with an area **≤1 cm²** per phase to minimize capacitive coupling to the heatsink and chassis.
> - Creepage distances must be maintained even after board assembly — verify that no component body, solder fillet, or conformal coating bridge reduces effective creepage below the rated value.

## 8. Related Documents

- [[__init]] — PDU top-level specifications
- [[01-Topology Selection]] — Vienna PFC topology rationale
- [[SiC Device Thermal Parameters]] — MOSFET and diode thermal data
- [[07-PCB-Layout/__init]] — Parent PCB layout overview
- [[07-PCB-Layout/DC-DC/__init|DC-DC]] — Downstream LLC/PSFB converter board

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
