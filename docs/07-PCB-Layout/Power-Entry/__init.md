---
tags: [pdu, pcb-layout, power-entry, contactor, relay, inrush]
created: 2026-02-22
status: draft
aliases: [Power Entry Board, Contactor Board, PE-CONT-01]
---

# Power Entry Board — Contactor and Relay Board

## Overview

The Power Entry board (PE-CONT-01) consolidates all **electromechanical power-path components** onto a single, independently replaceable PCB. It handles AC input protection (NTC inrush limiting, bypass relay), DC output isolation (main contactor, optional pre-charge), and provides the physical home for all external power connectors.

This board was introduced as part of the transition from 4-board to **[[07-PCB-Layout/00-Board Partitioning|5-board architecture]]** to address three problems with the original design:

1. **Serviceability** — Relays and contactors are wear items (10k–100k electrical operations) that should not be mixed with long-life power electronics. The Power Entry board can be replaced without disturbing the AC-DC or DC-DC boards.
2. **Thermal isolation** — NTCs dissipate significant I²R heat during inrush (~75 A × 10 Ω per phase). Relay and contactor coils add ~8 W continuous. Separating these from the AC-DC board's EMI filter zone prevents heating of temperature-sensitive CM choke cores.
3. **Voltage domain separation** — The AC input bypass relay (530 VAC, 60 A) and DC output contactor (1000 VDC, 100 A) serve different voltage domains. A dedicated board with physical separation avoids creepage/clearance challenges that arise from mixing both on a power stage board.

## Board Summary

| Parameter | Value |
|-----------|-------|
| Board designation | PE-CONT-01 |
| Function | AC input protection, DC output isolation, inrush management |
| Board dimensions | 150 mm × 120 mm |
| Layer count | 2 (or 4 for improved thermal spreading) |
| Copper weight | 4 oz (high-current paths: 60 A AC, 100 A DC) |
| Minimum trace/space | 0.3 mm / 0.3 mm (signal); power per IPC-2152 |
| Surface finish | HASL or ENIG |
| Board thickness | 2.0 mm (mechanical rigidity for relay/contactor mounting) |
| Material | FR-4 Tg 170°C (or CEM-3 for cost reduction) |

> [!tip] No High-Frequency Switching
> Unlike the AC-DC and DC-DC boards, the Power Entry board contains no active switching components. EMI generation is minimal — limited to relay/contactor coil transients, which are suppressed by flyback diodes and RC snubbers. This simplifies the design to a 2-layer board with heavy copper.

## Functional Zones

The board is organized into three physically separated zones:

```
┌──────────────────────────────────────────────────────────┐
│  AC Input Zone       │  Control Zone  │  DC Output Zone   │
│  (~60 mm)            │  (~30 mm)      │  (~60 mm)         │
│                      │                │                   │
│  AC input connector  │  Relay coil    │  Output contactor │
│  (P1a: 3P+PE)        │  drivers       │  (TE EV200)       │
│                      │  (3× NTC byp.  │                   │
│  3× NTC thermistors  │   + 1× cont.)  │  Pre-charge res.  │
│  (10 Ω, inrush)      │                │  (optional, Rev2) │
│                      │  Aux contact   │                   │
│  3× Bypass relays    │  sense inputs  │  DC output conn.  │
│  (60A, 600VAC N.O.)  │                │  (P3b: 2P+PE)     │
│                      │  LED status    │                   │
│  RC snubbers         │  indicators    │  Sense wires      │
│  (100Ω + 47nF)       │                │  (V_out, I_out)   │
│                      │  Signal conn.  │                   │
│  Fuse holders (opt.) │  (S4: 8-pin)   │                   │
└───────────────────────────────────────────────────────────┘
     ↑ P1a                                    P3b ↑
  AC from mains                          DC to vehicle
```

### Zone 1: AC Input Zone (~60 mm width)

Houses the AC mains entry point and inrush limiting components.

| Component | Specification | Qty | Reference |
|-----------|--------------|-----|-----------|
| AC input connector (P1a) | 3P+PE, 60 A, panel mount (M6 stud) | 1 | [[07-PCB-Layout/00-Board Partitioning\|Board Partitioning]] |
| NTC thermistors | 10 Ω @ 25°C, disc ≥15 mm, 150 J rated | 3 | [[08-Power-On Sequence and Inrush Management]] §3.2 |
| Bypass relays | 60 A, 600 VAC, N.O. single-pole (e.g., Panasonic HE1AN) | 3 | [[08-Power-On Sequence and Inrush Management]] §3.3 |
| RC snubbers | 100 Ω + 47 nF, 630 VAC rated, across each relay contact | 3 sets | [[08-Power-On Sequence and Inrush Management]] §3.5 |
| AC output connector (P1b) | 3P, 60 A, board-to-board or wire harness to AC-DC | 1 | — |

**Current path:** Mains → P1a → NTC → relay contact (bypasses NTC when closed) → P1b → AC-DC board EMI filter.

### Zone 2: Control Zone (~30 mm width)

Provides coil drive circuits and feedback sensing. All control signals run at 24 VDC or logic level (3.3 V).

| Component | Specification | Qty | Notes |
|-----------|--------------|-----|-------|
| Relay coil drivers | N-channel MOSFET + flyback diode, 24 VDC | 3 | One per bypass relay |
| Contactor coil driver | N-channel MOSFET + flyback diode, 24 VDC, 5 W | 1 | For TE EV200 |
| Auxiliary contact sense | Pull-up + RC debounce, contactor aux NO contact | 1 | Welding detection |
| Status LEDs | AC present, relay state, contactor state | 3 | Visual diagnostics |
| Signal connector (S4) | Molex Micro-Fit 3.0, 8-pin | 1 | To Controller board |

### Zone 3: DC Output Zone (~60 mm width)

Houses the main DC output contactor and output connector.

| Component | Specification | Qty | Reference |
|-----------|--------------|-----|-----------|
| Output contactor | TE EV200HAANA, 1000 VDC, 200 A, 24 VDC coil | 1 | [[08-Power-On Sequence and Inrush Management]] §4.3 |
| Pre-charge resistor | 100–500 Ω, 50 W (optional, Rev 2) | 1 | [[08-Power-On Sequence and Inrush Management]] §4.4 |
| Pre-charge relay | 10 A, 1000 VDC, N.O. (optional, Rev 2) | 1 | — |
| DC input connector (P3a) | 2P, 100 A, from DC-DC board output | 1 | — |
| DC output connector (P3b) | 2P+PE, 100 A, panel mount (M8 stud or Anderson SB175) | 1 | [[07-PCB-Layout/00-Board Partitioning\|Board Partitioning]] |

**Current path:** DC-DC board → P3a → contactor → P3b → vehicle connector.

## Creepage and Clearance

The Power Entry board carries two distinct high-voltage domains that must be separated from each other and from the control zone (PE-referenced).

| Interface | Working Voltage | Insulation Class | Creepage (min) | Clearance (min) | Implementation |
|-----------|----------------|-----------------|----------------|-----------------|----------------|
| AC zone → PE (control) | 530 VAC (750 Vpk) | Reinforced, PD2, IIIb | 10 mm | 6 mm | PCB routing gap |
| DC zone → PE (control) | 1000 VDC | Reinforced, PD2, IIIb | 15 mm | 8.5 mm | PCB routing gap |
| AC zone → DC zone | 530 VAC + 1000 VDC | Reinforced | ≥20 mm | ≥12 mm | **PCB slot** (routed channel) |
| Relay contacts (open) | 600 VAC | Basic | 6 mm | 3 mm | Internal to relay |
| Contactor contacts (open) | 1000 VDC | Basic | 10 mm | 6 mm | Internal to contactor |

> [!warning] AC-to-DC Zone Separation
> The AC input zone and DC output zone carry voltages from independent sources (grid and vehicle battery). A routed PCB slot (≥2 mm wide, ≥20 mm creepage path around the slot) provides the required reinforced insulation barrier between these domains per IEC 62368-1.

### PCB Slot Detail

```
         AC Input Zone                    DC Output Zone
    ┌─────────────────────┐          ┌─────────────────────┐
    │                     │          │                     │
    │  NTC  Relay  Snub   │  ≥20mm   │  Contactor  P3b     │
    │                     │ ┌──────┐ │                     │
    │  P1a         P1b    │ │ SLOT │ │  P3a        PE      │
    │                     │ │(rout)│ │                     │
    │                     │ └──────┘ │                     │
    └─────────────────────┘          └─────────────────────┘
                   Control Zone bridges above/below slot
                   (24 VDC only — safe voltage domain)
```

The control zone signal traces route around the ends of the slot, maintaining ≥10 mm creepage to both AC and DC copper on adjacent layers.

## Power Interfaces

### P1a: AC Mains → Power Entry Board (External Input)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | L1 (Phase A) | 530 VAC, 60 A | M6 stud or high-current terminal block |
| 2 | L2 (Phase B) | 530 VAC, 60 A | M6 stud |
| 3 | L3 (Phase C) | 530 VAC, 60 A | M6 stud |
| 4 | PE (Protective Earth) | Safety ground | M6 stud, bonded to chassis |

### P1b: Power Entry Board → AC-DC Board (Internal)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | L1_FILT (Phase A, post-NTC/relay) | 530 VAC, 60 A | Molex MegaFit or wire harness, 10 AWG |
| 2 | L2_FILT (Phase B, post-NTC/relay) | 530 VAC, 60 A | — |
| 3 | L3_FILT (Phase C, post-NTC/relay) | 530 VAC, 60 A | — |

> [!note] PE is not carried on P1b. The AC-DC board bonds to chassis PE independently via its own M4 stud, per the [[07-PCB-Layout/00-Board Partitioning#Grounding Strategy|grounding strategy]].

### P3a: DC-DC Board → Power Entry Board (Internal)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | DC_PRE_CONT+ | 150–1000 VDC, 100 A | M8 stud or bus bar, 8 AWG min |
| 2 | DC_PRE_CONT− | 150–1000 VDC, 100 A | M8 stud or bus bar |

### P3b: Power Entry Board → DC Output (External)

| Pin | Signal | Rating | Connector |
|-----|--------|--------|-----------|
| 1 | DC_OUT+ | 150–1000 VDC, 100 A | M8 stud or Anderson SB175 |
| 2 | DC_OUT− | 150–1000 VDC, 100 A | M8 stud or Anderson SB175 |
| 3 | PE | Safety ground | M6 stud |

## Signal Interface

### S4: Controller → Power Entry Board (Signal Harness)

| Pin | Signal | Type | Direction | Notes |
|-----|--------|------|-----------|-------|
| 1 | RELAY_A_DRV | 3.3 V logic → MOSFET gate | Ctrl → PE | Bypass relay A coil drive |
| 2 | RELAY_B_DRV | 3.3 V logic → MOSFET gate | Ctrl → PE | Bypass relay B coil drive |
| 3 | RELAY_C_DRV | 3.3 V logic → MOSFET gate | Ctrl → PE | Bypass relay C coil drive |
| 4 | CONT_DRV | 3.3 V logic → MOSFET gate | Ctrl → PE | Output contactor coil drive |
| 5 | CONT_AUX_FB | Digital input, pull-up on PE board | PE → Ctrl | Contactor auxiliary contact (welding detection) |
| 6 | +24V_COIL | 24 VDC from Aux PSU | — | Coil power supply |
| 7 | PE_STATUS | Digital output (3 bits encoded or SPI) | PE → Ctrl | Board health / LED mirror (optional) |
| 8 | GND | Signal ground reference | — | Tied to Aux PSU GND |

**Connector:** Molex Micro-Fit 3.0, 8-pin, keyed to prevent mis-mating with S1/S2/S3.

> [!tip] Coil Drive Architecture
> The 3.3 V logic signals from the Controller board drive N-channel MOSFETs (e.g., IRLML6244) on the Power Entry board. The MOSFETs switch the 24 VDC coil current. This keeps high-current coil wiring local to the Power Entry board and only routes low-current logic signals in the harness.

## Thermal Considerations

| Heat Source | Power (W) | Duty | Notes |
|-------------|----------|------|-------|
| NTC thermistors (3×) | ~200 W peak (transient) | ~3 s at startup | Self-heating; bypassed after pre-charge |
| Bypass relay coils (3×) | 3 W total (~1 W each) | Continuous after T2 | Low; relay body acts as heatsink |
| Output contactor coil | 4–5 W | Continuous after T5 | TE EV200 specifies 4 W coil |
| Contactor contact I²R | 3–10 W | Load-dependent | R_contact < 0.3 mΩ × 100² A = 3 W typ, 10 W max |
| **Total continuous** | **~10–18 W** | | |

The Power Entry board does not require a dedicated heatsink. Natural convection and enclosure airflow (from the main fan system) are sufficient for the ~18 W worst-case continuous dissipation. The NTC transient heat (~200 W for 3 s) is absorbed by the NTC disc thermal mass and dissipated before steady-state operation begins.

> [!note] Board Placement
> The Power Entry board should be mounted at the **enclosure edge** (AC input on one face, DC output on the opposite face) to keep power cable runs short and provide direct access for connector replacement. It sits upstream of the AC-DC board and downstream of the DC-DC board in the power flow.

## Mechanical Integration

- **Mounting:** 4× M3 standoffs, secured to chassis or DIN rail bracket
- **Connector orientation:** AC input (P1a) and DC output (P3b) face outward toward enclosure panel cutouts; internal connectors (P1b, P3a, S4) face inward toward the other boards
- **Contactor mounting:** TE EV200 has M5 mounting holes on 40 mm centers — PCB provides matching through-holes with reinforced copper pads
- **NTC mounting:** Disc NTCs soldered to heavy-copper pads (4 oz) or mounted with spring clips if through-hole leads are used
- **Relay mounting:** PCB-mount relays (e.g., Panasonic HE1AN has PCB pins) or chassis-mount with wire connections

## Design Verification Checklist

- [ ] PCB slot width ≥2 mm between AC and DC zones
- [ ] Creepage AC zone → PE ≥10 mm verified in layout
- [ ] Creepage DC zone → PE ≥15 mm verified in layout
- [ ] Creepage AC zone → DC zone ≥20 mm (around slot) verified
- [ ] All relay/contactor coil drivers include flyback diodes (e.g., 1N4148WS)
- [ ] RC snubbers rated ≥630 VAC across each bypass relay contact
- [ ] Contactor auxiliary contact debounce circuit verified (RC time constant ~10 ms)
- [ ] S4 connector keyed uniquely vs. S1/S2/S3
- [ ] P1a and P3b connector voltage ratings exceed working voltage + 20% margin
- [ ] 4 oz copper trace widths per IPC-2152 for 60 A (AC) and 100 A (DC) paths
- [ ] Board PE bond via M4 stud to chassis verified in grounding strategy

## Related Documents

- [[07-PCB-Layout/00-Board Partitioning]] — 5-board architecture overview and all interfaces
- [[07-PCB-Layout/AC-DC/__init|AC-DC Board]] — Receives AC input from this board via P1b
- [[07-PCB-Layout/DC-DC/__init|DC-DC Board]] — Sends DC output to this board via P3a
- [[08-Power-On Sequence and Inrush Management]] — NTC, relay, and contactor specifications and timing
- [[07-BOM and Cost Analysis]] — Component costs (NTC, relay, contactor unchanged; PCB + harness added)
- [[07-PCB-Layout/AC-DC/06-Creepage and Clearance|Creepage and Clearance (AC-DC)]] — IEC 62368-1 creepage/clearance reference

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: board definition, zone map, interfaces, creepage analysis |
