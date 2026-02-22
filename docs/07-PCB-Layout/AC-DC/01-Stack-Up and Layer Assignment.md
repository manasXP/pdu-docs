---
tags: [pdu, pcb-layout, vienna-pfc, stack-up, ipc-2152, impedance]
created: 2026-02-22
status: draft
---

# 01 — Stack-Up and Layer Assignment

## Purpose

This document defines the 6-layer PCB stack-up for the Vienna Rectifier PFC board, optimized for low power-loop inductance, effective EMI shielding, and adequate thermal performance. The stack-up is the single most critical layout decision — it determines the achievable loop inductance, EMC performance, and thermal capacity of every copper pour on the board.

## Stack-Up Definition

### Layer Table

| Layer | Name | Cu Weight | Thickness (µm) | Function | Notes |
|-------|------|-----------|-----------------|----------|-------|
| L1 | TOP_PWR | 2 oz | 70 | Top power plane, component pads | AC input pours, switching node, drain/source pads |
| — | Prepreg 1 | — | 100 (target) | L1–L2 dielectric | Low thickness for tight L1-L2 coupling |
| L2 | GND | 2 oz | 70 | Continuous ground plane | **Must remain unbroken** — primary return path |
| — | Core 1 | — | 360 | L2–L3 dielectric | Standard FR-4 core |
| L3 | SIG_1 | 1 oz | 35 | Signal routing | Gate drive signals, analog sensing, digital control |
| — | Core 2 | — | 360 | L3–L4 dielectric | Standard FR-4 core |
| L4 | SIG_PWR | 1 oz | 35 | Signal + power return | Low-current power returns, auxiliary supplies |
| — | Core 3 | — | 360 | L4–L5 dielectric | Standard FR-4 core |
| L5 | PWR_PLANE | 2 oz | 70 | Inner power plane | DC bus distribution, AC input return |
| — | Prepreg 2 | — | 100 (target) | L5–L6 dielectric | Low thickness for tight L5-L6 coupling |
| L6 | BOT_PWR | 2 oz | 70 | Bottom power plane | DC bus return, component pads |

**Total board thickness:** ~1.6 mm (adjust prepreg/core to hit target)

> [!tip] Why 2 oz on L1/L2/L5/L6?
> At 60 A AC input current, 1 oz copper requires impractically wide traces (>50 mm). The 2 oz outer layers halve the required trace width and significantly reduce I²R losses. The 2 oz L2 ground plane provides a low-impedance return path that is critical for both power loop performance and EMI control.

### Prepreg Selection — L1 to L2 Gap

The L1-to-L2 prepreg thickness is the most critical dimension in the stack-up. A thinner dielectric between L1 (power) and L2 (ground) reduces power loop inductance because:

$$L_{loop} \propto \frac{\mu_0 \cdot d}{w}$$

where $d$ is the dielectric thickness and $w$ is the overlap width between the forward and return current paths.

| Prepreg thickness | Loop inductance factor | Availability | Notes |
|-------------------|----------------------|--------------|-------|
| 50 µm | 0.5× baseline | Limited, expensive | Best performance but fragile |
| 75 µm | 0.75× baseline | Available from major fabs | Good compromise |
| 100 µm | 1.0× baseline | Standard | Recommended baseline |
| 200 µm | 2.0× baseline | Standard | Too thick — avoid |

**Target: 75–100 µm prepreg for L1-L2 and L5-L6 gaps.**

> [!warning] Fabrication Constraint
> Confirm the target prepreg thickness with your PCB fabricator before finalizing the design. Not all fabricators can reliably produce <100 µm prepreg with 2 oz copper on both sides. Request a stack-up review from the fab house and document the agreed-upon values.

### Impedance Considerations

While this is primarily a power board, controlled impedance is needed for:

| Signal | Target Z0 | Layer | Width (1 oz, 100µm prepreg) | Notes |
|--------|-----------|-------|-----------------------------|-------|
| Gate drive (STGAP2SiC output) | 50 Ω (target) | L3 | ~0.18 mm | Short runs, matched Rg dominates |
| CAN bus differential | 120 Ω differential | L3 | ~0.15 mm, 0.2 mm gap | If CAN transceiver is on this board |
| Current sense analog | Not controlled | L3 | 0.2 mm minimum | Guard traces recommended |

## Zone Map

The board is divided into four functional zones arranged along the primary axis (250 mm dimension). Airflow moves left-to-right.

```
        ←— 250 mm —————————————————————————————————→
   ┌──────────┬────────────────────┬───────────┬─────────┐  ↑
   │          │                    │           │         │  │
   │  Zone A  │      Zone B        │  Zone C   │ Zone D  │  │
   │  EMI     │   Vienna PFC       │  DC Bus   │ Conn &  │ 180
   │  Filter  │   Power Stage      │  Caps     │ Aux     │  mm
   │          │                    │           │         │  │
   │  ~50 mm  │    ~100 mm         │  ~50 mm   │ ~50 mm  │  │
   │          │                    │           │         │  ↓
   └──────────┴────────────────────┴───────────┴─────────┘
        ↑              ↑               ↑           ↑
   AC input       SiC MOSFETs     Bulk caps    DC output
   connector      + gate drivers  + film caps  connector
```

### Zone A — EMI Filter (~50 mm)

**Layer assignments:**
- **L1:** X-capacitor pads, CM choke pads, inrush relay pads
- **L2:** Continuous GND — serves as Y-capacitor return and shield
- **L3:** Inrush control signal routing
- **L5/L6:** AC input power return paths

**Key placement rules:**
- AC input connector at the board edge (left side)
- CM choke immediately after the connector
- X-caps between CM choke stages
- Y-caps from phase to L2 GND plane, shortest possible path
- Separation from Zone B: **≥20 mm clear zone** with double stitching via fence

> [!warning] EMI Filter Isolation
> The EMI filter zone must be physically and electrically isolated from the power stage zone. Conducted emissions from the switching node will couple back into the filter and degrade attenuation if the zones share return paths or have insufficient separation. See [[05-EMI-Aware Layout]] for the stitching via fence specification.

### Zone B — Vienna Rectifier Power Stage (~100 mm)

This is the most layout-critical zone on the board. It contains:

**L1 (top):**
- SiC MOSFET drain pads (TO-247 footprints)
- Switching node copper (area ≤1 cm² per phase)
- Snubber capacitor pads (C_snub1, C_snub2)
- Boost inductor connection pads

**L2 (GND):**
- Continuous ground pour — power loop return path
- No cuts, no routing, no thermal relief in this zone

**L3 (signal):**
- Gate driver to MOSFET gate traces
- Current sense resistor routing
- Temperature sensor routing
- STGAP2SiC SPI/control bus (if daisy-chained)

**L4 (signal/power return):**
- Gate driver auxiliary supply distribution
- Low-current power returns

**L5 (power plane):**
- DC bus positive distribution
- AC input phase routing (where needed for layer transitions)

**L6 (bottom):**
- DC bus negative / power return
- Snubber capacitor return pads (where bottom-side placement is used)
- Additional thermal copper for MOSFET tab cooling

**MOSFET placement pattern (per phase):**

```
         Phase A (repeated for B, C)
    ┌──────────────────────────────────┐
    │   C_snub1 ×4    C_snub1 ×4       │
    │   ┌──────┐      ┌──────┐         │
    │   │ Q_hi │      │ Q_lo │         │
    │   │TO-247│      │TO-247│         │
    │   └──────┘      └──────┘         │
    │   C_snub2 ×1    C_snub2 ×1       │
    │        ↕ <10mm                   │
    │   ┌──────────────────────┐       │
    │   │   C_bus (shared)     │       │
    │   └──────────────────────┘       │
    └──────────────────────────────────┘
```

### Zone C — DC Bus Capacitors (~50 mm)

**Layer assignments:**
- **L1:** Positive bus bar pour (2 oz)
- **L2:** Continuous GND
- **L5:** Negative bus bar pour or additional positive
- **L6:** Negative bus bar pour (2 oz)

**Components:**
- 4–6 × 470 µF 450V electrolytic capacitors (series pairs for 900V rating)
- Additional film capacitors for high-frequency decoupling
- Bleeder/balancing resistors across each series cap

### Zone D — Connectors and Auxiliary (~50 mm)

- DC output power connector (to [[07-PCB-Layout/DC-DC/__init|DC-DC]] board or bus bar)
- AC input connector (from EMI filter if external, or from Zone A)
- Auxiliary power connector (12V/5V for gate drivers, control)
- CAN bus connector (for module stacking communication)
- Signal/interlock connectors

## IPC-2152 Trace Width Calculations

Current-carrying traces must be sized per IPC-2152 for the required current and allowable temperature rise. The following table assumes 2 oz (70 µm) external copper and a 30°C temperature rise above ambient.

### External Layers (L1, L6) — 2 oz Copper

| Current (A) | Trace Width (mm) | Recommended Implementation | Application |
|-------------|-------------------|---------------------------|-------------|
| 60 | 30 | Copper pour / bus bar zone | AC input phases |
| 40 | 20 | Copper pour | DC bus ± |
| 20 | 8 | Wide trace or pour | Boost inductor feed |
| 10 | 3 | Trace | Auxiliary power |
| 5 | 1.2 | Trace | Gate driver supply bus |

### Internal Layers (L5) — 2 oz Copper

Internal layers have worse thermal dissipation. Apply a derating factor of approximately 0.5× compared to external layers.

| Current (A) | Trace Width (mm) | Notes |
|-------------|-------------------|-------|
| 40 | 40 | Full-width pour recommended |
| 20 | 16 | Wide pour |
| 10 | 6 | Pour or wide trace |

> [!tip] Use Copper Pours, Not Traces
> At 40–60 A, discrete traces are impractical. Use copper pour zones (polygon fills) that span the full available width in each zone. The "trace width" values above represent the **minimum** width — always use the maximum available width to reduce resistive losses and improve thermal performance.

### Internal Layers (L3, L4) — 1 oz Copper

These layers carry only signal and low-current auxiliary power. Maximum recommended current on L3/L4 is 2 A for power and <100 mA for signals.

| Current (A) | Trace Width (mm) | Notes |
|-------------|-------------------|-------|
| 2 | 1.5 | Auxiliary power distribution |
| 0.5 | 0.3 | Signal traces |
| 0.1 | 0.15 | Gate drive, analog sense |

## L2 Ground Plane Rules

The L2 ground plane is the most critical element of the stack-up. It serves three functions simultaneously:

1. **Power loop return path** — The AC input current and switching current return through L2 directly beneath the L1 power pours, forming a low-inductance loop.
2. **EMI shield** — L2 shields the inner signal layers (L3, L4) from the high dV/dt switching noise on L1.
3. **Signal reference** — All analog current sense signals and gate drive signals reference L2 for their return path.

### Mandatory Rules for L2

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| No routing on L2 | Zero traces | Any trace creates a slot that forces return current to detour |
| No splits | Single contiguous pour | Splits create slot antennas and increase loop inductance |
| No thermal relief on power vias | Direct connect | Thermal relief pads on L2 add inductance to the return path |
| Via stitching at zone boundaries | 0.3 mm vias, 2 mm pitch | Provides low-impedance connection across zones |
| Full coverage | >95% copper fill | Maximize continuous return path area |

> [!warning] L2 Integrity Check
> Before releasing the layout for fabrication, perform a dedicated L2 integrity review. Visually inspect the ground plane for any unintended cuts, narrow necks, or missing connections. Use the EDA tool's copper connectivity check to verify L2 is a single net with no islands.

## Via Strategy

### Power Vias (L1 ↔ L5/L6)

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.5 mm |
| Pad diameter | 1.0 mm |
| Finished hole | 0.4 mm |
| Current per via | ~1.5 A (IPC-2152, 30°C rise) |
| Array for 40A bus | 27 vias minimum (use 30+) |

Power transitions between L1 and L5/L6 must use via arrays. Place vias in a grid pattern within the copper pour zone.

### Signal Vias (L1/L6 ↔ L3)

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.3 mm |
| Pad diameter | 0.6 mm |
| Finished hole | 0.2 mm |
| Usage | Gate drive signals, analog sense, digital control |

### Thermal Vias

See [[04-Thermal Layout]] for thermal via arrays under MOSFET pads and gate driver packages.

### Stitching Vias

| Parameter | Value |
|-----------|-------|
| Drill diameter | 0.3 mm |
| Pad diameter | 0.6 mm |
| Pitch | 2 mm (single fence), 2 mm staggered (double fence) |
| Usage | Zone boundaries, board edges, EMI containment |

See [[05-EMI-Aware Layout]] for stitching via fence placement rules.

## Design for Manufacturing (DFM) Notes

| Parameter | Value | Standard |
|-----------|-------|----------|
| Minimum trace width (signal) | 0.15 mm | IPC Class 2 |
| Minimum trace spacing (signal) | 0.15 mm | IPC Class 2 |
| Minimum via-to-via spacing | 0.5 mm | Fab-dependent |
| Minimum annular ring | 0.125 mm | IPC Class 2 |
| Board thickness tolerance | ±10% | IPC-6012 Class 2 |
| Copper weight tolerance | ±10% | IPC-6012 Class 2 |
| Minimum solder mask dam | 0.1 mm | Fab-dependent |
| Surface finish | ENIG | For SiC pad soldering reliability |
| Solder mask color | Green (standard) | — |
| Silkscreen | White, both sides | Component references + zone labels |

> [!tip] Fabricator Communication
> Order a stack-up review from the PCB fabricator before finalizing the design. Provide:
> 1. Target prepreg thicknesses (75–100 µm for L1-L2 and L5-L6)
> 2. Copper weights per layer
> 3. Controlled impedance requirements (if any on L3)
> 4. Total board thickness target (1.6 mm)
>
> The fabricator will provide actual achievable values and adjust core/prepreg selections.

## Cross-References

- [[__init]] — Board overview and component summary
- [[02-Power Loop Analysis]] — How the stack-up enables low-inductance power loops
- [[04-Thermal Layout]] — Thermal via strategy and copper pour sizing
- [[05-EMI-Aware Layout]] — Stitching via fences and L2 ground plane integrity
- [[06-Creepage and Clearance]] — Internal layer clearances per IPC-2221B

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: 6-layer stack-up, zone map, IPC-2152 tables |
