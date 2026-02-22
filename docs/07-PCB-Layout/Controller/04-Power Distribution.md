---
tags: [pdu, pcb-layout, controller, power-distribution, decoupling, ldo]
created: 2026-02-22
status: draft
---

# Power Distribution

This document describes the power distribution network (PDN) for the Controller Board. The board receives all power from the [[07-PCB-Layout/Aux-PSU/__init|Aux PSU Board]] via the P5 connector. There are no on-board switching regulators — only an LDO for clean analog supply and passive filtering. This keeps the controller board free of switching noise.

## 1. Power Rails Summary

| Rail | Voltage | Source | Max current | Purpose |
|---|---|---|---|---|
| 3.3 V digital (VDD) | 3.3 V +/- 3% | Aux PSU via P5 | 500 mA | MCU, digital ICs, QCA7000, W5500 |
| 3.3 V analog (AVDD) | 3.3 V +/- 1% | Local LDO from 3.3 V digital | 50 mA | ADC VREF, op-amps (OPA2376) |
| 5 V | 5.0 V +/- 5% | Aux PSU via P5 | 100 mA | CAN transceiver (TCAN1044) |
| 12 V | 12.0 V +/- 10% | Aux PSU via P5 | 2 A | Fan drive pass-through |

## 2. P5 Power Connector

The P5 connector is a Molex Micro-Fit 3.0 (or equivalent), placed at the **southeast corner** of the board.

### P5 Pinout

| Pin | Signal | Wire gauge | Notes |
|---|---|---|---|
| 1 | 3.3 V | 22 AWG | Main digital supply |
| 2 | 3.3 V | 22 AWG | Paralleled for current sharing |
| 3 | 5 V | 22 AWG | CAN transceiver supply |
| 4 | 12 V | 20 AWG | Fan drive, higher current |
| 5 | 12 V | 20 AWG | Paralleled for current sharing |
| 6 | GND | 20 AWG | Power return |
| 7 | GND | 20 AWG | Power return, paralleled |
| 8 | PGOOD | 22 AWG | Power-good signal from Aux PSU |

> [!tip] PGOOD signal
> The PGOOD input from the Aux PSU indicates that all supply rails are stable. The MCU monitors this on a GPIO input. If PGOOD deasserts, the firmware enters a safe shutdown state, disabling all PWM outputs within one switching cycle. See [[06-Firmware Architecture]] for the fault handling sequence and [[08-Power-On Sequence and Inrush Management]] for startup sequencing.

## 3. Power Entry Filtering

Each power rail entering the board through P5 passes through an input filter stage before reaching the distribution network:

### 3.3 V Digital Input Filter

```
P5 pin 1,2 ──┬── FB1 ──┬── 3.3V_DIGITAL plane (L3)
              │         │
             4.7µF    100µF
              │         │
             GND       GND
```

| Component | Value | Package | Purpose |
|---|---|---|---|
| FB1 (ferrite bead) | BLM18PG221SN1 (220 ohm @ 100 MHz) | 0603 | HF noise rejection from Aux PSU cable |
| C_bulk1 | 100 µF / 6.3 V electrolytic or polymer | Radial 5 mm | Low-frequency energy storage |
| C_bulk2 | 4.7 µF / 10 V MLCC | 0805 | Mid-frequency decoupling |

### 5 V Input Filter

```
P5 pin 3 ──── FB2 ──┬── 5V island on L3
                     │
                    4.7µF
                     │
                    GND
```

| Component | Value | Package | Purpose |
|---|---|---|---|
| FB2 (ferrite bead) | BLM18PG331SN1 (330 ohm @ 100 MHz) | 0603 | HF noise rejection |
| C_5V_bulk | 4.7 µF / 10 V MLCC | 0805 | Bulk decoupling for TCAN1044 |

### 12 V Fan Pass-Through

The 12 V rail is a pass-through — it enters via P5 and exits via a separate fan connector (J1) on the east edge. Filtering is minimal since this rail drives fans (inductive loads), not sensitive electronics:

```
P5 pin 4,5 ──── Polyfuse (2A) ──┬── J1 Fan connector
                                  │
                                 100µF
                                  │
                                 GND
```

| Component | Value | Purpose |
|---|---|---|
| PTC fuse (Polyfuse) | 2 A hold, 4 A trip | Overcurrent protection for fan circuit |
| C_12V | 100 µF / 25 V electrolytic | Inrush limiting, decoupling |

> [!warning] Fan drive routing
> Route 12 V traces on L4 with 0.5 mm (20 mil) minimum width to handle 2 A. Keep 12 V traces away from the analog section (minimum 5 mm clearance). The 12 V trace does not use the L3 power plane — it is routed as a discrete trace on L4 to avoid contaminating the 3.3 V power plane.

## 4. Local LDO: Analog 3.3 V Supply

The analog circuits (op-amps, ADC reference) require a cleaner 3.3 V supply than what the Aux PSU provides after cable and connector drops. A low-noise LDO generates 3.3 V analog (AVDD) from the 3.3 V digital rail.

### LDO Selection: TPS7A20

| Parameter | Value |
|---|---|
| Part number | TPS7A2033DBVR |
| Package | SOT-23-5 |
| Output voltage | 3.3 V (fixed) |
| Input voltage range | 3.4–6.0 V (use 3.3 V digital, needs ~3.45 V min at load) |
| Dropout voltage | 100 mV typical at 50 mA |
| Output noise | 6.5 µV RMS (10 Hz–100 kHz) |
| PSRR | 75 dB at 1 kHz |
| Max output current | 200 mA (only 50 mA needed) |

> [!warning] LDO headroom
> The TPS7A20 requires a minimum dropout of 100 mV. If the 3.3 V digital rail drops below 3.4 V under load (possible with cable drop from the Aux PSU), the LDO exits regulation. Verify the Aux PSU output under worst-case load to ensure >= 3.45 V at P5. Alternatively, consider feeding the LDO from the 5 V rail (which has more headroom) and using a 3.3 V output LDO rated for 5 V input.

### Alternative: LDO from 5 V Rail

If headroom on the 3.3 V rail is insufficient:

```
5V (from P5 pin 3) ──── TPS7A4533 (5V-in, 3.3V-out, 150mA) ──── 3.3V_ANALOG
```

This provides 1.7 V of headroom, ensuring clean regulation even with supply variations.

### LDO Circuit and Layout

```
3.3V_DIGITAL ──── FB3 ──┬──── TPS7A20 ──┬──── 3.3V_ANALOG (AVDD)
                         │    IN    OUT   │
                        1µF              1µF + 100nF
                         │               │
                        GND             AGND (star point)
```

| Component | Value | Placement |
|---|---|---|
| FB3 (ferrite bead) | BLM18PG221 (220 ohm @ 100 MHz) | Between digital 3.3 V and LDO input |
| C_in | 1 µF / 10 V MLCC | Within 2 mm of LDO input pin |
| C_out | 1 µF / 10 V MLCC | Within 2 mm of LDO output pin |
| C_out2 | 100 nF / 10 V MLCC | Adjacent to C_out |

LDO placement rules:
- Place the LDO on the **west side** of the board, within the analog zone
- Route AVDD to the analog power island on L3 via a dedicated via
- The LDO GND pin connects to the analog star-ground point on L2

## 5. STM32G474RE Decoupling Strategy

The STM32G474RE (LQFP-64) has multiple VDD and VSS pins. Each VDD pin requires local decoupling.

### MCU Power Pins

| Pin name | Pin number (LQFP-64) | Rail | Decoupling |
|---|---|---|---|
| VDD_1 | 1 | 3.3 V digital | 100 nF |
| VDD_2 | 17 | 3.3 V digital | 100 nF |
| VDD_3 | 32 | 3.3 V digital | 100 nF |
| VDD_4 | 48 | 3.3 V digital | 100 nF |
| VDDA | 13 | 3.3 V analog | 1 µF + 100 nF |
| VREF+ | 14 | 3.3 V analog | 100 nF |
| VBAT | 1 | 3.3 V (or battery) | 100 nF |

### Decoupling Capacitor Placement

Each 100 nF capacitor must be placed according to these rules:

| Rule | Specification |
|---|---|
| Distance from VDD pin | Within 1.5 mm, ideally directly adjacent |
| Via to L3 power plane | Dedicated via within 1 mm of cap pad |
| Via to L2 GND plane | Dedicated via within 1 mm of cap pad |
| Capacitor package | 0402 preferred (small size, close placement) |
| Capacitor type | MLCC, X7R or X5R, 10 V rating minimum |

> [!tip] Via-in-pad for decoupling
> For optimal performance, use via-in-pad design for decoupling capacitors: place vias directly on the capacitor pads, connecting one pad to L2 GND and the other to L3 VDD. This eliminates trace inductance between the cap and the planes. Requires the fab to fill and cap the vias (VIPPO process), which adds cost. For a cost-sensitive design, standard pad-to-via traces of < 1 mm are acceptable.

### Bulk Decoupling Per Rail Section

In addition to per-pin 100 nF caps, place bulk capacitors at strategic points:

| Location | Capacitor | Value | Purpose |
|---|---|---|---|
| Near MCU (center) | C_bulk_MCU | 4.7 µF / 10 V MLCC, 0805 | Bulk storage for MCU transients |
| Near W5500 | C_bulk_ETH | 10 µF / 10 V MLCC, 0805 | Ethernet controller bursts |
| Near QCA7000 | C_bulk_PLC | 10 µF / 10 V MLCC, 0805 | PLC modem TX bursts |
| Near P5 entry | C_bulk_entry | 100 µF / 6.3 V polymer | Board-level energy reservoir |

## 6. Power Plane Partitioning on L3

The L3 power plane is divided into regions as described in [[07-PCB-Layout/Controller/01-Stack-Up and Layer Assignment]]:

### Plane Region Table

| Region | Rail | Area (approx) | Connected ICs |
|---|---|---|---|
| Main digital | 3.3 V | 70% of L3 | STM32, W5500, QCA7000, EEPROM |
| Analog island | 3.3 V analog | 15% of L3 | OPA2376 x3, VREF+, VDDA |
| 5 V island | 5.0 V | 10% of L3 | TCAN1044 |
| 12 V trace | 12 V | Trace on L4 | Fan connector J1 |

### Plane Partition Implementation

- Partition gaps on L3: 0.5 mm (20 mil) clearance between islands
- Ferrite bead bridges: each island connects to its source through a ferrite bead
- No signal trace on L4 should cross an L3 partition gap without a nearby GND stitching via to L2

```
L3 Power Plane Map
┌──────────────────────────────────────────────────┐
│                                                  │
│   ┌───────────┐                                  │
│   │ 3.3V      │  FB3                             │
│   │ ANALOG    │◀════════╗                        │
│   │ (AVDD)    │         ║                        │
│   └───────────┘         ║                        │
│                    ┌────╨────────────────────┐   │
│                    │     3.3V DIGITAL        │   │
│   ┌──────────┐    │     (main region)       │   │
│   │ 5V       │    │                         │   │
│   │ (CAN)    │    │                         │   │
│   └──────────┘    └─────────────────────────┘   │
│        ▲ FB2                ▲ FB1                │
│        │                    │                    │
│      P5 pin 3            P5 pin 1,2              │
└──────────────────────────────────────────────────┘
```

## 7. Power Distribution Routing Rules

| Rule | Detail |
|---|---|
| 3.3 V digital distribution | Via L3 plane — no explicit traces needed |
| 3.3 V analog distribution | Via L3 analog island — route from LDO output to island via |
| 5 V distribution | Via L3 5 V island — trace from P5 through FB2 to island |
| 12 V distribution | Trace on L4, 0.5 mm minimum width, from P5 to J1 |
| GND distribution | Via L2 plane — universal ground, no routing needed |
| GND returns from caps | Each cap GND pad gets a dedicated via to L2 |

## 8. Power Consumption Estimate

| Subsystem | Rail | Current (mA) | Power (mW) |
|---|---|---|---|
| STM32G474RE (170 MHz, all peripherals active) | 3.3 V | 120 | 396 |
| OPA2376 x 3 (dual op-amp, 6 channels) | 3.3 V analog | 6 | 20 |
| W5500 Ethernet controller | 3.3 V | 132 | 436 |
| QCA7000 PLC modem | 3.3 V | 300 | 990 |
| TCAN1044 CAN transceiver | 5 V | 70 | 350 |
| Misc (LEDs, pull-ups, EEPROM) | 3.3 V | 30 | 99 |
| **Total (excl. fans)** | — | **658** | **2,291** |
| Fans (pass-through) | 12 V | 1500 | 18,000 |

> [!tip] Thermal note
> Total board dissipation (excluding fan pass-through) is approximately 2.3 W. This is easily handled by natural convection in an enclosed PDU, but the board will also benefit from forced airflow from the fans it controls. No heatsinks are required on any controller board component.

## 9. Cross-References

- [[07-PCB-Layout/Controller/01-Stack-Up and Layer Assignment]] — L3 power plane partitioning details
- [[02-Signal Integrity]] — analog supply noise requirements, star-ground
- [[05-EMC and Grounding]] — ferrite bead filtering, power entry EMC
- [[07-PCB-Layout/Aux-PSU/__init|Aux PSU Board]] — source of all power rails
- [[__init|Controller Board Overview]] — P5 connector location and board zoning
- [[08-Power-On Sequence and Inrush Management]] — startup sequencing, PGOOD signaling

## 10. Design Checklist

| Item | Check |
|---|---|
| 100 nF cap within 1.5 mm of each MCU VDD pin | |
| 1 µF + 100 nF on VDDA pin | |
| Ferrite bead between digital and analog 3.3 V | |
| LDO for analog 3.3 V placed in analog zone | |
| Bulk cap (100 µF) at P5 power entry | |
| 5 V island isolated on L3 with ferrite bead | |
| 12 V routed on L4, not on L3 plane | |
| No L4 signal crosses L3 plane split without GND stitch | |
| PTC fuse on 12 V fan circuit | |
| PGOOD signal routed to MCU GPIO | |

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
