---
tags: [pdu, pcb-layout, dc-dc, llc, emi, resonant-tank, common-mode, shielding]
created: 2026-02-22
status: draft
---

# 05 — EMI-Aware Layout

## 1. Purpose

This document defines the EMI-aware layout strategies for the DC-DC LLC resonant converter board. The LLC topology has inherent EMI advantages over hard-switched topologies (ZVS reduces dV/dt-related emissions), but the 3-phase interleaved architecture and high-frequency transformer introduce unique challenges: **resonant tank symmetry**, **transformer CM capacitance**, and **inter-phase coupling**. The output cable connecting to the EV battery is also a significant EMI antenna.

## 2. EMI Source Identification

### Primary EMI Sources on the DC-DC Board

| Source | Mechanism | Frequency Range | Severity |
|--------|-----------|-----------------|----------|
| Primary switching nodes (×3) | dV/dt × C_parasitic → displacement current | 100 kHz – 30 MHz | **High** |
| Secondary rectifier switching nodes (×3) | dV/dt × C_parasitic → displacement current | 100 kHz – 30 MHz | **High** |
| Transformer CM capacitance (×3) | dV/dt × C_winding → CM current | 100 kHz – 10 MHz | **High** |
| Resonant tank (Lr, Cr) | High circulating current at f_r | 80–300 kHz | Medium |
| Gate driver switching | Fast edges on gate, DESAT sense | 1–100 MHz | Low–Medium |
| DC bus ripple current | Capacitor ESR/ESL, switching harmonics | 100 kHz – 5 MHz | Medium |
| Output cable radiation | CM current on cable acts as antenna | 150 kHz – 30 MHz | **High** (conducted EMI) |

### LLC Topology EMI Advantages

The LLC resonant converter operating at or near the resonant frequency achieves:

1. **ZVS on primary** — switching occurs at zero voltage, eliminating the high-dV/dt edges that dominate EMI in hard-switched converters. The switching node transitions are completed by the magnetizing current during dead time, producing a **sinusoidal-like** voltage transition rather than a sharp step.

2. **Near-ZCS on secondary** — the secondary current waveform is approximately sinusoidal, reducing high-frequency harmonic content compared to square-wave rectification.

3. **Lower EMI than PSFB** — Phase-Shifted Full Bridge has hard-switching on the secondary; LLC avoids this.

> [!tip] LLC EMI Advantage — Quantified
> In a well-designed LLC converter at the resonant frequency, the primary switching node dV/dt is:
> ```
> dV/dt ≈ V_bus / t_dead ≈ 920V / 200ns = 4.6 kV/µs
> ```
> Compare to hard-switched PFC:
> ```
> dV/dt ≈ 920V / 15ns = 61 kV/µs
> ```
> This is a **13× reduction** in dV/dt, translating to ~22 dB lower displacement current EMI. However, this advantage is only present at the resonant operating point. During startup, overload, or frequency modulation away from resonance, the LLC may lose ZVS and dV/dt increases dramatically.

## 3. Switching Node Area Control

### Requirement

Each LLC half-bridge switching node must have a copper pour area of **≤1.5 cm²** to limit electric-field (E-field) emissions from the high-dV/dt surface.

### Switching Node Physics

The displacement current radiated from a switching node is:

```
I_displacement = C_parasitic × dV/dt

Where C_parasitic includes:
  - MOSFET C_oss (output capacitance): ~200 pF per device
  - PCB copper-to-GND capacitance: C = ε₀ × εr × A / d
  - Stray capacitance to heatsink, enclosure, etc.

For a 1.5 cm² copper pour on L1, referenced to L2 GND at 0.27 mm distance:
  C_pcb = 8.85e-12 × 4.4 × 1.5e-4 / 0.27e-3 = 21.7 pF

During ZVS (4.6 kV/µs):
  I_disp_pcb = 21.7e-12 × 4.6e9 = 0.1 mA (negligible)

During hard-switching (61 kV/µs, loss of ZVS):
  I_disp_pcb = 21.7e-12 × 61e9 = 1.3 mA (significant at HF)
```

### Area Budget Per Phase

| Element on Switching Node | Area (cm²) | Notes |
|--------------------------|------------|-------|
| Q1 source / Q2 drain pad | 0.3 | TO-247 pads (fixed) |
| Connection trace Q1→Q2 | 0.2 | Keep as short as possible |
| Resonant inductor Lr connection | 0.3 | Lr connects to SW node |
| Snubber cap landing pad | 0.1 | At MOSFET D-S |
| Guard ring / thermal relief | 0.2 | Necessary for soldering |
| **Subtotal** | **1.1** | Below 1.5 cm² target |
| **Budget remaining** | **0.4** | Margin for routing adjustments |

> [!warning] Do Not Expand the Switching Node Pour
> It is tempting to make the switching node copper pour wider for better current handling. **Resist this.** The switching node carries current only during the brief transition; it does not need to handle steady-state DC. Use the minimum copper width per IPC-2152 for the RMS current, and keep the total area under 1.5 cm².

### Switching Node Shielding

Place the switching node pour on **L1 only**, with L2 GND plane directly underneath providing an electrostatic shield:

```
  L1:  ┌──SW Node──┐
       │  (1.5 cm²) │  ← dV/dt surface
       └────────────┘
  ─────────────────────── L2: Continuous GND plane (shield)
       No switching node copper on L3, L4, L5, L6
```

The L2 GND plane capacitively couples to the switching node, but the resulting displacement current flows into the GND plane (contained) rather than radiating. The GND plane must be **continuous** under the switching node — no splits, no vias, no trace interruptions.

## 4. Resonant Tank Layout — Lr/Cr Symmetry

### Why Symmetry Matters

The 3-phase interleaved LLC converter depends on balanced current sharing between phases. The resonant tank components (Lr and Cr) set the resonant frequency for each phase:

```
f_r = 1 / (2π × √(Lr × Cr))

If Lr or Cr vary between phases, f_r varies, causing:
  - Unequal current sharing
  - One phase may lose ZVS while others maintain it
  - Unequal thermal stress → premature failure of the hottest phase
  - Increased output ripple (imperfect interleaving)
```

### Symmetry Targets

| Parameter | Matching Target | Impact of Mismatch |
|-----------|----------------|-------------------|
| Lr (resonant inductor) | ±1% between phases | 0.5% frequency shift per 1% Lr change |
| Cr (resonant capacitor) | ±1% between phases | 0.5% frequency shift per 1% Cr change |
| PCB parasitic inductance (Lr path) | ±0.5 nH between phases | Adds to Lr; affects matching |
| PCB parasitic capacitance (Cr path) | ±1 pF between phases | Adds to Cr; negligible at nF level |
| Transformer leakage inductance | ±2% between phases | Major contributor to total Lr |

### Layout Strategy for Resonant Tank Symmetry

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| **R-1** | Place Lr and Cr at identical positions relative to MOSFETs in each phase | Equal trace lengths → equal parasitic inductance |
| **R-2** | Use identical trace routing for Lr/Cr connections across all 3 phases | Replicate layout exactly |
| **R-3** | Keep Lr/Cr traces on the same layer (L1) for all phases | Avoids layer-dependent parasitic variation |
| **R-4** | Lr and Cr placed between the half-bridge and the transformer | Natural signal flow: bus → bridge → Lr → Cr → TX |
| **R-5** | If Lr is integrated into transformer leakage, ensure equal air-gap tolerance | Mechanical tolerance directly affects Lr |
| **R-6** | Use matched Cr components from same production lot | Capacitance tolerance matching |

### Resonant Tank Physical Layout

```
  Per Phase (replicated ×3):

  Q1─┐
     ├── SW Node ── [Lr] ── [Cr] ── [TX Primary]
  Q2─┘
       │←─ 15mm ──→│←5mm→│←─ 10mm ──→│

  Total SW-to-TX primary path: ~30 mm
  Must be identical (±1 mm) across all 3 phases
```

### Resonant Current Loop

The resonant tank carries **high circulating current** (potentially exceeding the load current due to the resonant nature):

```
I_Lr_peak ≈ I_load × π/2 × n ≈ 28 × 1.57 × 1.1 ≈ 48 A peak (per phase)
I_Lr_rms ≈ I_Lr_peak / √2 ≈ 34 A RMS (per phase)
```

The resonant current flows in a loop: **C_bus → Q1 → SW node → Lr → Cr → TX primary → TX primary return → C_bus return**. This loop must be kept compact but not as aggressively minimized as the commutation loop (since the resonant current is sinusoidal, not a fast step).

> [!note] Resonant Loop vs. Commutation Loop
> Do not confuse the resonant current loop with the commutation loop. The **commutation loop** (analyzed in [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]]) is the high-frequency path during switching transitions and must be minimized to <8 nH. The **resonant loop** carries the sinusoidal resonant current and can tolerate more inductance (the extra PCB inductance just adds slightly to Lr, which can be compensated in the inductor design).

## 5. Transformer Common-Mode Current

### CM Current Generation

The transformer is the primary source of common-mode (CM) noise coupling between the primary and secondary domains. CM current flows through the inter-winding capacitance (C_winding) driven by the dV/dt across the transformer:

```
I_CM = C_winding × dV/dt

For 3 transformers:
  C_winding ≈ 30 pF per transformer (typical for 10 kW wound transformer)
  dV/dt ≈ 20 kV/µs (LLC near-resonance; lower than hard-switched)

  I_CM = 3 × 30e-12 × 20e9 = 1.8 mA (total, 3 phases)
```

During loss of ZVS:
```
  dV/dt ≈ 60 kV/µs
  I_CM = 3 × 30e-12 × 60e9 = 5.4 mA (worst case)
```

> [!warning] CM Current Path
> The 1.8–5.4 mA CM current must have a defined, low-impedance return path. If no return path is provided, the CM current flows through parasitic capacitances to the chassis/PE, through the mains earth, and back — radiating along the way. The defined return path is provided by **Y-capacitors** between primary GND and secondary GND, placed at the isolation barrier.

### CM Current Mitigation Layout

| Strategy | Implementation | Effectiveness |
|----------|---------------|---------------|
| **Y-capacitors** | 2× 4.7 nF / 3 kV safety-rated (Y1 class) between primary and secondary GND, at isolation barrier | High — provides low-Z return path |
| **Faraday shield** | Grounded copper foil between primary and secondary windings in transformer | High — shunts CM current to primary GND before it reaches secondary |
| **Balanced winding** | Symmetric winding structure reduces net CM voltage | Medium — depends on transformer construction |
| **CM choke on output** | Nanocrystalline CM choke on output cables | High — blocks CM current on output leads |
| **Stitching via fence** | Dense vias around transformer cutout, connecting L1 to L2 GND | Medium — reduces PCB-level coupling |

### Y-Capacitor Placement

```
  Primary GND ───┬─── [Y-cap 4.7nF] ───┬─── Secondary GND
                  │                      │
  (at isolation   └─── [Y-cap 4.7nF] ───┘   (at isolation
   barrier, pri         (redundant)           barrier, sec
   side)                                      side)
```

| Parameter | Specification |
|-----------|--------------|
| Capacitance | 4.7 nF each (2 in parallel for redundancy) |
| Voltage rating | ≥3 kV (Y1 safety class) |
| Placement | At isolation barrier, shortest possible path across the slot |
| Leakage current | Total: 2 × 4.7e-9 × 920 × 2π × 150e3 = 8.2 mA (check against safety limit of 10 mA for Class I equipment) |

> [!warning] Y-Capacitor Leakage Current
> The Y-capacitor leakage current at full bus voltage and switching frequency approaches the 10 mA safety limit. Verify with the actual switching waveform (not a continuous sine wave). If needed, reduce to 2.2 nF per capacitor to halve the leakage current. See [[09-Protection and Safety]] for earth leakage requirements.

## 6. Inter-Phase Isolation

### Stitching Via Fences Between Phases

Although the three LLC phases share the same primary and secondary voltage domains, they must be isolated from each other to prevent:
- Magnetic coupling between resonant inductors
- Capacitive coupling between switching nodes
- Conducted noise from one phase's high-dI/dt loop coupling into another phase's gate driver

| Boundary | Via Fence Specification |
|----------|----------------------|
| Phase A ↔ Phase B | Double row of stitching vias (L1 to L2), 2.5 mm pitch, spanning full primary zone height |
| Phase B ↔ Phase C | Same as above |
| Around each transformer cutout | Single row of stitching vias, 3 mm pitch, full perimeter of cutout |
| Board perimeter | Single row, 5 mm pitch |

### Via Fence Physical Implementation

```
  Phase A      │ Via Fence │     Phase B      │ Via Fence │     Phase C
               │ ○ ○ ○ ○  │                   │ ○ ○ ○ ○  │
  [Q1A][Q2A]   │ ○ ○ ○ ○  │   [Q1B][Q2B]     │ ○ ○ ○ ○  │   [Q1C][Q2C]
               │ ○ ○ ○ ○  │                   │ ○ ○ ○ ○  │
  [Lr_A][Cr_A] │ ○ ○ ○ ○  │   [Lr_B][Cr_B]   │ ○ ○ ○ ○  │   [Lr_C][Cr_C]
               │ ○ ○ ○ ○  │                   │ ○ ○ ○ ○  │

  ○ = stitching via (0.3mm, L1 GND pad to L2 GND plane)
  Double row, 2.5mm pitch, staggered
```

### Via Fence Shielding Effectiveness

```
For a via fence with pitch p at frequency f:

Shielding effectiveness degrades when:
  p > λ/20

At 200 MHz (highest concern frequency):
  λ = c / f = 3e8 / 200e6 = 1.5 m
  λ/20 = 75 mm

At 2.5 mm pitch, the fence is effective well beyond 200 MHz.
Actual shielding effectiveness: >40 dB up to several GHz.
```

## 7. L2 GND Plane Management

### Continuity Rules

The L2 GND plane is the foundation of the EMI strategy. Its continuity must be preserved:

| Zone | L2 GND Plane Rule |
|------|-------------------|
| DC bus input zone | Continuous, no splits |
| Primary bridge zone | Continuous under all gate drivers and sense circuits |
| Isolation barrier | Split into primary GND and secondary GND (only split on the board) |
| Transformer cutout | GND plane removed at cutout; surround with stitching vias |
| Secondary rectifier zone | Secondary GND continuous |
| Output zone | Secondary GND continuous |
| Phase boundaries | GND plane continuous across phases (not split between phases) |

> [!warning] GND Plane Splits — Only at Isolation Barrier
> The L2 GND plane may **only** be split at the primary-secondary isolation barrier. Do NOT split the GND plane between phases, between power and signal, or for any other reason. A split GND plane forces return currents to find alternative paths, dramatically increasing loop area and EMI.

### GND Plane Voiding Strategy

Where copper must be removed from L2 (e.g., for high-voltage clearance around mounting holes or transformer cutouts):

| Situation | Voiding Strategy |
|-----------|-----------------|
| TO-247 mounting hole | 0.5 mm clearance from M3 hole (insulated bushing provides isolation) |
| Transformer cutout | L2 copper removed 2 mm beyond cutout edge; stitching vias on perimeter |
| High-voltage trace crossing on L3 | Allowed over unbroken L2 (L2 acts as shield, not signal return for HV) |
| Bus bar mounting holes | 1 mm clearance from bolt hole |

## 8. Output Cable EMI

### The Output Cable as an Antenna

The output cables connecting the PDU to the EV carry up to 100 A DC. Any CM noise current on these cables radiates efficiently because the cable length (typically 2–5 m) is comparable to λ/4 at EMI frequencies of interest:

```
At 30 MHz: λ = 10 m, λ/4 = 2.5 m → cable is a quarter-wave antenna
At 150 kHz (start of conducted EMI band): λ = 2000 m → cable is electrically short
```

### Output EMI Mitigation

| Strategy | Implementation | Location |
|----------|---------------|----------|
| CM choke | Nanocrystalline toroid, both output conductors through core | At P3 output connector, on-board or external |
| Output filter capacitors | Additional MLCC bank at P3 connector pads | Output zone, last component before connector |
| Cable shielding | Shielded output cable with shield grounded at PDU end | External (cable specification) |
| Ferrite clamp | Snap-on ferrite on output cable | External (field fix if needed) |

### Output CM Choke Sizing

```
For conducted EMI compliance (EN 61000-6-3 / CISPR 11 Class B):
  Required attenuation at 150 kHz: ~40 dB (typical)
  Required impedance: Z_CM = 50 × 10^(40/20) = 5 kΩ at 150 kHz

  L_CM = Z_CM / (2πf) = 5000 / (2π × 150e3) = 5.3 mH

  Core: Nanocrystalline toroid (e.g., Vacuumschmelze W424 or equivalent)
  Turns: 8–12 turns of both output conductors
  Current rating: 100 A DC (core must not saturate — nanocrystalline has high B_sat)
```

> [!tip] CM Choke Placement
> Mount the CM choke as close to the output connector P3 as possible. Any PCB trace between the choke and the connector adds parasitic capacitance that bypasses the choke at high frequency. Ideally, the choke is the last component in the signal path before the connector.

## 9. EMI-Critical Component Placement Summary

| Component | EMI Constraint | Placement Rule |
|-----------|---------------|----------------|
| Primary switching node | ≤1.5 cm² area | L1 only, L2 GND shield underneath |
| Secondary switching node | ≤2.0 cm² area (more margin) | L1 only, L2 GND shield underneath |
| Resonant inductor Lr | Magnetic coupling risk | ≥15 mm from adjacent phase Lr, oriented perpendicular or shielded |
| Resonant capacitor Cr | Matched across phases | Identical layout position in each phase |
| Transformer | CM capacitance source | Faraday shield in winding, Y-caps at barrier |
| Gate driver signals | Susceptible to dV/dt coupling | Route on L3 under L2 GND shield, away from SW node |
| Current sense traces | Susceptible to dI/dt coupling | Kelvin connection, differential pair, L3 |
| Voltage sense traces | Susceptible to dV/dt coupling | High-impedance; route away from switching nodes |
| Y-capacitors | CM return path | At isolation barrier, shortest path |
| Output CM choke | Last filter element | Adjacent to P3 connector |
| Bus decoupling caps | Contain HF current | Directly at MOSFET pads (Tier 0) |

## 10. EMI Testing Considerations

### Test Points for Pre-Compliance

Include the following test provisions on the PCB:

| Test Point | Location | Purpose |
|------------|----------|---------|
| SMA connector (50 Ω) at primary SW node | Phase A, L1 | Measure switching waveform with oscilloscope |
| SMA connector at secondary SW node | Phase A, L1 | Secondary switching waveform |
| Current probe loop (0603 0Ω) in DC bus path | Phase A, L1 | Insert Rogowski or clip-on current probe |
| Current probe loop in output path | Output zone | Output ripple current measurement |
| GND test point near isolation barrier | L1, both sides | Measure CM voltage across barrier |

### Pre-Compliance EMI Scan Frequencies

| Standard | Frequency Range | Measurement |
|----------|----------------|-------------|
| CISPR 11 Class B (conducted) | 150 kHz – 30 MHz | LISN on input and output |
| CISPR 11 Class B (radiated) | 30 MHz – 1 GHz | Antenna measurement (3 m or 10 m) |
| EN 61000-6-3 | 150 kHz – 30 MHz | Conducted emissions limit |

## 11. Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board summary
- [[07-PCB-Layout/DC-DC/02-Power Loop Analysis|Power Loop Analysis]] — Commutation loop inductance (drives dV/dt)
- [[07-PCB-Layout/DC-DC/03-Gate Driver Layout|Gate Driver Layout]] — Isolation barrier, signal routing
- [[07-PCB-Layout/DC-DC/06-Creepage and Clearance|Creepage and Clearance]] — Isolation barrier physical dimensions
- [[07-PCB-Layout/AC-DC/05-EMI-Aware Layout|AC-DC EMI-Aware Layout]] — Input-side EMI strategies
- [[09-Protection and Safety]] — EMC compliance requirements, earth leakage limits

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
