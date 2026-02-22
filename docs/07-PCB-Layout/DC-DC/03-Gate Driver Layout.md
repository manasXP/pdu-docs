---
tags: [pdu, pcb-layout, dc-dc, llc, gate-driver, stgap2sic, isolation]
created: 2026-02-22
status: draft
---

# 03 — Gate Driver Layout

## 1. Purpose

This document specifies the PCB layout requirements for the gate drivers on the DC-DC LLC resonant converter board. The board uses **STGAP2SiC** isolated gate drivers for all 12 SiC MOSFETs (6 primary, 6 secondary). The LLC board has additional layout complexity compared to the [[07-PCB-Layout/AC-DC/03-Gate Driver Layout|AC-DC board]] due to the **primary-secondary isolation barrier** that must not be breached by any copper on any layer.

## 2. Gate Driver IC Summary

| Parameter | Value |
|-----------|-------|
| IC | STGAP2SiC (ST Microelectronics) |
| Package | SO-16W (wide body, 10.3 mm) |
| Isolation rating | 1200 V working, 5.7 kVRMS for 1 min |
| Propagation delay | 75 ns typical |
| dV/dt immunity | 150 kV/µs (CMTI) |
| Output drive current | 4 A source / 4 A sink (peak) |
| Supply voltage (output side) | 15–20 V |
| DESAT detection | Integrated, programmable threshold |
| UVLO | Integrated, both input and output sides |
| Active Miller clamp | Integrated |

### Driver Count and Assignment

| Location | Qty | MOSFETs Driven | Bus Voltage | dV/dt Stress |
|----------|-----|-----------------|-------------|-------------|
| Primary high-side (×3) | 3 | Q1A, Q1B, Q1C (1200V SiC) | 920V DC bus | **Extreme** — 920V transitions at >50 kV/µs |
| Primary low-side (×3) | 3 | Q2A, Q2B, Q2C (1200V SiC) | 920V DC bus | Moderate — referenced to DC bus return |
| Secondary high-side (×3) | 3 | Q3A, Q3B, Q3C (650V SiC) | Up to 500V reflected | **High** — fast SR transitions |
| Secondary low-side (×3) | 3 | Q4A, Q4B, Q4C (650V SiC) | Up to 500V reflected | Moderate |
| **Total** | **12** | **12 SiC MOSFETs** | — | — |

> [!warning] Primary High-Side Driver — Maximum dV/dt Stress
> The primary high-side drivers sit on the switching node, which swings the full 920V bus at dV/dt rates of 50–100 kV/µs. This is the most demanding position for the STGAP2SiC's CMTI (Common Mode Transient Immunity). The 150 kV/µs rating provides margin, but only if the layout minimizes parasitic capacitive coupling from the switching node to the driver's input side.

## 3. Gate Loop Design

### Gate Loop Budget

The gate loop inductance must be minimized to prevent:
- Gate voltage ringing that could cause spurious turn-on
- Coupled dV/dt from the switching node through C_gd (Miller capacitance)
- Increased switching loss from slow, ringing gate transitions

| Parameter | Target |
|-----------|--------|
| **Total gate loop inductance** | **<5 nH** |
| Gate resistor (Rg_on) | 3–5 Ω |
| Gate resistor (Rg_off) | 1–2 Ω |
| Steering diode | Schottky (SBR1U30, BAT54S or equivalent) |

### Gate Loop Circuit

```
  STGAP2SiC
  OUT+ ──── Rg_on (3-5Ω) ────┬──── Gate (MOSFET)
                             │
  OUT- ──── Rg_off (1-2Ω) ───┤
              │              │
              D_schottky ────┘  (cathode to gate, anode to Rg_off)
              │
           GND_drv (Kelvin source)

  Decoupling:
  VCC_drv ────┬── 10µF electrolytic ──┬── GND_drv
              └── 100nF ceramic ──────┘
              └── 10nF ceramic (at IC pin) ─┘
```

### Split Gate Resistor with Schottky Steering

The Schottky diode steers the turn-off current through the lower Rg_off (1–2 Ω) for fast turn-off, while turn-on uses the higher Rg_on (3–5 Ω) to limit dI/dt and reduce ringing:

```
  During TURN-ON:  Current flows through Rg_on (3-5Ω) → Gate
                   Schottky is reverse-biased → blocked
                   Slower dI/dt, controlled ringing

  During TURN-OFF: Current flows Gate → Schottky → Rg_off (1-2Ω) → GND
                   Schottky forward-biased → low impedance path
                   Fast turn-off, reduced switching loss
```

> [!tip] Gate Resistor Selection
> For 1200V primary MOSFETs: use **Rg_on = 4.7 Ω, Rg_off = 1.5 Ω** as starting values. For 650V secondary MOSFETs: use **Rg_on = 3.3 Ω, Rg_off = 1.0 Ω** (lower C_gd, less ringing risk). Verify by simulation with the specific MOSFET SPICE model and prototype measurement.

### Gate Loop Layout Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| **G-1** | Gate trace length from driver OUT+ to MOSFET gate pin: **≤10 mm** | Each mm adds ~1 nH |
| **G-2** | Gate return (Kelvin source / OUT−) trace runs **parallel and adjacent** to gate trace on same layer | Mutual inductance cancellation |
| **G-3** | Rg_on, Rg_off, D_schottky placed within **3 mm** of MOSFET gate pin | Minimize total loop area |
| **G-4** | Gate trace routed on **L3 (signal layer)** with L2 GND plane as reference | Controlled impedance, shielding from power layer |
| **G-5** | No power traces or pours cross under the gate trace on L1 or L5 | Prevents capacitive coupling of dV/dt into gate |
| **G-6** | Use Kelvin source (TO-247-4L pin 4) for gate return, NOT power source | Eliminates common source inductance feedback |
| **G-7** | Decoupling caps (100 nF + 10 nF) within **2 mm** of driver VCC/GND pins | Local energy storage for gate charge pulses |
| **G-8** | 10 µF electrolytic within **10 mm** of driver, low-ESR type | Bulk charge reservoir |

### Gate Loop Inductance Estimation

```
For a 10 mm gate trace with 0.2 mm width on L3, return on adjacent trace:

L_trace ≈ µ₀/(2π) × l × [ln(2l/w) + 0.5]  (single wire above ground plane)

Better estimate using parallel trace pair:
L_loop ≈ µ₀ × l × d / (π × w)

Where:
  l = 10 mm (trace length)
  d = 0.3 mm (center-to-center spacing of gate/return pair)
  w = 0.2 mm (trace width)

L_loop = 4π×10⁻⁷ × 10e-3 × 0.3e-3 / (π × 0.2e-3)
       = 4×10⁻⁷ × 10e-3 × 1.5e-3
       = 0.6 nH (trace pair contribution)

Add component pads and vias: ~1-2 nH
Total gate loop: ~2-3 nH → well within 5 nH budget
```

## 4. Driver Placement — Primary Side

### Physical Layout

Each primary half-bridge has two MOSFETs and two gate drivers:

```
  ┌─────────── Per Phase (~80mm wide) ───────────┐
  │                                              │
  │  ┌───────────────┐    ┌───────────────┐      │
  │  │   Q1 (HS)     │    │   Q2 (LS)     │      │
  │  │ ┌──TO-247──┐  │    │ ┌──TO-247──┐  │      │
  │  │ │  D  G  S │  │    │ │  D  G  S │  │      │
  │  │ │  [K.src] │  │    │ │  [K.src] │  │      │
  │  │ └──────────┘  │    │ └──────────┘  │      │
  │  │  [Rg][D_s]    │    │  [Rg][D_s]    │      │
  │  │  ┌────────┐   │    │  ┌────────┐   │      │
  │  │  │DRV1_HS │   │    │  │DRV2_LS │   │      │
  │  │  │STGAP2  │   │    │  │STGAP2  │   │      │
  │  │  │  SiC   │   │    │  │  SiC   │   │      │
  │  │  └────────┘   │    │  └────────┘   │      │
  │  │  [Cdecoup]    │    │  [Cdecoup]    │      │
  │  └───────────────┘    └───────────────┘      │
  │                                              │
  │  [Lr]              [Cr]          [Snubbers]  │
  └──────────────────────────────────────────────┘
```

### Driver-to-MOSFET Distance Constraints

| Connection | Max Distance | Preferred |
|------------|-------------|-----------|
| DRV OUT+ → Q gate pin | 10 mm | 5–7 mm |
| DRV OUT− → Q Kelvin source | 10 mm | 5–7 mm |
| DRV VCC → decoupling cap | 2 mm | 1 mm (direct pad) |
| DRV GND → decoupling cap | 2 mm | 1 mm (direct pad) |

### Primary Driver Isolation Considerations

The STGAP2SiC has internal galvanic isolation between its input (logic) side and output (gate drive) side. On the PCB:

| Requirement | Specification |
|-------------|--------------|
| Input-to-output creepage (on IC) | Per STGAP2SiC datasheet: 8 mm minimum on PCB under IC |
| PCB slot under driver IC | **3 mm wide slot** between input and output pad rows |
| Copper keep-out under slot | No copper on any layer (L1 through L6) within the slot |
| Conformal coating | Applied over the IC and slot area after assembly |

> [!note] PCB Slot Under Each Driver
> Each of the 12 STGAP2SiC ICs requires a **PCB slot** between the input-side pins and output-side pins. This slot prevents surface tracking at high dV/dt. The slot is typically 3 mm wide × 12 mm long (spanning the IC width). Total slot area per driver: ~36 mm². For 12 drivers: 432 mm² of board area lost to slots — factor this into zone allocation.

## 5. Driver Placement — Secondary Side

The secondary gate drivers are placed identically to the primary but operate at lower voltage stress (up to 500V reflected vs. 920V bus). The layout rules are the same, but with slightly relaxed urgency:

### Secondary vs. Primary Driver Comparison

| Parameter | Primary Drivers | Secondary Drivers |
|-----------|----------------|-------------------|
| Bus voltage | 920V | Up to 500V (reflected) |
| dV/dt on switching node | 50–100 kV/µs | 30–60 kV/µs |
| CMTI requirement | 150 kV/µs (use full rating) | 100 kV/µs (comfortable margin) |
| Gate loop inductance target | <5 nH | <5 nH (same — still SiC) |
| Rg_on | 4.7 Ω | 3.3 Ω |
| Rg_off | 1.5 Ω | 1.0 Ω |
| PCB slot under IC | Mandatory | Mandatory |

## 6. Primary-Secondary Isolation Barrier

### The Barrier Concept

The DC-DC board has a unique layout challenge not present on the AC-DC board: the **primary-secondary isolation barrier**. This barrier provides:

- **4 kV hipot test** withstand (per IEC 61851-23)
- **Reinforced insulation** classification
- Physical separation between 920V primary domain and up to 1000V secondary domain

### Barrier Implementation on PCB

| Feature | Specification |
|---------|--------------|
| Barrier type | **PCB slot** (routed channel through board) |
| Slot width | ≥4 mm (for 4 kV reinforced insulation per IPC-2221B) |
| Slot length | Full board width (250 mm) |
| Copper clearance from slot edge | ≥2 mm on all layers |
| No copper crossing on ANY layer | L1, L2, L3, L4, L5, L6 — all must be clear |
| Conformal coating | Both sides of the board at the barrier zone |
| Exceptions | Only transformer connections cross the barrier (through the transformer itself, not through PCB copper) |

```
  Primary Zone
  ─────────────────────────── copper
      ≥2mm clearance
  ════════════════════════════ PCB SLOT (≥4mm)
      ≥2mm clearance
  ─────────────────────────── copper
  Secondary Zone
```

> [!warning] No Signal Routing Across the Barrier
> Gate drive signals, sense signals, communication buses — **nothing** crosses the primary-secondary barrier on the PCB. All signals that must cross the barrier do so through:
> - The STGAP2SiC's internal isolation (for gate drive commands)
> - Isolated signal couplers (for current/voltage sense feedback)
> - Optocouplers or digital isolators (for fault signals)
> - The transformer itself (for power transfer)

### L2 GND Plane at the Barrier

The L2 GND plane is split into two separate ground domains at the isolation barrier:

```
  ┌─────────────────────────────────────────────┐
  │         PRIMARY GND (L2)                    │
  │  (connected to DC bus negative / PE)        │
  │                                             │
  ├════════════════════════════════════════════─┤  ← Isolation slot
  │                                             │
  │         SECONDARY GND (L2)                  │
  │  (connected to output negative / floating)  │
  └─────────────────────────────────────────────┘
```

These two GND domains must **never be directly connected** on the PCB. They are coupled only through:
- Y-capacitors (safety-rated, connecting primary GND to secondary GND for CM noise filtering)
- The transformer parasitic capacitance (unintentional, minimized)

## 7. Driver Decoupling

### Per-Driver Decoupling (Output Side)

| Component | Value | Package | Placement | Purpose |
|-----------|-------|---------|-----------|---------|
| C1 | 100 nF | 0402 or 0603 | **At VCC/GND pins** (<1 mm) | HF bypass, gate charge source |
| C2 | 10 nF | 0402 | At VCC/GND pins | UHF bypass |
| C3 | 10 µF | 1206 electrolytic or MLCC | Within 10 mm | Bulk charge reservoir |
| C4 | 1 µF | 0805 | Within 5 mm | Mid-frequency energy |

### Per-Driver Decoupling (Input Side)

| Component | Value | Package | Placement | Purpose |
|-----------|-------|---------|-----------|---------|
| C5 | 100 nF | 0402 | At VDD/GND pins | Logic-side bypass |
| C6 | 10 nF | 0402 | At VDD/GND pins | UHF bypass |

### Decoupling Layout Priority

```
Priority 1: C1 (100nF) and C2 (10nF) — directly at output VCC/GND pins
Priority 2: C4 (1µF) — within 5mm, on same layer if possible
Priority 3: C3 (10µF) — within 10mm, can be on opposite side of board
Priority 4: C5, C6 — at input-side pins (less critical, lower current)
```

> [!tip] Shared Isolated Power Supply
> Each STGAP2SiC output side needs an isolated 15–20V supply. For the primary side, a single isolated DC-DC converter (e.g., Murata MEJ2 series) can supply both high-side and low-side drivers through separate LDOs. This reduces component count but requires careful routing to avoid ground loops between the high-side and low-side driver GND references.

## 8. Driver Thermal Management

### Power Dissipation per Driver

```
P_driver = Q_g × V_drv × f_sw + I_q × V_drv

Where:
  Q_g  = 120 nC (typical SiC MOSFET gate charge)
  V_drv = 18 V
  f_sw  = 150 kHz
  I_q   = 5 mA (quiescent current)

P_driver = 120e-9 × 18 × 150e3 + 5e-3 × 18
         = 0.324 + 0.090
         = 0.414 W per driver

Total for 12 drivers: 12 × 0.414 = 4.97 W
```

### Thermal Via Array Under Each Driver

| Parameter | Specification |
|-----------|--------------|
| Via diameter | 0.3 mm |
| Via count | 9 (3×3 array) |
| Spacing | 1.0 mm pitch |
| Connected to | L2 GND plane (primary or secondary, per zone) |
| Copper pour on L1 | 15 mm × 15 mm minimum under IC exposed pad |

### Thermal Calculation

```
Rth_jc (STGAP2SiC, SO-16W) ≈ 30°C/W (estimated from package)
Rth_board (9 vias, 15×15mm Cu) ≈ 25°C/W
Rth_total ≈ 55°C/W

T_j = T_amb + P × Rth_total = 55 + 0.414 × 55 = 77.8°C

T_j_max (STGAP2SiC) = 150°C → adequate margin
```

## 9. DESAT (Desaturation) Detection Layout

The STGAP2SiC integrates DESAT detection for short-circuit protection. Layout considerations:

| Requirement | Specification |
|-------------|--------------|
| DESAT sense resistor | 10–100 kΩ, placed within 5 mm of MOSFET drain |
| DESAT diode (HV blocking) | BAS516 or equivalent, cathode to drain |
| Trace routing | Route on L3 signal layer, keep away from switching node pour |
| Blanking time | Set by external capacitor on DESAT pin |
| Response time | <3 µs from overcurrent to gate shutdown |

### DESAT Sense Connection

```
  MOSFET Drain ─── [BAS516 diode] ─── [R_desat 47kΩ] ─── DESAT pin (STGAP2SiC)
                    (cathode)  (anode)
                                  │
                              [C_blank] ─── GND_drv
                              (sets blanking time)
```

> [!warning] DESAT Routing on Primary High-Side
> The DESAT sense trace on the primary high-side drivers connects to the 920V DC bus through the MOSFET drain. This trace carries minimal current but sits at lethal voltage. Route on L3 with adequate creepage to adjacent low-voltage traces. Use a keep-out zone of ≥4 mm around the DESAT trace where it connects to the drain pad.

## 10. Anti-Parallel Diode Considerations

SiC MOSFETs have a relatively poor body diode (high V_f, slow recovery compared to Si). For the LLC topology:

- **Primary half-bridge**: The body diode conducts during dead time for ZVS. The SiC body diode's reverse recovery is acceptable in LLC due to ZVS conditions (near-zero current at switching).
- **Secondary synchronous rectifier**: The body diode conducts before the gate turns on. Fast body diode recovery is important here.

No external anti-parallel diodes are typically needed for LLC topology, but verify with the specific MOSFET selected. If added, the diode must be placed within 3 mm of the MOSFET D-S pads to be effective.

## 11. Layout Checklist

- [ ] All 12 STGAP2SiC ICs placed with output side facing MOSFET gate pins
- [ ] PCB slot (3 mm) under each driver IC between input and output pins
- [ ] Gate loop trace length ≤10 mm for all 12 drivers
- [ ] Gate/return traces routed as parallel pair on L3
- [ ] Rg_on, Rg_off, D_schottky within 3 mm of MOSFET gate pin
- [ ] Decoupling caps at VCC/GND pins (≤1 mm distance)
- [ ] 15×15 mm Cu pour under each driver with 9 thermal vias
- [ ] No power copper under gate traces on L1 or L5
- [ ] DESAT sense routed on L3 with creepage clearance
- [ ] Primary-secondary isolation barrier: no copper crossing on any layer
- [ ] L2 GND plane split at barrier (primary GND / secondary GND)
- [ ] Y-capacitors placed at barrier for CM filtering
- [ ] Kelvin source (pin 4) used for all TO-247-4L gate returns

## 12. Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board-level context
- [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] — Power loop interaction with gate loop
- [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] — Isolation barrier and driver creepage
- [[07-PCB-Layout/AC-DC/03-Gate Driver Layout|AC-DC Gate Driver Layout]] — Same STGAP2SiC IC, similar layout approach
- [[SiC Device Thermal Parameters]] — MOSFET gate charge and switching characteristics

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
