---
tags: [pdu, pcb-layout, dc-dc, llc, stack-up, ipc-2152]
created: 2026-02-22
status: draft
---

# 01 — Stack-Up and Layer Assignment

## 1. Purpose

This document defines the 6-layer PCB stack-up for the DC-DC LLC resonant converter board. The stack-up is **standardized with the AC-DC board** (see [[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment|AC-DC Stack-Up]]) to unify fabrication specifications across both power boards in the PDU.

## 2. 6-Layer Stack-Up Definition

### Cross-Section

```
         ┌─────────────────────────────────────┐
  L1     │  Top Power               2 oz Cu    │  35 µm × 2 = 70 µm
         ├─────────────────────────────────────┤
         │  Prepreg (7628)          0.20 mm    │
         ├─────────────────────────────────────┤
  L2     │  Continuous GND          2 oz Cu    │  70 µm
         ├─────────────────────────────────────┤
         │  Core (FR-4)             0.36 mm    │
         ├─────────────────────────────────────┤
  L3     │  Signal                  1 oz Cu    │  35 µm
         ├─────────────────────────────────────┤
         │  Prepreg (2116)          0.10 mm    │
         ├─────────────────────────────────────┤
  L4     │  Signal / Power Return   1 oz Cu    │  35 µm
         ├─────────────────────────────────────┤
         │  Core (FR-4)             0.36 mm    │
         ├─────────────────────────────────────┤
  L5     │  Power Plane             2 oz Cu    │  70 µm
         ├─────────────────────────────────────┤
         │  Prepreg (7628)          0.20 mm    │
         ├─────────────────────────────────────┤
  L6     │  Bottom Power            2 oz Cu    │  70 µm
         └─────────────────────────────────────┘

  Total board thickness: ~1.6 mm (±10%)
```

### Layer Assignment Table

| Layer | Name | Weight | Primary Function (DC-DC Board) |
|-------|------|--------|-------------------------------|
| L1 | Top Power | 2 oz | Primary H-bridge copper pours, secondary rectifier pours, bus bar landing pads, snubber components |
| L2 | Continuous GND | 2 oz | **Unbroken** ground reference plane. Primary GND and secondary GND are separate — connected only at a single star point or through isolation barrier |
| L3 | Signal | 1 oz | Gate driver signals (PWM, DESAT fault), current/voltage sense, SPI/I2C control bus, temperature sensor routing |
| L4 | Signal / Power Return | 1 oz | Auxiliary power rails (15V, 5V, 3.3V isolated supplies), additional signal routing, secondary-side control |
| L5 | Power Plane | 2 oz | DC bus positive (920V) distribution, output bus distribution, power return planes |
| L6 | Bottom Power | 2 oz | DC bus return, output return, additional current-carrying copper, heatsink interface pads |

> [!warning] L2 Ground Plane Integrity
> The L2 GND plane is the **single most critical layer** for EMI performance. It must remain continuous across the entire board with the sole exception of the **primary-secondary isolation slot**. No signal traces, no vias (except stitching vias), and no splits are permitted on L2. Any GND plane breach under a high-dV/dt node will create CM noise injection.

### Impedance Targets

| Trace Type | Layers | Target Z₀ | Width (1 oz) | Width (2 oz) |
|------------|--------|-----------|-------------|-------------|
| Single-ended signal | L3 (ref L2) | 50 Ω | ~0.28 mm | N/A |
| Differential pair (gate) | L3 (ref L2) | 100 Ω diff | ~0.20 mm / 0.15 mm gap | N/A |
| Single-ended signal | L4 (ref L5) | 50 Ω | ~0.28 mm | N/A |
| Power (low impedance) | L1/L6 | N/A (pour) | Per IPC-2152 | Per IPC-2152 |

> [!tip] Impedance Control
> Request impedance-controlled fabrication for L3 and L4. The fab house will adjust prepreg thickness slightly to hit 50 Ω. Specify Dk = 4.2–4.5 for FR-4 at 100 kHz–1 MHz (LLC switching range).

## 3. Board Zone Map — Detailed

The 250 mm × 180 mm board area is divided into functional zones arranged for optimal power flow and thermal management. The **primary-to-secondary isolation barrier** runs horizontally across the board, creating two electrically isolated halves.

### Zone Dimensions and Allocation

| Zone | Y-Position | Height | Width | Area | Function |
|------|-----------|--------|-------|------|----------|
| DC Bus Input | 0–40 mm | 40 mm | 250 mm | 100 cm² | Bus bar connector P2, DC bus capacitors |
| LLC Primary Bridge | 40–120 mm | 80 mm | 250 mm | 200 cm² | 3× half-bridges, gate drivers, resonant tanks |
| Isolation Barrier | ~120 mm | 3–5 mm | 250 mm | — | PCB slot, no copper crossing |
| Transformer Mount | 115–175 mm | 60 mm | 250 mm | 150 cm² | 3× transformer cutouts/mounting |
| Secondary Rectifier | 140–190 mm | 50 mm | 250 mm | 125 cm² | 3× sync rectifiers, gate drivers, output caps |
| Output | 165–180 mm | 30 mm | 250 mm | 75 cm² | Combined output capacitors, P3 connector |

> [!note] Zone Overlap
> The transformer zone overlaps with both primary and secondary zones because the transformer straddles the isolation barrier. The transformer primary pins land in the primary zone, and the secondary pins land in the secondary zone, with the isolation barrier passing through or around the transformer footprint.

### Detailed Zone Layout (Top View)

```
 0mm ┌──────────────────────── 250mm ────────────────────────────┐
     │                    DC BUS INPUT ZONE                       │
     │  ┌──────┐                                                  │
     │  │ P2   │  [C1][C2][C3]  [C4][C5][C6]  [C7][C8][C9]     │
     │  │BusBar│   Phase A        Phase B        Phase C          │
     │  └──────┘  decoupling     decoupling     decoupling        │
40mm ├────────────────────────────────────────────────────────────┤
     │                LLC PRIMARY BRIDGE ZONE                      │
     │                                                             │
     │  ┌──Phase A──────┐  ┌──Phase B──────┐  ┌──Phase C──────┐  │
     │  │ Q1A    Q2A    │  │ Q1B    Q2B    │  │ Q1C    Q2C    │  │
     │  │ [DrvA_hi]     │  │ [DrvB_hi]     │  │ [DrvC_hi]     │  │
     │  │ [DrvA_lo]     │  │ [DrvB_lo]     │  │ [DrvC_lo]     │  │
     │  │               │  │               │  │               │  │
     │  │ Lr_A   Cr_A   │  │ Lr_B   Cr_B   │  │ Lr_C   Cr_C   │  │
     │  │ [snub] [snub] │  │ [snub] [snub] │  │ [snub] [snub] │  │
     │  └───────────────┘  └───────────────┘  └───────────────┘  │
     │                                                             │
115mm│═══════════ ISOLATION BARRIER (PCB SLOT 3-5mm) ════════════│
     │                                                             │
     │  ┌──TX_A─────┐     ┌──TX_B─────┐     ┌──TX_C─────┐      │
     │  │ [cutout]  │     │ [cutout]  │     │ [cutout]  │      │
     │  │ pri  sec  │     │ pri  sec  │     │ pri  sec  │      │
     │  └───────────┘     └───────────┘     └───────────┘      │
     │            TRANSFORMER MOUNTING ZONE                       │
     ├────────────────────────────────────────────────────────────┤
     │              SECONDARY RECTIFIER ZONE                       │
     │  ┌──Phase A──────┐  ┌──Phase B──────┐  ┌──Phase C──────┐  │
     │  │ Q3A    Q4A    │  │ Q3B    Q4B    │  │ Q3C    Q4C    │  │
     │  │ [DrvA_sec]    │  │ [DrvB_sec]    │  │ [DrvC_sec]    │  │
     │  │ C_out_A       │  │ C_out_B       │  │ C_out_C       │  │
     │  └───────────────┘  └───────────────┘  └───────────────┘  │
     ├────────────────────────────────────────────────────────────┤
     │                    OUTPUT ZONE                              │
     │  [C_out_combined ×N]  ┌──────┐  [Sense] [Ctrl]           │
     │                       │ P3   │                             │
     │                       │BusBar│                             │
     │                       └──────┘                             │
180mm└────────────────────────────────────────────────────────────┘
```

### Per-Phase Allocation

Each of the 3 phases occupies approximately **80 mm × 60 mm** in the primary bridge zone and **80 mm × 45 mm** in the secondary rectifier zone. The phases are spaced equally across the 250 mm board width:

| Phase | X-Center | Primary Width | Secondary Width |
|-------|----------|---------------|-----------------|
| A | 42 mm | 80 mm | 80 mm |
| B | 125 mm | 80 mm | 80 mm |
| C | 208 mm | 80 mm | 80 mm |

> [!tip] Phase Symmetry
> All three phases must be **mirror-symmetric** in layout. Use KiCad's "Replicate Layout" feature: design Phase A completely, then replicate to Phase B and Phase C with identical component placement and routing. This ensures matched parasitic inductances and balanced current sharing. See [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] for inductance matching requirements.

## 4. Transformer Cutout / Mounting

The transformer mounting strategy is the single biggest board-level mechanical decision. Two approaches are under consideration:

### Option A: Through-Board Cutout

| Parameter | Specification |
|-----------|--------------|
| Cutout size | 40 mm × 35 mm per transformer (3 cutouts total) |
| Cutout spacing | 5 mm clearance from nearest copper pour |
| Pin landing | Through-hole pins on primary and secondary sides of the cutout |
| Mounting | Mechanical brackets or adhesive from underside |
| Advantage | Lower profile, better thermal coupling to chassis heatsink |
| Disadvantage | Removes board area, complicates routing, weakens board mechanically |

### Option B: On-Board Surface Mount (Planar Transformer)

| Parameter | Specification |
|-----------|--------------|
| Footprint | 50 mm × 40 mm per transformer |
| Pin count | ~12–16 pins (primary + secondary + aux winding) |
| PCB integration | Windings partially implemented as PCB traces on L1/L6 |
| Mounting | Soldered and/or mechanically clamped |
| Advantage | No cutout, integrated windings reduce assembly |
| Disadvantage | Larger footprint, higher profile, limited power handling |

> [!note] Decision Pending
> The transformer mounting method is tracked as an open issue in [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]]. Either approach must maintain the **4 kV primary-secondary isolation** requirement. See [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] for isolation barrier requirements around the transformer.

## 5. IPC-2152 Trace and Pour Sizing

All current-carrying conductors are sized per **IPC-2152** (2009) for the specified current, copper weight, and allowable temperature rise. The target temperature rise is **30°C** above ambient for internal layers and **20°C** for external layers (more conservative for external due to proximity to other components).

### External Layers (L1, L6) — 2 oz Cu

| Net | Current (A) | Temp Rise (°C) | Min Width (mm) | Recommended Pour (mm) | Notes |
|-----|-------------|-----------------|-----------------|----------------------|-------|
| DC Bus + (920V) | 28 (per phase) | 20 | 5.5 | 8–12 | Pour preferred, not trace |
| DC Bus − | 28 (per phase) | 20 | 5.5 | 8–12 | Matched to positive |
| LLC SW node | 28 (per phase) | 20 | 5.5 | 8–12 | Minimize area for EMI |
| Secondary out + | 33 (per phase) | 20 | 7.0 | 10–15 | Higher current than primary |
| Secondary out − | 33 (per phase) | 20 | 7.0 | 10–15 | Matched to positive |
| Combined output | 100 (total) | 20 | — | Bus bar + pour | Cannot be trace; bus bar mandatory |

### Internal Layers (L5) — 2 oz Cu

| Net | Current (A) | Temp Rise (°C) | Min Width (mm) | Notes |
|-----|-------------|-----------------|-----------------|-------|
| DC Bus distribution | 28 | 30 | 8.0 | Full-width pour preferred |
| Output distribution | 33 | 30 | 10.0 | Full-width pour preferred |

### Signal Layers (L3, L4) — 1 oz Cu

| Net | Current (mA) | Min Width (mm) | Notes |
|-----|-------------|-----------------|-------|
| Gate drive signals | <100 | 0.20 | Impedance controlled |
| Sense signals | <10 | 0.15 | Kelvin sense, differential |
| SPI/I2C | <10 | 0.15 | Controlled impedance |
| Auxiliary power (15V) | 500 | 0.50 | Gate driver supply |

> [!warning] 100A Output Path
> The combined 100 A output current **cannot** be carried by PCB copper alone at reasonable temperature rise. A **copper bus bar** soldered or bolted to the PCB is mandatory for the output path from the combined output capacitor bank to the P3 connector. Size the bus bar cross-section per IPC-2152: minimum 30 mm² copper cross-section for 100 A at 20°C rise.

### Bus Bar Sizing Calculation

For the output bus bar (100 A combined):

```
I = 100 A
ΔT_max = 20°C
Material: Cu (ρ = 1.72 × 10⁻⁸ Ω·m at 20°C, α = 0.004/°C)

Using IPC-2152 chart for external bus bar:
  Cross-section ≥ 30 mm² → e.g., 10 mm wide × 3 mm thick

Resistive loss check:
  L_busbar ≈ 50 mm = 0.05 m
  R = ρ × L / A = 1.72e-8 × 0.05 / 30e-6 = 28.7 µΩ
  P = I²R = 100² × 28.7e-6 = 0.287 W (negligible)
```

## 6. Via Specifications

### Power Vias (L1 ↔ L5, L1 ↔ L6)

| Parameter | Specification |
|-----------|--------------|
| Via diameter | 0.6 mm finished hole |
| Pad diameter | 1.2 mm |
| Current per via | ~1.5 A (conservative for 2 oz plating) |
| Vias needed per phase (28 A) | 19 minimum → use 24 (×1.25 margin) |
| Vias needed per phase secondary (33 A) | 22 minimum → use 28 |
| Array pattern | 4×6 or 5×5 grid in power pour areas |

### Thermal Vias (Under TO-247 Pads)

| Parameter | Specification |
|-----------|--------------|
| Via diameter | 0.3 mm finished hole |
| Pad diameter | 0.6 mm |
| Spacing | 1.2 mm pitch |
| Fill | Plugged and capped (prevent solder wicking) |
| Count per TO-247 | 12–16 vias in drain pad area |

### Stitching Vias (L1 GND ↔ L2 GND)

| Parameter | Specification |
|-----------|--------------|
| Via diameter | 0.3 mm |
| Spacing | ≤λ/20 at highest frequency of concern (~5 mm for 200 MHz) |
| Placement | Perimeter of each phase, around transformer cutouts, board edges |

## 7. Layer Assignment by Zone

### DC Bus Input Zone (0–40 mm)

| Layer | Content |
|-------|---------|
| L1 | Bus bar landing pads, capacitor pads, DC+ pour |
| L2 | GND plane (continuous) |
| L3 | Voltage sense traces, NTC temperature sensor |
| L4 | Auxiliary power for primary-side gate drivers |
| L5 | DC− return plane |
| L6 | Additional DC+ distribution, capacitor return pads |

### LLC Primary Bridge Zone (40–120 mm)

| Layer | Content |
|-------|---------|
| L1 | MOSFET drain/source pads, switching node pour (minimized area), snubber components, resonant tank (Lr, Cr) pads |
| L2 | GND plane (continuous — critical under gate drivers) |
| L3 | Gate drive signals, DESAT fault, PWM from controller, current sense |
| L4 | Gate driver isolated supply (15V), bootstrap capacitor connections |
| L5 | DC bus positive plane (wide pour, low impedance to decoupling caps) |
| L6 | DC bus return, MOSFET thermal pad interface to heatsink |

### Transformer Zone (115–175 mm)

| Layer | Content |
|-------|---------|
| L1 | Transformer primary pin pads (or planar winding traces) |
| L2 | GND plane — split into primary GND and secondary GND at isolation barrier |
| L3 | No routing across isolation barrier |
| L4 | No routing across isolation barrier |
| L5 | No copper across isolation barrier |
| L6 | Transformer secondary pin pads (or planar winding traces) |

> [!warning] Isolation Barrier — All Layers
> **No copper on any layer** may cross the primary-secondary isolation barrier except through the transformer itself. This includes L2 GND, L3/L4 signal, and L5 power. The barrier must be maintained on all 6 layers as a continuous PCB slot or keep-out zone. See [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] for detailed barrier requirements.

### Secondary Rectifier Zone (140–190 mm)

| Layer | Content |
|-------|---------|
| L1 | Sync rectifier MOSFET pads, output capacitor pads, secondary switching node |
| L2 | Secondary GND plane (continuous within secondary domain) |
| L3 | Secondary gate driver signals, output voltage/current sense |
| L4 | Secondary isolated supply, output sense return |
| L5 | Output positive plane |
| L6 | Output return, rectifier thermal pads |

### Output Zone (165–180 mm)

| Layer | Content |
|-------|---------|
| L1 | Output bus bar landing pads, combined capacitor bank pads |
| L2 | Secondary GND plane |
| L3 | Output voltage sense (Kelvin connection), CAN bus, OCPP interface |
| L4 | Output current sense signal routing |
| L5 | Output positive plane (connected to bus bar) |
| L6 | Output return plane |

## 8. Design Rules Summary

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Minimum trace width (signal) | 0.15 mm | Fabrication capability |
| Minimum trace spacing (signal) | 0.15 mm | Fabrication capability |
| Minimum via hole | 0.3 mm | Standard drill |
| Minimum annular ring | 0.15 mm | IPC Class 2 |
| Minimum pour-to-pour gap | 0.20 mm (same net), creepage-dependent (different net) | See [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage]] |
| Solder mask expansion | 0.05 mm per side | Standard |
| Board edge clearance | 0.5 mm (copper), 1.0 mm (component) | Mechanical |

## 9. Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board summary and design targets
- [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] — Why switching node pour area is minimized
- [[07-PCB-Layout/DC-DC/04-Thermal Layout|Thermal Layout]] — Thermal via specifications and heatsink interface
- [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] — Isolation barrier dimensions
- [[07-PCB-Layout/AC-DC/01-Stack-Up and Layer Assignment|AC-DC Stack-Up]] — Identical stack-up for fabrication standardization

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
