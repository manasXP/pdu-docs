---
tags: [PDU, testing, bring-up, prototype, verification, lab-procedure]
created: 2026-02-22
status: draft
---

# Board-Level Test Procedure — 30 kW PDU

> [!summary] Purpose
> This document defines the **lab-level board test procedures** for prototype bring-up and design verification of the 30 kW PDU's five independently fabricated PCBs. It covers equipment lists, standalone board test setups, step-by-step test sequences with pass/fail criteria, and test report templates. For field-level commissioning of an assembled system, see [[12-Project-Management/__init|12-Project Management]] → [[Commissioning Procedure]].

---

## 1. Lab Equipment List

### 1.1 Power Sources

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 1 | 3-phase programmable AC source | 0–530 VAC L-L, 60 A/phase, 30 kVA, 45–65 Hz, PF programmable | Chroma 61845 / Pacific Power 345-AMX | 1 |
| 2 | HV DC power supply (DC bus) | 0–1000 V, 0–10 A, 5 kW | Keysight N8957A / TDK-Lambda Z+ | 1 |
| 3 | HV DC power supply (output sim) | 0–600 V, 0–5 A, 1 kW | Keysight E36234A | 1 |
| 4 | Low-voltage bench supply | 0–30 V, 0–3 A, dual channel | Rigol DP832 / Keysight E36312A | 1 |
| 5 | 24 VDC supply (relay/contactor coils) | 24 V, 3 A | Any regulated bench supply | 1 |

### 1.2 Electronic Loads

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 6 | DC electronic load (main) | 30 kW, 0–1200 V, 0–100 A, CC/CV/CP modes | Chroma 63210A-1200-400 / NH Research 4760 | 1 |
| 7 | DC electronic load (bus) | 600 V, 40 A, 10 kW, CC mode | Chroma 63206A-600-840 | 1 |
| 8 | Resistive load bank | 10–100 Ω, 500 W, wirewound | Ohmite or custom | 1 set |

### 1.3 Measurement — Oscilloscope and Probes

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 9 | Digital oscilloscope | ≥500 MHz, 4 ch, 12-bit ADC, ≥2.5 GS/s, math/FFT | Keysight MSOX4054A / Tektronix MSO54 | 1 |
| 10 | HV differential probes | 1500 V, 100 MHz BW | Tektronix THDP0200 / PMK BumbleBee | 2 |
| 11 | Current probe (low) | 30 A, 120 MHz BW | Tektronix TCP0030A | 2 |
| 12 | Current probe (high) | 150 A, 20 MHz BW | PEM CWT Mini HF 06 Rogowski | 2 |
| 13 | Rogowski coil (primary) | 300 A pk, 30 MHz BW | PEM CWT Ultra-mini | 3 |

### 1.4 Measurement — Meters and Analyzers

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 14 | Power analyzer | 3P4W, ≥0.05% accuracy, ≥2 MHz BW, 6 ch | Yokogawa WT3000E / Hioki PW6001 | 1 |
| 15 | 6.5-digit DMM | 1000 VDC, 10 A, true-RMS | Keysight 34465A | 2 |
| 16 | LCR meter | 100 Hz–1 MHz, 4-wire | Keysight E4980AL | 1 |
| 17 | Thermal camera | ≥160×120, ±2°C, NETD ≤50 mK | FLIR E86 / InfiRay T630 | 1 |
| 18 | Thermocouple data logger | 8-ch, Type K, 0.1°C resolution | Pico TC-08 / Omega OM-DAQ-USB-2401 | 1 |
| 19 | Type K thermocouples | −40 to +260°C, adhesive-tip | — | 8 |

### 1.5 Safety Test Equipment

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 20 | Hipot tester (AC) | 0–5 kV AC, 50/60 Hz, adjustable ramp, 100 mA trip | Associated Research Hypot 3705 | 1 |
| 21 | Insulation resistance tester (Megger) | 500 V / 1000 V / 2500 V DC, ≥200 GΩ range | Fluke 1555 / Megger MIT515 | 1 |
| 22 | Earth bond tester | 25 A, ≤100 mΩ, 60 s hold | Associated Research 3705 (combo) | 1 |
| 23 | Leakage current meter | 0–10 mA AC/DC, MD network per IEC 62368-1 | — | 1 |

### 1.6 Signal and Protocol Equipment

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 24 | Function generator | 1 Hz–25 MHz, 2 ch, arbitrary waveform | Keysight 33500B | 1 |
| 25 | Logic analyzer | ≥16 ch, 100 MHz sampling | Saleae Logic Pro 16 | 1 |
| 26 | CAN bus interface | PCAN-USB FD, ISO 11898-compliant | Peak PCAN-USB FD | 2 |
| 27 | ST-Link V3 debugger/programmer | SWD, supports STM32G4 | STLINK-V3SET | 1 |
| 28 | CAN bus termination load | 120 Ω | Resistor + DB-9 plug | 2 |

### 1.7 Environmental

| # | Equipment | Minimum Specification | Suggested Make/Model | Qty |
|:-:|-----------|----------------------|---------------------|:---:|
| 29 | Thermal chamber (optional) | −40 to +85°C, interior ≥0.5 m³ | ESPEC / Thermotron | 1 |
| 30 | Production-spec fans | 3 × 92 mm, PWM, matching PDU spec | — | 3 |

### 1.8 Fixtures and Safety

| # | Item | Notes | Qty |
|:-:|------|-------|:---:|
| 31 | DUT mounting plate | Aluminum plate with standoff holes matching all 5 boards | 1 |
| 32 | Bus bar set (P2) | Laminated Cu, 2 mm, tin-plated, matching [[00-Board Partitioning]] §4.3 | 1 |
| 33 | Signal harness S1 | 12-pin Molex Pico-Lock, Controller → AC-DC, shielded | 1 |
| 34 | Signal harness S2 | 10-pin Molex Pico-Lock, Controller → DC-DC, shielded | 1 |
| 35 | Signal harness S3 | DB-9 or M12, CAN bus + termination | 1 |
| 36 | Signal harness S4 | 8-pin Molex Micro-Fit 3.0, Controller → Power Entry | 1 |
| 37 | Power harness P1b | 3 × 10 AWG, Power Entry → AC-DC | 1 |
| 38 | Power harness P3a | 2 × 8 AWG, DC-DC → Power Entry | 1 |
| 39 | Power harness P4 | Molex Micro-Fit 3.0, 8-pin, Aux PSU → power boards | 1 |
| 40 | Power harness P5 | Molex Micro-Fit 3.0, 4-pin, Aux PSU → Controller | 1 |
| 41 | Fuses (AC input) | 80 A, 600 VAC, fast-blow (one per phase) | 3 |
| 42 | Fuse (DC output) | 125 A, 1000 VDC, fast-blow | 1 |
| 43 | E-stop mushroom button | Wired to disconnect AC source enable + load enable | 1 |
| 44 | PPE kit | HV-rated gloves (Class 0, 1000 V), safety glasses, insulating mat | 1 set |
| 45 | Discharge probe | 10 kΩ, 50 W, insulated handles, rated 1200 V | 1 |

---

## 2. Test Setup Diagrams

### 2.1 Power Entry Board — Standalone

```
                     ┌──────────────────────────────────────┐
                     │        POWER ENTRY BOARD (DUT)       │
                     │                                      │
  24 VDC Bench  ────▶│ S4 pin 6 (+24V_COIL)                 │
  Supply (3A)        │ S4 pin 8 (GND)                       │
                     │                                      │
  Function Gen ─────▶│ S4 pin 1 (RELAY_A_DRV) ─┐            │
  (3.3V logic)       │ S4 pin 2 (RELAY_B_DRV)  ├ via jumper │
                     │ S4 pin 3 (RELAY_C_DRV)  │  or MCU    │
                     │ S4 pin 4 (CONT_DRV) ────┘            │
                     │                                      │
  Reduced AC   ─────▶│ P1a (L1, L2, L3, PE)                 │
  Source (50 VAC)    │                                      │
                     │ P1b (L1_FILT, L2_FILT, L3_FILT) ───▶ Resistive Load
                     │                                      │  (10 Ω / phase)
                     │ P3a ◀─── DC Supply 50V ────────────  │
                     │ P3b ──── to DMM (contact R meas) ──  │
                     │                                      │
  Oscilloscope ─────▶│ Probe: relay coil transients         │
  Ch1: relay coil    │ Probe: contactor aux contact         │
  Ch2: S4 pin 5 FB   │                                      │
                     └──────────────────────────────────────┘
```

> [!note] Reduced Voltage
> Test the Power Entry board at **reduced AC voltage** (50 VAC) initially. Full voltage testing occurs only during system integration.

### 2.2 Aux PSU Board — Standalone

```
                     ┌──────────────────────────────────────┐
                     │         AUX PSU BOARD (DUT)          │
                     │                                      │
  HV DC Supply  ────▶│ DC Bus Input (400–920 VDC)           │
  (600V, 1A)         │                                      │
                     │ P4 pin 1 (VDRV_AC +18V) ───▶ 36 Ω / 10W resistor
                     │ P4 pin 2 (VNEG_AC −5V)  ───▶ 25 Ω / 1W resistor
                     │ P4 pin 3 (VDRV_AC_RTN)                │
                     │ P4 pin 5 (VDRV_DC +18V) ───▶ 36 Ω / 10W resistor
                     │ P4 pin 6 (VNEG_DC −5V)  ───▶ 25 Ω / 1W resistor
                     │ P4 pin 7 (VDRV_DC_RTN)                │
                     │ P5 pin 1 (+5V)          ───▶ 5 Ω / 5W resistor
                     │ P5 pin 2 (+3.3V)        ───▶ 6.6 Ω / 2W resistor
                     │ P5 pin 4 (+12V_FAN)     ───▶ 6 Ω / 25W resistor
                     │ P5 pin 3 (GND)                        │
                     │                                       │
  DMM #1 ───────────▶│ Measure each output voltage           │
  DMM #2 ───────────▶│ Measure input current                 │
  Oscilloscope ─────▶│ Ch1: +18V ripple (AC-coupled, 20MHz BW)│
                     │ Ch2: +3.3V ripple                     │
                     │ Ch3: primary FET drain (HV diff probe)│
                     └───────────────────────────────────────┘
```

### 2.3 Controller Board — Standalone

```
                     ┌──────────────────────────────────────┐
                     │       CONTROLLER BOARD (DUT)         │
                     │                                      │
  Bench Supply  ────▶│ P5 pin 1 (+5V, 1A limit)             │
  Ch1: +5V           │ P5 pin 2 (+3.3V, 0.5A limit)         │
  Ch2: +3.3V         │ P5 pin 3 (GND)                       │
                     │ P5 pin 4 (+12V, via separate supply) │
                     │                                      │
  ST-Link V3   ─────▶│ SWD header (SWDIO, SWCLK, NRST, GND) │
                     │                                      │
  PCAN-USB #1  ─────▶│ S3 (CAN_H, CAN_L) + 120Ω term        │
  PCAN-USB #2  ─────▶│ (second CAN node for traffic gen)    │
                     │                                      │
  Oscilloscope ─────▶│ Ch1: PWM_A_H (S1 pin 1)              │
                     │ Ch2: PWM_LLC_A (S2 pin 1)            │
                     │ Ch3: CAN_H (S3 pin 1)                │
                     │ Ch4: ADC test input (P3 pin 1)       │
                     │                                      │
  Function Gen ─────▶│ P3 analog input (sine wave sim)      │
                     └──────────────────────────────────────┘
```

### 2.4 AC-DC Board — Standalone

```
                     ┌──────────────────────────────────────┐
                     │        AC-DC BOARD (DUT)             │
                     │                                      │
  3-Phase AC   ─────▶│ P1b (L1_FILT, L2_FILT, L3_FILT)      │
  Source             │  via 80A fuses (per phase)           │
  (260–530 VAC)      │                                      │
                     │ Gate Drive Supply (+18V/−5V) ◀────── Aux PSU or
                     │  P4 pins 1–4                         │  bench supply
                     │                                      │
                     │ Control Harness S1 ◀──────────────── Controller or
                     │  (12-pin: 6 PWM + 3 I_SENSE +        │  function gen
                     │   V_BUS_SENSE + FAULT_PFC + GND)     │
                     │                                      │
                     │ DC Bus Output (P2) ──────────────▶  DC Electronic
                     │  DC_BUS+ / DC_BUS−                   │  Load (bus)
                     │  (920 VDC, 40A max)                  │  600V / 40A
                     │                                      │
  Power Analyzer ───▶│ 3P4W AC input + DC output            │
  Oscilloscope ─────▶│ Ch1: V_DS switching node (HV probe)  │
                     │ Ch2: I_phase (Rogowski/current probe)│
                     │ Ch3: V_bus DC (HV diff probe)        │
                     │ Ch4: gate drive signal               │
  Thermal Camera ───▶│ MOSFET / diode / inductor surfaces   │
                     └──────────────────────────────────────┘
```

### 2.5 DC-DC Board — Standalone

```
                     ┌──────────────────────────────────────┐
                     │        DC-DC BOARD (DUT)             │
                     │                                      │
  HV DC Supply  ────▶│ P2 (DC_BUS+, DC_BUS−)                │
  (0–920 VDC)        │  via bus bar + fuse                  │
  or DC load on      │                                      │
  AC-DC output       │ Gate Drive Supply (+18V/−5V) ◀────── Aux PSU or
                     │  P4 pins 5–8                         │  bench supply
                     │                                      │
                     │ Control Harness S2 ◀──────────────── Controller or
                     │  (10-pin: 6 PWM + V_OUT_SENSE +      │  function gen
                     │   I_OUT_SENSE + FAULT_LLC + GND)     │
                     │                                      │
                     │ DC Output (P3a) ─────────────────▶  DC Electronic
                     │  DC_PRE_CONT+ / DC_PRE_CONT−         │  Load (main)
                     │  (150–1000 VDC, 100A max)            │  1200V / 100A
                     │                                      │
  Power Analyzer ───▶│ DC input + DC output                 │
  Oscilloscope ─────▶│ Ch1: V_DS primary half-bridge (HV)   │
                     │ Ch2: I_resonant (Rogowski)           │
                     │ Ch3: V_out DC (HV diff probe)        │
                     │ Ch4: V_DS secondary SR (HV)          │
  Thermal Camera ───▶│ MOSFETs / diodes / transformer       │
                     └──────────────────────────────────────┘
```

### 2.6 Full System Integration

```
 3-Phase AC Source (530 VAC, 60A)
       │
       │ 80A fuses (×3)
       ▼
 ┌──────────┐   P1b    ┌──────────┐   P2 bus   ┌──────────┐
 │  Power   │ ────────▶│  AC-DC   │ ═════════▶ │  DC-DC   │
 │  Entry   │          │  Board   │  bar       │  Board   │
 │  Board   │◀─────────│          │            │          │──▶ P3a
 │          │  P3a     └────┬─────┘            └────┬─────┘
 └──┬───┬───┘               │                       │
    │   │              ┌────┴─────┐            ┌────┴─────┐
    │   │              │ Aux PSU  │◀───────────│Controller│
    │   │              │  Board   │  P5        │  Board   │
    │   │              └──────────┘            └────┬─────┘
    │   │                                           │ S3
    │   └──── P3b ──▶ DC Electronic Load (30kW)     │
    │         (via contactor)   1200V / 100A         ▼
    │                                          PCAN-USB (PC)
    │
    └──── P1a ◀── AC Source

 Power Analyzer: 3P4W on AC input + DC wiring on output (6 channels)
 Thermocouple logger: 8 × Type K on MOSFETs, diodes, transformer, ambient
 Thermal camera: positioned for top-down view of all heatsinks
 E-stop: series with AC source enable + DC load enable
```

### 2.7 Safety / Hipot Test Connections

```
  Hipot Tester                    DUT (all boards assembled, power OFF)
  ┌──────────┐
  │          │─── HV lead ──▶  Test Point (varies per test)
  │  5 kV AC │
  │          │─── Return ───▶  Chassis PE stud
  └──────────┘

  Test 1: AC input → PE     HV on P1a (L1+L2+L3 shorted) │ Return on PE
  Test 2: DC bus → PE       HV on P2 (BUS+ & BUS− shorted)│ Return on PE
  Test 3: DC output → PE    HV on P3b (OUT+ & OUT− shorted)│ Return on PE
  Test 4: Primary → Secondary  HV on P2 │ Return on P3a (primary-to-sec isolation)

  ┌────────────────────────────────────────────────────────────┐
  │  IMPORTANT: Disconnect ALL signal harnesses (S1–S4) and    │
  │  electronic loads before hipot testing. Short each domain  │
  │  internally to avoid voltage stress across components.     │
  └────────────────────────────────────────────────────────────┘
```

---

## 3. Board-Level Test Procedures

### 3.1 Power Entry Board (PE-CONT-01)

Reference: [[07-PCB-Layout/Power-Entry/__init|Power Entry Board]], [[08-Power-On Sequence and Inrush Management]]

#### 3.1.1 Visual Inspection

| Step | Action | Instrument | Pass Criteria | Record |
|:----:|--------|-----------|---------------|--------|
| PE-V01 | Inspect all solder joints on NTC pads (3×) for cold joints or bridges | 10× magnifier | No solder bridges, smooth fillets on 4 oz Cu | ☐ P / ☐ F |
| PE-V02 | Inspect bypass relay solder pins (3×) for complete through-hole fill | 10× magnifier | ≥75% barrel fill per IPC-A-610 Class 2 | ☐ P / ☐ F |
| PE-V03 | Inspect output contactor (TE EV200) mounting hardware | Visual | M5 bolts torqued, no cracked PCB pads | ☐ P / ☐ F |
| PE-V04 | Verify RC snubber component values (100 Ω + 47 nF × 3 sets) | Visual + marking check | Correct values, 630 VAC rated caps | ☐ P / ☐ F |
| PE-V05 | Verify flyback diode polarity on all coil drivers (3 relay + 1 contactor) | Visual | Cathode stripe toward +24V rail | ☐ P / ☐ F |
| PE-V06 | Inspect PCB slot between AC and DC zones | 10× magnifier | Slot width ≥2 mm, no solder bridges across slot | ☐ P / ☐ F |
| PE-V07 | Verify creepage: AC zone to PE ≥10 mm, DC zone to PE ≥15 mm | Ruler / caliper | Distances per [[09-Protection and Safety]] §7.1.1 | ☐ P / ☐ F |
| PE-V08 | Verify connector keying: S4 unique vs S1/S2/S3, P1a/P1b/P3a/P3b correct | Mate check | Cannot cross-mate with wrong harness | ☐ P / ☐ F |

#### 3.1.2 Continuity and Resistance

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| PE-R01 | Measure NTC cold resistance (3×) at ambient temperature | DMM, Ω mode | 10 Ω ±20% at 25°C (8–12 Ω) | NTC_A: ___ Ω, NTC_B: ___ Ω, NTC_C: ___ Ω |
| PE-R02 | Measure NTC-to-NTC resistance balance | DMM | Max deviation between 3 NTCs ≤15% | ☐ P / ☐ F |
| PE-R03 | Verify bypass relay contact resistance (each relay, contacts forced closed) | DMM, mΩ mode (or 4-wire) | <5 mΩ per contact | Relay_A: ___ mΩ, Relay_B: ___ mΩ, Relay_C: ___ mΩ |
| PE-R04 | Measure contactor contact resistance (manually close or energize at 24 V) | DMM, mΩ (4-wire, 1A source) | <1 mΩ (TE EV200 spec: <0.3 mΩ) | ___ mΩ |
| PE-R05 | Verify contactor auxiliary contact: open when coil de-energized, closed when energized | DMM, continuity | Open >1 MΩ, Closed <1 Ω | ☐ P / ☐ F |
| PE-R06 | Insulation resistance: AC zone to PE | Megger, 500 VDC, 60 s | >100 MΩ | ___ MΩ |
| PE-R07 | Insulation resistance: DC zone to PE | Megger, 1000 VDC, 60 s | >100 MΩ | ___ MΩ |
| PE-R08 | Insulation resistance: AC zone to DC zone | Megger, 1000 VDC, 60 s | >100 MΩ | ___ MΩ |
| PE-R09 | Continuity: PE stud to chassis mounting hole | DMM, Ω | <0.1 Ω | ___ Ω |
| PE-R10 | Continuity: each phase P1a pin to corresponding P1b pin (through NTC) | DMM | 10 ±2 Ω (NTC in path) | L1: ___ Ω, L2: ___ Ω, L3: ___ Ω |
| PE-R11 | Continuity: P3a to P3b (through contactor, coil energized) | DMM | <5 mΩ (contactor + trace) | ___ mΩ |
| PE-R12 | Verify no short: P3a+ to P3a− | DMM | >10 MΩ | ☐ P / ☐ F |

#### 3.1.3 First Power-On

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| PE-P01 | Apply 24 VDC to S4 pin 6 / pin 8. Measure quiescent current | Bench supply, 24 V, 0.1 A limit | <10 mA (no coils energized) | ___ mA |
| PE-P02 | Drive RELAY_A_DRV high (3.3 V). Verify relay A clicks, measure coil current | Oscilloscope Ch1 on coil, DMM | Relay actuates; coil I ≈ 40–50 mA at 24 V | ___ mA |
| PE-P03 | Repeat PE-P02 for RELAY_B_DRV and RELAY_C_DRV | Same | Same criteria | B: ___ mA, C: ___ mA |
| PE-P04 | Drive CONT_DRV high (3.3 V). Verify contactor clicks, check aux contact S4 pin 5 | Oscilloscope, DMM | Contactor actuates within 20 ms; aux FB goes low | Actuation time: ___ ms |
| PE-P05 | De-energize contactor. Verify aux contact returns within 20 ms | Oscilloscope trigger on coil | Aux FB goes high within 20 ms | Release time: ___ ms |
| PE-P06 | Apply 50 VAC (reduced) 3-phase to P1a via current-limited AC source (5 A limit) | AC source, oscilloscope | No arcing, NTC current ≈ 5 A peak per phase | I_pk: ___ A |
| PE-P07 | With relays energized (NTC bypassed), measure voltage drop P1a → P1b per phase at 5 A | DMM AC mV | <100 mV per phase (relay contact drop) | L1: ___ mV, L2: ___ mV, L3: ___ mV |
| PE-P08 | Apply 50 VDC to P3a. Close contactor. Measure V at P3b | DMM | V_P3b = V_P3a ±0.1 V (contact drop negligible at low current) | ☐ P / ☐ F |
| PE-P09 | Monitor relay coil voltage transients on de-energize (check flyback diode function) | Oscilloscope, Ch1 across coil | Clamp voltage <30 V (flyback diode limits spike) | V_clamp: ___ V |

#### 3.1.4 Functional Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| PE-F01 | Full NTC inrush test: apply 260 VAC 3-phase, DC bus cap load (470 µF × 2 on each rail) connected via P1b → rectifier → caps. Measure peak inrush per phase | Rogowski coils, oscilloscope | I_peak ≤ 40 A/phase at 260 VAC (per [[08-Power-On Sequence and Inrush Management]] §2.1) | I_pk: ___ A |
| PE-F02 | Repeat PE-F01 at 530 VAC | Same | I_peak ≤ 75 A/phase | I_pk: ___ A |
| PE-F03 | Contactor contact resistance under 100 A DC load (requires system integration or external DC supply + load) | 4-wire mΩ meter | <1 mΩ (matches TE EV200 datasheet: <0.3 mΩ) | ___ mΩ |

#### 3.1.5 Protection Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| PE-X01 | Contactor welding detection: de-energize contactor coil; verify aux contact opens | DMM on S4 pin 5 | Aux contact open within 20 ms; firmware would flag WELD_FAULT if stuck | ☐ P / ☐ F |
| PE-X02 | Simulate contactor weld: hold S4 pin 5 low while coil is off; verify fault logic (requires controller firmware or manual check) | Logic analyzer on S4 | Fault flag set when aux disagrees with coil command | ☐ P / ☐ F |

#### 3.1.6 Thermal Characterization

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| PE-T01 | 1-hour continuous run at 60 A AC (requires system integration). Monitor NTC body (bypassed), relay body, contactor body temperatures | Thermocouple logger + thermal camera | Relay body <85°C, contactor body <80°C, no hot spots | Relay: ___°C, Contactor: ___°C |
| PE-T02 | 10× rapid NTC inrush cycles (530 VAC, 30 s interval). Monitor NTC disc temperature | Thermocouple on NTC disc | NTC disc <200°C (well within 150 J energy rating) | T_max: ___°C |

---

### 3.2 Aux PSU Board (AUX-PSU-01)

Reference: [[07-PCB-Layout/Aux-PSU/__init|Aux PSU Board]]

#### 3.2.1 Visual Inspection

| Step | Action | Instrument | Pass Criteria | Record |
|:----:|--------|-----------|---------------|--------|
| AX-V01 | Inspect flyback transformer solder joints and isolation slot (4 mm min) | 10× magnifier | No bridges across isolation barrier, slot width ≥4 mm | ☐ P / ☐ F |
| AX-V02 | Verify Y-capacitor placement (primary to secondary, across slot) | Visual | Only Y-rated caps cross the isolation barrier | ☐ P / ☐ F |
| AX-V03 | Verify optocoupler/feedback IC orientation | Visual | Pin 1 dot matches silkscreen | ☐ P / ☐ F |
| AX-V04 | Inspect output electrolytic capacitor polarity (all rails) | Visual | Stripe (negative) matches PCB marking | ☐ P / ☐ F |
| AX-V05 | Verify creepage primary → secondary ≥14 mm, clearance ≥8 mm | Ruler/caliper | Per [[09-Protection and Safety]] §7.1.1 | ☐ P / ☐ F |

#### 3.2.2 Continuity and Resistance

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AX-R01 | Insulation resistance: DC bus input to all secondary outputs (shorted together) | Megger, 1000 VDC, 60 s | >100 MΩ | ___ MΩ |
| AX-R02 | Insulation resistance: Domain A (VDRV_AC) to Domain B (VDRV_DC) | Megger, 500 VDC, 60 s | >50 MΩ (functional isolation) | ___ MΩ |
| AX-R03 | Measure flyback primary winding DCR | LCR meter, 1 kHz | Per design (typically 2–10 Ω for 920V input flyback) | ___ Ω |
| AX-R04 | Measure each secondary winding DCR | LCR meter, 1 kHz | Per design (typically 0.1–2 Ω) | VDRV_AC: ___ Ω, VDRV_DC: ___ Ω, Logic: ___ Ω |
| AX-R05 | Verify no short: DC bus input+ to input− | DMM | >1 MΩ (capacitors should not short) | ☐ P / ☐ F |

#### 3.2.3 First Power-On

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AX-P01 | Apply 400 VDC (minimum input) via HV DC supply, 100 mA current limit. Monitor input current | HV supply, DMM | Supply starts; I_in < 80 mA at no load | ___ mA |
| AX-P02 | Measure VDRV_AC (+18V rail) at P4 pin 1 vs pin 3, no load | DMM | 18 V ±5% (17.1–18.9 V) | ___ V |
| AX-P03 | Measure VNEG_AC (−5V rail) at P4 pin 2 vs pin 3, no load | DMM | −5 V ±5% (−4.75 to −5.25 V) | ___ V |
| AX-P04 | Measure VDRV_DC (+18V rail) at P4 pin 5 vs pin 7, no load | DMM | 18 V ±5% | ___ V |
| AX-P05 | Measure VNEG_DC (−5V rail) at P4 pin 6 vs pin 7, no load | DMM | −5 V ±5% | ___ V |
| AX-P06 | Measure +5V rail at P5 pin 1 vs pin 3, no load | DMM | 5.0 V ±2% (4.9–5.1 V) | ___ V |
| AX-P07 | Measure +3.3V rail at P5 pin 2 vs pin 3, no load | DMM | 3.3 V ±2% (3.234–3.366 V) | ___ V |
| AX-P08 | Measure +12V_FAN rail at P5 pin 4 vs pin 3, no load | DMM | 12 V ±5% (11.4–12.6 V) | ___ V |
| AX-P09 | Measure output ripple on +18V rail (AC-coupled, 20 MHz BW limit) | Oscilloscope, short ground lead | <100 mV pk-pk | ___ mV pp |
| AX-P10 | Measure output ripple on +3.3V rail | Oscilloscope, short ground lead | <30 mV pk-pk | ___ mV pp |

#### 3.2.4 Functional Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AX-F01 | Apply rated resistive loads to all outputs per §2.2 diagram. Measure all voltages under load | DMM | All rails within spec (±5% gate drive, ±2% logic) | See report |
| AX-F02 | Measure input power and total output power at full load | Power analyzer or DMM | Efficiency ≥80% | η = ___% |
| AX-F03 | Sweep input voltage 400 → 920 VDC. Verify all outputs remain in regulation | DMM, HV supply | All outputs within spec across full input range | ☐ P / ☐ F |
| AX-F04 | Verify startup time: time from input applied to +3.3V stable | Oscilloscope, trigger on input | <500 ms (per [[08-Power-On Sequence and Inrush Management]] §7.1) | ___ ms |
| AX-F05 | Load transient: step +5V load 0% → 100% → 0%. Measure voltage excursion | Electronic load, oscilloscope | Overshoot/undershoot <200 mV, recovery <1 ms | ___ mV |
| AX-F06 | Cross-regulation: load +18V VDRV_AC to 100%, measure +3.3V variation | DMM | +3.3V change <2% | ___ mV |
| AX-F07 | Verify isolation between Domain A and Domain B outputs at full load | Megger, 500 VDC (outputs off, just measure) | >10 MΩ | ___ MΩ |

#### 3.2.5 Protection Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AX-X01 | Short-circuit +5V output (via electronic load at 0V). Verify hiccup or shutdown | Oscilloscope, current probe | Output shuts down or hiccups; no component damage; auto-recovers when short removed | ☐ P / ☐ F |
| AX-X02 | Over-load +18V rail to 150% (0.75 A). Verify current limiting or shutdown | Resistive load 24 Ω, DMM | Voltage droops or supply shuts down; no damage | ☐ P / ☐ F |
| AX-X03 | Remove input voltage abruptly during full load. Verify no output voltage overshoot | Oscilloscope on all outputs | No rail exceeds 120% of nominal | ☐ P / ☐ F |

#### 3.2.6 Thermal Characterization

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AX-T01 | 1-hour run at full output load (23 W), 920 VDC input. Thermal camera + thermocouples on flyback FET, transformer, output diodes | Thermocouple logger, thermal camera | No component >110°C; transformer <100°C; FET <120°C | T_max: ___°C (component: ___) |
| AX-T02 | Repeat AX-T01 at 400 VDC input (worst-case duty cycle) | Same | Same limits | T_max: ___°C (component: ___) |

---

### 3.3 Controller Board

Reference: [[07-PCB-Layout/Controller/__init|Controller Board]], [[06-Firmware Architecture]]

#### 3.3.1 Visual Inspection

| Step | Action | Instrument | Pass Criteria | Record |
|:----:|--------|-----------|---------------|--------|
| CT-V01 | Inspect STM32G474RE LQFP64 solder joints | 10× magnifier or microscope | No bridges, all pins wetted, pin 1 aligned | ☐ P / ☐ F |
| CT-V02 | Inspect CAN transceiver (TCAN1044) solder joints and orientation | 10× magnifier | Correct orientation, no bridges | ☐ P / ☐ F |
| CT-V03 | Inspect QCA7000 PLC modem IC (if populated) | 10× magnifier | Correct orientation, no bridges | ☐ P / ☐ F |
| CT-V04 | Verify decoupling capacitors present on all power pins (MCU, CAN, PLC) | Visual | All marked positions populated | ☐ P / ☐ F |
| CT-V05 | Verify crystal oscillator marking and orientation | Visual | Correct frequency (8 MHz HSE), pin 1 correct | ☐ P / ☐ F |
| CT-V06 | Verify SWD header pin assignment matches ST-Link pinout | Schematic cross-check | SWDIO, SWCLK, NRST, GND in correct order | ☐ P / ☐ F |
| CT-V07 | Verify analog front-end: OPA2376 placement near ADC inputs, RC filter values | Visual + marking check | Correct values, short trace to ADC pins | ☐ P / ☐ F |

#### 3.3.2 Continuity and Resistance

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| CT-R01 | Verify no short: +3.3V to GND | DMM, diode mode | >2 V forward drop (MCU clamp); no dead short | ☐ P / ☐ F |
| CT-R02 | Verify no short: +5V to GND | DMM | No dead short (<1 Ω) | ☐ P / ☐ F |
| CT-R03 | Measure LDO output impedance (if on-board 3.3V LDO from 5V) | DMM | Input-to-output not shorted | ☐ P / ☐ F |
| CT-R04 | Verify CAN bus termination resistor value | DMM across CAN_H to CAN_L (S3) | 120 Ω ±5% (if on-board termination populated) | ___ Ω |

#### 3.3.3 First Power-On

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| CT-P01 | Apply +5V (1A limit) and +3.3V (0.5A limit) via P5. Measure quiescent current | Bench supply | +3.3V: 20–60 mA (MCU idle); +5V: <50 mA (CAN transceiver idle) | 3.3V: ___ mA, 5V: ___ mA |
| CT-P02 | Connect ST-Link V3. Verify SWD connection and MCU device ID read | STM32CubeProgrammer | Device ID = 0x469 (STM32G474) | ☐ P / ☐ F |
| CT-P03 | Flash test firmware (LED blink + UART "Hello" message) | ST-Link + terminal | LED blinks, UART output confirmed | ☐ P / ☐ F |
| CT-P04 | Verify 170 MHz system clock: toggle GPIO at max rate, measure on oscilloscope | Oscilloscope | GPIO toggle ≈ 85 MHz (170 MHz / 2) ±1% | ___ MHz |

#### 3.3.4 Functional Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| CT-F01 | HRTIM DLL calibration: run HAL_HRTIM_DLLCalibrationStart, verify completion | Firmware debug + oscilloscope on TA1 | DLL locks; 184 ps resolution achievable | ☐ P / ☐ F |
| CT-F02 | Generate PFC PWM on Timers A/B/C (65 kHz, 50% duty, 300 ns dead-time). Measure all 6 outputs | Oscilloscope | Frequency ±1%, duty ±1%, dead-time 300 ±20 ns, 120° phase shift between A/B/C | f: ___ kHz, DT: ___ ns |
| CT-F03 | Generate LLC PWM on Timers D/E/F (150 kHz, 50% duty, 100 ns dead-time, half-mode) | Oscilloscope | Frequency ±0.5%, duty 50% ±0.5%, dead-time 100 ±10 ns, 120° phase shift | f: ___ kHz, DT: ___ ns |
| CT-F04 | Sweep LLC frequency 100 → 300 kHz by updating PERxR. Verify smooth transition, no glitches | Oscilloscope (single-shot capture during ramp) | No missing pulses, no overlap, smooth frequency change | ☐ P / ☐ F |
| CT-F05 | ADC self-calibration on all 5 instances. Read reference voltage (internal VREFINT) | Firmware + UART dump | VREFINT reads within ±10 mV of 1.212 V | ___ V |
| CT-F06 | Apply 1.000 V DC to each analog input (P3 pins). Read ADC value | Bench supply + DMM + firmware | ADC reading within ±5 LSB of expected (1241 counts at 12-bit, 3.3V ref) | See report |
| CT-F07 | CAN bus loopback: send frame from PCAN-USB #1, receive on MCU, echo back, verify on PCAN-USB #2 | PCAN-View software | Frame integrity: all 8 data bytes match, no CRC errors, latency <1 ms | ☐ P / ☐ F |
| CT-F08 | CAN bus: transmit 100 frames/s for 60 s. Count errors | PCAN-View | 0 frame errors, 0 CRC errors | Errors: ___ |
| CT-F09 | HRTIM FLT1–FLT5 test: inject 3.3V → 0V transition on each fault pin. Verify PWM forces idle within 1 switching cycle | Oscilloscope + function gen (pulse) | PWM goes low within <1 µs of fault assertion | FLT1: ☐ P, FLT2: ☐ P, FLT3: ☐ P, FLT4: ☐ P, FLT5: ☐ P |
| CT-F10 | IWDG test: flash firmware that intentionally hangs. Verify MCU resets within 100 ms | Oscilloscope on NRST pin | Reset pulse observed within 100 ±10 ms | ___ ms |
| CT-F11 | NTC ADC readback: connect 10 kΩ NTC (or equivalent resistor) to ADC temp channel. Verify Steinhart-Hart conversion | Firmware + UART | Temperature reading within ±2°C of DMM-measured ambient | ___ °C vs ___ °C |
| CT-F12 | Fan PWM output: generate 25 kHz PWM at 0%, 50%, 100% duty. Measure on oscilloscope | Oscilloscope | Frequency 25 ±1 kHz, duty accurate ±2% | ☐ P / ☐ F |
| CT-F13 | GPIO relay/contactor drive outputs (S4 pins 1–4): toggle each, verify 3.3V logic levels | Oscilloscope / DMM | High >2.5 V, Low <0.4 V, rise/fall <100 ns | ☐ P / ☐ F |

#### 3.3.5 Protection Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| CT-X01 | WWDG test: verify NMI fires if refresh window missed | Firmware debug, oscilloscope on status GPIO | NMI handler executes, triggers graceful shutdown sequence in firmware | ☐ P / ☐ F |
| CT-X02 | Brown-out reset: reduce +3.3V supply slowly below BOR threshold (~2.7 V). Verify clean reset | Bench supply ramp down, oscilloscope on NRST | MCU resets cleanly, no latch-up | ☐ P / ☐ F |

#### 3.3.6 Thermal Characterization

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| CT-T01 | Run all peripherals (HRTIM, ADC, CAN, UART) at full rate for 1 hour. Measure MCU case temperature | Thermocouple on MCU package | T_case <85°C at 25°C ambient (40°C margin to 125°C Tj_max) | ___ °C |

---

### 3.4 AC-DC Board (Vienna PFC)

Reference: [[07-PCB-Layout/AC-DC/__init|AC-DC Board]], [[01-Topology Selection]], [[06-Firmware Architecture]] §4

#### 3.4.1 Visual Inspection

| Step | Action | Instrument | Pass Criteria | Record |
|:----:|--------|-----------|---------------|--------|
| AC-V01 | Inspect all 6 SiC MOSFET (HiP247) solder joints | 10× magnifier | Through-hole fill ≥75%, no cold joints, Kelvin source pin soldered | ☐ P / ☐ F |
| AC-V02 | Inspect all 6 SiC Schottky diode (TO-247) solder joints | 10× magnifier | Same criteria as AC-V01 | ☐ P / ☐ F |
| AC-V03 | Inspect 6× STGAP2SiC gate driver ICs (SO-8W) | 10× magnifier / microscope | No bridges, correct orientation, all pins wetted | ☐ P / ☐ F |
| AC-V04 | Verify snubber capacitor values and placement (<5 mm from drain) | Visual + marking | 100 nF C0G 630V; 4–8 per MOSFET | ☐ P / ☐ F |
| AC-V05 | Inspect EMI filter zone: CM choke, X-caps, Y-caps properly seated | Visual | No cracked ferrite, caps firmly soldered | ☐ P / ☐ F |
| AC-V06 | Verify DC bus capacitor polarity (series pairs) | Visual | Stripe (negative) matches PCB marking on all electrolytics | ☐ P / ☐ F |
| AC-V07 | Verify creepage: AC input to PE ≥10 mm, DC bus to PE ≥14 mm | Ruler/caliper | Per [[09-Protection and Safety]] §7.1.1 | ☐ P / ☐ F |
| AC-V08 | Check isolation slot/cutout between switching node and low-voltage signal area | 10× magnifier | Slot present and clear, no solder bridges | ☐ P / ☐ F |

#### 3.4.2 Continuity and Resistance

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-R01 | Measure DC bus capacitor banks: no short bus+ to bus− | DMM, initially shows low Ω (cap charging), rises | Final reading >1 MΩ | ☐ P / ☐ F |
| AC-R02 | Measure each boost inductor DCR (3×, external or board-mounted) | LCR meter, 1 kHz | Per design (typically 10–30 mΩ at 200 µH) | L1: ___ mΩ, L2: ___ mΩ, L3: ___ mΩ |
| AC-R03 | Measure each boost inductor L value | LCR meter, 10 kHz | 200 µH ±10% | L1: ___ µH, L2: ___ µH, L3: ___ µH |
| AC-R04 | Insulation resistance: AC input to DC bus | Megger, 500 VDC | >100 MΩ (diodes block at low voltage) | ___ MΩ |
| AC-R05 | Insulation resistance: DC bus to PE | Megger, 1000 VDC, 60 s | >100 MΩ | ___ MΩ |
| AC-R06 | Gate driver supply pins: verify no short +18V to GND or −5V to GND | DMM | >100 kΩ | ☐ P / ☐ F |

#### 3.4.3 First Power-On (Gate Drivers Only)

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-P01 | Apply gate drive supply (+18V / −5V) from Aux PSU or bench supply. Measure quiescent current | Bench supply, DMM | Each STGAP2SiC draws ~10–20 mA quiescent; total ~60–120 mA | ___ mA |
| AC-P02 | Verify STGAP2SiC UVLO release: ramp +18V slowly from 0. Gate output should enable at ~13 V | Oscilloscope on gate output, ramp supply | Gate output active above UVLO threshold (~13 V); inactive below | UVLO: ___ V |
| AC-P03 | Apply 3.3V PWM signal (65 kHz, 50%) to one gate driver input. Verify +18V/−5V gate output swing | Oscilloscope: Ch1 input, Ch2 gate output | V_GS swings from −5V to +18V, rise/fall <50 ns, correct dead-time | V_high: ___ V, V_low: ___ V |
| AC-P04 | Repeat AC-P03 for all 6 gate drivers | Same | All 6 drivers produce correct gate waveform | ☐ P / ☐ F (per driver) |

#### 3.4.4 First Power-On (Uncontrolled Rectification)

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-P05 | Apply 260 VAC 3-phase via P1b, MOSFETs OFF (no PWM). DC bus charges through body diodes | AC source (current-limited 5A), HV diff probe on DC bus | V_bus ≈ 260 × √2 × 0.95 ≈ 350 VDC (diode drop reduces slightly) | V_bus: ___ V |
| AC-P06 | Increase to 530 VAC. Verify V_bus ≈ 710 VDC (uncontrolled rectification) | Same + DMM | V_bus = 530 × √2 × 0.95 ≈ 710 VDC ±5% | V_bus: ___ V |
| AC-P07 | With V_bus established and a light resistive load on DC bus, begin soft-start: PFC PWM enabled at low duty (5%), verify bus voltage rises toward regulated setpoint | Oscilloscope + power analyzer | V_bus ramps smoothly, no current spikes > rated, PFC waveform clean | ☐ P / ☐ F |

#### 3.4.5 Functional Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-F01 | Full PFC regulation at 260 VAC, 15 kW (half load): V_bus regulated to 800 V, PF measured | Power analyzer 3P4W | V_bus = 800 V ±1%, PF ≥ 0.99, THDi ≤ 5% | V_bus: ___ V, PF: ___, THDi: ___% |
| AC-F02 | Full PFC regulation at 530 VAC, 30 kW: V_bus = 920 V | Power analyzer | V_bus = 920 V ±1%, PF ≥ 0.99, THDi ≤ 5%, I_in ≤ 60 A/phase | V_bus: ___ V, PF: ___, I_in: ___ A |
| AC-F03 | Phase balance: measure per-phase input current at 30 kW | Power analyzer | Phase currents balanced within ±3% | I_A: ___ A, I_B: ___ A, I_C: ___ A |
| AC-F04 | Efficiency at 530 VAC / 30 kW | Power analyzer (P_in 3P4W, P_out DC) | η ≥ 98% (per [[04-Thermal Budget]] §2.1: 98.7% target) | η = ___% |
| AC-F05 | Neutral point balance: V_cap_top − V_cap_bot < 10 V at rated load | DMM or oscilloscope | ΔV < 10 V | ΔV: ___ V |
| AC-F06 | Switching waveform quality: capture V_DS and I_phase at 530 VAC / 30 kW | Oscilloscope (HV probe + Rogowski) | Clean switching, no ringing > 30% of V_bus, no double-pulsing | ☐ P / ☐ F |

#### 3.4.6 Protection Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-X01 | DC bus OVP: increase V_bus setpoint above 960 V threshold (or inject via comparator test point) | Oscilloscope on HRTIM FLT3 and PWM outputs | All PFC PWM forced idle within <5 µs of 960 V crossing (per [[09-Protection and Safety]] §2.3) | Response: ___ µs |
| AC-X02 | Input OCP: apply current step >66 A on one phase | Oscilloscope + current probe | PFC duty cycle reduces within 1 ms; hard trip if sustained >100 ms | ☐ P / ☐ F |
| AC-X03 | Phase loss: disconnect one AC phase while running at 50% load | Oscilloscope, CAN log | PLL detects within 20 ms, LLC disabled in 20 ms, PFC disabled in 30 ms (per [[08-Power-On Sequence and Inrush Management]] §6.4) | Detection: ___ ms |
| AC-X04 | DESAT test (if STGAP2SiC DESAT is routed): inject V_DS above 8 V threshold on one MOSFET gate driver | External HV diode injection | Soft turn-off within <2 µs, FAULT pin asserts (per [[09-Protection and Safety]] §3.4.2) | Response: ___ µs |

#### 3.4.7 Thermal Characterization

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| AC-T01 | 1-hour run at 530 VAC / 30 kW with production-spec fans. Thermocouples on: 2× MOSFET heatsink, 2× diode heatsink, 1× boost inductor, 1× ambient | Thermocouple logger + thermal camera | MOSFET heatsink <95°C, PFC diode <108°C per [[04-Thermal Budget]] §4.2 (at 55°C ambient: adjust for lab ambient) | See report |
| AC-T02 | Thermal image of full board; identify any unexpected hot spots | Thermal camera | No component >120°C; no unexpected hot spots on traces or connectors | ☐ P / ☐ F |

---

### 3.5 DC-DC Board (LLC Resonant Converter)

Reference: [[07-PCB-Layout/DC-DC/__init|DC-DC Board]], [[02-Magnetics Design]], [[06-Firmware Architecture]] §5

#### 3.5.1 Visual Inspection

| Step | Action | Instrument | Pass Criteria | Record |
|:----:|--------|-----------|---------------|--------|
| DC-V01 | Inspect all 6 primary SiC MOSFETs (1200V, TO-247) solder joints | 10× magnifier | Through-hole fill ≥75%, no cold joints | ☐ P / ☐ F |
| DC-V02 | Inspect all 6 secondary SiC MOSFETs/diodes (650V, TO-247) solder joints | 10× magnifier | Same criteria | ☐ P / ☐ F |
| DC-V03 | Inspect 3× transformer mounting and pin connections | Visual | Firmly seated, all pins soldered, no cracked core | ☐ P / ☐ F |
| DC-V04 | Inspect primary-to-secondary isolation barrier (PCB slot) | 10× magnifier | Slot ≥2 mm wide, no solder/copper bridges, creepage ≥14 mm per [[09-Protection and Safety]] §7.1.1 | ☐ P / ☐ F |
| DC-V05 | Verify snubber resistor + capacitor values on each primary MOSFET (10 Ω + 1 nF) | Visual + marking | 6 sets populated, correct values (mandatory per DC-DC board overview) | ☐ P / ☐ F |
| DC-V06 | Inspect resonant capacitor arrays (C0G MLCC) — all populated, no cracks | 10× magnifier | All caps present, no visible cracks | ☐ P / ☐ F |
| DC-V07 | Verify gate driver IC orientation (STGAP2SiC × 6, primary + secondary) | Visual | Pin 1 correct on all 6 drivers | ☐ P / ☐ F |
| DC-V08 | Verify output capacitor polarity and DC bus input cap polarity | Visual | Stripe matches marking | ☐ P / ☐ F |

#### 3.5.2 Continuity and Resistance

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-R01 | Measure DC bus input capacitance: no short bus+ to bus− | DMM | Initially low Ω (charging), rises to >1 MΩ | ☐ P / ☐ F |
| DC-R02 | Measure output capacitance: no short out+ to out− | DMM | Same behavior | ☐ P / ☐ F |
| DC-R03 | Measure each resonant inductor DCR (3×) | LCR meter, 1 kHz | Per design (typically 20–50 mΩ for 33 µH) | Lr_A: ___ mΩ, Lr_B: ___ mΩ, Lr_C: ___ mΩ |
| DC-R04 | Measure each resonant inductor L value (3×) | LCR meter, 100 kHz | 33 µH ±10% (per [[02-Magnetics Design]]) | Lr_A: ___ µH, Lr_B: ___ µH, Lr_C: ___ µH |
| DC-R05 | Measure each resonant capacitor value (3 banks) | LCR meter, 100 kHz | Per design ±5% (per [[02-Magnetics Design]]) | Cr_A: ___ nF, Cr_B: ___ nF, Cr_C: ___ nF |
| DC-R06 | Calculate resonant frequency from Lr and Cr measurements | Calculation | f_r = 1/(2π√(Lr·Cr)) within ±5% of 150.5 kHz target | f_r_A: ___ kHz, f_r_B: ___ kHz, f_r_C: ___ kHz |
| DC-R07 | Measure each transformer primary winding DCR (3×) | LCR meter | Per design (typically 20–80 mΩ) | TX_A: ___ mΩ, TX_B: ___ mΩ, TX_C: ___ mΩ |
| DC-R08 | Measure each transformer secondary winding DCR (3×) | LCR meter | Per design | TX_A_sec: ___ mΩ, TX_B_sec: ___ mΩ, TX_C_sec: ___ mΩ |
| DC-R09 | Insulation resistance: primary side to secondary side (across isolation barrier) | Megger, 2500 VDC, 60 s | >100 MΩ (reinforced insulation) | ___ MΩ |
| DC-R10 | Insulation resistance: DC bus to PE; output to PE | Megger, 1000 VDC | >100 MΩ each | Bus-PE: ___ MΩ, Out-PE: ___ MΩ |

#### 3.5.3 First Power-On (Gate Drivers Only)

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-P01 | Apply gate drive supply (+18V/−5V) to primary and secondary drivers. Measure quiescent current | Bench supply | Total ~120–180 mA for 6 drivers | ___ mA |
| DC-P02 | Verify UVLO on each driver: ramp +18V; gate output active only above ~13 V | Oscilloscope | UVLO threshold ≈ 13 V on all 6 drivers | ☐ P / ☐ F |
| DC-P03 | Apply 150 kHz PWM (50% duty, half-mode) to each primary driver input. Verify gate swing +18V/−5V | Oscilloscope | Clean gate waveform, rise <50 ns, dead-time as set | ☐ P / ☐ F |
| DC-P04 | Apply sync-rect PWM to each secondary driver input. Verify gate output | Oscilloscope | Correct timing relative to primary | ☐ P / ☐ F |

#### 3.5.4 First Power-On (Low Voltage / Low Power)

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-P05 | Apply 100 VDC to DC bus input (P2) via HV supply, 1A limit. Enable LLC at f_max (300 kHz). Verify output voltage appears | Oscilloscope + DMM on output | V_out appears (low gain at f_max); no arcing, no smoke | V_out: ___ V |
| DC-P06 | Gradually reduce frequency toward f_r (150 kHz). Verify V_out increases as expected from LLC gain curve | Oscilloscope + DMM | V_out increases smoothly per [[03-LLC Gain Curve Verification]] | ☐ P / ☐ F |

#### 3.5.5 Functional Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-F01 | LLC regulation at V_bus = 800 V, V_out = 400 V, 15 kW (half load) | Power analyzer (DC-DC) | V_out = 400 V ±0.5%, I_out within regulation | V_out: ___ V, I_out: ___ A |
| DC-F02 | LLC regulation at V_bus = 920 V, V_out = 1000 V, 30 kW (full rated) | Power analyzer | V_out = 1000 V ±0.5%, I_out = 30 A, η measured | V_out: ___ V, η: ___% |
| DC-F03 | LLC regulation at V_bus = 920 V, V_out = 300 V, 30 kW (100 A) — constant power point | Power analyzer | V_out = 300 V ±1%, I_out = 100 A | V_out: ___ V, I_out: ___ A |
| DC-F04 | Efficiency at V_bus = 920 V, V_out = 800 V, 30 kW | Power analyzer | η ≥ 98% (per [[04-Thermal Budget]] §2.2: 98.3% target) | η: ___% |
| DC-F05 | Phase current balance: measure resonant current in each of 3 phases at 30 kW | 3× Rogowski coils + oscilloscope | Phase currents balanced within ±2% (per DC-DC board design target) | I_A: ___ A, I_B: ___ A, I_C: ___ A |
| DC-F06 | ZVS verification: capture V_DS of primary MOSFET at turn-on, verify voltage = 0 before gate rises | Oscilloscope (HV probe + gate probe) | V_DS < 50 V at gate turn-on (ZVS achieved) at all rated operating points | ☐ P / ☐ F |
| DC-F07 | Primary overshoot measurement: capture V_DS peak at turn-off at 920 V bus, 30 kW | Oscilloscope (HV probe, single-shot, full BW) | V_DS_peak ≤ 1061 V (with snubber, per DC-DC board design: 139 V margin to 1200 V) | V_DS_pk: ___ V |

#### 3.5.6 Protection Tests

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-X01 | Output OVP (hardware): inject voltage above 1100 V threshold on comparator test point | Oscilloscope on HRTIM FLT4 and PWM | All LLC PWM forced idle within <1 µs (per [[09-Protection and Safety]] §2.1.2); latch-type, requires reset | Response: ___ µs |
| DC-X02 | Output OVP (software): increase V_out setpoint to 105% of target, verify trip | CAN log + oscilloscope | LLC PWM disabled within 100 µs, contactor opens 10 ms later | ☐ P / ☐ F |
| DC-X03 | Output OCP (cycle-by-cycle): force output current above 110 A threshold | Electronic load CC mode at 112 A | Pulse skipping observed, output voltage droops, no hard fault | ☐ P / ☐ F |
| DC-X04 | Output OCP (hardware): force current above 120 A | Electronic load | All LLC PWM latched off within <500 ns, auto-retry after 1 s (per [[09-Protection and Safety]] §3.1.2) | Response: ___ ns |
| DC-X05 | DESAT detection: inject V_DS > 8 V on one primary MOSFET DESAT pin | External injection | Soft turn-off within <2 µs, fault latch asserts (per [[09-Protection and Safety]] §3.4.2) | Response: ___ µs |

#### 3.5.7 Thermal Characterization

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| DC-T01 | 1-hour run at V_bus = 920 V, V_out = 800 V, 30 kW with production fans. Thermocouples on: primary MOSFET heatsink, secondary diode heatsink, transformer core, ambient | Thermocouple logger + thermal camera | Primary MOSFET HS <93°C, secondary diode HS <133°C, transformer <120°C per [[04-Thermal Budget]] §4.2 (adjust for lab ambient vs. 55°C spec) | See report |
| DC-T02 | Thermal image: identify hot spots on resonant inductors, capacitors, bus bars | Thermal camera | No unexpected component >130°C | ☐ P / ☐ F |

---

## 4. System Integration Tests

### 4.1 First System Power-On

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| SY-01 | Assemble all 5 boards on DUT plate with bus bars, harnesses, and fans. Double-check all connections | Visual inspection | All connectors seated, bus bar bolts torqued, harnesses keyed correctly | ☐ P / ☐ F |
| SY-02 | Apply 260 VAC 3-phase, current-limited to 10 A. Observe full startup sequence | Oscilloscope (V_bus, V_out), CAN log | Sequence matches [[08-Power-On Sequence and Inrush Management]] §5.2: NTC pre-charge → relay bypass → PFC soft-start → LLC soft-start → contactor close | ☐ P / ☐ F |
| SY-03 | Verify startup timing: T0 (AC on) to T6 (READY) | Oscilloscope + CAN timestamp | Total ≤6 s (per spec; T0→T2 ~3 s, T2→T3 ~0.2 s, T3→T4 ~0.8 s, T4→T5 ~1.5 s, T5→T6 ~0.2 s) | Total: ___ s |
| SY-04 | Verify CAN status frame reports RUN state after startup | PCAN-USB + PCAN-View | Module state = RUN (0x01 status frame, per [[06-Firmware Architecture]] §6.2) | ☐ P / ☐ F |
| SY-05 | Repeat SY-02/SY-03 at 530 VAC | Same | Same timing criteria; V_bus reaches ~710 V during pre-charge | Total: ___ s |

### 4.2 Efficiency Sweep

Measure end-to-end efficiency (AC input to DC output, including all boards and harness losses) at 8 operating points.

**Power analyzer setup:** 3P4W on AC input (3 voltage channels + 3 current channels), DC power on output (+V and +I channels). 6 channels total.

| # | V_in (VAC) | V_out (VDC) | P_out (kW) | Load (%) | Expected η | Measured η | P/F |
|:-:|:----------:|:-----------:|:----------:|:--------:|:----------:|:----------:|:---:|
| 1 | 400 | 400 | 7.5 | 25% | >95% | ___% | ☐ |
| 2 | 400 | 400 | 15 | 50% | >96% | ___% | ☐ |
| 3 | 400 | 400 | 22.5 | 75% | >96.5% | ___% | ☐ |
| 4 | 400 | 400 | 30 | 100% | >96% | ___% | ☐ |
| 5 | 530 | 800 | 7.5 | 25% | >95% | ___% | ☐ |
| 6 | 530 | 800 | 15 | 50% | >96% | ___% | ☐ |
| 7 | 530 | 800 | 22.5 | 75% | >96.5% | ___% | ☐ |
| 8 | 530 | 800 | 30 | 100% | >96% | ___% | ☐ |

> [!note] Power analyzer accuracy must be ≤0.05% for meaningful efficiency data at >96%.

### 4.3 CC/CV Mode Transitions

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| SY-10 | Set CC mode at 50 A, gradually increase load voltage from 300 → 800 V. Verify transition to CV at setpoint | Electronic load (CV mode ramp), oscilloscope on V_out + I_out | Smooth transition CC → CV, V_out overshoot <5% of setpoint, no oscillation | Overshoot: ___% |
| SY-11 | Set CV mode at 800 V, gradually increase load current 0 → 50 A → 100 A. Verify transition to CC at 100 A | Electronic load (CC mode ramp), oscilloscope | Smooth transition CV → CC, I_out overshoot <5 A, settling <100 ms | Overshoot: ___ A |
| SY-12 | Slew rate test: step V_out setpoint from 400 V to 800 V via CAN command. Measure rise time | CAN command + oscilloscope | Rise time 100–500 ms (controlled ramp, not step), no ring | Rise: ___ ms |

### 4.4 Protection Coordination

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| SY-20 | Output OVP end-to-end: force V_out above 105% of setpoint (software) then 110% of max (hardware) | Oscilloscope, CAN log | Software OVP: LLC off in <100 µs, contactor open in 10 ms. Hardware OVP: LLC off in <1 µs, latches | ☐ P / ☐ F |
| SY-21 | DC bus OVP: simulate bus overshoot to 960 V | Oscilloscope on HRTIM FLT3 | PFC PWM disabled <5 µs; LLC continues briefly to discharge bus; auto-retry after 5 s if <900 V | ☐ P / ☐ F |
| SY-22 | Phase loss: disconnect one AC phase at 50% load | Oscilloscope, CAN log | Detection in ≤20 ms (PLL), LLC off in 20 ms, contactor open in 25 ms, PFC off in 30 ms | Det: ___ ms |
| SY-23 | CAN timeout: disconnect CAN cable while running at 50% load | CAN log, oscilloscope on V_out | Derate to 50% in 50 ms; full shutdown if no recovery in 200 ms (per [[06-Firmware Architecture]] §6.3) | ☐ P / ☐ F |
| SY-24 | OTP simulation: heat one NTC with hot-air gun above 125°C warning threshold, then above 140°C trip | Thermocouple + CAN log | Warning at 125°C (fan boost + CAN warning); power reduction at 140°C; shutdown if no recovery | ☐ P / ☐ F |
| SY-25 | Fan failure: block one fan while running at 75% load. Monitor thermal response | Tachometer log, thermocouple logger | CAN warning within 2 s (RPM <50% setpoint); power derate if T rises; shutdown if all fans fail (per [[09-Protection and Safety]] §4.5) | ☐ P / ☐ F |
| SY-26 | E-stop: press E-stop at full load | Oscilloscope on V_out, V_bus | All power stages disabled within <100 ms; V_bus bleeds to <60 V within 5 s (per IEC 61851-23 §6.3.1) | Bleed time: ___ s |

### 4.5 CAN Stacking (Multi-Module)

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| SY-30 | 2-module current sharing: connect 2 PDU modules on shared CAN bus and common DC output. Set 60 kW total | PCAN-View, 2× power analyzers | Current imbalance ≤5% between modules (per [[06-Firmware Architecture]] §6.3) | Imbalance: ___% |
| SY-31 | Hot-swap: disable module #2 via CAN while running at 40 kW total (2 modules). Verify module #1 absorbs load to 30 kW without output interruption | CAN log, oscilloscope on V_out | V_out transient <5% during handoff, module #1 reaches 30 kW within 500 ms | V_dip: ___% |
| SY-32 | Master failover: disconnect master module's CAN while 2 modules run. Verify slave assumes master role | CAN log | Slave detects timeout, promotes to master, output maintained within 200 ms | Failover: ___ ms |
| SY-33 | 5-module test (if available): 150 kW total, verify current sharing across all 5 | 5× CAN status frames | All modules within ±5% of mean current | Max imbalance: ___% |

### 4.6 EMC Pre-Scan

| Step | Action | Instrument / Settings | Pass Criteria | Record |
|:----:|--------|----------------------|---------------|--------|
| SY-40 | Conducted emissions: connect LISN on each AC input phase. Measure 150 kHz – 30 MHz spectrum at 30 kW | LISN + spectrum analyzer, quasi-peak + average | Below EN 55032 Class B limits with ≥6 dB margin (pre-compliance) | See spectrum plot |
| SY-41 | Radiated near-field probe: scan around enclosure seams, cable entry points, and heatsink vents at 30 kW | Near-field H/E probe set + spectrum analyzer | No resonances exceeding Class B estimates by >10 dB | ☐ P / ☐ F |

---

## 5. Test Report Template

### 5.1 Per-Board Test Report

| Field | Value |
|-------|-------|
| **Board Name** | _________________________ |
| **Board Designation** | _________________________ |
| **Serial Number** | _________________________ |
| **PCB Revision** | _________________________ |
| **Firmware Version** (if applicable) | _________________________ |
| **Test Date** | _________________________ |
| **Test Engineer** | _________________________ |
| **Lab Temperature** | _____ °C |
| **Lab Humidity** | _____ % RH |

**Test Results:**

| Test ID | Description | Measured Value | Pass Criteria | P/F | Notes |
|---------|-------------|---------------|---------------|:---:|-------|
| | | | | ☐ | |
| | | | | ☐ | |
| | | | | ☐ | |

*(Copy rows from the relevant board procedure section above)*

### 5.2 Summary Table

| Board | Total Tests | Passed | Failed | N/A | Overall |
|-------|:----------:|:------:|:------:|:---:|:-------:|
| Power Entry (PE-CONT-01) | | | | | ☐ PASS / ☐ FAIL |
| Aux PSU (AUX-PSU-01) | | | | | ☐ PASS / ☐ FAIL |
| Controller | | | | | ☐ PASS / ☐ FAIL |
| AC-DC (VPFC-01) | | | | | ☐ PASS / ☐ FAIL |
| DC-DC (LLC-01) | | | | | ☐ PASS / ☐ FAIL |
| **System Integration** | | | | | ☐ PASS / ☐ FAIL |

### 5.3 Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Engineer | | | |
| Design Engineer | | | |
| Quality | | | |

### 5.4 Non-Conformance Log

| NCR # | Test ID | Description of Failure | Root Cause | Corrective Action | Status |
|:-----:|---------|----------------------|------------|-------------------|:------:|
| 1 | | | | | ☐ Open / ☐ Closed |
| 2 | | | | | ☐ Open / ☐ Closed |

---

## 6. Safety Warnings

> [!danger] HAZARDOUS VOLTAGES
> This PDU operates at voltages up to **1000 VDC output** and **920 VDC internal DC bus** (peak AC input: 750 Vpk). Contact with these voltages can cause **fatal electric shock**.

### 6.1 Mandatory Discharge Procedure

Before touching any board or conductor after power-off:

1. **Disconnect** AC source and electronic load
2. **Wait ≥5 minutes** for DC bus bleed resistors to discharge capacitors
3. **Verify** V_bus < 10 V using a DMM (rated ≥1000 VDC CAT III)
4. **Verify** V_out < 10 V using same DMM
5. **Apply discharge probe** (10 kΩ / 50 W) across DC bus and output bus as a secondary measure
6. **Only then** handle boards, change connections, or attach probes

> [!warning] Stored Energy
> DC bus capacitors store up to **73 J at 920 V** (per [[08-Power-On Sequence and Inrush Management]] §1.2). This is sufficient to cause severe burns and cardiac arrest. Never assume capacitors are discharged — always measure first.

### 6.2 PPE Requirements

| Item | Requirement | When Required |
|------|------------|---------------|
| HV-rated gloves | Class 0 (1000 V) per IEC 60903 | Any time boards are energized or capacitors may be charged |
| Safety glasses | ANSI Z87.1 / EN 166 | All lab work |
| Insulating mat | IEC 61111, rated ≥1000 V | Floor mat at test bench |
| Closed-toe shoes | Non-conductive soles | All lab work |
| Arc-flash PPE | Not required at 30 kW (below arc-flash threshold for enclosed design) | Optional for open-frame testing at >20 kW |

### 6.3 Probe Safety Rules

- **Always use rated probes:** HV differential probes rated ≥1500 V for all measurements on DC bus, output bus, and AC mains
- **Never use grounded oscilloscope clips** on floating circuits — use differential probes or isolated inputs
- **Ground clip warning:** The oscilloscope ground clip is connected to mains earth. Clipping it to a floating high-voltage node will create a **short circuit to earth**, potentially destroying the probe, oscilloscope, and DUT, and causing arc flash
- **Probe attachment order:** Connect ground lead first, then signal lead. Reverse for disconnection
- **Current probes:** Zero-flux (Hall) probes must be degaussed before each measurement session

### 6.4 E-Stop and Buddy System

- **E-stop** must be wired and tested before any power-on test. It must disconnect the AC source enable signal and the DC load enable signal
- **Buddy system:** No one should perform HV testing alone. A second person must be present and know the location of the E-stop, first aid kit, and AED
- **Barrier:** Use a physical barrier (chain/rope + "HIGH VOLTAGE — TESTING IN PROGRESS" sign) around the test bench when energized

### 6.5 Hipot Test Safety

- **Clear the area** — hipot tests apply up to 5 kV AC. Anyone touching the DUT or connected cables will receive a lethal shock
- **Disconnect all signal harnesses** (S1–S4) and electronic loads before hipot testing
- **Short each domain internally** (e.g., all three AC phases together, DC bus+ to bus−) to avoid stressing components
- **Use a hipot tester with a foot switch** — operator can release instantly if needed
- **After hipot:** wait for tester to discharge, verify <50 V on DUT before handling

---

## 7. Cross-References

| Document | Relevance |
|----------|-----------|
| [[07-PCB-Layout/00-Board Partitioning]] | Connector pinouts P1a–P5, S1–S4; 5-board architecture |
| [[09-Protection and Safety]] | All protection thresholds and hipot requirements |
| [[08-Power-On Sequence and Inrush Management]] | Startup timing, NTC/relay/contactor specs, discharge |
| [[06-Firmware Architecture]] | HRTIM map, ADC channels, CAN frames, fault inputs |
| [[04-Thermal Budget]] | Loss allocation, temperature limits per component |
| [[07-PCB-Layout/Power-Entry/__init\|Power Entry Board]] | PE-CONT-01 component references |
| [[07-PCB-Layout/AC-DC/__init\|AC-DC Board]] | Vienna PFC board references |
| [[07-PCB-Layout/DC-DC/__init\|DC-DC Board]] | LLC board references |
| [[07-PCB-Layout/Controller/__init\|Controller Board]] | Controller board references |
| [[07-PCB-Layout/Aux-PSU/__init\|Aux PSU Board]] | Auxiliary PSU board references |
| [[Commissioning Procedure]] | Field-level commissioning (post-lab verification) |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
