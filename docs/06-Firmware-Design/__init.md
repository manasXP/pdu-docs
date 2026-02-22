---
tags: [PDU, firmware, STM32G474, implementation, index]
created: 2026-02-22
---

# 06 – Firmware Design: Implementation Details

This sub-folder extends [[06-Firmware Architecture]] with implementation-level detail needed to write production C code. The parent document defines HRTIM resource mapping, ADC allocation, control loop structures, CAN frame formats, and protection thresholds. **These sub-documents do not duplicate that content** — they cover the gaps: state machine transitions, pseudocode, DMA configuration, fault recovery logic, burst mode algorithms, and CAN master sequencing.

---

## Sub-Documents

| # | Document | Gap Addressed | Dependencies |
|---|----------|---------------|--------------|
| 01 | [[01-Application State Machine]] | No formal state machine or transition table in parent | None (defines state vocabulary for all others) |
| 02 | [[02-Power-On Sequence and Ramp Control]] | FW-side sequencing detail, ramp profiles, lock detection | 01 (state names) |
| 03 | [[03-Fault State Machine and Recovery]] | Fault classification, derate curves, logging, retry logic | 01 (FAULT/DERATE states) |
| 04 | [[04-LLC Burst Mode]] | Light-load state machine, HRTIM burst register config | 01 (RUN sub-states) |
| 05 | [[05-CAN Master and Module Stacking]] | Master FSM, enable sequencing, failover, redistribution | 01 (state vocabulary), 03 (fault handling) |
| 06 | [[06-ADC Pipeline and DMA Configuration]] | DMA buffers, oversampling config, filter coefficients | None |
| 07 | [[07-Neutral Point Balancing]] | P-controller implementation, zero-sequence injection | None |

## Reading Order

1. **Start with 01** — it defines the 10-state vocabulary (`POWER_ON`, `STANDBY`, `PLL_LOCK`, etc.) referenced everywhere else
2. **Then 02 + 03** — power-on sequence and fault handling flesh out the state transitions
3. **04–07 in any order** — each is self-contained once you know the state vocabulary

## Cross-References to Existing Documents

| Existing Document | Relevance |
|-------------------|-----------|
| [[06-Firmware Architecture]] | Parent specification — HRTIM map, ADC allocation, control loops, CAN frames |
| [[08-Power-On Sequence and Inrush Management]] | HW-side inrush (NTC, relay, contactor) — complementary to 02 (FW-side ramps) |
| [[09-Protection and Safety]] | Protection thresholds, insulation, compliance — complementary to 03 (FW fault FSM) |
| [[04-Thermal Budget]] | Junction temperature limits and derating curves — input to 03 (thermal derate) |
| [[01-Topology Selection]] | Resonant frequencies, ZVS boundaries — input to 04 (burst mode thresholds) |
| [[02-Magnetics Design]] | LLC resonant tank parameters — input to 04 and 07 |

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 7 sub-documents |
