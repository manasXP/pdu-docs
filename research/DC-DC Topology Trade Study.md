---
tags: [pdu, dc-dc, topology, trade-study, SiC]
created: 2026-02-21
aliases: [DC-DC Converter Topology Comparison]
---

# Isolated DC-DC Converter Topology Trade Study

See also: [[3-Phase PFC Topology Selection]], [[Commercial Reference Designs Survey]]

> [!info] Context
> Second-stage DC-DC converter for a **30 kW EV DC fast charger power module**.
> - **Input:** ~700-800 VDC bus (from 3-phase Vienna rectifier / PFC stage)
> - **Output:** 150-1000 VDC, 0-100 A
> - **Charging modes:** CC/CV per IEC 61851
> - **Efficiency target:** >98% peak for the DC-DC stage
> - **Semiconductors:** SiC MOSFETs preferred (1200 V class)
>
> See [[__init]] for full PDU specifications.

---

## 1. The Wide-Output-Voltage Challenge

The 150-1000 VDC output range represents a **6.67:1 voltage ratio** -- one of the most demanding requirements in power converter design. This range is dictated by the need to charge everything from legacy 200 V packs (older Nissan Leaf, small city EVs) to modern 800 V architectures (Porsche Taycan, Hyundai Ioniq 5/6, Kia EV6).

### 1.1 Power Envelope

The charger operates in two distinct regions:

| Region | Voltage | Current | Power | Notes |
|--------|---------|---------|-------|-------|
| **Reduced power** | 150-300 V | 0-100 A | 0-30 kW | Current-limited at 100 A; power scales linearly with voltage |
| **Constant power** | 300-1000 V | 100-30 A | 30 kW | Full rated power; current decreases as voltage rises |

At 150 V / 100 A, the module delivers only 15 kW. The constant-power region (300-1000 V) is where the converter spends most of its operating life during a typical CCS charging session. Design optimization should therefore target the 400-850 V band for peak efficiency, while ensuring safe and stable operation down to 150 V.

### 1.2 Why Wide Range Is Hard for Resonant Converters

For an LLC or CLLC converter, the resonant tank is designed for optimal operation at a specific voltage gain (at or near the resonant frequency). Moving away from that point requires large frequency excursions:
- At 150 V output (with 800 V input, gain ~0.19), the converter must operate far above resonance -- switching losses rise, ZVS may be lost.
- At 1000 V output (gain ~1.25), operation is near or below resonance -- achievable but magnetizing current increases.

A **6.67:1 voltage gain range** would require a switching frequency span of roughly 2-3x (e.g., 100-300 kHz), which stresses magnetics, complicates EMI filtering, and degrades efficiency at the extremes.

---

## 2. Topology Comparison

### 2.1 LLC Resonant Converter

**Operating Principle:** A full-bridge (or half-bridge) inverter drives a resonant tank consisting of a series inductor (Lr), a parallel (magnetizing) inductor (Lm), and a series capacitor (Cr), coupled through a high-frequency transformer. Output is rectified by diodes (or synchronous rectifiers). Voltage regulation is achieved by varying switching frequency around the resonant frequency.

**Component Count:**
- Primary: 4 SiC MOSFETs (full-bridge) or 2 (half-bridge)
- Secondary: 4 rectifier diodes (or SiC Schottky diodes / sync-rect MOSFETs)
- Resonant tank: Lr, Lm (often integrated into transformer), Cr
- 1 high-frequency transformer
- Output filter capacitor (no output inductor needed)

**Wide Output Range (150-1000 V):**
- Fundamental limitation for this application. The LLC is optimized for operation near the resonant frequency (fr), where gain = n (turns ratio).
- Covering 150-1000 V from an 800 V bus requires gain range of ~0.19 to 1.25 (assuming n:1 turns ratio optimized for ~800 V output). This demands very wide frequency variation (e.g., 135-250 kHz per the Wolfspeed CRD30DD12N reference).
- At low output voltages (150-300 V), the converter operates far above resonance; efficiency drops and ZCS on secondary is lost.
- Interleaving (3-phase interleaved LLC) helps distribute thermal stress and reduce output ripple but does not fundamentally solve the gain range issue.

**Efficiency Profile:**
- Exceptional at the resonant point: >98.5% demonstrated
- Degrades at extremes of voltage/load range
- Wolfspeed CRD30DD12N achieves >98% peak efficiency over 200-1000 V range using 3-phase interleaving

**Soft Switching:**
- Primary side: ZVS across most of the operating range (ensured by magnetizing current)
- Secondary side: ZCS at and below resonant frequency
- ZVS can be lost at very light loads or at operating points far above resonance

**Control Complexity:** Moderate
- Frequency modulation (FM) is the primary control variable
- Advanced designs add burst mode (for light load) and hybrid FM + PWM modulation
- No inherent current-limiting; CC mode requires an outer current loop adjusting frequency

**Bidirectional Capability:** Not inherently bidirectional. Requires replacing secondary diodes with active switches and additional control modes (becomes a CLLC -- see Section 2.4).

**Pros for 30 kW EV Charging:**
- Highest peak efficiency of any topology considered
- Wolfspeed has a production-proven 30 kW reference design (CRD30DD12N-K)
- ST Microelectronics offers a complete 30 kW LLC solution (STDES-30KWLLC) with STM32G4 control
- No output inductor simplifies magnetics and reduces volume
- Sinusoidal resonant currents reduce EMI

**Cons for 30 kW EV Charging:**
- Wide frequency range (135-250+ kHz) makes magnetics and EMI filter design challenging
- Efficiency degrades below ~300 V output
- Not bidirectional (no V2G without topology change)
- Resonant tank sensitivity to component tolerances
- Load must be carefully considered during resonant tank design

---

### 2.2 Phase-Shifted Full Bridge (PSFB)

**Operating Principle:** A full-bridge inverter on the primary drives a transformer using fixed-frequency PWM. Voltage regulation is achieved by phase-shifting the switching of the two bridge legs relative to each other. The secondary uses a center-tapped or full-bridge rectifier with an output inductor.

**Component Count:**
- Primary: 4 SiC MOSFETs
- Secondary: 2 diodes (center-tap) or 4 diodes (full-bridge rectifier), or synchronous rectifiers
- 1 transformer + 1 external or leakage inductor (for ZVS)
- 1 output inductor (required -- significant component)
- Output filter capacitor
- Often requires a clamp circuit for secondary voltage ringing

**Wide Output Range (150-1000 V):**
- Handles wide voltage range through duty cycle (phase shift) control -- inherently better than LLC for variable-ratio applications
- Reconfigurable PSFB variants with switchable transformer taps or dual secondaries can extend the efficient operating range
- At low output voltages, the effective duty cycle is very small, and ZVS may be lost on the lagging leg

**Efficiency Profile:**
- Good but not class-leading: typically 96-97% peak at 30 kW class
- Efficiency degrades at light load and low output voltage due to circulating currents and hard switching on the lagging leg
- The output inductor adds copper and core losses not present in resonant topologies
- A 10 kW SiC prototype demonstrated 96.69% efficiency at full load (900 V in, 800 V out)

**Soft Switching:**
- Leading leg: ZVS achieved across most of the load range
- Lagging leg: ZVS only at medium-to-high loads; lost at light load due to insufficient energy stored in the leakage inductor
- Secondary diodes: Hard-switched (reverse recovery is a concern with Si diodes; SiC Schottky diodes eliminate this)
- Various ZVS extension techniques exist (auxiliary circuits, wide-range ZVS clamps) but add complexity

**Control Complexity:** Low to Moderate
- Fixed-frequency PWM -- simplest control of all topologies considered
- Phase-shift control is well understood with decades of application history
- CC/CV modes are straightforward to implement with standard control loops
- Fixed frequency simplifies EMI filter design

**Bidirectional Capability:** Not inherently bidirectional. The output inductor and rectifier structure must be redesigned for reverse power flow.

**Pros for 30 kW EV Charging:**
- Mature, well-understood topology with extensive literature
- Fixed-frequency operation simplifies EMI compliance
- Handles wide output voltage range through phase-shift duty cycle
- Straightforward CC/CV control implementation
- Abundant IC support (UCC28950, LTC3722, etc.)

**Cons for 30 kW EV Charging:**
- Lower peak efficiency than resonant topologies (~96-97% vs. >98%)
- Output inductor is bulky and lossy at 30 kW / high frequency
- Secondary voltage stress: Ringing voltages can reach 2-3x the output voltage, particularly problematic at 1000 V output (requires 1700 V rated secondary devices or complex clamp circuits)
- ZVS loss on lagging leg at light load
- Not bidirectional
- Circulating current during freewheeling intervals reduces efficiency

---

### 2.3 Dual Active Bridge (DAB)

**Operating Principle:** Two full-bridge converters (primary and secondary) are coupled through a high-frequency transformer with a series inductor (leakage or external). Power transfer is controlled by the phase shift between the two bridges. The inductor current is shaped by the voltage difference applied by the two bridges.

**Component Count:**
- Primary: 4 SiC MOSFETs (1200 V class)
- Secondary: 4 SiC MOSFETs (1200 V class for 1000 V output)
- 1 high-frequency transformer
- 1 series inductor (may be integrated as transformer leakage)
- Output filter capacitor (no output inductor needed)
- **Total: 8 active switches** -- highest switch count

**Wide Output Range (150-1000 V):**
- Handles the full 150-1000 V range more naturally than LLC
- Phase-shift control provides continuous voltage regulation
- However, at voltage ratios far from the transformer turns ratio (e.g., 800 V in / 150 V out), circulating reactive currents increase significantly, degrading efficiency
- Advanced modulation (dual-phase-shift, triple-phase-shift) can optimize operation across the full range
- Variable switching frequency + phase shift gives an additional control degree of freedom

**Efficiency Profile:**
- Peak efficiency ~98-98.5% achievable with SiC at the design point (matched voltage ratio)
- onsemi describes DAB-ZVT as providing "stable high efficiency across a wide output voltage range"
- At 800 V input / 500 V output, reference designs report 98.4% peak
- Efficiency drops at voltage ratios far from n:1 (turns ratio) due to reactive circulating currents
- Advanced TPS (triple-phase-shift) modulation recovers some of this loss by minimizing RMS currents

**Soft Switching:**
- ZVS achievable on all 8 switches under favorable conditions
- At light load: ZVS can be lost -- requires advanced modulation (DPS/TPS) or variable frequency to maintain
- The SiC MOSFET body diode has very low reverse recovery, which helps maintain ZVS transition quality
- Full ZVS range is a strong function of modulation strategy; simple SPS (single-phase-shift) has the narrowest ZVS range

**Control Complexity:** High
- Single-phase-shift (SPS) control is simple but inefficient at wide voltage ratios
- Dual-phase-shift (DPS) and triple-phase-shift (TPS) required for optimized operation -- significantly more complex
- Real-time optimization of phase shifts for ZVS + minimum RMS current is computationally demanding
- Requires sophisticated digital control (DSP/MCU with fast ADC and high-resolution PWM)
- STM32G4, TMS320F280x, or dsPIC33 class controllers typically used

**Bidirectional Capability:** **Natively bidirectional** -- the defining advantage. Reverse power flow is achieved simply by reversing the phase-shift direction. No hardware changes needed for V2G operation.

**Pros for 30 kW EV Charging:**
- Native bidirectionality for V2G / vehicle-to-home (V2H) applications
- Wide output voltage capability with phase-shift control
- ZVS on all switches (with proper modulation)
- No output inductor -- compact design
- Easily paralleled and stacked for higher power
- Tighter EMI spectrum than variable-frequency topologies (can use fixed or narrow-band frequency)
- Actively promoted by onsemi, TI (TIDA-010054), and ST (25 kW DAB reference)

**Cons for 30 kW EV Charging:**
- 8 active switches (highest BOM cost for semiconductors)
- Complex control algorithms (TPS modulation, ZVS boundary tracking)
- High circulating currents at extreme voltage ratios (150 V output from 800 V bus)
- Transformer design must handle bidirectional flux -- no DC bias allowed
- Gate driver count doubled vs. LLC with diode rectification

---

### 2.4 CLLC Resonant Converter

**Operating Principle:** A symmetric variant of the LLC converter with resonant elements on both sides of the transformer: Lr1-Cr1 on the primary, Lr2-Cr2 on the secondary, with Lm as the magnetizing inductance. Both sides use full-bridge active switches. In the forward direction, it behaves like an LLC; in reverse, the secondary-side resonant elements ensure similar resonant behavior.

**Component Count:**
- Primary: 4 SiC MOSFETs (1200 V)
- Secondary: 4 SiC MOSFETs (1200 V)
- Resonant tank: Lr1, Cr1, Lm, Lr2, Cr2 (5 resonant elements)
- 1 high-frequency transformer
- Output filter capacitor
- **Total: 8 active switches + more complex resonant tank than LLC**

**Wide Output Range (150-1000 V):**
- Same fundamental frequency-modulation limitation as LLC for gain range
- The symmetric resonant tank helps maintain ZVS over a wider range than asymmetric LLC in bidirectional mode
- For the forward (charging) direction, the voltage gain range challenge is essentially the same as LLC
- Hybrid modulation (frequency + phase shift) can extend the useful range
- Wolfspeed CRD-22DD12N (22 kW bidirectional) demonstrates the approach at a slightly lower power level

**Efficiency Profile:**
- Similar to LLC in forward mode: >98% peak at optimal operating point
- Symmetric tank design means reverse-mode efficiency is comparable to forward mode (unlike LLC which suffers in reverse)
- Efficiency degrades at voltage extremes, same as LLC
- Maintains ZVS over a wider operating range than DAB (per simulation studies)

**Soft Switching:**
- ZVS on all primary switches (ensured by magnetizing current, as in LLC)
- ZCS on secondary diodes at/below resonance (in forward mode)
- In bidirectional mode, ZVS can be maintained on all 8 switches with proper design
- Wider natural ZVS range compared to DAB without requiring complex modulation

**Control Complexity:** High
- Frequency modulation for forward mode (similar to LLC)
- Requires different control strategies for forward vs. reverse operation
- Optimal triple-phase-shift (TPS) modulation proposed for full operating range
- Accurate modeling of the 5-element resonant tank is more complex than LLC or DAB
- Fixed-frequency operation possible with auxiliary LC networks but adds components

**Bidirectional Capability:** **Natively bidirectional** -- the primary motivation for CLLC over LLC. Symmetric resonant tank ensures comparable performance in both directions.

**Pros for 30 kW EV Charging:**
- Bidirectional with symmetric performance (V2G capable)
- Higher peak efficiency than DAB at matched operating points
- Wider natural ZVS range than DAB
- Reduced EMI due to sinusoidal resonant currents
- No output inductor

**Cons for 30 kW EV Charging:**
- 8 active switches + more resonant components than any other topology
- Same wide-frequency limitation as LLC for the 150-1000 V range
- More complex resonant tank design (5 elements to optimize)
- Less mature in commercial 30 kW off-board charger designs (more common in 6.6-22 kW OBCs)
- Control complexity is the highest of all topologies considered

---

### 2.5 Series Resonant Converter (SRC)

**Operating Principle:** A full-bridge inverter drives a series LC resonant tank through a transformer. Unlike LLC, there is no parallel (magnetizing) inductance in the resonant network. The series Lr-Cr tank acts as a bandpass filter; output voltage is regulated by varying switching frequency relative to the resonant frequency.

**Component Count:**
- Primary: 4 SiC MOSFETs (full-bridge)
- Secondary: 4 diodes (or synchronous rectifiers)
- Resonant tank: Lr, Cr only (simplest tank of all resonant topologies)
- 1 high-frequency transformer
- Output filter capacitor

**Wide Output Range (150-1000 V):**
- DC voltage gain is always less than 1 (subunity) -- the SRC can only step down from the reflected input voltage
- Cannot boost; this limits flexibility at high output voltages unless the turns ratio is chosen to accommodate 1000 V, which means very poor efficiency at 150 V
- Gain range limitation makes it poorly suited for the full 150-1000 V range as a standalone converter

**Efficiency Profile:**
- High efficiency at the resonant frequency (comparable to LLC)
- Efficiency degrades rapidly away from resonance
- Light-load regulation is problematic: at no load, the output voltage cannot be regulated (frequency must go to infinity)
- Not well-suited for battery charging where load varies from 0 to 100%

**Soft Switching:**
- Above resonance: ZVS on primary switches, but turn-off losses remain
- Below resonance: ZCS on primary switches, but can cause audible noise
- Secondary diodes: Natural ZCS near resonance

**Control Complexity:** Low to Moderate
- Simple frequency control
- But inability to regulate at no-load is a fundamental limitation requiring additional circuits or topology modifications

**Bidirectional Capability:** Can be made bidirectional with active secondary (DAB-SRC variant), but the gain limitation persists in both directions.

**Pros for 30 kW EV Charging:**
- Simplest resonant tank (fewer components than LLC or CLLC)
- Current-source behavior suits CC charging mode
- Good short-circuit tolerance (inherent current limiting)

**Cons for 30 kW EV Charging:**
- Subunity gain makes it unsuitable for the full 150-1000 V range
- Cannot regulate at no-load or very light loads
- Efficiency degrades sharply away from resonance
- Rarely used as a standalone topology in modern EV chargers
- Generally considered inferior to LLC for this application class

---

## 3. Summary Comparison Table

| Parameter | LLC | PSFB | DAB | CLLC | SRC |
|-----------|-----|------|-----|------|-----|
| **Primary switches** | 4 | 4 | 4 | 4 | 4 |
| **Secondary devices** | 4 diodes | 4 diodes | 4 MOSFETs | 4 MOSFETs | 4 diodes |
| **Resonant elements** | Lr, Lm, Cr | Leakage L only | Series L only | Lr1, Cr1, Lm, Lr2, Cr2 | Lr, Cr |
| **Output inductor** | No | **Yes** (bulky) | No | No | No |
| **Peak efficiency** | >98.5% | ~96-97% | ~98-98.5% | >98% | ~97-98% |
| **Wide-V efficiency** | Degrades below 300 V | Moderate | Good with TPS | Same as LLC | Poor |
| **ZVS range** | Good (primary) | Partial (lagging leg) | Full (with TPS) | Widest | Partial |
| **Control complexity** | Moderate | Low | High | Highest | Low |
| **Bidirectional** | No | No | **Yes** | **Yes** | No (without mods) |
| **V2G ready** | No | No | **Yes** | **Yes** | No |
| **Fixed frequency** | No (FM control) | **Yes** | Yes (or hybrid) | No (FM control) | No |
| **EMI friendliness** | Moderate (FM) | **Best** (fixed f) | Good | Moderate (FM) | Moderate |
| **Commercial maturity (30 kW off-board)** | **Highest** | High | Growing | Low-Medium | Low |
| **BOM cost** | Lowest | Low-Medium | Highest | High | Low |

---

## 4. Single-Stage vs. Two-Stage DC-DC Architecture

### 4.1 Single-Stage Approach

A single isolated DC-DC stage covers the full 150-1000 V output range directly from the ~800 V PFC bus. This is the most common commercial approach for 30 kW modules.

**Advantages:**
- Fewer components, lower cost, smaller size
- Higher overall efficiency (no cascaded losses)
- Simpler thermal management

**Disadvantages:**
- The DC-DC converter must handle the full 6.67:1 voltage range
- Resonant converters (LLC, CLLC) suffer efficiency degradation at low output voltages
- Transformer and magnetics must be designed for worst-case (lowest voltage / highest current)

### 4.2 Two-Stage Cascaded Approach

A fixed-ratio isolated DC-DC converter (DCX) is followed by a non-isolated buck or buck-boost stage for fine regulation.

**Example architecture** (from recent IEEE publications):
- **Stage 1:** LLC converter operating at fixed resonant frequency (maximum efficiency ~99%) with dual secondary windings, providing an intermediate bus
- **Stage 2:** Interleaved buck converter for voltage regulation (150-1000 V)
- **Reconfiguration switches:** 3 auxiliary switches change the series/parallel connection of LLC secondaries to extend the effective range

**Advantages:**
- The LLC always operates at resonance (peak efficiency, minimal stress)
- The buck stage handles the wide voltage range efficiently
- Total efficiency can be higher than a single wide-range LLC: e.g., 99% (LLC) x 99% (buck) = 98% system
- Each stage is simpler to design and control independently

**Disadvantages:**
- More components overall (two power stages + reconfiguration switches)
- Increased board area and cost
- Reliability: more components = more failure modes
- Additional control coordination between stages

### 4.3 Recommendation

For a **commercial 30 kW module targeting 150-1000 V**, the single-stage approach dominates the market because:
1. The constant-power region (300-1000 V) is where >90% of charging energy is delivered
2. Operation at 150-300 V is infrequent and power-derated anyway (current-limited, not power-limited)
3. A well-designed interleaved LLC or DAB can achieve >97% efficiency even at 200 V output
4. Cost and size constraints of a modular charger favor fewer stages

The two-stage approach is worth considering only if the specification absolutely demands >98% efficiency across the entire 150-1000 V range, including the low-voltage region.

---

## 5. What Commercial Modules Actually Use

### 5.1 Wolfspeed -- 3-Phase Interleaved LLC

**Reference design:** [CRD30DD12N-K](https://www.wolfspeed.com/products/power/reference-designs/crd30dd12n-k/)
- **Topology:** 3-phase interleaved LLC resonant converter
- **Power:** 30 kW
- **Input:** 650-850 VDC (from Vienna rectifier PFC)
- **Output:** 200-1000 VDC
- **Switching frequency:** 135-250 kHz
- **Peak efficiency:** >98%
- **Power density:** 6.5 kW/L
- **Semiconductors:** 1200 V C3M SiC MOSFETs (primary), 650 V C6D SiC Schottky diodes (secondary)
- **Controller:** Digital (DSP/MCU based)

Wolfspeed also offers a 60 kW variant (CRD-60DD12N-K) and a **22 kW bidirectional CLLC** (CRD-22DD12N) for applications requiring V2G.

### 5.2 STMicroelectronics -- 3-Phase LLC

**Reference design:** STDES-30KWLLC (presented at APEC 2024)
- **Topology:** 3-phase interleaved LLC
- **Power:** 30 kW
- **Input:** 650-850 VDC
- **Output:** 200-1000 VDC
- **Switching frequency:** 100-300 kHz
- **Peak efficiency:** >98%
- **Semiconductors:** Gen 3 SiC MOSFETs, STGAP2SIC gate drivers
- **Controller:** STM32G474 (Cortex-M4 with high-resolution timer)
- **Paired PFC stage:** STDES-30KWVRECT (Vienna rectifier)

### 5.3 onsemi -- DAB-ZVT

onsemi actively promotes the **DAB-ZVT (Dual Active Bridge with Zero-Voltage Transition)** topology for DC fast chargers, describing it as "one of the most versatile and suitable alternative solutions for DCFC." Their solution emphasizes:
- Stable high efficiency across wide output voltage range
- Native bidirectionality for V2G
- Easier paralleling and stacking than LLC
- Tighter EMI spectrum (fixed or narrow-band frequency)

### 5.4 Texas Instruments -- DAB

**Reference design:** [TIDA-010054](https://www.ti.com/lit/ug/tidues0e/tidues0e.pdf)
- **Topology:** Bidirectional Dual Active Bridge
- **Targets:** EV charging and battery energy storage systems
- **Controller:** C2000 real-time MCU family
- **Emphasis:** Bidirectional operation, SiC integration

### 5.5 Infineon / Arrow -- SiC CoolSiC Easy Modules

Arrow Electronics developed a **30 kW DC fast charger reference platform** using Infineon CoolSiC 1200 V Easy power modules. The platform supports bidirectional charging and uses modular power block architecture.

### 5.6 Vincotech -- Power Modules for EV Charging

Vincotech provides flow-type power modules (pre-packaged half-bridge and full-bridge SiC modules) targeting 20-60 kW charger building blocks. Their modules are topology-agnostic, used in both LLC and DAB implementations by system integrators.

---

## 6. Industry Trend Summary

The market is bifurcating into two camps:

**Camp 1: LLC (unidirectional, highest efficiency)**
- Wolfspeed, STMicroelectronics
- Interleaved LLC is the proven workhorse for 30 kW off-board charger modules
- Optimized for the 200-1000 V range with >98% peak efficiency
- Best for cost-optimized, unidirectional charger deployments (majority of current installations)

**Camp 2: DAB / CLLC (bidirectional, V2G-ready)**
- onsemi, TI, Infineon/Arrow
- Growing rapidly as V2G standards (ISO 15118-20) mature
- Slightly higher BOM cost (8 active switches) offset by future-proofing
- DAB preferred for off-board (control maturity); CLLC preferred for on-board (smaller magnetics at 6.6-22 kW)

---

## 7. Design Recommendation for This PDU

> [!tip] Recommended Topology

**For a 30 kW module without V2G requirement:** 3-phase interleaved LLC resonant converter, following the Wolfspeed CRD30DD12N-K architecture. This gives:
- Proven >98% peak efficiency
- Mature control and reference designs available
- Lowest active component count (SiC Schottky diode rectification)
- 6.5 kW/L power density demonstrated

**If V2G / bidirectional operation is required:** Dual Active Bridge (DAB) with SiC MOSFETs on both sides, using triple-phase-shift (TPS) modulation. Accept the higher control complexity and semiconductor cost for the benefit of full bidirectionality and inherent wide-voltage capability.

**Not recommended:**
- PSFB -- efficiency penalty at this power level; output inductor adds bulk
- SRC -- gain limitation makes it unsuitable for 150-1000 V
- CLLC for off-board -- less mature than DAB at 30 kW; better suited for on-board chargers

### Key Design Decisions Still Needed

1. **Turns ratio selection** -- optimize for the 400-800 V constant-power band
2. **Interleaving** -- 2-phase vs. 3-phase (3-phase preferred for 30 kW per Wolfspeed/ST)
3. **Switching frequency** -- 100-200 kHz target range for SiC; higher enables smaller magnetics but increases switching losses
4. **Transformer construction** -- planar vs. wound; consider integrated magnetics (Lr + Lm in one core)
5. **Thermal management** -- forced-air vs. cold-plate; ties into power density target
6. **Digital controller selection** -- STM32G4, TMS320F280x, or dsPIC33CK

---

## References and Further Reading

- [Wolfspeed CRD30DD12N-K 30 kW Interleaved LLC Reference Design](https://www.wolfspeed.com/products/power/reference-designs/crd30dd12n-k/)
- [Wolfspeed EV Charging Power Topologies Design Guidebook (PRD-08367)](https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_PRD-08367_EV_Charging_Power_Topologies_Design_Guidebook_Application_Note.pdf)
- [Wolfspeed CRD-22DD12N 22 kW Bidirectional CLLC Reference Design](https://www.wolfspeed.com/products/power/reference-designs/crd-22dd12n/)
- [onsemi: DC Fast EV Charging -- Common System Topologies and Power Devices](https://www.onsemi.com/company/news-media/blog/automotive/en-us/dc-fast-ev-charging-common-system-topologies-and-power-devices)
- [ST 30 kW SiC MOSFET DC-DC with STM32G4 (APEC 2024)](https://www.st.com/content/dam/static-page/events/apec-2024/demo-apec-24-30kw-dc-dc.pdf)
- [TI TIDA-010054 Bidirectional DAB Reference Design](https://www.ti.com/lit/ug/tidues0e/tidues0e.pdf)
- [Arrow 30 kW DC Fast Charger Reference Platform (Infineon CoolSiC)](https://evtechinsider.com/arrow-electronics-unveils-new-30kw-dc-fast-charger-reference-platform-using-infineon-power-modules/)
- [Infineon EV Charging Solutions (30-150 kW)](https://www.infineon.com/cms/en/applications/industrial/ev-charging/chargers-from-30kw-to-150kw/)
- [EDN: CLLLC vs. DAB for EV Onboard Chargers](https://www.edn.com/power-tips-102-clllc-vs-dab-for-ev-onboard-chargers/)
- [IEEE: Design of an Isolated DC/DC Topology with High Efficiency >97% for EV Fast Chargers](https://ieeexplore.ieee.org/document/8880520/)
- [Reconfigurable Two-Stage 11 kW DC-DC for 150-1000 V Output](https://www.researchgate.net/publication/370996365/)
- [50 kW Two-Stage Converter for Wide Output 150-1000 V](https://www.researchgate.net/publication/389230716/)
- [ScienceDirect: Review on Classification of Resonant Converters for EV Application](https://www.sciencedirect.com/science/article/pii/S2352484721014517)
