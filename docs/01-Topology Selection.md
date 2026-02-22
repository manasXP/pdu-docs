---
tags: [PDU, topology, design-decision, SiC, EV-charging]
created: 2026-02-21
status: approved
---

# Topology Selection — 30 kW PDU for DC Fast Charging

> [!summary] Decision
> **Vienna Rectifier (PFC) + 3-Phase Interleaved LLC Resonant (DC-DC)**
> Unidirectional, all-SiC, single STM32G4 controller. Reference baseline: ST STDES-30KWVRECT + STDES-30KWLLC.

## 1. Design Requirements

From [[__init]]:

| Parameter | Specification |
|-----------|--------------|
| Input voltage | 260–530 VAC, 3-phase + PE |
| Input current | ≤60 A per module |
| Input frequency | 45–65 Hz |
| Power factor | ≥0.99 |
| THDi | ≤5% at full load |
| Output voltage | 150–1000 VDC |
| Output current | 0–100 A |
| Rated power | 30 kW (constant power 300–1000 VDC) |
| Peak efficiency | >96% (target >97% with SiC) |
| Voltage accuracy | ±0.5% |
| Current accuracy | ±1% |
| Output ripple | <0.5% RMS |
| Soft start | ≤6 s |
| Stacking | 5 modules via CAN bus, ≤5% current imbalance |
| Dimensions | ~455 × 300 × 94 mm (~17 kg) |
| Cooling | Forced air, ≤65 dB |
| Temperature | −30°C to +55°C full load |
| Standards | IEC 61851-23, UL 2202, CE |
| Power flow | **Unidirectional** (grid-to-vehicle only) |

## 2. Architecture Overview

```
3φ AC ──► EMI Filter ──► Vienna Rectifier (PFC) ──► DC Bus (700-920V) ──► 3-Phase Interleaved LLC ──► DC Output
  260-530V              PF≥0.99, THD≤5%              ±1% regulated               ZVS/ZCS              150-1000V
                        η > 98.5%                                                  η > 98%              0-100A
                                                                                                        30 kW
                        ┌────────────────────────────────────────────────────────────────┐
│              STM32G474RE (single controller)                   │
│  PFC loop ─── DC bus regulation ─── LLC freq control ─── CC/CV |  
│                                                                | └────────────────────────────────────────────────────────────────┘
                                            │
                                         CAN bus ──► Module stacking / OCPP interface
```

## 3. PFC Stage — Vienna Rectifier

### 3.1 Why Vienna

See [[3-Phase PFC Topology Selection]] for the full trade study. Summary:

| Topology | Efficiency | Switches | Bidirectional | EMI | Risk |
|----------|-----------|----------|---------------|-----|------|
| **Vienna Rectifier** | **98.0–98.6%** | 6 MOSFETs + 12 diodes | No | Low (3-level) | **Lowest** |
| B6 Active Bridge | 98.0–98.5% | 6 MOSFETs | Yes | Higher (2-level) | Low |
| Swiss Rectifier | 96.5–97.5% | 8+ switches + 12+ diodes | No | Lowest | High |
| Two-Level VSI | 98.0–98.5% | 6 MOSFETs | Yes | Higher (2-level) | Low |

**Decision: Vienna Rectifier.** Bidirectional capability is not required, so the Vienna's 3-level switching advantage (lower EMI filter size, lower dV/dt stress, simpler control) makes it the clear choice. It is the most widely adopted topology for unidirectional 30 kW EV charger modules — every major SiC vendor offers a reference design around it.

### 3.2 Operating Principle

The Vienna rectifier is a 3-phase, 3-level boost-type PFC. Each phase uses a bidirectional switch cell (two back-to-back MOSFETs or a MOSFET + diode bridge) that connects the phase to the DC bus midpoint. The output is a split DC bus (two series capacitors). Three-level switching means each device only blocks half the bus voltage (~400 V instead of ~800 V), enabling use of lower-voltage, lower-Rdson SiC devices or reducing switching losses with 1200 V parts.

### 3.3 Key Specifications

| Parameter | Value |
|-----------|-------|
| Topology | 3-phase Vienna rectifier (boost-type, 3-level) |
| DC bus voltage | 700–920 VDC (regulated, split ±350–460 V) |
| SiC MOSFETs | SCTWA90N65G2V-4 (650 V, Gen 2 SiC, ST) |
| SiC diodes | STPSC40H12C (1200 V, 40 A SiC Schottky, ST) |
| Gate driver | STGAP2SiC (isolated, SiC-optimized) |
| Switching frequency | 48–65 kHz (per switch cell) |
| Effective ripple frequency | 96–130 kHz (3-level doubling) |
| Peak efficiency | >98.55% (measured on STDES-30KWVRECT) |
| Control | Digital — STM32G474RE |
| Firmware | STSW-30KWVRECT (ST-provided) |

### 3.4 Design Considerations

- **Input EMI filter:** 3-level switching significantly reduces differential-mode noise. A two-stage LC filter should suffice for EN 55032 Class B compliance. Size reduction vs. 2-level is ~30–40%.
- **DC bus capacitors:** Split bus requires midpoint balancing. Electrolytic + film hybrid recommended for ripple current handling and life.
- **Inrush limiting:** Pre-charge relay or NTC required. Soft-start firmware handles controlled ramp to rated bus voltage in ≤6 s.
- **Bus voltage setpoint:** Nominally 800 VDC for max headroom. Can be actively adjusted (700–920 V) by the controller to optimize LLC operating point at different output voltages. The upper limit of 920 V ensures ZVS is maintained at 1000 V output (see [[03-LLC Gain Curve Verification]]).

## 4. DC-DC Stage — 3-Phase Interleaved LLC Resonant Converter

### 4.1 Why Interleaved LLC

See [[DC-DC Topology Trade Study]] for the full trade study. Summary:

| Topology | Peak Eff. | Wide Vout | Soft Switching | Bidirectional | Complexity |
|----------|----------|-----------|----------------|---------------|------------|
| **3-Ph Interleaved LLC** | **>98%** | Adequate | ZVS + ZCS | No | Medium |
| Dual Active Bridge (DAB) | 97–98% | Best | ZVS (with TPS) | Yes | High |
| CLLC Resonant | 97–98% | Adequate | ZVS both sides | Yes | High |
| Phase-Shifted Full Bridge | 96–97% | Good | ZVS primary only | No | Low |
| Series Resonant (SRC) | — | Poor | — | No | — |

**Decision: 3-Phase Interleaved LLC.** Highest efficiency, proven at 30 kW, and the 3-phase interleaving provides critical benefits:
- Input/output ripple current reduced by ~3× (meets <0.5% RMS ripple spec)
- Each phase handles only 10 kW → smaller magnetics per phase
- 120° phase offset enables continuous power delivery
- Fault tolerance — system can derate to 20 kW on two phases if one fails

### 4.2 Operating Principle

Three LLC half-bridge cells operate in parallel with 120° phase offset. Each cell consists of a half-bridge (2 SiC MOSFETs), a resonant tank (Lr, Lm, Cr), and a high-frequency transformer with secondary rectification (SiC Schottky diodes). Voltage regulation is achieved by varying switching frequency around the resonant frequency (fr). At fr, the converter achieves unity gain and peak efficiency with ZVS on the primary and ZCS on the secondary.

### 4.3 Key Specifications

| Parameter | Value |
|-----------|-------|
| Topology | 3-phase interleaved LLC half-bridge |
| Phases | 3 (120° offset, 10 kW each) |
| Input | 650–920 VDC (from Vienna PFC bus) |
| Output | 200–1000 VDC |
| Output current | 0–100 A |
| SiC MOSFETs (primary) | 1200 V, 25–40 mΩ class (ST Gen 3 or Wolfspeed C3M0040120K) |
| Rectifier diodes (secondary) | 650 V SiC Schottky (for ≤500 V output) + 1200 V SiC Schottky (for >500 V) |
| Gate driver | STGAP2SiC |
| Switching frequency | 100–300 kHz (adaptive) |
| Resonant frequency | ~150 kHz (design target) |
| Peak efficiency | >98% |
| Transformer | Planar or litz-wire, 3 separate cores |
| Control | Frequency modulation + burst mode at light load |

### 4.4 Wide Output Voltage Strategy

The 150–1000 VDC output range (6.7:1 ratio) is the primary design challenge. Strategy:

**300–1000 VDC (constant power region, 30 kW):**
- LLC operates near resonance with frequency modulation
- DC bus voltage actively adjusted by PFC (700–920 V) to keep LLC gain close to unity
- At 1000 V output, Vbus raised to 920 V → M = 1.09, maintaining ZVS (see [[03-LLC Gain Curve Verification]])
- Transformer turns ratio optimized for ~800 V in / ~600 V out (mid-range)
- Efficiency remains >97.5% across this range

**150–300 VDC (reduced power region, current-limited at 100 A → 15–30 kW):**
- LLC operates at higher frequency (above resonance, below-unity gain)
- Efficiency degrades to ~95–96% but this is acceptable because:
  - Power is derated (not 30 kW)
  - <5% of real-world charging sessions operate here (legacy 200–400 V EVs at low SoC)
  - Thermal stress is lower due to reduced power

**Alternative considered:** Series/parallel secondary reconfiguration (as in Wolfspeed CRD30DD12N-K) could extend high-efficiency range but adds relays, complexity, and a brief interruption during switchover. Not recommended for initial design; can be added in Rev 2 if field data shows significant time spent below 300 V.

### 4.5 Design Considerations

- **Resonant tank design:** Lr, Cr, Lm ratios set the gain curve shape. Target Ln (= Lm/Lr) ≈ 5–7 for a good balance between gain range and circulating current.
- **Transformer:** Three separate planar transformers (one per phase). Interleaved windings to minimize leakage. Lr can be integrated as transformer leakage inductance to save a discrete inductor.
- **Synchronous rectification:** Optional — SiC Schottky diodes have zero reverse recovery, so passive rectification is efficient. SR adds ~0.3% efficiency but increases complexity and cost. Defer to Rev 2.
- **Burst mode:** At light load (<10% rated), switch to burst/pulse-skipping mode to maintain efficiency and meet <8 W standby spec.
- **Current sharing:** Phase current balancing via individual frequency trim or current-mode control. Imbalance target ≤3% (tighter than the 5% inter-module CAN bus spec).

## 5. Controller Architecture

### 5.1 Single-MCU Approach

| Parameter | Value |
|-----------|-------|
| MCU | STM32G474RE |
| Core | Arm Cortex-M4F, 170 MHz |
| ADC | 5× 12-bit ADCs (up to 4 Msps), simultaneous sampling |
| Timers | HRTIM (high-resolution timer, 184 ps resolution) — critical for LLC frequency control |
| Math | FPU + CORDIC + FMAC accelerators |
| Comms | CAN-FD, SPI, UART |
| Firmware base | STSW-30KWVRECT (PFC) — extend for LLC control |

**Why single MCU:** The STM32G474RE has enough HRTIM channels (6 complementary outputs) plus ADC bandwidth to control both the Vienna PFC (3 switch cells) and 3-phase LLC (3 half-bridges) simultaneously. ST's reference design demonstrates this. A second MCU adds cost, board space, and inter-processor communication complexity with no performance benefit at 30 kW.

### 5.2 Control Loops

```
                    ┌──────────────────────────────────┐
                    │         Supervisory Layer        │
                    │  State machine: startup, run,    │
                    │  fault, standby, CAN protocol    │
                    └──────────┬───────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼───────┐  ┌─────▼──────┐  ┌──────▼────────┐
     │   PFC Control  │  │  DC Bus    │  │ LLC Control   │
     │                │  │  Regulation│  │               │
     │ • Phase current│  │ • Vbus ref │  │ • CC/CV mode  │
     │   PI loops (3x)│  │ • Balancing│  │ • Freq control│
     │ • PLL for grid │  │ • Soft-start│ │ • Phase balance│
     │   sync         │  │            │  │ • Burst mode  │
     │ • THD shaping  │  │            │  │ • OCP/OVP     │
     └────────────────┘  └────────────┘  └───────────────┘
```

- **PFC:** dq-frame current control with feedforward. Outer voltage loop regulates DC bus. PLL tracks grid frequency (45–65 Hz).
- **DC bus:** Setpoint adjusted dynamically (700–850 V) based on LLC output demand to keep LLC near resonance.
- **LLC:** Outer CC/CV loop sets power reference. Inner loop modulates switching frequency. Phase currents balanced via individual frequency trim.

## 6. Semiconductor Bill of Materials

| Function | Part Number | Spec | Qty | Vendor |
|----------|-------------|------|-----|--------|
| PFC MOSFETs | SCTWA90N65G2V-4 | 650 V, Gen 2 SiC | 6 | ST |
| PFC diodes | STPSC40H12C | 1200 V, 40 A SiC Schottky | 12 | ST |
| LLC primary MOSFETs | SCTW90N120G2AG (or C3M0040120K) | 1200 V, ~40 mΩ SiC | 6 | ST (or Wolfspeed) |
| LLC secondary diodes | STPSC20H065 (or C6D20065D) | 650 V SiC Schottky | 6–12 | ST (or Wolfspeed) |
| Gate drivers (all stages) | STGAP2SiC | Isolated, SiC-optimized | 6 | ST |
| Controller | STM32G474RE | Cortex-M4F, 170 MHz, HRTIM | 1 | ST |
| CAN transceiver | SN65HVD230 (or similar) | CAN 2.0 / CAN-FD | 1 | TI |

## 7. Expected Performance

| Metric | Spec Requirement | Expected |
|--------|-----------------|----------|
| PFC efficiency | — | >98.5% |
| LLC efficiency (300–1000 V) | — | >98% peak, >97.5% across range |
| **System efficiency** | **>96%** | **~96.5–97%** |
| Power factor | ≥0.99 | >0.995 |
| THDi | ≤5% | <3% |
| Output ripple | <0.5% RMS | <0.3% (3-phase interleaving) |
| Standby power | <8 W | <5 W (burst mode + PFC sleep) |
| Soft start time | ≤6 s | ~3–4 s |
| Power density | ~7 kW/L (455×300×94 mm) | 6–6.5 kW/L |

## 8. Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| LLC efficiency below 300 V | Low | Medium | Active bus voltage adjustment; power derated anyway |
| EMI compliance (EN 55032) | Medium | Low | 3-level Vienna reduces filter; add margin in filter design |
| Transformer saturation at wide freq range | Medium | Low | Careful Bmax budget; split cores with gap |
| DC bus capacitor life at 55°C | Medium | Medium | Hybrid electrolytic + film; derate capacitors for 60,000 hr life |
| SiC MOSFET gate oxide reliability | Low | Low | STGAP2SiC clamps Vgs; follow ST gate drive guidelines |
| Thermal margin in 94 mm height | Medium | Medium | Detailed CFD analysis; consider heat pipe if needed |

## 9. Reference Documents

| Resource | Source |
|----------|--------|
| [[3-Phase PFC Topology Selection]] | PFC trade study |
| [[DC-DC Topology Trade Study]] | DC-DC trade study |
| [[Commercial Reference Designs Survey]] | Vendor reference design survey |
| [STDES-30KWVRECT](https://www.st.com/en/evaluation-tools/stdes-30kwvrect.html) | ST Vienna PFC reference design |
| [STDES-30KWLLC](https://www.st.com/content/dam/static-page/events/apec-2024/demo-apec-24-30kw-dc-dc.pdf) | ST LLC DC-DC APEC 2024 |
| [Wolfspeed CRD30DD12N-K](https://www.wolfspeed.com/products/power/reference-designs/crd30dd12n-k/) | Wolfspeed 30 kW LLC reference |
| [Wolfspeed EV Charging Topologies Guidebook (PRD-08367)](https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_PRD-08367_EV_Charging_Power_Topologies_Design_Guidebook_Application_Note.pdf) | Comprehensive topology comparison |

## 10. Next Steps

- [x] Magnetics design — resonant tank parameters (Lr, Lm, Cr) and transformer specifications → [[02-Magnetics Design]]
- [x] Thermal budget — loss breakdown and cooling strategy for 455×300×94 mm envelope → [[04-Thermal Budget]]
- [x] Control firmware — STM32G474RE HRTIM/ADC allocation, PFC dq control, LLC PFM, CAN stacking → [[06-Firmware Architecture]]
- [x] EMI filter design — input filter for EN 55032 Class B → [[05-EMI Filter Design]]
- [x] Detailed BOM and cost analysis → [[07-BOM and Cost Analysis]]
- [x] PCB layout — power loop optimization for SiC dV/dt → [[07-PCB-Layout/__init|07-PCB Layout]]
- [x] Power-on sequence — inrush limiting, pre-charge, contactor, startup/shutdown timing → [[08-Power-On Sequence and Inrush Management]]
