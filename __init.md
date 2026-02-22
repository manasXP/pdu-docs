
**30 kW PDU Design Specification for DC Fast Charger**

A 30 kW Power Delivery Unit (PDU), often implemented as a modular DC charging power module, converts 3-phase AC input to adjustable DC output for EV fast charging, designed for parallel stacking to achieve higher total power like 150 kW with 5 units.evcharging-station+1

## Input Specifications

- Voltage: 260-530 VAC, 3-phase + PE (typically 3P+N+PE at 400/480 VAC).[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    
- Current: Up to 60 A maximum per module; frequency 45-65 Hz.maxwellpower+1
    
- Power factor: ≥0.99; THDi: ≤5% at full load.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    

## Output Specifications

- Rated power: 30 kW (constant power from ~300-1000 VDC).szwinline+1
    
- Voltage range: 150-1000 VDC; current range: 0-100 A.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    
- Accuracy: Voltage ±0.5%, current ±1%; ripple <0.5% RMS.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    

## Efficiency and Performance

Efficiency exceeds 96% peak, with standby power under 8 W and MTBF >120,000 hours.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​  
Soft start ≤6 s prevents inrush; supports CC/CV modes per IEC 61851.webstore.iec+1

## Stacking and System Integration

Five modules stack in parallel via CAN bus for current sharing (imbalance ≤5%), enabling 150 kW total with smart allocation to 2 dispensers.cyberswitching+1  
Modular slot installation; complies with EN/IEC 61851-23 for DC EVSE up to 1500 VDC.webstore.iec+1

## Physical and Environmental

- Dimensions: ~455 x 300 x 94 mm (compact, ~17 kg); fan-cooled, noise ≤65 dB.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    
- Temperature: -30°C to +55°C full load; IP20 enclosure (NEMA 3S/IP54 options).esolutions.free2move+1
    
- Protections: Over/under voltage, current, temperature, short circuit, surge; certifications CE, UL 2202.[[evcharging-station](https://www.evcharging-station.com/sale-12796897-1000v-constant-power-ev-charging-module-30-kw-for-dc-fast-charging-station.html)]​
    

## Communication and Safety

CAN protocol for module coordination; OCPP 1.6, ISO 15118 support in full system.esolutions.free2move+1
For medical/precision applications like your robotics work, prioritize SiC-based designs (e.g., >98% efficiency) and MISRA-compliant controls for reliability.[[wolfspeed](https://www.wolfspeed.com/products/power/reference-designs/crd30dd12n-k/)]​

## Design Documents

- [[01-Topology Selection]] -- **Vienna PFC + 3-Phase Interleaved LLC** (approved)
- [[02-Magnetics Design]] -- LLC resonant tank (Lr, Lm, Cr), transformer, and inductor design (draft)
- [[03-LLC Gain Curve Verification]] -- FHA + ngspice simulation of gain curve and ZVS boundary
- [[04-Thermal Budget]] -- System loss breakdown, junction temperatures, cooling design (draft)
- [[05-EMI Filter Design]] -- Input EMI filter for EN 55032 Class B, surge protection, inrush limiting (draft)
- [[06-Firmware Architecture]] -- STM32G474RE firmware: HRTIM resource map, ADC allocation, Vienna PFC dq control, LLC PFM, CAN stacking protocol, protection, OCPP/ISO 15118 interface
- [[10-Mechanical Integration]] -- Enclosure design, 4-board mounting, heatsink attachment, bus bar routing, airflow path, fan system, connector panel layout, assembly sequence
- [[07-BOM and Cost Analysis]] -- Per-module BOM, cost breakdown @100/@500 qty, procurement notes, alternates
- [[07-PCB-Layout/__init|07-PCB Layout]] -- 6-layer stack-up, power loop optimization, gate driver layout, thermal management, EMI-aware routing, creepage/clearance
- [[08-Power-On Sequence and Inrush Management]] -- Startup/shutdown sequence, inrush analysis, NTC pre-charge, output contactor, cold-start verification
- [[09-Protection and Safety]] -- OVP/OCP/OTP/short-circuit/ground-fault protection design, insulation coordination, surge immunity, hipot requirements, safety compliance matrix (IEC 61851-23, IEC 62368-1, UL 2202)

## Research

- [[3-Phase PFC Topology Selection]] -- Vienna rectifier vs B6, Swiss rectifier, two-level VSI
- [[DC-DC Topology Trade Study]] -- LLC vs DAB vs PSFB vs CLLC vs SRC
- [[Commercial Reference Designs Survey]] -- Wolfspeed, ST, Infineon, onsemi, TI, ADI platforms

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |