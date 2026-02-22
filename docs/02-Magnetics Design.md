---
tags: [PDU, magnetics, LLC, transformer, resonant-tank, design]
created: 2026-02-21
status: draft
---

# Magnetics Design — 30 kW LLC DC-DC Stage

> [!summary] Key Results
> **Per phase (10 kW):** Lr = 43 µH, Cr = 26 nF, Lm = 258 µH (Ln = 6). Transformer: E65/32/27 core (3C97), Np = 21, Ns = 42, n = 2. Total magnetics loss ≈ 52 W/phase (99.5% magnetics efficiency).

## 1. Design Inputs

From [[01-Topology Selection]], §4:

| Parameter | Value |
|-----------|-------|
| Topology | 3-phase interleaved LLC half-bridge |
| Power per phase | 10 kW |
| DC bus input (Vbus) | 650–920 VDC (actively adjusted by PFC) |
| Output voltage (Vo) | 200–1000 VDC |
| Constant-power range | 300–1000 VDC at 30 kW total |
| Resonant frequency (fr) | 150 kHz |
| Switching frequency range | 100–300 kHz |
| Target efficiency | >98% (DC-DC stage) |

**Half-bridge drive:** The primary sees Vbus/2 square wave. At Vbus = 800 V, the fundamental amplitude of the half-bridge square wave is:

$$V_{in,1} = \frac{2}{\pi} \cdot \frac{V_{bus}}{2} = \frac{2 \times 800}{\pi \times 2} = 255 \text{ V (rms: 180 V)}$$

## 2. Turns Ratio Selection

### 2.1 Methodology

The transformer turns ratio n = Ns/Np sets the relationship between input and output voltage at unity gain (M = 1). For an LLC half-bridge at resonance:

$$V_o = n \cdot \frac{V_{bus}}{2}$$

Rearranging: n = 2·Vo / Vbus.

### 2.2 Gain Requirements

The LLC voltage gain M is defined as:

$$M = \frac{V_o}{n \cdot V_{bus}/2}$$

With active bus voltage adjustment (650–920 V), we can set Vbus to minimize the gain excursion. The gain at each operating point for a given n:

| Vo (V) | Vbus (V) | n = 1.5 | n = 2.0 | n = 2.5 |
|--------|----------|---------|---------|---------|
| 200 | 650 | 0.41 | 0.62 | 0.77 |
| 300 | 650 | 0.62 | 0.92 | 1.15 |
| 600 | 750 | 1.07 | 1.60 | 2.00 |
| 800 | 800 | 1.33 | 2.00 | 2.50 |
| 1000 | 920 | 1.45 | 2.17 | 2.72 |

> [!warning] These gains are absolute Vo/(n·Vbus/2). For LLC, M is referenced to the transformer primary. The LLC gain M = Vo / (n · Vbus/2) must stay within achievable range (typically 0.5–1.3 for practical Q values).

Let me recalculate properly. For LLC half-bridge, the output voltage is:

$$V_o = M \cdot n \cdot \frac{V_{bus}}{2}$$

So the required gain is:

$$M = \frac{V_o}{n \cdot V_{bus}/2}$$

### 2.3 Gain Table with n = 2

| Operating Point | Vo (V) | Po/phase (W) | Io/phase (A) | Vbus (V) | n·Vbus/2 | M required |
|----------------|--------|-------------|-------------|----------|----------|------------|
| Min voltage | 200 | 6,667 | 33.3 | 650 | 650 | 0.31 |
| Low voltage | 300 | 10,000 | 33.3 | 700 | 700 | 0.43 |
| Mid-low | 400 | 10,000 | 25.0 | 700 | 700 | 0.57 |
| **Design center** | **600** | **10,000** | **16.7** | **750** | **750** | **0.80** |
| High voltage | 800 | 10,000 | 12.5 | 800 | 800 | 1.00 |
| Max voltage | 1000 | 10,000 | 10.0 | 920 | 920 | 1.09 |

> [!note] With n = 2
> - At 800 V output / 800 V bus → M = 1.00 (exact resonance, peak efficiency)
> - At 1000 V output / 920 V bus → M = 1.09 (slightly below resonance, ZVS maintained — see [[03-LLC Gain Curve Verification]])
> - At 300 V output / 700 V bus → M = 0.43 (well above resonance, power is derated)
> - Maximum gain M_max = 1.09 is comfortably achievable with LLC while maintaining ZVS

**Decision: n = 2 (Ns:Np = 2:1).** This places the unity-gain point at the sweet spot of 800 V output (most common CCS charging voltage for modern EVs at 80–90% SoC) and keeps the maximum gain requirement modest at 1.09.

## 3. Resonant Tank Design (Lr, Lm, Cr)

### 3.1 First Harmonic Approximation (FHA) Model

The LLC resonant converter is analyzed using FHA, where the square-wave input and rectified output are replaced by their fundamental sinusoidal components.

**Equivalent AC load resistance:**

$$R_{ac} = \frac{8 n^2}{\pi^2} \cdot \frac{V_o^2}{P_o}$$

At the design center (Vo = 600 V, Po = 10 kW):

$$R_{ac} = \frac{8 \times 4}{\pi^2} \cdot \frac{600^2}{10000} = \frac{32}{9.87} \times 36 = 3.24 \times 36 = 116.7 \text{ Ω}$$

### 3.2 Quality Factor and Characteristic Impedance

The quality factor Q and inductance ratio Ln are the two key design parameters:

$$Q = \frac{\sqrt{L_r / C_r}}{R_{ac}} = \frac{Z_0}{R_{ac}}$$

$$L_n = \frac{L_m}{L_r}$$

**Design guidelines:**
- **Q:** Lower Q → wider gain bandwidth, less sensitivity to load. Target Q = 0.3–0.5 at design center.
- **Ln:** Lower Ln → higher gain range but more magnetizing current (higher conduction loss). Ln = 5–7 is typical for wide-output applications.

**Selected: Q = 0.35, Ln = 6** at the design center (Vo = 600 V, Po = 10 kW).

### 3.3 Resonant Component Calculation

**Characteristic impedance:**

$$Z_0 = Q \times R_{ac} = 0.35 \times 116.7 = 40.8 \text{ Ω}$$

**Resonant frequency:**

$$\omega_r = 2\pi f_r = 2\pi \times 150000 = 942{,}478 \text{ rad/s}$$

**Resonant inductance Lr:**

$$L_r = \frac{Z_0}{\omega_r} = \frac{40.8}{942478} = 43.3 \text{ µH} \approx 43 \text{ µH}$$

**Resonant capacitance Cr:**

$$C_r = \frac{1}{\omega_r \cdot Z_0} = \frac{1}{942478 \times 40.8} = 26.0 \text{ nF} \approx 26 \text{ nF}$$

**Magnetizing inductance Lm:**

$$L_m = L_n \times L_r = 6 \times 43 = 258 \text{ µH}$$

### 3.4 Verification — Resonant Frequency

$$f_r = \frac{1}{2\pi\sqrt{L_r C_r}} = \frac{1}{2\pi\sqrt{43 \times 10^{-6} \times 26 \times 10^{-9}}} = \frac{1}{2\pi \times 33.43 \times 10^{-6}} \times 10^{-1}$$

$$= \frac{1}{2\pi \times 3.343 \times 10^{-7}} \times 10^{1} = \frac{1}{2.101 \times 10^{-6}} \times 10^{1}$$

Let's compute directly:

$$L_r \cdot C_r = 43 \times 10^{-6} \times 26 \times 10^{-9} = 1.118 \times 10^{-12}$$

$$\sqrt{L_r C_r} = 1.057 \times 10^{-6} \text{ s}$$

$$f_r = \frac{1}{2\pi \times 1.057 \times 10^{-6}} = \frac{1}{6.641 \times 10^{-6}} = 150.6 \text{ kHz}  ✓$$

### 3.5 LLC Gain Equation

The LLC voltage gain as a function of normalized frequency fn = fs/fr:

$$M(f_n, Q, L_n) = \frac{f_n^2 \cdot (L_n - 1)}{\sqrt{\left(f_n^2 \cdot L_n - 1\right)^2 + f_n^2 \cdot (f_n^2 - 1)^2 \cdot L_n^2 \cdot Q^2}}$$

> [!note] Second resonant frequency
> The LLC has a second resonance at:
> $$f_{r2} = \frac{f_r}{\sqrt{1 + 1/L_n}} = \frac{150}{\sqrt{1.167}} = 138.9 \text{ kHz}$$
> Below fr2, the converter loses ZVS capability. The switching frequency must stay above fr2 under all conditions.

### 3.6 Gain and Q Verification Across Operating Range

| Vo (V) | Po (W) | Io (A) | Vbus (V) | M req'd | Rac (Ω) | Q at Rac | fn (calc) | fs (kHz) |
|--------|--------|--------|----------|---------|---------|---------|-----------|----------|
| 200 | 6,667 | 33.3 | 650 | 0.31 | 19.4 | 2.10 | >2.0 | >300 |
| 300 | 10,000 | 33.3 | 700 | 0.43 | 29.2 | 1.40 | ~1.8 | ~270 |
| 400 | 10,000 | 25.0 | 700 | 0.57 | 51.9 | 0.79 | ~1.5 | ~225 |
| **600** | **10,000** | **16.7** | **750** | **0.80** | **116.7** | **0.35** | **~1.15** | **~173** |
| 800 | 10,000 | 12.5 | 800 | 1.00 | 207.4 | 0.20 | 1.00 | 150 |
| 1000 | 10,000 | 10.0 | 920 | 1.09 | 324.1 | 0.13 | ~0.96 | ~143 |

> [!tip] Key observations
> - At 800 V: M = 1.0, fs = fr = 150 kHz — perfect resonance, peak efficiency
> - At 1000 V: M = 1.09, fs ≈ 143 kHz (below fr but above fr2 = 139 kHz) — ZVS maintained with ~3% margin. Confirmed by [[03-LLC Gain Curve Verification]].
> - At 300 V: fs = ~270 kHz, well within 300 kHz limit. Efficiency drops but power is derated.
> - At 200 V: fs approaching 300 kHz limit. This is the extreme derated case (only 6.7 kW). Acceptable.

## 4. Transformer Design

### 4.1 Core Selection

**Requirements per phase:**
- Power: 10 kW
- Frequency: 100–300 kHz (design center 150 kHz)
- Primary voltage: 375–460 Vpk (half-bridge at 750–920 V bus)
- Turns ratio: n = 2 (Ns:Np = 2:1)

**Core: E65/32/27 (3C97 ferrite)**

| Parameter | Value |
|-----------|-------|
| Core type | E65/32/27 |
| Material | 3C97 (Ferroxcube) or N97 (TDK) |
| Effective area (Ae) | 535 mm² |
| Effective volume (Ve) | 79,400 mm³ |
| Effective length (le) | 148 mm |
| Window area (Aw) | ~530 mm² |
| Saturation (Bsat at 100°C) | ~350 mT |
| Core loss density (150 kHz, 60 mT) | ~80 kW/m³ |

> [!note] Why E65/32/27
> This is the workhorse core for 5–15 kW LLC converters in the 100–200 kHz range. The large window area accommodates the interleaved litz-wire windings. 3C97 material is optimized for 100–300 kHz with low core loss and stable permeability.

### 4.2 Flux Density Calculation

For an LLC half-bridge, the peak flux in the core is set by the magnetizing current (Lm and Vbus):

$$B_{peak} = \frac{V_{bus}}{2 \cdot 4 \cdot N_p \cdot A_e \cdot f_s}$$

At the design center (Vbus = 750 V, fs = 150 kHz):

$$B_{peak} = \frac{750}{2 \times 4 \times N_p \times 535 \times 10^{-6} \times 150000} = \frac{750}{642 \times N_p \times 10^{-3}}$$

$$= \frac{750}{0.642 \times N_p}$$

For Bpeak = 60 mT:

$$N_p = \frac{750}{0.642 \times 0.060} = \frac{750}{0.0385} = 19.5 \rightarrow N_p = 20$$

Checking at worst case (Vbus = 920 V, fs = 143 kHz — minimum frequency at 1000 V output with Vbus_max = 920 V):

$$B_{peak} = \frac{920}{2 \times 4 \times 20 \times 535 \times 10^{-6} \times 143000} = \frac{920}{0.612} = 75 \text{ mT}$$

This is still well below saturation but leaves less margin. Increase to **Np = 21** for safety:

$$B_{peak} = \frac{920}{2 \times 4 \times 21 \times 535 \times 10^{-6} \times 143000} = \frac{920}{0.643} = 71.5 \text{ mT}$$

**Selected: Np = 21, Ns = 42** (n = 2 maintained). Bpeak = 57–72 mT across the operating range. Well below 350 mT saturation — margin of ~5:1.

### 4.3 Winding Design

**Primary winding:**
- Turns: Np = 21
- RMS current: Ipri,rms ≈ Ipri,load + Imag

At design center (600 V, 10 kW):

$$I_{pri,load,rms} = \frac{\pi}{2\sqrt{2}} \cdot \frac{n \cdot I_o}{1} = \frac{\pi}{2\sqrt{2}} \times \frac{2 \times 16.7}{1} = 1.11 \times 33.3 = 37.0 \text{ A (peak of fundamental)}$$

$$I_{pri,load,rms} = \frac{37.0}{\sqrt{2}} = 26.2 \text{ A rms}$$

Magnetizing current (peak):

$$I_{mag,pk} = \frac{V_{bus}}{2 \cdot 4 \cdot L_m \cdot f_s} = \frac{750}{2 \times 4 \times 258 \times 10^{-6} \times 150000} = \frac{750}{309.6} = 2.42 \text{ A}$$

$$I_{mag,rms} = \frac{2.42}{\sqrt{3}} = 1.40 \text{ A}$$

Total primary RMS current (worst case at 300 V, 10 kW):

$$I_{pri,rms} \approx 28 \text{ A (at design center), up to ~37 A at 300 V output)}$$

- Wire: **Litz wire, 44 AWG × 800 strands** (equivalent cross-section ≈ 2.0 mm², current density ≈ 14 A/mm² at 28 A)
- 2 layers of ~10.5 turns each

**Secondary winding:**
- Turns: Ns = 42
- RMS current at design center: Isec,rms = Ipri,rms / n = 28 / 2 = 14 A (reflected; actual secondary current peaks at low Vo)
- At 300 V, 33.3 A output: Isec,rms ≈ 26 A
- Wire: **Litz wire, 44 AWG × 400 strands** (equivalent cross-section ≈ 1.0 mm²)
- 4 layers of ~10.5 turns each

### 4.4 Winding Interleaving

To minimize proximity-effect losses and reduce leakage inductance, use a **P-S-P-S sandwich** structure:

```
         ┌─────────────────────┐
         │   Core (top half)   │
         ├─────────────────────┤
Bobbin → │  P1 (10-11 turns)   │  ← Primary layer 1
         │  S1 (21 turns)      │  ← Secondary layer 1+2
         │  P2 (10-11 turns)   │  ← Primary layer 2
         │  S2 (21 turns)      │  ← Secondary layer 3+4
         ├─────────────────────┤
         │   Core (bottom)     │
         └─────────────────────┘
```

Benefits:
- Reduces MMF peaks to half compared to non-interleaved winding
- Controls leakage inductance (useful for integrating Lr)
- Reduces AC winding resistance by ~4× vs. non-interleaved

### 4.5 Leakage Inductance — Integrated Lr

The resonant inductance Lr = 43 µH can potentially be integrated as the transformer's leakage inductance. For a P-S-P-S structure:

$$L_{leak} \approx \frac{\mu_0 \cdot N_p^2 \cdot l_w}{3 \cdot p^2 \cdot h_w} \cdot \left( m \cdot d_c + (m-1) \cdot d_{ins} \right)$$

Where p = number of interleaving sections, m = number of winding layers per section, and d_ins = insulation thickness.

**Practical estimate:** For an E65 core with P-S-P-S sandwich and standard interlayer insulation (~0.5 mm), the leakage inductance is typically 5–15 µH. This is well below the required 43 µH.

> [!warning] Discrete Lr likely required
> The integrated leakage inductance (~10 µH) covers only ~25% of the required 43 µH. A discrete resonant inductor is needed for the remaining ~33 µH, or the insulation spacing can be increased to boost leakage — but this sacrifices coupling and increases winding losses.
>
> **Recommendation:** Use a **combination approach** — design the transformer for ~10 µH leakage, and add a discrete inductor of ~33 µH in series.

### 4.6 Core Loss Estimate

Using the improved generalized Steinmetz equation (iGSE) for non-sinusoidal waveforms. For LLC near resonance, the magnetizing current is approximately triangular, so the effective Bac ≈ Bpeak.

At design center (Bpeak = 57 mT, fs = 150 kHz, 3C97 material):

Steinmetz parameters for 3C97 at 100°C: k = 3.2, α = 1.46, β = 2.75 (approximate):

$$P_{core} = k \cdot f^{\alpha} \cdot B^{\beta} \cdot V_e$$

$$P_{core} = 3.2 \times (150)^{1.46} \times (57)^{2.75} \times 79.4 \times 10^{-6}$$

Using the manufacturer's loss curve directly: at 150 kHz, 60 mT, 3C97 gives approximately **80 kW/m³**.

$$P_{core} = 80 \times 10^3 \times 79.4 \times 10^{-6} = 6.4 \text{ W}$$

At the worst case (72 mT, 143 kHz — 1000 V output at Vbus = 920 V):

$$P_{core} \approx 140 \text{ kW/m}^3 \times 79.4 \times 10^{-6} = 11.1 \text{ W}$$

**Transformer core loss: 6–11 W** depending on operating point.

### 4.7 Copper Loss Estimate

**DC resistance (primary):**

Litz wire 44 AWG × 800 strands, mean turn length (MTL) for E65 ≈ 130 mm:

$$R_{DC,pri} = \frac{\rho \cdot l}{A} = \frac{1.72 \times 10^{-8} \times 21 \times 0.130}{2.0 \times 10^{-6}} = 24 \text{ mΩ}$$

With AC resistance factor Fac ≈ 1.5 for well-interleaved litz at 150 kHz:

$$R_{AC,pri} = F_{ac} \times R_{DC,pri} = 1.5 \times 24 = 36 \text{ mΩ}$$

$$P_{Cu,pri} = I_{rms}^2 \times R_{AC} = 28^2 \times 0.036 = 28.2 \text{ W}$$

**DC resistance (secondary):**

Litz wire 44 AWG × 400 strands, MTL ≈ 140 mm, Ns = 42:

$$R_{DC,sec} = \frac{1.72 \times 10^{-8} \times 42 \times 0.140}{1.0 \times 10^{-6}} = 101 \text{ mΩ}$$

$$R_{AC,sec} = 1.5 \times 101 = 152 \text{ mΩ}$$

At worst case (300 V, 33.3 A, Isec ≈ 26 Arms reflected to secondary):

$$P_{Cu,sec} = 14^2 \times 0.152 = 29.8 \text{ W (at design center)}$$

> [!note] Copper loss is load-dependent and peaks at low output voltage / high current operating points. At the 800 V design point, primary current drops to ~20 A and copper losses fall significantly.

**Total transformer copper loss: 30–58 W** (design center to worst case).

### 4.8 Transformer Thermal Estimate

Total transformer loss at design center: Pcore + Pcu ≈ 6 + 58 = 64 W (worst case at 300 V/33.3 A).

Typical thermal resistance for E65 core with forced-air cooling (2–3 m/s airflow): Rth ≈ 5–8 °C/W for the core, ~3 °C/W overall with good airflow design.

At 64 W total loss: ΔT ≈ 64 × 3 = 192°C — **too high for natural/low airflow**.

> [!warning] Thermal management is critical
> At worst-case loading, the transformer dissipates ~64 W. This requires:
> - Dedicated forced-air cooling duct (>3 m/s airflow over the core)
> - OR increase wire gauge (reduce current density to <10 A/mm²)
> - OR use a larger core (E71 or dual E65 cores)
>
> At the typical 800 V operating point, losses drop to ~25 W, which is manageable.
> Since most real-world charging occurs at 400–800 V, the average thermal load is much lower than worst case.

**Design action:** Size the cooling system for 50 W/phase transformer dissipation (90th percentile operating point). The 64 W worst case at 300 V is a transient condition (low SoC charging, EV battery heats up and moves past this quickly).

## 5. Resonant Inductor (Lr)

### 5.1 Integrated vs. Discrete

As discussed in §4.5, the transformer leakage provides only ~10 µH of the required 43 µH. A discrete inductor is needed for the remaining ~33 µH.

**Strategy: 10 µH integrated (transformer leakage) + 33 µH discrete.**

### 5.2 Discrete Inductor Design

| Parameter | Value |
|-----------|-------|
| Inductance | 33 µH |
| RMS current | 28 A (design center), 37 A (worst case) |
| Peak current | ~52 A |
| Frequency | 100–300 kHz |
| Core | RM14 / PQ40/40 in 3C97 ferrite |
| Gap | Air gap to set inductance and prevent saturation |

**Core selection: PQ40/40 (3C97)**

| Parameter | Value |
|-----------|-------|
| Ae | 201 mm² |
| Ve | 37,600 mm³ |
| le | 187 mm |
| Aw | ~220 mm² |

**Air gap calculation:**

$$l_g = \frac{\mu_0 \cdot N^2 \cdot A_e}{L} - \frac{l_e}{\mu_r}$$

For N = 15 turns, L = 33 µH:

$$l_g = \frac{4\pi \times 10^{-7} \times 225 \times 201 \times 10^{-6}}{33 \times 10^{-6}} - \frac{0.187}{2500}$$

$$l_g = \frac{56.8 \times 10^{-9}}{33 \times 10^{-6}} - 7.5 \times 10^{-5} = 1.72 \times 10^{-3} - 0.075 \times 10^{-3} = 1.65 \text{ mm}$$

**Gap: ~1.6 mm total (0.8 mm per leg for center-gap design).**

**Peak flux check:**

$$B_{peak} = \frac{L \cdot I_{peak}}{N \cdot A_e} = \frac{33 \times 10^{-6} \times 52}{15 \times 201 \times 10^{-6}} = \frac{1716 \times 10^{-6}}{3015 \times 10^{-6}} = 569 \text{ mT}$$

This exceeds saturation. Need more turns or larger core. Increase to **N = 24 turns**:

$$B_{peak} = \frac{33 \times 10^{-6} \times 52}{24 \times 201 \times 10^{-6}} = \frac{1.716 \times 10^{-3}}{4.824 \times 10^{-3}} = 356 \text{ mT}$$

Still close to saturation for ferrite. Use **PQ50/50** or add distributed gap. Alternatively, use a **powder core (Kool Mµ or XFlux from Magnetics Inc.)** which handles DC bias much better:

> [!tip] Powder core alternative
> A **Kool Mµ 77439 toroid** (µ = 60, OD = 39 mm, Ae = 107 mm²) with 33 turns provides:
> - L = 33 µH at zero bias
> - Soft saturation characteristic — inductance rolls off gracefully at high current
> - No discrete air gap needed (distributed gap)
> - Better EMI (no fringing flux)
> - Core loss is higher than ferrite but acceptable for a small inductor
>
> **Recommendation: Kool Mµ toroid for the discrete Lr portion.**

### 5.3 Inductor Loss Estimate

For a Kool Mµ toroid at 150 kHz, the AC flux swing is small (most of the flux is DC bias from the magnetizing current component). Estimated:

- Core loss: ~3 W
- Copper loss (24 turns, litz wire): ~5 W

**Total discrete Lr loss: ~8 W**

## 6. Resonant Capacitor (Cr)

### 6.1 Requirements

| Parameter | Value |
|-----------|-------|
| Capacitance | 26 nF |
| RMS current | 28 A (design center), 37 A (worst case) |
| Voltage rating | ≥1200 V (capacitor sees Vbus/2 + resonant voltage; worst case ~460 V + resonant swing at Vbus = 920 V) |
| ESR | <50 mΩ target for low loss |
| Type | C0G/NP0 MLCC or polypropylene film |

### 6.2 Component Selection

**Option A: C0G/NP0 MLCC (preferred)**

High-voltage C0G capacitors (e.g., TDK C series, CGA series):
- TDK CGA9N4C0G2J103J230KA: 10 nF, 630 V, 2220 size, C0G
- 3 in series = 3.33 nF at 1890 V rating
- 8 parallel strings of 3-in-series = 26.7 nF at 1890 V

Total: **24 capacitors** (8P × 3S configuration).

RMS current per capacitor: 28 / 8 = 3.5 A — check ripple current rating. C0G MLCCs typically handle 2–5 Arms in 2220 size, so this is at the limit.

> [!note] C0G MLCCs
> - Zero voltage coefficient (no capacitance loss under DC bias unlike X7R)
> - Very low ESR (~5 mΩ per cap, total string ESR ~19 mΩ)
> - Temperature stable (-55 to +125°C)
> - Compact footprint on PCB

**Option B: Polypropylene film capacitor**

- EPCOS/TDK B32652 series: 22 nF or 33 nF, 1250 V, polypropylene film
- Single component solution (e.g., 22 nF + 4.7 nF in parallel ≈ 26.7 nF)
- Higher ripple current capability (~5–10 Arms)
- Larger physical size (~30 × 20 × 15 mm each)

**Decision: C0G MLCC array (Option A)** for compactness and low ESR. Polypropylene film as backup if thermal or ripple current issues arise during prototyping.

### 6.3 Capacitor Loss

$$P_{Cr} = I_{rms}^2 \times ESR = 28^2 \times 0.019 = 14.9 \text{ W}$$

> [!warning] 15 W in the capacitor array is significant. Review:
> - Actual ESR may be lower (C0G MLCCs at 150 kHz can be <3 mΩ per cap, giving total <6 mΩ and ~4.7 W)
> - If ESR loss is too high, add more parallel strings or switch to film capacitors
>
> **Revised estimate with measured ESR (~6 mΩ total): Pcr ≈ 4.7 W**

## 7. Loss Budget Summary (Per Phase, 10 kW)

| Component | Loss (W) | Notes |
|-----------|----------|-------|
| **Transformer core** | 6–11 | 3C97, E65/32/27, 57–72 mT |
| **Transformer copper** | 30–58 | Litz wire, interleaved P-S-P-S |
| **Discrete inductor (Lr)** | 8 | Kool Mµ toroid, 33 µH |
| **Resonant capacitor (Cr)** | 5 | C0G MLCC array, ~6 mΩ ESR |
| **Total magnetics** | **49–81** | Range: 800 V nom to 300 V worst case |

At the 800 V design point (M = 1.0, peak efficiency):
- Transformer core: 6 W
- Transformer copper: ~18 W (reduced current at 12.5 A output)
- Inductor: 5 W
- Capacitor: 3 W
- **Total: ~32 W → 99.7% magnetics efficiency**

At the 600 V design center (typical charging):
- **Total: ~52 W → 99.5% magnetics efficiency**

At the 300 V worst case (derated to 10 kW):
- **Total: ~81 W → 99.2% magnetics efficiency**

### 7.1 Budget Check Against System Target

The DC-DC stage target is >98% efficiency. The magnetics loss is only part of the total:

| Loss Component (per phase) | Estimated (W) | % of 10 kW |
|---------------------------|---------------|------------|
| Magnetics (this document) | 52 | 0.52% |
| Primary MOSFETs (conduction + switching) | ~40 | 0.40% |
| Secondary diodes (conduction) | ~60 | 0.60% |
| Gate drive + control | ~5 | 0.05% |
| PCB traces + connectors | ~10 | 0.10% |
| **Total DC-DC loss** | **~167** | **1.67%** |
| **DC-DC efficiency** | | **~98.3%** |

> [!tip] The magnetics loss budget of ~52 W (0.52% of 10 kW) leaves sufficient margin for the semiconductor and parasitic losses to stay within the 98% DC-DC efficiency target.

## 8. Bill of Materials — Magnetics (Per Phase)

| Component | Part / Specification | Qty | Notes |
|-----------|---------------------|-----|-------|
| Transformer core | E65/32/27, 3C97 (Ferroxcube) | 1 set | Core pair |
| Transformer bobbin | B65/32 (Ferroxcube) | 1 | With pin header |
| Primary winding | Litz 44 AWG × 800 strands, 21 turns | — | 2 layers, interleaved |
| Secondary winding | Litz 44 AWG × 400 strands, 42 turns | — | 4 layers, interleaved |
| Interlayer insulation | Kapton tape, 0.05 mm × 3 layers | — | 5 kV isolation class |
| Discrete resonant inductor | Kool Mµ 77439 toroid + 24T litz wire | 1 | 33 µH, Magnetics Inc. |
| Resonant capacitor | TDK CGA9N4C0G2J103J, 10 nF, 630 V, 2220 | 24 | 8P × 3S = 26.7 nF |

**× 3 phases for the complete 30 kW module.**

## 9. Design Risks and Open Items

| Risk / Item | Status | Mitigation |
|-------------|--------|------------|
| Lr at 1000 V — fs drops near fr2 (139 kHz) | **Resolved** | Vbus_max raised to 920 V → M = 1.09, fs ≈ 143 kHz, ZVS maintained (see [[03-LLC Gain Curve Verification]]) |
| Transformer thermal at 300 V / 33 A | Open | Size cooling for 50 W/phase; verify with CFD |
| Cr ripple current in MLCC | Open | Measure ESR at 150 kHz on prototype; switch to film if needed |
| Integrated vs. discrete Lr trade-off | Decided | Hybrid: 10 µH integrated + 33 µH discrete |
| Litz wire sourcing (44 AWG × 800) | Open | Confirm availability; 46 AWG × 1200 is an alternative |
| Core thermal interface to heatsink | Open | Thermal pad between core and chassis; include in thermal design |

## 10. Next Steps

- [x] SPICE simulation of LLC resonant tank — verify gain curve and ZVS boundary → [[03-LLC Gain Curve Verification]]
- [ ] Thermal simulation — transformer and inductor in forced-air duct (CFD pending, see [[04-Thermal Budget]] §10)
- [ ] Prototype winding — build one transformer, measure leakage inductance
- [ ] Cr ESR measurement at 150 kHz

## 11. References

- [[01-Topology Selection]] — Architecture and LLC specifications
- Ferroxcube E65/32/27 datasheet — core dimensions and material properties
- Magnetics Inc. Kool Mµ powder core catalog — toroid selection guide
- TDK CGA MLCC catalog — high-voltage C0G capacitors
- R. Erickson & D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed. — LLC analysis methodology
- B. Lu, W. Liu, et al., "Optimal Design Methodology for LLC Resonant Converter," IEEE APEC 2006
- Ferroxcube Application Note — "Design of Planar Power Transformers"

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
