# 30 kW Power Delivery Unit (PDU) — Design Documentation

Design documentation for a **30 kW DC fast-charging power module** intended for EV charging infrastructure. The module converts 3-phase AC to adjustable high-voltage DC, and 5 units stack via CAN bus to deliver 150 kW.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Input | 3-phase 260–530 VAC, up to 60 A, PF ≥ 0.99 |
| Output | 150–1000 VDC, 0–100 A, 30 kW constant power |
| Efficiency | > 96% peak (SiC-based, targeting > 98%) |
| Topology | Vienna Rectifier PFC + 3-phase interleaved LLC DC-DC |
| Controller | STM32G474RE (170 MHz, HRTIM) |
| Stacking | 5 modules via CAN bus → 150 kW |
| Form factor | ~455 × 300 × 94 mm, fan-cooled, < 17 kg |
| Standards | IEC 61851-23, IEC 62368-1, UL 2202, CE, OCPP 1.6, ISO 15118 |

## Multi-Board Architecture

The PDU is split into 5 separate PCBs interconnected by power bus bars and signal harnesses:

| Board | Function | Layers | Size |
|-------|----------|--------|------|
| **Power Entry** | AC input protection (NTC inrush, bypass relays), DC output contactor | 2 | 150 × 120 mm |
| **AC-DC** | Vienna Rectifier PFC — EMI filter, 3-phase rectification, DC bus caps | 6 | 250 × 180 mm |
| **DC-DC** | LLC Resonant converter — primary bridge, transformers, secondary rectifier | 6 | 250 × 180 mm |
| **Controller** | STM32G474RE, CAN bus, analog conditioning, OCPP/ISO 15118 | 4 | 120 × 100 mm |
| **Aux PSU** | Isolated supplies — gate drive (+18 V/−5 V), logic (3.3/5 V), fan (12 V) | 4 | 100 × 80 mm |

## Repository Structure

```
pdu-docs/
├── __init.md                          # Project definition and specifications
├── CLAUDE.md                          # Claude Code workspace guidance
│
├── docs/                              # Design documentation
│   ├── 01-Topology Selection.md       # Vienna PFC + 3-phase interleaved LLC
│   ├── 02-Magnetics Design.md        # LLC resonant tank, transformer, inductor
│   ├── 03-LLC Gain Curve Verification.md  # FHA + ngspice simulation
│   ├── 04-Thermal Budget.md          # Loss breakdown, junction temps, cooling
│   ├── 05-EMI Filter Design.md       # EN 55032 Class B, surge, inrush
│   ├── 06-Firmware Architecture.md   # STM32G474 HRTIM, ADC, control loops
│   ├── 06-Firmware-Design/           # Firmware implementation details (8 docs)
│   │   ├── __init.md                 # Index and reading order
│   │   ├── 01-Application State Machine.md
│   │   ├── 02-Power-On Sequence and Ramp Control.md
│   │   ├── 03-Fault State Machine and Recovery.md
│   │   ├── 04-LLC Burst Mode.md
│   │   ├── 05-CAN Master and Module Stacking.md
│   │   ├── 06-ADC Pipeline and DMA Configuration.md
│   │   └── 07-Neutral Point Balancing.md
│   ├── 07-BOM and Cost Analysis.md   # Per-module BOM, cost @ 100/500 qty
│   ├── 08-Power-On Sequence and Inrush Management.md
│   ├── 09-Protection and Safety.md   # OVP/OCP/OTP, insulation, hipot,compliance
│   ├── 10-Mechanical Integration.md  # Enclosure,heatsink,fans,bus bars,assembly
│   │
│   └── 07-PCB-Layout/                # Multi-board PCB layout documentation
│       ├── __init.md                  # 5-board overview and design targets
│       ├── 00-Board Partitioning.md   # Inter-board interfaces, connectors, grounding
│       ├── AC-DC/                     # Vienna PFC board (7 docs)
│       │   ├── __init.md
│       │   ├── 01-Stack-Up and Layer Assignment.md
│       │   ├── 02-Power Loop Analysis.md
│       │   ├── 03-Gate Driver Layout.md
│       │   ├── 04-Thermal Layout.md
│       │   ├── 05-EMI-Aware Layout.md
│       │   └── 06-Creepage and Clearance.md
│       ├── DC-DC/                     # LLC converter board (7 docs)
│       │   ├── __init.md
│       │   ├── 01-Stack-Up and Layer Assignment.md
│       │   ├── 02-Power Loop Analysis.md
│       │   ├── 03-Gate Driver Layout.md
│       │   ├── 04-Thermal Layout.md
│       │   ├── 05-EMI-Aware Layout.md
│       │   └── 06-Creepage and Clearance.md
│       ├── Controller/                # Digital control board (6 docs)
│       │   ├── __init.md
│       │   ├── 01-Stack-Up and Layer Assignment.md
│       │   ├── 02-Signal Integrity.md
│       │   ├── 03-Communication Interfaces.md
│       │   ├── 04-Power Distribution.md
│       │   └── 05-EMC and Grounding.md
│       ├── Aux-PSU/                   # Auxiliary power supply board (6 docs)
│       │   ├── __init.md
│       │   ├── 01-Stack-Up and Layer Assignment.md
│       │   ├── 02-Isolated Converter Layout.md
│       │   ├── 03-Thermal Layout.md
│       │   ├── 04-Output Filtering and Regulation.md
│       │   └── 05-Safety and Isolation.md
│       └── Power-Entry/               # Contactor and relay board (1 doc)
│           └── __init.md
│
│   └── 12-Project-Management/            # Consolidated project management
│       ├── __init.md                     # Epic overview, Gantt, milestones, gate reviews
│       ├── EP-01 Design Review and Procurement.md    (18 stories)
│       ├── EP-02 Rev A Prototype Build.md            (14 stories)
│       ├── EP-03 Firmware Bring-Up.md                (16 stories)
│       ├── EP-04 System Integration.md               (15 stories)
│       ├── EP-05 Rev B Prototype.md                  (12 stories)
│       ├── EP-06 Firmware Maturation.md              (14 stories)
│       ├── EP-07 Certification Prep.md               (13 stories)
│       ├── EP-08 Pre-Production Validation.md        (11 stories)
│       ├── EP-09 Production Release.md               (10 stories)
│       ├── Budget Estimate.md            # $390k–$615k detailed budget
│       ├── Risk Register.md              # 21 risks, 5×5 scoring matrix
│       └── Commissioning Procedure.md    # 7-stage field deployment
│
├── research/                          # Research notes and trade studies
│   ├── 3-Phase PFC Topology Selection.md
│   ├── DC-DC Topology Trade Study.md
│   ├── Commercial Reference Designs Survey.md
│   ├── EMC-EMI Limits and Filter Design.md
│   └── SiC Device Thermal Parameters.md
│
└── sim/                               # Simulation files
    ├── llc_fha_gain.py                # First Harmonic Approximation gain model
    ├── llc_ngspice_sweep.py           # ngspice parameter sweep automation
    ├── llc_halfbridge.cir             # SPICE netlist — LLC half-bridge
    ├── llc_sweep.cir                  # SPICE netlist — frequency sweep
    ├── llc_gain_curves.png            # FHA gain curves output
    ├── llc_spice_vs_fha.png           # SPICE vs FHA comparison
    └── llc_zvs_detail.png             # ZVS boundary detail plot
```

## Documentation Overview

### Design Documents (`docs/`)

| # | Document | Status |
|---|----------|--------|
| 01 | **Topology Selection** — Vienna PFC + 3-phase interleaved LLC | Approved |
| 02 | **Magnetics Design** — LLC resonant tank (Lr, Lm, Cr), transformer | Draft |
| 03 | **LLC Gain Curve Verification** — FHA model + ngspice validation | Draft |
| 04 | **Thermal Budget** — System losses, junction temperatures, cooling | Draft |
| 05 | **EMI Filter Design** — EN 55032 Class B, CM/DM filtering | Draft |
| 06 | **Firmware Architecture** — STM32G474RE HRTIM, control loops, CAN | Draft |
| 06 | **Firmware Design** — Implementation details: state machine, ramps, faults, burst mode, CAN master, ADC/DMA, NP balance (8 sub-documents) | Draft |
| 07 | **BOM and Cost Analysis** — Component selection, cost at volume | Draft |
| 07 | **PCB Layout** — Multi-board layout across 5 PCBs (29 sub-documents) | Draft |
| 08 | **Power-On Sequence** — Startup/shutdown, inrush, pre-charge | Draft |
| 09 | **Protection and Safety** — OVP/OCP/OTP, insulation, hipot, compliance | Draft |
| 10 | **Mechanical Integration** — Enclosure, heatsink, fans, bus bars | Draft |
| 12 | **Project Management** — 9 epics (123 stories), Gantt timeline, milestones, gate reviews, budget estimate, risk register, commissioning procedure (13 documents) | Draft |

### PCB Layout (`docs/07-PCB-Layout/`)

The PCB layout section contains **29 documents** organized by board:

- **Power Entry Board** (1 doc) — 2-layer, NTC inrush limiting, bypass relays, DC output contactor, AC/DC zone separation
- **AC-DC Board** (7 docs) — 6-layer, Vienna PFC power loops (≤10 nH), SiC gate drivers, 530 VAC creepage
- **DC-DC Board** (7 docs) — 6-layer, LLC primary loop (≤8 nH, critical margin), 4 kV primary-secondary isolation
- **Controller Board** (6 docs) — 4-layer digital, signal integrity, CAN/OCPP/ISO 15118 interfaces
- **Aux PSU Board** (6 docs) — 4-layer, flyback converter, reinforced isolation from 920 VDC bus

### Research Notes (`research/`)

Trade studies and component evaluations supporting the design decisions:
- PFC topology comparison (Vienna vs B6, Swiss, two-level VSI)
- DC-DC topology comparison (LLC vs DAB, PSFB, CLLC, SRC)
- Commercial reference design survey (Wolfspeed, ST, Infineon, onsemi, TI, ADI)
- EMC/EMI limits and filter design methodology
- SiC MOSFET thermal characterization and package comparison

### Simulations (`sim/`)

Python scripts and SPICE netlists for LLC resonant converter verification:
- First Harmonic Approximation (FHA) gain model
- ngspice transient simulation and frequency sweep
- Gain curve validation (FHA vs SPICE)
- ZVS boundary analysis

## Viewing These Documents

This repository is designed as an [Obsidian](https://obsidian.md/) vault. For the best experience:

1. Clone the repo
2. Open the folder as a vault in Obsidian
3. Navigate using `[[wiki links]]` — all internal links resolve within the vault

The documents are also readable as standard Markdown in any viewer (GitHub, VS Code, etc.), though `[[wiki links]]` will not be clickable outside Obsidian.

## Author

**Manas Pradhan**

## License

All rights reserved JouleWorX LLP 2025. This documentation is proprietary.
