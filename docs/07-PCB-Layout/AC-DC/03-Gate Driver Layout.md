---
tags: [pdu, pcb-layout, vienna-pfc, gate-driver, stgap2sic, sic-mosfet]
created: 2026-02-22
status: draft
---

# 03 — Gate Driver Layout

## 1. Purpose

This document specifies the PCB layout rules for the STGAP2SiC isolated gate drivers used to drive the 6 SiC MOSFETs in the Vienna Rectifier PFC stage. The gate driver layout is critical because:

1. **Gate loop inductance** directly causes gate voltage overshoot/undershoot, risking false turn-on (shoot-through) or gate oxide damage.
2. **dV/dt immunity** determines whether the driver can withstand the 35+ kV/µs switching transients without malfunctioning.
3. **Isolation integrity** must be maintained between the high-side gate drive circuit and the low-voltage control logic.

The STGAP2SiC was selected for its high dV/dt immunity (>100 V/ns), 4A peak gate current capability, integrated Miller clamp, and SPI configurability. See [[01-Topology Selection]] for driver selection rationale.

## 2. Gate Driver Overview — STGAP2SiC

| Parameter | Value | Notes |
|-----------|-------|-------|
| Package | SO-8W (wide body) | 5.3 mm creepage across isolation barrier |
| Peak source/sink current | 4 A / 4 A | Adequate for SiC gate at 48–65 kHz |
| Output voltage (high) | VDRV (up to +20 V) | Typ. +18V for SiC |
| Output voltage (low) | VNEG (down to −5 V) | Negative bias prevents parasitic turn-on |
| dV/dt immunity (CMTI) | >100 V/ns | Exceeds 35 kV/µs requirement |
| Propagation delay | ~80 ns typ. | Matched across 6 drivers via SPI trim |
| Isolation voltage | 1200 V working, 5700 V surge | Adequate for 920V DC bus |
| Configuration | SPI (primary side) | Deadtime, UVLO thresholds, fault reporting |
| DESAT detection | Integrated | Programmable threshold and blanking time |
| Miller clamp | Integrated | Active clamp on output during off-state |

## 3. Placement Strategy

### Driver-to-MOSFET Relationship

Each STGAP2SiC drives one SiC MOSFET. The 6 driver ICs are placed in close proximity to their respective MOSFETs:

```
    Phase A              Phase B              Phase C
    ┌──────┐             ┌──────┐             ┌──────┐
    │ U1   │─── Q1 (hi)  │ U3   │─── Q3 (hi)  │ U5   │─── Q5 (hi)
    │STGAP │             │STGAP │             │STGAP │
    └──────┘             └──────┘             └──────┘
    ┌──────┐             ┌──────┐             ┌──────┐
    │ U2   │─── Q2 (lo)  │ U4   │─── Q4 (lo)  │ U6   │─── Q6 (lo)
    │STGAP │             │STGAP │             │STGAP │
    └──────┘             └──────┘             └──────┘
```

### Placement Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| Driver-to-MOSFET distance | ≤15 mm (pad-to-pad) | Minimize gate loop path length |
| Driver orientation | Output pins toward MOSFET gate/source | Shortest gate trace routing |
| Driver side | Same side as MOSFET (L1/top) | Avoid via transitions in gate loop |
| Minimum spacing from switching node | **≥5 mm** from any switching node copper | dV/dt coupling protection |
| Driver-to-driver spacing | ≥5 mm between different phase drivers | Prevent cross-coupling |
| SPI bus routing | L3 (signal layer) | Away from switching nodes |

> [!warning] Driver Placement Near Switching Node
> The STGAP2SiC output pins (OUTH, OUTL) must be close to the MOSFET gate, but the driver body must be kept **≥5 mm away from switching node copper** (the drain-side copper that transitions between V_bus and 0V at each switching event). The dV/dt on the switching node (35 kV/µs) will capacitively couple into the driver through the PCB dielectric if the driver overlaps the switching node area on an adjacent layer.

## 4. Gate Loop Analysis

### Gate Loop Path

The gate drive loop includes all conductors carrying the gate charge/discharge current:

```
    Gate Loop (per MOSFET):

    STGAP2SiC OUTH pin
         │
         ├── Rg_on (series resistor, on-path)
         │      │
         │      ├── MOSFET Gate pin
         │      │      │
         │      │      └── MOSFET (internal Cgs, Cgd)
         │      │             │
         │      │             ├── MOSFET Kelvin Source pin
         │      │             │
         │      └─────────────┘
         │
    STGAP2SiC OUTL/Source return pin
         │
         └── Rg_off (parallel path via Schottky steering diode)
```

### Gate Loop Inductance Budget

| Element | Symbol | Value (nH) | Notes |
|---------|--------|-----------|-------|
| STGAP2SiC output pin bond wire | L_drv | 1.0 | SO-8W package |
| PCB trace: OUTH to Rg_on | L_trace1 | 0.5 | <5 mm trace, L1 |
| Rg_on resistor body | L_Rg | 0.5 | 0402 or 0603 package |
| PCB trace: Rg_on to gate pin | L_trace2 | 0.5 | <5 mm trace, L1 |
| MOSFET gate bond wire + internal | L_gate | 1.0 | TO-247-4 |
| MOSFET Kelvin source lead | L_Ks | 0.5 | 4th pin, dedicated Kelvin |
| PCB trace: Kelvin source to driver return | L_trace3 | 0.5 | <5 mm trace, L1 |
| STGAP2SiC source return bond wire | L_ret | 0.5 | SO-8W package |
| **Total** | **L_gate_loop** | **~5.0** | Budget target: **<5 nH** |

> [!tip] Gate Loop Budget is Tight
> The 5 nH budget leaves almost no margin for PCB routing. Every millimeter of trace adds ~1 nH/mm (for a narrow trace without a ground return plane directly beneath). To stay within budget:
> - Route gate traces **exclusively on L1** with L2 ground return directly beneath
> - Keep all traces **<5 mm** between driver and MOSFET
> - Use 0402 passives for Rg to minimize package inductance
> - Never route gate traces through vias

## 5. Gate Resistor Design

### Turn-On Path — Rg_on

| Parameter | Value | Notes |
|-----------|-------|-------|
| Resistance | 3–5 Ω | Controls dV/dt at turn-on; higher = slower, lower EMI |
| Power dissipation | P = Qg × Vdrv × fsw ≈ 200 nC × 23V × 65kHz = **0.3 W** | Use 0603 or 0805 rated ≥0.25W |
| Package | 0402 (preferred for low inductance) or 0603 | Thin-film for tight tolerance |
| Quantity | 1 per MOSFET | Series in gate-on path |

### Turn-Off Path — Rg_off with Schottky Steering

For fast turn-off (to prevent dV/dt-induced parasitic turn-on), a lower resistance path is used during turn-off, steered by a Schottky diode:

```
    STGAP2SiC OUTH ────┬──── Rg_on (3-5Ω) ────┬──── MOSFET Gate
                       │                       │
                       └── D_steer ── Rg_off ──┘
                           (Schottky)  (1-2Ω)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Rg_off | 1–2 Ω | Lower than Rg_on for faster turn-off |
| Schottky diode | BAT54S or similar | Low Vf (<0.4V), fast switching |
| Diode orientation | Cathode toward driver, anode toward gate | Conducts during turn-off (gate discharge) |
| Package | SOD-323 or SOD-523 | Small package for short loop |

> [!warning] Schottky Diode Placement
> The Schottky steering diode must be placed **immediately adjacent** to the Rg_on resistor — within 2 mm pad-to-pad. The diode and Rg_off form a parallel path that must not add length to the gate loop. Poor placement of the steering network can actually increase gate loop inductance, negating its benefit.

### Turn-Off dV/dt Immunity Check

At maximum dV/dt (35 kV/µs) across the MOSFET, the Miller capacitor Cgd injects current into the gate:

$$I_{Miller} = C_{gd} \times \frac{dV}{dt}$$

For a typical SiC MOSFET with Cgd ≈ 15 pF at high Vds:

$$I_{Miller} = 15 \text{ pF} \times 35 \text{ kV/µs} = 0.525 \text{ A}$$

The gate voltage induced by this current through Rg_off:

$$V_{gate} = I_{Miller} \times R_{g\_off} = 0.525 \text{ A} \times 2 \text{ Ω} = 1.05 \text{ V}$$

With the STGAP2SiC driving −5V on the gate during off-state, the net gate voltage is:

$$V_{gs} = -5 \text{ V} + 1.05 \text{ V} = -3.95 \text{ V}$$

This is well below the SiC MOSFET threshold voltage (~2.5–4V), so **no parasitic turn-on occurs**. The −5V negative bias is essential.

> [!tip] Negative Gate Bias is Critical for SiC
> SiC MOSFETs have lower threshold voltages (2.5–4V) compared to Si IGBTs (5–7V). Without negative gate bias during off-state, dV/dt-induced Miller current can easily push the gate above threshold and cause shoot-through. The STGAP2SiC's VNEG supply (−5V) provides this protection. **Never omit the negative gate supply.**

## 6. Kelvin Source Connection

### Why Kelvin Source Matters

The TO-247-4 package has a dedicated 4th pin — the Kelvin source. This pin connects directly to the MOSFET die source bond wire with minimal inductance, bypassing the power source pin's package inductance (5–8 nH).

Without Kelvin source:
- Gate loop includes the power source inductance (5–8 nH)
- At 10 A/ns switching, the source inductance develops 50–80V, opposing gate drive
- Effective gate voltage reduced, switching slows dramatically
- Worse: during turn-off, source inductance boosts gate voltage, risking parasitic turn-on

With Kelvin source:
- Gate loop uses the low-inductance Kelvin path (<0.5 nH)
- Gate drive voltage is accurately applied to Vgs
- Fast, clean switching with predictable dV/dt

### Kelvin Source Routing Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| Kelvin source trace connects to | STGAP2SiC output return (source) pin only | Dedicated gate return path |
| Kelvin source trace must NOT connect to | Power source copper pour | Would couple power dI/dt noise into gate |
| Trace routing | L1 only, <5 mm, directly from pin 4 to driver | Minimum inductance |
| Trace width | 0.3–0.5 mm | Signal-level current only (gate charge/discharge) |
| Ground reference | Kelvin source is the local ground for the driver secondary side | All driver decoupling returns to Kelvin source |

```
    TO-247-4 Pin Assignment:

    Pin 1: Gate ─────────────── to Rg_on
    Pin 2: Drain ────────────── to DC bus / switching node
    Pin 3: Source (POWER) ───── to power copper pour (high current)
    Pin 4: Kelvin Source ────── to STGAP2SiC return (gate loop ONLY)
                                 │
                                 ├── VDRV decoupling return
                                 ├── VNEG decoupling return
                                 └── DESAT sense return
```

> [!warning] Kelvin Source Isolation
> The Kelvin source trace must be **electrically isolated** from the power source copper pour on L1. Use a clearance of ≥1 mm between the Kelvin source trace and the power source pour. If they connect at any point, the benefit of the Kelvin source is lost because power loop dI/dt will couple into the gate loop.

## 7. Driver Decoupling

### VDRV Supply (Positive Gate Drive, +15V to +20V)

| Component | Value | Dielectric | Package | Placement |
|-----------|-------|-----------|---------|-----------|
| C_VDRV_1 | 100 nF | C0G / NP0 | 0402 or 0603 | <3 mm from VDRV pin |
| C_VDRV_2 | 10 µF | X5R | 0805 or 1206 | <5 mm from VDRV pin |

The 100 nF C0G provides the high-frequency decoupling for the 4A gate current pulses. The 10 µF X5R provides bulk energy storage to prevent VDRV droop during the gate charge pulse.

**VDRV droop check:**

$$\Delta V_{DRV} = \frac{Q_g}{C_{local}} = \frac{200 \text{ nC}}{10 \text{ µF}} = 0.02 \text{ V}$$

A 20 mV droop is negligible. The 10 µF is adequate.

### VNEG Supply (Negative Gate Drive, −3V to −5V)

| Component | Value | Dielectric | Package | Placement |
|-----------|-------|-----------|---------|-----------|
| C_VNEG_1 | 100 nF | C0G / NP0 | 0402 or 0603 | <3 mm from VNEG pin |
| C_VNEG_2 | 4.7 µF | X5R | 0603 or 0805 | <5 mm from VNEG pin |

### VCC Supply (Primary Side Logic, 3.3V or 5V)

| Component | Value | Dielectric | Package | Placement |
|-----------|-------|-----------|---------|-----------|
| C_VCC | 100 nF | X7R | 0402 | <3 mm from VCC pin |

### Decoupling Return Path

**All secondary-side decoupling capacitors (VDRV, VNEG) must return to the Kelvin source net**, not to the power source or a generic ground pour. This ensures the decoupling current loop is contained within the gate drive circuit and does not inject noise into other circuits.

```
    VDRV ──┤C_VDRV_1├──┤C_VDRV_2├── Kelvin Source
    VNEG ──┤C_VNEG_1├──┤C_VNEG_2├── Kelvin Source
```

## 8. dV/dt Immunity Layout Measures

The switching node transitions at 35 kV/µs or more. Capacitive coupling from the switching node to the gate driver can cause malfunction. The following layout measures mitigate this risk:

### 1. No Copper Across the Isolation Gap

The STGAP2SiC SO-8W package has primary-side pins (1–4) and secondary-side pins (5–8) separated by a molded isolation gap. On the PCB:

| Rule | Requirement |
|------|-------------|
| No copper traces | Between primary-side pads and secondary-side pads on any layer |
| No copper pours | Beneath the isolation gap on L2, L3, L4, L5 |
| No vias | Beneath the package body in the isolation gap zone |
| Clearance zone | ≥1 mm beyond the package body outline on all layers |

### 2. PCB Slot Under Driver

A routed slot in the PCB beneath the STGAP2SiC isolation gap dramatically increases the creepage and clearance across the isolation barrier:

| Parameter | Value |
|-----------|-------|
| Slot width | 1.5 mm |
| Slot length | Equal to the driver package width (~6 mm) |
| Slot position | Centered under the isolation gap (between pins 1–4 and 5–8) |
| Copper keepout around slot | 0.5 mm on all layers |

> [!warning] Structural Integrity
> PCB slots reduce mechanical strength. Do not place mounting holes, connectors, or heavy components near a slotted area. Verify with the PCB fabricator that the slot can be routed with acceptable tolerances (typically ±0.1 mm).

### 3. Minimum Distance from Switching Node

| Distance from switching node copper | Action |
|-------------------------------------|--------|
| 0–3 mm | **Forbidden zone** — no driver placement allowed |
| 3–5 mm | Marginal — acceptable only with PCB slot and guard ring |
| ≥5 mm | Acceptable — standard placement |
| ≥10 mm | Preferred — maximum dV/dt rejection |

### 4. Common-Mode Current from Driver Parasitic Capacitance

Each STGAP2SiC has a parasitic capacitance across the isolation barrier (Cdh ≈ 5 pF typical). When the switching node transitions at high dV/dt, this capacitance injects CM current:

$$I_{CM\_driver} = C_{dh} \times \frac{dV}{dt} = 5 \text{ pF} \times 35 \text{ kV/µs} = 0.175 \text{ A per driver}$$

For 6 drivers total:

$$I_{CM\_total\_drivers} = 6 \times 0.175 = **1.05 \text{ A}**$$

This 1 A of CM current must return through the EMI filter Y-capacitors and chassis ground. It contributes to conducted emissions and must be included in the EMI filter design. See [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout]] for the complete CM current budget.

## 9. SPI Bus Routing (Primary Side)

The STGAP2SiC supports SPI configuration on the primary (low-voltage) side. For a 6-driver daisy chain:

### SPI Routing Rules

| Rule | Requirement |
|------|-------------|
| Layer | L3 (signal layer) exclusively |
| Trace width | 0.2 mm |
| Spacing from high-voltage | ≥2 mm from any secondary-side copper |
| Clock frequency | ≤5 MHz (STGAP2SiC limit) |
| Trace length matching | Not required at ≤5 MHz |
| Bypass caps | 100 nF on VCC at each driver (already specified above) |
| Pull-up/pull-down | Per STGAP2SiC datasheet recommendations |

### Daisy Chain Topology

```
    MCU SPI ──→ U1 ──→ U2 ──→ U3 ──→ U4 ──→ U5 ──→ U6
      │                                              │
      └──────────────── SDO return ───────────────────┘
```

Route the SPI bus on L3, keeping it physically separated from all secondary-side (high-voltage) copper by at least 2 mm on every layer.

## 10. DESAT Detection Routing

The STGAP2SiC includes desaturation detection (DESAT) for short-circuit protection. The DESAT pin connects to the MOSFET drain through a high-voltage diode and sense resistor.

### DESAT Layout Rules

| Rule | Requirement |
|------|-------------|
| DESAT diode placement | <5 mm from DESAT pin |
| DESAT trace | Short, guarded, on L1 |
| DESAT trace routing | Away from gate drive traces (different side of driver) |
| Sense resistor | 0402 or 0603, placed adjacent to DESAT pin |
| HV diode voltage rating | ≥1200V (must withstand full bus voltage) |

> [!tip] DESAT Noise Immunity
> The DESAT input is sensitive to noise. Route the DESAT trace on L1 with a ground guard ring on L2 beneath it. Keep the trace short and away from the switching node copper. Use the STGAP2SiC's programmable blanking time (via SPI) to filter legitimate switching transients.

## 11. Thermal Management

Gate driver ICs dissipate power from:
1. Gate charge delivery: P_gate = Qg × (VDRV − VNEG) × fsw = 200 nC × 23V × 65 kHz = **0.3 W per driver**
2. Quiescent current: P_q ≈ 5 mA × 5V = 0.025 W
3. Total per driver: **~0.33 W**
4. Total for 6 drivers: **~2 W**

See [[07-PCB-Layout/AC-DC/04-Thermal Layout]] for the driver thermal management specification (15×15 mm copper pour + 9 thermal vias per driver, target Rth_jA ~60–80°C/W).

## 12. Layout Checklist

- [ ] Each STGAP2SiC placed ≤15 mm from its MOSFET
- [ ] Gate trace length <5 mm (OUTH to gate pin)
- [ ] Kelvin source trace isolated from power source copper (≥1 mm gap)
- [ ] Rg_on + Schottky steering + Rg_off within 2 mm of each other
- [ ] VDRV decoupling: 100 nF C0G <3 mm + 10 µF X5R <5 mm from pin
- [ ] VNEG decoupling: 100 nF C0G <3 mm + 4.7 µF X5R <5 mm from pin
- [ ] All secondary decoupling returns to Kelvin source net
- [ ] No copper across isolation gap on any layer
- [ ] PCB slot under each driver (1.5 mm wide)
- [ ] ≥5 mm from switching node copper to driver body
- [ ] SPI bus on L3, ≥2 mm from HV copper
- [ ] DESAT trace short, guarded, on L1

## 13. Cross-References

- [[__init]] — Board overview and driver IC summary
- [[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment]] — Layer assignments for gate traces
- [[07-PCB-Layout/AC-DC/02-Power Loop Analysis]] — Power loop (separate from gate loop)
- [[07-PCB-Layout/AC-DC/04-Thermal Layout]] — Driver IC thermal management
- [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout]] — CM current contribution from driver Cdh
- [[07-PCB-Layout/AC-DC/06-Creepage and Clearance]] — Isolation gap and slot dimensions
- [[01-Topology Selection]] — STGAP2SiC selection rationale
- [[SiC Device Thermal Parameters]] — MOSFET gate charge data

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
