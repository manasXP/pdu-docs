---
tags: [PDU, EMC, EMI, CE-marking, filter-design, conducted-emissions]
created: 2026-02-22
aliases: [EMC Limits, EMI Filter Research]
---

# EMC / EMI Limits and Filter Design — 30 kW EV Charger PDU

This note consolidates the regulatory emission limits, immunity test requirements, and EMI filter design data relevant to CE marking of the 30 kW DC fast charger power module. The module draws up to 60 A per phase at low mains (260 VAC) and uses a 3-level Vienna rectifier front end followed by an LLC DC-DC stage.

Related notes: [[01-Topology Selection]] | [[3-Phase PFC Topology Selection]] | [[SiC Device Thermal Parameters]]

---

## 1. EN 55032 (CISPR 32) Class B — Conducted Emission Limits

> [!note] Standard Applicability
> EN 55032 (which replaced EN 55022) applies to multimedia equipment and is the conducted emission standard cited in CE marking for power electronics and EV charging infrastructure in the EU. The limits below are for **mains terminals (AC power port)**.
>
> For equipment classified under industrial environments, EN 55011 (CISPR 11) Group 1 Class A may alternatively apply — its limits are 6 dB more relaxed than EN 55032 Class B. Always confirm the applicable product standard with a notified body; IEC 61851-21-2 references EN 55011 for off-board EVSE.

### 1.1 EN 55032 Class B Conducted Emission Limits (Mains Port)

| Frequency Range | Quasi-Peak Limit (dBµV) | Average Limit (dBµV) |
|---|---|---|
| 150 kHz – 500 kHz | 66 → 56 (decreases log-linearly) | 56 → 46 (decreases log-linearly) |
| 500 kHz – 5 MHz | 56 | 46 |
| 5 MHz – 30 MHz | 60 | 50 |

**Key breakpoints (exact values):**

| Frequency | QP Limit (dBµV) | AVG Limit (dBµV) |
|---|---|---|
| 150 kHz | 66 | 56 |
| 500 kHz | 56 | 46 |
| 5 MHz | 56 | 46 |
| 30 MHz | 60 | 50 |

> [!warning] Log-Linear Interpolation in 150–500 kHz Band
> Between 150 kHz and 500 kHz the limit is not flat — it decreases **linearly with the logarithm of frequency**. At any intermediate frequency f (in kHz):
> - QP limit = 66 − 10 × log₁₀(f / 150) / log₁₀(500 / 150) × 10 dBµV
> - This is the most critical band for a 48–65 kHz switcher, since 3× and 4× the switching frequency land here.

### 1.2 EN 55011 Group 1 Class A Limits (Alternative for Industrial EVSE)

| Frequency Range | Quasi-Peak Limit (dBµV) | Average Limit (dBµV) |
|---|---|---|
| 150 kHz – 500 kHz | 79 → 66 (log-linear) | 66 → 56 (log-linear) |
| 500 kHz – 30 MHz | 73 | 60 |

> [!tip] Filter Design Margin
> Design to **Class B** limits wherever feasible — this provides 6–13 dB headroom over Class A and ensures product can be repositioned for commercial environments without re-testing.

---

## 2. EN 61000-3-2 — Harmonic Current Limits (≤16 A/phase)

> [!note] Applicability
> EN 61000-3-2:2019 + A2:2024 applies to equipment with **input current ≤ 16 A per phase**. The 30 kW module at full load draws ~38–58 A/phase depending on mains voltage and is therefore **out of scope** for EN 61000-3-2. However, at partial load or when the module is operated at reduced output power below ~7 kW (single module), this standard may apply. More critically, it applies to the auxiliary power supply (SMPS for control electronics).

### 2.1 Class A Harmonic Current Limits

Class A covers: balanced 3-phase equipment, household appliances (except Class D), tools (except portable), audio equipment, all equipment not in other classes.

**Odd harmonics:**

| Harmonic Order (n) | Max. Allowable Current (A) |
|---|---|
| 3 | 2.30 |
| 5 | 1.14 |
| 7 | 0.77 |
| 9 | 0.40 |
| 11 | 0.33 |
| 13 | 0.21 |
| 15 ≤ n ≤ 39 (odd only) | 0.15 × (15/n) |

**Even harmonics:**

| Harmonic Order (n) | Max. Allowable Current (A) |
|---|---|
| 2 | 1.08 |
| 4 | 0.43 |
| 6 | 0.30 |
| 8 ≤ n ≤ 40 (even only) | 0.23 × (8/n) |

> [!tip] Vienna Rectifier Performance vs. EN 61000-3-2
> A properly controlled Vienna rectifier achieves THD < 5% with near-unity PF ≥ 0.99. The dominant harmonics are the 5th and 7th due to the 6-pulse nature. At 30 kW / 3 phases / 400 VAC: I_fund ≈ 43 A. Even at partial loads where Class A limits apply (≤16 A/phase, ~10.5 kW), the 5th harmonic target of 1.14 A represents only ~2.6% of the fundamental — achievable with active PFC control.

---

## 3. EN 61000-3-12 — Harmonic Limits for Equipment >16 A and ≤75 A/phase

> [!note] Primary Applicable Standard for This Module
> EN 61000-3-12:2011 + A1:2021 is the **primary harmonic standard** for this 30 kW module. At 400 VAC, 3-phase: rated current ≈ 43 A/phase at full load, and up to 60 A at low mains (260 VAC). This falls within the 16–75 A/phase scope.
>
> Limits in this standard are **conditional on the minimum short-circuit ratio Rsce** at the point of common coupling (PCC). The equipment manufacturer must declare the minimum Rsce at which the equipment meets limits, and the DNO must confirm the actual Rsce at the installation site.

### 3.1 Rsce — Short-Circuit Ratio Definition

Rsce = Ssc / Sequ

Where:
- Ssc = 3-phase short-circuit apparent power at the PCC (VA)
- Sequ = rated apparent power of the equipment (VA)

For a 30 kW module at 400 VAC: Sequ = 30,000 / 0.99 ≈ 30.3 kVA.
At a typical commercial supply point with Ssc = 1 MVA: Rsce = 1,000,000 / 30,300 ≈ 33.

### 3.2 Harmonic Current Limits for Balanced 3-Phase Equipment (EN 61000-3-12, Table 3)

Limits expressed as percentage of the reference current Iref (= rated input current at rated power).

| Min. Rsce | I₅ (%) | I₇ (%) | I₁₁ (%) | I₁₃ (%) | THC/Iref (%) | PWHC/Iref (%) |
|---|---|---|---|---|---|---|
| 33 | 10.7 | 7.2 | 3.1 | 2.0 | 13 | 22 |
| 66 | 14.0 | 9.0 | 5.0 | 3.0 | 16 | 25 |
| 120 | 19.0 | 12.0 | 7.0 | 4.0 | 22 | 28 |
| 250 | 31.0 | 20.0 | 12.0 | 7.0 | 37 | 38 |
| ≥350 | 40.0 | 25.0 | 15.0 | 10.0 | 48 | 46 |

**Notes:**
- I₃ and I₉ (odd triplen harmonics): No limits for **balanced** 3-phase equipment — these cancel in the line currents.
- Even harmonics up to order 12: shall not exceed 16/h % of Iref (e.g., I₂ ≤ 8%, I₄ ≤ 4%, I₆ ≤ 2.7%).
- Harmonics I₁₄ to I₄₀ not listed: ≤ 3% of Iref.
- THC = Total Harmonic Current (RMS of all harmonics, h ≥ 2).
- PWHC = Partial Weighted Harmonic Current (weighted sum emphasizing lower orders).
- Linear interpolation between Rsce values is permitted.

### 3.3 Absolute Values at Rsce = 33 for This Module

At Iref = 43 A (400 VAC, 30 kW, PF = 0.99):

| Harmonic | Limit (% Iref) | Max. Absolute Current (A) |
|---|---|---|
| I₅ | 10.7% | 4.6 A |
| I₇ | 7.2% | 3.1 A |
| I₁₁ | 3.1% | 1.3 A |
| I₁₃ | 2.0% | 0.86 A |
| THC | 13% | 5.6 A |
| PWHC | 22% | 9.5 A |

> [!tip] Vienna Rectifier Compliance Margin
> A Vienna rectifier with active digital control (FOC / predictive current control) achieves 5th harmonic < 2% and THD < 3% of fundamental. This gives ~5× margin over the Rsce = 33 limits. The standard does not require pre-verification by the manufacturer if equipment uses active PFC — instead, measurement at rated conditions during type test is required.

---

## 4. EN 61000-4 Series — Immunity Tests for EV Charging Equipment

> [!note] Governing Standard
> **IEC 61851-21-2:2018** (BS EN IEC 61851-21-2:2021) is the primary EMC standard for off-board EVSE (DC fast chargers). It references the EN 61000-4 basic standards for immunity test methods and defines the applicable test levels. Tests are performed in both **standby mode** and **charge mode at 20% ± 10% rated power**.

### 4.1 Immunity Test Summary

| Test | Standard | Port(s) | Test Level | Performance Criterion |
|---|---|---|---|---|
| Electrostatic Discharge (ESD) | EN 61000-4-2 | Enclosure | ±4 kV contact / ±8 kV air (Level 3) | B |
| Radiated RF Field | EN 61000-4-3 | Enclosure | 10 V/m, 80 MHz – 1 GHz (Level 3) | A |
| Electrical Fast Transients / Burst (EFT) | EN 61000-4-4 | AC power, DC output, signal | 2 kV / 5 kHz (Level 3, power port); 1 kV (signal port) | B |
| Surge | EN 61000-4-5 | AC power port | 2 kV line-to-earth, 1 kV line-to-line (Level 3) | B |
| Conducted RF Immunity | EN 61000-4-6 | AC power, DC output, signal | 10 Vrms, 150 kHz – 80 MHz (Level 3) | A |
| Power-Frequency Magnetic Field | EN 61000-4-8 | Enclosure | 100 A/m (for >32 A systems) | A |
| Voltage Dips & Interruptions | EN 61000-4-11 | AC power | 0%, 40%, 70% dip; 250 cycle interruption | B/C |

### 4.2 EN 61000-4-2 ESD Test Levels (All Four Levels)

| Level | Contact Discharge (kV) | Air Discharge (kV) | Peak Current (A) |
|---|---|---|---|
| 1 | ±2 | ±2 | 7.5 |
| 2 | ±4 | ±4 | 15 |
| 3 | ±6 | ±8 | 22.5 |
| 4 | ±8 | ±15 | 30 |

> [!warning] EV Charger Level Selection
> IEC 61851-21-2 typically specifies **Level 3** (±6 kV contact / ±8 kV air) for accessible surfaces of DC EVSE. Connector interfaces and cable-accessible ports should be tested at Level 3–4.

### 4.3 EN 61000-4-4 EFT/Burst Test Levels

| Level | Peak Voltage (kV) | Rise Time (ns) | Burst Duration (ms) | Repetition Rate (kHz) |
|---|---|---|---|---|
| 1 | 0.5 | 5 | 15 | 5 |
| 2 | 1.0 | 5 | 15 | 5 |
| 3 | 2.0 | 5 | 15 | 5 |
| 4 | 4.0 | 5 | 15 | 5 |

Power port: Level 3 (2 kV). Signal/control ports: Level 2 (1 kV).

### 4.4 EN 61000-4-5 Surge Test Levels

| Level | Peak Voltage (kV) | Short-Circuit Current (kA) |
|---|---|---|
| 1 | 0.5 | 0.25 |
| 2 | 1.0 | 0.5 |
| 3 | 2.0 | 1.0 |
| 4 | 4.0 | 2.0 |

- Line-to-earth coupling: 12 Ω impedance, 9 µF capacitor.
- Line-to-line coupling: 2 Ω impedance, 18 µF capacitor.
- For AC mains port: Level 3 = 2 kV L-E, 1 kV L-L.
- For DC output port: Level 2 typically (1 kV, 0.5 kA).

### 4.5 Performance Criterion Definitions

| Criterion | Definition |
|---|---|
| A | Equipment continues to operate normally during and after the test |
| B | Equipment may degrade during test but recovers automatically afterward |
| C | Equipment may require operator intervention to recover after test |

---

## 5. Vienna Rectifier DM Noise Spectrum Analysis (48–65 kHz Switching)

### 5.1 Differential-Mode Noise Generation Mechanism

In a 3-level Vienna rectifier, the switching action creates a pulse-width-modulated voltage on the AC lines with respect to the DC mid-point. The differential-mode noise is caused by the **switching ripple current** in the boost inductor and **voltage switching transitions** at the switching frequency and its harmonics.

**DM noise spectral structure:**

| Harmonic | Frequency at fsw = 48 kHz | Frequency at fsw = 65 kHz | Band Position |
|---|---|---|---|
| 1× fsw | 48 kHz | 65 kHz | Below 150 kHz conducted band |
| 2× fsw | 96 kHz | 130 kHz | Below 150 kHz conducted band |
| 3× fsw | **144 kHz** | 195 kHz | **Just below / at 150 kHz threshold** |
| 4× fsw | **192 kHz** | 260 kHz | **In the 150–500 kHz band** |
| 5× fsw | **240 kHz** | 325 kHz | **In the 150–500 kHz band** |
| 6× fsw | **288 kHz** | 390 kHz | **In the 150–500 kHz band** |
| 7× fsw | **336 kHz** | 455 kHz | **In the 150–500 kHz band** |
| 10× fsw | **480 kHz** | 650 kHz | **In the 150–500 kHz band** |
| 20× fsw | 960 kHz | 1.3 MHz | 500 kHz – 5 MHz band |
| 40× fsw | 1.92 MHz | 2.6 MHz | 500 kHz – 5 MHz band |
| 100× fsw | 4.8 MHz | 6.5 MHz | 5 MHz – 30 MHz band |

> [!warning] Critical Observation for 48 kHz Switching
> At fsw = 48 kHz, the **3rd harmonic (144 kHz)** falls just below the 150 kHz measurement start frequency, and the **4th harmonic (192 kHz)** is the **first significant noise peak inside the conducted emissions measurement band**. This peak coincides with the **steepest part of the Class B limit** (66→56 dBµV in 150–500 kHz), which makes it the worst-case point for filter design. The required DM attenuation at 192 kHz may be 30–40 dB depending on unfiltered noise level.
>
> At fsw = 65 kHz, the 3rd harmonic (195 kHz) is the first peak in the band — slightly more favorable as the limit is ~64.5 dBµV QP at 195 kHz.

### 5.2 DM Noise Spectral Shape Characteristics

- **Dominant region:** Low harmonics (3rd–10th × fsw) have the highest amplitude due to decreasing inductor current ripple with frequency.
- **Roll-off rate:** DM noise amplitude decreases at approximately **40 dB/decade** above the switching frequency (two-pole LC characteristic of the boost inductor + LISN capacitance). This is before the EMI filter is applied.
- **Sidebands:** PWM modulation creates sidebands around each switching harmonic at offsets of n × fline (50 Hz), spaced 50 Hz apart. These are generally below the QP detector threshold.
- **Intermodulation:** The 3-phase interleaving in a Vienna rectifier (120° phase shift between legs) causes partial cancellation of the 6th harmonic of switching frequency in the line current. Net DM ripple effectively has a dominant component at **3× fsw** (i.e., the 3-level topology reduces DM ripple vs. 2-level).

### 5.3 Approximate Unfiltered DM Noise Level (Engineering Estimate)

For a 30 kW, 3-phase Vienna rectifier at 400 VAC, 48 kHz:
- Switching voltage amplitude at switching node: ~700 V peak (DC bus).
- LISN impedance: 50 Ω.
- Approximate raw DM noise at first significant harmonic (4× fsw = 192 kHz): **~100–110 dBµV** (before filter).
- Required attenuation to meet Class B QP limit (~64 dBµV at 192 kHz): **~40–50 dB**.

---

## 6. Common-Mode Noise Sources in Vienna Rectifier + LLC System

### 6.1 Primary CM Noise Paths

| Noise Source | Mechanism | Dominant Frequency Range |
|---|---|---|
| MOSFET drain-to-heatsink capacitance | High dv/dt at switching transitions couples CM current through insulation pad to PE (heatsink connected to chassis/earth) | fsw to ~10 MHz |
| Transformer primary-to-secondary interwinding capacitance | Displacement current flows through Cp-sec during DC-DC switching transitions; returns via PE | DC-DC fsw (typ. 100–300 kHz) to ~30 MHz |
| PCB trace-to-chassis capacitance | High-voltage switching nodes capacitively couple to nearby chassis structures | fsw harmonics, 1–30 MHz |
| DC bus mid-point to earth | CM voltage on DC bus (±350 V) drives current through stray capacitances to chassis | fsw to ~5 MHz |

### 6.2 Typical Parasitic Capacitance Values

| Parasitic Element | Typical Range | Notes |
|---|---|---|
| SiC MOSFET drain-to-heatsink (C_ds-hs) | 50–200 pF per device | Depends on thermal interface material and pad area. ~100 pF typical with Kapton pad (0.125 mm) at 1200 V SiC TO-247; lower with ceramic pads. |
| Heatsink-to-chassis/PE (C_hs-pe) | 10–100 pF | Depends on mounting and isolation distance. Often intentionally bonded to DC mid-point to reduce CM noise by ~5 dB. |
| LLC transformer interwinding (C_ps) | 10–700 pF | Wire-wound: 10–50 pF typical; Planar transformer: 100–700 pF due to interleaved PCB layers. |
| Gate drive transformer interwinding | 6–15 pF | Isolated gate driver transformers (e.g., Würth WE-AGDT): 6.8–15 pF. |
| PCB trace-to-chassis (distributed) | 5–50 pF total | Estimated; layout dependent. |

### 6.3 CM Noise Current Estimation

The CM current through a parasitic capacitance Cp is:

I_cm = Cp × (dV/dt)

For a SiC MOSFET switching 700 V in 20 ns (dV/dt = 35 kV/µs):
- Through one device at 100 pF drain-to-heatsink: I_cm_peak = 100 × 10⁻¹² × 35 × 10⁹ = **3.5 A peak per device**.
- In a 3-phase Vienna rectifier with 6 active switches: CM current is vectorially summed; partial cancellation occurs due to symmetry.

> [!tip] CM Noise Reduction Techniques
> 1. **Bond heatsink to DC bus mid-point** — reduces CM current by ~5 dBµV at 2–4 MHz (Wolfspeed PRD-08907).
> 2. **Balanced transformer winding** — insert a faraday shield between primary and secondary, or use interleaved-then-balanced winding to cancel Cp × dV/dt.
> 3. **Reduce SiC switching speed** (increase gate resistance) — trade-off against switching losses; increasing Rg by 2× typically reduces dv/dt by ~30%, reducing I_cm by same factor.
> 4. **Split CM capacitor to mid-point** — Y capacitors to PE split between hot and neutral at the filter provides CM shunt.

### 6.4 LLC Converter CM Noise Specifics

In the LLC half-bridge topology:
- The switching node (drain of low-side FET = source of high-side FET) swings between 0 and V_bus at the DC-DC switching frequency (typically 100–300 kHz for a 30 kW LLC).
- The transformer primary-to-secondary capacitance (Cp-sec) creates a CM current path: switching node → Cp-sec → secondary → PE → earth → LISN → mains.
- **Mitigation:** A faraday (electrostatic) shield connected to PE between primary and secondary windings intercepts the displacement current before it reaches the secondary. This is standard practice in isolated DC-DC converters targeting Class B.

---

## 7. EMI Filter Design — Typical Component Values for 30 kW 3-Phase PFC

### 7.1 Filter Topology

A standard 3-phase PFC input EMI filter uses two cascaded stages:

```
Mains (L1, L2, L3, PE)
  │
 [Stage 1: CM Choke Lcm1 + Y-caps Cy1]
  │
 [Stage 2: DM Inductors Ldm + X-caps Cx]
  │
 [Vienna Rectifier Input]
```

For high power (>10 kW), a two-stage filter is typical:
- Stage 1 (line side): CM choke + Y capacitors — primarily attenuates CM noise.
- Stage 2 (load side): Smaller CM choke + X capacitors + DM inductors — attenuates remaining DM noise and provides additional CM attenuation.

### 7.2 Typical Component Values — 30 kW 3-Phase Vienna PFC Filter

These values are derived from the Microchip MSCSICPFC/REF5 30 kW reference design, Schaffner application notes (AN-RB Common-Mode Chokes), and published academic work on 30 kW PFC filter design optimization.

| Component | Value (Typical) | Function | Notes |
|---|---|---|---|
| CM Choke Lcm1 (stage 1) | 1–5 mH | Attenuates CM noise > ~5 kHz | Nanocrystalline core (e.g., Vacuumschmelze VITROPERM 500F); handles 60 A DC without saturation |
| CM Choke Lcm2 (stage 2) | 0.5–2 mH | CM attenuation at higher frequencies | Ferrite core (MnZn) for higher frequency performance |
| DM Inductor Ldm (each phase) | 50–200 µH | Attenuates DM switching ripple | Often the boost inductor itself provides DM filter function; dedicated DM filter inductors are additional |
| X Capacitors Cx (line-to-line) | 1–10 µF (per phase pair) | DM filtering; Y-rated capacitors | 305 VAC X2-rated; must not cause excessive reactive current |
| Y Capacitors Cy (line-to-PE) | 10–47 nF per line | CM filtering; shunts CM to PE | 250 VAC Y2-rated; total leakage current must be < 3.5 mA (IEC 60950) or 10 mA (industrial) |
| DM Filter Capacitor Cx2 | 2.2–4.7 µF | Second stage DM | X2 class, 305 VAC |

**Example: 4 kW Inverter Scaled to 30 kW (from Schaffner application data):**

| Parameter | 4 kW Example | 30 kW Estimate (scaled) |
|---|---|---|
| Lcm (CM choke) | 8.4 mH | 1.5–3 mH (lower L needed at higher current) |
| Ldm (DM inductor) | 62 µH | 30–60 µH per phase |
| Cx (DM cap) | 4.7 µF × 6 | 10–22 µF (higher power, more X-cap) |
| Cy (CM cap to PE) | 47 nF | 33–47 nF (leakage current constraint) |

> [!note] Core Material Selection
> - **Nanocrystalline** (VITROPERM, FINEMET): Best for CM chokes > 1 mH operating at 10 Hz–1 MHz; excellent permeability retention, minimal core saturation under DC bias. Suitable for Lcm1.
> - **MnZn Ferrite** (e.g., TDK PC95, Ferroxcube 3C90): Best for 100 kHz–2 MHz; lower permeability at lower frequencies but excellent high-frequency characteristics. Suitable for Lcm2.
> - **Powder Core** (e.g., Micrometals, Magnetics Inc.): Best for DM inductors with DC bias; stable permeability under high DC current.

### 7.3 Filter Design Methodology — Required Attenuation

| Frequency | Estimated Unfiltered DM Noise (dBµV) | EN 55032 Class B QP Limit (dBµV) | Required DM Attenuation (dB) |
|---|---|---|---|
| 192 kHz (4× 48 kHz) | ~105 | ~64.5 | ~40 |
| 240 kHz (5× 48 kHz) | ~100 | ~62 | ~38 |
| 480 kHz (10× 48 kHz) | ~90 | 56 | ~34 |
| 1 MHz | ~80 | 46 | ~34 |
| 5 MHz | ~60 | 46 | ~14 |
| 10 MHz | ~50 | 50 | ~0 (marginal) |

> [!tip] Filter Rolloff Target
> A two-stage LC filter with Ldm = 100 µH and Cx = 10 µF provides a corner frequency of fc = 1/(2π√(LC)) ≈ 5 kHz, with a theoretical **40 dB/decade rolloff** above fc. At 192 kHz (≈38× fc), attenuation ≈ 40 × log₁₀(38) ≈ **62 dB** — more than adequate. In practice, parasitics limit high-frequency attenuation, so a **second filter stage** is required to maintain 40+ dB attenuation above 5 MHz.

### 7.4 Y Capacitor Leakage Current Constraint

Maximum allowed PE leakage current (IEC 62368-1 / IEC 60950-1 for accessible equipment):
- Portable / household equipment: 3.5 mA
- Industrial fixed equipment: 10 mA
- Medical equipment: 0.5 mA

At 50 Hz, for Cy = 33 nF per line, 3-phase: I_leak = 3 × (2π × 50 × 33 × 10⁻⁹ × 230) ≈ **7.1 mA**.
At 47 nF per line: I_leak ≈ **10.2 mA** — at the industrial limit.

> [!warning] Leakage Current Budget
> For a stacked 5-module system (150 kW), the PE leakage from 5 × 3 × Cy = 15 capacitors becomes significant. Design Cy ≤ 22 nF per line if modules share a single PE/chassis connection and the system must meet ≤ 30 mA total (industrial).

### 7.5 Reference Designs and Application Notes

| Source | Document | Key Data |
|---|---|---|
| Microchip | MSCSICPFC/REF5 30 kW Vienna PFC Reference Design | Complete BOM with CM choke, DM filter, Y-caps; CISPR 22 Class B compliance shown |
| Schaffner | AN-RB Common-Mode Chokes (Parts 1 & 2) | CM/DM filter topology, component selection, Cy leakage calculation |
| Wolfspeed | PRD-08907: Mitigating EMI with SiC in Grid-Connected Converters | Heatsink bonding effect, SiC dv/dt and CM noise relationship |
| ETH Zurich | "EMI Filter Design for a 1 MHz, 10 kW Three-Phase/Level PWM Rectifier" (IEEE TPEL) | Filter design methodology for Vienna topology, measured compliance results |
| ETH Zurich | "Volume Optimization of a 30 kW Boost PFC Converter Focusing on CM/DM EMI Filter Design" | Optimal CM/DM split, nanocrystalline core selection, 30 kW validated design |
| TDK | EPCOS EMI Filter Design Guide | Component selection tables for 3-phase filters up to 100 A |
| Würth Elektronik | WE-TPBHV Series Datasheet | Nanocrystalline CM chokes 20–46 A, 0.52–208 mH, 1 kHz–20 MHz |

---

## 8. Summary — EMC Compliance Checklist for CE Marking

| Requirement | Standard | Key Metric | Status |
|---|---|---|---|
| Conducted emissions (AC port) | EN 55032 Class B (or EN 55011 Group 1 Class A) | ≤ 56 dBµV QP at 500 kHz | Requires 2-stage EMI filter |
| Harmonic currents | EN 61000-3-12 (>16 A, ≤75 A/phase) | THC ≤ 13% Iref at Rsce=33 | Active PFC achieves with margin |
| ESD immunity | EN 61000-4-2, Level 3 | ±6 kV contact, ±8 kV air | Enclosure design + TVS at ports |
| EFT/Burst immunity | EN 61000-4-4, Level 3 | 2 kV at power ports | Common-mode choke + shunt caps |
| Surge immunity | EN 61000-4-5, Level 3 | 2 kV L-E, 1 kV L-L | MOV + TVS at AC input |
| Conducted RF immunity | EN 61000-4-6, Level 3 | 10 Vrms, 150 kHz–80 MHz | Input EMI filter provides attenuation |
| Radiated RF immunity | EN 61000-4-3, Level 3 | 10 V/m, 80 MHz–1 GHz | Shielded enclosure + cable filtering |
| Power-frequency magnetic field | EN 61000-4-8 | 100 A/m (>32 A system) | Low susceptibility of digital control |
| Voltage dips / interruptions | EN 61000-4-11 | Per IEC 61851-21-2 tables | Bulk capacitance, hold-up time design |

---

## Sources

- [EN 55032 / CISPR 32 conducted limits overview — TI Technical Review of EMI Standards](https://www.ti.com/lit/pdf/sszt673)
- [EN 55032 Class B limit values — PowerCTC EMI Conducted Emission Limitations](https://www.powerctc.com/en/node/5883)
- [IEC 61000-3-2 harmonic limits — ResearchGate Table 2](https://www.researchgate.net/figure/EC-61000-3-2-current-harmonic-limits-Harmonics-n-Class-A-A-Class-B-A-Class-C_tbl2_260496494)
- [IEC 61000-3-2 Ed. 5.2b:2024 — IEC Webstore](https://webstore.iec.ch/en/publication/92799)
- [IEC 61000-3-12 Ed. 2.1b:2021 — ANSI Webstore](https://webstore.ansi.org/standards/iec/iec6100012ed2021)
- [IEC 61000-3-12 Table 3 data — absolute-emc.com tutorial](https://absolute-emc.com/article/tutorial-on-harmonics-flicker-and-related-immunity)
- [IEC 61000-3-12 accuracy evaluation with harmonic data — PMC / NCBI](https://pmc.ncbi.nlm.nih.gov/articles/PMC11175187/)
- [IEC 61851-21-2:2018 — EV Supply Equipment EMC Tests thesis (Kokkola, Theseus)](https://www.theseus.fi/bitstream/handle/10024/866122/Kokkola_Lassi.pdf?sequence=2&isAllowed=y)
- [IEC 61851-21-2 overview — Testups.com](https://www.testups.com/iec-en-61851-21-2-emc-electric-vehicle-charging-systems/)
- [EN 61000-4-2 ESD test levels — AMETEK CTS](https://www.ametek-cts.com/know-how/iec-transient-pulse-immunity/iec61000-4-2-esd)
- [EN 61000-4-4 EFT test levels — Transient Specialists](https://transientspecialists.com/blogs/blog/electrical-fast-transient-burst-iec-61000-4-4)
- [EN 61000-4-5 surge test levels — EMC FastPass overview](https://www.emcfastpass.com/wp-content/uploads/2017/04/surge_overview.pdf)
- [Vienna rectifier EMI study — ResearchGate (conducted EMI reduction)](https://www.researchgate.net/publication/224165218_Study_of_conducted_EMI_reduction_for_three-phase_Vienna-type_rectifier)
- [Vienna rectifier CM modeling — ResearchGate simplified approach](https://www.researchgate.net/publication/342454805_A_simplified_approach_to_CM_modeling_of_a_Vienna_rectifier_for_electromagnetic_compliance)
- [Microchip 30 kW Vienna PFC Reference Design MSCSICPFC/REF5](https://ww1.microchip.com/downloads/en/DeviceDoc/MSCSICPFC-REF5-3-Phase-30-kW-Vienna-PFC-Reference-Design-DS50002952A.pdf)
- [Wolfspeed PRD-08907: Mitigating EMI with SiC in Grid-Connected Converters](https://assets.wolfspeed.com/uploads/2024/12/Wolfspeed_PRD-08907_Mitigating_EMI_with_SiC_Solutions_in_Renewable_Energy_and_Grid-Connected_Power_Converters.pdf)
- [Schaffner AN: EMC/EMI Filter Design with RB Common-Mode Chokes](https://www.simpex.ch/wp-content/uploads/2022/02/Schaffner_AN_RB_common_chockes.pdf)
- [ETH Zurich: EMI Filter Design for 10 kW Three-Phase/Level PWM Rectifier](https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/06_EMI_Filter_Design.pdf)
- [SiC heatsink parasitic capacitance and EMI — Wolfspeed application note](https://assets.wolfspeed.com/uploads/2024/12/Wolfspeed_PRD-08907_Mitigating_EMI_with_SiC_Solutions_in_Renewable_Energy_and_Grid-Connected_Power_Converters.pdf)
- [Transformer interwinding parasitic capacitance models — Shuo Wang et al.](https://peeprlgator.github.io/Shuo.Wang/publicationattachments/Two-Capacitor%20Transformer%20Winding%20Capacitance%20Models%20for%20Common-Mode%20EMI%20Noise%20Analysis%20in%20Isolated%20DC%E2%80%93DC%20Converters.pdf)
