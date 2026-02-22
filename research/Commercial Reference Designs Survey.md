---
tags: [PDU, reference-design, SiC, EV-charging]
created: 2026-02-21
---

# Commercial Reference Designs Survey

> Survey of production-grade and evaluation-grade reference designs for 30 kW EV charger power modules from major semiconductor vendors. Data drawn from vendor publications, APEC 2024 presentations, and product pages current through early 2025.

See also: [[3-Phase PFC Topology Selection]], [[DC-DC Topology Trade Study]]

---

## Comparative Summary

| Vendor | Design | PFC | DC-DC | Peak Eff. | Output Range | Bi-Dir | Controller |
|---|---|---|---|---|---|---|---|
| **Wolfspeed** | CRD30DD12N-K | N/A (ext.) | 3-ph interleaved LLC | >98% | 200-1000 V | No | Not disclosed |
| **Infineon/Arrow** | 30kW DCFC Platform | CoolSiC-based | CoolSiC-based | N/A | N/A | Yes | N/A |
| **Infineon** | REF-DAB11KIZSICSYS | N/A | CLLC resonant DAB | >=97.2% | 550-800 V | Yes | Not disclosed |
| **ST** | STDES-30KWVRECT | Vienna | -- | >98.55% | -- | No | STM32G474RE |
| **ST** | STDES-30KWLLC | -- | 3-ph interleaved LLC | >98% | 200-1000 V | No | STM32G474RE |
| **onsemi** | SEC-25KW-SIC-PIM | 6-sw active rect. | DAB | 96% (system) | 200-1000 V | Yes | Zynq-7000 SoC |
| **TI** | TIDA-010054 | -- | DAB (phase-shifted) | 98.7% | 500-800 V | Yes | TMS320F280039 |
| **TI** | TIDA-01606 | 3-level T-type | -- | N/A | 800 V bus | Yes | TMS320F28388D |
| **ADI** | EVAL-DCDC-CHARGER | N/A | 3-ph interleaved HB | 98% | Up to 750 V | Yes | LT3999 |
| **Microchip** | Polymorphic DC-DC | N/A | Dual full-bridge PSFB | 98.6% | 400 V class | No | **Discontinued** |

---

## 1. Wolfspeed -- CRD30DD12N-K

| Parameter | Value |
|---|---|
| **DC-DC Topology** | 3-phase interleaved LLC resonant converter |
| **PFC Topology** | Not included (requires external AFE to supply 650-900 VDC bus) |
| **Primary SiC MOSFETs** | C3M0040120K -- 1200 V, 40 mohm, TO-247-4 (Gen 3 C3M) |
| **Secondary Diodes** | C6D20065D / C6D10065A -- 650 V SiC Schottky |
| **Output Voltage** | 200-1000 VDC |
| **Input DC Bus** | 650-900 VDC |
| **Peak Efficiency** | >98% |
| **Switching Frequency** | 130-250 kHz (adaptive control) |
| **Power Density** | 6.5 kW/L |

**Unique Features:** Secondary side manually reconfigurable between series and parallel connection for full 200-1000 V range. Also available as CRD-60DD12N-K (60 kW scaled version).

**Source:** [Wolfspeed CRD30DD12N-K](https://www.wolfspeed.com/products/power/reference-designs/crd30dd12n-k/)

---

## 2. Infineon / Arrow -- 30 kW DCFC Reference Platform

| Parameter | Value |
|---|---|
| **Power Modules** | 1200 V CoolSiC Easy power modules (EasyPACK) |
| **PFC Topology** | Not publicly detailed |
| **DC-DC Topology** | Not publicly detailed |
| **Bi-directional** | Yes |
| **Energy Metering** | Integrated |

Developed by Arrow's High Power Center of Excellence with eInfochips and Infineon. Demonstrated at APEC 2024.

**Related -- REF-DAB11KIZSICSYS (11 kW stackable block):**

| Parameter | Value |
|---|---|
| **Topology** | CLLC resonant DAB (bi-directional) |
| **SiC MOSFETs** | IMZ120R030M1H (1200 V CoolSiC) |
| **Gate Driver** | 1EDC20I12AH |
| **Output** | 550-800 V, 11 kW |
| **Peak Efficiency** | >=97.2% |

Three units in parallel reach 30 kW+ with V2G/V2H support.

**Source:** [Arrow/Infineon APEC 2024](https://evtechinsider.com/arrow-electronics-unveils-new-30kw-dc-fast-charger-reference-platform-using-infineon-power-modules/)

---

## 3. STMicroelectronics -- STDES-30KWVRECT + STDES-30KWLLC

The most complete reference -- matched PFC + DC-DC pair forming a full 30 kW charger.

**PFC Stage -- STDES-30KWVRECT:**

| Parameter | Value |
|---|---|
| **Topology** | Vienna rectifier (3-phase, 3-level) |
| **SiC MOSFETs** | SCTWA90N65G2V-4 (Gen 2 SiC) |
| **SiC Diodes** | STPSC40H12C |
| **Gate Driver** | STGAP2SiC |
| **Controller** | STM32G474RE (Cortex-M4F) |
| **Peak Efficiency** | >98.55% |
| **Firmware** | STSW-30KWVRECT (provided) |

**DC-DC Stage -- STDES-30KWLLC:**

| Parameter | Value |
|---|---|
| **Topology** | 3-phase interleaved LLC resonant |
| **SiC MOSFETs** | Gen 3 SiC |
| **Gate Driver** | STGAP2SiC |
| **Controller** | STM32G474RE |
| **DC Input** | 650-850 VDC |
| **DC Output** | 200-1000 VDC |
| **Switching Freq** | 100-300 kHz |
| **Peak Efficiency** | >98% |

**Source:** [STDES-30KWVRECT](https://www.st.com/en/evaluation-tools/stdes-30kwvrect.html), [ST APEC 2024 Presentation](https://www.st.com/content/dam/static-page/events/apec-2024/demo-apec-24-30kw-dc-dc.pdf)

---

## 4. onsemi -- SEC-25KW-SIC-PIM-GEVK

| Parameter | Value |
|---|---|
| **PFC Topology** | 6-switch active rectifier (3-phase) |
| **DC-DC Topology** | Dual Active Bridge (DAB), phase-shifted modulation |
| **SiC Modules** | NXH010P120MNF1 -- 1200 V, 10 mohm EliteSiC M3S half-bridge PIM |
| **Controller** | Zynq-7000 SoC (FPGA + ARM) |
| **Input** | 400 VAC (EU) / 480 VAC (US) |
| **Output** | 200-1000 VDC |
| **System Efficiency** | 96% (PFC + DC-DC combined) |
| **Bi-directional** | Yes |
| **Power** | 25 kW nominal, scalable to 100 kW |

**Unique Features:** PIM approach reduces parasitic inductance. 40% smaller and 52% lighter than IGBT equivalents. TNPC module variant available (NXH008T120M3F2PTHG) for 3-level topologies.

**Source:** [onsemi SEC-25KW-SIC-PIM-GEVK](https://www.onsemi.com/design/evaluation-board/SEC-25KW-SIC-PIM-GEVK)

---

## 5. Texas Instruments -- TIDA Series (Stackable Building Blocks)

TI offers modular 10-11 kW blocks (3x = 30 kW):

**TIDA-010054 (10 kW DAB DC-DC):**

| Parameter | Value |
|---|---|
| **Topology** | Single-phase DAB (phase-shifted) |
| **SiC Gate Driver** | UCC21710 |
| **Controller** | TMS320F280039 (C2000, 120 MHz) |
| **Switching Freq** | 100 kHz with planar magnetics |
| **Peak Efficiency** | 98.7% |
| **Full-Load Eff** | 98% |
| **Bi-directional** | Yes |

**TIDA-01606 (11 kW T-type PFC):**

| Parameter | Value |
|---|---|
| **Topology** | 3-phase, 3-level T-type bidirectional |
| **Controller** | TMS320F28388D (C2000) |
| **Switching Freq** | 90 kHz |
| **DC Bus** | 800 V nominal, 900 V max |
| **Output THD** | <2.5% at full load |

**Source:** [TIDA-010054](https://www.ti.com/tool/TIDA-010054), [TIDA-01606](https://www.ti.com/tool/TIDA-01606)

---

## 6. Analog Devices -- EVAL-DCDC-CHARGER

| Parameter | Value |
|---|---|
| **Topology** | 3-phase interleaved half-bridge (buck/boost, bidirectional) |
| **Gate Drivers** | ADuM4135, ADuM4136 (isolated) |
| **Controller** | LT3999 |
| **DC Link** | 1000 V |
| **Battery Voltage** | Up to 750 V |
| **Current** | 100 A typical, 150 A max |
| **Switching Freq** | 80 kHz |
| **Peak Efficiency** | 98% |

**Source:** [ADI EVAL-DCDC-CHARGER](https://wiki.analog.com/resources/eval/eval-dcdc-charger)

---

## Topology Trends 2024-2025

**PFC Stage:**
- **Vienna Rectifier** -- Most popular for unidirectional 30 kW. 3-level, low THD, >98.5% with SiC.
- **3-Level T-type (TNPC)** -- Growing for bidirectional/V2G. Full 4-quadrant operation.
- **6-Switch Active Rectifier** -- Simple bidirectional option (2-level, higher switching stress).

**DC-DC Stage:**
- **3-Phase Interleaved LLC** -- Dominant for unidirectional (Wolfspeed, ST). Low ripple, high efficiency.
- **CLLC Resonant DAB** -- Emerging for bidirectional (Infineon). ZVS on both sides.
- **Dual Active Bridge (DAB)** -- Bidirectional workhorse (onsemi, TI). Wide voltage range via phase-shift.

**Dominant pairing:** Vienna + Interleaved LLC (unidirectional) or T-type/AFE + CLLC/DAB (bidirectional/V2G).

---

## GaN vs SiC at 30 kW

| Factor | SiC (1200 V) | GaN (650 V) |
|---|---|---|
| Voltage rating | Direct 800 V bus operation | Requires series stacking or multilevel |
| Switching loss | Low (~50% less than Si) | ~50% less than SiC; enables MHz |
| Thermal conductivity | 330-490 W/m-K | ~130 W/m-K |
| Maturity at 30 kW | **Proven** -- all vendors ship reference designs | Emerging -- most designs at 3-10 kW |
| Cost (2024-2025) | Declining; approaching Si parity | Premium at high current ratings |

**Verdict:** At 30 kW, **1200 V SiC is the clear choice** for 2024-2026 designs. Every reference design surveyed uses SiC. GaN may become competitive when 1200 V GaN devices mature.

---

## Key Takeaways for PDU Design

1. **Vienna + Interleaved LLC** is the highest-efficiency proven combination for unidirectional 30 kW (system >97%)
2. **T-type PFC + CLLC/DAB** if bidirectional (V2G) is required
3. **STM32G4** (ST) and **C2000 TMS320F28003x** (TI) are the dominant controller platforms with the most mature firmware
4. **1200 V SiC MOSFETs** in the 25-65 mohm range are standard across all vendors
5. **Power density** benchmarks: 4-6.5 kW/L (air-cooled); >10 kW/L (liquid-cooled, emerging)
6. The [Wolfspeed EV Charging Power Topologies Design Guidebook (PRD-08367)](https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_PRD-08367_EV_Charging_Power_Topologies_Design_Guidebook_Application_Note.pdf) is an excellent free resource

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
