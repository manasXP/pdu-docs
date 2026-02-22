---
tags: [PDU, PFC, power-electronics, EV-charging, topology, SiC]
created: 2026-02-21
---

# 3-Phase AC-DC PFC Topology Selection for 30 kW EV Fast Charger Module

See also: [[DC-DC Topology Trade Study]], [[Commercial Reference Designs Survey]]

## Design Requirements Recap

| Parameter | Specification |
|-----------|--------------|
| Input voltage | 260--530 VAC, 3-phase |
| Input current | Up to 60 A |
| Power factor | >= 0.99 |
| Input THDi | <= 5% at full load |
| DC bus output | 700--800 VDC nominal (feeding isolated DC-DC stage) |
| PFC stage efficiency target | >= 98% |
| Overall module efficiency | >= 96% |
| Preferred switches | SiC MOSFETs (1200 V class) |

> [!note] Architecture Context
> The PFC stage produces a regulated DC bus (typically 750--800 V) that feeds an isolated DC-DC converter (e.g., CLLC or DAB). The DC-DC stage then provides the wide 150--1000 VDC output to the EV battery.

---

## 1. Vienna Rectifier (3-Switch, 3-Level Boost)

### Operating Principle

The Vienna rectifier is a unidirectional, three-phase, three-level boost-type PFC. Conceptually it is a three-phase diode bridge with an integrated boost converter per phase. Each phase leg contains a single controlled bidirectional switch (typically implemented as two back-to-back MOSFETs or a MOSFET with series diodes) and freewheeling diodes connecting to the split DC bus. When the switch is ON, current ramps up in the boost inductor; when OFF, current flows through the freewheeling diodes into the upper or lower DC bus capacitor depending on the input voltage polarity. The three-level switching means each device only blocks half the DC bus voltage (~400 V for an 800 V bus), enabling use of 650 V devices in some implementations or very comfortable margins with 1200 V SiC.

### Component Count

| Component | Quantity | Notes |
|-----------|----------|-------|
| Active switches (MOSFETs) | 6 (3 bidirectional switch cells, each = 2 MOSFETs back-to-back) | Or 3 MOSFETs + 6 series diodes in T-type variant |
| Fast diodes | 6 (freewheeling) + 6 (bridge/clamping) | 12 total in classic implementation |
| Boost inductors | 3 | One per phase |
| DC bus capacitors | 2 (split bus) | Midpoint connected |

> [!tip] SiC Implementation
> Modern all-SiC Vienna designs (e.g., Microchip MSCSICPFC/REF5) use 6x SiC MOSFETs for the bidirectional switches plus 6x SiC Schottky barrier diodes, eliminating Si diode forward-voltage losses.

### Pros

- **Industry-proven at 30 kW**: Multiple reference designs exist (Microchip, ST, Wolfspeed) specifically at 30 kW
- **High efficiency**: 98.4--98.6% demonstrated at 30 kW with SiC (Microchip ref design at 140 kHz)
- **Three-level switching**: Reduced dv/dt per switching event, lower EMI filter requirements vs. two-level
- **Reduced device voltage stress**: Switches block only Vbus/2
- **Lower switching losses**: Due to half-voltage switching transitions
- **Simpler control than B6**: Only 3 PWM channels (one per phase), no shoot-through risk
- **Mature ecosystem**: Well-supported by TI C2000, ST STM32G4, Microchip dsPIC control platforms

### Cons

- **Unidirectional only**: Cannot support V2G (vehicle-to-grid) power flow
- **High diode count**: Always 2 diodes in the current conduction path, adding conduction losses
- **Fixed boost output**: Output voltage must exceed peak line-to-line voltage (Vbus > Vll_peak * ~1.05); for 530 VAC input, minimum bus ~785 V
- **No step-down capability**: Cannot produce bus voltage below the input peak

### Efficiency at 30 kW

- **98.6%** peak (Microchip MSCSICPFC/REF5, all-SiC, 140 kHz)
- **~98.4%** (ST STDES-VIENNARECT, SiC MOSFETs + STM32G4)
- **~98%** typical across 50--100% load range

### Control Complexity

**Medium.** Standard d-q frame current control or hysteresis/average current mode. Three independent duty cycles. No shoot-through possible (inherently safe). Well-documented control algorithms available in TI, ST, and Microchip application notes.

### Bidirectional (V2G)

**No.** The diode bridge prevents reverse power flow. A modified "active Vienna" with additional switches exists in literature but loses the simplicity advantage.

---

## 2. Six-Switch Active Bridge (B6 / 2-Level VSI as Active Rectifier)

### Operating Principle

The B6 topology is a conventional three-phase, two-level voltage-source inverter (VSI) operated as an active rectifier. It uses six active switches (3 half-bridges) with antiparallel diodes. By controlling the switches with sinusoidal PWM (SPWM) or space-vector modulation (SVM), the converter shapes the input current to be sinusoidal and in phase with the voltage. The same hardware can reverse power flow direction simply by changing the control phase angle, making it inherently bidirectional.

### Component Count

| Component | Quantity | Notes |
|-----------|----------|-------|
| Active switches (MOSFETs) | 6 | 3 half-bridge legs |
| Antiparallel diodes | 6 | Intrinsic body diodes of SiC MOSFETs often sufficient |
| Boost inductors | 3 | One per phase |
| DC bus capacitors | 1 (or 2 for midpoint) | Single bus voltage |

> [!note] SiC Advantage
> With SiC MOSFETs, the body diode has acceptable reverse recovery, so external antiparallel diodes can often be omitted, reducing component count to just 6 MOSFETs + 3 inductors + bus cap.

### Pros

- **Bidirectional power flow**: Natively supports V2G -- the same hardware works as inverter and rectifier
- **Lowest component count**: Only 6 switches, no additional diodes needed with SiC
- **Flexible control**: Full four-quadrant operation, reactive power compensation possible
- **Mature topology**: Standard three-phase inverter modules (e.g., Infineon EasyPACK, Wolfspeed WolfPACK) directly applicable
- **Lower conduction losses at high power**: Only one switch in the current path (vs. switch + 2 diodes in Vienna)
- **Semiconductor efficiency advantage**: At 30 kW with SiC, ~0.5--0.8% higher semiconductor efficiency vs. Vienna at low-medium switching frequencies (40--60 kHz)

### Cons

- **Two-level switching**: Full bus voltage (800 V) switched at each transition -- higher dv/dt, larger EMI filter needed
- **Shoot-through risk**: Complementary gate driving required with dead time; control firmware must be robust
- **Higher switching losses**: Each device blocks full Vbus (need 1200 V SiC exclusively; no 650 V option)
- **Larger EMI filter**: Common-mode voltage steps are 2x those of Vienna (800 V vs 400 V)
- **More complex control**: 6 PWM channels, dead-time management, requires current sensors on all 3 phases

### Efficiency at 30 kW

- **~98.0--98.5%** with SiC MOSFETs at 40--60 kHz switching frequency
- At higher frequencies (>80 kHz), efficiency drops faster than Vienna due to full-voltage switching
- **Conduction losses are lower** than Vienna (one device vs. three in path), but **switching losses are higher**
- Net result: roughly comparable to Vienna at 30 kW; can be slightly better or worse depending on frequency

### Control Complexity

**High.** Requires synchronous (d-q) frame current control, PLL for grid synchronization, dead-time compensation, and robust shoot-through protection. Six independent gate drives with precise timing. Standard FOC-like control well understood but more firmware effort than Vienna.

### Bidirectional (V2G)

**Yes.** This is the primary advantage. The same power stage operates as rectifier (grid-to-DC) or inverter (DC-to-grid) with only a control mode change. Required for V2G-capable chargers per ISO 15118-20.

---

## 3. Swiss Rectifier (Buck-Type 3-Phase PFC)

### Operating Principle

The Swiss rectifier is a three-phase buck-type PFC rectifier, conceptually a three-phase diode bridge feeding a multi-pulse buck converter with injection network. It uses a combination of low-frequency (line-commutated) thyristors or diodes for phase selection and high-frequency active switches for the buck stage. An injection network with bidirectional switches actively shapes the input current to achieve sinusoidal waveforms and unity power factor despite the buck-type operation.

### Component Count

| Component | Quantity | Notes |
|-----------|----------|-------|
| High-frequency active switches | 2 (buck stage) | Interleaved buck legs |
| Injection network switches | 6 (bidirectional, low-frequency) | Line-frequency commutated |
| Diodes | 12+ (bridge + freewheeling) | Significant diode count |
| Buck inductors | 2 | For interleaved output |
| DC bus capacitors | 1 | Output filter |

### Pros

- **Buck-type output**: Output voltage can be lower than input peak -- direct battery charging without intermediate DC-DC is theoretically possible
- **Direct start-up**: No pre-charge circuit needed (unlike boost topologies)
- **Output current limiting**: Inherent short-circuit protection capability
- **Very low common-mode noise**: The injection network provides a defined CM voltage path, significantly reducing CM EMI compared to boost topologies
- **Wide output voltage range**: Can regulate from near-zero to below input peak

### Cons

- **High component count**: 8+ active switches, 12+ diodes -- most complex power stage of the four options
- **Lower efficiency than boost types**: More semiconductor devices in conduction path; typically 96--97.5% at this power level
- **Unidirectional only**: Buck-type structure does not support reverse power flow
- **Complex control**: Multi-carrier PWM with sector-dependent modulation; injection network timing is non-trivial
- **Not mainstream for EV DC fast charging**: Very few commercial implementations or reference designs at 30 kW
- **Unnecessary for this application**: Since a DC-DC stage follows anyway, the buck output advantage is redundant -- the boost-type Vienna or B6 feeding an isolated DC-DC is more efficient overall

### Efficiency at 30 kW

- **96.5--97.5%** typical (lower than boost alternatives due to higher component count in conduction path)
- The efficiency penalty makes it difficult to meet the >98% PFC stage target

### Control Complexity

**Very High.** Sector-based modulation, injection network timing, current balancing between interleaved legs, and input current shaping all require sophisticated control. Less mature tool/library support compared to Vienna or B6.

### Bidirectional (V2G)

**No.** Buck-type topology is inherently unidirectional.

---

## 4. Two-Level VSI Used as Active Rectifier

> [!note] Topology Clarification
> This is essentially the same as the B6 topology described in Section 2. The "two-level VSI" and "6-switch active bridge (B6)" refer to the same converter structure. The distinction sometimes made is between using it as a dedicated rectifier (AFE -- Active Front End) vs. as a general-purpose bidirectional converter. The electrical topology, component count, and characteristics are identical. See Section 2 for full details.

For completeness, the key differentiator when specifically marketed as "2-level AFE" vs. "B6 bidirectional":

- **AFE mode**: Optimized control for unity PF rectification only; may use simpler DPWM (discontinuous PWM) to reduce switching losses by ~33%
- **Bidirectional mode**: Full four-quadrant control for both rectifier and inverter operation
- **DPWM1 modulation**: At full power, the 2L-VSI with DPWM1 achieves roughly equal losses to the Vienna rectifier while maintaining lower component count

---

## Comparison Summary

| Feature | Vienna Rectifier | B6 (6-Switch) | Swiss Rectifier | 2L-VSI/AFE |
|---------|-----------------|---------------|-----------------|------------|
| **Type** | 3-level boost | 2-level boost | Buck | 2-level boost |
| **Active switches** | 6 (3 bidir. cells) | 6 | 8+ | 6 |
| **Diodes** | 12 | 0--6 | 12+ | 0--6 |
| **Levels** | 3 | 2 | N/A | 2 |
| **Device voltage stress** | Vbus/2 (~400 V) | Vbus (~800 V) | Varies | Vbus (~800 V) |
| **Min. device rating** | 650 V possible | 1200 V required | Mixed | 1200 V required |
| **Efficiency (30 kW, SiC)** | 98.0--98.6% | 98.0--98.5% | 96.5--97.5% | 98.0--98.5% |
| **EMI filter size** | Smaller (3-level) | Larger (2-level) | Smallest (buck + injection) | Larger (2-level) |
| **Bidirectional (V2G)** | No | **Yes** | No | **Yes** |
| **Control complexity** | Medium | High | Very High | High |
| **Shoot-through risk** | None | Yes (dead time req.) | Partial | Yes (dead time req.) |
| **30 kW ref. designs** | Many (Microchip, ST, Wolfspeed) | Several (Infineon, Wolfspeed) | Very few | Same as B6 |
| **Commercial adoption** | **Dominant** | Growing (V2G) | Rare | Same as B6 |

---

## Commercial Reference Designs and Industry Adoption

### Vienna Rectifier -- The Industry Standard

The Vienna rectifier is the **most commonly used topology** in commercial 30 kW EV DC fast charger power modules today:

- **Microchip/Microsemi MSCSICPFC/REF5**: 30 kW, all-SiC (mSiC MOSFETs + SiC SBDs), 98.6% efficiency at 140 kHz. The most complete publicly available 30 kW Vienna reference design. ([Microchip Reference Design](https://www.microchip.com/en-us/tools-resources/reference-designs/vienna-3-phase-power-factor-correction-reference-design))

- **STMicroelectronics STDES-VIENNARECT**: 30 kW Vienna PFC with SiC MOSFETs and STM32G4 digital control. Full reference design with firmware. ([ST Product Page](https://www.st.com/en/evaluation-tools/stdes-viennarect.html))

- **Wolfspeed**: EV Charging Power Topologies Design Guidebook (PRD-08367) covers Vienna as a primary 3-phase PFC topology for DC fast charging. 30 kW DC-DC reference design (CRD-30DD12N-K) pairs with Vienna PFC front end. ([Wolfspeed Design Guidebook](https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_PRD-08367_EV_Charging_Power_Topologies_Design_Guidebook_Application_Note.pdf))

- **TI C2000**: Vienna rectifier reference design (TIDM-1022) with TMS320F28337xD, supporting up to 10 kW per phase. ([TI Reference](https://www.ti.com/lit/ug/tiducj0b/tiducj0b.pdf))

### B6 Topology -- For V2G Applications

- **Infineon CoolSiC**: Application notes show that for bidirectional (V2G) PFC, the B6 with CoolSiC MOSFETs has the lowest power loss and supports the highest switching frequency. For unidirectional-only, Infineon notes the Vienna hybrid (CoolSiC diode) has comparable losses at lower cost. ([Infineon Fast EV Charging](https://www.infineon.com/cms/en/applications/industrial/fast-ev-charging/chargers-from-30kw-to-150kw/))

- **Wolfspeed**: Bidirectional 6.6 kW OBC reference designs use B6 topology; principles scale to 30 kW for V2G DC fast chargers. ([Wolfspeed V2G Article](https://www.wolfspeed.com/knowledge-center/article/silicon-carbide-meets-power-v2g-demands-in-ev-fast-charger-market/))

---

## Recommendation for PDU Project

### If V2G is NOT required (unidirectional charger):

**Vienna Rectifier** is the clear choice.

- Best-in-class efficiency (98.5%+) at 30 kW with SiC
- Lowest risk: multiple proven reference designs at exactly this power level
- Simpler control, no shoot-through hazard
- Smaller EMI filter than two-level alternatives
- Lower semiconductor cost (can use 650 V devices in some configurations)

### If V2G IS required (bidirectional charger):

**B6 (6-Switch Active Bridge)** is the only practical choice among these four topologies.

- Only topology that natively supports bidirectional power flow
- Comparable efficiency to Vienna with SiC at 30 kW
- Standard three-phase power module packaging available
- Higher control complexity and EMI filter cost are acceptable trade-offs for V2G capability

### Swiss Rectifier:

**Not recommended** for this application. The buck-type advantage is negated by the downstream isolated DC-DC stage, and the efficiency penalty (~1--2% vs. Vienna) makes the >98% PFC target very difficult to achieve.

---

## Key References

1. [Microchip 30 kW Vienna PFC Reference Design (MSCSICPFC/REF5)](https://ww1.microchip.com/downloads/en/DeviceDoc/MSCSICPFC-REF5-3-Phase-30-kW-Vienna-PFC-Reference-Design-DS50002952A.pdf)
2. [ST 30 kW Vienna Rectifier PFC with SiC + STM32G4](https://www.st.com/content/dam/is22/document/pe2_02_jianjun_ni_30kw_sic_mosfet_vienna_rectifier_pfc_solution_with_stm32g4_ev_charger_en.pdf)
3. [Wolfspeed EV Charging Power Topologies Design Guidebook (PRD-08367)](https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_PRD-08367_EV_Charging_Power_Topologies_Design_Guidebook_Application_Note.pdf)
4. [TI SLUP417: Comparison of AC/DC Power-Conversion Topologies for Three-Phase](https://www.ti.com/lit/pdf/slup417)
5. [Infineon: SiC Devices Used in PFC for EV Charger Applications](https://www.infineon.com/dgdl/Infineon-SiC_Devices_Used_in_PFC_for_EV_Charger_Applications-Article-v01_00-EN.pdf?fileId=8ac78c8c80027ecd018040e8f07c7ff3)
6. [onsemi: Demystifying Three-Phase PFC Topologies](https://www.onsemi.com/site/pdf/H2PToday2102_design_ONSemi.pdf)
7. [Vincotech: Benchmarking Highly Efficient Three-Level PFC Topologies](https://www.vincotech.com/fileadmin/user_upload/content_media/documents/pdf/support-documents/technical-papers/Vincotech_TP_2016-05-001-v01_Benchmark_of_High_Efficient_Three-Level_PFC_Topologies.pdf)
8. [Swiss Rectifier -- IEEE (Soeiro et al., APEC 2012)](https://ieeexplore.ieee.org/document/6166192/)
