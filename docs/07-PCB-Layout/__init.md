---
tags: [PDU, PCB, layout, multi-board, SiC]
created: 2026-02-22
status: draft
---

# 07 – PCB Layout: Multi-Board Architecture for 30 kW PDU

> [!summary] Overview
> PCB layout documentation for the 30 kW PDU, organized as a **5-board architecture**. Each board is independently designed, fabricated, and testable, interconnected by power bus bars and signal harnesses. The 5th board — the [[07-PCB-Layout/Power-Entry/__init\|Power Entry board]] — consolidates all electromechanical wear items (NTC thermistors, bypass relays, output contactor) for serviceability and thermal isolation. Layout guidelines address SiC switching transients (20–35 kV/µs dV/dt, 5–15 A/ns dI/dt), safety isolation (IEC 62368-1), and EN 55032 Class B EMC compliance.

## 1. Board Architecture

| Board | Function | Layers | Size (mm) | Cu Weight |
|-------|----------|--------|-----------|-----------|
| **[[07-PCB-Layout/Power-Entry/__init\|Power Entry]]** | AC input protection (NTC, bypass relay), DC output isolation (contactor), external connectors | 2 | 150 × 120 | 4 oz |
| **[[07-PCB-Layout/AC-DC/__init\|AC-DC]]** | Vienna Rectifier PFC — EMI filter, 3-phase rectification, DC bus caps | 6 | 250 × 180 | 2 oz |
| **[[07-PCB-Layout/DC-DC/__init\|DC-DC]]** | LLC Resonant converter — primary bridge, transformers, secondary rectifier, output caps | 6 | 250 × 180 | 2 oz |
| **[[07-PCB-Layout/Controller/__init\|Controller]]** | STM32G474RE, CAN bus, analog signal conditioning, OCPP/ISO 15118 | 4 | 120 × 100 | 1 oz |
| **[[07-PCB-Layout/Aux-PSU/__init\|Aux-PSU]]** | Isolated supplies — gate drive (+18 V/−5 V), logic (3.3 V/5 V), fan (12 V), standby | 4 | 100 × 80 | 1 oz |

See [[00-Board Partitioning]] for inter-board connector pinouts, harness design, and grounding strategy.

## 2. System Block Diagram

```
  AC Input     ┌──────────┐  P1b     ┌──────────┐  P2 (Bus Bar)  ┌──────────┐
  3φ 530 VAC ─→│  Power   │ ──60A──→ │  AC-DC   │ =====920V===→  │  DC-DC   │
  60 A    P1a  │  Entry   │  530VAC  │  Board   │     40 A       │  Board   │
               │  Board   │          └────┬─────┘                └────┬─────┘
  DC Output  ←─│          │←── P3a ─── 100A DC ──────────────────────┘
  150–1000 VDC │(contactor│  (pre-contactor)
  100 A   P3b  └────┬─────┘
                  S4 │ Signal Harness          S1 │          S2 │
               ┌─────┴─────────────────────────┬──┴──────┬───┴──┐
               │         Controller Board       │         │      │
               │         STM32G474RE            │         │      │
               └────────────┬───────────────────┘         │      │
                            │ CAN / OCPP / ISO 15118      │      │
                       ┌────┴─────┐                       │      │
                       │  Aux PSU │ ── Gate Drive Power ──┘      │
                       │  Board   │ ── +18 V / −5 V ────────────┘
                       │          │ ── +24 V coil (to Power Entry via S4)
                       └──────────┘
```

## 3. Documents

### System-Level

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[00-Board Partitioning]] | Board partitioning | 5-board rationale, connector/harness definitions, grounding strategy |

### Power Entry Board (Contactor and Relay Board)

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[07-PCB-Layout/Power-Entry/__init\|Power Entry Overview]] | Board overview | 150×120 mm, 2-layer, 4 oz Cu, NTC/relay/contactor zones, creepage analysis |

### AC-DC Board (Vienna Rectifier PFC)

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[07-PCB-Layout/AC-DC/__init\|AC-DC Overview]] | Board overview | 250×180 mm, 6-layer, BOM cross-references |
| [[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment\|AC-DC Stack-Up]] | Stack-up and layer assignment | 6-layer, 2 oz Cu, zone map (EMI → rectifier → DC bus) |
| [[07-PCB-Layout/AC-DC/02-Power Loop Analysis\|AC-DC Power Loops]] | Power loop analysis | Vienna PFC loop ≤10 nH, DC bus charge loop |
| [[07-PCB-Layout/AC-DC/03-Gate Driver Layout\|AC-DC Gate Drivers]] | Gate driver layout | STGAP2SiC × 6, Kelvin source, bootstrap |
| [[07-PCB-Layout/AC-DC/04-Thermal Layout\|AC-DC Thermal]] | Thermal layout | TO-247 heatsink, thermal vias, IPC-2152 traces |
| [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout\|AC-DC EMI]] | EMI-aware layout | CM choke placement, switching node area, filter grounding |
| [[07-PCB-Layout/AC-DC/06-Creepage and Clearance\|AC-DC Creepage]] | Creepage and clearance | AC input 530 VAC, DC bus 920 VDC, safety distances |

### DC-DC Board (LLC Resonant Converter)

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[07-PCB-Layout/DC-DC/__init\|DC-DC Overview]] | Board overview | 250×180 mm, 6-layer, resonant tank strategy |
| [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment\|DC-DC Stack-Up]] | Stack-up and layer assignment | High-current secondary, transformer cutout |
| [[07-PCB-Layout/DC-DC/02-Power Loop Analysis\|DC-DC Power Loops]] | Power loop analysis | Primary loop ≤8 nH (critical!), secondary ≤12 nH |
| [[07-PCB-Layout/DC-DC/03-Gate Driver Layout\|DC-DC Gate Drivers]] | Gate driver layout | Primary H-bridge + secondary sync rect drivers |
| [[07-PCB-Layout/DC-DC/04-Thermal Layout\|DC-DC Thermal]] | Thermal layout | Transformer thermal interface, rectifier heatsinking |
| [[07-PCB-Layout/DC-DC/05-EMI-Aware Layout\|DC-DC EMI]] | EMI-aware layout | Resonant tank shielding, output cable EMI |
| [[07-PCB-Layout/DC-DC/06-Creepage and Clearance\|DC-DC Creepage]] | Creepage and clearance | Primary-secondary 4 kV isolation, output 1000 VDC |

### Controller Board

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[07-PCB-Layout/Controller/__init\|Controller Overview]] | Board overview | 120×100 mm, 4-layer, MCU pinout |
| [[07-PCB-Layout/Controller/01-Stack-Up and Layer Assignment\|Controller Stack-Up]] | Stack-up and layer assignment | 4-layer digital-grade, solid GND plane |
| [[07-PCB-Layout/Controller/02-Signal Integrity\|Signal Integrity]] | Signal integrity | ADC routing, HRTIM signals, analog guard rings |
| [[07-PCB-Layout/Controller/03-Communication Interfaces\|Communication]] | Communication interfaces | CAN bus, OCPP/ISO 15118 PHY, connectors |
| [[07-PCB-Layout/Controller/04-Power Distribution\|Power Distribution]] | Power distribution | 3.3 V / 5 V rails, decoupling, LDO placement |
| [[07-PCB-Layout/Controller/05-EMC and Grounding\|EMC and Grounding]] | EMC and grounding | Digital/analog ground, connector filtering, ESD |

### Auxiliary PSU Board

| Doc | Title | Key Focus |
|-----|-------|-----------|
| [[07-PCB-Layout/Aux-PSU/__init\|Aux-PSU Overview]] | Board overview | 100×80 mm, output rails, isolation domains |
| [[07-PCB-Layout/Aux-PSU/01-Stack-Up and Layer Assignment\|Aux-PSU Stack-Up]] | Stack-up and layer assignment | 4-layer, isolation barrier definition |
| [[07-PCB-Layout/Aux-PSU/02-Isolated Converter Layout\|Converter Layout]] | Isolated converter layout | Flyback magnetics, primary-secondary gap |
| [[07-PCB-Layout/Aux-PSU/03-Thermal Layout\|Aux-PSU Thermal]] | Thermal layout | 5–10 W dissipation, natural convection |
| [[07-PCB-Layout/Aux-PSU/04-Output Filtering and Regulation\|Output Filtering]] | Output filtering and regulation | Post-regulator, ripple, load transient |
| [[07-PCB-Layout/Aux-PSU/05-Safety and Isolation\|Safety and Isolation]] | Safety and isolation | Reinforced insulation, IEC 62368-1 creepage |

## 4. Design Targets Summary

| Parameter | Target | Board | Rationale |
|-----------|--------|-------|-----------|
| Vienna PFC loop L_loop | ≤10 nH | AC-DC | Overshoot <170 V at 10 A/ns on 650 V devices |
| LLC primary loop L_loop (PCB) | ≤8 nH | DC-DC | Package L (~24 nH) dominates; total ≤34 nH for 1200 V margin |
| LLC secondary loop L_loop | ≤12 nH | DC-DC | Wide pours for 33 A/phase |
| Gate loop inductance | <5 nH | AC-DC, DC-DC | dV/dt immunity and Miller clamp effectiveness |
| Switching node area (PFC) | ≤1 cm² | AC-DC | CM noise ∝ dV/dt × area |
| Switching node area (LLC) | ≤1.5 cm² | DC-DC | CM noise ∝ dV/dt × area |
| EMI filter ↔ power stage gap | ≥20 mm | AC-DC | Per [[05-EMI Filter Design]] risk table |
| DC bus bus bar inductance | <5 nH | AC-DC ↔ DC-DC | Avoid additional overshoot at LLC input |
| Creepage (AC input → PE) | 10 mm | AC-DC, Power Entry | IEC 62368-1, PD2, IIIb, reinforced |
| Creepage (DC bus → PE) | 14 mm | AC-DC, DC-DC | IEC 62368-1, 920 VDC, reinforced |
| Creepage (DC output → PE) | 15 mm | DC-DC, Power Entry | IEC 62368-1, 1000 VDC, reinforced |
| Creepage (AC zone → DC zone) | ≥20 mm | Power Entry | Reinforced insulation, PCB slot between voltage domains |
| Primary-secondary isolation | 4 kV hipot | DC-DC, Aux-PSU | Reinforced insulation per IEC 62368-1 |
| Signal harness length | ≤200 mm | All | Minimize EMI pickup and propagation delay |

> [!warning] Critical Constraint
> The LLC primary half-bridge loop has only **8 V margin** to the 1200 V device rating without an RC snubber. A 10 Ω + 1 nF snubber per MOSFET is **mandatory** — see [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|DC-DC Power Loop Analysis]] for full analysis.

## 5. Cross-References to Upstream Docs

| Source | Relevance |
|--------|-----------|
| [[01-Topology Selection]] | Component BOM, switching parameters, dV/dt values |
| [[02-Magnetics Design]] | Transformer specs, resonant tank geometry |
| [[04-Thermal Budget]] | Loss allocation per board, heatsink Rth, enclosure zoning |
| [[05-EMI Filter Design]] | CM/DM noise sources, Cdh values, 20 mm separation rule |
| [[06-Firmware Architecture]] | HRTIM dead-time settings, PWM frequencies, control signal mapping |
| [[08-Power-On Sequence and Inrush Management]] | NTC, relay, contactor specs; startup sequence timing |
| [[10-Mechanical Integration]] | Enclosure, 5-board mounting, bus bar routing, airflow path |
| [[SiC Device Thermal Parameters]] | Package types, Rth, HiP247-4 pinout, gate driver thermal |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
