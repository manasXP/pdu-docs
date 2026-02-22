---
tags: [pdu, pcb-layout, controller, signal-integrity, adc, hrtim, analog]
created: 2026-02-22
status: draft
---

# Signal Integrity

This document covers signal integrity considerations for the Controller Board. The board carries three classes of signals with distinct routing requirements: **analog sense inputs** (high accuracy, low noise), **HRTIM PWM outputs** (high speed, matched timing), and **digital communication buses** (controlled impedance). Each class is addressed below with specific layout rules.

## 1. Analog Sense Input Routing

The controller board receives six analog signals from the power stages via the P3 connector. These signals represent current and voltage measurements that directly affect control loop accuracy. A 1% error in sensing translates to a 1% error in output regulation.

### Signal List

| Signal | Source | Full scale | Bandwidth | ADC |
|---|---|---|---|---|
| PFC phase A current | Hall sensor / shunt + amp | 0–3.3 V | DC–50 kHz | ADC1_IN1 |
| PFC phase B current | Hall sensor / shunt + amp | 0–3.3 V | DC–50 kHz | ADC1_IN2 |
| PFC phase C current | Hall sensor / shunt + amp | 0–3.3 V | DC–50 kHz | ADC1_IN3 |
| DC bus voltage | Resistor divider + buffer | 0–3.3 V | DC–10 kHz | ADC2_IN1 |
| Output voltage | Resistor divider + buffer | 0–3.3 V | DC–10 kHz | ADC2_IN2 |
| Output current | Shunt + amp | 0–3.3 V | DC–50 kHz | ADC2_IN3 |

### Analog Signal Conditioning Circuit

Each analog input passes through a front-end conditioning stage on the controller board before reaching the MCU ADC pin:

```
From P3       OPA2376 (1/2)           Anti-Alias Filter
connector    ┌──────────┐            ┌──────────────┐
─────┬───────┤ IN+   OUT├────────────┤  R     C     ├──── ADC pin
     │       │          │            │  1kΩ   10nF  │
     R1      │  IN-  V+ ├── 3.3VA    │  fc ≈ 16 kHz │
     10kΩ    │      V-  ├── GND      └──────────────┘
     │       └──────────┘
     ├── C_in 100pF (input filter)
     │
    GND
```

- **Op-amp**: OPA2376 (dual, rail-to-rail, low offset 5 µV, low noise 7.5 nV/rtHz)
- **Configuration**: unity-gain buffer (voltage follower) for voltage signals; gain stage for current signals if needed
- **Anti-aliasing filter**: 1st-order RC, R = 1 kohm, C = 10 nF, fc = 15.9 kHz
- **Placement**: filter components must be within **5 mm of the ADC input pin** to minimize trace length after filtering

> [!warning] Filter placement is critical
> If the anti-aliasing RC filter is placed far from the ADC pin, the trace between the filter and the pin acts as an antenna that picks up noise **after** filtering. The filter loses its effectiveness. Keep the R and C as close to the MCU pin as physically possible.

### Analog Routing Rules

| Rule | Specification |
|---|---|
| Routing layer | L1 only — directly over L2 GND plane |
| Trace width | 0.20 mm (8 mil) minimum |
| Guard trace | GND guard on both sides, 0.25 mm clearance, stitched to L2 every 5 mm |
| Maximum trace length | 30 mm from P3 connector to op-amp input |
| Separation from digital | Minimum 2 mm from any digital trace or via |
| Via prohibition | No vias in analog signal path; route entirely on L1 |
| Plane reference | L2 GND only — never cross a split in L2 (L2 has no splits) |

### Guard Traces

Guard traces are GND-connected traces that run parallel to high-impedance analog signals on both sides. They serve two purposes:

1. **Shielding**: prevent capacitive coupling from adjacent digital signals
2. **Defined return path**: keep the return current directly under the signal trace in L2

Implementation:
- Guard trace width: 0.25 mm
- Gap between guard and signal: 0.25 mm
- Stitch guard traces to L2 GND with vias every 5 mm
- Extend guard traces 2 mm beyond the signal trace at each end

```
         Guard via    Guard via    Guard via
            │            │            │
 ───GND─────┼────GND─────┼────GND────┼────GND──── Guard trace (top)
            │            │            │
     ═══════════════════════════════════════      Analog signal trace
            │            │            │
 ───GND─────┼────GND─────┼────GND────┼────GND──── Guard trace (bottom)
            │            │            │
         Guard via    Guard via    Guard via
```

### Analog Guard Ring Around Op-Amp Circuits

Each OPA2376 op-amp has a GND guard ring surrounding its footprint:

- Guard ring width: 0.3 mm
- Ring clearance from component pads: 0.5 mm
- Stitching vias on the ring: every 3 mm
- The ring connects to the analog ground region of L2

> [!tip] Star-ground for analog reference
> The VREF+ pin of the STM32 connects to the analog 3.3 V supply (3.3VA) through a dedicated trace. The GND return for VREF is routed as a separate trace from the VSSA pin back to the analog ground star point — the single point where analog and digital ground domains meet on L2. This star point should be located near the Aux PSU power entry connector P5.

## 2. HRTIM PWM Output Routing

The STM32G474 HRTIM peripheral generates 12 PWM channels (6 for the Vienna PFC, 6 for the LLC DC-DC). These signals control SiC MOSFET gate drivers on the power boards via harness cables.

### PWM Channel Assignment

| HRTIM Timer | Output | Function | Connector |
|---|---|---|---|
| Timer A | TA1 / TA2 | PFC phase A (high/low) | P1 pin 1,2 |
| Timer B | TB1 / TB2 | PFC phase B (high/low) | P1 pin 3,4 |
| Timer C | TC1 / TC2 | PFC phase C (high/low) | P1 pin 5,6 |
| Timer D | TD1 / TD2 | LLC phase A (high/low) | P2 pin 1,2 |
| Timer E | TE1 / TE2 | LLC phase B (high/low) | P2 pin 3,4 |
| Timer F | TF1 / TF2 | LLC phase C (high/low) | P2 pin 5,6 |

### Matched-Length Routing for Complementary Pairs

Each HRTIM timer produces a complementary pair (e.g., TA1 and TA2). The dead-time between high-side and low-side switching is programmed with 184 ps resolution. To preserve this accuracy at the board level:

| Routing parameter | Requirement |
|---|---|
| Length matching within a pair | +/- 1 mm (< 7 ps skew at propagation velocity ~150 mm/ns) |
| Length matching between pairs | +/- 5 mm (not critical — each phase independent) |
| Trace impedance | 50 ohm single-ended (referenced to L2 GND) |
| Routing layer | L1 only |
| Minimum spacing between pairs | 3x trace width (0.81 mm for 0.27 mm traces) |

### Series Termination Resistors

Each HRTIM output has a **33 ohm series termination resistor** placed at the MCU pin (source termination):

```
STM32 HRTIM pin ──[33Ω]──── 50Ω trace ──── P1/P2 connector pin
                  ^
                  Resistor placed within
                  3 mm of MCU pad
```

Purpose:
- Absorbs reflections from the cable-end impedance mismatch
- Reduces edge rate to lower EMI on the harness cable
- Resistor value: 33 ohm (Zo - Rout_MCU, where Rout is approx 17 ohm for STM32 GPIO)

> [!tip] Resistor placement
> Place the 33 ohm series resistors in a row adjacent to the MCU, oriented so that the trace runs straight from the MCU pad through the resistor and onward to the connector. Do not route the trace away from the MCU and then back to the resistor — this creates a stub.

### PWM Signal Routing Summary

| Characteristic | Value |
|---|---|
| Number of PWM traces | 12 |
| Trace width | 0.27 mm (50 ohm on L1) |
| Series termination | 33 ohm 0402 at MCU pin |
| Max trace length | 50 mm (MCU to connector) |
| Pair length matching | +/- 1 mm |
| Layer | L1 exclusively |
| Reference plane | L2 GND (continuous, no breaks) |

## 3. Current Sense Signal Conditioning Layout

The current sense circuit is the most noise-sensitive analog subsystem. Layout for each current sense channel:

### Component Placement Order

Place components in a **linear flow** from connector to ADC pin:

```
P3 pin ──▶ Input R (10kΩ) ──▶ Input C (100pF) ──▶ OPA2376 ──▶ R_AA (1kΩ) ──▶ C_AA (10nF) ──▶ ADC pin
         [ESD clamp]
```

| Rule | Detail |
|---|---|
| Flow direction | Linear, west-to-east (P3 on west edge, MCU in center) |
| Component spacing | 1–2 mm between components in the chain |
| Ground returns | Each GND pad connects to L2 via its own via, within 1 mm |
| Feedback path (if gain stage) | Route under the IC body or on L1 adjacent to IC |
| Power supply bypass | 100 nF cap within 2 mm of OPA2376 V+ pin |

### Noise Budget

The ADC LSB at 12 bits and 3.3 V reference is:

```
LSB = 3.3 V / 4096 = 0.806 mV
```

To achieve 12-bit accuracy, total input-referred noise (including layout-induced pickup) must be less than 0.5 LSB = 0.4 mV RMS. The noise budget allocation:

| Source | Budget (µV RMS) |
|---|---|
| Op-amp input noise (OPA2376, BW = 16 kHz) | 95 |
| Resistor thermal noise (10 kohm, BW = 16 kHz) | 51 |
| PCB pickup (layout-dependent) | < 200 |
| **Total RSS** | **< 400** |

> [!warning] PCB pickup dominance
> The PCB layout contribution dominates the noise budget. Poor routing (long traces, missing guard traces, crossing digital signals) can easily exceed the 200 µV budget. Follow all analog routing rules strictly.

## 4. SPI Bus Routing (QCA7000 Interface)

The SPI interface to the QCA7000 PLC modem runs at up to 24 MHz (STM32G474 SPI maximum). Layout considerations:

| Signal | Type | Impedance | Notes |
|---|---|---|---|
| SCK | Clock | 50 ohm | Source-terminated with 33 ohm at MCU |
| MOSI | Data out | 50 ohm | Length-matched to SCK +/- 5 mm |
| MISO | Data in | 50 ohm | Length-matched to SCK +/- 5 mm |
| CS | Chip select | 50 ohm | Not length-critical |

- Route on L1 over L2 GND
- Keep SPI traces at least 2 mm from analog traces
- Place a 100 nF bypass capacitor at the QCA7000 VDD pin within 1 mm

## 5. MCU Crystal / Oscillator Layout

The STM32G474RE uses an 8 MHz crystal (HSE) with a PLL to generate the 170 MHz system clock. Crystal layout is critical for reliable startup and low jitter.

| Rule | Detail |
|---|---|
| Crystal placement | Within 5 mm of OSC_IN / OSC_OUT pins |
| Load capacitors | Within 2 mm of crystal pads |
| Guard ring | GND guard ring around crystal and load caps |
| Routing | L1 only, traces as short as possible |
| No vias | No vias in crystal circuit |
| Ground plane | Continuous L2 under crystal — absolutely no breaks |
| Separation | 5 mm minimum from any high-speed digital trace |

> [!tip] Crystal ground pad
> If the crystal has a metal case or ground pad, connect it to L2 GND with a via directly under the crystal. This provides shielding and reduces EMI from the oscillator.

## 6. Cross-References

- [[07-PCB-Layout/Controller/01-Stack-Up and Layer Assignment]] — layer definitions and impedance targets
- [[03-Communication Interfaces]] — CAN differential pair routing details
- [[04-Power Distribution]] — analog vs. digital power separation
- [[05-EMC and Grounding]] — guard rings, ground strategy
- [[06-Firmware Architecture]] — ADC sampling configuration, HRTIM timer setup
- [[__init|Controller Board Overview]] — board zoning and connector pinout

## 7. Design Checklist

| Item | Check |
|---|---|
| All analog traces on L1 over continuous L2 GND | |
| Guard traces on all 6 analog channels | |
| Anti-alias RC within 5 mm of each ADC pin | |
| 33 ohm series termination on all 12 HRTIM outputs | |
| HRTIM complementary pairs matched to +/- 1 mm | |
| Crystal guard ring and short traces | |
| SPI signals length-matched to +/- 5 mm | |
| No analog traces crossing digital traces | |
| No analog vias (all analog routing on L1) | |
| Star-ground point defined for analog reference | |

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
