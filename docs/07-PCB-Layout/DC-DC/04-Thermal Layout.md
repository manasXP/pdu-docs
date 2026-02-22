---
tags: [pdu, pcb-layout, dc-dc, llc, thermal, heatsink, ipc-2152]
created: 2026-02-22
status: draft
---

# 04 — Thermal Layout

## 1. Purpose

This document specifies the thermal management layout for the DC-DC LLC resonant converter board. The board dissipates approximately **600–900 W** at full load (30 kW at 96–98% efficiency), distributed across primary MOSFETs, secondary rectifier MOSFETs, transformers, and passive components. Effective thermal management is critical for reliability and must be coordinated with the mechanical enclosure design (see [[10-Mechanical Integration]]).

## 2. Power Loss Budget

### 2.1 Per-Phase Loss Breakdown (at 10 kW per phase)

| Component | Loss Type | Power (W) | Quantity | Subtotal (W) |
|-----------|-----------|-----------|----------|---------------|
| Primary MOSFET Q1 | Conduction + switching | 15–25 | 1 | 15–25 |
| Primary MOSFET Q2 | Conduction + switching | 15–25 | 1 | 15–25 |
| Transformer | Core + copper | 30–50 | 1 | 30–50 |
| Resonant inductor Lr | Core + copper | 10–15 | 1 | 10–15 |
| Secondary MOSFET Q3 | Conduction | 10–20 | 1 | 10–20 |
| Secondary MOSFET Q4 | Conduction | 10–20 | 1 | 10–20 |
| Bus capacitors (ESR) | I²R | 2–5 | — | 2–5 |
| Output capacitors (ESR) | I²R | 2–5 | — | 2–5 |
| Gate drivers (×4) | Switching + quiescent | 0.4 | 4 | 1.6 |
| Snubber resistors (×2) | Damping | 0.13 | 2 | 0.26 |
| PCB copper (I²R) | Resistive | 3–8 | — | 3–8 |
| **Phase subtotal** | | | | **100–175** |

### 2.2 Total Board Loss

| Condition | Per Phase | 3 Phases | Notes |
|-----------|-----------|----------|-------|
| Full load, 98% efficiency | 67 W | 200 W | Best case (SiC, full ZVS) |
| Full load, 97% efficiency | 100 W | 300 W | Typical operating point |
| Full load, 96% efficiency | 133 W | 400 W | Conservative / partial ZVS loss |
| Overload transient | 175 W | 525 W | Short duration, thermal capacitance absorbs |

> [!note] LLC Efficiency Advantage
> The LLC resonant topology achieves ZVS on the primary and near-ZCS on the secondary, significantly reducing switching losses compared to hard-switched topologies. At the resonant frequency, switching losses are near zero, and conduction losses dominate. The thermal design should target the **300 W typical** case with margin for the **400 W conservative** case.

## 3. MOSFET Thermal Design — Primary (1200V SiC, TO-247)

### 3.1 Thermal Interface

| Parameter | Specification |
|-----------|--------------|
| Package | TO-247-4L (4-pin Kelvin source) |
| Mounting | Vertical, tab side against heatsink |
| TIM | Bergquist GP3000S (3.0 W/m·K, 0.25 mm thick) |
| Mounting hardware | M3 screw + washer + insulating bushing |
| Insulation | Electrically insulating TIM (GP3000S is insulating) |
| Mounting torque | 0.5 N·m (per Bergquist specification) |

### 3.2 Thermal Resistance Stack

```
T_junction
    │
    ├── Rth_jc = 0.5 °C/W (typical 1200V SiC TO-247, junction to case)
    │
T_case
    │
    ├── Rth_TIM = t / (k × A)
    │           = 0.25e-3 / (3.0 × 1.7e-4)
    │           = 0.49 °C/W  (GP3000S, TO-247 tab area ~170 mm²)
    │
T_heatsink_surface
    │
    ├── Rth_heatsink = varies by heatsink design
    │   (target: 0.3–0.5 °C/W per device with forced air)
    │
T_ambient
```

### 3.3 Temperature Calculation — Primary MOSFET

```
Worst case: P_MOSFET = 25 W per device, T_amb = 55°C

Rth_ja = Rth_jc + Rth_TIM + Rth_hs
       = 0.5 + 0.49 + 0.4
       = 1.39 °C/W

T_j = T_amb + P × Rth_ja
    = 55 + 25 × 1.39
    = 89.8°C

T_j_max (SiC) = 175°C → margin = 85°C (adequate)

At thermal derating threshold (55°C ambient):
  T_j = 55 + 25 × 1.39 = 89.8°C → still well below limit
```

### 3.4 PCB Thermal Interface for TO-247

The TO-247 devices are through-hole mounted. The PCB area under and around the device contributes to heat spreading:

| Feature | Specification |
|---------|--------------|
| Drain pad copper pour | 15 mm × 20 mm minimum on L1 |
| Thermal vias under drain pad | 12–16 vias, 0.3 mm diameter, 1.2 mm pitch |
| Via fill | Plugged and capped (prevent solder wicking through during wave/reflow) |
| L6 copper pour (bottom) | Mirror of L1 pour, connected through thermal vias |
| Purpose | Spread heat into PCB, supplement heatsink cooling path |

> [!tip] Thermal Via Effectiveness
> Each 0.3 mm plugged thermal via has approximately:
> ```
> Rth_via = L / (k × A × N_barrel)
>         = 1.6e-3 / (385 × π × (0.15e-3)² × 0.025/0.15)
>         ≈ 70°C/W per via (approximate, with plating thickness ~25µm)
> ```
> With 16 vias in parallel: Rth_array ≈ 4.4°C/W. This is a secondary path — the primary heat path is through the TO-247 tab to the heatsink. The thermal vias provide ~15–20% additional heat dissipation into the PCB.

## 4. MOSFET Thermal Design — Secondary (650V SiC, TO-247)

### 4.1 Thermal Parameters

| Parameter | Specification |
|-----------|--------------|
| Package | TO-247-4L |
| Rth_jc | 0.4°C/W (typical for 650V SiC, slightly better than 1200V) |
| TIM | Bergquist GP3000S (same as primary) |
| Current per phase | 33 A (higher than primary 28 A) |
| Dominant loss | Conduction (synchronous rectification, near-ZCS) |
| Power dissipation | 10–20 W per device |

### 4.2 Temperature Calculation — Secondary MOSFET

```
P_MOSFET = 20 W (worst case), T_amb = 55°C

Rth_ja = 0.4 + 0.49 + 0.4 = 1.29 °C/W

T_j = 55 + 20 × 1.29 = 80.8°C

T_j_max = 175°C → margin = 94°C (comfortable)
```

> [!note] Secondary Has More Thermal Margin
> The secondary MOSFETs dissipate less power (conduction-dominated in LLC SR mode) and have slightly better Rth_jc. Thermal design can be slightly relaxed on the secondary side, but maintain identical TIM and mounting for manufacturing consistency.

## 5. Transformer Thermal Design

The transformers are the **largest individual heat sources** on the DC-DC board, each dissipating 30–50 W of combined core and winding losses.

### 5.1 Mounting Options and Thermal Paths

#### Option A: Through-Board Cutout Mounting

```
     Heatsink (chassis)
  ═══════════════════════
     TIM (GP3000S or thermal pad)
  ─────────────────────────
  │    Transformer Core    │
  │    ┌──────────┐        │
  │    │ Winding  │        │  ← Core bottom face contacts TIM
  │    │  layers  │        │     through PCB cutout
  │    └──────────┘        │
  ─────────────────────────
     PCB (cutout area)
  ═══════════════════════
     Mounting bracket
```

| Parameter | Specification |
|-----------|--------------|
| Cutout dimensions | 40 mm × 35 mm per transformer |
| Core-to-heatsink TIM | Bergquist GP5000S (5.0 W/m·K) for transformer |
| Contact area | ~30 mm × 25 mm (core bottom face) |
| Rth_core-to-heatsink | t/(k×A) = 0.5e-3/(5.0×750e-6) = 0.13°C/W |
| Mounting | Mechanical bracket from below, screwed to heatsink |
| Advantage | Excellent thermal path (core directly on heatsink) |

#### Option B: On-Board (Planar) Mounting

| Parameter | Specification |
|-----------|--------------|
| Heat path | Core → mounting pad → PCB copper → thermal vias → heatsink |
| Rth_PCB_path | ~5–10°C/W (significantly worse than cutout) |
| Thermal vias required | 40–60 per transformer footprint |
| Disadvantage | Much higher thermal resistance; may require derating |

> [!warning] Transformer Thermal Is Design-Driving
> At 50 W loss per transformer and T_amb = 55°C:
> - **Cutout mount**: T_core = 55 + 50×0.13 = 61.5°C (excellent)
> - **On-board mount**: T_core = 55 + 50×7.5 = 430°C (impossible!)
>
> The on-board mounting option **requires active cooling** of the transformer itself (direct airflow over the core) or a **thermal interface bracket** that bypasses the PCB. Through-board cutout mounting is strongly preferred for thermal reasons.

### 5.2 Transformer Cutout Thermal Considerations

The PCB cutout removes copper and FR-4 material, affecting nearby component cooling:

| Concern | Mitigation |
|---------|------------|
| Loss of L2 GND plane continuity near cutout | Route GND plane around cutout with stitching vias on all sides |
| Reduced copper area for heat spreading | Extend copper pours 10 mm beyond cutout on all sides |
| Mechanical weakness (board flex) | Add stiffener ribs or support posts under transformer brackets |
| Airflow disruption | Design cutout to not block forced-air channel |

## 6. Gate Driver Thermal

### 6.1 Power Dissipation and Cooling

| Parameter | Value |
|-----------|-------|
| Power per driver | 0.41 W |
| 12 drivers total | 4.97 W |
| Package | SO-16W |
| Rth_ja (still air) | ~70°C/W (SO-16W) |
| Rth_ja (with Cu pour + vias) | ~40°C/W |

### 6.2 Driver Thermal Layout

| Feature | Specification |
|---------|--------------|
| Cu pour under IC | 15 mm × 15 mm on L1, connected to exposed pad |
| Thermal vias | 9 (3×3 array), 0.3 mm, 1.0 mm pitch |
| Connection to L2 | Via to L2 GND plane for heat spreading |
| Temperature at full load | T_j = 55 + 0.41 × 40 = 71.4°C (well below 150°C max) |

## 7. Passive Component Thermal

### 7.1 Resonant Components (Lr, Cr)

| Component | Loss (W) | Thermal Consideration |
|-----------|----------|----------------------|
| Lr (resonant inductor) | 10–15 per phase | Mount vertically with airflow access; may need heatsink clip |
| Cr (resonant capacitor bank) | 2–5 per phase | Film/ceramic caps; distribute across area for thermal spreading |

### 7.2 Electrolytic Capacitors

| Parameter | Specification |
|-----------|--------------|
| Temperature rating | 105°C minimum (prefer 125°C for bus capacitors) |
| Spacing from heat sources | ≥15 mm from MOSFET heatsink area |
| Airflow | Place upstream of MOSFETs in airflow path |
| Lifetime consideration | Every 10°C reduction in temperature doubles electrolytic life |

> [!warning] Capacitor Placement and Lifetime
> Electrolytic capacitor failure is the #1 reliability concern in power supplies. Place DC bus electrolytics in the **coolest zone** of the board (near the air inlet). The output electrolytics are less accessible to cool air (downstream in the airflow path), so use higher temperature-rated parts (125°C) for the output stage.

## 8. Airflow Path Design

### 8.1 Forced-Air Cooling Architecture

The PDU enclosure uses forced-air cooling with fans drawing air across the boards. The airflow direction across the DC-DC board is designed to cool the **lowest-power components first** (entering cool air) and **highest-power components last** (where the air is warmest but the components have the highest temperature ratings):

```
  AIR INLET (cool)
      ↓
  ┌────────────────────────────────────────────┐
  │  DC Bus Input Zone                         │
  │  [Electrolytic caps — 105°C rated]         │  ← Coolest air here
  │  [Ceramic bus caps — 125°C rated]          │
  ├────────────────────────────────────────────┤
  │  LLC Primary Bridge Zone                   │
  │  [SiC MOSFETs — 175°C rated]               │  ← Warm air, high Tj margin
  │  [Gate drivers — 150°C rated]              │
  │  [Resonant inductors Lr]                   │
  ├────────────────────────────────────────────┤
  │  Transformer Zone                          │
  │  [Transformers — 130°C rated core]         │  ← Hottest zone
  │  [Through cutout → direct heatsink path]   │
  ├────────────────────────────────────────────┤
  │  Secondary Rectifier Zone                  │
  │  [SiC MOSFETs — 175°C rated]               │  ← Air warming
  │  [Gate drivers — 150°C rated]              │
  ├────────────────────────────────────────────┤
  │  Output Zone                               │
  │  [Output electrolytics — 125°C rated]      │  ← Warmest air, highest rating
  │  [Output bus bar — copper, no limit]       │
  └────────────────────────────────────────────┘
      ↓
  AIR OUTLET (warm)
```

> [!tip] Airflow Optimization
> The transformer zone creates the most significant airflow obstruction (large core bodies). Ensure the PCB cutouts are sized to allow airflow through/around the transformer. If using through-board cutouts, the transformer core sits below the board surface, and airflow over the top side is unobstructed. Consider airflow baffles to direct air across MOSFET heatsink fins.

### 8.2 Airflow Requirements

| Parameter | Value | Notes |
|-----------|-------|-------|
| Required airflow | 15–25 CFM across DC-DC board | Depends on heatsink fin design |
| Air velocity at components | 2–3 m/s minimum | Below MOSFET heatsink fins |
| Pressure drop budget | 5–10 Pa across board | Typical for 40 mm axial fans |
| Fan specification | 2× 80 mm, 12V, 25 CFM each | Redundant; one fan sustains derating |

### 8.3 Thermal Derating

Per the PDU specification, thermal derating begins at **55°C ambient**:

| Ambient Temp | Max Output Power | Thermal Action |
|-------------|-----------------|----------------|
| ≤45°C | 30 kW (100%) | Normal operation, full fan speed not required |
| 45–55°C | 30 kW (100%) | Fans at full speed |
| 55–65°C | Linear derating to 20 kW | Reduce output current proportionally |
| 65–75°C | Linear derating to 10 kW | Reduce further |
| >75°C | Shutdown (OTP) | Over-temperature protection |

## 9. IPC-2152 Thermal Trace Sizing Summary

Consolidated from [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment|Stack-Up and Layer Assignment]], with thermal context:

| Current Path | Current (A) | Layer | Cu Weight | Min Width (mm) | ΔT Target (°C) |
|-------------|-------------|-------|-----------|-----------------|-----------------|
| DC bus (per phase) | 28 | L1 (ext) | 2 oz | 5.5 | 20 |
| DC bus (per phase) | 28 | L5 (int) | 2 oz | 8.0 | 30 |
| Secondary (per phase) | 33 | L1 (ext) | 2 oz | 7.0 | 20 |
| Combined output | 100 | Bus bar | — | Bus bar (30 mm²) | 20 |
| Resonant tank (Lr/Cr) | 28 | L1 (ext) | 2 oz | 5.5 | 20 |
| SW node (keep small) | 28 | L1 (ext) | 2 oz | 5.5 min, ≤1.5cm² area | 20 |

### 9.1 I²R Loss in PCB Copper

```
Example: DC bus trace, one phase, L1 (2 oz external)

I = 28 A
L = 40 mm (bus capacitor to MOSFET)
W = 10 mm (pour width)
t = 70 µm (2 oz Cu)
ρ_Cu = 1.72 × 10⁻⁸ Ω·m (at 20°C), ×1.3 at 85°C = 2.24 × 10⁻⁸

R = ρ × L / (W × t)
  = 2.24e-8 × 40e-3 / (10e-3 × 70e-6)
  = 2.24e-8 × 40e-3 / 7e-7
  = 1.28 mΩ

P = I²R = 28² × 1.28e-3 = 1.003 W per trace segment

For all primary copper paths (3 phases, ×2 for +/−): ~6 W total
For all secondary copper paths: ~8 W total
Total PCB I²R loss: ~14 W (included in efficiency calculation)
```

## 10. Thermal Simulation Recommendations

Before fabrication, perform a thermal simulation to validate the layout:

| Tool | Method | Fidelity |
|------|--------|----------|
| Ansys Icepak | Full 3D CFD + thermal | High — includes airflow |
| COMSOL Multiphysics | FEA thermal + optional CFD | High |
| KiCad + external thermal solver | Export geometry → thermal solver | Medium |
| Hand calculation (this doc) | Rth stack-up per component | Low — conservative |

### 10.1 Key Simulation Inputs

| Input | Value | Source |
|-------|-------|--------|
| Ambient temperature | 55°C (worst case) | PDU specification |
| Airflow | 20 CFM across board | Fan specification |
| MOSFET power (primary) | 25 W each, 6 total = 150 W | Loss analysis |
| MOSFET power (secondary) | 20 W each, 6 total = 120 W | Loss analysis |
| Transformer power | 50 W each, 3 total = 150 W | Magnetics analysis |
| Gate driver power | 0.41 W each, 12 total = 5 W | Driver analysis |
| PCB copper loss | 14 W total | I²R calculation |
| Snubber loss | 0.76 W total | Snubber analysis |
| **Total simulated loss** | **~440 W** | Sum of above |

## 11. Layout Checklist — Thermal

- [ ] TO-247 drain pad copper pour ≥15×20 mm on L1 and L6
- [ ] 12–16 plugged thermal vias under each TO-247 drain pad
- [ ] Bergquist GP3000S TIM specified for all MOSFET-to-heatsink interfaces
- [ ] M3 mounting holes for each TO-247 device
- [ ] Transformer cutout dimensions confirmed (40×35 mm per transformer)
- [ ] Transformer TIM (GP5000S) contact area verified
- [ ] Gate driver Cu pour 15×15 mm with 9 thermal vias each
- [ ] Electrolytic capacitors placed in coolest airflow zone
- [ ] Airflow path unobstructed from inlet to outlet
- [ ] No tall components blocking airflow over MOSFET heatsinks
- [ ] Output bus bar sized for 100A with ≤20°C rise
- [ ] Resonant inductor mounting allows airflow contact
- [ ] Board stiffeners specified near transformer cutouts

## 12. Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board dimensions and specifications
- [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment|Stack-Up and Layer Assignment]] — IPC-2152 trace widths
- [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] — Snubber dissipation values
- [[07-PCB-Layout/DC-DC/03-Gate Driver Layout|Gate Driver Layout]] — Driver thermal vias
- [[07-PCB-Layout/AC-DC/04-Thermal Layout|AC-DC Thermal Layout]] — Shared heatsink and airflow architecture
- [[10-Mechanical Integration]] — Enclosure, heatsink, fan specifications
- [[SiC Device Thermal Parameters]] — MOSFET Rth_jc values and Tj_max
- [[02-Magnetics Design]] — Transformer and inductor loss budgets

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
