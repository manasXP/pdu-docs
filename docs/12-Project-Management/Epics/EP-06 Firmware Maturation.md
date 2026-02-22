---
tags: [PDU, project-management, epic, phase-5, firmware, CAN, OCPP, stacking]
created: 2026-02-22
---

# EP-06 — Firmware Maturation

> **Phase 5 | Duration: 10 weeks | Lead: FW-COM**
> Gate exit: 5-module CAN stacking validated at 150 kW. OCPP 1.6 and ISO 15118 interface working with charger controller. Burst mode characterized. All firmware features integration-tested.

---

## Epic Summary

This epic matures the firmware from single-module operation to a production-ready multi-module system. The CAN master FSM enables 5-module stacking with current redistribution and failover. The OCPP/ISO 15118 interface connects the PDU modules to the charger controller. Burst mode and advanced features are characterized.

**Entry criteria:** Rev B units available (EP-05-007). Single-module 30 kW working (EP-04 complete).
**Exit criteria:** 5 modules stacked at 150 kW. OCPP session starts/stops correctly. Firmware version tagged as release candidate.

---

## Stories

### CAN Stacking

#### EP-06-001: Set Up 5-Module Test Bench
| Field | Value |
|-------|-------|
| **Assignee** | PE, ME |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-05-011 |
| **Blocks** | EP-06-002 |

**Description:** Wire 5 Rev B modules on CAN bus (daisy-chain, 120 ohm terminations). Configure DIP switches for node IDs 0–4. Connect all modules to common AC input (3-phase, 60 A capacity) and common DC output bus (parallel connection to 150 kW DC load). Install safety barriers for 1000 VDC operation.

**Acceptance criteria:**
- [ ] 5 modules physically installed and wired
- [ ] CAN bus operational (all 5 nodes visible on bus analyzer)
- [ ] AC input breaker sized for 150 kW (65 A at 400 VAC)
- [ ] DC load configured for 150 kW CC/CV operation
- [ ] Safety review completed for high-power test setup

---

#### EP-06-002: Implement Master Discovery and Election
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-001, EP-03-014 |
| **Blocks** | EP-06-003 |

**Description:** Implement master FSM INIT state per [[06-Firmware-Design/05-CAN Master and Module Stacking]] §2: 500 ms discovery scan, module table build, lowest-ID-wins election. Verify discovery completes with 1–5 modules present.

**Acceptance criteria:**
- [ ] Master (node 0) discovers all 4 slaves within 500 ms
- [ ] Module table correctly populated (node ID, FW version, state)
- [ ] Discovery works with 1, 2, 3, 4, and 5 modules
- [ ] MASTER_ANNOUNCE broadcast received by all slaves

---

#### EP-06-003: Implement Sequential Enable Sequence
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-002 |
| **Blocks** | EP-06-004 |

**Description:** Implement master FSM ENABLE_SEQ state: send ENABLE_CMD to modules one at a time, 200 ms spacing. Wait for each module to report RUN before enabling the next. Implement LIFO disable with 30 s minimum on-time.

**Acceptance criteria:**
- [ ] 5 modules start sequentially (200 ms spacing, confirmed on scope/CAN log)
- [ ] Total startup <=2 s after all modules individually ready
- [ ] Disable follows LIFO order (module 4 first, then 3, 2, 1)
- [ ] 30 s minimum on-time enforced (test: try to disable at 15 s → rejected)

---

#### EP-06-004: Validate 5-Module Current Sharing at 150 kW
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM, PE |
| **Size** | L (15 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-003, EP-04-009 |
| **Blocks** | EP-06-005, EP-07-001 |

**Description:** Run 5 modules in parallel at 150 kW (750 V, 200 A total, 40 A each). Verify current sharing imbalance < 5%. Test at various power levels: 30/60/90/120/150 kW. Verify module add/shed behavior.

**Acceptance criteria:**
- [ ] 150 kW sustained for 30 minutes (5 × 30 kW)
- [ ] Current imbalance < 5% at all tested power levels
- [ ] Module add at increasing demand: smooth transition, no output dip > 2%
- [ ] Module shed at decreasing demand: smooth, no overshoot
- [ ] Droop-based current sharing stable (no oscillation)

---

#### EP-06-005: Implement Fault Redistribution and Failover
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-004 |
| **Blocks** | EP-06-006 |

**Description:** Implement `Master_Redistribute()` per [[06-Firmware-Design/05-CAN Master and Module Stacking]] §4. Test fault scenarios: 5→4, 4→3, capacity exceeded. Verify slave behavior on master loss (derate at 50 ms, shutdown at 200 ms).

**Acceptance criteria:**
- [ ] 5→4 module transition: remaining modules absorb current in < 100 ms
- [ ] 4→3 module transition: works correctly with ramp
- [ ] Capacity exceeded: upstream notification sent, I_out clamped
- [ ] Master loss: all slaves derate at 50 ms, shutdown at 200 ms
- [ ] Master self-fault: continues CAN coordination while own outputs disabled

---

#### EP-06-006: Implement Diagnostic CAN Frames
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-005 |
| **Blocks** | EP-09-006 |

**Description:** Implement diagnostic frame handlers per [[06-Firmware-Design/05-CAN Master and Module Stacking]] §6: discovery request/response, fault log read-out, FW version query, calibration data read, fault clear command.

**Acceptance criteria:**
- [ ] Fault log read-out via CAN diagnostic frame (verified with CAN tool)
- [ ] FW version response correct (major.minor.build)
- [ ] Diagnostic clear command resets latched faults
- [ ] All diagnostic frames documented in protocol spec

---

### OCPP / ISO 15118 Interface

#### EP-06-007: Implement Charger Controller CAN Interface
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-004 |
| **Blocks** | EP-06-009 |

**Description:** Implement the internal CAN messages between PDU master and charger controller per [[06-Firmware Architecture]] §8.2: Charger_Setpoint (controller → PDU), PDU_Status (PDU → controller), PDU_Fault (PDU → controller). Map OCPP actions to PDU behavior per §8.3.

**Acceptance criteria:**
- [ ] Charger_Setpoint received and applied (V_target, I_target, mode)
- [ ] PDU_Status broadcast at 100 ms (V_out, I_out, P_out, T_max, fault_code, state)
- [ ] PDU_Fault event sent immediately on fault occurrence
- [ ] RemoteStartTransaction → modules start charging
- [ ] RemoteStopTransaction → modules ramp down and stop

---

### Advanced Features

#### EP-06-008: Characterize Burst Mode at Light Load
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-016, EP-04-004 |
| **Blocks** | — |

**Description:** Full characterization of LLC burst mode per [[06-Firmware-Design/04-LLC Burst Mode]]. Test at 1, 2, 3 kW. Measure efficiency improvement vs. continuous PFM. Tune burst frequency and duty cycle for best efficiency/ripple trade-off. Verify entry/exit hysteresis stability.

**Acceptance criteria:**
- [ ] Burst mode activates at < 3 kW (f_sw > 280 kHz threshold)
- [ ] Efficiency at 1 kW: > 85% with burst (vs. ~75% without)
- [ ] Output ripple < 0.5% RMS at all burst-mode points
- [ ] Burst entry/exit smooth (no audible click or voltage transient > 10 V)
- [ ] Load transient exit: < 200 us response to 5 A step

---

#### EP-06-009: End-to-End OCPP Charging Session Test
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-007 |
| **Blocks** | — |

**Description:** Simulate complete OCPP 1.6 charging session using a charger controller emulator (or actual SECC if available). Test: RemoteStartTransaction → CC ramp → CV hold → taper → RemoteStopTransaction. Verify MeterValues reporting and StatusNotification.

**Acceptance criteria:**
- [ ] Complete charge session from start to stop
- [ ] MeterValues (energy, power) reported correctly
- [ ] StatusNotification transitions: Available → Preparing → Charging → Finishing → Available
- [ ] Fault during session: StatusNotification → Faulted, charging stops gracefully

---

#### EP-06-010: Adaptive Dead-Time Optimization
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-04-004 |
| **Blocks** | — |

**Description:** Investigate adaptive dead-time for LLC (vary DT based on load/frequency to optimize ZVS margin while minimizing body diode conduction). Implement measurement-based DT lookup table or closed-loop DT adjustment.

**Acceptance criteria:**
- [ ] Dead-time optimization quantified: efficiency gain at 50% and 100% load
- [ ] No ZVS loss at any operating point (drain waveform verification)
- [ ] Lookup table or algorithm documented and committed

---

#### EP-06-011: Firmware Code Review and Static Analysis
| Field | Value |
|-------|-------|
| **Assignee** | FW, FW-COM |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-005, EP-06-007 |
| **Blocks** | EP-07-001 |

**Description:** Full code review of all firmware modules. Run MISRA-C static analysis (cppcheck or PC-lint). Address all high-severity findings. Document known deviations with justification.

**Acceptance criteria:**
- [ ] All modules peer-reviewed (reviewer sign-off per module)
- [ ] Zero critical MISRA violations
- [ ] All high-severity warnings addressed or justified
- [ ] Code coverage measured (target: > 80% for safety-critical modules)

---

#### EP-06-012: Firmware Release Candidate Tag
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-011 |
| **Blocks** | EP-07-001 |

**Description:** Tag firmware release candidate (e.g., v1.0-rc1). Generate release notes with feature list, known issues, and configuration parameters. Build binary for production flash programming.

**Acceptance criteria:**
- [ ] Git tag created (v1.0-rc1)
- [ ] Release notes document committed
- [ ] Binary .hex file generated and checksummed (SHA-256)
- [ ] Flash programming procedure documented

---

#### EP-06-013: Module Power Management Algorithm
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-06-004 |
| **Blocks** | — |

**Description:** Implement `Master_ModuleSelection()` algorithm: enable/shed modules based on total power demand with 15% hysteresis to prevent cycling. Optimize for efficiency at partial loads (fewer modules at higher utilization vs. more modules at lower utilization).

**Acceptance criteria:**
- [ ] Modules added when demand > (N-1) × 30 kW × 0.95
- [ ] Modules shed when demand < (N-1) × 30 kW × 0.85
- [ ] No rapid cycling (30 s minimum on-time enforced)
- [ ] Efficiency at 60 kW: 3 modules vs. 5 modules compared (document which is better)

---

#### EP-06-014: Calibration Data Storage and Recall
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-009 |
| **Blocks** | EP-09-006 |

**Description:** Implement per-unit calibration data storage in flash: ADC offset/gain for V_bus, I_out, V_out, NTC lookup table parameters. Data written during factory calibration, read at startup.

**Acceptance criteria:**
- [ ] Calibration struct defined and stored in dedicated flash sector
- [ ] Data survives power cycle (read back verified)
- [ ] CRC integrity check on calibration data at startup
- [ ] Default values used if calibration data is blank or corrupt

---

## References

- [[06-Firmware Architecture]] — CAN protocol (§6), OCPP/ISO 15118 interface (§8)
- [[06-Firmware-Design/__init|06-Firmware Design]] — Master FSM, burst mode, stacking implementation
- [[12-Project-Management/__init|Project Management]] — Phase 5 entry/exit criteria

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 14 stories |
