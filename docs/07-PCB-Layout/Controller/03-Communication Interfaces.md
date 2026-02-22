---
tags: [pdu, pcb-layout, controller, can-bus, ocpp, iso15118, communication]
created: 2026-02-22
status: draft
---

# Communication Interfaces

This document covers the PCB layout of all communication interfaces on the Controller Board. The board implements three communication channels: **CAN bus** for inter-module stacking, **OCPP 1.6** for cloud connectivity, and **ISO 15118** for vehicle-to-charger communication via PLC. All communication connectors are grouped on the **north edge** of the board to simplify cable management within the PDU enclosure.

## Connector Placement Strategy

All external communication connectors are placed along the north edge of the 120 mm board width:

```
North edge (120 mm)
┌───────────────────────────────────────────────────────────┐
│  P4 CAN    │   P6 OCPP          │   P7 ISO 15118          │
│  (Molex    │   (RJ45 or         │   (coax / BNC           │
│   4-pin)   │    6-pin header)   │    or SMA)              │
│  20 mm     │   35 mm            │   25 mm                 │
└───────────────────────────────────────────────────────────┘
     ◀─ West                                    East ─▶
```

> [!tip] Connector grouping rationale
> Placing all communication connectors on a single edge achieves three goals: (1) cable harnesses exit the enclosure in one direction, (2) communication signals are physically separated from the power-stage harness on the south edge, and (3) EMC filtering components can be concentrated in one board region.

### Connector Summary

| Connector | Interface | Type | Pins | Placement |
|---|---|---|---|---|
| P4 | CAN bus | Molex Micro-Fit 3.0, 4-pin | CANH, CANL, GND, Shield | Northwest corner |
| P6 | OCPP 1.6 | RJ45 (Ethernet) or 6-pin header | TX+/-, RX+/-, GND, Shield | North center |
| P7 | ISO 15118 PLC | SMA or BNC coax | Signal, GND | Northeast corner |

## CAN Bus Interface

### CAN Transceiver: TCAN1044

The TCAN1044 is a 3.3 V logic, 5 V bus CAN transceiver from Texas Instruments. It supports CAN 2.0B at up to 5 Mbps (used here at 1 Mbps).

| Parameter | Value |
|---|---|
| IC | TCAN1044VDRQ1 (SOIC-8) |
| Logic supply (VIO) | 3.3 V |
| Bus supply (VCC) | 5 V |
| Data rate | 1 Mbps (CAN 2.0B) |
| Standby current | 5 µA |
| ESD rating | +/- 8 kV HBM on bus pins |

### TCAN1044 Placement

- Place the TCAN1044 within **10 mm of the P4 connector** to minimize the length of the unshielded differential pair between the transceiver and the connector
- Orient the IC so that bus-side pins (CANH, CANL) face the connector and logic-side pins (TXD, RXD) face the MCU
- Place a ground pad or via array under the IC thermal pad for heat dissipation

### CAN Schematic and Key Components

```
                        TCAN1044
                    ┌──────────┐
STM32 CAN_TX ───────┤ TXD  VCC ├──── 5V (100nF + 4.7µF bypass)
STM32 CAN_RX ───────┤ RXD  VIO ├──── 3.3V (100nF bypass)
         GND ───────┤ GND   S  ├──── Standby control (or GND)
                    │          │
                    │ CANH     ├──┬── CMC ───┬── P4 pin 1 (CANH)
                    │ CANL     ├──┤          ├── P4 pin 2 (CANL)
                    └──────────┘  │          │
                                  │  120Ω    │
                                  │ ┌─┤├──┐  │
                                  └─┘     └──┘
                                  Termination
```

### CAN Differential Pair Routing

The CANH/CANL differential pair between the TCAN1044 and P4 connector must be routed as a controlled-impedance pair:

| Parameter | Specification |
|---|---|
| Differential impedance | 100 ohm +/- 10% |
| Trace width | 0.20 mm (8 mil) |
| Pair spacing (edge-to-edge) | 0.18 mm (7 mil) |
| Routing layer | L1 (referenced to L2 GND) |
| Length matching | +/- 0.5 mm within the pair |
| Maximum trace length | 15 mm (transceiver to connector) |
| Clearance from other signals | 4x trace width (0.8 mm minimum) |

> [!warning] Differential pair continuity
> The CANH/CANL pair must not cross any plane split on L2 or change layers. Route entirely on L1 with a continuous L2 GND reference underneath. Any discontinuity in the reference plane creates a common-mode noise source.

### CAN Termination Resistor

A 120 ohm termination resistor is placed at the P4 connector between CANH and CANL:

- Use a 0402 or 0603 SMD resistor, 1% tolerance
- Place within 5 mm of the P4 connector pins
- Consider a solder-jumper option to disable termination if this module is not at the end of the CAN bus daisy-chain

In a 5-module stacking configuration, only the two end nodes need the 120 ohm termination. The middle three modules should have termination disabled.

| Configuration | Termination |
|---|---|
| Single module (standalone) | 120 ohm installed |
| End-of-bus module (in stack) | 120 ohm installed |
| Middle module (in stack) | 120 ohm removed / jumper open |

### Common-Mode Choke

A common-mode choke (CMC) is placed between the TCAN1044 and the P4 connector to suppress common-mode noise on the CAN bus:

| Parameter | Specification |
|---|---|
| Part (example) | Wurth 744232090 or Murata DLW21SN900 |
| Impedance | 90 ohm at 100 MHz |
| DC resistance | < 0.5 ohm per winding |
| Rated current | > 200 mA |
| Package | 0805 or 0603 common-mode |

Placement: between TCAN1044 bus pins and the 120 ohm termination / P4 connector. The CMC must be on the bus side of the termination resistor.

## OCPP 1.6 Interface

### Architecture Options

OCPP 1.6 communicates via JSON over WebSocket over TCP/IP. Two implementation options exist:

| Option | Interface to MCU | PHY / IC | Pros | Cons |
|---|---|---|---|---|
| **Ethernet** | SPI / RMII | W5500 (SPI-to-Ethernet) or LAN8720 (RMII PHY) | Standard networking, direct OCPP | More complex layout, magnetics |
| **UART bridge** | UART | External Linux SBC (e.g., RPi CM) | Simple MCU interface | Requires SBC, more board space |

> [!tip] Recommended approach
> For a production design, use the **W5500** SPI-to-Ethernet IC. It integrates the TCP/IP stack in hardware, minimizing MCU software complexity. It connects to the MCU via SPI (shared bus or dedicated) and to the network via a standard RJ45 connector with integrated magnetics.

### W5500 Ethernet Controller Layout

| Parameter | Specification |
|---|---|
| IC | W5500 (LQFP-48, 7x7 mm) |
| Interface to MCU | SPI (SCK, MOSI, MISO, CS, INT) up to 33 MHz |
| Crystal | 25 MHz, placed within 5 mm of IC |
| RJ45 connector | With integrated magnetics (e.g., Pulse J0011D21BNL) |
| Placement | North-center of board, near P6 |

Layout rules for W5500:

| Rule | Detail |
|---|---|
| SPI routing | 50 ohm controlled, L1, length-matched +/- 5 mm |
| Crystal | Within 5 mm, GND guard ring, no vias |
| Decoupling | 100 nF on each VDD pin (3 pins), 10 µF bulk |
| TX+/TX- differential pair | 100 ohm, route on L1, keep within 10 mm to RJ45 |
| RX+/RX- differential pair | 100 ohm, route on L1, keep within 10 mm to RJ45 |
| Clearance from analog section | Minimum 10 mm |

### RJ45 Connector (P6) with Magnetics

Use an RJ45 jack with integrated magnetics and LED indicators:

```
                   W5500
              ┌──────────┐
MCU SPI ──────┤ SPI  TX+ ├──── Integrated ─────┐
              │      TX- ├──── magnetics  ─────┤── RJ45 P6
              │      RX+ ├──── in jack    ─────┤
              │      RX- ├──── connector  ─────┘
              └──────────┘
```

- The RJ45 connector's shield pins connect to chassis GND through a 1 Mohm resistor in parallel with a 4.7 nF capacitor (RC filter to chassis)
- Place ESD protection (TVS diode array) between the magnetics and the W5500 inputs

## ISO 15118 PLC Modem Interface

### QCA7000 Overview

The Qualcomm QCA7000 is a HomePlug Green PHY (HPGP) PLC modem used for ISO 15118 vehicle-to-charger communication over the control pilot / proximity pilot lines.

| Parameter | Specification |
|---|---|
| IC | QCA7000 (QFN-32, 5x5 mm) |
| Interface to MCU | SPI (up to 24 MHz) |
| Supply | 3.3 V, approximately 300 mA |
| PLC coupling | Via analog front-end (AFE) and coupling transformer |
| Firmware | Loaded from external SPI flash or MCU at boot |

### QCA7000 Placement and Routing

Place the QCA7000 in the **northeast section** of the board, near the P7 coax connector:

| Rule | Detail |
|---|---|
| SPI to MCU | 50 ohm controlled, L1, length-matched +/- 5 mm |
| SPI trace length | < 40 mm (MCU center to northeast corner) |
| INT line | Route adjacent to SPI bus, pull-up 10 kohm to 3.3V |
| RESET line | Route from MCU GPIO, 10 kohm pull-up, 100 nF cap to GND |
| Decoupling | 100 nF per VDD pin, 10 µF bulk, placed within 2 mm |

### PLC Analog Front-End and Coupling Circuit

The QCA7000 connects to the charging cable's control pilot line through an analog front-end (AFE) circuit:

```
QCA7000           Coupling         P7 Coax
TX/RX  ──▶  AFE  ──▶  Transformer  ──▶  Connector
pins        circuit     1:1             (to CP line)
```

| Component | Purpose | Placement |
|---|---|---|
| TX low-pass filter | Band-limit transmit signal (2–30 MHz) | Adjacent to QCA7000 TX pins |
| RX band-pass filter | Select HPGP band, reject out-of-band noise | Adjacent to QCA7000 RX pins |
| Coupling transformer | Galvanic isolation, impedance matching | Between AFE and P7 connector |
| Line driver / amp | Boost TX signal level for cable attenuation | Between TX filter and transformer |

> [!warning] PLC analog routing
> The PLC transmit and receive paths carry signals in the 2–30 MHz band. These traces are NOT baseband analog like the ADC sense channels. Route them as 50 ohm controlled impedance on L1 and keep them at least 5 mm from any other signal. The coupling transformer must be within 10 mm of the P7 connector.

### SPI Flash for QCA7000 Firmware

If the QCA7000 boots from external SPI flash (rather than MCU-loaded firmware):

| Component | Specification |
|---|---|
| Flash IC | W25Q16 or similar, 2 MB SPI NOR, SOIC-8 |
| Placement | Within 10 mm of QCA7000 |
| SPI routing | Dedicated SPI bus (not shared with MCU SPI) |
| Decoupling | 100 nF at flash VDD pin |

## Communication Interface Summary

| Interface | Transceiver IC | Bus type | Connector | Board zone |
|---|---|---|---|---|
| CAN 2.0B | TCAN1044 | Differential, 1 Mbps | P4 Molex 4-pin | Northwest |
| OCPP 1.6 | W5500 | SPI-to-Ethernet | P6 RJ45 | North center |
| ISO 15118 | QCA7000 | SPI-to-PLC | P7 SMA / BNC | Northeast |

## Connector Pin Assignments

### P4 — CAN Bus (Molex Micro-Fit 3.0, 4-pin)

| Pin | Signal | Notes |
|---|---|---|
| 1 | CANH | CAN high |
| 2 | CANL | CAN low |
| 3 | GND | Signal ground |
| 4 | Shield | Cable shield, connect to chassis GND via RC |

### P6 — OCPP Ethernet (RJ45)

Standard Ethernet pinout (T568B), integrated magnetics in jack.

| Pin | Signal |
|---|---|
| 1 | TX+ |
| 2 | TX- |
| 3 | RX+ |
| 6 | RX- |
| 4,5,7,8 | Unused (or PoE if needed) |

### P7 — ISO 15118 PLC (SMA or BNC)

| Pin | Signal | Notes |
|---|---|---|
| Center | PLC signal | AC-coupled via transformer |
| Shield | GND | Chassis ground at connector |

## Cross-References

- [[01-Stack-Up and Layer Assignment]] — impedance targets for differential and single-ended traces
- [[02-Signal Integrity]] — SPI routing rules, series termination
- [[05-EMC and Grounding]] — connector ESD protection, common-mode filtering
- [[04-Power Distribution]] — 5 V supply for CAN transceiver, 3.3 V for W5500 and QCA7000
- [[__init|Controller Board Overview]] — board zoning, connector map
- [[06-Firmware Architecture]] — CAN protocol stack, OCPP implementation, ISO 15118 stack

## Design Checklist

| Item | Check |
|---|---|
| CAN differential pair routed at 100 ohm on L1 | |
| CAN termination resistor within 5 mm of P4 | |
| Common-mode choke on CAN bus | |
| TCAN1044 within 10 mm of P4 | |
| W5500 crystal with guard ring | |
| Ethernet TX/RX differential pairs at 100 ohm | |
| RJ45 shield to chassis GND via RC filter | |
| QCA7000 SPI length-matched +/- 5 mm | |
| PLC coupling transformer within 10 mm of P7 | |
| All communication connectors on north edge | |
| ESD protection TVS on all external connector pins | |

## Revision History

| Rev | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-02-22 | — | Initial draft |
