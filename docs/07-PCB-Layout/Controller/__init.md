---
tags: [pdu, pcb-layout, controller, stm32, overview]
created: 2026-02-22
status: draft
aliases: [Controller Board, Control PCB]
---

# Controller Board — Overview

This document describes the **Controller Board** for the 30 kW EV Charger PDU. The board hosts the central MCU and all supervisory, sensing, and communication electronics. It is physically separated from the power stages by a minimum of 50 mm and connects to the [[07-PCB-Layout/AC-DC/__init|AC-DC (Vienna PFC)]] and [[07-PCB-Layout/DC-DC/__init|DC-DC (LLC)]] boards via signal harness cables.

## Board Summary

| Parameter | Value |
|---|---|
| **Board dimensions** | 120 mm x 100 mm |
| **Layer count** | 4 |
| **Stack-up** | Signal / GND / 3.3 V Power / Signal |
| **Copper weight** | 1 oz (35 µm) all layers |
| **MCU** | STM32G474RE — LQFP64, 170 MHz Cortex-M4F |
| **Primary supply** | 3.3 V from Aux PSU |
| **Secondary supplies** | 5 V (CAN transceiver), 12 V pass-through (fans) |
| **Mounting** | 4x M3 mounting holes, 5 mm inset from corners |

## Functional Block Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    CONTROLLER BOARD                       │
│                                                          │
│  ┌──────────┐   HRTIM PWM (12ch)   ┌───────────────┐   │
│  │          │──────────────────────▶│  P1/P2 PWM    │   │
│  │          │                       │  Connectors   │───┼──▶ Power Boards
│  │          │   ADC (6ch analog)    │               │   │
│  │ STM32    │◀──────────────────────│  P3 Analog    │   │
│  │ G474RE   │                       │  Connector    │───┼──◀ Sense Signals
│  │          │                       └───────────────┘   │
│  │          │   CAN 2.0B            ┌───────────────┐   │
│  │          │◀─────────────────────▶│  TCAN1044     │───┼──▶ CAN Bus
│  │          │                       └───────────────┘   │
│  │          │   UART / Ethernet     ┌───────────────┐   │
│  │          │◀─────────────────────▶│  OCPP I/F     │───┼──▶ Cloud
│  │          │                       └───────────────┘   │
│  │          │   SPI                 ┌───────────────┐   │
│  │          │◀─────────────────────▶│  QCA7000      │───┼──▶ ISO 15118 PLC
│  │          │                       │  PLC Modem    │   │
│  └──────────┘                       └───────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  P5 Power Input: 3.3 V, 5 V, 12 V from Aux PSU │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Key Interfaces

### HRTIM PWM Generation

The STM32G474RE HRTIM peripheral generates all gate-drive PWM signals:

| Channel group | Destination | Signals | Switching freq |
|---|---|---|---|
| HRTIM A/B/C | Vienna PFC (3-phase) | 6 complementary outputs | up to 100 kHz |
| HRTIM D/E/F | LLC DC-DC (3-phase) | 6 complementary outputs | up to 500 kHz |

- Resolution: 184 ps (5.44 GHz equivalent counter clock)
- Dead-time insertion handled in hardware
- Outputs routed to P1 (PFC) and P2 (LLC) harness connectors

### Analog Sensing

| Signal | Range | Conditioning | ADC channel |
|---|---|---|---|
| PFC phase A current | 0–3.3 V | Op-amp + RC filter | ADC1_IN1 |
| PFC phase B current | 0–3.3 V | Op-amp + RC filter | ADC1_IN2 |
| PFC phase C current | 0–3.3 V | Op-amp + RC filter | ADC1_IN3 |
| DC bus voltage | 0–3.3 V | Resistor divider + buffer | ADC2_IN1 |
| Output voltage | 0–3.3 V | Resistor divider + buffer | ADC2_IN2 |
| Output current | 0–3.3 V | Op-amp + RC filter | ADC2_IN3 |

- ADC: 12-bit, 5 MSPS internal ADCs
- Front-end: OPA2376 dual op-amp for signal conditioning
- Anti-aliasing: 2nd-order RC low-pass at each ADC input

### Communication

| Interface | IC / Method | Protocol | Connector |
|---|---|---|---|
| CAN bus | TCAN1044 transceiver | CAN 2.0B, 1 Mbps | P4 (DB9 or Molex) |
| OCPP 1.6 | UART or Ethernet PHY | JSON over WebSocket | P6 (RJ45 or header) |
| ISO 15118 | QCA7000 PLC modem | SPI to MCU | P7 (BNC / coax coupler) |

## Board Zoning

The 120 x 100 mm board area is divided into functional zones:

```
        North edge (communication connectors P4, P6, P7)
 ┌──────────────────────────────────────────────────┐
 │  CAN xcvr  │   OCPP / Ethernet   │  PLC modem   │
 │────────────┼─────────────────────┼──────────────│
 │            │                     │              │
 │  Analog    │      STM32G474RE    │  Digital     │
 │  front-end │      (center)       │  support     │
 │  (west)    │                     │  (east)      │
 │            │                     │              │
 │────────────┼─────────────────────┼──────────────│
 │  P3 Analog │  P1 PFC PWM  P2 LLC PWM │ P5 Power │
 └──────────────────────────────────────────────────┘
        South edge (power stage harness connectors)
```

> [!tip] Placement rationale
> Communication connectors are grouped on the **north** edge to keep harness cables away from the power-stage connectors on the **south** edge. Analog circuits sit on the **west** side, nearest to the analog input connector P3, to minimize trace lengths for sensitive signals.

## Topic Documents

| # | Document | Content |
|---|---|---|
| 1 | [[01-Stack-Up and Layer Assignment]] | 4-layer stack-up, impedance targets, via strategy |
| 2 | [[02-Signal Integrity]] | ADC routing, HRTIM matched pairs, guard traces |
| 3 | [[03-Communication Interfaces]] | CAN, OCPP, ISO 15118 layout details |
| 4 | [[04-Power Distribution]] | Decoupling, LDO, power plane partitioning |
| 5 | [[05-EMC and Grounding]] | Grounding strategy, ESD, connector filtering |

## Cross-References

- [[06-Firmware Architecture]] — software that runs on this board
- [[00-Board Partitioning]] — how this board fits in the overall PDU assembly
- [[07-PCB-Layout/AC-DC/__init|AC-DC Board]] — PFC power stage driven by this controller
- [[07-PCB-Layout/DC-DC/__init|DC-DC Board]] — LLC power stage driven by this controller
- [[07-PCB-Layout/Aux-PSU/__init|Aux PSU Board]] — provides 3.3 V / 5 V / 12 V to this board

## Design Status

| Milestone | Status |
|---|---|
| Schematic capture | Not started |
| Component placement | Not started |
| Routing | Not started |
| DRC / ERC | Not started |
| Gerber release | Not started |

> [!warning] Clearance requirement
> The controller board must maintain a minimum **50 mm physical separation** from all power-stage PCBs. Harness cables between boards should be shielded twisted-pair where carrying analog sense signals.

## Revision History

| Rev | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-02-22 | — | Initial draft |
