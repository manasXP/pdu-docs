---
tags: [PDU, EMI, EMC, filter, Vienna, conducted-emissions, EN-55032]
created: 2026-02-22
status: draft
---

# EMI Filter Design — 30 kW PDU Input Stage

> [!summary] Key Results
> Two-stage LC filter: CM choke 1 (3.3 mH nanocrystalline) + CM choke 2 (1.0 mH MnZn ferrite) + DM capacitors (2.2 µF X2 per phase) + Y-caps (22 nF Y2 per line). Total filter attenuation >55 dB at 150 kHz. Estimated filter volume ~0.8 L, mass ~2.5 kg. Meets EN 55032 Class B with ≥6 dB design margin.

## 1. EMC Requirements

### 1.1 Applicable Standards

| Standard | Scope | Applies to |
|----------|-------|-----------|
| **EN 55032 (CISPR 32) Class B** | Conducted emissions, 150 kHz – 30 MHz | Primary EMC target for CE marking |
| **EN 61000-3-12** | Harmonic currents (16–75 A/phase) | Input current distortion |
| **EN 61000-4-2/3/4/5/6/8/11** | Immunity (ESD, surge, EFT, RF, dips) | Via IEC 61851-21-2 for EVSE |
| IEC 61851-21-2 | EMC for EV charging equipment | Master standard referencing EN 61000 series |

### 1.2 EN 55032 Class B Conducted Emission Limits

| Frequency Range | Quasi-Peak Limit (dBµV) | Average Limit (dBµV) |
|----------------|------------------------|---------------------|
| 150 kHz – 500 kHz | 66 → 56 (log-linear) | 56 → 46 (log-linear) |
| 500 kHz – 5 MHz | 56 | 46 |
| 5 MHz – 30 MHz | 60 | 50 |

> [!note] The 150–500 kHz range is the most critical band for this design. The Vienna rectifier's first in-band switching harmonics (3rd–4th of fsw) land squarely here, where the limit slopes from 66 dBµV down to 56 dBµV.

### 1.3 EN 61000-3-12 Harmonic Current Limits

For 3-phase balanced equipment at Rsce = 33 (typical public grid):

| Harmonic | Limit (% of Iref) | Absolute at 43 A ref (A) |
|----------|-------------------|--------------------------|
| 5th | 10.7% | 4.6 |
| 7th | 7.2% | 3.1 |
| 11th | 3.1% | 1.3 |
| 13th | 2.0% | 0.9 |
| THC | 13% | 5.6 |

The Vienna PFC with dq-frame current control achieves THDi < 3% at full load (per [[01-Topology Selection]] §7). Harmonic compliance is met by the active PFC — no passive harmonic filter needed.

### 1.4 Immunity Test Levels (IEC 61851-21-2)

| Test | Standard | Level | Specification |
|------|----------|-------|--------------|
| ESD | EN 61000-4-2 | 3 | ±6 kV contact, ±8 kV air |
| Radiated RF | EN 61000-4-3 | 3 | 10 V/m, 80 MHz – 1 GHz |
| EFT/Burst | EN 61000-4-4 | 3 / 2 | 2 kV (power) / 1 kV (signal) |
| Surge | EN 61000-4-5 | 3 | 2 kV L-E, 1 kV L-L |
| Conducted RF | EN 61000-4-6 | 3 | 10 Vrms, 150 kHz – 80 MHz |
| Voltage dips | EN 61000-4-11 | Per table | 0%, 40%, 70% dip; 250-cycle interruption |

The input EMI filter also provides surge attenuation. A dedicated metal-oxide varistor (MOV) stage handles the 2 kV surge per EN 61000-4-5.

## 2. Noise Source Analysis

### 2.1 Vienna Rectifier Switching Noise

From [[01-Topology Selection]] §3.3:
- Switching frequency: 48–65 kHz per switch cell
- 3-level topology → effective ripple frequency 96–130 kHz
- SiC MOSFETs (SCTWA90N65G2V-4): dV/dt ≈ 20–35 kV/µs

**Differential-mode (DM) noise spectrum:**

The Vienna rectifier produces a 3-level PWM voltage at each phase. The first switching harmonics:

| Harmonic | At fsw = 48 kHz (kHz) | At fsw = 65 kHz (kHz) | In EN 55032 band? |
|----------|----------------------|----------------------|-------------------|
| 1st | 48 | 65 | No |
| 2nd | 96 | 130 | No |
| **3rd** | **144** | **195** | Marginal / **Yes** |
| **4th** | **192** | **260** | **Yes** |
| 5th | 240 | 325 | Yes |

The 3-level switching reduces DM noise compared to 2-level by ~6 dB (halved voltage step). Unfiltered DM noise at the first in-band harmonic (~150–200 kHz) is estimated at **100–110 dBµV**.

Required DM attenuation at 150 kHz:

$$A_{DM,req} = 110 - 66 + 6 = 50 \text{ dB (with 6 dB margin)}$$

### 2.2 Common-Mode (CM) Noise Sources

| CM Parasitic | Typical Value | Impact |
|-------------|--------------|--------|
| SiC MOSFET drain-to-heatsink (Cdh) | 50–100 pF per device | Dominant below 5 MHz |
| LLC transformer interwinding (Cw) | 10–50 pF (litz wire) | Significant 1–10 MHz |
| Heatsink-to-PE chassis (Chp) | 10–100 pF | Path to LISN measurement |
| Gate driver isolation (Cio) | 2–5 pF (STGAP2SiC) | Negligible |

At dV/dt = 35 kV/µs and Cdh = 100 pF per device (6 PFC MOSFETs):

$$I_{CM,peak} = C_{total} \times \frac{dV}{dt} = 600 \times 10^{-12} \times 35 \times 10^{9} = 21 \text{ A peak (impulse)}$$

This CM current impulse is very short-lived but produces broadband noise extending to 30+ MHz. Estimated unfiltered CM noise: **90–100 dBµV** in the 150 kHz – 5 MHz range.

Required CM attenuation at 150 kHz:

$$A_{CM,req} = 100 - 66 + 6 = 40 \text{ dB (with 6 dB margin)}$$

### 2.3 LLC Stage Noise

The LLC DC-DC stage operates at 100–300 kHz with ZVS, which significantly reduces high-frequency emissions. However:
- Transformer CM currents (interwinding capacitance) couple to the output
- Output rectifier diode ringing creates broadband noise at the DC output
- These are attenuated by the DC bus capacitor bank between PFC and LLC stages

The **input** EMI filter addresses AC-side conducted emissions. LLC noise reaches the AC input through the DC bus → PFC → input path, attenuated by at least 40 dB by the PFC control loop and bus capacitors.

## 3. Filter Topology

### 3.1 Two-Stage CM/DM Filter

```
AC Input    ┌────────┐    ┌──────┐    ┌────────┐    ┌──────┐    To PFC
  L1 ───────┤        ├────┤ Cx1  ├────┤        ├────┤ Cx2  ├──── L1'
  L2 ───────┤ CM     ├────┤ (DM) ├────┤ CM     ├────┤ (DM) ├──── L2'
  L3 ───────┤ Choke 1├────┤      ├────┤ Choke 2├────┤      ├──── L3'
  PE ───┬───┤        ├──┬─┤      ├──┬─┤        ├──┬─┤      ├──── PE
        │   └────────┘  │ └──────┘  │ └────────┘  │ └──────┘
        │               │           │              │
       MOV             Cy1         Cy2            Cy3
       (surge)       (Y-caps)    (Y-caps)       (Y-caps)
```

**Stage 1 (grid-facing):** Large CM choke (Lcm1) + X-capacitors (Cx1) + Y-capacitors (Cy1)
- Primary attenuation at 150–500 kHz
- Handles bulk energy of conducted noise
- Nanocrystalline core for high impedance at low frequency

**Stage 2 (PFC-facing):** Smaller CM choke (Lcm2) + X-capacitors (Cx2) + Y-capacitors (Cy2/Cy3)
- High-frequency attenuation (1–30 MHz)
- MnZn ferrite core for stable impedance at high frequency
- Cleans up residual noise and CM ringing

### 3.2 DM Filtering

The DM filter relies on:
1. **Leakage inductance of CM chokes** — typically 0.5–2% of Lcm → provides ~15–50 µH of DM inductance per stage
2. **X-capacitors** between phases
3. **PFC boost inductors** (external to the EMI filter) provide additional DM attenuation — typically 100–300 µH per phase, giving >40 dB DM rejection at 150 kHz

> [!tip] The Vienna PFC boost inductors are part of the DM filter
> Each boost inductor (~150 µH per phase) combined with the DC bus capacitors forms a low-pass filter with a corner frequency well below 150 kHz. This provides ≥40 dB of DM attenuation at the first in-band harmonic — so the dedicated DM filter only needs to contribute an additional ~10–15 dB.

## 4. Component Selection

### 4.1 CM Choke 1 — Nanocrystalline (Grid-Side)

| Parameter | Value |
|-----------|-------|
| Inductance (CM) | 3.3 mH |
| Core material | Nanocrystalline (VITROPERM 500F, Vacuumschmelze) |
| Core size | W914 toroid (OD ≈ 80 mm) or equivalent |
| Winding | 3-phase, 15–20 turns per winding |
| Rated current | 60 A |
| Leakage inductance (DM) | ~30–50 µH (1–1.5% of Lcm) |
| Impedance at 150 kHz | >2 kΩ |
| Impedance at 1 MHz | >5 kΩ |
| Saturation current | >80 A (peak, including inrush) |
| Temperature rating | 130°C |

> [!note] Why nanocrystalline
> Nanocrystalline cores (µr ~ 30,000–80,000) provide 3–5× higher CM inductance per unit volume compared to MnZn ferrite. They maintain high impedance from 10 kHz to 1 MHz — ideal for the first-stage CM choke where the 150–500 kHz band needs maximum attenuation. The Vacuumschmelze VITROPERM W914 or Magnetec M-403 are common choices for 30 kW PFC filters.

**Candidate parts:**
- Vacuumschmelze T60006-L2080-W914 (VITROPERM 500F, 80 mm OD)
- Magnetec M-403-A (nanocrystalline, 3-phase, 60 A rated)
- Schaffner RD3132-80 (complete 3-phase CM choke module)

### 4.2 CM Choke 2 — MnZn Ferrite (PFC-Side)

| Parameter | Value |
|-----------|-------|
| Inductance (CM) | 1.0 mH |
| Core material | MnZn ferrite (TDK PC95 or Ferroxcube 3E6) |
| Core size | 2× stacked R42 toroids (OD ≈ 42 mm) |
| Winding | 3-phase, 8–10 turns per winding |
| Rated current | 60 A |
| Leakage inductance (DM) | ~10–20 µH |
| Impedance at 1 MHz | >3 kΩ |
| Impedance at 10 MHz | >1 kΩ |

MnZn ferrite excels at high frequency (1–30 MHz) where nanocrystalline cores lose effectiveness due to winding capacitance.

### 4.3 X-Capacitors (DM)

| Parameter | Stage 1 (Cx1) | Stage 2 (Cx2) |
|-----------|---------------|---------------|
| Capacitance | 2.2 µF per phase pair | 1.0 µF per phase pair |
| Voltage | 310 VAC (X2 rated) | 310 VAC (X2 rated) |
| Quantity | 3 (L1-L2, L2-L3, L3-L1) | 3 |
| Type | Metallized polypropylene film | Metallized polypropylene film |
| Self-discharge | <1 s to 34 V (per EN 60384-14) | <1 s |

**Candidate:** EPCOS/TDK B32924 series (2.2 µF, 310 VAC, X2, 27.5 mm pitch).

Total X-capacitance per phase pair: 3.2 µF. This provides DM filtering corner frequency with the CM choke leakage:

$$f_{DM} = \frac{1}{2\pi\sqrt{L_{leak} \times C_x}} = \frac{1}{2\pi\sqrt{40 \times 10^{-6} \times 3.2 \times 10^{-6}}} = 14 \text{ kHz}$$

At 150 kHz (10× the corner), DM attenuation is ~40 dB per stage.

### 4.4 Y-Capacitors (CM)

| Parameter | Value |
|-----------|-------|
| Capacitance | 22 nF per line (L-to-PE) |
| Voltage | 250 VAC (Y2 rated) |
| Quantity | 6 total (2 per line, distributed at Cy1 and Cy2 positions) |
| Type | Ceramic disc, Y2 safety rated |
| Leakage current | <3.5 mA total (per IEC 61140, <10 mA for fixed equipment) |

**Leakage current check:**

$$I_{leak} = 2\pi f \times C_{total} \times V_{line} = 2\pi \times 50 \times (6 \times 22 \times 10^{-9}) \times 400 = 16.6 \text{ mA}$$

> [!warning] Leakage current exceeds 10 mA limit
> At 6 × 22 nF = 132 nF total Y-capacitance and 400 VAC line voltage, the 50 Hz leakage is ~17 mA. This exceeds the IEC 61140 / EN 55032 protective-earth current limit of 10 mA for Class I equipment.
>
> **Mitigation options:**
> - Reduce to 10 nF per line → 6 × 10 nF = 60 nF → I_leak = 7.5 mA ✓
> - Or use a split Y-cap arrangement (Y-caps to DC bus midpoint instead of PE) which does not contribute to PE leakage
>
> **Decision: 10 nF Y2 per line, 6 total** → 7.5 mA leakage, meets <10 mA limit.

### 4.5 Surge Protection (MOV)

| Parameter | Value |
|-----------|-------|
| Type | Metal-oxide varistor (MOV) |
| Placement | Input side (before CM choke 1) |
| Configuration | 3 × L-PE + 3 × L-L (delta + star) |
| L-PE varistor | 680 VAC (e.g., EPCOS B72220S0681K101) |
| L-L varistor | 680 VAC |
| Surge rating | 2 kV / 1.2/50 µs (per EN 61000-4-5 Level 3) |
| Clamping voltage | <1.8 kV at 500 A |

## 5. Filter Attenuation Verification

### 5.1 CM Attenuation

Each CM stage provides attenuation based on the LC resonance:

**Stage 1:** Lcm1 = 3.3 mH, Cy1 = 30 nF (3 × 10 nF)

$$f_{CM1} = \frac{1}{2\pi\sqrt{3.3 \times 10^{-3} \times 30 \times 10^{-9}}} = 16 \text{ kHz}$$

At 150 kHz (~10× corner): attenuation = -40 dB (2nd order LC).

**Stage 2:** Lcm2 = 1.0 mH, Cy2 = 30 nF

$$f_{CM2} = \frac{1}{2\pi\sqrt{1.0 \times 10^{-3} \times 30 \times 10^{-9}}} = 29 \text{ kHz}$$

At 150 kHz (~5× corner): attenuation = -28 dB.

**Total CM attenuation at 150 kHz: ~68 dB** (both stages cascaded, with ~10 dB deduction for non-ideal coupling → **~58 dB effective**).

Required: 40 dB. **Margin: ~18 dB. ✓**

### 5.2 DM Attenuation

**EMI filter DM path:** Lleakage (40 µH per stage) + X-caps (3.2 µF per stage) + PFC boost inductor (~150 µH).

DM attenuation from EMI filter alone at 150 kHz:

Stage 1: -40 dB (fcorner = 14 kHz, ×10)
Stage 2: -34 dB (fcorner = 20 kHz, ×7.5)

Subtotal from EMI filter: -74 dB (theoretical), derate to **~55 dB effective** for parasitic coupling.

PFC boost inductor adds another **~20 dB** at 150 kHz.

**Total DM attenuation at 150 kHz: ~75 dB effective.**

Required: 50 dB. **Margin: ~25 dB. ✓**

### 5.3 Attenuation Summary

| Frequency | CM Noise (dBµV) | CM Atten. (dB) | CM at LISN | DM Noise (dBµV) | DM Atten. (dB) | DM at LISN | Limit QP (dBµV) | Margin (dB) |
|-----------|----------------|---------------|-----------|----------------|---------------|-----------|----------------|------------|
| 150 kHz | 100 | 58 | 42 | 110 | 75 | 35 | 66 | >24 |
| 500 kHz | 85 | 72 | 13 | 90 | 90 | 0 | 56 | >43 |
| 1 MHz | 80 | 80 | 0 | 75 | 95 | 0 | 56 | >56 |
| 5 MHz | 70 | 60 | 10 | 55 | 95 | 0 | 56 | >46 |
| 10 MHz | 60 | 45 | 15 | 40 | 95 | 0 | 60 | >45 |

> [!success] All operating points meet EN 55032 Class B with ≥6 dB margin. The 150 kHz point is the tightest, with ~24 dB margin. This provides a comfortable buffer for PCB layout parasitics, component tolerances, and production spread.

## 6. Physical Implementation

### 6.1 Filter Layout

```
AC input     [MOV]  [CM1]   [Cx1]  [Cy1]  [CM2]   [Cx2]  [Cy2]   To PFC
connector    stage   3.3mH   2.2µF  10nF   1.0mH   1.0µF  10nF    stage
   ↓          ↓       ↓       ↓      ↓       ↓       ↓      ↓
 ┌──┐      ┌──┐   ┌──────┐ ┌──┐  ┌──┐   ┌──────┐ ┌──┐  ┌──┐
 │  │      │  │   │      │ │  │  │  │   │      │ │  │  │  │
 └──┘      └──┘   └──────┘ └──┘  └──┘   └──────┘ └──┘  └──┘
  30mm      25mm    80mm     30mm  15mm    45mm     25mm  15mm
                     ↑                      ↑
              Nanocrystalline         MnZn ferrite
               toroid core           stacked toroids
```

### 6.2 Volume and Weight Estimate

| Component | Volume (cm³) | Weight (g) | Qty |
|-----------|-------------|-----------|-----|
| CM choke 1 (3.3 mH nanocrystalline) | 250 | 800 | 1 |
| CM choke 2 (1.0 mH MnZn) | 80 | 250 | 1 |
| X-capacitors (all) | 120 | 200 | 6 |
| Y-capacitors (all) | 15 | 30 | 6 |
| MOV array | 40 | 100 | 6 |
| PCB + mounting | 100 | 200 | 1 |
| Wiring / bus bars | 50 | 150 | — |
| **Total EMI filter** | **~655** | **~1730** | |

**Volume: ~0.66 L** (~5% of 12.8 L enclosure volume)
**Weight: ~1.7 kg** (~10% of 17 kg target)

> [!tip] The 3-level Vienna topology pays off here — a 2-level PFC would require ~40% larger DM filter components, adding ~0.3 L and ~0.7 kg.

### 6.3 Thermal Considerations

From [[04-Thermal Budget]]:
- EMI filter estimated loss: 15 W (CM choke core loss + capacitor ESR)
- Filter is located near the AC input, upstream of the PFC heatsink
- Receives fresh ambient air from fans → component temperatures stay below 80°C
- Nanocrystalline cores are rated to 130°C — ample margin

## 7. Inrush Current Limiting

The EMI filter X-capacitors (total ~9.6 µF across 3 phase pairs) and DC bus capacitors create a large inrush current at power-on.

### 7.1 Pre-Charge Circuit

| Parameter | Value |
|-----------|-------|
| Method | NTC + bypass relay |
| NTC resistance (cold) | 10 Ω per phase |
| NTC steady-state resistance | <0.1 Ω (self-heated) |
| Bypass relay | 60 A rated, engages after soft-start complete |
| Soft-start time | ~3 s (NTC phase) + ~3 s (PFC ramp) = ≤6 s total |

Alternative: active pre-charge using the PFC MOSFETs in linear mode during startup. This eliminates the NTC but requires firmware support — available in the STSW-30KWVRECT reference firmware.

> [!info] For detailed inrush current calculations, NTC sizing, bypass relay selection, output contactor specification, and complete startup/shutdown timing, see [[08-Power-On Sequence and Inrush Management]].

## 8. Design for Immunity

### 8.1 Surge (EN 61000-4-5)

- 2 kV L-E, 1 kV L-L handled by the MOV array (§4.5)
- CM choke 1 provides additional surge impedance
- DC bus capacitors absorb residual energy

### 8.2 EFT/Burst (EN 61000-4-4)

- 2 kV on power lines
- The CM chokes and X-capacitors attenuate EFT pulses (5 ns rise, 50 ns duration)
- Y-capacitors divert CM EFT energy to PE

### 8.3 Conducted RF Immunity (EN 61000-4-6)

- 10 Vrms, 150 kHz – 80 MHz
- The two-stage EMI filter provides >40 dB rejection across this band
- Additional decoupling at the MCU and CAN interface

### 8.4 ESD (EN 61000-4-2)

- Not an EMI filter issue — handled by enclosure design (metal chassis, grounded connectors)
- TVS diodes on signal interfaces (CAN, UART)

## 9. Bill of Materials — EMI Filter

| Component | Part / Specification | Qty | Notes |
|-----------|---------------------|-----|-------|
| CM Choke 1 | VITROPERM W914, 3.3 mH, 60 A, 3-phase | 1 | Nanocrystalline toroid |
| CM Choke 2 | MnZn ferrite R42 stacked, 1.0 mH, 60 A | 1 | TDK PC95 or 3E6 |
| X-capacitor (Cx1) | 2.2 µF, 310 VAC, X2 (EPCOS B32924) | 3 | L-L, delta config |
| X-capacitor (Cx2) | 1.0 µF, 310 VAC, X2 | 3 | L-L, delta config |
| Y-capacitor (Cy) | 10 nF, 250 VAC, Y2 ceramic disc | 6 | L-PE, distributed |
| MOV (L-PE) | 680 VAC, 20 kA surge (EPCOS B72220S0681K101) | 3 | Star to PE |
| MOV (L-L) | 680 VAC, 20 kA surge | 3 | Delta between phases |
| NTC thermistor | 10 Ω cold, 60 A bypass relay | 3 | Inrush limiting |
| Bypass relay | 60 A, 600 VAC, normally open | 1 | Engages after soft-start |
| Discharge resistors | 1 MΩ across each X-cap | 6 | IEC 60384-14 compliance |

## 10. Design Risks and Open Items

| Risk / Item | Severity | Status | Mitigation |
|-------------|----------|--------|------------|
| CM choke saturation during surge | Medium | Open | Verify surge current vs. nanocrystalline core saturation; add gap if needed |
| Y-cap leakage current margin (7.5 mA vs. 10 mA limit) | Low | Acceptable | 25% margin; use split-Y to midpoint if needed |
| PCB layout coupling between filter stages | Medium | Open | Maintain ≥20 mm separation between stage 1 and stage 2; shield partition |
| CM choke resonance with Y-caps | Low | Open | Verify no resonance peak in 150 kHz – 30 MHz band; add damping resistor if needed |
| NTC cold start at −30°C ambient | Low | Open | NTC resistance higher when cold — verify inrush stays within breaker trip curve |
| Filter insertion loss vs. frequency — prototype measurement | Medium | Planned | Measure with network analyzer before compliance testing |

## 11. Next Steps

- [ ] Procure CM choke samples (nanocrystalline + MnZn) and measure impedance vs. frequency
- [ ] Network analyzer measurement of filter insertion loss (CM and DM)
- [ ] Pre-compliance conducted emissions scan on prototype
- [ ] Verify surge withstand with MOV array (EN 61000-4-5 Level 3)
- [ ] EFT and conducted RF immunity testing per IEC 61851-21-2
- [ ] Finalize NTC + relay sizing for −30°C cold start

## 12. References

- [[01-Topology Selection]] — Vienna PFC switching frequency, semiconductor BOM
- [[04-Thermal Budget]] — EMI filter loss allocation (15 W)
- [[EMC-EMI Limits and Filter Design]] — Detailed limits tables and design references
- EN 55032:2015+A11:2020 — Conducted emission limits for multimedia equipment
- IEC 61851-21-2 — EMC requirements for EV charging equipment
- EN 61000-3-12 — Harmonic current limits for >16 A equipment
- Vacuumschmelze VITROPERM 500F — Nanocrystalline core datasheet and selection guide
- EPCOS/TDK B32924 — X2 capacitor datasheet
- Microchip MSCSICPFC/REF5 — 30 kW SiC Vienna PFC reference design (EMI filter section)
- Wolfspeed PRD-08907 — Mitigating EMI with SiC in grid-connected converters

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
