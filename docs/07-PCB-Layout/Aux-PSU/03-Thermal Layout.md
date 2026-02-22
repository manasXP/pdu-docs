---
tags: [pdu, pcb-layout, aux-psu, thermal, natural-convection, derating]
created: 2026-02-22
status: draft
---

# 03 — Thermal Layout

## 1. Purpose

This document specifies the thermal design aspects of the Aux PSU board. Unlike the main power boards (AC-DC and DC-DC) which dissipate hundreds of watts and require dedicated heatsinks with forced-air cooling, the Aux PSU dissipates only **5–10 W total**. This modest dissipation level allows the board to rely on **natural convection and PCB conduction** to the enclosure chassis, supplemented by incidental airflow from the main system fan.

Despite the low total dissipation, individual hot spots — particularly the primary MOSFET and secondary rectifier diodes — require careful thermal layout to stay within safe operating limits at the 55°C ambient maximum.

## 2. Thermal Budget Overview

### 2.1 Power Dissipation Breakdown

| Component | Loss Mechanism | Estimated Loss (W) | Worst Case (W) | Notes |
|-----------|---------------|-------------------|-----------------|-------|
| Primary MOSFET (Q1) | Conduction + switching | 1.5 | 2.5 | Rdson losses + turn-off loss at 65–130 kHz |
| Flyback transformer (T1) | Core loss + copper loss | 1.0 | 2.0 | Ferrite core EE25, ~100 mW/cm³ at 65 kHz |
| Clamp resistor (R_clamp) | Leakage energy dissipation | 0.05 | 0.2 | Negligible at normal operation; higher during transients |
| Rectifier diode D_A (+18 V AC-DC) | Vf x Iavg | 0.25 | 0.4 | Schottky Vf ~0.5 V at 0.5 A |
| Rectifier diode D_B (+18 V DC-DC) | Vf x Iavg | 0.25 | 0.4 | Same as D_A |
| Rectifier diode D_C (+12 V / +5 V) | Vf x Iavg | 0.5 | 0.8 | Higher current: 0.5 V x (2 A + 1 A) |
| −5 V rectifier diodes (x2) | Vf x Iavg | 0.2 | 0.3 | 0.5 V x 0.2 A each |
| +5 V LDO (from 12 V or dedicated winding) | Linear dropout loss | 0.5 | 1.0 | (Vin − Vout) x Iout worst case; see [[04-Output Filtering and Regulation]] |
| +3.3 V LDO (from 5 V) | Linear dropout loss | 0.85 | 1.0 | (5 V − 3.3 V) x 0.5 A = 0.85 W |
| PWM controller IC (U1) | Quiescent + gate drive | 0.15 | 0.3 | VCC x ICC + Qg x f x VCC |
| PCB trace I²R losses | Resistive heating | 0.1 | 0.2 | Low current, negligible |
| **Total** | | **5.35** | **9.1** | |

> [!warning] LDO Dissipation Dominates
> The +3.3 V LDO (fed from +5 V) and the +5 V LDO (if fed from +12 V) together account for 1.35–2.0 W — approximately 25% of total board dissipation. If the +5 V rail is derived from the +12 V winding through an LDO, the dropout loss is $(12 - 5) \times 1.0 = 7.0$ W, which is unacceptable. The +5 V rail **must** have its own dedicated winding or use a small buck regulator from the +12 V rail. See [[04-Output Filtering and Regulation]] for alternatives.

### 2.2 Temperature Targets

| Component | Package | Max Junction/Case Temp | Target Operating Temp | Max Dissipation |
|-----------|---------|----------------------|---------------------|-----------------|
| Primary MOSFET Q1 | TO-263 (D2PAK) | 150–175°C | ≤120°C | 2.5 W |
| Flyback transformer T1 | EE25 (through-hole) | 130°C (core) | ≤105°C | 2.0 W |
| Rectifier diodes D_A/B/C | SMA / SMB | 150°C | ≤115°C | 0.8 W each |
| +3.3 V LDO | SOT-223 or DPAK | 150°C | ≤110°C | 1.0 W |
| +5 V regulator | SOT-223 or SOIC-8 | 150°C | ≤110°C | 1.0 W |
| PWM controller U1 | SOIC-8 | 150°C | ≤100°C | 0.3 W |
| Electrolytic output caps | Radial | 105°C (case) | ≤85°C | ESR loss only |

## 3. Cooling Strategy — Natural Convection + Conduction

### 3.1 No Dedicated Forced Air

The Aux PSU board is positioned in the enclosure near the main system fan but does **not** have dedicated forced-air cooling. The thermal design relies on:

1. **PCB copper spreading** — Large copper pours on L1 and L4 conduct heat from point sources to a wider area
2. **Thermal vias** — Transfer heat from L1 to L4 for double-sided dissipation
3. **Conduction to chassis** — Board mounting screws and standoffs provide a thermal path to the metal enclosure
4. **Incidental airflow** — The main system fan (exhausting from the power boards) creates some air movement around the Aux PSU
5. **Radiation** — Black solder mask and copper surfaces radiate heat to the enclosure walls

### 3.2 Thermal Resistance Estimates (Natural Convection, 55°C Ambient)

| Cooling Path | Estimated Rth (°C/W) | Notes |
|-------------|---------------------|-------|
| Junction to case (Rth_jc) — TO-263 MOSFET | 1.0–2.0 | Package datasheet value |
| Case to PCB (Rth_cp) — exposed pad | 1.0–3.0 | Depends on thermal via array |
| PCB to ambient (Rth_pa) — natural convection | 20–40 per cm² | For 1 oz copper, vertical board |
| PCB to chassis (Rth_pc) — via standoffs | 10–20 per standoff | M3 standoff, 5 mm length |
| Junction to ambient (Rth_ja) — total for TO-263 with thermal vias | 30–50 | With 10 cm² copper pour + 9 thermal vias |

### 3.3 Temperature Rise Calculations

#### Primary MOSFET (Q1) — 2.5 W Worst Case

With a 10 cm² copper pour and 3x3 thermal via array:

$$T_j = T_{amb} + P_{diss} \times R_{th\_ja} = 55 + 2.5 \times 40 = 155°C$$

This exceeds the 120°C target. Mitigation options:

| Option | Effect on Rth_ja | Notes |
|--------|-----------------|-------|
| Increase copper pour to 20 cm² | Reduces to ~30°C/W | Requires ~25% of board area |
| Add 4x4 thermal via array (16 vias) | Reduces to ~25°C/W | L4 bottom-side heat dissipation |
| Mount thermal pad to chassis standoff | Reduces to ~15°C/W | **Recommended** — direct chassis conduction |
| Use TO-220 package with small clip-on heatsink | Reduces to ~20°C/W | Alternative if chassis contact not feasible |

> [!tip] Chassis Conduction Path
> The most effective cooling strategy for Q1 is to place it near a board mounting standoff and create a thermal copper pour that extends from the Q1 thermal pad to the standoff mounting hole. The standoff (metal M3, >5 mm diameter) conducts heat directly into the aluminum chassis. With this approach, the effective Rth_ja can be reduced to 15–20°C/W, giving: $T_j = 55 + 2.5 \times 18 = 100°C$ — well within target.

#### +3.3 V LDO — 1.0 W Worst Case

With SOT-223 package (Rth_ja ~90°C/W from datasheet, no copper pour):

$$T_j = 55 + 1.0 \times 90 = 145°C \quad \text{(exceeds 110°C target)}$$

With 4 cm² copper pour and 2x2 thermal via array (Rth_ja ~50°C/W):

$$T_j = 55 + 1.0 \times 50 = 105°C \quad \text{(meets target)}$$

> [!warning] LDO Thermal Pads Are Mandatory
> Both the +5 V and +3.3 V LDOs **must** have dedicated copper pour thermal pads on L1, connected through thermal vias to L4 bottom-side pours. Without these pours, the SOT-223 packages will overheat at 55°C ambient. Minimum copper pour: 4 cm² per LDO.

## 4. Thermal Via Arrays

### 4.1 Under Primary MOSFET (Q1) — TO-263

| Parameter | Value |
|-----------|-------|
| Via drill diameter | 0.3 mm |
| Via pad diameter | 0.6 mm |
| Via pitch | 1.27 mm (50 mil) |
| Array size | 4x4 (16 vias) under exposed pad |
| Via fill | Tented (prototype) or plugged (production) |
| Thermal relief | **None — direct connect on all layers** |
| L1 copper pour | 20 cm² minimum, primary GND net |
| L4 copper pour | 20 cm² minimum, matching L1 area |

```
    Q1 TO-263 thermal pad with via array (L1):

    ┌──────────────────────────────────────┐
    │          20 cm² copper pour           │
    │     (PRI_GND net, 2 oz copper)       │
    │                                       │
    │     ┌────────────────────┐           │
    │     │  ○ ○ ○ ○           │           │
    │     │  ○ ○ ○ ○  TO-263   │           │
    │     │  ○ ○ ○ ○  exposed  │           │
    │     │  ○ ○ ○ ○  pad      │           │
    │     │   D    G    S   S  │ ← pins    │
    │     └────────────────────┘           │
    │                                       │
    └──────────────────────────────────────┘
    ○ = thermal via (0.3mm drill, 1.27mm pitch)
```

### 4.2 Under Secondary Rectifier Diodes

For SMA/SMB package rectifiers dissipating 0.4–0.8 W each:

| Parameter | Value |
|-----------|-------|
| Via array | 2x2 (4 vias) under cathode pad |
| Via drill | 0.3 mm |
| Pitch | 1.0 mm |
| L1 copper pour | 2–4 cm² per diode |
| L4 copper pour | Matching area on bottom |

### 4.3 Under LDO Regulators (SOT-223)

| Parameter | Value |
|-----------|-------|
| Via array | 2x3 (6 vias) under tab pad |
| Via drill | 0.3 mm |
| Pitch | 1.0 mm |
| L1 copper pour | 4 cm² minimum |
| L4 copper pour | 4 cm² minimum, matching |

## 5. Copper Pour Heat Spreading

### 5.1 Primary Side Thermal Pours

| Pour | Net | Area | Layer(s) | Connected Components |
|------|-----|------|----------|---------------------|
| Q1 thermal pad | PRI_GND | 20 cm² | L1 + L4 | Q1 exposed pad, R_sense return |
| Input cap return | PRI_GND | 5 cm² | L1 | C_in negative terminal |
| Clamp resistor | CLAMP | 2 cm² | L1 | R_clamp (heat spreading for 1 W) |

### 5.2 Secondary Side Thermal Pours

| Pour | Net | Area | Layer(s) | Connected Components |
|------|-----|------|----------|---------------------|
| +18 V rectifier A | VDRV_AC+ | 3 cm² | L1 + L4 | D_A cathode, L_A input |
| +18 V rectifier B | VDRV_DC+ | 3 cm² | L1 + L4 | D_B cathode, L_B input |
| +12 V rectifier | V12V | 4 cm² | L1 + L4 | D_C cathode, L_C input |
| +3.3 V LDO | V3V3 or SEC_GND | 4 cm² | L1 + L4 | LDO tab (check datasheet for tab net) |
| +5 V regulator | V5V or SEC_GND | 4 cm² | L1 + L4 | Regulator thermal pad |

> [!tip] Check LDO Tab Connection
> Some LDOs connect the tab (exposed pad) to the output pin, others to the ground pin. Verify the specific LDO datasheet before assigning the thermal pour net. Connecting the tab to the wrong net will short the output.

## 6. Operating Temperature Analysis at 55°C Ambient

### 6.1 Thermal Summary Table

| Component | Dissipation (W) | Rth_ja (°C/W) | Tj at 55°C (°C) | Target (°C) | Margin (°C) | Status |
|-----------|-----------------|---------------|-----------------|-------------|-------------|--------|
| Q1 (with chassis path) | 2.5 | 18 | 100 | 120 | +20 | OK |
| Q1 (no chassis path) | 2.5 | 40 | 155 | 120 | −35 | FAIL |
| T1 transformer | 2.0 | 25 (core surface to air) | 105 | 105 | 0 | MARGINAL |
| D_A rectifier | 0.4 | 60 | 79 | 115 | +36 | OK |
| D_B rectifier | 0.4 | 60 | 79 | 115 | +36 | OK |
| D_C rectifier | 0.8 | 50 | 95 | 115 | +20 | OK |
| +3.3 V LDO | 1.0 | 50 | 105 | 110 | +5 | MARGINAL |
| +5 V regulator | 1.0 | 50 | 105 | 110 | +5 | MARGINAL |
| U1 PWM controller | 0.3 | 120 | 91 | 100 | +9 | OK |

> [!warning] Chassis Thermal Path is Mandatory for Q1
> Without direct chassis conduction through a mounting standoff, the primary MOSFET Q1 exceeds its target temperature by 35°C at worst-case ambient. The layout **must** include a copper thermal path from Q1 to a board mounting standoff. This is a firm design constraint, not optional.

## 7. Component Derating Guidelines

### 7.1 Derating at 55°C Ambient

| Component Type | Parameter | Derated Value at 55°C | Derating Rule |
|---------------|-----------|----------------------|---------------|
| Electrolytic capacitor | Ripple current | 80% of 25°C rating | Linear derating above 45°C |
| Ceramic capacitor | Voltage | 80% of rated voltage | X7R loses capacitance at high temp |
| MOSFET Q1 | Rdson | 1.5x of 25°C value | Positive tempco; increases losses |
| Schottky diode | Reverse leakage | 10x of 25°C value | Doubles per 10°C; verify at max Vr |
| LDO regulator | Output current | Per SOA curve at Tj | Check dropout at elevated temperature |
| Transformer core | Saturation flux | 90% of 25°C value | Ferrite Bsat decreases ~0.3%/°C |
| Resistors (1%) | Tolerance | Within spec if Tj < 125°C | Standard metal film |

### 7.2 Derating Table for Key Components

| Component | Rated Value | Derated Value (55°C) | Safety Margin |
|-----------|------------|---------------------|---------------|
| C_in (1 uF 1000 V X7R) | 1000 V | Use at ≤920 V (92%) | 8% |
| C_out electrolytic (470 uF 25 V) | 1.5 A ripple | 1.2 A ripple (80%) | Verify against actual ripple |
| Q1 (1200 V SiC, Rdson = 1.0 ohm at 25°C) | 1.0 ohm | 1.5 ohm at 150°C Tj | Recalculate conduction loss |
| LDO (1 A, SOT-223) | 1 A at 25°C | Check SOA at Tj = 105°C | May need to limit to 0.8 A |

## 8. Thermal Design Verification

### Pre-Layout Checks

- [ ] Q1 placed within 15 mm of a board mounting standoff
- [ ] Copper pour areas allocated per component thermal requirements
- [ ] Thermal via arrays sized per this document
- [ ] LDO input source selected to minimize dropout loss (see [[04-Output Filtering and Regulation]])

### Post-Layout Checks

- [ ] All thermal via arrays placed and connected (no thermal relief on power pads)
- [ ] Copper pours meet minimum area requirements per thermal budget
- [ ] No narrow copper necks in thermal paths (minimum 3 mm width for thermal pours)
- [ ] Board mounting standoff holes have thermal copper connection to nearest hot component
- [ ] No high-dissipation components placed adjacent to electrolytic capacitors

## 9. Cross-References

- [[__init]] — Board overview, power budget
- [[07-PCB-Layout/Aux-PSU/01-Stack-Up and Layer Assignment]] — Copper weights, layer assignments
- [[02-Isolated Converter Layout]] — Primary MOSFET and rectifier placement
- [[04-Output Filtering and Regulation]] — LDO selection and dropout losses
- [[05-Safety and Isolation]] — Conformal coating considerations for thermal management
- [[04-Thermal Budget]] — System-level thermal allocation

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
