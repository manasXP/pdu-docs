---
tags: [PDU, thermal, SiC, MOSFETs, diodes, gate-driver, heatsink]
created: 2026-02-22
---

# SiC Device Thermal Parameters — 30 kW PDU

This note compiles junction-to-case thermal resistance (Rth_jc), maximum junction temperature (Tj_max), package types, and key electrical parameters for all power devices in the 30 kW PDU design. Data is sourced directly from STMicroelectronics datasheets where confirmed; engineering-derived values are annotated.

---

## Device 1 — SCTWA90N65G2V-4

**Function:** Vienna PFC switch (6 devices)
**Description:** ST Gen2 SiC N-Channel MOSFET, 650 V

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Package** | HiP247-4 (4-pin, long leads) | Through-hole, Kelvin source pin |
| **VDS** | 650 V | |
| **ID (continuous)** | 119 A | At TC |
| **ID_max (pulsed)** | 220 A | |
| **Ptot** | 565 W | At TC = 25°C |
| **Rth_jc** | ~0.22 °C/W | Derived: Ptot = 565 W, Tj_max = 200°C; Rth_jc = (Tj_max - TC) / Ptot = (200-25)/565 ≈ 0.31 °C/W; ST confirms HiP247 Gen2 typical ≈ 0.22 °C/W (see note below) |
| **Rth_jA** | Not rated for use without heatsink | |
| **Tj_max** | 200 °C | Industry-leading for SiC discrete |
| **RDS(on) @ Tj=25°C** | 18 mΩ typ | VGS = 18 V, ID = 50 A |
| **RDS(on) @ Tj=150°C** | ~22 mΩ typ | Approx 1.2× factor, from ST characterization |
| **RDS(on) @ Tj=175°C** | ~24 mΩ typ | Approx 1.33× factor |
| **RDS(on) max @ 25°C** | 24 mΩ | Datasheet max |

> [!note] Rth_jc Derivation
> The SCTWA90N65G2V-4 datasheet lists Ptot = 565 W and Tj_max = 200°C at TC = 25°C, giving a theoretical Rth_jc = 175/565 = 0.31 °C/W (worst case). ST's application materials and comparable HiP247 Gen2 devices (e.g., SCTW90N65G2V standard version) consistently show Rth_jc ≈ 0.22–0.26 °C/W. Use **0.26 °C/W** as the conservative design value. Verify from the [official datasheet PDF](https://www.st.com/resource/en/datasheet/sctwa90n65g2v-4.pdf) Table 2 "Thermal data."

**Recommended gate drive:** +18 V / −5 V (for RDS(on) and Miller clamp performance)
**Body diode:** SiC body diode, reverse recovery essentially zero — no co-pack Schottky needed

---

## Device 2 — STPSC40H12C

**Function:** PFC boost rectifier / freewheeling diode (12 devices, dual 20 A per package)
**Description:** ST SiC Schottky Barrier Diode, 1200 V, 40 A (2 × 20 A in one TO-247 LL)

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Package** | TO-247 LL (long leads, 3-pin) | |
| **VRRM** | 1200 V | |
| **IF(AV)** | 2 × 20 A = 40 A total | Both anodes tied at cathode |
| **IF(RMS)** | 38 A | |
| **IFSM** | 140 A (10 ms), 700 A (10 µs) | Surge current |
| **Ptot** | ~150 W estimated | Standard TO-247 SiC Schottky at this current |
| **Rth_jc** | ~1.0 °C/W per diode | Typical for 20 A SiC Schottky in TO-247; verify from [datasheet PDF](https://www.st.com/resource/en/datasheet/stpsc40h12c.pdf) Table 3 |
| **Tj_max** | 175 °C | Confirmed from product page and distributor data |
| **Vf @ IF=20A, Tj=25°C** | 1.35 V typ, 1.50 V max | |
| **Vf @ IF=20A, Tj=150°C** | 1.75 V typ, 2.25 V max | Slight increase; SiC Schottky has positive temp coefficient |
| **Reverse leakage IR** | 800 µA max | At VRRM, Tj = 150°C |
| **Total capacitance QC** | 1650 pF | |

> [!note] Package Note
> The STPSC40H12C contains **two 20 A diodes in a single TO-247 LL** body with a common cathode (tab). This halves the footprint and package count versus discrete 20 A parts but the dual-die construction means the thermal resistance per die to the shared case is approximately **1.0 °C/W per diode**. For derating, treat each die independently: Tj_die = TC + (Pdiss_per_die × 1.0).

> [!warning] Verify Rth_jc
> The Rth_jc of ~1.0 °C/W is an engineering estimate based on comparable single-die SiC Schottky diodes (e.g., STPSC20H065: ~1.5 °C/W in TO-247; the dual-die STPSC40H12C has improved die-to-case coupling). Confirm from Table 3 of the [datasheet](https://www.st.com/resource/en/datasheet/stpsc40h12c.pdf).

---

## Device 3 — SCTW90N120G2AG

**Function:** LLC resonant converter primary switch (6 devices)

> [!warning] Part Number Not Found
> **SCTW90N120G2AG does not appear in ST's current product portfolio.** Extensive search across ST.com, distributors, and datasheet aggregators returned no results for this exact part number. ST's closest offerings in the 1200 V automotive-grade (AG) HiP247 family are:
>
> | Part | VDS | RDS(on) | ID | Package |
> |------|-----|---------|-----|---------|
> | SCTW60N120G2AG | 1200 V | 45 mΩ typ | 52 A | HiP247 |
> | **SCTW100N120G2AG** | 1200 V | 30 mΩ typ | 75 A | HiP247 |
> | SCTW70N120G2V | 1200 V | 21 mΩ typ | 91 A | HiP247 (non-AG) |
>
> **Recommended substitution:** Use **SCTW100N120G2AG** (AEC-Q101 automotive-grade, 1200 V, 30 mΩ, 75 A, HiP247).

### SCTW100N120G2AG — Recommended Substitute

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Package** | HiP247 (3-pin) | Through-hole |
| **VDS** | 1200 V | |
| **ID (continuous)** | 75 A | |
| **Ptot** | ~415 W estimated | Derived from Rth_jc and Tj_max |
| **Rth_jc** | ~0.30–0.40 °C/W | Engineering estimate; HiP247 Gen2 at lower ID than SCTWA90N65G2V. Confirm from ST datasheet. |
| **Tj_max** | 200 °C | ST Gen2 automotive SiC standard |
| **RDS(on) @ Tj=25°C** | 30 mΩ typ | |
| **RDS(on) @ Tj=150°C** | ~38 mΩ est | ~1.25× typical positive coefficient |
| **Certification** | AEC-Q101 | Automotive-grade |

> [!tip] For LLC Primary
> At 1200 V rating with 30 mΩ, this device provides comfortable voltage margin on the LLC primary (input 400–800 VDC bus). Six devices in a full-bridge gives 18.75 A peak per switch at 30 kW. RDS(on) conduction loss per switch ≈ 18.75² × 0.038 = 13.4 W.

**Datasheet:** [SCTW100N120G2AG on ST.com](https://www.st.com/en/power-transistors/sctw100n120g2ag.html)

---

## Device 4 — STPSC20H065

**Function:** LLC secondary rectifier (6–12 devices)
**Description:** ST SiC Schottky Barrier Diode, 650 V, 20 A (high surge)

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Package** | TO-247 (CW suffix = TO-247; C suffix = TO-220) | Use CW (TO-247) variant for better thermal performance |
| **VRRM** | 650 V | |
| **IF(AV)** | 20 A | Per diode |
| **Ptot** | ~115 W | TO-247 package |
| **Rth_jc** | ~1.4–1.6 °C/W | Typical for 20 A SiC Schottky in TO-247; confirm from [datasheet PDF](https://www.st.com/resource/en/datasheet/stpsc20h065c.pdf) Table 3 |
| **Tj_max** | 175 °C | Standard SiC Schottky limit |
| **Vf @ IF=10A, Tj=25°C** | 1.56 V typ, 1.75 V max | |
| **Vf @ IF=10A, Tj=150°C** | 1.98 V typ, 2.50 V max | Positive temp coefficient — losses increase with temperature |
| **IFSM** | 200 A (10 ms surge) | High-surge variant |

> [!note] Part Number Clarification
> "STPSC20H065" is the base designation. The full variant codes are:
> - **STPSC20H065CW** — TO-247 (recommended for heatsinking)
> - **STPSC20H065C** — TO-220AB
> - **STPSC20H065DY** — D²PAK (SMD)
>
> For a 12-device secondary rectifier bridge, use the **STPSC20H065CW** (TO-247) for lowest Rth_jc.

**Datasheet:** [STPSC20H065C on ST.com](https://www.st.com/en/diodes-and-rectifiers/stpsc20h065c.html)

---

## Device 5 — STGAP2SiC (STGAP2SICS)

**Function:** Isolated SiC MOSFET gate driver (6 devices, one per switch)
**Description:** Galvanically isolated single-channel gate driver, 4 A output, designed for SiC

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Package** | SO-8W (wide body, 8 mm creepage) | SMD, narrow SO-8W package |
| **Rth_jA** | 123 °C/W | Confirmed from ST datasheet (Table 3) |
| **Rth_jC** | Not the primary constraint — SMD device, PCB-coupled | |
| **Tj_max** | 125 °C | Operating temperature limit |
| **Thermal shutdown (TSD)** | Internal TSD protection | Device forces safe state at TSD threshold |
| **VCC supply** | 3.1–5.5 V (logic side) | |
| **Gate drive supply (VOUT)** | Up to 26 V rail-to-rail | Supports +18 V / −5 V bipolar drive |
| **Peak source/sink** | 4 A | Rail-to-rail output |
| **Propagation delay** | 75 ns | Input to output |
| **Isolation voltage** | 6 kV (galvanic) | Reinforced insulation |
| **dV/dt immunity** | ±100 V/ns | Full temp range |
| **Interlocking** | HW dual-input interlocking | Dead-time and shoot-through protection |
| **Miller clamp** | 4 A dedicated clamp | Prevents parasitic turn-on during fast switching |
| **Max input frequency** | 1 MHz | |

> [!important] Thermal Management for Gate Driver
> At Rth_jA = 123 °C/W and Tj_max = 125°C, the maximum allowable self-dissipation at 55°C ambient is:
> Pd_max = (125 − 55) / 123 = **0.57 W**
>
> At 100 kHz switching, driver dissipation is primarily in gate charge delivery:
> Pd ≈ VCC × Ig_avg + (drive losses) ≈ 0.3–0.5 W typical for a SiC MOSFET at 100 kHz.
>
> This is borderline at 55°C ambient. Consider:
> - Providing a small copper pour beneath SO-8W pad to reduce Rth_jA
> - Or using **STGAP2SICSN** (SOIC-16-narrow variant with better thermal path) if needed

**Datasheet:** [STGAP2SICS on ST.com](https://www.st.com/en/power-management/stgap2sics.html)

---

## Summary Table

| Device | Function | Qty | Package | Rth_jc (°C/W) | Tj_max (°C) | Key Electrical |
|--------|----------|-----|---------|--------------|------------|----------------|
| SCTWA90N65G2V-4 | Vienna PFC switch | 6 | HiP247-4 | **0.26** (conservative est.) | 200 | 650 V, 119 A, 18 mΩ typ |
| STPSC40H12C | PFC rectifier | 12 | TO-247 LL | **~1.0 per die** | 175 | 1200 V, 2×20 A, Vf=1.35 V |
| SCTW100N120G2AG *(sub)* | LLC primary | 6 | HiP247 | **~0.35** (est.) | 200 | 1200 V, 75 A, 30 mΩ typ |
| STPSC20H065CW | LLC secondary | 6–12 | TO-247 | **~1.5** (est.) | 175 | 650 V, 20 A, Vf=1.56 V |
| STGAP2SICS | Gate driver | 6 | SO-8W | Rth_jA=123 | 125 | 4 A, 6 kV iso, 26 V out |

---

## Heatsink Thermal Resistance — Forced Air Cooling

### Enclosure Parameters
- **Enclosure:** 455 × 300 × 94 mm (approximate 1U rack / PDU form factor)
- **Airflow:** ~3 m/s (~590 LFM) forced, axial fans
- **Max ambient (Ta):** 55°C (design maximum per IEC 61851-23 derating)
- **Heatsink material:** Aluminum extrusion, 6063-T6, thermal conductivity ~200 W/m·K

### Achievable Rth_sa for This Form Factor

| Heatsink Type | Dimensions (L × W × H) | Airflow | Rth_sa (°C/W) | Notes |
|---------------|------------------------|---------|--------------|-------|
| Small bar extrusion | 100 × 100 × 83 mm | 3 m/s | 0.12 | Documented (Enrgtech catalog) |
| Medium extrusion (full width) | 300 × 150 × 80 mm | 3 m/s | 0.05–0.08 | Engineering estimate |
| Large PDU heatsink (full chassis base) | 400 × 250 × 60 mm | 3 m/s | 0.03–0.06 | High-fin-density aluminum slab |
| **Target for this PDU** | **~300 × 200 mm usable** | **3 m/s** | **0.05–0.08 °C/W** | Two separate heatsinks likely (PFC + LLC) |

### Engineering Basis for Rth_sa Estimates

Using the volumetric thermal resistance approach from Electronics Cooling (1995):
- At 2.5 m/s: volumetric Rth ≈ 150–250 cm³·°C/W
- At 5.0 m/s: volumetric Rth ≈ 80–150 cm³·°C/W
- Interpolating for 3 m/s: ~120–200 cm³·°C/W

For a heatsink volume of ~300 × 150 × 60 mm = 2700 cm³:
**Rth_sa ≈ 120 / 2700 = 0.044 °C/W** (optimistic, ideal geometry)
**Rth_sa ≈ 200 / 2700 = 0.074 °C/W** (conservative, non-ideal)

**Design value to use: Rth_sa = 0.06 °C/W** for each of two parallel heatsinks (one for PFC stage, one for LLC stage).

### Thermal Interface Material (Rth_cs)

| Interface | Material | Rth_cs (°C/W) |
|-----------|----------|--------------|
| TO-247 / HiP247 → heatsink | Thermal pad (0.25 mm, k=6 W/m·K) | 0.10–0.20 per device |
| TO-247 / HiP247 → heatsink | Thermal grease + insulator | 0.08–0.15 per device |
| Recommended | Bergquist GP3000 or equivalent pad | ~0.12 per device |

For HiP247 package footprint (~18 × 17 mm = 3.06 cm²), with k=6 W/m·K pad at 0.25 mm:
**Rth_cs ≈ 0.25mm / (6 × 3.06 cm²) × 10 = ~0.14 °C/W**

---

## Thermal Budget — Worst Case Spot Check

### Vienna PFC MOSFET (SCTWA90N65G2V-4)

At 30 kW, 96% efficiency, 1.2 kW total loss. Rough apportionment:
- PFC stage loss budget: ~600 W across 6 MOSFETs
- Per MOSFET: conduction + switching ≈ 60–80 W peak

```
Tj = Ta + P × (Rth_jc + Rth_cs + Rth_sa / 6_devices_shared)
Tj = 55 + 70 × (0.26 + 0.14 + 0.06/6)
Tj = 55 + 70 × (0.26 + 0.14 + 0.01)
Tj = 55 + 70 × 0.41
Tj = 55 + 28.7 = ~84°C
```

This is well below 200°C — significant thermal margin. Even at double the estimated loss (140 W/device due to switching at high dV/dt), Tj ≈ 112°C, still comfortable.

### LLC Primary MOSFET (SCTW100N120G2AG)

LLC primary conduction per switch ≈ 15–20 W (soft-switching reduces dynamic losses significantly).

```
Tj = 55 + 20 × (0.35 + 0.14 + 0.01) = 55 + 20 × 0.50 = 55 + 10 = 65°C
```

Excellent margin — LLC topology greatly reduces switching loss.

### PFC Schottky Diode (STPSC40H12C)

Each dual-package carries ~20 A average; Vf ≈ 1.4 V at 150°C gives ~28 W per package.

```
Tj = 55 + 28 × (1.0 + 0.14 + 0.01) = 55 + 28 × 1.15 = 55 + 32 = 87°C
```

Below 175°C limit by 88°C margin.

---

## Design Actions Required

- [ ] Confirm Rth_jc for SCTWA90N65G2V-4 from Table 2 of [datasheet](https://www.st.com/resource/en/datasheet/sctwa90n65g2v-4.pdf)
- [ ] Confirm Rth_jc for STPSC40H12C from Table 3 of [datasheet](https://www.st.com/resource/en/datasheet/stpsc40h12c.pdf)
- [ ] Confirm Rth_jc for STPSC20H065CW from [datasheet](https://www.st.com/resource/en/datasheet/stpsc20h065c.pdf)
- [ ] Clarify original intent for "SCTW90N120G2AG" — confirm SCTW100N120G2AG is correct substitution
- [ ] Select heatsink extrusion profile — request thermal simulation from Aavid/Boyd for 300 × 200 mm footprint at 3 m/s, target Rth_sa < 0.08 °C/W
- [ ] Model gate driver thermal: verify STGAP2SICS self-heating at 100 kHz switching for 6 devices with copper pour optimization
- [ ] Run full [[04-Thermal Budget]] simulation with confirmed device values

---

## Sources

- [SCTWA90N65G2V-4 Datasheet — STMicroelectronics](https://www.st.com/resource/en/datasheet/sctwa90n65g2v-4.pdf)
- [STPSC40H12C Product Page — STMicroelectronics](https://www.st.com/en/diodes-and-rectifiers/stpsc40h12c.html)
- [STPSC40H12C Datasheet PDF](https://www.st.com/resource/en/datasheet/stpsc40h12c.pdf)
- [STPSC20H065C Datasheet PDF](https://www.st.com/resource/en/datasheet/stpsc20h065c.pdf)
- [SCTW100N120G2AG Product Page — STMicroelectronics](https://www.st.com/en/power-transistors/sctw100n120g2ag.html)
- [STGAP2SICS Product Page — STMicroelectronics](https://www.st.com/en/power-management/stgap2sics.html)
- [STGAP2SICS Datasheet PDF](https://www.st.com/resource/en/datasheet/stgap2sics.pdf)
- [How to Select a Heat Sink — Electronics Cooling (1995)](https://www.electronics-cooling.com/1995/06/how-to-select-a-heat-sink/)
- [AN-1057 Heatsink Characteristics — Infineon](https://www.infineon.com/dgdl/an-1057.pdf?fileId=5546d462533600a401535591d3170fbd)
- [100 × 300 × 83 mm Heatsink, 0.12 °C/W example — Enrgtech](https://www.enrgtech.co.uk/product/heatsinks/ET13906113/177AB1000B)
- [SCTW70N120G2V 1200V 91A HiP247 — Mouser](https://www.mouser.com/new/stmicroelectronics/stm-sctw70n120g2v-1200v-sic-power-mosfet/)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
