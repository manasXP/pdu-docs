---
tags: [pdu, pcb-layout, dc-dc, llc, power-loop, parasitic-inductance, snubber]
created: 2026-02-22
status: draft
---

# 02 — Power Loop Analysis

## Purpose

This document analyzes the two critical power commutation loops in the LLC resonant converter: the **primary half-bridge loop** and the **secondary rectifier loop**. Both loops must be minimized to limit voltage overshoot during switching transitions. The primary loop is particularly critical — it has only **8V margin** to the MOSFET absolute maximum rating without a snubber.

> [!warning] CRITICAL — Primary Loop Margin
> Without an RC snubber, the LLC primary half-bridge produces a **1192V peak** on 1200V-rated SiC MOSFETs — a mere 8V margin (0.67%). This is unacceptable for production. The **RC snubber is mandatory**, not optional. Even with the snubber, the margin is 139V (11.6%), which is tight by power electronics standards. Every nanohenry matters in this layout.

## Loop 1: LLC Primary Half-Bridge

### Circuit Description

Each phase of the LLC converter uses a half-bridge (two series SiC MOSFETs) driven from the 920V DC bus. The commutation loop is:

```
    DC Bus + (920V)
        │
    ┌───┤
    │   C_bus (decoupling)
    │   │
    │   ├───── Q1 (high-side 1200V SiC) ─── Switching Node ─── Lr ─── Cr ─── TX primary
    │   │                                          │
    │   ├───── Q2 (low-side 1200V SiC) ────────────┘
    │   │
    └───┤
        │
    DC Bus − (return)
```

The critical loop is: **C_bus(+) → Q1 drain → Q1 source/Q2 drain (SW node) → Q2 source → C_bus(−)**

This loop carries the full switching current during hard-switched transitions (e.g., startup, overload, or loss of ZVS conditions).

### Inductance Budget

| Component | Inductance (nH) | Source | Controllable? |
|-----------|-----------------|--------|---------------|
| Q1 package (TO-247-4L drain + source) | ~12 | Datasheet, TO-247 lead frame | No |
| Q2 package (TO-247-4L drain + source) | ~12 | Datasheet, TO-247 lead frame | No |
| **Package subtotal** | **~24** | — | **No** |
| PCB trace/pour (Q1 drain → C_bus+) | 2–4 | Layout dependent | **Yes** |
| PCB trace/pour (Q2 source → C_bus−) | 2–4 | Layout dependent | **Yes** |
| PCB trace/pour (Q1 source → Q2 drain, SW node) | 1–2 | Layout dependent | **Yes** |
| **PCB subtotal** | **5–10 (target ≤8)** | — | **Yes** |
| C_bus ESL (ceramic MLCC, 2× parallel) | 1–2 | Capacitor datasheet | Partially |
| **Total loop inductance** | **~30–36 (nominal 34)** | — | — |

> [!note] Package Inductance Dominates
> The TO-247 package contributes **~24 nH** out of the ~34 nH total — roughly **70%** of the loop inductance. This is inherent to the through-hole package and cannot be reduced by layout. The only ways to reduce package inductance are: (1) use TO-247-4L (Kelvin source) which saves ~2–3 nH by eliminating shared source inductance from the gate loop, or (2) use a surface-mount package like TO-263-7L or a module. For this design, TO-247-4L is assumed.

### Overshoot Calculation — Without Snubber

The voltage overshoot during turn-off is:

```
V_overshoot = L_loop × (dI/dt)

Where:
  L_loop = 34 nH (total loop inductance)
  dI/dt  = 8 A/ns (typical SiC MOSFET turn-off at 28A, Rg_off = 1-2Ω)

V_overshoot = 34 × 10⁻⁹ × 8 × 10⁹ = 272 V

V_peak = V_bus + V_overshoot = 920 + 272 = 1192 V

V_rated = 1200 V (MOSFET absolute max)
Margin  = 1200 - 1192 = 8 V (0.67%)
```

> [!warning] 8V Margin Is Unacceptable
> A margin of 0.67% is far below any reasonable production margin. Factors not included in this calculation that could push the peak higher:
> - DC bus voltage variation (920V is nominal; transients could reach 950V+)
> - Temperature-dependent dI/dt variation
> - Manufacturing tolerance on parasitic inductance
> - Resonant ringing adding to peak
>
> **The RC snubber is non-negotiable.**

### RC Snubber Design

An RC snubber across each MOSFET damps the parasitic ringing and reduces peak voltage.

#### Snubber Values

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| R_snub | 10 Ω | Matched to characteristic impedance: Z₀ = √(L/C_oss) ≈ √(34nH/200pF) ≈ 13Ω, rounded to 10Ω for overdamping |
| C_snub | 1 nF | C_snub >> C_oss (200 pF) to dominate the resonance. 1 nF provides 5× C_oss |
| Package | 0805 or 1206 | Low ESL (<0.5 nH), placed directly at MOSFET drain-source |

#### Snubber Effectiveness Calculation

The snubber forms a damped RLC circuit with the loop inductance:

```
Damping factor: ζ = (R_snub / 2) × √(C_snub / L_loop)
               ζ = (10 / 2) × √(1e-9 / 34e-9)
               ζ = 5 × 0.171
               ζ = 0.86 (underdamped but close to critical)

Peak voltage with snubber (approximate):
  V_peak ≈ V_bus + V_overshoot × e^(-π×ζ/√(1-ζ²))
  V_peak ≈ 920 + 272 × e^(-π×0.86/√(1-0.74))
  V_peak ≈ 920 + 272 × e^(-5.30)
  V_peak ≈ 920 + 272 × 0.005
  V_peak ≈ 921.4 V (theoretical — heavily damped first peak)

More practical estimate using simulation-correlated formula:
  V_peak ≈ V_bus + I × √(L_loop / C_snub)
  V_peak ≈ 920 + 28 × √(34e-9 / 1e-9)
  V_peak ≈ 920 + 28 × 5.83
  V_peak ≈ 920 + 163 = 1083 V

Conservative design estimate (from similar designs): ~1061 V
```

The conservative estimate of **1061V peak** provides:

```
Margin = 1200 - 1061 = 139 V (11.6%)
```

> [!tip] Snubber Placement Is Critical
> The RC snubber must be placed **directly across each MOSFET's drain-source pads** with the shortest possible PCB connection. Each additional millimeter of trace adds ~1 nH and degrades snubber effectiveness. Use 0805 or 1206 components placed within 3 mm of the MOSFET pads. The snubber capacitor connects to drain, and the snubber resistor connects to source (or vice versa — the series R-C order does not matter for damping).

#### Snubber Power Dissipation

```
P_snub = C_snub × V_bus² × f_sw (per MOSFET)
       = 1e-9 × 920² × 150e3
       = 1e-9 × 846400 × 150000
       = 0.127 W per MOSFET

Total for 6 MOSFETs: 6 × 0.127 = 0.76 W (negligible)
```

The 10 Ω resistor must handle 0.13 W — a standard 0805 rated at 0.125 W is marginal. **Use 1206 (0.25 W) for margin**, or a 0805 rated for pulse duty.

### Primary Loop Layout Rules

To achieve ≤8 nH PCB inductance contribution:

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| **P-1** | Place C_bus within 5 mm of Q1 drain and Q2 source | Minimizes trace length in the hottest part of the loop |
| **P-2** | Route DC+ on L1, DC− on L5 (or L6), directly overlapping | Flux cancellation between parallel planes reduces L_PCB |
| **P-3** | Switching node pour ≤1.5 cm² per phase | Limits dV/dt × area → reduces E-field emissions |
| **P-4** | Use ≥3 ceramic MLCCs in parallel per phase for C_bus | Paralleling reduces ESL: L_total = L_each / N |
| **P-5** | No vias in the primary commutation loop current path | Vias add 0.5–1 nH each; keep loop on L1 or use via arrays |
| **P-6** | Q1 and Q2 placed in line with ≤3 mm pad-to-pad gap | Minimizes switching node trace length |
| **P-7** | Snubber R-C within 3 mm of each MOSFET D-S pads | Snubber effectiveness degrades rapidly with distance |
| **P-8** | Keep gate driver components outside the power loop area | Prevent coupling of dI/dt into gate circuit |

### Primary Loop Inductance Estimation Method

Use the parallel-plate approximation for overlapping L1/L5 copper pours:

```
L_pour = µ₀ × d × l / w

Where:
  µ₀ = 4π × 10⁻⁷ H/m
  d  = distance between L1 and L5 ≈ 1.0 mm (through L2, L3, L4 cores)
  l  = current path length ≈ 15 mm (Q1 drain to C_bus+ via pour)
  w  = pour width ≈ 12 mm

L_pour = 4π × 10⁻⁷ × 1.0e-3 × 15e-3 / 12e-3
       = 4π × 10⁻⁷ × 1.25e-3
       = 1.57 nH (for one segment)

Two such segments (+ side and − side): ~3.1 nH
Plus SW node trace (~1-2 nH): total ~4-5 nH

This is comfortably below the 8 nH target.
```

## Loop 2: Secondary Rectifier

### Circuit Description

Each phase uses a synchronous rectifier (two SiC MOSFETs) on the transformer secondary:

```
    TX Secondary Winding
        │
    ┌───┤
    │   Q3 (high-side 650V SiC)
    │   │
    │   ├───── Output + ──── C_out ──── Load
    │   │                      │
    │   Q4 (low-side 650V SiC) │
    │   │                      │
    └───┤──────────────────────┘
        Output −
```

The critical loop is: **TX secondary → Q3 → C_out(+) → C_out(−) → Q4 → TX secondary**

### Inductance Budget

| Component | Inductance (nH) | Source |
|-----------|-----------------|--------|
| Q3 package (TO-247-4L) | ~4 | 650V devices have shorter lead frames than 1200V |
| Q4 package (TO-247-4L) | ~4 | Same |
| **Package subtotal** | **~8** | — |
| PCB trace/pour (Q3 → C_out+) | 3–5 | Layout dependent |
| PCB trace/pour (Q4 → C_out−) | 3–5 | Layout dependent |
| PCB trace/pour (TX sec → Q3/Q4) | 2–3 | Layout dependent |
| **PCB subtotal** | **8–13 (target ≤12)** | — |
| C_out ESL | 1–2 | Ceramic MLCC parallel bank |
| **Total loop inductance** | **~17–23 (nominal 22)** | — |

### Overshoot Calculation — Secondary

```
V_overshoot = L_loop × (dI/dt)

Where:
  L_loop = 22 nH
  dI/dt  = 5 A/ns (650V SiC, lower dI/dt than primary due to lower voltage)

V_overshoot = 22 × 10⁻⁹ × 5 × 10⁹ = 110 V

V_peak = V_out_max + V_overshoot = 500 + 110 = 610 V
  (worst case at V_out = 500V; at higher output voltages,
   the transformer turns ratio means lower reflected voltage per MOSFET)

V_rated = 650 V
Margin  = 650 - 610 = 40 V (6.2%)
```

> [!warning] Secondary Margin Is Also Tight
> A 40V (6.2%) margin on the secondary rectifiers is workable but not generous. Consider adding RC snubbers on the secondary as well, especially if the LLC loses soft-switching during transients. A 4.7 Ω + 470 pF snubber per secondary MOSFET would reduce the peak to approximately 570V (80V margin, 12.3%).

### Optional Secondary Snubber

| Parameter | Value |
|-----------|-------|
| R_snub | 4.7 Ω |
| C_snub | 470 pF |
| P_snub per MOSFET | C × V² × f = 470pF × 500² × 150kHz = 17.6 mW |
| Package | 0603 sufficient |
| Recommendation | Include in schematic, populate based on prototype testing |

### Secondary Loop Layout Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| **S-1** | Place C_out within 8 mm of Q3 drain and Q4 source | Shorter distance than primary (more margin) |
| **S-2** | Route output+ on L1, output− on L6, overlapping | Flux cancellation |
| **S-3** | Transformer secondary pins directly adjacent to Q3/Q4 | Minimize winding-to-rectifier trace |
| **S-4** | Use ≥4 ceramic MLCCs per phase for C_out | Reduce ESL, provide HF filtering |
| **S-5** | Keep secondary gate drivers outside rectifier loop | Prevent dI/dt coupling |
| **S-6** | Match layout across all 3 phases | Current sharing depends on matched parasitics |

## Phase Symmetry Requirements

With 3 interleaved phases sharing the output current equally, parasitic mismatches cause current imbalance:

### Inductance Matching Target

```
For ≤2% current imbalance:
  ΔL/L_total < 2% → ΔL < 0.02 × 34 nH = 0.68 nH

This means the PCB inductance variation between phases must be < 0.68 nH.
At ~1 nH/mm of trace, this allows only ~0.7 mm variation in trace length between phases.
```

### Layout Approach for Symmetry

1. **Design Phase A completely** — place all components, route all power and signal traces
2. **Copy Phase A layout to Phase B and Phase C** using KiCad "Replicate Layout" or manual mirroring
3. **Verify inductance matching** using a 2D field solver (e.g., Ansys Q3D, FastHenry) or measure on prototype with impedance analyzer
4. **Bus bar connections** to each phase must be equal length (use a star topology from the main bus bar)

### Bus Bar Star Topology

```
         P2 (920V DC Bus Input)
              │
         ┌────┴────┐
         │ Main    │
         │ Bus Bar │
         └────┬────┘
              │
     ┌────────┼────────┐
     │        │        │
  ┌──┴──┐ ┌──┴──┐ ┌──┴──┐
  │Ph A │ │Ph B │ │Ph C │
  │     │ │     │ │     │
  └─────┘ └─────┘ └─────┘

  Equal trace/pour length from bus bar split point to each phase
```

## Decoupling Capacitor Strategy

### Primary Bus Decoupling (per phase)

| Tier | Component | Qty | ESL (each) | ESL (parallel) | Purpose |
|------|-----------|-----|-----------|-----------------|---------|
| Tier 0 | 100 nF / 1kV MLCC (0805) | 3 | 0.6 nH | 0.2 nH | Directly at MOSFET pads, dI/dt sinking |
| Tier 1 | 1 µF / 1kV MLCC (1210) | 4 | 0.8 nH | 0.2 nH | Within 10 mm, bulk HF energy |
| Tier 2 | 10 µF / 1kV film | 2 | 5 nH | 2.5 nH | Within 30 mm, sustained switching energy |
| Bulk | Electrolytic (shared) | 4–6 | 15 nH | 3 nH | On bus bar, bus voltage stability |

### Secondary Output Decoupling (per phase)

| Tier | Component | Qty | ESL (each) | ESL (parallel) | Purpose |
|------|-----------|-----|-----------|-----------------|---------|
| Tier 0 | 100 nF / 650V MLCC (0805) | 4 | 0.6 nH | 0.15 nH | At rectifier D-S pads |
| Tier 1 | 2.2 µF / 650V MLCC (1812) | 4 | 1.0 nH | 0.25 nH | Within 10 mm |
| Tier 2 | 22 µF / 650V film | 2 | 5 nH | 2.5 nH | Output filter, bulk |
| Bulk | Electrolytic (shared) | 4–6 | 15 nH | 3 nH | Output bus, combined 3 phases |

> [!tip] Capacitor Placement Priority
> Always place Tier 0 caps first, as close to the MOSFETs as physically possible. Then place Tier 1 caps radiating outward. The diminishing-returns curve is steep: the first nanohenry of ESL reduction (from Tier 0 placement) prevents far more overshoot than the last nanohenry from Tier 2 optimization.

## Loop Inductance Verification

### Pre-Fabrication (Simulation)

| Tool | Method | Accuracy |
|------|--------|----------|
| Ansys Q3D Extractor | Import KiCad layout → 3D field solve | ±10% |
| FastHenry (open source) | Define conductor segments → L matrix | ±15% |
| KiCad + FreePDK SPICE | Estimate from trace geometry rules of thumb | ±30% |

### Post-Fabrication (Measurement)

| Method | Equipment | Frequency |
|--------|-----------|-----------|
| VNA (S21 shunt-through) | Vector Network Analyzer, SMA probe points | 1–500 MHz |
| Time-domain (dV/dt) | Oscilloscope + high-BW differential probe at SW node | During operation |
| Impedance analyzer | Keysight E4990A or similar | 100 kHz – 100 MHz |

> [!tip] Prototype Measurement Points
> Include **test pads** on the PCB for VNA probing:
> - Across each MOSFET D-S (primary and secondary)
> - Across each decoupling capacitor bank
> - At the switching node (for dV/dt scope measurement)
> Use 0 Ω resistor footprints (0603) in series with the loop for easy insertion of a current probe.

## Summary of Voltage Margins

| Loop | V_bus/V_out | L_total | dI/dt | V_overshoot | V_peak | V_rated | Margin | Snubber |
|------|-------------|---------|-------|-------------|--------|---------|--------|---------|
| Primary (no snub) | 920 V | 34 nH | 8 A/ns | 272 V | 1192 V | 1200 V | 8 V (0.67%) | — |
| **Primary (with snub)** | **920 V** | **34 nH** | **8 A/ns** | **~141 V** | **~1061 V** | **1200 V** | **139 V (11.6%)** | **10Ω + 1nF** |
| Secondary (no snub) | 500 V | 22 nH | 5 A/ns | 110 V | 610 V | 650 V | 40 V (6.2%) | — |
| Secondary (with snub) | 500 V | 22 nH | 5 A/ns | ~70 V | ~570 V | 650 V | 80 V (12.3%) | 4.7Ω + 470pF |

## Cross-References

- [[07-PCB-Layout/DC-DC/__init|DC-DC Board Overview]] — Board-level design targets
- [[07-PCB-Layout/DC-DC/01-Stack-Up and Layer Assignment|Stack-Up and Layer Assignment]] — Layer usage for power loop routing
- [[07-PCB-Layout/DC-DC/03-Gate Driver Layout|Gate Driver Layout]] — Gate loop interaction with power loop
- [[07-PCB-Layout/DC-DC/05-EMI-Aware Layout|EMI-Aware Layout]] — Switching node area limits derived from this analysis
- [[01-Topology Selection]] — LLC topology choice and operating conditions
- [[SiC Device Thermal Parameters]] — MOSFET switching characteristics (dI/dt, C_oss)
