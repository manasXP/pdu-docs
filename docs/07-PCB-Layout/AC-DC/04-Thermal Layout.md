---
tags: [pdu, pcb-layout, vienna-pfc, thermal, heatsink, ipc-2152, tim]
created: 2026-02-22
status: draft
---

# 04 — Thermal Layout

## 1. Purpose

This document specifies the thermal design aspects of the Vienna Rectifier PFC board layout, including MOSFET heatsink mounting, thermal interface materials, thermal via arrays, copper pour sizing for current capacity, airflow path optimization, and gate driver thermal management.

At 30 kW with >96% efficiency, the board dissipates up to **1200 W** of heat (at 96%). With SiC-based designs at >98% efficiency, dissipation drops to ~600 W, but this is still substantial and requires careful thermal management to keep junction temperatures within safe operating limits.

## 2. Thermal Budget Overview

### Power Dissipation Breakdown (Per Phase, 10 kW)

| Component | Loss Mechanism | Estimated Loss (W) | Notes |
|-----------|---------------|-------------------|-------|
| SiC MOSFET Q_hi | Conduction + switching | 30–50 | Rdson × Irms² + switching loss |
| SiC MOSFET Q_lo | Conduction + switching | 30–50 | Same as Q_hi |
| Boost diode | Conduction (Vf × Iavg) | 20–30 | SiC Schottky: Vf ≈ 1.5V |
| Boost inductor | Core + copper loss | 40–60 | External or board-mounted |
| Snubber/bus caps | ESR loss | 5–10 | Ripple current × ESR |
| Gate driver | Gate charge + quiescent | 0.3 | Per [[07-PCB-Layout/AC-DC/03-Gate Driver Layout]] |
| PCB copper | I²R loss | 10–20 | Depends on pour width/length |
| **Total per phase** | | **135–220 W** | |
| **Total 3-phase** | | **400–660 W** | Consistent with 98–96% efficiency |

### Temperature Targets

| Component | Max Junction/Case Temp | Target Operating Temp | Notes |
|-----------|----------------------|---------------------|-------|
| SiC MOSFET | 175°C (Tj_max) | ≤125°C | Derating per [[SiC Device Thermal Parameters]] |
| SiC Schottky diode | 175°C | ≤125°C | Same heatsink as MOSFETs |
| STGAP2SiC driver | 150°C (Tj_max) | ≤105°C | Board-cooled, no heatsink |
| Electrolytic capacitors | 105°C (case) | ≤85°C | Lifetime doubles per 10°C reduction |
| FR-4 PCB | 170°C (Tg) | ≤100°C locally | Near MOSFET mounting area |

## 3. TO-247 Heatsink Mounting

### Mechanical Specification

The 6 SiC MOSFETs (and 6 boost diodes, if discrete TO-247) are mounted in TO-247 / HiP247 packages with a shared heatsink. The heatsink is a separate mechanical assembly that attaches through the PCB.

| Parameter | Value | Notes |
|-----------|-------|-------|
| Package | TO-247-4 (HiP247 for Kelvin source) | Tab is drain (electrically hot) |
| Mounting hardware | M3 screws, spring washers | Per manufacturer recommendation |
| Torque | **0.4–0.5 N·m** | Critical: under-torque increases Rth, over-torque cracks die |
| TIM | Bergquist GP3000S (or equivalent) | See TIM section below |
| Heatsink material | Extruded aluminum, anodized | Black anodize for radiation |
| Heatsink-to-board gap | 0–1 mm (package sits flush or slightly raised) | Depends on lead forming |

> [!warning] TO-247 Tab is Electrically Hot
> The TO-247 metal tab is connected to the drain of the SiC MOSFET. The drain operates at the switching node voltage (0 to 920 VDC). The thermal interface material must provide **electrical isolation** between the tab and the heatsink. The heatsink is typically connected to PE (protective earth) or floating — in either case, the TIM must withstand the full bus voltage plus transients.

### Thermal Interface Material — Bergquist GP3000S

| Parameter | Value | Notes |
|-----------|-------|-------|
| Type | Gap pad (compressible) | Conforms to surface irregularities |
| Thermal conductivity | 3.0 W/m·K | |
| Thickness | 0.5 mm (compressed) | At 0.4–0.5 N·m mounting torque |
| Thermal resistance (per TO-247 tab) | **Rth_cs ≈ 0.12°C/W** | Based on tab area ~1.5 cm² |
| Dielectric breakdown | >5 kV AC | Adequate for 920V bus + margin |
| Operating temperature | −40°C to +200°C | |
| Hardness | Shore 00-55 (compressed) | Soft enough to conform |

### Thermal Stack (Junction to Ambient)

For one SiC MOSFET at maximum dissipation:

| Element | Rth (°C/W) | Notes |
|---------|-----------|-------|
| Junction to case (Rth_jc) | 0.3–0.6 | From SiC MOSFET datasheet |
| Case to sink (Rth_cs) | 0.12 | Bergquist GP3000S |
| Sink to ambient (Rth_sa) | 0.5–1.5 | Depends on heatsink + airflow |
| **Total Rth_ja** | **0.92–2.22** | |

At 50 W dissipation per MOSFET and 55°C ambient:

$$T_j = T_{amb} + P_{diss} \times R_{th\_ja} = 55 + 50 \times 1.5 = 130°C$$

This is within the 175°C absolute max but above the 125°C operating target. **The heatsink Rth_sa must be ≤1.0°C/W** with forced-air cooling to meet the target.

> [!tip] Heatsink Selection Drives Layout
> The heatsink dimensions and mounting hole pattern directly affect the PCB layout. Select the heatsink early in the design process and incorporate its footprint into the PCB layout from the beginning. The heatsink mounting holes must align with the PCB mounting holes and maintain creepage from drain copper to PE. See [[07-PCB-Layout/AC-DC/06-Creepage and Clearance]].

### PCB Mounting Pad Design

The TO-247 package has three elements that contact the PCB:

1. **Lead pins** (3 or 4 pins) — soldered into through-hole or surface-mount pads
2. **Tab/heatsink surface** — faces away from the PCB (toward the heatsink)
3. **Mounting screw hole** — passes through the tab and PCB into the heatsink

**PCB mounting hole for M3 screw:**

| Parameter | Value |
|-----------|-------|
| Drill diameter | 3.2 mm (for M3 screw clearance) |
| Pad diameter | 6.0 mm (annular ring for structural support) |
| Copper keepout around hole | Per creepage requirements — see [[07-PCB-Layout/AC-DC/06-Creepage and Clearance]] |
| Plating | Non-plated (NPTH) if heatsink is PE-connected; plated if drain-connected |

> [!warning] Mounting Hole Creepage
> The M3 mounting hole passes through the PCB in close proximity to the drain copper pad. The drain is at switching node voltage (up to 920V). If the heatsink is connected to PE or chassis ground, the creepage from drain copper to the mounting hole must meet the DC bus creepage requirement (**14 mm** per [[07-PCB-Layout/AC-DC/06-Creepage and Clearance]]). This often requires a large copper keepout zone around the mounting hole and may necessitate a PCB slot to increase the effective creepage path.

## 4. Thermal Via Arrays

Thermal vias conduct heat from the top copper layer (L1) through the PCB stack-up to inner and bottom layers, increasing the effective thermal conduction area.

### Under MOSFET Pads

For the TO-247 drain pad on L1, a thermal via array conducts heat to L5/L6:

| Parameter | Value |
|-----------|-------|
| Via drill diameter | 0.3 mm |
| Via pad diameter | 0.6 mm |
| Via pitch | 1.27 mm (50 mil) |
| Array size | 3×3 minimum (9 vias) per MOSFET pad |
| Via fill | Plugged and plated (preferred) or tented |
| Thermal relief | **None — direct connect on all layers** |
| Estimated Rth per via | ~70°C/W (for 1.6 mm board, 0.3 mm drill) |
| Array Rth (9 vias parallel) | ~7.8°C/W |

```
    Drain pad (L1) with thermal via array:

    ┌───────────────────────┐
    │  ○  ○  ○              │  ○ = thermal via (0.3mm drill)
    │  ○  ○  ○   TO-247     │  Pitch: 1.27mm
    │  ○  ○  ○   drain pad  │  3×3 array minimum
    │                       │
    └───────────────────────┘
```

> [!warning] No Thermal Relief on Power Pads
> Thermal relief pads (spoke-pattern connections) on power pads are **forbidden** on this board. Thermal relief adds resistance and inductance to the power path and reduces thermal conduction. All power pad connections to copper pours and planes must use **direct (solid) connections** on all layers.
>
> This applies to:
> - MOSFET drain/source pads
> - Snubber capacitor pads
> - DC bus capacitor pads
> - Power connector pads
> - Thermal vias under MOSFET pads
>
> Thermal relief is only acceptable on signal-level pads where soldering by hand may be required during prototyping.

### Via Fill Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Open (unfilled) | Cheapest | Solder wicking, uneven surface | Not recommended for MOSFET pads |
| Tented (solder mask covered) | Low cost, prevents solder wicking | Mask may crack, trapped air | Acceptable for prototypes |
| Plugged + plated (VIPPO) | Flat surface, best thermal, allows SMD on pad | Most expensive | **Recommended for production** |
| Filled with epoxy | Moderate cost, flat surface | Lower thermal conductivity than copper fill | Acceptable alternative |

## 5. Gate Driver Thermal Management

### STGAP2SiC Thermal Design

The STGAP2SiC in SO-8W package dissipates ~0.33 W per driver. With a typical SO-8W Rth_ja of 120–150°C/W, the temperature rise at 0.33 W would be 40–50°C — acceptable but leaves little margin at 55°C ambient.

To improve thermal performance, add a copper pour and thermal via array on the PCB beneath each driver:

| Parameter | Value |
|-----------|-------|
| Copper pour (L1, top) | 15 mm × 15 mm centered on the driver exposed pad |
| Copper pour (L6, bottom) | 15 mm × 15 mm, connected via thermal vias |
| Thermal via array | 3×3 grid (9 vias), 0.3 mm drill, 1.27 mm pitch |
| Connection | Driver exposed pad (if present) or thermal pad on L1 |
| Target Rth_ja with pour + vias | **60–80°C/W** |

Temperature rise with improved thermal design:

$$\Delta T = P_{diss} \times R_{th\_ja} = 0.33 \text{ W} \times 70 \text{ °C/W} = 23°C$$

At 55°C ambient: Tj = 55 + 23 = **78°C** — well within the 150°C maximum.

> [!tip] Copper Pour Must Be on Kelvin Source Net
> The copper pour beneath the STGAP2SiC (secondary side) is connected to the driver's exposed pad, which is typically the secondary-side ground (Kelvin source net for that phase). Ensure this pour does not connect to a different ground net or to the primary-side ground. Check the STGAP2SiC datasheet for the exposed pad connection.

### Driver Thermal Pour Layout

```
    L1 (top):
    ┌─────────────────────────────┐
    │     15mm × 15mm Cu pour     │
    │     (Kelvin source net)     │
    │   ┌─────────────────┐       │
    │   │   STGAP2SiC     │       │
    │   │   (SO-8W)       │       │
    │   └─────────────────┘       │
    │   ○ ○ ○  thermal vias (9×)  │
    │   ○ ○ ○  0.3mm drill        │
    │   ○ ○ ○  1.27mm pitch       │
    └─────────────────────────────┘

    L6 (bottom):
    ┌─────────────────────────────┐
    │     15mm × 15mm Cu pour     │
    │     (Kelvin source net)     │
    │   ○ ○ ○  matching vias      │
    │   ○ ○ ○                     │
    │   ○ ○ ○                     │
    └─────────────────────────────┘
```

## 6. IPC-2152 Bus Trace / Pour Sizing

### AC Input Traces (60 A per phase)

The AC input current flows from the input connector (Zone A/D) through the EMI filter (Zone A) to the boost inductors and then to the MOSFETs (Zone B). Each phase carries up to 60 A RMS.

| Parameter | Value |
|-----------|-------|
| Current | 60 A RMS |
| Copper weight | 2 oz (L1, L6) |
| Temperature rise limit | 30°C |
| Required trace/pour width | **≥30 mm** (per IPC-2152) |
| Implementation | Full-width copper pour in each phase zone |
| Layers used | L1 + L6 in parallel where possible |
| Via arrays between L1 and L6 | 40+ vias (0.5 mm drill) per transition |

> [!tip] Parallel Layers for Current Sharing
> Using L1 and L6 in parallel for the AC input phases effectively doubles the copper cross-section. With 30 mm pours on both L1 and L6 connected by via arrays, the effective cross-section is equivalent to a 30 mm, 4 oz copper trace. This reduces temperature rise and I²R losses. Ensure the via arrays are distributed along the pour length, not just at the ends.

### DC Bus Traces (40 A)

The DC bus current flows from the MOSFETs through the snubber array to the bulk capacitors and then to the output connector.

| Parameter | Value |
|-----------|-------|
| Current | 40 A (DC + ripple) |
| Copper weight | 2 oz (L1, L5, L6) |
| Temperature rise limit | 30°C |
| Required trace/pour width | **≥20 mm** (per IPC-2152) |
| Implementation | Copper pour zones on L1 and L5/L6 |
| Positive bus | L1 (top) pour, extending from snubbers through Zone C to connector |
| Negative bus | L5/L6 pour, extending from MOSFET sources through Zone C |

### Internal Layer (L5) DC Bus Distribution

| Parameter | Value |
|-----------|-------|
| Current | 40 A |
| Copper weight | 2 oz |
| Derating factor | 0.5× (internal layer) |
| Required pour width | **≥40 mm** |
| Implementation | Full-width pour on L5 across Zones B–D |

### Resistive Loss Estimation

For a 100 mm copper pour carrying 40 A on L1 (2 oz, 20 mm wide):

$$R = \frac{\rho \cdot L}{A} = \frac{1.72 \times 10^{-8} \times 0.1}{0.020 \times 70 \times 10^{-6}} = 1.23 \text{ mΩ}$$

$$P = I^2 \times R = 40^2 \times 0.00123 = **1.97 \text{ W}$$

For three phases of AC input (60 A each, 200 mm path, 30 mm wide):

$$P_{total\_AC} = 3 \times 60^2 \times \frac{1.72 \times 10^{-8} \times 0.2}{0.030 \times 70 \times 10^{-6}} = 3 \times 60^2 \times 1.64 \times 10^{-3} = **17.7 \text{ W}$$

This is significant and motivates using the widest possible pours and parallel layers.

## 7. Airflow Path Design

### Airflow Direction

The board is oriented with airflow from left (AC input) to right (DC output):

```
    Fan intake → EMI Filter → PFC MOSFETs → DC Bus Caps → Exhaust
    (coolest)    (Zone A)      (Zone B)       (Zone C)     (hottest)
```

This sequence is deliberate:

1. **EMI filter components (Zone A)** see the coolest incoming air. EMI filter performance degrades at high temperature (capacitor ESR increases, ferrite permeability drops).

2. **SiC MOSFETs (Zone B)** see slightly warmed air but have the highest allowable temperature (175°C Tj). They are actively cooled by the heatsink.

3. **DC bus electrolytic capacitors (Zone C)** see the warmest air. This is a trade-off — electrolytics are the most temperature-sensitive component (lifetime halves per 10°C), but placing them upstream of the MOSFETs would increase the power loop length.

> [!warning] Capacitor Lifetime at Elevated Temperature
> With 55°C ambient and 10–20°C air temperature rise through the MOSFET heatsink, the air reaching the electrolytic capacitors may be 65–75°C. At 75°C, a 105°C-rated cap has approximately:
>
> $$Lifetime = L_{base} \times 2^{(105-75)/10} = L_{base} \times 8$$
>
> This gives 8× the base lifetime (typically 2000–5000 hours base → 16,000–40,000 hours). For a 10-year product life (~87,000 hours), consider:
> - Using 125°C-rated capacitors
> - Adding a thermal baffle between MOSFETs and caps
> - Increasing heatsink fin area to reduce air temperature rise

### Component Height Profile

Ensure components are arranged with increasing height along the airflow direction to avoid flow shadows:

| Zone | Component | Typical Height |
|------|-----------|---------------|
| A (EMI filter) | CM choke | 20–30 mm |
| A | X/Y capacitors | 5–15 mm |
| B (PFC stage) | TO-247 MOSFETs + heatsink | 15–25 mm |
| B | Gate drivers (SO-8W) | 2 mm |
| C (DC bus) | Electrolytic caps (snap-in) | 25–40 mm |
| D (connectors) | Power connectors | 15–20 mm |

> [!tip] CM Choke Height
> The CM choke in Zone A is often the tallest component. Position it so the heatsink and capacitors downstream are not in its flow shadow. If necessary, offset the CM choke toward one edge of the board.

## 8. Thermal Management Summary Table

| Component | Cooling Method | Rth_ja Target | Max Dissipation | Max Temp Rise |
|-----------|---------------|---------------|-----------------|---------------|
| SiC MOSFET (×6) | Heatsink + TIM + forced air | ≤2.0°C/W | 50 W each | 100°C (55°C amb → 155°C Tj) |
| Boost diode (×6) | Shared heatsink | ≤2.5°C/W | 30 W each | 75°C |
| STGAP2SiC driver (×6) | PCB copper pour + thermal vias | ≤80°C/W | 0.33 W each | 26°C |
| Electrolytic caps | Forced air (downstream) | N/A | ESR loss only | 20°C above air temp |
| Snubber caps | PCB copper | N/A | <1 W each | Negligible |
| PCB copper pours | Convection + conduction | N/A | 18 W total (I²R) | 20–30°C local |

## 9. Thermal Design Verification

### Pre-Layout Thermal Simulation

Before committing to the final layout, perform a thermal simulation using:
- Input: component power dissipation values, airflow velocity (from fan spec), ambient temperature
- Tool: CFD simulation (FloTHERM, Icepak) or simplified conduction model
- Output: Temperature distribution on the board and heatsink
- Criteria: All junctions below target operating temperatures at maximum power and maximum ambient (55°C)

### Post-Layout Verification

After layout completion:
1. Extract copper pour areas and thicknesses from the EDA tool
2. Calculate I²R losses for each current-carrying pour
3. Verify thermal via arrays are correctly placed and connected
4. Check that no thermal relief pads exist on power connections
5. Verify heatsink mounting hole clearances meet creepage requirements

## 10. Cross-References

- [[__init]] — Board overview and component list
- [[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment]] — Copper weights and layer assignments
- [[07-PCB-Layout/AC-DC/02-Power Loop Analysis]] — Snubber placement (affects thermal layout)
- [[07-PCB-Layout/AC-DC/03-Gate Driver Layout]] — Driver power dissipation and thermal pour spec
- [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout]] — Airflow and zone separation considerations
- [[07-PCB-Layout/AC-DC/06-Creepage and Clearance]] — Mounting hole creepage requirements
- [[SiC Device Thermal Parameters]] — MOSFET and diode thermal data

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
