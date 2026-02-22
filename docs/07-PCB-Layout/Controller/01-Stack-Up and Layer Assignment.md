---
tags: [pdu, pcb-layout, controller, stack-up, impedance]
created: 2026-02-22
status: draft
---

# Stack-Up and Layer Assignment

This document defines the 4-layer PCB stack-up for the Controller Board of the 30 kW PDU. The stack-up is optimized for a **digital/mixed-signal control board** — not a power converter board — so the emphasis is on signal integrity, controlled impedance, and clean power distribution rather than high-current capacity.

## 1. Layer Stack-Up

| Layer | Name | Type | Cu weight | Material | Thickness |
|---|---|---|---|---|---|
| L1 | TOP | Signal + Components | 1 oz (35 µm) | — | 35 µm |
| — | Prepreg | Dielectric | — | FR-4 (Er ≈ 4.2) | 0.20 mm (200 µm) |
| L2 | GND | Continuous ground plane | 1 oz (35 µm) | — | 35 µm |
| — | Core | Dielectric | — | FR-4 (Er ≈ 4.4) | 0.80 mm (800 µm) |
| L3 | PWR | 3.3 V power plane | 1 oz (35 µm) | — | 35 µm |
| — | Prepreg | Dielectric | — | FR-4 (Er ≈ 4.2) | 0.20 mm (200 µm) |
| L4 | BOT | Signal + Components | 1 oz (35 µm) | — | 35 µm |

**Total board thickness:** approximately 1.57 mm (62 mil), within standard 1.6 mm tolerance.

> [!tip] Why this order matters
> Placing GND on L2 directly beneath L1 (the primary signal layer) gives every L1 trace a tight, low-inductance return path. The 200 µm prepreg spacing between L1 and L2 supports controlled impedance for CAN differential pairs and HRTIM outputs.

## 2. Controlled Impedance Targets

The following impedance values are required for specific signal classes. They must be communicated to the PCB fabricator with a tolerance of +/-10%.

### 2.1 Single-Ended Traces (50 ohm)

Used for general-purpose digital I/O, SPI clock/data, UART, and HRTIM outputs.

| Parameter | Value |
|---|---|
| Target impedance | 50 ohm |
| Reference layer | L2 (GND) |
| Trace width (L1 microstrip) | ~0.27 mm (10.6 mil) |
| Dielectric thickness to ref | 0.20 mm (200 µm) |
| Copper thickness | 35 µm (1 oz) |
| Dielectric constant | 4.2 (prepreg) |

Calculated using the microstrip approximation:

```
Z0 = (87 / sqrt(Er + 1.41)) * ln(5.98 * h / (0.8 * w + t))

where:
  Er = 4.2, h = 0.20 mm, w = 0.27 mm, t = 0.035 mm
  Z0 ≈ 50.2 ohm
```

### 2.2 Differential Pairs (100 ohm)

Used for the CAN bus differential pair (CANH / CANL) and any Ethernet differential pairs.

| Parameter | Value |
|---|---|
| Target impedance | 100 ohm differential |
| Reference layer | L2 (GND) |
| Trace width | 0.20 mm (8 mil) |
| Trace spacing (gap) | 0.18 mm (7 mil) |
| Dielectric thickness to ref | 0.20 mm (200 µm) |

> [!warning] Fabricator note
> Specify impedance control on the fabrication drawing. Request a **TDR coupon** on the panel for impedance verification. The fab should adjust trace widths to hit targets based on their actual prepreg thickness and Er.

## 3. Layer Assignment Rules

### 3.1 L1 — Top Signal/Component Layer

This is the **primary routing layer** and the component-side layer.

| Signal class | Routing on L1 |
|---|---|
| HRTIM PWM outputs (12 channels) | Yes — matched-length pairs |
| ADC analog inputs (6 channels) | Yes — guarded, short runs |
| SPI to QCA7000 PLC modem | Yes — 50 ohm controlled |
| CAN differential pair | Yes — 100 ohm controlled |
| MCU crystal / oscillator | Yes — short, guarded |
| General GPIO, LED, debug | Yes |

> [!tip] Analog routing priority
> All analog sense traces (current sense, voltage sense) **must** be routed on L1 directly above the continuous L2 GND plane. Never route analog signals on L4 where the reference is the L3 power plane — the power plane carries switching noise from decoupling transients.

### 3.2 L2 — Ground Plane

**This layer must be an unbroken, continuous copper pour connected to GND.**

Rules:
- No signal routing on L2 — it is a dedicated reference plane
- No splits, slots, or cutouts under any signal trace
- Vias passing through L2 must not create anti-pads larger than 0.6 mm to preserve plane continuity
- The only acceptable openings are via anti-pads and the board mounting holes

The continuous GND plane serves three critical functions:
1. **Return-current path** for all L1 and L4 signals
2. **Shielding** between L1 signals and L3 power
3. **Thermal spreading** for the STM32 exposed pad (if applicable)

### 3.3 L3 — Power Plane (3.3 V)

The 3.3 V power plane on L3 is partitioned into regions:

```
┌──────────────────────────────────────────────────┐
│                                                  │
│    3.3 V ANALOG           3.3 V DIGITAL          │
│    (AVDD, VREF+)          (VDD, VDDA)            │
│                                                  │
│    ┌──────────┐    FB     ┌───────────────────┐  │
│    │  Clean   │◀──────────│  Main 3.3 V from  │  │
│    │  analog  │  ferrite  │  Aux PSU          │  │
│    │  island  │  bead     │                   │  │
│    └──────────┘           └───────────────────┘  │
│                                                  │
│              5 V island (CAN transceiver)         │
│              ┌────────────┐                      │
│              │ 5 V local  │                      │
│              └────────────┘                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

- **Main 3.3 V digital**: largest region, feeds MCU digital VDD pins and all digital ICs
- **3.3 V analog island**: isolated from digital via a ferrite bead (e.g., BLM18PG221), feeds VREF+ and analog op-amp supply
- **5 V island**: small region near the TCAN1044, fed from Aux PSU 5 V rail via P5 connector

> [!warning] Plane partitioning caution
> Keep L3 splits narrow (0.5 mm gap) and run them **perpendicular** to the board's longest dimension. Never let a signal trace on L4 cross a split in L3 without a stitching via to L2 GND nearby — this avoids return-current discontinuities.

### 3.4 L4 — Bottom Signal/Component Layer

Secondary routing layer. Used for:

| Signal class | Notes |
|---|---|
| Non-critical digital signals | I2C, status LEDs, test points |
| Power distribution traces | 5 V, 12 V distribution from P5 |
| Component placement | Bypass capacitors, bulk caps, connectors |
| Short routing escapes | Fan-out from BGA/QFP pads if needed |

Avoid routing the following on L4:
- Analog sense signals (use L1 over L2 GND only)
- HRTIM PWM outputs (keep on L1 for matched impedance)
- CAN differential pair (keep on L1 for impedance control)

## 4. Via Strategy

### 4.1 Via Types

| Via type | Drill | Pad | Annular ring | Usage |
|---|---|---|---|---|
| Standard through-hole | 0.3 mm | 0.6 mm | 0.15 mm | Signal vias, general routing |
| Power via | 0.4 mm | 0.8 mm | 0.20 mm | VDD connections, bulk current |
| Stitching via | 0.3 mm | 0.6 mm | 0.15 mm | GND stitching, edge vias, guard rings |

### 4.2 Via Placement Rules

1. **Decoupling vias**: each bypass capacitor connects to its VDD and GND planes through a dedicated via pair, placed within 1 mm of the capacitor pad
2. **Signal transition vias**: when a signal moves from L1 to L4, place a GND stitching via within 1 mm of the signal via to provide a return-current path
3. **Thermal vias**: under the STM32 exposed pad, place a 3x3 array of 0.3 mm vias on 1.2 mm pitch, connected to L2 GND
4. **Edge stitching**: GND vias around the board perimeter at 2 mm pitch (see [[05-EMC and Grounding]])

> [!tip] Return-current stitching
> Every time a signal transitions between L1 and L4, the return current must also transition between L2 (GND reference for L1) and the reference for L4. Place a GND via adjacent to every signal via to ensure this transition is low-inductance.

## 5. Board Zoning and Placement Strategy

The 120 x 100 mm board is divided into functional zones. Component placement follows the zoning defined in the [[__init|Controller Board Overview]]:

| Zone | Location | Components |
|---|---|---|
| MCU | Center | STM32G474RE, crystal, boot config |
| Analog | West side | OPA2376 op-amps, RC filters, sense connectors |
| Digital / Support | East side | EEPROM, debug header, LEDs, test points |
| Communication | North edge | TCAN1044, Ethernet PHY, QCA7000, connectors |
| Power entry | Southeast corner | P5 connector, bulk caps, ferrite beads, LDO |
| PWM / Harness | South edge | P1 (PFC PWM), P2 (LLC PWM), P3 (analog sense) |

## 6. Fabrication Notes

| Parameter | Specification |
|---|---|
| Board material | FR-4, Tg ≥ 150 C |
| Minimum trace width | 0.15 mm (6 mil) |
| Minimum trace spacing | 0.15 mm (6 mil) |
| Minimum via drill | 0.3 mm (12 mil) |
| Surface finish | ENIG (for fine-pitch QFP and reliable contact) |
| Solder mask | Both sides, green |
| Silkscreen | Both sides, white |
| Impedance control | Yes — 50 ohm SE, 100 ohm diff (L1 referenced to L2) |
| Panelization | Per fab recommendation |

## 7. Cross-References

- [[__init|Controller Board Overview]] — board-level summary and block diagram
- [[02-Signal Integrity]] — trace routing rules for analog and PWM signals
- [[04-Power Distribution]] — decoupling and power plane design detail
- [[05-EMC and Grounding]] — edge stitching, ground strategy
- [[00-Board Partitioning]] — physical placement of controller within the PDU enclosure

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
