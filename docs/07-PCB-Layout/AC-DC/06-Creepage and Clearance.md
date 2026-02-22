---
tags: [pdu, pcb-layout, vienna-pfc, creepage, clearance, safety, iec-62368, ipc-2221]
created: 2026-02-22
status: draft
---

# 06 — Creepage and Clearance

## Purpose

This document defines the creepage and clearance requirements for the Vienna Rectifier PFC board, based on the applicable safety standards (IEC 62368-1, IEC 61851-23) and the board's operating voltages. Creepage and clearance violations are safety-critical defects that can lead to flashover, tracking, or dielectric breakdown — potentially causing fire or electric shock.

The AC-DC board operates at the highest voltages in the PDU system:
- **AC input:** Up to 530 VAC RMS (750 Vpk line-to-PE)
- **DC bus:** Up to 920 VDC
- **Gate drive:** ±20V (functional isolation from switching node)

These voltages, combined with pollution degree 2 (PD2) and material group IIIb (standard FR-4), determine the minimum creepage and clearance distances for every conductor pair on the board.

## Applicable Standards

| Standard | Scope | Application |
|----------|-------|-------------|
| IEC 62368-1 | Audio/video, IT, and communication equipment safety | Primary safety standard for the PDU |
| IEC 61851-23 | EV charging — DC charging stations | Supplementary requirements for EV charger |
| IPC-2221B | Generic standard on printed board design | PCB internal clearances (between layers) |
| UL 2202 | EV charging equipment (US) | Supplementary for UL listing |

### Environmental Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Pollution degree (PD) | 2 | Indoor equipment, no conductive pollution expected |
| Material group | IIIb | Standard FR-4 (CTI 100–174V) |
| Altitude | ≤2000 m | Standard — no altitude derating required |
| Overvoltage category | III (AC input), II (DC bus) | AC mains connection = OVC III |
| Insulation type | Reinforced (AC→PE, DC→PE) | Single-fault safety required |

> [!warning] Material Group Matters
> FR-4 is classified as material group IIIb (CTI 100–174V), which requires the **largest creepage distances** of any material group. Using a higher-CTI material (e.g., polyimide, CTI >600V, material group I) would significantly reduce creepage requirements. However, FR-4 is used for cost and availability reasons, so the larger creepage distances must be accommodated in the layout.

## Voltage Pairs and Insulation Requirements

### Identification of Voltage Pairs

Every pair of conductors on the board that can have a voltage difference must be classified:

| Pair | Working Voltage | Peak/Transient Voltage | Insulation Type | Notes |
|------|----------------|----------------------|-----------------|-------|
| AC input phase → PE | 530 VAC RMS | 750 Vpk + surge | Reinforced | User-accessible PE; single-fault safety |
| AC input phase → phase | 530 × √3 = 918 VAC | 1300 Vpk | Basic | Same circuit, operational insulation |
| DC bus (+) → PE | 920 VDC | 920 V + transient | Reinforced | Bus connects to EV via cable |
| DC bus (+) → DC bus (−) | 920 VDC | 920 V + ripple | Functional | Same circuit |
| DC bus → AC input | 920 VDC | 920 V + surge | Basic | Separated by boost inductor |
| Gate drive HV side → LV control | 920 VDC (worst case) | Per STGAP2SiC rating | Reinforced | Isolation across gate driver |
| Gate drive → MOSFET (functional) | 25 V (VDRV + VNEG) | 25 V | Functional | Same floating circuit |
| LV control (5V/3.3V) → PE | 5 V | Negligible | Functional | SELV/PELV circuit |

## Creepage and Clearance Requirements

### AC Input to PE (Reinforced Insulation)

| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Working voltage | 530 VAC RMS | Maximum AC input per [[__init]] |
| Peak working voltage | 750 V (530 × √2) | |
| Pollution degree | PD2 | |
| Material group | IIIb | FR-4, CTI 100–174V |
| Insulation type | Reinforced | Required for accessible PE |
| **Clearance (IEC 62368-1, Table 21)** | **6.4 mm** | Reinforced, PD2, 750 Vpk |
| **Creepage (IEC 62368-1, Table 22)** | **10 mm** | Reinforced, PD2, IIIb, 530 VAC |

> [!tip] Creepage vs. Clearance
> - **Clearance** is the shortest distance through air between two conductors. It protects against voltage breakdown through the air gap (flashover).
> - **Creepage** is the shortest distance along the surface of the insulating material between two conductors. It protects against tracking (carbonization of the surface due to pollution and moisture).
>
> On a PCB, creepage is typically the controlling dimension because the surface path is longer than the air path only when PCB slots or raised features are used. Without slots, creepage = clearance on a flat PCB surface.

### DC Bus to PE (Reinforced Insulation)

| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Working voltage | 920 VDC | Maximum DC bus per [[__init]] |
| Peak working voltage | 920 V (DC = peak) | |
| Pollution degree | PD2 | |
| Material group | IIIb | FR-4 |
| Insulation type | Reinforced | Required for accessible PE |
| **Clearance (IEC 62368-1, Table 21)** | **8 mm** | Reinforced, PD2, 920 Vpk |
| **Creepage (IEC 62368-1, Table 22)** | **14 mm** | Reinforced, PD2, IIIb, 920 VDC |

### Gate Drive Isolation (Reinforced)

The STGAP2SiC gate drivers provide reinforced isolation between the primary (control) side and the secondary (high-voltage) side.

| Parameter | Value | Notes |
|-----------|-------|-------|
| Working voltage across isolation | Up to 920 VDC | Secondary referenced to switching node |
| STGAP2SiC rated isolation | 1200 V working, 5700 V surge | Exceeds requirement |
| PCB creepage across driver | Per IC package (SO-8W: 5.3 mm) | Supplemented by PCB slot |
| **PCB slot under driver** | **1.5–2 mm wide** | Increases effective creepage |
| **Total creepage target** | **≥8 mm** | Including slot contribution |

### Functional Insulation (Gate Drive Circuit)

Within the gate drive circuit on the secondary (floating) side, the voltages are low:

| Pair | Voltage | Clearance | Creepage |
|------|---------|-----------|----------|
| VDRV (+18V) → Kelvin source | 18 V | 0.2 mm | 0.5 mm |
| VNEG (−5V) → Kelvin source | 5 V | 0.1 mm | 0.3 mm |
| Gate trace → source trace | 23 V (VDRV − VNEG) | 0.2 mm | 0.5 mm |

These are well within standard PCB trace/space capabilities (0.15 mm minimum).

### Phase-to-Phase (Basic Insulation)

| Parameter | Value |
|-----------|-------|
| Working voltage | 918 VAC RMS (line-to-line at 530V input) |
| Peak voltage | 1300 Vpk |
| Clearance | 5 mm (basic, PD2) |
| Creepage | 8 mm (basic, PD2, IIIb) |

### Summary Table — All Voltage Pairs

| Pair | Clearance (mm) | Creepage (mm) | Insulation | Notes |
|------|----------------|---------------|------------|-------|
| AC phase → PE | 6.4 | 10 | Reinforced | Controlling: creepage |
| DC bus → PE | 8 | 14 | Reinforced | **Largest requirement on board** |
| AC phase → phase | 5 | 8 | Basic | Line-to-line |
| DC bus (+) → (−) | 5 | 8 | Basic | Same circuit, operational |
| DC bus → AC input | 5 | 8 | Basic | Separated by inductor |
| Gate drive HV → LV | 6.4 | 10 | Reinforced | Across STGAP2SiC isolation |
| Gate functional | 0.2 | 0.5 | Functional | Within floating gate circuit |
| LV control → PE | 0.5 | 1.0 | Functional | SELV circuit |

## PCB Slot Strategy

Where the required creepage distance cannot be achieved by copper spacing alone (due to board area constraints), PCB slots are used to increase the effective creepage path:

### How Slots Increase Creepage

A slot forces the creepage path to go around the slot edges, increasing the surface distance:

```
    Without slot:
    ───copper A──── gap ────copper B───
                   ←6mm→
    Creepage = 6 mm

    With slot (2mm wide):
    ───copper A────╱    ╲────copper B───
                  │ slot │
                  │ 2mm  │
    ───           ╲    ╱           ───
    Creepage = 6mm + 2×1.6mm(slot depth×2 sides) = ~9.2mm
```

The slot adds approximately 2× the board thickness to the creepage path (current must traverse down one side of the slot and up the other).

### Slot Specifications

| Parameter | Value |
|-----------|-------|
| Slot width | 1.5–2.0 mm |
| Slot routing tool | 1.5 mm end mill (minimum) |
| Copper keepout around slot | 0.5 mm on all layers |
| Slot depth into board | Full through-cut (both sides open) |
| Minimum slot length | 5 mm (structural integrity) |
| Maximum slot length | Per fabricator capability (typically unlimited for routing) |

### Where Slots Are Required

| Location | Purpose | Slot Width |
|----------|---------|-----------|
| Under each STGAP2SiC driver | Increase creepage across isolation barrier | 1.5 mm |
| Between AC input connector and PE | If 10 mm creepage cannot be achieved with copper spacing | 2.0 mm |
| Between DC bus copper and mounting holes | If 14 mm creepage cannot be achieved | 2.0 mm |
| Between phase conductors (if tight) | If 8 mm creepage cannot be achieved | 1.5 mm |

> [!warning] Slots Weaken the Board
> Each slot removes material from the PCB, reducing mechanical strength and potentially creating stress concentration points. Do not place slots:
> - Near board edges (within 3 mm)
> - Near mounting holes (within 5 mm)
> - In areas subjected to bending stress (connector insertion zones)
> - Parallel to and close to each other (maintain ≥5 mm between slots)
>
> Verify structural integrity with the mechanical design team if multiple slots are used in close proximity.

## Heatsink Mounting — Creepage to PE

### Problem Statement

The TO-247 MOSFET mounting hole passes through the PCB near the drain copper pad. The drain is at switching node voltage (0 to 920 VDC). The heatsink mounting screw connects to the heatsink, which may be connected to PE (protective earth) or chassis ground.

The creepage path from drain copper to the PE-connected mounting hole must meet the DC bus→PE requirement: **14 mm**.

### Solution

| Measure | Specification |
|---------|--------------|
| Copper keepout around mounting hole | Drain copper pulled back ≥14 mm from the edge of the mounting hole |
| Slot between drain copper and mounting hole | 2 mm wide slot if 14 mm spacing is not achievable |
| Alternative: Insulated mounting bushing | Plastic shoulder washer isolates screw from heatsink/PE |
| Alternative: Floating heatsink | Heatsink not connected to PE (reduces creepage requirement to basic) |

```
    TO-247 mounting detail (top view):

    ┌───────────────────────────────────┐
    │         Drain copper (L1)         │
    │         (switching node)          │
    │                                   │
    │     ┌─────────┐                   │
    │     │  TO-247  │                  │
    │     │  body    │                  │
    │     └─────────┘                   │
    │         │                         │
    │         │  ≥14mm                  │
    │         │                         │
    │    ─────┼───── no copper zone ────│
    │         │                         │
    │         ○ M3 mounting hole (PE)   │
    │                                   │
    └───────────────────────────────────┘
```

> [!tip] Insulated Mounting Hardware
> Using insulated shoulder washers and bushings at the mounting holes allows the heatsink to float (not connected to PE). In this case:
> - The insulation is part of the safety system — it must be rated and tested
> - The creepage requirement from drain to mounting hole becomes **functional** (much smaller)
> - However, the floating heatsink will charge to the CM voltage, increasing radiated emissions
> - A compromise: connect the heatsink to PE through a high-value Y-capacitor (4.7 nF) to provide a CM return path while maintaining isolation at DC

## Internal Layer Clearances (IPC-2221B)

### L1-to-L2 Clearance (Through Prepreg)

Conductors on adjacent layers are separated by the prepreg or core dielectric. IPC-2221B specifies minimum internal clearances based on voltage and the dielectric type:

| Parameter | Value |
|-----------|-------|
| Voltage between L1 and L2 | Up to 920 VDC (DC bus on L1, GND on L2) |
| Dielectric material | FR-4 prepreg |
| Dielectric thickness | 75–100 µm (per [[01-Stack-Up and Layer Assignment]]) |
| Dielectric strength of FR-4 | ~20 kV/mm (minimum per IPC-4101) |
| Breakdown voltage at 100 µm | 20 kV/mm × 0.1 mm = 2000 V |
| Safety margin | 2000 / 920 = 2.17:1 |
| IPC-2221B internal clearance (Table 6-1) | 0.25 mm for 500V; extrapolate for 920V → ~0.5 mm |

**Minimum internal clearance between conductors on L1 and L2: 0.5 mm**

This means that copper features on L1 and L2 that belong to different nets must not overlap with less than 0.5 mm clearance when viewed from above.

> [!warning] Internal Clearance at 920V
> The 100 µm prepreg between L1 and L2 has a theoretical breakdown of 2000V, but this assumes perfect dielectric with no voids, no contamination, and no aging. In practice:
> - Manufacturing defects (voids, pinholes) can reduce breakdown by 50%
> - Humidity and ionic contamination degrade dielectric over time
> - Temperature cycling creates microcracks
>
> Maintain the minimum 0.5 mm internal clearance (plan view) between different voltage domains on adjacent layers. For the most critical pairs (DC bus on L1 vs. GND on L2), the overlap is intentional and beneficial (reduces loop inductance) — the dielectric isolation is adequate for this voltage class.

### L3-to-L4 Clearance

| Parameter | Value |
|-----------|-------|
| Voltage between L3 and L4 | ≤25V (signal layers, auxiliary power) |
| Core thickness | 360 µm |
| Required clearance | Standard (0.15 mm minimum trace/space) |

No special internal clearance considerations for L3-L4.

## DRC Net Class Table

Configure the EDA tool's Design Rule Check (DRC) with net classes to enforce creepage and clearance automatically:

### Net Class Definitions

| Net Class | Nets Included | Min Clearance to PE Class | Min Clearance to HV-DC Class | Min Clearance to AC Class | Min Clearance within Class |
|-----------|---------------|--------------------------|-----------------------------|--------------------------|-----------------------------|
| **HV-DC** | DC_BUS_P, DC_BUS_N | 14 mm (creepage) / 8 mm (clearance) | 8 mm | 8 mm | 5 mm |
| **AC-PHASE** | AC_L1, AC_L2, AC_L3 | 10 mm (creepage) / 6.4 mm (clearance) | 8 mm | 8 mm (phase-phase) | 5 mm |
| **PE-EARTH** | PE, CHASSIS_GND, HEATSINK | — | 14 mm | 10 mm | 0.3 mm |
| **SW-NODE** | SW_A, SW_B, SW_C | 14 mm | 5 mm | 5 mm | 5 mm |
| **GATE-HV** | GATE_A..F, KELVIN_A..F, VDRV_A..F, VNEG_A..F | 10 mm | 5 mm | 5 mm | 0.5 mm |
| **LV-CTRL** | SPI_CLK, SPI_MOSI, SPI_MISO, VCC_5V, VCC_3V3 | 1.0 mm | 10 mm | 10 mm | 0.15 mm |
| **GND** | GND (L2 plane) | 0.3 mm | N/A (adjacent planes) | N/A | — |

### DRC Rule Matrix (Clearance, mm)

|  | HV-DC | AC-PHASE | PE-EARTH | SW-NODE | GATE-HV | LV-CTRL | GND |
|--|-------|----------|----------|---------|---------|---------|-----|
| **HV-DC** | 5 | 8 | 14 | 5 | 5 | 10 | * |
| **AC-PHASE** | 8 | 5 | 10 | 5 | 5 | 10 | * |
| **PE-EARTH** | 14 | 10 | 0.3 | 14 | 10 | 1.0 | 0.3 |
| **SW-NODE** | 5 | 5 | 14 | 5 | 5 | 10 | * |
| **GATE-HV** | 5 | 5 | 10 | 5 | 0.5 | 10 | * |
| **LV-CTRL** | 10 | 10 | 1.0 | 10 | 10 | 0.15 | 0.3 |
| **GND** | * | * | 0.3 | * | * | 0.3 | — |

\* GND plane (L2) intentionally underlies all nets for return path — internal clearance rules apply per IPC-2221B, not surface creepage.

> [!tip] DRC Setup in EDA Tool
> Most EDA tools (Altium, KiCad, etc.) support net class–based clearance rules. Set up the net classes early in the design and assign all nets before starting routing. Run DRC frequently during layout to catch violations before they become difficult to fix.
>
> **Important:** The DRC clearance values in the table above are the **creepage** values (worst case). The EDA tool's DRC checks clearance (air gap), not creepage (surface path). For flat PCB surfaces, clearance = creepage, so this is conservative. Where slots are used, the effective creepage is larger than the air clearance.

## Conformal Coating Considerations

Conformal coating can reduce effective creepage on assembled boards if the coating bridges gaps:

| Rule | Requirement |
|------|-------------|
| Coating type | Acrylic or silicone-based, IEC 60664-3 compliant |
| Coating thickness | 25–75 µm per IPC-CC-830 |
| Keep-out areas | Do not coat connector mating surfaces, test points, mounting holes |
| Creepage under coating | IEC 60664-3 allows reduced creepage with qualifying coating; verify with test lab |
| Assembly verification | After coating, inspect all high-voltage gaps for coating bridges or voids |

> [!warning] Conformal Coating Does NOT Automatically Reduce Creepage
> A common misconception is that conformal coating allows reduced creepage distances. Per IEC 60664-3, this is only valid if:
> 1. The coating is applied per a qualified process
> 2. The coating material is tested to the required voltage
> 3. The process is validated with production-level testing
>
> Until the conformal coating process is qualified, design the PCB to meet **uncoated** creepage requirements.

## Assembly and Inspection Considerations

### Critical Inspection Points

After board assembly, the following must be inspected for creepage compliance:

| Location | What to Check | Accept/Reject Criteria |
|----------|---------------|----------------------|
| AC input terminal pads | Solder fillet extent | Fillet must not extend beyond pad, reducing creepage |
| DC bus capacitor leads | Solder wicking on leads | Wicking must not bridge to adjacent conductors |
| MOSFET mounting area | Thermal pad solder/TIM placement | No solder or TIM extending beyond the pad |
| PCB slots | Slot edges clean, no debris | No conductive debris bridging the slot |
| STGAP2SiC isolation gap | No solder bridges | Zero bridges across the isolation gap |
| Heatsink mounting holes | Insulating bushings in place | Bushing seated, no metal-to-metal contact |
| Board edges near HV copper | No copper exposure | Copper pulled back ≥0.5 mm from board edge |

### Hipot (Dielectric Withstand) Testing

Per IEC 62368-1, the following hipot tests are required on the finished board/assembly:

| Test | Voltage | Duration | Between |
|------|---------|----------|---------|
| AC input to PE | 3000 VAC (or 4242 VDC) | 60 seconds | AC phases shorted together vs. PE |
| DC bus to PE | 3680 VDC (2× working + 1000V) | 60 seconds | DC bus vs. PE |
| Gate drive isolation | Per STGAP2SiC spec (5700 Vpk surge) | 1 second | Primary vs. secondary |

> [!warning] Hipot Testing After Assembly
> Hipot testing must be performed on **every production unit**, not just qualification samples. The test voltages are high enough to damage components if applied incorrectly. Ensure:
> - All sensitive components (ICs, capacitors below rated voltage) are disconnected or protected during testing
> - Test fixtures are designed to safely apply and remove HV
> - Operators are trained in HV safety procedures
> - Test equipment has current-limited outputs and interlock mechanisms

## Design Review Checklist

Before releasing the layout for fabrication, verify:

- [ ] All net pairs in the DRC rule matrix have clearance/creepage rules assigned
- [ ] DRC runs clean (zero violations) with the high-voltage rule set
- [ ] PCB slots are present at all locations specified in the slot table
- [ ] Heatsink mounting holes have adequate copper keepout (14 mm from drain copper)
- [ ] No copper extends to within 0.5 mm of any board edge
- [ ] Internal clearance between L1 and L2 copper features on different voltage domains is ≥0.5 mm
- [ ] Conformal coating keep-out areas are defined in the assembly drawing
- [ ] Hipot test points are accessible on the assembled board
- [ ] All solder mask openings near HV gaps have been reviewed for adequate coverage
- [ ] Silkscreen does not bridge HV gaps (silkscreen ink can be slightly conductive when contaminated)

## Cross-References

- [[__init]] — Board overview and operating voltages
- [[01-Stack-Up and Layer Assignment]] — Prepreg thickness for internal clearance
- [[03-Gate Driver Layout]] — STGAP2SiC isolation gap and PCB slot
- [[04-Thermal Layout]] — Heatsink mounting hole proximity to drain copper
- [[05-EMI-Aware Layout]] — Y-capacitor placement and leakage current
- [[01-Topology Selection]] — Device voltage class selection
- [[SiC Device Thermal Parameters]] — Package dimensions for pad sizing

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-02-22 | — | Initial draft: creepage/clearance tables, slot strategy, DRC net classes |
