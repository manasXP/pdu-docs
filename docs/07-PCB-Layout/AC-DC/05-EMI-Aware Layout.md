---
tags: [pdu, pcb-layout, vienna-pfc, emi, common-mode, switching-node, conducted-emissions]
created: 2026-02-22
status: draft
---

# 05 — EMI-Aware Layout

## Purpose

This document defines the EMI-aware layout strategy for the Vienna Rectifier PFC board. At 30 kW with SiC MOSFETs switching at 35+ kV/µs and 10+ A/ns, this board is a significant source of both conducted and radiated electromagnetic interference. The layout must minimize EMI generation at the source and contain residual emissions within the board boundaries to avoid corrupting the EMI filter performance.

The three primary EMI mechanisms in the Vienna PFC are:

1. **Differential-mode (DM) conducted emissions** — caused by high dI/dt switching currents through parasitic loop inductances. Addressed by loop minimization (see [[02-Power Loop Analysis]]).

2. **Common-mode (CM) conducted emissions** — caused by high dV/dt on the switching node coupling through parasitic capacitances to the heatsink, chassis, and PE conductor. This is typically the dominant EMI source in SiC-based PFC converters.

3. **Radiated emissions** — caused by loop antennas (current loops with large area) and electric field radiation from high dV/dt nodes. Addressed by minimizing loop areas and switching node copper area.

## Common-Mode Current Budget

### CM Current Sources

The primary CM current sources on the AC-DC board are:

#### 1. MOSFET Drain-to-Heatsink Capacitance (Cdh)

Each SiC MOSFET in a TO-247 package has parasitic capacitance between the drain (tab) and the heatsink through the TIM:

$$C_{dh} = \frac{\varepsilon_0 \cdot \varepsilon_r \cdot A_{tab}}{d_{TIM}}$$

| Parameter | Value |
|-----------|-------|
| Tab area (A_tab) | ~1.5 cm² = 150 mm² |
| TIM thickness (d_TIM) | 0.5 mm (Bergquist GP3000S, compressed) |
| TIM relative permittivity (εr) | ~5 (silicone-based gap pad) |
| Calculated Cdh per MOSFET | ~13 pF |
| Measured/typical Cdh | **~100 pF** (including fringing and mounting hardware) |

> [!warning] Cdh is Much Larger Than Calculated
> The simple parallel-plate calculation underestimates Cdh significantly. The actual value includes:
> - Fringing fields around the tab edges
> - Capacitance through the mounting screw (metal-to-metal through insulating washer)
> - Capacitance from drain copper on the PCB to the heatsink through the board
>
> Use the measured/datasheet value of **~100 pF per MOSFET** for CM current calculations.

**CM current from 6 MOSFETs:**

$$I_{CM\_MOSFET} = N \times C_{dh} \times \frac{dV}{dt} = 6 \times 100 \text{ pF} \times 35 \text{ kV/µs} = **21 \text{ A (peak)}$$

This is the dominant CM current source. It flows through the heatsink to chassis/PE and returns through the Y-capacitors in the EMI filter.

#### 2. Gate Driver Isolation Capacitance (Cdh_driver)

Per [[03-Gate Driver Layout]], each STGAP2SiC contributes:

$$I_{CM\_driver} = 6 \times 5 \text{ pF} \times 35 \text{ kV/µs} = **1.05 \text{ A (peak)}$$

#### 3. PCB-to-Chassis Capacitance

The PCB bottom layer (L6) has parasitic capacitance to the metal chassis/enclosure:

| Parameter | Estimate |
|-----------|----------|
| Board area | 250 × 180 mm = 450 cm² |
| Board-to-chassis gap | 5–10 mm (standoff height) |
| Estimated capacitance | 5–20 pF (low, due to air gap) |
| CM current contribution | <1 A peak |

### Total CM Current Budget

| Source | CM Current (peak) | Percentage |
|--------|-------------------|------------|
| MOSFET Cdh (6×100 pF) | 21 A | 91% |
| Driver Cdh (6×5 pF) | 1.05 A | 5% |
| PCB-to-chassis | <1 A | 4% |
| **Total** | **~23 A peak** | 100% |

> [!warning] 23 A Peak CM Current
> This is an extremely high CM current that must be managed through:
> 1. **Reducing dV/dt** (increases switching loss — last resort)
> 2. **Reducing Cdh** (better TIM, thicker insulation, reduced drain copper area)
> 3. **Providing a low-impedance CM return path** (Y-caps, chassis bonding)
> 4. **EMI filter attenuation** (CM choke + Y-caps in Zone A)
>
> The EMI filter must attenuate this CM current to below the EN 55032 / CISPR 32 Class B limits at the AC input terminals.

## Switching Node Area Minimization

### Why Switching Node Area Matters

The switching node is the connection between the MOSFET drain and the boost inductor. It transitions between 0V and V_bus (up to 920V) at every switching cycle. Any copper connected to the switching node acts as an electric field antenna radiating at the switching frequency and its harmonics.

Additionally, switching node copper on L1 couples capacitively to L2 (ground plane) and to the heatsink, generating additional CM current.

### Switching Node Area Target

| Parameter | Target | Notes |
|-----------|--------|-------|
| Area per phase | **≤1 cm²** (100 mm²) | Total copper area on all layers |
| Layer restriction | **L1 only** | No switching node copper on L2–L6 |
| Copper on L2 beneath switching node | Continuous ground pour | Shields switching node from inner layers |

### Implementation Strategy

The switching node copper consists of:
- MOSFET drain pad (TO-247 tab pad): ~150 mm² (already exceeds 1 cm² target)
- Routing from drain pad to boost inductor connection
- Snubber capacitor pads connected to drain

Since the TO-247 drain pad alone is ~150 mm², achieving <100 mm² total switching node area is impossible with a standard TO-247 footprint. The **practical target is to minimize the area beyond the pad footprint**:

| Element | Estimated Area (mm²) | Minimization Strategy |
|---------|---------------------|----------------------|
| TO-247 drain pad | 150 | Fixed — cannot reduce |
| Drain-to-snubber routing | 20–50 | Place C_snub1 immediately adjacent to pad |
| Drain-to-inductor routing | 30–80 | Shortest possible trace; use L1 only |
| Additional copper | 0 | No unnecessary copper on switching node net |
| **Total** | **200–280** | Target <300 mm² practical |

> [!tip] Revised Practical Target
> With the TO-247 drain pad contributing 150 mm², the absolute target of ≤100 mm² per phase is not achievable without package changes. The practical target is:
> - **≤300 mm² (3 cm²)** total switching node copper per phase
> - **Zero switching node copper on L2–L6** (shielded by L2 ground plane)
> - Drain pad + snubbers + inductor connection only — no extra copper

### Switching Node Copper Rules

| # | Rule | Rationale |
|---|------|-----------|
| 1 | Switching node copper on L1 only | L2 ground plane shields inner layers |
| 2 | No copper pour flood on switching node net | Only pad and trace connections |
| 3 | Minimize drain pad area (use exact TO-247 footprint) | Reduce antenna area |
| 4 | Route drain-to-inductor as short as possible | Minimize loop area and antenna |
| 5 | No switching node traces crossing EMI filter zone | Prevents re-injection |
| 6 | L2 ground plane continuous beneath switching node | Provides shielding and CM return |

## EMI Filter Zone Separation

### Separation Requirement

The EMI filter in Zone A must be physically and electrically separated from the power stage in Zone B. Without adequate separation, the switching noise from the power stage couples back into the filter output, reducing the effective filter attenuation.

| Parameter | Requirement |
|-----------|-------------|
| Physical separation | **≥20 mm** clear zone between Zone A boundary and Zone B boundary |
| Stitching via fence | **Double row**, 0.3 mm drill, 2 mm pitch, staggered |
| Copper pour in separation zone | L2 GND plane only (no other copper on L1, L3–L6) |
| Component placement | No components in the 20 mm separation zone |
| Trace routing | No traces crossing the separation zone on any layer except L2 GND |

### Stitching Via Fence Specification

The double-row stitching via fence creates a low-impedance ground connection across the zone boundary, containing EMI within each zone:

```
    Zone A          Separation Zone (≥20 mm)          Zone B
    (EMI filter)    (no components, no routing)       (PFC stage)

    ─────────── ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ──────────────
                 ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
    ─────────── ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ──────────────

    ○ = stitching via (0.3mm drill, GND net)
    Row spacing: 2 mm (staggered)
    Via pitch within row: 2 mm
    Fence length: full board width (180 mm)
```

| Parameter | Value |
|-----------|-------|
| Via drill | 0.3 mm |
| Via pad | 0.6 mm |
| Via pitch (within row) | 2 mm |
| Row-to-row spacing | 2 mm (staggered) |
| Number of rows | 2 (double fence) |
| Fence length | Full board width (180 mm) |
| Total vias | ~180 (90 per row) |
| Net | GND (L2 plane) |
| Effective shielding | >20 dB at 30 MHz, >30 dB at 100 MHz |

> [!tip] Via Fence Effectiveness
> A stitching via fence is effective up to the frequency where the via spacing equals λ/20. For 2 mm pitch:
>
> $$f_{max} = \frac{c}{20 \times d \times \sqrt{\varepsilon_r}} = \frac{3 \times 10^8}{20 \times 0.002 \times \sqrt{4.5}} \approx 3.5 \text{ GHz}$$
>
> This is well above the frequency range of concern for conducted emissions (150 kHz – 30 MHz) and most radiated emissions (30 MHz – 1 GHz). The via fence is effective across the entire relevant spectrum.

### Additional Separation Measures

| Measure | Implementation | Benefit |
|---------|---------------|---------|
| Guard ring | Grounded copper ring on L1 and L6 around the separation zone | Reduces E-field coupling between zones |
| No shared return paths | EMI filter ground returns to the input connector, not through the power stage | Prevents CM noise injection into filter |
| Separate ground tie point | EMI filter GND connects to L2 at the input connector only | Star-ground topology for CM |

## L2 Ground Plane Integrity

### Critical Importance

The L2 ground plane is the single most important EMI mitigation element on the board. As detailed in [[01-Stack-Up and Layer Assignment]], L2 must remain continuous and unbroken. This section specifies the EMI-related reasons:

1. **Shield between L1 (switching noise) and L3 (sensitive signals):** The L2 plane attenuates electric field coupling by >40 dB.

2. **Low-impedance return path for power loops:** The return current flows on L2 directly beneath the L1 forward current, forming a tight loop. Any cut in L2 forces the return current to detour, increasing the effective loop area and both DM and CM emissions.

3. **CM current return path:** The CM current injected by MOSFET Cdh into the heatsink returns through the Y-caps and L2 ground plane. Slots or splits in L2 increase the CM loop area.

### L2 Rules (EMI-Focused)

| # | Rule | Consequence of Violation |
|---|------|------------------------|
| 1 | No traces routed on L2 | Creates slots that increase loop area |
| 2 | No splits or divisions | Forced return current detour → increased CM/DM emissions |
| 3 | No thermal relief on vias/pads | Adds impedance to return path |
| 4 | No large via clusters that fragment the plane | Island formation → return path disruption |
| 5 | >95% copper fill | Maximum continuous return path |
| 6 | GND vias at every signal via | Provides local return path for L3 signals |
| 7 | Stitching vias along board edges | Contains fields within the board boundary |

### Signal Via Return Path Rule

Every signal via that transitions from L1 to L3 (or L6 to L3) must have a companion ground via within 2 mm. Without this companion via, the return current on L2 has no low-impedance path to transition to the correct layer, and it must find an alternative path — increasing the effective loop area.

```
    Signal via + companion GND via:

    L1:  ──── sig ────○──────────────────
                      │  ○ ← GND via (within 2mm)
    L2:  ═════════════●══════════════════  (continuous GND plane)
                      │  ●
    L3:  ──── sig ────○──────────────────
```

## Sensitive Signal Routing

### Signal Categories and Routing Rules

| Signal Category | Examples | Layer | Routing Rules |
|----------------|----------|-------|---------------|
| Gate drive (high dV/dt) | STGAP2SiC to MOSFET gate | L1 | <5mm, on L1 only, see [[03-Gate Driver Layout]] |
| Current sense (analog) | Shunt resistor voltage | L3 | Differential pair, guard traces, away from SW node |
| Temperature sense | NTC thermistor | L3 | Away from power traces, guard traces |
| SPI control | STGAP2SiC daisy chain | L3 | ≥2mm from HV, standard digital routing |
| CAN bus | Inter-module communication | L3 | 120Ω differential, terminated |
| Fault/interlock | OVP, OCP, OTP signals | L3 | Guard traces, filtered at source |
| Auxiliary power | 12V, 5V, 3.3V distribution | L4 | Decoupled locally, via to L2 return |

### Current Sense Routing

The Vienna PFC requires accurate current sensing for each phase (for PFC control) and for the DC bus (for current limiting). Current sense signals are the most noise-sensitive signals on the board.

| Rule | Requirement |
|------|-------------|
| Routing layer | L3 exclusively |
| Trace type | Differential pair from shunt resistor to ADC/comparator |
| Guard traces | Grounded guard on both sides, connected to L2 via stitching vias every 5 mm |
| Distance from switching node | ≥10 mm horizontal separation |
| Distance from gate drive traces | ≥5 mm |
| Filtering | RC low-pass at the ADC input (100Ω + 100pF, fc ≈ 16 MHz) |
| Common-mode rejection | Route both traces of the differential pair with identical length and symmetry |

```
    Current sense differential routing on L3:

    L2: ═══════════════════════════════════════  (GND plane)

    L3: ──GND guard──┬── sense+ ──┬──GND guard──
                     │            │
         GND via ○   │            │   ○ GND via
                     │            │
    L3: ──GND guard──┴── sense− ──┴──GND guard──

    L2: ═══════════════════════════════════════  (GND plane)
```

### Analog Ground Considerations

The Vienna PFC board does not use a split ground plane (L2 is continuous). However, the current sense and control circuits benefit from a localized "quiet" zone on L1:

- Define a region on L1 (typically near the control connector or MCU interface) where no power copper pours are present
- Route all analog sense signals to this quiet zone before transitioning to the control board connector
- Place anti-aliasing filters and protection circuits in this quiet zone
- Connect this zone to L2 through a cluster of vias at a single point (quasi-star-ground)

## EMI Filter Component Placement

### Zone A Layout Strategy

The EMI filter components in Zone A must be arranged to maximize filter attenuation and minimize parasitic coupling:

```
    Zone A — EMI Filter Layout (top view)

    AC input     ┌─────────────────────────────────────┐
    connector    │                                     │
    ──Phase A──→ │  CM Choke  →  X-cap  →  CM Choke  →│── to Zone B
    ──Phase B──→ │  (stage 1)    (DM)     (stage 2)   │   (after
    ──Phase C──→ │                                     │    20mm gap)
    ──PE ──────→ │  Y-caps to GND                      │
                 │  (between stages)                   │
                 └─────────────────────────────────────┘
                                                        ↑
                                                   Via fence
```

### CM Choke Placement

| Rule | Requirement |
|------|-------------|
| Position | Immediately after AC input connector |
| Orientation | Windings perpendicular to airflow (for cooling) |
| Mounting | Through-hole or surface-mount (depends on core size) |
| Clearance to PCB edge | ≥5 mm (for creepage to chassis) |
| Clearance to other magnetics | ≥10 mm (prevent mutual coupling) |

### X-Capacitor Placement

| Rule | Requirement |
|------|-------------|
| Position | Between CM choke stages (if two-stage filter) |
| Type | X2-rated, metallized film |
| Connection | Line-to-line (phase-to-phase) |
| Trace length | Short, direct connection between phase conductors |

### Y-Capacitor Placement

| Rule | Requirement |
|------|-------------|
| Position | Between each CM choke stage and ground (L2) |
| Type | Y2-rated ceramic (4.7 nF typical) |
| Connection | Each phase to L2 GND via shortest possible path |
| Return path | Directly to L2 via stitching vias, not through long traces |
| Safety | Y2 rating required for reinforced insulation applications |
| Leakage current | Total Y-cap leakage must meet IEC 62368-1 limits (<3.5 mA) |

> [!warning] Y-Capacitor Leakage Current
> Y-capacitors conduct a small AC leakage current from line to PE ground. At 50 Hz with 3× Y2 caps of 4.7 nF:
>
> $$I_{leakage} = 3 \times 2\pi \times 50 \times 4.7 \times 10^{-9} \times 530 = 2.35 \text{ mA}$$
>
> This is below the 3.5 mA limit for fixed equipment (IEC 62368-1). However, increasing Y-cap values for better CM attenuation will increase leakage. Check the total leakage budget before sizing Y-caps.

## Board Edge Stitching

In addition to the zone-boundary via fence, place stitching vias along all four board edges:

| Parameter | Value |
|-----------|-------|
| Via pitch | 3 mm (looser than zone fence) |
| Via drill | 0.3 mm |
| Distance from board edge | 1.5–2 mm |
| Net | GND (L2) |
| Purpose | Contains fringing fields, reduces edge radiation |

## EMI Verification

### Pre-Layout EMI Estimate

Before layout, estimate conducted emissions using:

1. CM current budget (23 A peak, as calculated above)
2. EMI filter transfer function (from filter design)
3. LISN impedance (50 Ω per standard)
4. Predicted voltage at LISN = I_CM × Z_filter_output × Z_LISN

### Post-Layout EMI Verification

After layout:
1. Measure switching node copper area on each phase (target <3 cm²)
2. Verify L2 continuity — no unintended slots or splits
3. Verify via fence completeness — no gaps >3 mm
4. Verify all signal vias have companion ground vias
5. Measure separation distance between Zone A and Zone B (≥20 mm)
6. Check current sense routing for proper guarding and differential symmetry

### Near-Field Scanning (Prototype)

On the first prototype, perform near-field scanning with an H-field probe to identify:
- Unexpected current loop areas
- L2 ground plane return current distribution
- CM current paths through the heatsink mounting
- Coupling between EMI filter and power stage

## Cross-References

- [[__init]] — Board overview and zone map
- [[01-Stack-Up and Layer Assignment]] — L2 ground plane definition
- [[02-Power Loop Analysis]] — Power loop area minimization (DM emissions)
- [[03-Gate Driver Layout]] — Driver CM current contribution
- [[04-Thermal Layout]] — Airflow path and heatsink coupling
- [[06-Creepage and Clearance]] — Safety spacings affect routing options

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: CM budget, switching node area, filter separation, L2 rules |
