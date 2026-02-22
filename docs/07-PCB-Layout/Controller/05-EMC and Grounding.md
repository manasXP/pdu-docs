---
tags: [pdu, pcb-layout, controller, emc, grounding, esd, shielding]
created: 2026-02-22
status: draft
---

# EMC and Grounding

This document defines the electromagnetic compatibility (EMC) and grounding strategy for the Controller Board. As a digital/mixed-signal control board operating inside a PDU enclosure that also contains high-power switching converters (Vienna PFC at up to 100 kHz, LLC at up to 500 kHz), robust EMC design is essential for reliable operation.

## 1. Grounding Philosophy

### 1.1 Single GND Plane — No Splits

The Controller Board uses a **single, continuous ground plane on L2** with no intentional splits or cuts. This is the recommended approach for a mixed-signal board where the analog and digital sections share a single ADC (the STM32's internal ADCs).

> [!warning] Why no ground splits
> A split ground plane forces return currents to find alternative paths around the split, which increases loop area and creates common-mode noise. The STM32G474 has analog and digital ground pins (VSSA, VSS) that are internally connected within the IC die. Splitting the external ground plane while the IC connects them internally creates a ground loop through the IC package. A single plane with **careful component partitioning** is superior.

### 1.2 Partitioning by Placement, Not by Plane Cuts

Instead of splitting the ground plane, analog and digital sections are separated by **component placement zoning**:

| Zone | Location | Components | Current return behavior |
|---|---|---|---|
| Analog zone | West side | OPA2376, RC filters, LDO | Low-frequency, low-amplitude return currents |
| Digital zone | Center and east | STM32, W5500, QCA7000, EEPROM | Higher-frequency, pulsed return currents |
| Communication zone | North edge | TCAN1044, connectors | Mixed, with external cable coupling |
| Power entry | Southeast | P5 connector, bulk caps | High-di/dt transients from supply |

The continuous L2 plane allows return currents to flow directly under their source traces. Since analog components are grouped on the west side and digital components on the east side, their return currents naturally stay in separate regions of the plane without a physical cut forcing them elsewhere.

### 1.3 Star-Ground Point

The analog ground star point is the **single location** where the analog ground region (under the op-amps and LDO) and digital ground region (under the MCU) are defined to have equal potential. In practice, with a continuous plane, the star point is simply the location where the analog supply return (AGND from the LDO) connects to L2.

Location: near the P5 power entry connector, where the main GND from the Aux PSU enters the board.

```
                    P5 Connector (GND pins)
                         │
                         ▼
              ┌──── Star Ground Point ────┐
              │     (on L2 plane)         │
              ▼                           ▼
     Analog return currents      Digital return currents
     (west side of board)        (center/east of board)
```

> [!tip] Star-ground implementation
> On a continuous plane, the "star point" is implemented by ensuring that the high-current digital return and the sensitive analog return both reach the P5 GND pins through low-impedance paths. Place the P5 connector at the boundary between analog and digital zones so that neither return current must cross the other zone to reach the connector.

## 2. Board Edge Stitching Vias

A perimeter ring of GND stitching vias connects L1 GND copper (guard traces, edge copper) to the L2 GND plane around the entire board perimeter. This ring provides:

1. **Shielding**: reduces edge radiation from the L1-L2 cavity
2. **Return-current containment**: prevents currents from flowing along the board edge
3. **Mechanical grounding**: provides multiple low-impedance connections for any enclosure contact

### 2.1 Stitching Via Specification

| Parameter | Value |
|---|---|
| Via drill | 0.3 mm |
| Via pad | 0.6 mm |
| Pitch | 2 mm (center-to-center) |
| Inset from board edge | 1.5 mm |
| Total via count | ~220 vias (perimeter of 120+100+120+100 = 440 mm, at 2 mm pitch) |
| Connected layers | L1 GND copper to L2 GND plane |

### 2.2 Edge Copper Pour

On L1, a 2 mm wide GND copper pour runs along the board perimeter, connected to the stitching vias:

```
Board edge
│
│  1.5mm  │ 2mm GND pour │
│◀───────▶│◀────────────▶│
│         ┊ via  via  via ┊
│         ┊  ●    ●    ● ┊ ← stitching vias at 2mm pitch
│         ┊              ┊
│         └──────────────┘
```

> [!tip] Stitching via spacing
> The 2 mm via pitch provides effective shielding up to approximately 15 GHz (lambda/20 at 2 mm), which is far above the highest frequency of concern on this board (the HRTIM switching harmonics at a few hundred MHz). For the communication interfaces (CAN at 1 MHz, Ethernet at 25 MHz, PLC at 30 MHz), this pitch is more than adequate.

## 3. Connector EMC Filtering

Every external connector on the board is a potential EMC ingress/egress point. Each connector has a dedicated filtering and protection scheme.

### 3.1 P4 — CAN Bus Connector

| Protection | Component | Placement |
|---|---|---|
| Common-mode choke | Wurth 744232090 (90 ohm @ 100 MHz) | Between TCAN1044 and connector |
| TVS diode (ESD) | PESD2CAN (dual bidirectional, Vclamp = 24V) | At connector pins, before CMC |
| Bus filter capacitor | 100 pF / 50 V COG | CANH-to-CANL, at connector |

ESD path: External surge enters P4, TVS clamps to safe voltage, CMC rejects common-mode component, TCAN1044 sees clean differential signal.

```
P4 pin ──┬── TVS ──┬── CMC ──── TCAN1044
          │        │
         GND      GND
```

### 3.2 P6 — OCPP Ethernet (RJ45)

| Protection | Component | Placement |
|---|---|---|
| Integrated magnetics | In RJ45 jack (Pulse J0011D21BNL) | At connector |
| TVS diode array | RCLAMP0524P (quad, rail-to-rail clamp) | Between magnetics and W5500 |
| Shield-to-GND | 1 Mohm // 4.7 nF to chassis GND | At RJ45 shield pins |

The RJ45 connector shield is connected to **chassis ground** (not signal ground) through a parallel RC network. This bleeds off static charge without creating a direct path for common-mode currents between signal GND and chassis GND.

| Component | Value | Purpose |
|---|---|---|
| R_shield | 1 Mohm | DC bleed for static charge |
| C_shield | 4.7 nF / 2 kV | AC coupling for HF noise to chassis |

### 3.3 P7 — ISO 15118 PLC (Coax)

| Protection | Component | Placement |
|---|---|---|
| Galvanic isolation | Coupling transformer (1:1) | Between AFE and connector |
| TVS diode | PESD5V0S1BL (unidirectional, 5 V clamp) | At transformer secondary |
| Gas discharge tube | 2026-09-SM (90 V, for lightning surge) | At connector center pin |

The coupling transformer provides inherent galvanic isolation. The GDT (gas discharge tube) protects against high-energy surges coupled through the charging cable.

### 3.4 P3 — Analog Sense Inputs

| Protection | Component | Placement |
|---|---|---|
| TVS diode array | TPD4E05U06 (quad, 5 V clamp) | At P3 connector pins |
| Series resistor | 10 kohm (already in signal path) | Between connector and op-amp |
| Bypass capacitor | 100 pF COG to GND | At each P3 pin |

> [!warning] Analog connector ESD
> The TVS diodes on P3 must be low-capacitance types (< 5 pF per channel) to avoid degrading the analog signal bandwidth. The TPD4E05U06 has 1.5 pF per channel, which is acceptable for the DC–50 kHz bandwidth of the current sense signals.

### 3.5 P1/P2 — PWM Harness Connectors

| Protection | Component | Placement |
|---|---|---|
| Series resistor | 33 ohm (already in signal path) | At MCU pin (source termination) |
| TVS diode array | TPD6E05U06 (6-ch, 5 V clamp) | At connector pins |
| Bypass capacitor | 100 pF to GND | At each connector pin |

### 3.6 P5 — Power Entry Connector

| Protection | Component | Placement |
|---|---|---|
| Ferrite beads | Per rail (see [[04-Power Distribution]]) | Between connector and plane |
| Bulk bypass | 100 µF + 4.7 µF per rail | At connector |
| TVS on PGOOD | PESD5V0S1BL (5 V clamp) | At PGOOD pin |

## 4. ESD Protection Strategy

### 4.1 Design Target

The controller board must survive ESD events per **IEC 61000-4-2**:

| Test level | Contact discharge | Air discharge |
|---|---|---|
| Level 4 (target) | +/- 8 kV | +/- 15 kV |

### 4.2 Protection Architecture

ESD protection is implemented in three tiers:

| Tier | Location | Method | Purpose |
|---|---|---|---|
| 1. Connector level | At each external connector | TVS diodes, GDTs | Clamp voltage before it enters the board |
| 2. Trace level | Series components in signal path | Resistors (10k–33 ohm) | Limit current, slow edge rate |
| 3. IC level | Internal to ICs | IC ESD structures | Last line of defense (not relied upon) |

### 4.3 TVS Diode Selection Criteria

| Parameter | Requirement |
|---|---|
| Working voltage | > signal voltage (3.3 V or 5 V) |
| Clamp voltage (at 8 kV) | < IC absolute maximum rating |
| Capacitance | < 5 pF for analog, < 15 pF for digital |
| Peak pulse current | > 5 A (8/20 µs waveform) |
| Package | SOT-23 or smaller for per-pin, array for multi-pin |

### 4.4 ESD Current Path Design

ESD currents must have a low-impedance path from the connector pin to ground **without flowing through sensitive IC pins**:

```
Connector pin
     │
     ├──── TVS diode ──── GND (via to L2 plane, within 1 mm)
     │
     ├──── Series R ──── Signal trace ──── IC pin
     │
```

Key rules:
- TVS GND via must be within **1 mm** of the TVS pad
- The GND via connects to a wide copper pour on L2, not a thin trace
- The signal trace to the IC branches **after** the TVS, so the ESD current does not flow along the signal trace
- Route the TVS-to-GND path as a **wide, short trace** (0.5 mm minimum width)

## 5. Cable Shield Grounding

All shielded cables entering the board (CAN, Ethernet, PLC, analog sense) must have their shields terminated at the connector entry point:

| Cable | Shield termination | Method |
|---|---|---|
| CAN (P4) | Chassis GND via connector shell | 360-degree shield clamp at connector |
| Ethernet (P6) | Chassis GND via RJ45 shell | RC to chassis (1M // 4.7 nF) |
| PLC coax (P7) | Chassis GND via SMA/BNC shell | Direct contact to connector body |
| Analog sense (P3) | Signal GND on L2 plane | Shield drain wire to GND via at connector |

> [!tip] 360-degree shield termination
> For maximum EMC performance, use connectors with metal shells that provide 360-degree contact with the cable shield. Pigtail connections (drain wire) are inferior because they create an inductive loop at the shield termination point. For the CAN and coax connectors, this is straightforward. For the Molex-style analog connector (P3), use a shield drain wire connected to a GND pad within 5 mm of the connector body.

## 6. Board-Level EMC Design Rules

### 6.1 Bypass Capacitor Strategy

Every connector pin that enters or exits the board has a bypass capacitor to GND:

| Connector | Signal type | Bypass cap | Value |
|---|---|---|---|
| P1, P2 | PWM outputs | COG MLCC | 100 pF |
| P3 | Analog inputs | COG MLCC | 100 pF |
| P4 | CAN differential | COG MLCC | 100 pF (CANH-CANL) |
| P5 | Power | MLCC + Electrolytic | 100 nF + 100 µF per rail |
| P6 | Ethernet | Via magnetics | — (magnetics provide isolation) |
| P7 | PLC coax | Via transformer | — (transformer provides isolation) |

### 6.2 Ferrite Bead Placement

Ferrite beads are used at three locations:

| Location | Part | Impedance | Purpose |
|---|---|---|---|
| 3.3 V power entry (FB1) | BLM18PG221 | 220 ohm @ 100 MHz | Reject Aux PSU HF noise |
| 5 V power entry (FB2) | BLM18PG331 | 330 ohm @ 100 MHz | Reject Aux PSU HF noise |
| Analog 3.3 V isolation (FB3) | BLM18PG221 | 220 ohm @ 100 MHz | Isolate analog from digital noise |

### 6.3 Trace Routing for EMC

| Rule | Specification |
|---|---|
| No traces on L1 crossing L2 plane gaps | L2 has no gaps — rule satisfied by design |
| Signal return vias | Place within 1 mm of every L1-to-L4 transition via |
| Clock trace shielding | GND guard traces on both sides of SPI SCK, HSE clock |
| No stubs | All series components placed in-line, no T-branches |
| Loop area minimization | Signal trace and return (on L2 plane) separated by only 0.2 mm prepreg |

## 7. Ground Plane Integrity Audit

Before releasing the PCB layout for fabrication, verify the following on L2:

| Check | Method |
|---|---|
| No accidental splits | Visual inspection of L2 copper pour |
| No signal routes on L2 | DRC rule: no traces assigned to L2 |
| Anti-pad size check | All via anti-pads <= 0.6 mm to maintain plane continuity |
| Thermal relief on GND vias | Use direct connections (no thermal relief) for all GND stitching vias |
| Mounting hole clearance | 3.5 mm clearance ring around M3 holes (no copper in contact with screw) |

> [!warning] Thermal relief on GND vias
> Standard PCB tools add thermal relief patterns (spoke connections) to plane-connected vias by default. For GND stitching vias and decoupling cap GND vias, **disable thermal relief** and use solid connections. Thermal relief adds inductance to the ground connection, degrading bypass capacitor effectiveness. Only use thermal relief on through-hole component GND pins to ensure solderability.

## 8. EMC Test Plan

The assembled controller board should be evaluated for EMC compliance before integration into the full PDU:

| Test | Standard | Limit | Method |
|---|---|---|---|
| Conducted emissions | EN 61000-6-4 | Class A | LISN on power input |
| Radiated emissions | EN 61000-6-4 | Class A | 3 m semi-anechoic |
| ESD immunity | IEC 61000-4-2 | Level 4 (+/- 8 kV contact) | Apply to all connectors |
| Burst immunity | IEC 61000-4-4 | Level 3 (2 kV) | Apply to power and signal ports |
| Surge immunity | IEC 61000-4-5 | Level 3 (1 kV diff, 2 kV CM) | Apply to CAN and Ethernet ports |

## 9. Cross-References

- [[07-PCB-Layout/Controller/01-Stack-Up and Layer Assignment]] — L2 GND plane definition, edge stitching via spec
- [[02-Signal Integrity]] — guard traces, analog routing over GND plane
- [[03-Communication Interfaces]] — CAN CMC, Ethernet magnetics, PLC transformer
- [[04-Power Distribution]] — ferrite bead filtering, power entry bypass
- [[__init|Controller Board Overview]] — connector map and board zoning
- [[00-Board Partitioning]] — PDU enclosure grounding, board-to-chassis connections

## 10. Design Checklist

| Item | Check |
|---|---|
| L2 GND plane continuous — no intentional splits | |
| Edge stitching vias at 2 mm pitch around perimeter | |
| TVS diodes on all external connector pins | |
| CMC on CAN bus (P4) | |
| RJ45 shield to chassis via RC (1M // 4.7 nF) | |
| Coupling transformer on PLC (P7) | |
| ESD current path avoids IC pins | |
| TVS GND vias within 1 mm of TVS pad | |
| Ferrite beads on all power entry rails | |
| 100 pF bypass cap on each P1/P2/P3 connector pin | |
| GND stitching vias use solid connection (no thermal relief) | |
| Cable shield grounded at connector entry point | |
| No signal traces on L2 | |

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
