---
tags: [pdu, pcb-layout, aux-psu, filtering, ldo, regulation, ripple, gate-drive]
created: 2026-02-22
status: draft
---

# 04 — Output Filtering and Regulation

## Purpose

This document specifies the output filtering and post-regulation design for each Aux PSU rail. The flyback converter produces raw rectified voltages from its multiple secondary windings; these must be filtered and regulated to meet the stringent ripple and noise specifications required by sensitive downstream loads — particularly the gate driver supplies (where ripple can cause shoot-through or gate oxide stress) and the MCU logic supply (where noise corrupts ADC readings).

## Ripple Specification Summary

| Rail | Voltage | Current | Max Ripple (pk-pk) | Max Noise (20 MHz BW) | Load Type | Criticality |
|------|---------|---------|-------------------|----------------------|-----------|-------------|
| VDRV_AC (+18 V) | 18 V | 0.5 A | 100 mV | 200 mV | Gate drivers (AC-DC board) | High |
| VNEG_AC (−5 V) | −5 V | 0.2 A | 50 mV | 100 mV | Negative gate bias (AC-DC) | High |
| VDRV_DC (+18 V) | 18 V | 0.5 A | 100 mV | 200 mV | Gate drivers (DC-DC board) | High |
| VNEG_DC (−5 V) | −5 V | 0.2 A | 50 mV | 100 mV | Negative gate bias (DC-DC) | High |
| +5 V | 5 V | 1.0 A | 50 mV | 100 mV | CAN transceiver, digital I/O | Medium |
| +3.3 V | 3.3 V | 0.5 A | 30 mV | 50 mV | MCU logic, ADC reference | Very High |
| +12 V_FAN | 12 V | 2.0 A | 200 mV | 500 mV | Fan motor | Low |
| STBY (3.3 V) | 3.3 V | 50 mA | 50 mV | 100 mV | Standby wake logic | Medium |

> [!tip] Ripple vs. Noise Distinction
> **Ripple** is the fundamental switching frequency component (65–130 kHz) and its harmonics. **Noise** includes all high-frequency content up to 20 MHz, including switching transient spikes and ringing. The output filter must address both — the LC filter handles fundamental ripple while ceramic decoupling caps handle high-frequency noise.

## Per-Rail Filter Design

### +18 V Gate Drive Rails (VDRV_AC, VDRV_DC)

Each +18 V rail is derived from a dedicated secondary winding and rectified by a Schottky diode. The gate drive supply is the most layout-sensitive output because ripple directly modulates the gate-source voltage of the SiC MOSFETs.

#### Filter Topology: LC + Ceramic Decoupling

```
From transformer    D_rect     L_out        To P4 connector
secondary pin ──→ ──|>|── ──┤LLLL├── ──┬── ──→ VDRV (+18V)
                              22 uH     │
                                    ┌───┴───┐
                                    │ C_bulk│ 100 uF / 25 V
                                    │ (alum)│ electrolytic
                                    └───┬───┘
                                        │
                                    ┌───┴───┐
                                    │ C_cer │ 10 uF / 25 V
                                    │ (X7R) │ ceramic
                                    └───┬───┘
                                        │
                                    ┌───┴───┐
                                    │ C_hf  │ 100 nF / 25 V
                                    │ (C0G) │ ceramic
                                    └───┬───┘
                                        │
                                    ── RTN (isolated return)
```

#### Component Selection

| Component | Value | Package | Rating | Notes |
|-----------|-------|---------|--------|-------|
| L_out | 22 uH | Shielded SMD (WE-PD series, 7x7 mm) | 1 A sat, DCR <200 mohm | Shielded to prevent coupling to adjacent domains |
| C_bulk | 100 uF | Radial electrolytic, 8x11 mm | 25 V, 105°C, low ESR (<200 mohm) | Handles bulk energy storage for load transients |
| C_cer | 10 uF | 1206 X7R | 25 V | Low ESR, handles mid-frequency ripple |
| C_hf | 100 nF | 0603 C0G | 25 V | High-frequency noise suppression |
| D_rect | Schottky, 100 V / 1 A | SMA (DO-214AC) | Vf < 0.5 V at 0.5 A | Low forward voltage for efficiency |

#### Ripple Calculation

At 65 kHz, 0.5 A load, 18 V output, duty cycle ~0.35:

$$\Delta V_{ripple} = \frac{I_{out}}{C_{cer} \cdot f_{sw}} = \frac{0.5}{10 \times 10^{-6} \times 65000} \approx 77 \text{ mV pp (ceramic alone)}$$

With the LC filter (22 uH + 10 uF ceramic):

$$f_{LC} = \frac{1}{2\pi\sqrt{LC}} = \frac{1}{2\pi\sqrt{22 \times 10^{-6} \times 10 \times 10^{-6}}} \approx 10.7 \text{ kHz}$$

Attenuation at 65 kHz: $(65/10.7)^2 \approx 37\times$ or ~31 dB

Resulting ripple after LC filter: $\frac{77}{37} \approx 2.1$ mV pp — well within the 100 mV specification.

> [!tip] Inductor Selection — Shielded Type Required
> Use a **shielded** SMD power inductor (e.g., Wurth WE-PD, TDK CLF, or Coilcraft XAL series). Unshielded inductors radiate magnetic field that can couple into adjacent gate drive domains, defeating the functional isolation. The shielded construction confines the magnetic flux within the ferrite.

#### Placement Rules

1. **D_rect** within 5 mm of transformer secondary pin
2. **L_out** immediately after D_rect cathode (no long trace between diode and inductor)
3. **C_bulk** within 10 mm of L_out output, close to P4 connector
4. **C_cer** directly at the P4 connector pins (last cap before the cable)
5. **C_hf** adjacent to C_cer, between C_cer and connector pad

### −5 V Negative Gate Bias Rails (VNEG_AC, VNEG_DC)

The −5 V rails provide negative turn-off bias for the SiC MOSFET gates, ensuring reliable turn-off and preventing false turn-on from dV/dt-induced gate charge.

#### Filter Topology: LC Filter

```
From transformer    D_rect     L_out
sec. (−5V tap) ──→ ──|>|── ──┤LLLL├── ──┬── ──→ VNEG (−5V)
                              10 uH     │
                                    ┌───┴───┐
                                    │ 47 uF │ electrolytic
                                    └───┬───┘
                                    ┌───┴───┐
                                    │ 4.7 uF│ ceramic X7R
                                    └───┬───┘
                                        │
                                    ── RTN (same domain as +18V)
```

| Component | Value | Package | Rating | Notes |
|-----------|-------|---------|--------|-------|
| L_out | 10 uH | Shielded SMD, 5x5 mm | 0.5 A sat, DCR <300 mohm | Lower inductance OK — less current |
| C_bulk | 47 uF | Radial electrolytic, 6x7 mm | 10 V, 105°C | Low ESR |
| C_cer | 4.7 uF | 0805 X7R | 10 V | Mid-frequency filtering |

**Ripple at 65 kHz, 0.2 A:** approximately 0.7 mV pp after LC filter — well within 50 mV spec.

> [!warning] −5 V Rail Polarity
> The −5 V rail is negative with respect to the isolated return (RTN_AC or RTN_DC). Verify that the rectifier diode is oriented correctly — the diode cathode connects to the isolated return, and the anode connects through the inductor to the −5 V output. An incorrectly oriented diode will produce +5 V instead of −5 V and may damage gate driver ICs.

### +12 V Fan Drive Rail

The fan motor is tolerant of ripple and noise. The +12 V rail has the most relaxed filtering requirements but carries the highest current (2 A).

#### Filter Topology: Direct from Winding + Bulk Cap

```
From transformer    D_rect
sec. (+12V) ────→ ──|>|── ──┬── ──→ +12V_FAN
                             │
                         ┌───┴───┐
                         │ 220 uF│ electrolytic (low ESR)
                         └───┬───┘
                         ┌───┴───┐
                         │ 22 uF │ ceramic X7R 1210
                         └───┬───┘
                             │
                         ── SEC_GND
```

| Component | Value | Package | Rating | Notes |
|-----------|-------|---------|--------|-------|
| C_bulk | 220 uF | Radial electrolytic, 10x12 mm | 16 V, 105°C, ESR <100 mohm | Main energy storage |
| C_cer | 22 uF | 1210 X7R | 16 V | Ripple current handling |
| D_rect | Schottky, 30 V / 3 A | SMB (DO-214AA) | Vf < 0.45 V at 2 A | Low loss at high current |

No output inductor is required — the 220 uF electrolytic plus 22 uF ceramic provides sufficient filtering for the fan motor.

**Ripple estimate:** $\Delta V = I/(C \cdot f) = 2.0 / (22e{-6} \times 65000) \approx 140$ mV pp from ceramic; electrolytic further smooths to ~100 mV pp total. Within 200 mV spec.

### +5 V Logic Rail

The +5 V rail feeds the CAN transceiver and digital I/O. It requires moderate ripple performance and must be independently regulated.

#### Option A: Dedicated Winding + Rectifier + LDO

```
From transformer    D_rect      C_pre
sec. (+7–8V) ───→ ──|>|── ──┬── ──┬── ──→ LDO ──→ +5V
                              │    │           │
                          100 uF  10 uF    ┌──┴──┐
                                           │C_out│ 22 uF + 100 nF
                                           └──┬──┘
                                              │
                                           SEC_GND
```

LDO dropout loss: $(7.5 - 5.0) \times 1.0 = 2.5$ W — manageable with SOT-223 + thermal pour.

#### Option B: Small Buck Regulator from +12 V

```
+12V ──→ ┌──────────┐ ──→ +5V (1A)
         │ TPS5430  │
         │ Buck     │
SEC_GND ─│ Reg.     │── SEC_GND
         └──────────┘
```

Buck regulator efficiency: ~88% at 12 V to 5 V, 1 A. Dissipation: $5 \times 1.0 / 0.88 - 5 = 0.68$ W — much better than the 2.5 W LDO option.

> [!tip] Recommended: Option B (Buck Regulator)
> The buck regulator from +12 V is strongly preferred. It reduces the +5 V rail dissipation from 2.5 W (LDO) to 0.68 W (buck), saving 1.82 W of on-board heat. This also eliminates the need for a dedicated +7.5 V transformer winding, simplifying the transformer design. Use a small integrated buck like TPS54302 (SOT-23-6, 3 A) or TPS5430 (SOIC-8, 3 A).

#### +5 V Output Filtering (Either Option)

| Component | Value | Package | Notes |
|-----------|-------|---------|-------|
| C_out_bulk | 22 uF | 1206 X7R | LDO output or buck output cap |
| C_out_hf | 100 nF | 0603 C0G | High-frequency decoupling at connector |

### +3.3 V MCU Logic Rail

The +3.3 V rail is the most noise-sensitive output — it powers the MCU ADCs and any precision voltage references on the controller board. A low-noise LDO is mandatory.

#### LDO Selection: TPS7A20 or Equivalent

| Parameter | Specification |
|-----------|---------------|
| LDO IC | TPS7A2033 (or MCP1700, AP2112K-3.3) |
| Input | +5 V rail |
| Output | 3.3 V, 0.5 A |
| Dropout | <200 mV at 0.5 A |
| PSRR | >60 dB at 100 kHz |
| Output noise | <15 uV RMS (10 Hz – 100 kHz) |
| Package | SOT-23-5 or SOT-223 |

```
+5V ──┬── ┌──────────┐ ──┬── ──→ +3.3V
      │   │TPS7A2033 │   │
   C_in   │ LDO      │ C_out
   10 uF  └──────────┘ 22 uF + 100 nF + 10 nF
      │                   │
   SEC_GND             SEC_GND
```

#### Component Selection

| Component | Value | Package | Notes |
|-----------|-------|---------|-------|
| C_in | 10 uF | 0805 X7R, 10 V | LDO input cap — within 3 mm of VIN pin |
| C_out | 22 uF | 0805 X7R, 6.3 V | LDO output cap — within 3 mm of VOUT pin; check LDO stability requirements |
| C_hf_out | 100 nF | 0402 C0G, 6.3 V | High-frequency decoupling |
| C_noise | 10 nF | 0402 C0G | Noise reduction cap on NR pin (if available) |

#### Dropout Loss

$(5.0 - 3.3) \times 0.5 = 0.85$ W — dissipated in the LDO. Manageable with SOT-223 + 4 cm² thermal pour (see [[03-Thermal Layout]]).

#### Placement Rules

1. LDO placed **close to P5 connector** — the +3.3 V output trace to the connector should be <15 mm
2. Input capacitor (10 uF) within 3 mm of LDO VIN pin
3. Output capacitor (22 uF) within 3 mm of LDO VOUT pin
4. C0G decoupling caps adjacent to the output capacitor
5. Ground pour under LDO connects to SEC_GND via thermal vias
6. No high-current switching traces routed near the +3.3 V output path

> [!warning] LDO Stability — ESR Sensitivity
> Many LDOs are sensitive to output capacitor ESR. The TPS7A20 requires a minimum output capacitance of 1 uF with ESR <1 ohm. Ceramic capacitors (X7R, X5R) easily meet this. However, some older LDO designs require a minimum ESR (e.g., 0.1–1 ohm) for stability — verify the selected LDO's capacitor requirements before finalizing the BOM.

### Standby Rail (3.3 V, 50 mA)

The standby rail must be operational within 50 ms of the DC bus voltage appearing. It powers the MCU wake-up logic and the CAN transceiver in standby mode.

#### Implementation: Auxiliary Bias Winding + Small LDO

The flyback transformer's auxiliary (bias) winding on the primary side normally powers the PWM controller VCC. A separate small secondary winding (or a tap from an existing secondary) provides a standby voltage that is regulated by a micro-power LDO:

| Component | Value | Notes |
|-----------|-------|-------|
| LDO | MCP1700-3302 (SOT-23) | 250 mA max, 2 uA quiescent |
| C_in | 4.7 uF ceramic | Input from rectified standby winding |
| C_out | 4.7 uF ceramic | Standby output |

Placement: Near the transformer secondary side, within the logic domain (SEC_GND).

## Load Transient Response

### Gate Driver Transient

When the gate drivers switch SiC MOSFETs, the +18 V rail experiences a transient current step. The worst case occurs at maximum switching frequency when all drivers on one board switch simultaneously:

| Parameter | Value |
|-----------|-------|
| Gate charge per MOSFET (Qg) | ~100 nC (SiC, 650 V class) |
| Number of MOSFETs per board | 6 |
| Switching events per cycle | 2 (turn-on + turn-off) |
| Switching frequency | 65 kHz |
| Peak transient current | $6 \times 100 \times 10^{-9} \times 65000 \times 2 = 78$ mA average; **peaks up to 4 A for ~25 ns per event** |

The 100 uF electrolytic + 10 uF ceramic at the output must supply these transient peaks without excessive voltage droop:

$$\Delta V = \frac{I_{peak} \times t_{pulse}}{C_{cer}} = \frac{4 \times 25 \times 10^{-9}}{10 \times 10^{-6}} = 10 \text{ mV}$$

This is well within the 100 mV ripple budget. The ceramic capacitor handles the transient; the electrolytic handles the average current.

### Fan Motor Start-Up

The fan motor draws an inrush current of 3–5x the steady-state current at start-up (~6–10 A for a 2 A fan). The +12 V output cap must handle this:

$$\Delta V = \frac{I_{inrush} \times t_{start}}{C_{total}} = \frac{10 \times 0.01}{220 \times 10^{-6}} = 455 \text{ V}$$

This is clearly excessive — the 220 uF cap cannot support 10 A for 10 ms without significant droop. **Solution: soft-start the fan using a PWM drive from the controller.** The controller ramps fan PWM duty over 500 ms, limiting inrush.

> [!warning] Fan Inrush Current
> Do not connect the fan directly to the +12 V output. Use the controller's PWM output through a MOSFET to soft-start the fan. The +12 V_FAN rail on P5 should feed through a low-side MOSFET on the controller board, controlled by a PWM signal. This limits inrush and allows variable fan speed control based on temperature. See [[07-PCB-Layout/Controller/__init]] for fan drive circuit details.

## Output Connector Decoupling

The final line of defense for output noise is a decoupling capacitor placed **at the output connector pins** — as close to P4 and P5 as physically possible:

### P4 Connector (Gate Drive Outputs)

| Pin | Signal | Decoupling Cap | Package | Notes |
|-----|--------|---------------|---------|-------|
| 1 | VDRV_AC (+18 V) | 100 nF C0G + 10 uF X7R | 0603 + 0805 | Within 3 mm of pin 1 pad |
| 2 | VNEG_AC (−5 V) | 100 nF C0G + 4.7 uF X7R | 0603 + 0805 | Within 3 mm of pin 2 pad |
| 3 | RTN_AC | — | — | Return pin |
| 5 | VDRV_DC (+18 V) | 100 nF C0G + 10 uF X7R | 0603 + 0805 | Within 3 mm of pin 5 pad |
| 6 | VNEG_DC (−5 V) | 100 nF C0G + 4.7 uF X7R | 0603 + 0805 | Within 3 mm of pin 6 pad |
| 7 | RTN_DC | — | — | Return pin |

### P5 Connector (Logic + Fan Outputs)

| Pin | Signal | Decoupling Cap | Package | Notes |
|-----|--------|---------------|---------|-------|
| 1 | +5 V | 100 nF C0G + 10 uF X7R | 0603 + 0805 | Within 3 mm of pin 1 pad |
| 2 | +3.3 V | 100 nF C0G + 10 uF X7R | 0603 + 0805 | Within 3 mm of pin 2 pad |
| 3 | GND | — | — | Return pin |
| 4 | +12 V_FAN | 100 nF X7R + 22 uF X7R | 0603 + 1210 | Within 5 mm of pin 4 pad |

## Design Verification Checklist

- [ ] All output capacitors placed within specified distance of connectors and LDOs
- [ ] LC filter resonant frequencies verified below switching frequency for each rail
- [ ] LDO input/output caps meet manufacturer stability requirements (ESR, minimum capacitance)
- [ ] Shielded inductors used for gate drive rail filters
- [ ] −5 V diode polarity verified in schematic and layout
- [ ] +5 V rail uses buck regulator (not LDO from +12 V) to limit dissipation
- [ ] Fan inrush handled by external soft-start (not Aux PSU capacitors)
- [ ] Ground returns for each domain are separate (no shared current paths between domains)
- [ ] Decoupling caps at connector pins verified per placement rules

## Cross-References

- [[__init]] — Output rail summary, isolation domains
- [[02-Isolated Converter Layout]] — Transformer secondaries, rectifier placement
- [[03-Thermal Layout]] — LDO and regulator thermal management
- [[05-Safety and Isolation]] — Y-capacitor across isolation barrier for CM noise
- [[00-Board Partitioning]] — P4 and P5 connector pin definitions
- [[07-PCB-Layout/Controller/__init]] — Controller board, consumer of +5 V/+3.3 V/+12 V

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: per-rail filter design, ripple analysis, LDO selection, transient analysis |
