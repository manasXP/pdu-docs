---
tags: [pdu, project-plan, resources, team]
created: 2026-02-22
---

# 03 — Resource Plan

This document defines the team, equipment, facilities, and external services required to execute the 30 kW PDU development programme.

> [!note] See [[04-Budget Estimate]] for associated costs and [[01-Development Phases]] for resource loading by phase.

## Core Team

| Role | FTE | Phases | Key Responsibilities |
|------|-----|--------|---------------------|
| **Power Electronics Lead** | 1.0 | 0–8 | System architecture, PFC/LLC design, power stage debug, certification liaison |
| **Firmware Engineer** | 1.0 | 0–7 | STM32 BSP, control loops (PFC dq, LLC PFM), CAN protocol, OCPP/ISO 15118 |
| **PCB Layout Designer** | 0.5 | 0–1, 4 | Schematic capture, PCB layout, DFM, Gerber release |
| **Mechanical Engineer** | 0.5 | 0–1, 4, 8 | Enclosure, heatsink, bus bars, thermal simulation, assembly drawings |
| **EMC Specialist** | 0.3 | 0, 5–7 | [[05-EMI Filter Design|EMI filter]] tuning, pre-compliance testing, accredited lab liaison |
| **Technician** | 1.0 | 1–7 | Assembly, soldering, wiring, test setup, instrumentation, data logging |

### Optional / Part-Time Roles

| Role | FTE | Phases | Notes |
|------|-----|--------|-------|
| Project Manager | 0.25 | 0–8 | Schedule tracking, procurement, vendor management |
| Quality Engineer | 0.25 | 6–8 | TCF preparation, IPC inspection, production test design |
| Safety Consultant | 0.1 | 6–7 | IEC 62368-1 / UL 2202 interpretation, lab liaison |

### Team Loading by Phase

| Phase | PE Lead | FW Eng | PCB | Mech | EMC | Tech |
|-------|---------|--------|-----|------|-----|------|
| 0 — Design Review | 100% | 50% | 100% | 80% | 30% | 20% |
| 1 — Rev A Build | 60% | 30% | 20% | 60% | — | 100% |
| 2 — FW Bring-Up | 40% | 100% | — | — | — | 80% |
| 3 — Integration | 100% | 100% | — | 20% | — | 100% |
| 4 — Rev B | 60% | 20% | 100% | 40% | 20% | 100% |
| 5 — FW Maturation | 30% | 100% | — | — | 20% | 60% |
| 6 — Cert Prep | 80% | 30% | — | — | 100% | 80% |
| 7 — Pre-Prod | 60% | 20% | — | 20% | 80% | 100% |
| 8 — Release | 40% | 20% | 30% | 40% | — | 40% |

---

## Test Equipment

### Must-Have (Buy or Rent)

| Equipment | Specification | Est. Cost | Buy/Rent | Phase Needed |
|-----------|--------------|-----------|----------|-------------|
| Programmable AC source | 3-phase, 530 VAC, 45 kVA | $25,000–40,000 | Buy (if ongoing) or rent | 3 |
| Electronic DC load | 1000 V, 100 A, 30 kW | $15,000–25,000 | Buy | 3 |
| Power analyzer | 3-phase, 0.1% (Yokogawa WT5000 or equiv.) | $20,000–35,000 | Buy | 3 |
| Oscilloscope | 4-ch, 500 MHz+, 5 GS/s | $8,000–15,000 | Buy | 1 |
| HV differential probes (×4) | 1000 V, 100 MHz | $1,500–3,000 ea. | Buy | 1 |
| Current probes (×4) | 100 A, DC–50 MHz | $1,000–2,000 ea. | Buy | 1 |
| Thermal camera | ≥320×240, -20 to +250°C | $3,000–8,000 | Buy | 3 |
| Hipot tester | 5 kVAC, leakage measurement | $3,000–5,000 | Buy | 6 |
| Insulation resistance tester | 5 kV DC | $1,000–2,000 | Buy | 6 |
| Earth bond tester | 25 A, mΩ resolution | $2,000–4,000 | Buy | 6 |

### Nice-to-Have / Rent

| Equipment | Specification | Est. Cost (Rental/mo) | Phase Needed |
|-----------|--------------|----------------------|-------------|
| EMC pre-compliance receiver | 150 kHz – 1 GHz + LISN | $2,000–4,000/mo | 6 |
| Near-field probe set | H/E field, 30 MHz – 3 GHz | $500–1,500 (buy) | 6 |
| Environmental chamber | -40 to +85°C, humidity | $3,000–5,000/mo | 7 |
| Vibration table | 50 Grms random | $2,000–4,000/mo | 7 |

### Development Tools

| Tool | Specification | Est. Cost |
|------|--------------|-----------|
| STM32CubeIDE + debugger | ST-Link V3 or J-Link | $50–500 |
| CAN bus analyzer | PCAN-USB FD or similar | $300–500 |
| Logic analyzer | 8+ channels, 200 MHz | $300–1,000 |
| Soldering station | Hot air + iron, 0201 capable | $500–1,500 |
| Microscope | Stereo, 7–45× zoom | $500–1,500 |
| ESD workstation | Mat, wrist strap, ionizer | $200–500 |

---

## Facilities

### Power Electronics Lab

| Requirement | Specification |
|-------------|--------------|
| Power supply | 3-phase 400 VAC, 63 A service (minimum) |
| Isolation | Dedicated circuit breaker panel; RCD/GFCI protected |
| Grounding | Dedicated lab earth; separate from building PE if possible |
| Bench space | ≥3 benches (assembly, testing, debug) |
| Ventilation | Fume extraction for soldering; adequate airflow for 30 kW heat load |
| Safety | Fire extinguisher (CO2 + dry powder), first aid, emergency stop, safety glasses |
| ESD | ESD-safe workstations throughout |

### Environmental Chamber Access

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| Temperature range | -40 to +85°C minimum | For thermal cycling and HALT |
| Humidity control | 10–95% RH | For humidity testing |
| Internal size | ≥600×600×600 mm | Must fit assembled PDU unit |
| Power feedthrough | 3-phase 400 VAC, 63 A | For powered thermal testing |
| Vibration (HALT) | 50 Grms 6-axis | Often combined with thermal |

> [!tip] Environmental testing can be outsourced to a test lab if in-house chamber is not available. Budget for 2–4 weeks of chamber rental in Phase 7.

### EMC Chamber Access

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| Type | Semi-anechoic (SAC) or GTEM cell | For radiated emissions |
| Size | 3 m or 10 m measurement distance | 10 m preferred for formal test |
| LISN | 50 Ω / 50 uH, calibrated | For conducted emissions |
| Accreditation | ISO/IEC 17025 (for formal test) | Phase 7 — accredited lab required |
| Pre-compliance | In-house or rented chamber OK | Phase 6 |

---

## External Services

### PCB Fabrication and Assembly

| Service | Specification | Lead Time | Phase |
|---------|--------------|-----------|-------|
| PCB fabrication (prototype) | 6-layer, 2 oz Cu, 3 mil trace/space | 5–10 business days | 1, 4 |
| PCB fabrication (production) | Same spec, panelized | 10–15 business days | 8 |
| PCBA (prototype) | SMT + reflow, 5–10 unit runs | 2–3 weeks (including parts) | 1, 4 |
| PCBA (production) | Full turnkey, 100+ units | 4–6 weeks | 8 |
| Stencil | Stainless steel, laser cut | 3–5 business days | 1, 4 |

### EMC Accredited Lab

| Service | Scope | Duration | Phase |
|---------|-------|----------|-------|
| Full EMC test suite | EN 55032 + EN 61000-series | 2–3 weeks | 7 |
| Emissions only (if re-test needed) | Conducted + radiated | 3–5 days | 7 |
| Test report and CB certificate | IECEE CB scheme | 1–2 weeks after test | 7 |

### Safety Certification Body

| Service | Scope | Duration | Phase |
|---------|-------|----------|-------|
| IEC 62368-1 evaluation | Full safety evaluation | 4–8 weeks | 7 |
| UL 2202 listing | Parallel with CB scheme | 6–12 weeks | 7 |
| CB test certificate | International mutual recognition | Included with evaluation | 7 |
| Factory inspection | Initial production audit | 1 day | 8 |

### Mechanical Fabrication

| Service | Scope | Lead Time | Phase |
|---------|-------|-----------|-------|
| Sheet metal (prototype) | Enclosure panels, brackets — laser cut + bend | 2–3 weeks | 1, 4 |
| Sheet metal (production) | Tooled, powder coated | 4–6 weeks | 8 |
| Heatsink extrusion | Custom profile, anodized (NRE for extrusion die) | 4–8 weeks | 1 |
| Bus bars | Copper, tin-plated, custom shape | 2–3 weeks | 1, 4 |
| CNC machining | Heatsink pocketing, mounting features | 1–2 weeks | 1, 4 |

### Custom Magnetics

| Service | Scope | Lead Time | Phase |
|---------|-------|-----------|-------|
| LLC transformer (prototype) | Custom wound, 5–10 units | 3–4 weeks | 0–1 |
| PFC inductor (prototype) | Custom wound, 5–10 units | 3–4 weeks | 0–1 |
| Magnetics (production) | Tooled bobbin, automated winding | 6–8 weeks | 8 |

---

## Resource Procurement Timeline

| Month | Key Procurement Actions |
|-------|----------------------|
| M1 | Long-lead components ordered (SiC, gate drivers, connectors); magnetics vendor engaged |
| M1.5 | PCB fabrication released; custom magnetics ordered |
| M2 | PCBA service engaged (if not hand-assembling); mechanical fab released |
| M3 | Heatsink extrusion die ordered (if custom) |
| M4 | All Rev A parts received; assembly begins |
| M9 | Rev B component orders; PCBA service for 10 units |
| M11 | EMC lab booked (8–12 weeks ahead); safety certification body engaged |
| M13 | Environmental chamber booked (if renting) |
| M16 | Production component orders; CM engaged |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
