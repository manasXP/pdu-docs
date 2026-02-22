---
tags: [PDU, PCB, architecture, multi-board]
created: 2026-02-22
status: draft
---

# 00 – Board Partitioning: Multi-Board Architecture

> [!summary] Overview
> The 30 kW PDU is split into **5 separate PCBs** interconnected by power bus bars and signal harnesses. This document defines the rationale for the split, the physical interfaces between boards, and the connector/harness specifications.

## 1. Rationale for 5-Board Architecture

| Driver | Single-Board Problem | Multi-Board Solution |
|--------|----------------------|----------------------|
| Thermal zoning | PFC and DC-DC hot spots on one board create thermal cross-coupling | Separate heatsink mounting per board; independent airflow zones |
| EMI isolation | High dV/dt switching nodes couple into sensitive analog/digital circuits | Controller board physically separated from power stages |
| Voltage domain separation | AC input (530 VAC), DC bus (920 VDC), and output (1000 VDC) on one board demand extreme creepage everywhere | Each board handles one voltage domain; isolation at connectors |
| Serviceability | Single 455×300 mm board is expensive to rework or replace | Individual boards can be swapped independently |
| Wear item isolation | Relays (100k ops) and contactors (10k ops) mixed with long-life power electronics complicates replacement | Power Entry board consolidates all electromechanical wear items onto one replaceable PCB |
| Stacking modularity | 5-module 150 kW system needs identical power stages | Power boards are standardized; controller can vary per application |

## 2. Board Summary

| PCB | Function | Layer Count | Estimated Size (mm) | Cu Weight |
|-----|----------|-------------|----------------------|-----------|
| **Power Entry** | AC input protection (NTC, bypass relay), DC output isolation (contactor), external connectors | 2 | 150 × 120 | 4 oz |
| **AC-DC** | Vienna Rectifier PFC — EMI filter, 3-phase rectification, DC bus caps | 6 | 250 × 180 | 2 oz (4 oz power layers optional) |
| **DC-DC** | LLC Resonant converter — primary bridge, transformer, secondary rectifier, output caps | 6 | 250 × 180 | 2 oz (4 oz power layers optional) |
| **Controller** | STM32G474RE, CAN bus, analog signal conditioning, OCPP/ISO 15118 | 4 | 120 × 100 | 1 oz |
| **Aux PSU** | Isolated supplies — gate drives (+18 V/−5 V), logic (3.3 V/5 V), fan (12 V), standby | 4 | 100 × 80 | 1 oz (2 oz for power rails) |

## 3. Mechanical Arrangement

```
┌───────────────────────────────────────────────────────────────────┐
│  ENCLOSURE (1U or 2U rack-mount, forced-air cooled)               │
│                                                                   │
│  ┌────────────┐          ┌────────────┐          ┌────────────┐   │
│  │ Power Entry│  P1b     │  AC-DC     │  P2      │  DC-DC     │   │
│  │ Board      │ ──60A──→ │  Board     │ =======> │  Board     │   │
│  │            │  530VAC  │            │  920VDC  │            │   │
│  │ AC In(P1a) │          │            │  40A     │       P3a  │   │
│  │ DC Out(P3b)│ ←──────────────────────────────────── 100A ──┘   │
│  └─────┬──────┘          └─────┬──────┘          └─────┬──────┘   │
│     S4 │ Harness               │ Harness               │ Harness │
│        │                 ┌─────┴──────┐          ┌─────┴──────┐   │
│        │                 │ Aux PSU    │ ←──3.3V── │ Controller │   │
│        └────────────────→│ Board      │ ──18V/─5V─│ Board      │   │
│                          │  (+24V coil)│          │        CAN──→  │
│                          └────────────┘          └────────────┘   │
│                                                                   │
│  ← Airflow direction (fan on exhaust side)                        │
└───────────────────────────────────────────────────────────────────┘
```

> [!note] Power Entry Board Placement
> The Power Entry board sits at the enclosure edge with AC input (P1a) and DC output (P3b) connectors facing outward through panel cutouts. Internal connections (P1b to AC-DC, P3a from DC-DC, S4 from Controller) route inward. This keeps high-current external cabling short and provides direct access for connector/relay/contactor replacement.

## 4. Power Interfaces

### 4.1 P1a: AC Mains → Power Entry Board (External Input)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | L1 (Phase A) | 530 VAC, 60 A | M6 stud or high-current terminal block |
| 2 | L2 (Phase B) | 530 VAC, 60 A | M6 stud |
| 3 | L3 (Phase C) | 530 VAC, 60 A | M6 stud |
| 4 | PE (Protective Earth) | Safety ground | M6 stud, bonded to chassis |

### 4.2 P1b: Power Entry Board → AC-DC Board (Internal)

AC is routed through the NTC thermistors and bypass relays on the [[07-PCB-Layout/Power-Entry/__init|Power Entry board]] before reaching the AC-DC board's EMI filter.

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | L1_FILT (Phase A, post-NTC/relay) | 530 VAC, 60 A | Molex MegaFit or wire harness, 10 AWG |
| 2 | L2_FILT (Phase B, post-NTC/relay) | 530 VAC, 60 A | — |
| 3 | L3_FILT (Phase C, post-NTC/relay) | 530 VAC, 60 A | — |

### 4.3 P2: AC-DC Board → DC-DC Board (DC Bus)

> [!warning] Critical Interface
> This is a high-current, high-voltage bus bar connection. Parasitic inductance must be minimized (<5 nH) to avoid voltage overshoot on the LLC primary.

| Pin | Signal | Rating | Implementation |
|-----|--------|--------|----------------|
| 1 | DC_BUS+ | 920 VDC, 40 A | Laminated bus bar, M4 bolted |
| 2 | DC_BUS− | 920 VDC, 40 A | Laminated bus bar, M4 bolted |
| 3 | DC_BUS_MID (optional) | Vienna midpoint | For balancing sense |

**Bus bar specification:**
- Material: Copper, 2 mm thick, tin-plated
- Width: ≥20 mm (for 40 A with <30°C rise)
- Laminated pair (+ and − sandwiched with 0.2 mm Kapton) for low inductance
- Length: ≤80 mm between boards

### 4.4 P3a: DC-DC Board → Power Entry Board (Internal, Pre-Contactor)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | DC_PRE_CONT+ | 150–1000 VDC, 100 A | M8 stud or bus bar, 8 AWG min |
| 2 | DC_PRE_CONT− | 150–1000 VDC, 100 A | M8 stud or bus bar |

### 4.5 P3b: Power Entry Board → DC Output (External)

DC output is routed through the output contactor (TE EV200) on the [[07-PCB-Layout/Power-Entry/__init|Power Entry board]] before reaching the external connector.

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | DC_OUT+ | 150–1000 VDC, 100 A | M8 stud or Anderson SB175 |
| 2 | DC_OUT− | 150–1000 VDC, 100 A | M8 stud or Anderson SB175 |
| 3 | PE | Safety ground | M6 stud |

### 4.6 P4: Aux PSU Board → Power Boards (Gate Drive Power)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | VDRV_AC+ | +18 V, 0.5 A (AC-DC board) | Molex Micro-Fit 3.0, 4-pin |
| 2 | VNEG_AC | −5 V, 0.2 A (AC-DC board) | — |
| 3 | VDRV_AC_RTN | Isolated return | — |
| 4 | Shield | Cable shield to PE | — |
| 5 | VDRV_DC+ | +18 V, 0.5 A (DC-DC board) | Molex Micro-Fit 3.0, 4-pin |
| 6 | VNEG_DC | −5 V, 0.2 A (DC-DC board) | — |
| 7 | VDRV_DC_RTN | Isolated return | — |
| 8 | Shield | Cable shield to PE | — |

> [!tip] Isolation Domains
> Each gate drive supply pair (VDRV/VNEG) is independently isolated from logic ground and from each other. The Aux PSU provides 2 isolated gate drive channels — one per power board.

### 4.7 P5: Aux PSU Board → Controller Board (Logic Power)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | +5 V | 5 V, 1 A | Molex Micro-Fit 3.0, 4-pin |
| 2 | +3.3 V | 3.3 V, 0.5 A | — |
| 3 | GND | Logic ground | — |
| 4 | +12 V_FAN | 12 V, 2 A (fan supply) | — |

## 5. Signal Interfaces

### 5.1 S1: Controller → AC-DC Board (Control Harness)

| Pin | Signal | Type | Connector |
|-----|--------|------|-----------|
| 1 | PWM_A_H | HRTIM output, 3.3 V | Molex Pico-Lock, 12-pin |
| 2 | PWM_A_L | HRTIM output, 3.3 V | — |
| 3 | PWM_B_H | HRTIM output, 3.3 V | — |
| 4 | PWM_B_L | HRTIM output, 3.3 V | — |
| 5 | PWM_C_H | HRTIM output, 3.3 V | — |
| 6 | PWM_C_L | HRTIM output, 3.3 V | — |
| 7 | I_SENSE_A | Analog, 0–3.3 V | Shielded pair |
| 8 | I_SENSE_B | Analog, 0–3.3 V | Shielded pair |
| 9 | I_SENSE_C | Analog, 0–3.3 V | Shielded pair |
| 10 | V_BUS_SENSE | Analog, 0–3.3 V | Shielded pair |
| 11 | FAULT_PFC | Open-drain, active low | — |
| 12 | GND_SENSE | Analog ground reference | — |

### 5.2 S2: Controller → DC-DC Board (Control Harness)

| Pin | Signal | Type | Connector |
|-----|--------|------|-----------|
| 1 | PWM_LLC_A | HRTIM output, 3.3 V | Molex Pico-Lock, 10-pin |
| 2 | PWM_LLC_B | HRTIM output, 3.3 V | — |
| 3 | PWM_LLC_C | HRTIM output, 3.3 V | — |
| 4 | PWM_SR_A | Sync rect drive, 3.3 V | — |
| 5 | PWM_SR_B | Sync rect drive, 3.3 V | — |
| 6 | PWM_SR_C | Sync rect drive, 3.3 V | — |
| 7 | V_OUT_SENSE | Analog, 0–3.3 V | Shielded pair |
| 8 | I_OUT_SENSE | Analog, 0–3.3 V | Shielded pair |
| 9 | FAULT_LLC | Open-drain, active low | — |
| 10 | GND_SENSE | Analog ground reference | — |

### 5.3 S3: Controller → CAN Bus (External)

| Pin | Signal | Type | Connector |
|-----|--------|------|-----------|
| 1 | CAN_H | CAN 2.0B, 1 Mbps | DB-9 or M12 |
| 2 | CAN_L | CAN 2.0B, 1 Mbps | — |
| 3 | GND | CAN ground reference | — |
| 4 | Shield | Cable shield | — |

### 5.4 S4: Controller → Power Entry Board (Relay/Contactor Control)

| Pin | Signal | Type | Connector |
|-----|--------|------|-----------|
| 1 | RELAY_A_DRV | 3.3 V logic (relay coil drive) | Molex Micro-Fit 3.0, 8-pin |
| 2 | RELAY_B_DRV | 3.3 V logic (relay coil drive) | — |
| 3 | RELAY_C_DRV | 3.3 V logic (relay coil drive) | — |
| 4 | CONT_DRV | 3.3 V logic (contactor coil drive) | — |
| 5 | CONT_AUX_FB | Digital input (contactor aux contact) | — |
| 6 | +24V_COIL | 24 VDC coil power from Aux PSU | — |
| 7 | PE_STATUS | Digital output (board health, optional) | — |
| 8 | GND | Signal ground reference | — |

> [!note] The S4 harness carries only low-current logic signals (pins 1–5, 7–8) and the 24 VDC coil supply (pin 6, ≤0.5 A). The N-channel MOSFET coil drivers reside on the Power Entry board, keeping high-current relay/contactor coil wiring local. See [[07-PCB-Layout/Power-Entry/__init|Power Entry Board]] for driver circuit details.

## 6. Harness Design Rules

> [!warning] EMI-Critical Routing
> Signal harnesses between controller and power boards carry HRTIM PWM signals (up to 500 kHz fundamental) adjacent to analog sense signals. Proper harness design is essential.

1. **PWM signals:** Use twisted pairs (signal + ground return) — impedance ~100 Ω
2. **Analog sense signals:** Use shielded twisted pairs with shield grounded at controller end only (avoids ground loops)
3. **Power harness cables:** ≥16 AWG for gate drive supplies, ≥12 AWG for fan/logic
4. **Harness length:** ≤200 mm between any two boards (minimize propagation delay and EMI pickup)
5. **Separation:** Maintain ≥20 mm between power bus bar and signal harness bundles
6. **Connector keying:** Each harness uses a unique connector keying to prevent mis-mating

## 7. Grounding Strategy

```
                    ┌─────────────┐
                    │  Chassis PE │ (single-point bond to enclosure)
                    └──────┬──────┘
                           │
     ┌─────────────────────┼───────────────────┐
     │            │        │          │         │
┌────┴─────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ Power    │ │ AC-DC   │ │ DC-DC   │ │ Aux PSU │
│ Entry    │ │ Power   │ │ Power   │ │ Safety  │
│ PE Bond  │ │ GND     │ │ GND     │ │ GND     │
└──────────┘ └─────────┘ └─────────┘ └─────────┘
                                          │
                                    ┌─────┴──────┐
                                    │ Controller │
                                    │ Logic GND  │
                                    └────────────┘
```

- Each power board has its own ground plane, bonded to chassis PE via a single low-impedance point (M4 stud)
- Controller logic GND connects to chassis through the Aux PSU board (single reference)
- No ground loops between boards — star topology from chassis PE
- Analog sense returns routed as dedicated wires in signal harness (not through power ground)

## 8. Design Verification Checklist

- [ ] Bus bar inductance P2 measured or simulated <5 nH
- [ ] All connector voltage ratings exceed working voltage + 20% margin
- [ ] Harness length ≤200 mm, separation from bus bar ≥20 mm
- [ ] Each isolation domain independently tested (hipot per IEC 62368-1)
- [ ] Connector keying prevents all possible mis-mating scenarios
- [ ] Thermal interface between boards and chassis validated (no air gaps)

## 9. Related Documents

- [[07-PCB-Layout/Power-Entry/__init|Power Entry Board]] — NTC, bypass relay, output contactor, external connectors
- [[01-Topology Selection]] — Circuit topology that defines the power stages
- [[02-Magnetics Design]] — Transformer and inductor specs for DC-DC board
- [[04-Thermal Budget]] — Loss allocation per board, cooling requirements
- [[05-EMI Filter Design]] — EMI filter on AC-DC board, separation rules
- [[06-Firmware Architecture]] — Control signals mapped to harness pinouts
- [[08-Power-On Sequence and Inrush Management]] — Startup sequence, NTC/relay/contactor specifications

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
