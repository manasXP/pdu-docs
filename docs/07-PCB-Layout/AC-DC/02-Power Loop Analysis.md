---
tags: [pdu, pcb-layout, vienna-pfc, power-loop, parasitic-inductance, decoupling]
created: 2026-02-22
status: draft
---

# 02 — Power Loop Analysis

## Purpose

This document analyzes the critical commutation loops in the Vienna Rectifier PFC stage and defines the parasitic inductance budget, decoupling capacitor placement strategy, and layout rules required to achieve the target loop inductance of **≤10 nH PCB contribution** per phase.

In a Vienna PFC switching at 48–65 kHz with SiC MOSFETs, the commutation loop inductance directly determines:
- **Voltage overshoot** at turn-off (V_overshoot = L_loop × dI/dt)
- **Switching loss** (higher overshoot forces larger deadtime or higher Vds_margin)
- **EMI emissions** (loop area is proportional to radiated emissions)
- **Device stress** (repetitive overshoot accelerates gate oxide degradation)

## Vienna PFC Commutation Loops

### Topology Review

The Vienna rectifier has three phases, each with two SiC MOSFETs (high-side and low-side relative to the neutral point). During each switching cycle, current commutates between a MOSFET and the corresponding boost diode through the DC bus capacitors.

There are two primary commutation loops per phase:

### Loop 1 — MOSFET Turn-Off (Main Commutation Loop)

When Q_hi turns off during a positive half-cycle, current transfers from Q_hi to D_hi through the snubber capacitors:

```
                    Loop 1: MOSFET Turn-Off
    ┌─────────────────────────────────────────┐
    │                                         │
    │   L_boost ─→ Q_hi(drain) ─→ C_snub ──┐ │
    │       ↑                               │ │
    │       │                               ↓ │
    │   AC input ←── D_hi ←── C_bus(+) ←───┘ │
    │                                         │
    └─────────────────────────────────────────┘

    Critical path (high dI/dt):
    Q_hi drain → C_snub1 → C_snub2 → C_bus(+) → D_hi → Q_hi source
```

**This is the most critical loop.** It carries the full switching current at turn-off (up to 60 A peak) with dI/dt of 5–15 A/ns. Every nanohenry of inductance in this loop adds voltage overshoot.

### Loop 2 — DC Bus Charge Loop

After commutation, the boost inductor current charges the DC bus capacitors through the boost diode:

```
                    Loop 2: DC Bus Charge
    ┌─────────────────────────────────────────┐
    │                                         │
    │   L_boost ─→ D_hi ─→ C_bus(+) ───────┐ │
    │       ↑                               │ │
    │       │                               ↓ │
    │   AC input ←────── C_bus(−) ←─────────┘ │
    │                                         │
    └─────────────────────────────────────────┘
```

This loop carries the average inductor current (up to 40 A) but at a lower dI/dt (limited by inductor). The inductance requirement is less stringent than Loop 1, but the current is continuous, so resistive losses in the traces dominate.

### Loop 3 — Gate Drive Loop

See [[03-Gate Driver Layout]] for the gate loop analysis. The gate loop is a separate, smaller loop with its own inductance budget (<5 nH).

## Parasitic Inductance Budget

### Component-Level Parasitics

| Element | Symbol | Value (nH) | Source | Notes |
|---------|--------|-----------|--------|-------|
| SiC MOSFET package (TO-247-4) | L_pkg_D + L_pkg_S | 5–8 | Datasheet, Kelvin source | 4-pin package; power source ≈5 nH, Kelvin source ≈0.5 nH |
| Snubber cap C_snub1 (1206 C0G) | L_cap1 | 0.8–1.2 | Capacitor datasheet | ESL of C0G 1206 at 630V |
| Snubber cap C_snub2 (1812 X7R) | L_cap2 | 1.5–2.0 | Capacitor datasheet | ESL of X7R 1812 at 630V |
| Bulk electrolytic C_bus | L_cap_bus | 10–15 | Capacitor datasheet | Not in the hot loop (decoupled by C_snub) |
| PCB traces + vias | L_PCB | **≤10 (target)** | Layout-dependent | This is what we control |

### Total Loop Inductance Budget (Loop 1)

| Contributor | Value (nH) | Notes |
|-------------|-----------|-------|
| MOSFET package (drain + source) | 7 | TO-247-4 with Kelvin source |
| C_snub1 ESL (parallel array of 4–8) | 0.2 | 1 nH / 4 parallel = 0.25, use 4 minimum |
| C_snub2 ESL (parallel pair) | 1.0 | 2 nH / 2 parallel |
| PCB interconnect (target) | **10** | Traces, vias, pad transitions |
| **Total** | **~18.2** | |

### Voltage Overshoot Calculation

At maximum switching current with the target loop inductance:

| Parameter | Value |
|-----------|-------|
| Peak switching current (I_pk) | 60 A |
| Turn-off dI/dt | 10 A/ns (SiC MOSFET typical) |
| Total loop inductance (L_total) | 18 nH |
| Voltage overshoot (V_os = L × dI/dt) | 18 nH × 10 A/ns = **180 V** |
| DC bus voltage (V_bus) | 460 V (nominal at 260 VAC input) |
| Peak drain voltage (V_ds_pk) | 460 + 180 = **640 V** |
| MOSFET rated voltage | 650 V |
| Safety margin | **10 V (1.5%)** |

> [!warning] Tight Voltage Margin
> With 650V-rated SiC MOSFETs, the margin at 460V bus + 180V overshoot is only 10V (1.5%). This is unacceptably tight for production.
>
> **Mitigation options (implement at least two):**
> 1. Reduce L_PCB to ≤5 nH (aggressive layout optimization) → V_os = 130V, margin = 60V
> 2. Use 900V or 1200V SiC MOSFETs → margin increases to 260V or 560V
> 3. Add RC snubber across the MOSFET to slow dI/dt
> 4. Reduce switching speed via Rg_on increase (increases switching loss)
>
> The topology selection in [[01-Topology Selection]] should specify the device voltage class. With a 920V DC bus capability, 1200V SiC MOSFETs are likely required regardless.

### Revised Budget for 1200V Devices at 920V Bus

| Parameter | Value |
|-----------|-------|
| DC bus voltage (V_bus) | 920 V (max, at 530 VAC input) |
| Total loop inductance (L_total) | 18 nH |
| dI/dt at turn-off | 10 A/ns |
| Voltage overshoot | 180 V |
| Peak drain voltage | 920 + 180 = **1100 V** |
| MOSFET rated voltage | 1200 V |
| Safety margin | **100 V (8.3%)** |

With 1200V devices, the 18 nH total budget provides adequate margin. The 10 nH PCB target remains the design goal.

## Decoupling Capacitor Array

### Tiered Decoupling Strategy

The decoupling is organized in three tiers, each serving a different frequency range:

```
    Frequency coverage:

    C_snub1 (100nF C0G)  ──────────────────────────────  >10 MHz
    C_snub2 (1µF X7R)    ─────────────────────  1–10 MHz
    C_bus (470µF elec)    ────────────  <1 MHz

    ├──────┼──────┼──────┼──────┼──────┤
    100Hz  1kHz  10kHz  100kHz 1MHz  10MHz
```

### C_snub1 — First-Tier High-Frequency Decoupling

| Parameter | Specification |
|-----------|--------------|
| Capacitance | 100 nF |
| Dielectric | C0G / NP0 (essential — X7R is too lossy and has voltage derating) |
| Voltage rating | 630 V minimum (1000V preferred for margin) |
| Package | 1206 or 1210 |
| Quantity per MOSFET | 4–8 |
| Placement | **<5 mm from drain pad** (measured pad-to-pad) |
| Return path | Direct to source pad or L2 GND via adjacent via |
| Orientation | Parallel to current flow (minimize loop area) |

**Placement detail:**

```
    Top view (L1) — one MOSFET

         Drain pad
    ┌─────────────────┐
    │    TO-247        │
    │   ┌─────────┐   │
    │   │         │   │
    │   │  Q_hi   │   │  C_snub1 array (4× minimum)
    │   │         │   │  ┌──┐ ┌──┐ ┌──┐ ┌──┐
    │   └─────────┘   │  │  │ │  │ │  │ │  │
    │    Source pad    │  └──┘ └──┘ └──┘ └──┘
    └─────────────────┘    ↕ <5mm from drain
                          Return vias to L2 ○ ○ ○ ○
```

> [!tip] C0G vs X7R for C_snub1
> C0G (NP0) ceramic capacitors are mandatory for C_snub1. Unlike X7R, C0G has:
> - No voltage derating (X7R 630V loses 60–80% capacitance at rated voltage)
> - No temperature derating
> - Very low ESR (lower losses at switching frequency)
> - Linear impedance characteristic
>
> The trade-off is lower volumetric capacitance — hence only 100 nF per cap in 1206/1210. Use 4–8 in parallel to achieve both the required total capacitance and low ESL.

### C_snub2 — Second-Tier Decoupling

| Parameter | Specification |
|-----------|--------------|
| Capacitance | 1 µF |
| Dielectric | X7R (acceptable at this frequency range) |
| Voltage rating | 630 V minimum |
| Package | 1812 or 2220 |
| Quantity per MOSFET | 2 |
| Placement | **<10 mm from drain pad** |
| Return path | Via to L2 GND or direct to source copper |

### C_bus — Bulk DC Bus Capacitors

| Parameter | Specification |
|-----------|--------------|
| Capacitance | 470 µF per cap |
| Type | Electrolytic, low-ESR, high-ripple-current rated |
| Voltage rating | 450 V (series pairs for 900V bus) |
| Quantity | 4–6 total (2–3 series pairs) |
| Placement | Zone C, **<50 mm from the nearest MOSFET** |
| Ripple current | Size for 3× switching frequency ripple (144–195 kHz) |

> [!warning] Series Electrolytic Capacitors
> When using two electrolytics in series for 900V bus rating:
> - Each cap sees nominally V_bus/2, but imbalance can cause one cap to see >450V
> - **Mandatory:** Add balancing resistors (100 kΩ–470 kΩ) across each capacitor
> - **Mandatory:** Add balancing/bleeder resistors for safety discharge
> - Match capacitor values within ±10% (same manufacturer lot preferred)
> - Verify ripple current rating is adequate for the total bus ripple at 3× fsw

## DC Bus Charge Loop (Loop 2)

The DC bus charge loop extends from the boost inductor through the boost diode to the bulk capacitors and back. This loop carries continuous current (up to 40 A) and must be sized for low resistive loss.

### Layout Rules for Loop 2

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| Copper pour width | ≥20 mm (L1, 2oz) for 40A | IPC-2152 derating |
| Via array L1↔L5/L6 | ≥30 vias (0.5 mm drill) | 40A / 1.5A per via |
| Path length | Minimize — keep C_bus within 50 mm of diodes | Reduce I²R loss |
| L2 return path | Unbroken ground plane beneath | Low-inductance return |

### DC Output to LLC Board Connector

The DC bus connects from the bulk capacitors (Zone C) to the output connector (Zone D) that feeds the [[07-PCB-Layout/DC-DC/__init|DC-DC]] converter board. This path must handle 40 A continuous:

| Parameter | Value |
|-----------|-------|
| Copper pour width | ≥20 mm (L1 + L6 parallel, 2 oz each) |
| Via array at connector | ≥30 vias |
| Connector type | High-current PCB terminal block or bus bar |
| Rated current | ≥50 A (with derating) |

## Layout Rules Summary

### Power Loop (Loop 1) — Mandatory Rules

| # | Rule | Target |
|---|------|--------|
| 1 | Forward current path on L1, return on L2 (and/or L6) | Overlapping planes |
| 2 | C_snub1 pad-to-drain-pad distance | <5 mm |
| 3 | C_snub2 pad-to-drain-pad distance | <10 mm |
| 4 | Switching node copper area (L1 only) | ≤1 cm² per phase |
| 5 | Loop area (drain→C_snub→return via→source) | <2 cm² per phase |
| 6 | No routing on L2 beneath power stage zone | Zero traces on L2 |
| 7 | MOSFET and snubber caps on same board side | Top side (L1) |
| 8 | Return vias from C_snub to L2 | <3 mm from cap pad |
| 9 | Via count for return path | ≥4 vias per cap group |
| 10 | Total PCB loop inductance | ≤10 nH |

### Same-Side Placement Rule

All components in the hot commutation loop (MOSFET, snubber caps, boost diode) **must be placed on the same board side** (L1/top). Placing components on opposite sides forces current through vias in the hot loop, adding 0.5–1 nH per via transition and increasing total loop inductance.

Exception: If the boost diode is placed on L6 (bottom), the via transition inductance (~1 nH for a 4-via array) may be acceptable if it enables a shorter overall loop path. Evaluate on a case-by-case basis with field solver simulation.

## Simulation and Verification

### Pre-Layout Estimation

Use the following formula for a rough PCB loop inductance estimate:

$$L_{PCB} \approx \mu_0 \cdot \frac{d \cdot l}{w}$$

Where:
- $d$ = dielectric thickness between forward and return layers (100 µm = 0.1 mm)
- $l$ = loop path length (target <20 mm)
- $w$ = overlap width of forward and return copper (target >10 mm)

$$L_{PCB} \approx 4\pi \times 10^{-7} \times \frac{0.0001 \times 0.020}{0.010} = 0.25 \text{ nH}$$

This extremely low value assumes perfect overlap. Real layouts with pad transitions, via transitions, and non-uniform overlap will be 10–40× higher. Use this formula for relative comparison between layout options, not absolute values.

### Post-Layout Verification

After completing the layout, extract loop inductance using:

1. **2D field solver** — Cross-section analysis of the stack-up (e.g., Altium PDN Analyzer, Ansys Q3D)
2. **3D field solver** — Full loop extraction including via transitions (Ansys Q3D Extractor, CST)
3. **Time-domain simulation** — Import extracted parasitics into a SPICE model and verify V_ds overshoot matches the budget

> [!tip] Loop Inductance Measurement
> If a prototype board is available, measure the loop inductance by:
> 1. Shorting the MOSFET drain-source with a low-inductance jumper
> 2. Measuring impedance from the snubber cap pads using a VNA (vector network analyzer)
> 3. Extract inductance from the impedance vs. frequency plot (look for the inductive region above the capacitor SRF)
>
> Target: measured loop inductance should be within 20% of the simulated value.

## Cross-References

- [[__init]] — Board overview and component list
- [[01-Stack-Up and Layer Assignment]] — Stack-up that enables low-inductance loops
- [[03-Gate Driver Layout]] — Gate loop (separate inductance budget)
- [[04-Thermal Layout]] — MOSFET placement affects loop path
- [[05-EMI-Aware Layout]] — Loop area minimization for EMI
- [[06-Creepage and Clearance]] — Spacing constraints that may increase loop path
- [[01-Topology Selection]] — Vienna PFC topology and device selection
- [[SiC Device Thermal Parameters]] — MOSFET package parasitic data

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: loop analysis, parasitic budget, decoupling strategy |
