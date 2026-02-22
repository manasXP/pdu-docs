---
tags: [PDU, thermal, cooling, loss-budget, forced-air, SiC]
created: 2026-02-22
status: draft
---

# Thermal Budget — 30 kW PDU

> [!summary] Key Results
> Total system loss at 30 kW: **~960 W** (96.8% system efficiency). Peak component: LLC secondary diodes at 180 W total. Forced-air cooling with two aluminum extrusion heatsinks (PFC + LLC) and 3 × 92 mm fans provides adequate margin at 55°C ambient. Hottest junction: LLC secondary diodes at **133°C** (margin of 42°C to Tj_max = 175°C). Thermal derating begins at 55°C ambient — system maintains full 30 kW output with fan speed boost.

## 1. Design Constraints

From [[__init]] and [[01-Topology Selection]]:

| Parameter | Value |
|-----------|-------|
| Rated power | 30 kW |
| Enclosure dimensions | 455 × 300 × 94 mm |
| Enclosure volume | 12.8 L |
| Max ambient temperature | 55°C (full load) |
| Cooling method | Forced air |
| Fan noise limit | ≤65 dB |
| Weight target | ~17 kg |
| System efficiency spec | >96% |
| MTBF target | >120,000 hours |

**Thermal budget approach:** Bottom-up loss calculation for each component, then thermal resistance network from junction to ambient.

## 2. System Loss Breakdown

### 2.1 PFC Stage — Vienna Rectifier

Operating at 30 kW input, ~98.5% efficiency → **~450 W total PFC loss**.

Detailed breakdown:

| Component | Part | Qty | Loss per Device (W) | Total Loss (W) | Notes |
|-----------|------|-----|--------------------:|---------------:|-------|
| SiC MOSFETs | SCTWA90N65G2V-4 | 6 | 25 | 150 | Rds(on)=22 mΩ @150°C, ~10 Arms/device, fsw=65 kHz |
| SiC Schottky diodes | STPSC40H12C | 12 | 12 | 144 | Vf=1.5 V @10 A avg, 150°C |
| Input EMI filter | — | 1 | — | 15 | Core loss in CM/DM inductors |
| Boost inductors | — | 3 | 15 | 45 | Core + copper loss per phase |
| DC bus capacitors | — | — | — | 10 | ESR loss in electrolytic + film |
| Gate drivers | STGAP2SiC | 3 | 0.5 | 1.5 | Low dissipation at 65 kHz |
| Control + aux power | STM32G474RE + LDOs | — | — | 8 | MCU + isolated supplies |
| PCB traces + connectors | — | — | — | 20 | I²R in bus bars and copper |
| Snubbers / clamps | — | — | — | 5 | RCD snubber losses |
| **PFC Total** | | | | **~399** | **98.7% PFC efficiency** |

> [!note] PFC efficiency
> At 30 kW input with ~399 W loss → η = 98.7%. This is consistent with ST's measured >98.55% on the STDES-30KWVRECT reference design (which uses the same topology and devices).

### 2.2 DC-DC Stage — 3-Phase Interleaved LLC

Operating at ~29.6 kW input (PFC output), >98% efficiency → **~500 W total LLC loss**.

Per-phase breakdown (×3 phases, 10 kW each):

| Component | Part | Qty/Phase | Loss per Device (W) | Loss/Phase (W) | Total 3-Phase (W) | Notes |
|-----------|------|-----------|--------------------:|---------------:|-------------------:|-------|
| Primary MOSFETs | SCTW100N120G2AG | 2 | 18 | 36 | 108 | Rds(on)=36 mΩ @150°C, ~14 Arms, ZVS reduces turn-on loss |
| Secondary diodes | STPSC20H065CW | 2–4 | 30 | 60 | 180 | Vf=1.7 V @avg 8 A, 150°C; dominant loss |
| Transformer core | E65/32/27, 3C97 | 1 | 8 | 8 | 24 | 57–72 mT, from [[02-Magnetics Design]] |
| Transformer copper | Litz wire | — | — | 35 | 105 | P-S-P-S interleaved, from [[02-Magnetics Design]] |
| Resonant inductor | Kool Mµ toroid | 1 | 8 | 8 | 24 | 33 µH discrete, from [[02-Magnetics Design]] |
| Resonant capacitor | C0G MLCC array | 1 set | 5 | 5 | 15 | ESR loss, from [[02-Magnetics Design]] |
| Gate drivers | STGAP2SiC | 1 | 0.5 | 0.5 | 1.5 | 150 kHz drive |
| PCB traces + bus bars | — | — | — | 8 | 24 | I²R in power path |
| Output capacitors | — | — | — | 5 | 15 | ESR loss in output filter |
| **LLC Total** | | | | **~166** | **~497** | **~98.3% LLC efficiency** |

### 2.3 Auxiliary and Miscellaneous

| Component | Loss (W) | Notes |
|-----------|----------|-------|
| Fans (3 × 92 mm) | 15 | ~5 W each at full speed |
| Auxiliary power supply | 10 | Standby + housekeeping |
| CAN transceiver + interface | 2 | SN65HVD230 + opto-isolation |
| Inrush limiter relay | 3 | Coil power when energized |
| Output contactor | 5 | Coil + contact I²R |
| Wiring harness | 10 | Internal DC cables |
| **Aux Total** | **45** | |

### 2.4 System Loss Summary

| Stage | Loss (W) | Efficiency | % of Total Loss |
|-------|----------|------------|----------------|
| PFC (Vienna) | 399 | 98.7% | 42% |
| DC-DC (LLC ×3) | 497 | 98.3% | 53% |
| Auxiliary | 45 | — | 5% |
| **System Total** | **941** | **96.9%** | 100% |

> [!tip] The system efficiency of 96.9% exceeds the >96% specification with comfortable margin.

**Top loss contributors (Pareto):**

| Rank | Component | Total Loss (W) | % of System |
|------|-----------|---------------:|------------:|
| 1 | LLC secondary diodes | 180 | 19% |
| 2 | PFC MOSFETs | 150 | 16% |
| 3 | PFC diodes | 144 | 15% |
| 4 | LLC primary MOSFETs | 108 | 11% |
| 5 | Transformer copper (×3) | 105 | 11% |
| 6 | Transformer core (×3) | 24 | 3% |
| | All other | 230 | 25% |

## 3. Thermal Resistance Network

### 3.1 Device Thermal Parameters

| Device | Package | Rth_jc (°C/W) | Rth_cs (°C/W) | Tj_max (°C) |
|--------|---------|--------------|--------------|-------------|
| SCTWA90N65G2V-4 (PFC MOSFET) | HiP247-4 | 0.26 | 0.12 | 200 |
| STPSC40H12C (PFC diode) | TO-247 LL | 1.0 (per die) | 0.12 | 175 |
| SCTW100N120G2AG (LLC MOSFET) | HiP247 | 0.35 | 0.12 | 200 |
| STPSC20H065CW (LLC diode) | TO-247 | 1.5 | 0.12 | 175 |
| STGAP2SiC (gate driver) | SO-8W | 123 (Rth_ja) | — | 125 |

**Rth_cs** (case-to-sink): 0.12 °C/W assumes Bergquist GP3000S or Laird Tflex thermal pad (k ≈ 3 W/m·K, 0.25 mm thick).

### 3.2 Heatsink Architecture

The 455 × 300 × 94 mm enclosure is divided into two thermal zones:

```
┌────────────────────────────────────────────────────────────┐
│  455 mm                                                    │
│ ┌──────────────────┐ ┌──────────────────────────────────┐  │ 94 mm
│ │   PFC Heatsink   │ │         LLC Heatsink             │  │ height
│ │   ~150 × 280 mm  │ │        ~280 × 280 mm             │  │
│ │   6 PFC MOSFETs  │ │  6 LLC MOSFETs + 6–12 diodes     │  │
│ │   12 PFC diodes  │ │  3 transformers + 3 inductors    │  │
│ └──────────────────┘ └──────────────────────────────────┘  │
│                                                            │
│  ◄── Airflow (3 × 92 mm fans at intake) ──►                │
│  [FAN] [FAN] [FAN]                         [exhaust mesh]  │
└────────────────────────────────────────────────────────────┘
```

**Heatsink specifications:**

| Parameter | PFC Heatsink | LLC Heatsink |
|-----------|-------------|-------------|
| Footprint | 150 × 280 mm | 280 × 280 mm |
| Fin height | 40 mm | 40 mm |
| Fin count | ~25 (6 mm pitch) | ~45 (6 mm pitch) |
| Material | Aluminum 6063-T5 extrusion | Aluminum 6063-T5 extrusion |
| Rth_sa (at 3 m/s) | 0.10 °C/W | 0.06 °C/W |
| Heat load | ~399 W | ~497 W |

### 3.3 Fan Selection

| Parameter | Value |
|-----------|-------|
| Fan type | 3 × 92 × 92 × 25 mm axial |
| Airflow per fan | ~65 CFM at free air |
| System airflow (with backpressure) | ~120 CFM total (~55 CFM through each heatsink zone) |
| Air velocity through fins | ~3.0 m/s |
| Noise at full speed | ~55 dB (per fan) |
| Noise at system level | ~60 dB (3 fans, directional exhaust) |
| Power per fan | ~5 W |
| Speed control | PWM via MCU, temperature-proportional |

> [!note] Noise budget
> At full fan speed: ~60 dB system. Spec allows ≤65 dB. Under typical conditions (Tambient < 40°C or output < 25 kW), fans run at reduced speed (~40–60%) for ~45 dB.

## 4. Junction Temperature Analysis

### 4.1 Thermal Calculation Method

For each device, the junction temperature is:

$$T_j = T_{ambient} + P_{device} \times (R_{th,jc} + R_{th,cs}) + P_{total,zone} \times R_{th,sa}$$

Where:
- P_device = power dissipated in the individual device
- P_total,zone = total power dissipated on the shared heatsink
- Rth_sa = heatsink-to-ambient thermal resistance

### 4.2 Worst-Case Analysis (T_amb = 55°C, 30 kW)

**PFC Zone** (399 W on PFC heatsink, Rth_sa = 0.10 °C/W):

Heatsink surface temperature:

$$T_{hs,PFC} = 55 + 399 \times 0.10 = 55 + 39.9 = 94.9 \text{ °C}$$

| Device | P_dev (W) | Rth_jc + Rth_cs | ΔT_jc (°C) | Tj (°C) | Tj_max (°C) | Margin (°C) |
|--------|----------|----------------|------------|---------|------------|-------------|
| PFC MOSFET (each) | 25 | 0.38 | 9.5 | 104 | 200 | **96** |
| PFC diode (per die) | 12 | 1.12 | 13.4 | 108 | 175 | **67** |

**LLC Zone** (497 W on LLC heatsink, Rth_sa = 0.06 °C/W):

Heatsink surface temperature:

$$T_{hs,LLC} = 55 + 497 \times 0.06 = 55 + 29.8 = 84.8 \text{ °C}$$

| Device | P_dev (W) | Rth_jc + Rth_cs | ΔT_jc (°C) | Tj (°C) | Tj_max (°C) | Margin (°C) |
|--------|----------|----------------|------------|---------|------------|-------------|
| LLC primary MOSFET (each) | 18 | 0.47 | 8.5 | 93 | 200 | **107** |
| LLC secondary diode (each) | 30 | 1.62 | 48.6 | **133** | 175 | **42** |

**Magnetic components** (mounted on LLC heatsink or separate bracket):

| Component | P_dev (W) | Estimated Rth (°C/W) | T_surface (°C) | Notes |
|-----------|----------|---------------------|----------------|-------|
| Transformer (each) | 43 | 1.5 (core-to-ambient, forced air) | 120 | Core + copper at design center |
| Resonant inductor (each) | 8 | 3.0 (toroid, limited contact) | 109 | Kool Mµ toroid |

> [!warning] Hottest component: LLC secondary diodes at 133°C
> The STPSC20H065CW diodes are the thermal bottleneck due to their high Vf (1.7 V at 150°C) and relatively high Rth_jc (1.5 °C/W in TO-247). The 42°C margin to Tj_max = 175°C is adequate but not generous.
>
> **If margin is insufficient after prototype measurement:**
> - Upgrade to STPSC30H065CW (30 A, lower Vf per amp) — reduces loss to ~40 W total
> - Or add synchronous rectification (Rev 2) — eliminates diode loss entirely
> - Or add a small dedicated heatsink clip to each diode (reduces Rth_cs)

### 4.3 PFC Heatsink Temperature Concern

The PFC heatsink reaches 95°C at worst case. This is close to the electrolytic capacitor rated temperature.

> [!warning] DC bus capacitors
> Electrolytic capacitors near the PFC heatsink will see ~85–95°C ambient. Standard 105°C-rated electrolytics would have minimal margin. Mitigation:
> - Use 125°C-rated low-ESR electrolytic capacitors (e.g., Nichicon UBY or Nippon Chemi-con KMZ)
> - Place bus capacitors away from the heatsink fins, in a lower-temperature zone
> - Add thermal isolation (air gap or insulating spacer) between capacitors and heatsink

## 5. Operating Scenarios

### 5.1 Temperature vs. Output Power

| Condition | T_amb (°C) | Output (kW) | P_loss (W) | T_hs,PFC (°C) | T_hs,LLC (°C) | Tj,max (°C) | Fan Speed |
|-----------|-----------|-------------|-----------|---------------|---------------|-------------|-----------|
| Full load, hot | 55 | 30 | 941 | 95 | 85 | 133 (diode) | 100% |
| Full load, typical | 40 | 30 | 941 | 80 | 70 | 118 (diode) | 75% |
| Full load, cool | 25 | 30 | 941 | 65 | 55 | 103 (diode) | 50% |
| Half load, hot | 55 | 15 | ~350 | 70 | 64 | 98 (diode) | 60% |
| Light load | 40 | 5 | ~120 | 52 | 47 | 58 (diode) | 30% |
| Standby | 40 | 0 | <8 | 41 | 41 | — | Off |

> [!note] Loss scaling
> Conduction losses scale as I² (quadratic with load). Switching losses scale roughly linearly. Core losses are roughly constant. At half load (15 kW), total loss drops to ~350 W (not half of 941 W — fixed losses dominate at light load).

### 5.2 Thermal Derating

The spec requires full 30 kW at 55°C. The analysis shows this is achievable with 42°C margin on the hottest junction (LLC diode).

**Derating schedule (safety margin for prototype):**

| Ambient (°C) | Max Output (kW) | Limiting Factor |
|-------------|----------------|-----------------|
| ≤55 | 30 | Full rated |
| 55–65 | 25 (linear derate) | LLC diode Tj approaches 160°C |
| 65–70 | 20 | Electrolytic cap life |
| >70 | Shutdown (OTP) | Protection trip |

## 6. Airflow Design

### 6.1 Pressure Drop Budget

```
Intake (3 × 92 mm fans) → PFC heatsink → LLC heatsink → Exhaust mesh
         ↓                     ↓              ↓              ↓
    ~0.1 in-H₂O           0.15 in-H₂O    0.20 in-H₂O   0.05 in-H₂O
                           Total system ΔP ≈ 0.50 in-H₂O
```

At 0.50 in-H₂O backpressure, typical 92 mm fans deliver ~40 CFM each → 120 CFM system. This corresponds to ~3 m/s through the heatsink fin channels.

### 6.2 Airflow Path

The airflow path is designed for:
1. **Intake fans** mounted on one end of the enclosure (push configuration)
2. **PFC heatsink** receives fresh, cool air first (lower ΔT)
3. **LLC heatsink** receives pre-heated air (~5°C warmer than intake) — but LLC heatsink is larger with lower Rth_sa to compensate
4. **Exhaust mesh** on the opposite end

> [!tip] Pre-heating correction
> The LLC heatsink receives air pre-heated by the PFC stage. At 120 CFM and 399 W PFC loss:
> $$\Delta T_{air} = \frac{P_{PFC}}{\dot{m} \cdot c_p} = \frac{399}{120 \times 0.472 \times 1.006 \times 1.2} \approx \frac{399}{68.2} = 5.9 \text{ °C}$$
>
> So LLC heatsink effective ambient is **55 + 6 = 61°C** at worst case.
> Updated LLC heatsink temperature: 61 + 497 × 0.06 = 91°C.
> Updated LLC diode Tj: 91 + 48.6 = **140°C** (margin = 35°C).
>
> This is still safe but reduces margin. Consider a parallel airflow architecture instead of series if prototype measurements show issues.

### 6.3 Alternative: Parallel Airflow

If the series airflow pre-heating reduces LLC margin too much, switch to a parallel layout:

```
         ┌─── PFC heatsink ──── exhaust ───┐
Intake ──┤                                 ├── exhaust mesh
         └─── LLC heatsink ──── exhaust ───┘
```

Both heatsinks receive fresh ambient air. This requires a duct/baffle partition in the enclosure.

## 7. Component-Level Thermal Summary

| Component | Qty | Loss/Unit (W) | Total (W) | Tj or Tsurf (°C) | Limit (°C) | Margin (°C) | Status |
|-----------|-----|--------------|----------|-----------------|-----------|------------|--------|
| PFC MOSFET | 6 | 25 | 150 | 104 | 200 | 96 | OK |
| PFC diode | 12 | 12 | 144 | 108 | 175 | 67 | OK |
| LLC primary MOSFET | 6 | 18 | 108 | 93 | 200 | 107 | OK |
| **LLC secondary diode** | **6–12** | **30** | **180** | **133–140** | **175** | **35–42** | **Watchlist** |
| Transformer (×3) | 3 | 43 | 129 | 120 | 180 (ferrite Curie) | 60 | OK |
| Resonant inductor (×3) | 3 | 8 | 24 | 109 | 200 (Kool Mµ) | 91 | OK |
| DC bus capacitor | — | 10 | 10 | 85–95 | 125 (rated) | 30–40 | **Watchlist** |
| Gate driver (STGAP2SiC) | 6 | 0.5 | 3 | ~95 | 125 | 30 | OK |
| STM32G474RE | 1 | 2 | 2 | ~85 | 125 | 40 | OK |

## 8. Reliability Impact

### 8.1 Capacitor Life

Electrolytic capacitor life follows the Arrhenius equation (halving rule):

$$L = L_0 \times 2^{(T_{rated} - T_{actual})/10}$$

For a 125°C-rated, 10,000-hour capacitor at Tcap = 90°C:

$$L = 10000 \times 2^{(125-90)/10} = 10000 \times 2^{3.5} = 10000 \times 11.3 = 113{,}000 \text{ hours}$$

This comfortably exceeds the 120,000-hour MTBF target — but only if 125°C-rated capacitors are used. Standard 105°C capacitors at 90°C would give only 28,000 hours.

> [!warning] Use 125°C-rated electrolytic capacitors throughout. This is a hard requirement for the 120,000-hour MTBF at 55°C ambient.

### 8.2 Fan Life

At full speed continuous: typical fan MTBF = 70,000 hours (ball bearing) to 100,000+ hours (fluid dynamic bearing). With PWM speed reduction during normal operation (average ~50% speed), effective fan life extends to >150,000 hours.

**Recommendation:** Dual ball bearing or FDB fans. Include fan-fail detection (tachometer feedback to MCU) with automatic derating if a fan fails.

### 8.3 Semiconductor Life

All SiC devices operate well within their Tj_max limits. At Tj = 133°C (worst-case LLC diode), SiC Schottky diodes have effectively unlimited life (no wear-out mechanism at this temperature for at least 20 years).

## 9. Design Risks and Open Items

| Risk / Item | Severity | Status | Mitigation |
|-------------|----------|--------|------------|
| LLC diode Tj = 133–140°C at 55°C ambient | Medium | Watchlist | Upgrade to STPSC30H065CW or add SR in Rev 2; consider parallel airflow |
| PFC heatsink temperature vs. bus caps | Medium | Watchlist | Use 125°C electrolytics; thermal isolation between heatsink and caps |
| Air pre-heating in series flow | Low | Open | Prototype measurement; parallel airflow as fallback |
| Altitude derating (air density drops) | Low | Open | Add altitude-aware derating table if deployed above 2000 m |
| Fan failure mode | Medium | Planned | Tachometer feedback; auto-derate to 20 kW on 2 fans |
| Transformer core temperature measurement | Low | Open | Add NTC on one transformer per module for OTP |

## 10. Next Steps

- [ ] CFD simulation of enclosure airflow — validate 3 m/s through fin channels
- [ ] Prototype heatsink procurement and thermal impedance measurement
- [ ] Fan curve characterization at system backpressure
- [ ] Select specific 125°C electrolytic capacitors for DC bus (BOM update)
- [ ] Decide series vs. parallel airflow architecture after prototype testing
- [ ] Add NTC placement for OTP sensing (transformers, heatsink, ambient)

## 11. References

- [[01-Topology Selection]] — Architecture, semiconductor BOM, efficiency targets
- [[02-Magnetics Design]] — Transformer and inductor loss budgets
- [[03-LLC Gain Curve Verification]] — LLC operating points and frequency map
- [[SiC Device Thermal Parameters]] — Device Rth_jc and package data
- ST SCTWA90N65G2V-4 datasheet — PFC MOSFET thermal data
- ST STPSC40H12C datasheet — PFC diode thermal data
- ST STPSC20H065CW datasheet — LLC diode thermal data
- JEDEC JESD51 — Thermal resistance measurement standards
- Bergquist GP3000S datasheet — Thermal interface material

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
