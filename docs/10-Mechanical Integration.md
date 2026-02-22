---
tags: [PDU, mechanical, enclosure, thermal, heatsink]
created: 2026-02-22
status: draft
aliases: [Mechanical Integration, Enclosure Design]
---

# 10 — Mechanical Integration

## 1. Overview

This document defines the mechanical integration of the 30 kW PDU module, covering how four PCBs, the shared heatsink assembly, fan system, bus bars, signal harnesses, and external connectors are packaged into a single hot-swappable enclosure.

### 1.1 Scope

The mechanical design addresses:

- **Enclosure** — sheet metal housing with EMC shielding, rack-mount interface, and serviceability features
- **Heatsink** — forced-air cooled extrusion shared between the AC-DC and DC-DC power boards
- **Fan system** — axial fans with PWM speed control and dust filtration
- **Bus bars** — laminated DC bus interconnect and high-current output bars
- **Board mounting** — standoffs, heatsink attachment, vibration resistance
- **Connectors** — all external and internal electrical interfaces
- **Airflow path** — front-to-rear forced convection through heatsink fins

### 1.2 Form Factor

| Parameter | Value |
|-----------|-------|
| Dimensions (W × D × H) | 455 × 300 × 94 mm |
| Rack format | 3U × half-rack width (or 2U full-width variant) |
| Weight target | < 17 kg |
| Module stacking | 5 modules per 150 kW rack via CAN bus |
| Insertion method | Slide-rail hot-swap, blind-mate DC output |

### 1.3 Design Philosophy

1. **Serviceability** — each board is independently replaceable without removing the heatsink or other boards. Signal harnesses use latching connectors for tool-free disconnect.
2. **Thermal performance** — direct MOSFET-to-heatsink mounting with low-resistance TIM; heatsink sized for full 30 kW at 45°C ambient without derating.
3. **EMC shielding** — continuous conductive contact at all panel joints; filtered cable entries; internal partitioning between power and control sections.
4. **Manufacturability** — sheet metal enclosure uses standard bend radii and hardware; heatsink is a single extrusion cut to length.

---

## 2. Enclosure Design

### 2.1 Material and Finish

| Property | Specification |
|----------|---------------|
| Material | Aluminum 6061-T6, 1.2 mm walls / 1.6 mm baseplate |
| Surface treatment | Chromate conversion coating (MIL-DTL-5541, Type I, Class 3) |
| Exterior finish | Powder coat, RAL 7016 (anthracite grey), 60–80 µm |
| EMC conductivity | Chromate under powder coat on mating surfaces; bare aluminum or conductive gasket at panel joints |

> [!tip] Why 6061-T6?
> Provides good strength-to-weight ratio (yield 276 MPa), machinability, and corrosion resistance. 1.2 mm sheet keeps weight under budget while providing adequate stiffness for rack-mount loads.

### 2.2 IP Rating

- **IP20 (baseline):** Top and bottom panels include ventilation slots for direct airflow. Suitable for indoor cabinet installations where the outer enclosure provides weather protection.
- **IP54 (option):** All ventilation sealed; cooling via air-to-air heat exchanger or sealed recirculating loop. Adds ~2 kg and ~15% thermal derating.

### 2.3 Panel Layout

**Front panel (455 × 94 mm):**
- AC input connector (3-phase + N + PE), left side
- CAN bus port (DB-9 or M12), center
- Ethernet port (RJ45, shielded), center
- Status LEDs (Power, Fault, CAN Activity), right of center
- Extraction handle with latch mechanism, right side

**Rear panel (455 × 94 mm):**
- DC output studs (M8, + / − / PE), center
- Fan exhaust grille (perforated, 60% open area), full width
- PE bonding stud (M6), bottom corner

**Top panel (455 × 300 mm):**
- Ventilation slots (IP20): 3 mm wide × 30 mm long, staggered pattern, ≥40% open area over heatsink region
- Removable cover secured by 4× M3 captive screws (for board access)

**Bottom panel (455 × 300 mm):**
- Intake ventilation slots (IP20), same pattern as top
- Rack slide rail mounting points, 4× M4 tapped holes per side

### 2.4 Rack Slide Rails

- Type: Telescoping ball-bearing slides, 300 mm travel
- Load rating: ≥25 kg per pair (provides margin for 17 kg module)
- Hot-swap: module slides out for service; blind-mate DC connector at rear engages automatically on insertion
- Latch: front panel latch locks module in operating position; lever releases for extraction
- Guide pins: 2× tapered guide pins on rear panel align module to backplane before electrical contact

---

## 3. Internal Layout and Board Arrangement

### 3.1 Top-Down Layout Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ FRONT PANEL  [AC IN]  [CAN] [ETH] [LEDs]  [HANDLE/LATCH]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐    ┌──────────────────────┐       │
│  │                      │    │                      │       │
│  │     AC-DC Board      │    │     DC-DC Board      │       │
│  │     250 × 180 mm     │ P2 │     250 × 180 mm     │       │
│  │                      │◄──►│                      │       │
│  │  [EMI]  [PFC]  [Caps]│bus │ [Pri] [Xfmr] [Sec]   │       │
│  │                      │bar │                      │       │
│  └──────────┬───────────┘    └──────────┬───────────┘       │
│             │                           │                   │
│       ┌─────┴──────┐  ┌────────────┐    │  output bus bar   │
│       │  Aux PSU   │  │ Controller │    │  to rear panel    │
│       │  100 × 80  │  │ 120 × 100  │    ▼                   │
│       └────────────┘  └────────────┘  [DC OUT STUDS]        │
│                                                             │
│                     ◄── AIRFLOW DIRECTION ──►               │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            FAN ZONE  (80mm × 2 or 120mm × 1)           │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ REAR PANEL      [DC+] [DC−] [PE]     [FAN EXHAUST GRILLE]   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Side Profile (Cross-Section)

```
          ◄─── 300 mm (depth) ──►
    ┌─────────────────────────────┐ ─┬─
    │  TOP COVER (removable)      │  │
    ├─────────────────────────────┤  │
    │  PCB components (top side)  │  │
    │  ─ ─ ─ ─ PCB ─ ─ ─ ─ ─ ─  │  │ 94 mm
    │  MOSFET tabs ↓              │  │
    │  ═══ TIM (0.25 mm) ═══════ │  │
    │  ▓▓▓ HEATSINK BASE (8mm) ▓ │  │
    │  ║║║║ FINS (35 mm) ║║║║║║║ │  │
    ├─────────────────────────────┤  │
    │  BASEPLATE                  │  │
    └─────────────────────────────┘ ─┴─
```

### 3.3 Board Placement Rules

| Rule | Specification |
|------|---------------|
| AC-DC board position | Left side, adjacent to AC input connector |
| DC-DC board position | Right side, adjacent to DC output studs |
| Controller board position | Bottom-center, below power boards, shielded from power stage EMI |
| Aux PSU position | Bottom-left, between AC-DC and controller, close to gate drive outputs |
| Board-to-board clearance | ≥ 10 mm vertical, ≥ 5 mm horizontal (airflow channels) |
| Signal harness routing | Along enclosure side walls, physically separated ≥ 15 mm from bus bars |
| Creepage (AC-DC to enclosure) | ≥ 8 mm (per IEC 62109-1 for 530 VAC working voltage) |
| Creepage (DC bus to enclosure) | ≥ 10 mm (920 VDC bus) |

### 3.4 Airflow Path

The airflow path is designed as a single front-to-rear pass:

1. **Intake** — air enters through bottom and front ventilation slots, passes through removable dust filter
2. **EMI filter section** — low-loss components, air pre-heats minimally (~2–3°C)
3. **PFC MOSFETs and boost inductors** — primary heat source on AC-DC board, heatsink fins below
4. **DC bus capacitors** — moderate heating, benefits from airflow
5. **LLC primary MOSFETs** — second major heat source on DC-DC board
6. **Transformer and output rectifiers** — remaining losses on DC-DC board
7. **Exhaust fans** — pull air through the entire heatsink fin field and exhaust through rear grille

> [!warning] Do not reverse the airflow direction
> The EMI filter components have the lowest thermal sensitivity and should receive the coolest air. Reversing the flow would expose the most temperature-sensitive components (SiC MOSFETs) to pre-heated air from the transformer, reducing thermal margin.

---

## 4. Heatsink Design

### 4.1 Heatsink Geometry

| Parameter | Value |
|-----------|-------|
| Type | Extruded aluminum, single piece |
| Material | 6063-T5 (k = 201 W/m·K) |
| Overall length | 455 mm (spans both AC-DC and DC-DC boards) |
| Width | 180 mm (matches board width) |
| Base thickness | 8 mm |
| Fin height | 35 mm |
| Fin thickness | 1.5 mm |
| Fin pitch | 3.5 mm (center-to-center) |
| Number of fins | ~50 |
| Fin efficiency (forced air, 2.5 m/s) | ~82% |
| Total surface area | ~0.85 m² |
| Mass | ~3.2 kg |

### 4.2 Heatsink Configuration Options

**Option A — Single Continuous Heatsink (recommended):**

- One extrusion spans the full 455 mm enclosure width
- Both AC-DC and DC-DC boards mount to the same heatsink
- Advantages: better thermal spreading between boards, simpler assembly, fewer parts
- Disadvantage: replacing one board requires partial disassembly of the other board's mounting

**Option B — Dual Separate Heatsinks:**

- Two extrusions, each ~220 mm long, with a 15 mm gap between them
- Each board has its own thermally independent heatsink
- Advantage: easier single-board replacement
- Disadvantage: no thermal cross-coupling benefit, slightly higher total Rth_sa

> [!note] Recommendation
> Option A (single heatsink) is selected as the baseline. The thermal spreading benefit is worth ~5°C at the hottest MOSFET, which directly translates to extended derating headroom. Board replacement is infrequent enough that the minor disassembly penalty is acceptable.

### 4.3 Thermal Interface Material (TIM)

| Property | Specification |
|----------|---------------|
| Material | Bergquist Gap Pad GP3000S30 (or equivalent) |
| Thermal conductivity | 3.0 W/m·K |
| Thickness | 0.25 mm (compressed) |
| Compressive force | 50–100 psi at rated thickness |
| Operating temperature | −40°C to +200°C |
| Dielectric breakdown | 10 kV/mm (2.5 kV at 0.25 mm) |

Alternative: Shin-Etsu MicroSi TC-30AG thermal grease (4.3 W/m·K) for lower Rth_cs but requires careful dispensing control during assembly.

### 4.4 Thermal Resistance Budget

Per MOSFET device (e.g., C3M0032120K in TO-247-4):

| Thermal Path | Symbol | Value (°C/W) | Notes |
|--------------|--------|-------------|-------|
| Junction to case | Rth_jc | 0.50 | Datasheet maximum |
| Case to heatsink | Rth_cs | 0.12 | GP3000S, 0.25 mm, 1.3 cm² contact |
| Heatsink to ambient | Rth_sa | 0.35 | Forced air 2.5 m/s, per device footprint |
| **Junction to ambient** | **Rth_ja** | **0.97** | **Total** |

**Temperature check at worst case (55°C ambient, single MOSFET dissipating 40 W):**

```
T_junction = T_ambient + (P_diss × Rth_ja)
T_junction = 55 + (40 × 0.97) = 93.8°C
```

This provides 81°C margin to the 175°C SiC junction limit, or 56°C margin to the 150°C design target.

### 4.5 Heatsink Mounting

- MOSFET packages (TO-247-4, HiP247) are screwed directly through the PCB mounting hole into tapped M3 holes in the heatsink base
- Screw: M3 × 8 mm pan-head, zinc-plated steel
- Washer: Belleville spring washer (maintains clamp force under thermal cycling)
- Torque: 0.4–0.5 N·m
- Additional PCB support: 4× M3 standoffs at board corners, 8 mm height, brass (nickel-plated), tapped into heatsink

> [!warning] Torque control is critical
> Under-torquing increases Rth_cs and risks thermal runaway. Over-torquing can crack the ceramic substrate in insulated packages or deform the PCB. Use a calibrated torque screwdriver during assembly.

---

## 5. Fan System

### 5.1 Fan Configuration

The baseline design uses two 80 mm axial fans in a push-pull arrangement at the rear of the enclosure:

| Parameter | Specification |
|-----------|---------------|
| Configuration | 2× 80 mm axial fans, exhaust (pull) |
| Arrangement | Side-by-side, covering full heatsink width |
| Total airflow required | ≥ 55 CFM (at system impedance) |
| System impedance | ~7 mm H₂O at 55 CFM |
| Voltage | 12 VDC (from Aux PSU board) |
| Speed control | PWM, 25 kHz, duty range 20–100% |
| Tachometer output | Open-drain pulse, 2 pulses/revolution |
| Bearing type | Dual ball bearing (rated ≥70,000 hours at 60°C) |

### 5.2 Fan Candidates

| Model | Size | Max CFM | Max Pressure | Noise (max) | Current | MTBF |
|-------|------|---------|-------------|-------------|---------|------|
| Sanyo Denki 9GA0812P4G01 | 80×25 mm | 67.9 CFM | 11.2 mm H₂O | 52 dBA | 0.58 A | 70k hr |
| Delta FFB0812EH | 80×25 mm | 57.2 CFM | 9.1 mm H₂O | 50 dBA | 0.51 A | 70k hr |
| Sunon MF80252V1-1000U-A99 | 80×25 mm | 62.0 CFM | 8.5 mm H₂O | 45 dBA | 0.42 A | 70k hr |
| NMB 3115RL-04W-B86 | 80×25 mm | 55.0 CFM | 7.8 mm H₂O | 43 dBA | 0.65 A | 100k hr |

> [!tip] Fan selection
> The Sanyo Denki 9GA0812P4G01 is the baseline selection due to its high static pressure (11.2 mm H₂O) which provides margin against heatsink fin resistance. At 70% PWM duty the noise target of < 55 dB is met while still delivering > 40 CFM per fan.

### 5.3 Noise Budget

| Condition | Fan Duty | Airflow (total) | Noise |
|-----------|----------|-----------------|-------|
| Light load (< 15 kW, T_amb ≤ 35°C) | 30% | ~25 CFM | < 35 dBA |
| Half load (15 kW, T_amb ≤ 45°C) | 50% | ~40 CFM | < 45 dBA |
| Full load (30 kW, T_amb ≤ 45°C) | 70% | ~55 CFM | < 55 dBA |
| Full load, high ambient (30 kW, T_amb = 55°C) | 100% | ~68 CFM | < 63 dBA |
| Emergency derating | 100% | ~68 CFM | < 63 dBA |

### 5.4 Fan Speed Control Algorithm

The controller board reads heatsink temperature via NTC thermistors (one per power board, bonded to heatsink base) and applies a piecewise-linear fan curve:

```
Heatsink Temp (°C)    Fan PWM Duty (%)
───────────────────   ─────────────────
      ≤ 40                  20  (minimum)
       50                   40
       60                   60
       70                   80
      ≥ 75                 100
      ≥ 90            FAULT → OTP shutdown
```

Fan tachometer feedback is monitored continuously. If either fan reports < 500 RPM while commanded > 30% duty, the controller asserts a fan-fail warning and begins power derating per [[09-Protection and Safety]].

### 5.5 Fan Mounting

- Fans are mounted to an internal bracket (1.2 mm aluminum) using 4× M4 screws with silicone rubber grommets at each mounting point
- Grommets decouple fan vibration from the enclosure, reducing structure-borne noise by ~5 dBA
- Fan bracket is secured to the enclosure rear panel with 4× M3 screws
- Wire routing: fan power/PWM/tach cables routed along the enclosure side wall to the Aux PSU and Controller boards respectively

### 5.6 Dust Filter

- Location: intake side (bottom panel, IP20 configuration)
- Media: polyester mesh, 45 PPI (pores per inch), ~80% open area
- Frame: snap-in plastic frame, tool-free removal for cleaning
- Replacement interval: every 6 months (or as indicated by pressure differential)
- Pressure drop (clean): < 0.5 mm H₂O
- Pressure drop (dirty, replacement threshold): 2.0 mm H₂O

---

## 6. Bus Bar Design

### 6.1 P2 DC Bus Bar (AC-DC → DC-DC)

The P2 bus bar carries the full DC bus current (~35 A at 30 kW, 920 VDC) between the AC-DC board output capacitors and the DC-DC board primary input.

| Parameter | Specification |
|-----------|---------------|
| Type | Laminated bus bar pair (DC_BUS+ / DC_BUS−) |
| Material | Electrolytic copper, C11000, tin-plated (3–5 µm) |
| Conductor thickness | 2.0 mm per layer |
| Conductor width | 25 mm |
| Insulation | Kapton HN polyimide film, 0.2 mm (rated 7 kV/mm) |
| Total stack height | 2.0 + 0.2 + 2.0 = 4.2 mm |
| Length | 65 mm (center-to-center, board gap) |
| DC resistance | < 0.15 mΩ |
| Inductance | ≤ 3 nH (laminated pair, < 5 nH target) |
| Current rating | 40 A continuous (< 20°C rise in still air) |
| Voltage rating | 1000 VDC (working), 2500 VDC (hipot test) |
| Mounting | M4 hex-flange bolts, 2 per end |
| Torque | 1.0–1.2 N·m |

```
CROSS-SECTION (P2 BUS BAR):

    ┌────────────────────────┐
    │  DC_BUS+ (Cu, 2 mm)   │  ← bolts to AC-DC board pad
    ├════════════════════════┤
    │  Kapton (0.2 mm)       │  ← dielectric insulation
    ├════════════════════════┤
    │  DC_BUS− (Cu, 2 mm)   │  ← bolts to AC-DC board pad
    └────────────────────────┘
    ◄──────── 25 mm ────────►
```

> [!warning] Laminated bus bar parasitic inductance
> The low inductance of the laminated bus bar is critical to limiting voltage overshoot during MOSFET switching on the DC-DC primary side. If the bus bar inductance exceeds 5 nH, the voltage spike at turn-off (with 35 A, 50 ns di/dt) reaches V_spike = L × di/dt ≈ 5 nH × 700 A/µs = 3.5 V — manageable, but larger inductance values compound with PCB trace inductance and can cause ringing above the 1200 V device rating.

### 6.2 Output Bus Bar (DC-DC → Rear Panel)

| Parameter | Specification |
|-----------|---------------|
| Rating | 100 A continuous |
| Material | Copper, C11000, tin-plated |
| Thickness | 3.0 mm |
| Width | 30 mm |
| Length | ~100 mm (DC-DC board edge to rear panel studs) |
| DC resistance | < 0.10 mΩ |
| Current density | < 3.3 A/mm² (< 25°C rise) |
| Insulation | Kapton sleeve or heat-shrink, rated 1000 VDC |
| Mounting (board side) | M5 bolts to PCB bus bar pads, 1.5 N·m |
| Mounting (panel side) | M8 studs through rear panel, insulating bushings |

Two bars are required: DC_OUT+ and DC_OUT−. A third PE bar or braid bonds the DC output ground reference to the enclosure PE stud.

### 6.3 AC Input Interconnect

| Parameter | Specification |
|-----------|---------------|
| Type | Individual wires or flat bus bars, 3 phases + neutral + PE |
| Wire gauge (if wired) | 10 AWG (5.26 mm²) minimum per phase, silicone insulated, rated 600 V |
| Bus bar option | 1.5 mm copper, 15 mm wide per phase, insulated |
| Length | ~200 mm (front panel connector to AC-DC board edge) |
| Termination (panel side) | Ring terminals or direct bolted to input connector studs |
| Termination (board side) | Soldered or bolted to PCB input pads |

---

## 7. Connector Specifications

### 7.1 External Connectors

| ID | Connector | Type | Rating | Location | Mating Cycles |
|----|-----------|------|--------|----------|---------------|
| J1 | AC Input (L1/L2/L3/N/PE) | Phoenix COMBICON GMSTBA 2.5/5-ST or M6 studs | 530 VAC, 60 A | Front panel | 100+ (studs) |
| J2 | DC Output (+) | M8 stud, flanged, insulated bushing | 1000 VDC, 100 A | Rear panel | 500 (blind-mate option) |
| J3 | DC Output (−) | M8 stud, flanged, insulated bushing | 1000 VDC, 100 A | Rear panel | 500 |
| J4 | PE Output | M6 stud, direct bonded to enclosure | — | Rear panel | — |
| J5 | CAN Bus | DB-9 male (CANopen pinout) or M12-A 5-pin | 1 Mbps, 5 VDC | Front panel | 500 |
| J6 | Ethernet (OCPP) | RJ45, shielded, Cat5e | 100 Mbps | Front panel | 750 |

### 7.2 Internal Connectors (Board-to-Board)

| ID | Connector | Mating Pair | Rating | From → To |
|----|-----------|-------------|--------|-----------|
| P2 | Bus bar (bolted) | M4 bolted pads | 920 VDC, 40 A | AC-DC → DC-DC |
| P4 | Molex Micro-Fit 3.0, 8-pin (43025-0800) | 43020-0801 | 18 VDC, 0.5 A/pin | Aux PSU → AC-DC & DC-DC gate drives |
| P5 | Molex Micro-Fit 3.0, 4-pin (43025-0400) | 43020-0401 | 5 VDC, 1 A/pin | Aux PSU → Controller board |
| S1 | Molex Pico-Lock 12-pin (504050-1200) | 504051-1201 | 3.3 V signal, 50 mA | Controller → AC-DC (PFC PWM, ADC, fault) |
| S2 | Molex Pico-Lock 10-pin (504050-1000) | 504051-1001 | 3.3 V signal, 50 mA | Controller → DC-DC (LLC PWM, ADC, fault) |
| F1 | JST PH 2-pin (B2B-PH-K-S) | PHR-2 | 12 VDC, 0.6 A | Aux PSU → Fan 1 power |
| F2 | JST PH 2-pin (B2B-PH-K-S) | PHR-2 | 12 VDC, 0.6 A | Aux PSU → Fan 2 power |
| F3 | JST PH 4-pin (B4B-PH-K-S) | PHR-4 | 5 V signal | Controller → Fan PWM & tach (2× fans) |
| T1 | JST PH 2-pin | PHR-2 | NTC signal | Heatsink NTC 1 → Controller ADC |
| T2 | JST PH 2-pin | PHR-2 | NTC signal | Heatsink NTC 2 → Controller ADC |

### 7.3 Connector Placement Rules

- High-voltage connectors (P2, J1, J2, J3): minimum 10 mm creepage to enclosure and to any signal connector
- Signal harnesses (S1, S2, F3, T1, T2): routed in a dedicated channel along the enclosure side wall, separated ≥ 15 mm from any power conductor
- Power harnesses (P4, P5): routed between Aux PSU and power boards, twisted pair where possible to reduce EMI
- All connectors must be keyed or polarized to prevent mis-mating
- Locking/latching connectors required for all harnesses subject to vibration (Micro-Fit 3.0 and Pico-Lock both have latches)

---

## 8. Board Mounting and Standoffs

### 8.1 Mounting Summary

| Board | Mount Surface | Standoff Height | Standoff Type | Fastener | Count |
|-------|--------------|-----------------|---------------|----------|-------|
| AC-DC | Heatsink | 0 mm (direct via MOSFET screws) + 8 mm corner standoffs | Brass, M3, nickel-plated | M3 × 8 pan-head + Belleville | 6 MOSFET + 4 corner |
| DC-DC | Heatsink | 0 mm (direct via MOSFET screws) + 8 mm corner standoffs | Brass, M3, nickel-plated | M3 × 8 pan-head + Belleville | 6 MOSFET + 4 corner |
| Controller | Enclosure floor | 8 mm | Nylon, M3 (isolated from chassis ground) | M3 × 6 nylon screw | 4 corner |
| Aux PSU | Enclosure floor | 6 mm | Brass, M3, nickel-plated | M3 × 6 pan-head | 4 corner |

> [!note] Controller board isolation
> The Controller board uses nylon standoffs to prevent ground loops between the digital ground plane and the chassis/power ground. A single-point chassis connection is made via a dedicated grounding pad on the Controller PCB, bonded to the enclosure with a short braid.

### 8.2 Standoff Details

**Brass standoffs (power boards and Aux PSU):**

| Dimension | Value |
|-----------|-------|
| Thread | M3 × 0.5, female-female |
| Length | 6 mm (Aux PSU) or 8 mm (power boards) |
| Material | CDA 360 brass, nickel-plated |
| Hex width | 5.5 mm across flats |
| Mounting to heatsink/chassis | M3 × 5 mm flat-head screw from below |

**Nylon standoffs (Controller board):**

| Dimension | Value |
|-----------|-------|
| Thread | M3 × 0.5, female-female |
| Length | 8 mm |
| Material | Nylon 6/6, UL94 V-2 rated |
| Hex width | 5.5 mm across flats |
| Temperature rating | −40°C to +85°C |

### 8.3 Vibration and Shock Requirements

Per IEC 60068-2-6 and IEC 60068-2-27 (referenced by IEC 61851-23 for EV charging equipment):

| Test | Specification |
|------|---------------|
| Sinusoidal vibration | 10–150 Hz, 2g peak, 2 hours per axis (3 axes) |
| Mechanical shock | 30g, 11 ms half-sine, 3 shocks per direction (18 total) |
| Random vibration (transport) | 5–200 Hz, 1.5 grms, 30 min per axis |

Design features for vibration resistance:

- All screws use spring washers (Belleville for MOSFET screws, split lock for standoffs) or thread-locking compound (Loctite 243, medium strength)
- PCB mass is supported at ≥ 4 points, limiting maximum unsupported span to < 80 mm
- Heavy components (inductors, transformers) have supplemental adhesive bonding (Dow Corning 3145 RTV) to PCB in addition to solder joints
- Fan mounting uses silicone rubber grommets to decouple vibration
- Wire harnesses have strain relief at both connector ends and tie-down points every 50 mm along the routing path

---

## 9. Thermal Derating and Airflow Validation

### 9.1 CFD Simulation Targets

| Parameter | Target | Limit |
|-----------|--------|-------|
| Max heatsink surface temp (at hottest MOSFET) | < 85°C at 55°C ambient, full load | 95°C absolute max |
| Max MOSFET junction temp | < 150°C | 175°C (device rating) |
| Max transformer hotspot | < 130°C | 155°C (Class F insulation) |
| Max DC bus capacitor temp | < 85°C | 105°C (rated life) |
| Airflow velocity over fins | ≥ 2.0 m/s | 1.5 m/s minimum |
| Total enclosure pressure drop | < 10 mm H₂O | 12 mm H₂O (fan stall margin) |
| Air temperature rise (inlet to outlet) | < 25°C | 30°C |

### 9.2 Thermal Derating Table

| Ambient Temp (°C) | Max Output Power (kW) | % of Rated | Fan Speed (%) | Heatsink Temp (°C) | T_j Estimate (°C) |
|---|---|---|---|---|---|
| ≤ 35 | 30.0 | 100% | 30–50 | ≤ 60 | ≤ 100 |
| 40 | 30.0 | 100% | 50–60 | ≤ 70 | ≤ 110 |
| 45 | 30.0 | 100% | 60–80 | ≤ 80 | ≤ 120 |
| 50 | 25.0 | 83% | 80–90 | ≤ 82 | ≤ 130 |
| 55 | 20.0 | 67% | 100 | ≤ 85 | ≤ 140 |
| 60 | 15.0 | 50% | 100 | ≤ 85 | ≤ 140 |
| 65 | 0 (shutdown) | 0% | 100 → off | — | — |

> [!tip] Derating is applied gradually
> The controller implements a continuous derating curve (not step changes) by reducing the maximum current command proportionally as heatsink temperature rises above the 75°C threshold. This avoids abrupt power transients during charging sessions. See [[09-Protection and Safety]] for OTP threshold definitions.

### 9.3 Airflow Resistance Estimate

```
Component              Pressure Drop (mm H₂O)
─────────────────────  ──────────────────────
Dust filter (clean)           0.5
Intake grille                 0.3
Heatsink fins (50 fins,       5.5
  35 mm tall, 3.5 mm pitch,
  455 mm long, at 2.5 m/s)
PCB obstructions              0.5
Exhaust grille                0.3
──────────────────────────────────
Total system impedance        7.1 mm H₂O
```

At 7.1 mm H₂O, the Sanyo Denki 9GA0812P4G01 (2× fans in parallel) delivers approximately 55 CFM, which is sufficient for the ~1 kW dissipation budget.

---

## 10. EMC Enclosure Considerations

### 10.1 Shielding Effectiveness Targets

| Frequency Range | Target SE | Method |
|----------------|-----------|--------|
| 150 kHz – 30 MHz (conducted) | N/A (handled by EMI filter) | — |
| 30 MHz – 200 MHz | ≥ 40 dB | Panel joint continuity, gaskets |
| 200 MHz – 1 GHz | ≥ 30 dB | Slot control, waveguide vents |
| > 1 GHz | ≥ 20 dB | Aperture size control |

### 10.2 Panel Joint Design

- All panel edges have continuous conductive contact via one of:
  - Finger stock gasket (BeCu, tin-plated) on removable covers
  - Conductive EMI gasket (Chomerics CHO-SEAL 1285) on permanent joints
  - Direct metal-to-metal contact with chromate-coated mating surfaces (screw spacing ≤ 30 mm)
- Maximum slot length at any panel joint: < 15 mm (λ/4 at 5 GHz)
- Screw spacing along panel joints: ≤ 30 mm for panels, ≤ 50 mm for non-critical covers

### 10.3 Cable Entry EMC

| Entry Point | EMC Treatment |
|-------------|---------------|
| AC input (J1) | Shielded cable, shield terminated 360° at panel bulkhead via EMC cable gland |
| DC output (J2/J3) | Studs with insulated bushings; cable shield bonded to PE stud at panel exit |
| CAN bus (J5) | Shielded DB-9 with conductive backshell bonded to panel |
| Ethernet (J6) | Shielded RJ45 jack with integrated common-mode choke, shell bonded to panel |
| Fan wires (internal) | Ferrite bead on each fan wire pair, placed within 20 mm of board connector |

### 10.4 Ventilation EMC

For IP20 ventilation slots to maintain shielding effectiveness:

- Slot geometry: 3 mm wide × 30 mm long (waveguide below cutoff above ~5 GHz)
- Slots oriented perpendicular to longest enclosure dimension
- For frequencies below 1 GHz: slot length must be < 75 mm (λ/4 at 1 GHz); the 30 mm slots satisfy this
- Optional: honeycomb EMI filter panels (cell size 3 mm, depth 10 mm) for applications requiring > 40 dB SE at high frequencies

### 10.5 Internal Partitioning

An optional internal EMC shield (0.5 mm aluminum sheet) can be installed between the power section (AC-DC and DC-DC boards) and the control section (Controller and Aux PSU boards):

- Shield is bonded to enclosure at ≥ 4 points
- Pass-through holes for signal harnesses (S1, S2) use ferrite-lined grommets
- Pass-through holes for power harnesses (P4, P5) use feedthrough capacitors or ferrite beads

---

## 11. Assembly Sequence

### 11.1 Assembly Procedure

| Step | Action | Fastener/Tool | Torque |
|------|--------|--------------|--------|
| 1 | Install heatsink into enclosure baseplate | 6× M4 × 10 flat-head, from below | 1.2 N·m |
| 2 | Apply TIM pads to heatsink at MOSFET locations | Pre-cut GP3000S pads, peel-and-place | — |
| 3 | Install AC-DC board corner standoffs into heatsink | 4× M3 brass standoffs, threaded insert | Hand-tight |
| 4 | Mount AC-DC board onto heatsink | 6× M3 × 8 MOSFET screws + Belleville washers; 4× M3 × 6 at corner standoffs | 0.45 N·m |
| 5 | Apply TIM pads for DC-DC board MOSFETs | Pre-cut GP3000S pads | — |
| 6 | Install DC-DC board corner standoffs | 4× M3 brass standoffs | Hand-tight |
| 7 | Mount DC-DC board onto heatsink | Same as step 4 | 0.45 N·m |
| 8 | Install P2 DC bus bar | 4× M4 hex-flange bolts (2 per board) | 1.0 N·m |
| 9 | Install Aux PSU standoffs on enclosure floor | 4× M3 brass standoffs, 6 mm | Hand-tight |
| 10 | Mount Aux PSU board | 4× M3 × 6 pan-head screws | 0.3 N·m |
| 11 | Install Controller board standoffs | 4× M3 nylon standoffs, 8 mm | Hand-tight |
| 12 | Mount Controller board | 4× M3 nylon screws | 0.2 N·m |
| 13 | Connect S1 harness (Controller → AC-DC) | Pico-Lock, click-to-lock | — |
| 14 | Connect S2 harness (Controller → DC-DC) | Pico-Lock, click-to-lock | — |
| 15 | Connect P4 harness (Aux PSU → gate drives) | Micro-Fit 3.0, click-to-lock | — |
| 16 | Connect P5 harness (Aux PSU → Controller) | Micro-Fit 3.0, click-to-lock | — |
| 17 | Install output bus bars (DC-DC → rear panel) | 2× M5 bolts (board side), M8 nuts (panel side) | 1.5 N·m / 3.0 N·m |
| 18 | Install fan bracket with 2× fans | 8× M4 screws with rubber grommets | 0.5 N·m |
| 19 | Connect fan power (F1, F2) and control (F3) harnesses | JST PH connectors | — |
| 20 | Connect NTC harnesses (T1, T2) | JST PH connectors | — |
| 21 | Route AC input cables from front panel to AC-DC board | Ring terminals, M6 stud nuts | 2.0 N·m |
| 22 | Install dust filter at intake | Snap-in frame | — |
| 23 | Close top cover | 4× M3 captive screws | 0.3 N·m |
| 24 | Final inspection: verify all panel screws torqued, harnesses seated, no loose hardware | — | — |

### 11.2 Disassembly for Board Replacement

To replace a single power board (e.g., AC-DC):

1. Remove top cover (4× captive screws)
2. Disconnect signal harness S1 (Pico-Lock release tab)
3. Disconnect power harness P4 (Micro-Fit 3.0 release tab)
4. Remove P2 bus bar (4× M4 bolts — only the 2 bolts on the target board side if using Option B heatsink)
5. Remove 6× MOSFET screws and 4× corner standoff screws
6. Lift board vertically off heatsink
7. Clean and replace TIM pads on heatsink
8. Install replacement board (reverse of above)

Estimated field replacement time: < 15 minutes per board.

---

## 12. Cross-References

- [[00-Board Partitioning]] — Board dimensions, layer counts, connector pinout definitions, harness specifications
- [[04-Thermal Budget]] — Loss allocation per board, thermal derating curves, CFD simulation parameters
- [[07-PCB-Layout/__init|07-PCB Layout]] — PCB-level thermal and mechanical constraints, keepout zones
- [[07-PCB-Layout/AC-DC/04-Thermal Layout|AC-DC Thermal Layout]] — MOSFET pad placement, heatsink mounting hole pattern, TIM application area
- [[07-PCB-Layout/DC-DC/04-Thermal Layout|DC-DC Thermal Layout]] — Transformer thermal interface, secondary rectifier heatsinking
- [[09-Protection and Safety]] — Fan failure detection logic, OTP thresholds, fault response matrix
- [[08-Power-On Sequence and Inrush Management]] — Startup sequence, pre-charge contactor mechanical placement
- [[SiC Device Thermal Parameters]] — Package thermal resistance data (Rth_jc, Rth_jb) for all selected SiC MOSFETs
