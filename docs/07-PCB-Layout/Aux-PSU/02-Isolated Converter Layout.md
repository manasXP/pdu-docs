---
tags: [pdu, pcb-layout, aux-psu, flyback, transformer, magnetics, isolation]
created: 2026-02-22
status: draft
---

# 02 — Isolated Converter Layout

## Purpose

This document specifies the layout of the isolated flyback converter that forms the heart of the Aux PSU board. The flyback topology is used because it naturally supports multiple isolated outputs from a single transformer, making it ideal for generating the diverse rail voltages required by the PDU system (+18 V, −5 V, +12 V, +5 V, +3.3 V, standby).

The primary layout challenges are:
1. Positioning the flyback transformer **across the isolation barrier** (4 mm PCB slot)
2. Minimizing the primary switching loop inductance to control voltage spikes
3. Placing the RCD clamp snubber close to the transformer primary to absorb leakage inductance energy
4. Routing multiple secondary windings to their respective rectifiers without crossing isolation domain boundaries

## Topology Selection — Multi-Output Flyback

### Why Flyback?

| Factor | Flyback Advantage | Alternative Disadvantage |
|--------|-------------------|--------------------------|
| Multiple outputs | Single transformer with multiple secondary windings | Forward converter needs individual LC filters per output; LLC needs additional post-regulators |
| Low power (15–25 W) | Flyback is cost-effective and simple below 50 W | LLC is overkill at this power level; adds complexity |
| Wide input range (400–920 V) | Flyback handles wide input with duty cycle variation | Resonant converters have narrower efficient operating range |
| Isolation | Transformer provides galvanic isolation inherently | Discrete DC-DC modules add cost at ~$5–8 per channel |
| Component count | One MOSFET, one transformer, few rectifiers | Multiple module approach requires 4–5 separate converters |

### Key Converter Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Input voltage | 400–920 VDC | From DC bus (see [[00-Board Partitioning]]) |
| Switching frequency | 65 kHz (QR mode, variable up to 130 kHz at light load) | Quasi-resonant for low switching loss |
| Primary MOSFET | 1200 V SiC or 1500 V Si superjunction | Single device, TO-263 or D2PAK |
| Controller IC | UCC28C44 or similar peak-current-mode | Primary-side regulation with optocoupler feedback |
| Transformer | EE25 or EFD25 core, 6-pin bobbin (minimum) | Through-hole; primary on one bobbin side, secondaries on the other |
| Clamp | RCD clamp (R + C + ultrafast diode) | Absorbs leakage inductance energy |
| Maximum duty cycle | 0.45 (at minimum input voltage) | Continuous conduction mode at full load |

> [!tip] Quasi-Resonant Operation
> At 920 V input, the flyback operates in discontinuous conduction mode (DCM) with valley switching. This reduces turn-on switching loss in the primary MOSFET. The switching frequency varies between 65 kHz (full load, low input) and 130 kHz (light load, high input). Layout must accommodate the higher harmonic content at 130 kHz.

## Component Placement Strategy

### Overall Placement

The flyback converter components straddle the isolation barrier, with the transformer centered on the 4 mm PCB slot:

```
        PRIMARY SIDE                    SECONDARY SIDE
        (~35 mm)                        (~61 mm)

   ┌─────────────────╥──────────────────────────────┐
   │                 ║                              │
   │  ┌───┐  ┌───┐  ║  ┌───┐  ┌───┐  ┌───┐       │
   │  │C_in│  │R_C│  ║  │D_A│  │D_B│  │D_C│       │
   │  │    │  │D_C│  ║  │   │  │   │  │   │       │
   │  └───┘  │C_C│  ║  └───┘  └───┘  └───┘       │
   │         └───┘  ║                              │
   │  ┌───┐         ╠═══════╗                      │
   │  │ Q1│  ┌──────╫─XFMR──╫────┐                │
   │  │FET│  │ PRI  ╫  T1   ╫ SEC│                │
   │  └───┘  └──────╫───────╫────┘                │
   │         ┌───┐  ╠═══════╝                      │
   │  ┌───┐  │R_s│  ║  ┌───┐  ┌───┐  ┌───┐       │
   │  │U1 │  │   │  ║  │L_A│  │L_B│  │L_C│       │
   │  │PWM│  └───┘  ║  └───┘  └───┘  └───┘       │
   │  └───┘         ║                              │
   │  ┌───┐  ┌───┐  ║  ┌───┐  ┌───┐  ┌───┐       │
   │  │C_b│  │OPT│──║──│OPT│  │C_oA│ │C_oB│      │
   │  └───┘  └───┘  ║  └───┘  └───┘  └───┘       │
   │                 ║                              │
   └─────────────────╨──────────────────────────────┘

   C_in = Input cap           D_A/B/C = Rectifier diodes
   Q1   = Primary MOSFET      L_A/B/C = Output inductors
   U1   = PWM controller      C_oA/B/C = Output caps
   R_C/D_C/C_C = RCD clamp    OPT = Optocoupler (bridges barrier)
   R_s  = Current sense        C_b = Bias cap
```

### Transformer Placement — The Critical Decision

The flyback transformer T1 is the **only power component that physically bridges the isolation barrier**. Its placement drives the entire board layout:

| Requirement | Specification |
|-------------|---------------|
| Transformer position | Centered on the 4 mm PCB slot |
| Primary winding pins | On the primary side of the slot (L1/L4 pads) |
| Secondary winding pins | On the secondary side of the slot (L1/L4 pads) |
| Mounting | Through-hole pins into plated through-holes |
| Pin-to-slot clearance | Each pin must maintain 5 mm from the nearest slot edge (creepage path) |
| Core footprint | Must not overhang the slot edges by more than the core body width |
| Bobbin creepage | Transformer bobbin must provide ≥14 mm creepage between primary and secondary winding terminals per IEC 62368-1 |

```
    Side view — Transformer T1 on PCB slot:

              Transformer Core (EE25)
           ┌──────────────────────────┐
           │  ┌──PRI──┐  ┌──SEC──┐   │
           │  │winding │  │winding│   │
           │  └────────┘  └───────┘   │
    ───────┤                          ├───────  ← PCB L1
    ═══════╪══════════════════════════╪═══════  ← 4mm slot
    ───────┤                          ├───────  ← PCB L4 (optional)
           │   PRI pins     SEC pins  │
           └──────────────────────────┘

    ←─PRI SIDE─→│← 4mm →│←─SEC SIDE──→
                  slot
```

> [!warning] Transformer Safety Compliance
> The flyback transformer is a **safety-critical component**. It must comply with IEC 61558-2-16 (or UL 5085-3) for reinforced insulation between primary and secondary windings. The transformer datasheet or test report must document:
> - Creepage and clearance between primary and secondary terminals (≥14 mm on bobbin)
> - Dielectric withstand between primary and secondary (4000 VAC, 60 s)
> - Triple-insulated wire for secondary winding (if wound over primary)
> - Safety agency approval marks (UL, VDE, or equivalent)

### Primary Side Component Placement

#### Input Capacitor (C_in)

| Parameter | Specification |
|-----------|---------------|
| Location | Within 10 mm of Q1 drain and transformer primary pin 1 |
| Type | Ceramic (X7R or C0G) 1 uF 1000 V + film 10 uF 450 V |
| Purpose | Decouple the primary switching loop from the DC bus |
| Placement priority | **Highest on primary side** — this cap defines the primary loop area |

#### Primary MOSFET (Q1)

| Parameter | Specification |
|-----------|---------------|
| Package | TO-263 (D2PAK) or TO-252 (DPAK) for SMD; TO-220 for THT |
| Location | Adjacent to transformer primary pin, <15 mm lead-to-lead |
| Orientation | Drain toward transformer, source toward current sense resistor |
| Thermal pad | Connected to PRI_GND via thermal via array (see [[03-Thermal Layout]]) |

#### RCD Clamp Circuit

| Parameter | Specification |
|-----------|---------------|
| Components | R_clamp (100 kohm 1W), C_clamp (1–10 nF 1000V), D_clamp (ultrafast, 1000V) |
| Location | **Within 5 mm of transformer primary winding pin** |
| Clamp diode anode | Connected to transformer primary (drain side) |
| Clamp diode cathode | Connected to C_clamp/R_clamp junction |
| Loop area | Minimize clamp loop — D_clamp → C_clamp → T1 primary pin → D_clamp must form a tight loop |

> [!warning] Clamp Placement is Safety-Critical
> If the clamp is too far from the transformer primary, the leakage inductance spike on the drain of Q1 will exceed the MOSFET's breakdown voltage rating. At 920 V input, the drain voltage can reach 1400–1600 V during the leakage spike. The 1200 V or 1500 V MOSFET has very little margin. Place the clamp **as close as physically possible** to the transformer primary pin and the MOSFET drain.

#### PWM Controller (U1)

| Parameter | Specification |
|-----------|---------------|
| Package | SOIC-8 or SOIC-16 |
| Location | Primary side, >10 mm from switching node (EMI susceptibility) |
| Decoupling | 100 nF + 10 uF within 3 mm of VCC pin |
| Current sense | R_sense connected between Q1 source and PRI_GND, routed as Kelvin pair to CS pin |
| RT/CT | Timing components within 5 mm of RT/CT pins |

### Secondary Side Component Placement

Each secondary output has its own rectifier diode (or synchronous MOSFET), output inductor (for LC filter), and output capacitors. These must be placed within their respective isolation domains.

#### Rectifier Diodes (D_A, D_B, D_C)

| Output | Diode Type | Package | Placement |
|--------|-----------|---------|-----------|
| +18 V / −5 V (AC-DC) | Schottky or ultrafast, 100 V | SMA or SMB | Within 5 mm of corresponding transformer secondary pin |
| +18 V / −5 V (DC-DC) | Schottky or ultrafast, 100 V | SMA or SMB | Within 5 mm of corresponding transformer secondary pin |
| +12 V / aux winding | Schottky, 30–40 V | SMA | Within 5 mm of transformer secondary pin |

> [!tip] Diode Orientation for Low Loop Area
> Orient each rectifier diode so the anode-to-cathode direction follows the shortest path from the transformer secondary pin to the output capacitor. The secondary rectification loop (transformer secondary → diode → output cap → transformer return) should enclose the smallest possible area on L1.

#### Output Inductors (L_A, L_B, L_C)

Post-rectification LC filter inductors for each output rail:

| Output | Inductor Value | Package | Placement |
|--------|---------------|---------|-----------|
| +18 V (each channel) | 22–47 uH, 1 A | Shielded SMD (e.g., Wurth WE-PD) | Between rectifier diode and output caps |
| +12 V | 10–22 uH, 3 A | Shielded SMD | Between rectifier and output caps |
| +5 V | Fed from LDO, no separate inductor | — | — |

#### Output Capacitors

See [[04-Output Filtering and Regulation]] for detailed capacitor selection per rail.

## Primary Switching Loop Optimization

The primary switching loop is the most EMI-critical loop on the Aux PSU board. It consists of:

```
Primary switching loop (minimize this area):

    C_in (+) ──→ T1 primary pin 1 ──→ T1 primary pin 2 ──→ Q1 drain
       ↑                                                      │
       │                                                      │
    C_in (−) ←──────── R_sense ←──────── Q1 source ←──────────┘

    ← Total loop path length: target <30 mm →
    ← Enclosed loop area: target <2 cm² →
```

### Loop Inductance Budget

| Element | Estimated Inductance | Notes |
|---------|---------------------|-------|
| Input capacitor (C_in) ESL | 1–3 nH | Use ceramic X7R, 1206 or smaller |
| PCB trace C_in → T1 pin 1 | 2–4 nH | <5 mm trace, L1 over L2 GND |
| Transformer leakage | 2–5 uH | **Not part of switching loop per se — absorbed by clamp** |
| PCB trace T1 pin 2 → Q1 drain | 2–4 nH | <10 mm trace |
| Q1 package inductance | 2–5 nH | TO-263: ~3 nH; TO-220: ~5 nH |
| PCB trace Q1 source → R_s → C_in | 3–5 nH | <15 mm total path |
| **Total PCB contribution** | **<15 nH target** | Excluding transformer leakage |

### Layout Rules for Primary Loop

1. **C_in directly adjacent to T1 and Q1** — the three components form a tight triangle on L1
2. **Return path on L2** — PRI_GND copper pour directly beneath the L1 primary loop traces
3. **No vias in the switching loop** — keep the entire primary loop on L1 where possible
4. **Short, wide traces** — 2 oz copper, minimum 1 mm width for primary current path
5. **Current sense resistor in the return path** — R_sense between Q1 source and PRI_GND, not in the drain path

```
    Optimized primary loop layout (L1 top view):

    ┌──────────────────────────────────┐
    │                                  │
    │   ┌────┐      ┌───────────┐     │
    │   │C_in│──────│ T1 Pri    │     │
    │   │1uF │ <5mm │ Pin 1     │     │
    │   │    │──┐   │           │     │
    │   └────┘  │   │  Pin 2 ───│──┐  │
    │           │   └───────────┘  │  │
    │     ┌─────┘                  │  │
    │     │  ┌────┐     ┌─────┐   │  │
    │     └──│R_s │─────│ Q1  │───┘  │
    │        │10mΩ│     │ FET │      │
    │        └────┘     └─────┘      │
    │                                  │
    │   Total loop area: <2 cm²       │
    └──────────────────────────────────┘
```

## Clamp Snubber Layout Detail

The RCD clamp must intercept the leakage inductance energy spike immediately as Q1 turns off. Placement tolerance is critical:

| Rule | Specification |
|------|---------------|
| D_clamp anode to T1 primary pin 2 | <5 mm trace length |
| D_clamp cathode to C_clamp | <3 mm |
| C_clamp to R_clamp | <5 mm |
| R_clamp return to C_in positive | <10 mm |
| Clamp loop area | <1 cm² |

```
    Clamp circuit placement (L1):

         T1 Pin 2 (primary, drain side)
              │
              │ <5mm
              ↓
         ┌─────────┐
         │ D_clamp │ (ultrafast, 1000V)
         └────┬────┘
              │ <3mm
         ┌────┴────┐
         │ C_clamp │ (1-10nF, 1000V)
         └────┬────┘
              │ <5mm
         ┌────┴────┐
         │ R_clamp │ (100kΩ, 1W)
         └────┬────┘
              │
              → to DC bus (C_in positive)
```

> [!tip] Clamp Resistor Power Rating
> The clamp resistor dissipates the leakage inductance energy: $P_{clamp} = \frac{1}{2} L_{leak} \cdot I_{pk}^2 \cdot f_{sw}$. At worst case (920 V input, 65 kHz, ~0.5 A peak, ~5 uH leakage), this is approximately 0.04 W — negligible. However, use a 1 W resistor for margin and to handle transient overloads during startup. A 1206 or 2010 SMD resistor is adequate.

## Multiple Secondary Windings — Routing Strategy

The transformer has multiple secondary windings, each routed to its respective isolation domain:

| Winding | Pins | Domain | Route To |
|---------|------|--------|----------|
| SEC-A (+18 V / −5 V AC-DC) | S1, S2, CT_A | Gate Drive A zone | D_A rectifiers, then L_A, C_oA |
| SEC-B (+18 V / −5 V DC-DC) | S3, S4, CT_B | Gate Drive B zone | D_B rectifiers, then L_B, C_oB |
| SEC-C (+12 V / +5 V logic) | S5, S6 | Logic zone | D_C rectifier, then L_C, C_oC |
| AUX (bias winding) | AUX1, AUX2 | Primary side | VCC for PWM controller |

### Routing Rules for Secondary Windings

1. Each secondary winding pair must route **directly** from the transformer pin to its domain — no crossing through other domains
2. Secondary winding traces must maintain the domain-to-domain functional isolation gap (1 mm minimum)
3. The center-tap (if used) of each +18 V / −5 V pair is the return for that domain (RTN_AC or RTN_DC)
4. The bias winding routes entirely on the primary side — it does not cross the isolation barrier

## Optocoupler Feedback Path

The output voltage feedback from the secondary to the primary uses an optocoupler that bridges the isolation barrier:

| Parameter | Specification |
|-----------|---------------|
| Component | PC817 or equivalent (CTR > 100%) |
| Package | DIP-4 or SMD-4 (SOP-4) |
| Placement | Straddling the isolation barrier, similar to the transformer |
| LED side (secondary) | Connected to TL431 voltage reference in the logic domain |
| Phototransistor side (primary) | Connected to U1 (PWM controller) FB/COMP pin |
| Creepage | Optocoupler package must provide ≥14 mm creepage (reinforced) |
| PCB pads | LED pads on secondary side, phototransistor pads on primary side of slot |

> [!warning] Optocoupler Creepage
> Standard DIP-4 optocouplers have pin-to-pin distance of only 7.62 mm — insufficient for reinforced insulation at 920 V. Use a **wide-body** optocoupler package (e.g., LSOP-6 with 8 mm lead spacing) or a dedicated safety-rated optocoupler (e.g., Broadcom ACPL-xxx series with 8 mm minimum creepage). Alternatively, route the optocoupler pads with extended creepage traces and use the PCB slot to supplement the package creepage.

## Design Verification Checklist

- [ ] Primary switching loop enclosed area <2 cm², path length <30 mm
- [ ] C_in within 10 mm of both T1 primary pin 1 and Q1 drain
- [ ] Clamp diode within 5 mm of T1 primary pin 2
- [ ] Transformer centered on PCB slot, all primary pins on primary side, all secondary pins on secondary side
- [ ] Optocoupler package provides reinforced insulation creepage (≥14 mm)
- [ ] Each secondary winding routes entirely within its assigned domain
- [ ] No copper or solder mask bridges across the 4 mm PCB slot (except designated component pads)
- [ ] Primary loop return path on L2 (PRI_GND) directly beneath L1 switching loop traces
- [ ] All primary-side components maintain 14 mm creepage to any secondary-side copper

## Cross-References

- [[__init]] — Board overview, output rails, isolation domains
- [[01-Stack-Up and Layer Assignment]] — Layer assignments, split ground plane
- [[03-Thermal Layout]] — Primary MOSFET and rectifier diode thermal management
- [[04-Output Filtering and Regulation]] — Output capacitor and filter design per rail
- [[05-Safety and Isolation]] — Reinforced insulation requirements, creepage distances
- [[00-Board Partitioning]] — P4/P5 connector definitions, inter-board interfaces

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: flyback layout, primary loop, clamp placement, transformer positioning |
