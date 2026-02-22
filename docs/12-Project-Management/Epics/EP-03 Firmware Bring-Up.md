---
tags: [PDU, project-management, epic, phase-2, firmware, bring-up, STM32G474]
created: 2026-02-22
---

# EP-03 — Firmware Bring-Up

> **Phase 2 | Duration: 7 weeks | Lead: FW**
> Gate exit: Open-loop PFC and LLC verified on hardware. All 12 HRTIM channels producing correct PWM. ADC readings calibrated. SRF-PLL locking to grid. Basic protection functional. CAN loopback working.

---

## Epic Summary

This epic transitions firmware from a Nucleo dev board to the actual Rev A hardware. Peripherals are configured, control loops are tested in open-loop mode first (fixed duty / fixed frequency), and hardware protection is validated. The goal is to have a known-good platform ready for closed-loop system integration (EP-04).

**Entry criteria:** MCU boots on target board (EP-02-007). Gate driver waveforms verified (EP-02-008). ADC channels responding (EP-02-009).
**Exit criteria:** Open-loop PFC and LLC produce correct output. ADC readings match power analyzer. HRTIM fault inputs trip correctly.

---

## Stories

### Peripheral Initialization

#### EP-03-001: Implement System Init Sequence
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-01-016, EP-02-007 |
| **Blocks** | EP-03-002, EP-03-003, EP-03-004 |

**Description:** Implement the initialization sequence from [[06-Firmware-Design/02-Power-On Sequence and Ramp Control]] §1: clock config (170 MHz), GPIO, HRTIM DLL calibration (14 ms, 50 ms timeout), ADC self-calibration (5 instances × 2 ms), DMA config, CORDIC/FMAC init, TIM6 (1 kHz), flash fault log init.

**Acceptance criteria:**
- [ ] `System_Init()` runs to completion on all 5 units
- [ ] HRTIM DLL lock confirmed (DLLRDY flag within 20 ms)
- [ ] All 5 ADC self-calibrations complete without timeout
- [ ] TIM6 1 kHz tick verified with scope on GPIO toggle
- [ ] Total init time < 50 ms (measured)

---

#### EP-03-002: Implement Application State Machine Framework
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-001 |
| **Blocks** | EP-03-004, EP-03-006, EP-03-010 |

**Description:** Implement `App_SM_Run()` per [[06-Firmware-Design/01-Application State Machine]]. All 10 states, `State_Transition()` helper with CAN broadcast and state log. ISR-to-main-loop flag passing via atomic operations. For this phase, implement POWER_ON, STANDBY, and DISABLED states fully; stub remaining states.

**Acceptance criteria:**
- [ ] State machine cycles at 1 kHz (measured)
- [ ] POWER_ON → STANDBY transition on successful init
- [ ] POWER_ON → DISABLED on simulated init failure
- [ ] State transitions logged to UART debug output
- [ ] State change broadcast on CAN (verified with bus analyzer)

---

#### EP-03-003: Implement ADC Pipeline and DMA
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-001, EP-02-009 |
| **Blocks** | EP-03-004, EP-03-006 |

**Description:** Implement the full ADC pipeline per [[06-Firmware-Design/06-ADC Pipeline and DMA Configuration]]: HRTIM trigger routing (`ADC_TriggerRouting_Init()`), injected group ISR read, regular group DMA circular double-buffer, 16x hardware oversampling on regular group. Implement software filters: bus voltage biquad IIR (100 Hz), temperature EMA (alpha=0.01), LLC output 1st-order IIR (fc ~955 Hz).

**Acceptance criteria:**
- [ ] Injected channels triggered by HRTIM CMP2 events (verified with scope: ADC_EOC flag vs PWM center)
- [ ] DMA circular buffer filling correctly (half-transfer and transfer-complete interrupts firing)
- [ ] Hardware oversampling producing 16-bit effective resolution on NTC channels
- [ ] Biquad filter attenuating 300 Hz by >=18 dB (inject sine wave, measure output)
- [ ] ES0430 errata workaround verified (no DMA corruption under mixed injected/regular)

---

### PFC Bring-Up

#### EP-03-004: PFC Open-Loop PWM Test
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-002, EP-03-003, EP-02-008 |
| **Blocks** | EP-03-005 |

**Description:** Configure HRTIM Timers A, B, C for PFC at 65 kHz with fixed duty cycle. Verify all 6 outputs (TA1/TA2, TB1/TB2, TC1/TC2), dead-time (300 ns), and 120-degree phase interleaving via Master timer compare registers. Run into resistive load at low voltage (50 VAC input) to verify waveform quality.

**Test conditions:**
| Parameter | Value |
|-----------|-------|
| Input voltage | 50 VAC, 3-phase (variac) |
| Switching frequency | 65 kHz |
| Duty cycle | Fixed 30% (open-loop) |
| Load | Resistive (bus capacitors only) |

**Acceptance criteria:**
- [ ] All 6 PFC outputs switching at 65 kHz (±0.1%)
- [ ] Dead-time 300 ns ±50 ns on all 3 legs
- [ ] Phase interleaving: 120° ±2° between legs (measured via scope)
- [ ] Bus voltage rises to expected level at 30% duty (Vbus ≈ 50/0.7 ≈ 71 V)
- [ ] No shoot-through (verified by measuring shunt current spikes)

---

#### EP-03-005: Implement SRF-PLL and Verify Grid Lock
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-004 |
| **Blocks** | EP-04-001 |

**Description:** Implement SRF-PLL per [[06-Firmware Architecture]] §4.2 and lock detection per [[06-Firmware-Design/02-Power-On Sequence and Ramp Control]] §2. Omega-hat ramp from 0 (rate limit 500 rad/s²). Lock detection: |V_q| < 5 V for 20 consecutive samples. 2 s timeout.

**Test at:**
- 400 VAC / 50 Hz (nominal)
- 480 VAC / 60 Hz
- 260 VAC / 50 Hz (minimum input)
- 530 VAC / 50 Hz (maximum input)

**Acceptance criteria:**
- [ ] PLL locks within 1 s at all test voltages (well under 2 s timeout)
- [ ] Theta-hat tracks grid angle with < 2° error (measured against zero-crossing)
- [ ] Omega-hat settles to 314.16 rad/s ±0.5% at 50 Hz grid
- [ ] V_q < 5 V sustained after lock
- [ ] PLL_LOCK → SOFT_START_PFC transition fires correctly

---

### LLC Bring-Up

#### EP-03-006: LLC Open-Loop Frequency Sweep
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (8 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-002, EP-03-003, EP-02-008, EP-02-014 |
| **Blocks** | EP-03-007 |

**Description:** Configure HRTIM Timers D, E, F for LLC with HALF mode (50% duty). Sweep frequency from 300 kHz down to 100 kHz in open-loop steps (no voltage regulation). Record output voltage vs. frequency to validate gain curve against [[03-LLC Gain Curve Verification]].

**Test conditions:**
| Parameter | Value |
|-----------|-------|
| Bus voltage | 800 VDC (from bench supply to DC bus) |
| Frequency sweep | 300 kHz → 100 kHz in 10 kHz steps |
| Load | 10 ohm resistive (for ~5 kW test) |
| Phases enabled | Single phase first, then all 3 |

**Acceptance criteria:**
- [ ] Gain curve matches FHA model within ±10%
- [ ] Resonant peak identified near 150 kHz (within 140–160 kHz)
- [ ] ZVS confirmed at all frequencies above resonance (drain waveform transitions before gate-on)
- [ ] Phase interleaving verified: 120° between D, E, F outputs
- [ ] No resonant current overshoot (I_LLC_peak < 2x rated at any frequency)

---

#### EP-03-007: LLC Soft-Start Sequence Verification
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-006 |
| **Blocks** | EP-04-004 |

**Description:** Implement `LLC_SoftStart_Begin()` and `LLC_SoftStart_Tick()` per [[06-Firmware-Design/02-Power-On Sequence and Ramp Control]] §4. Verify staggered phase enable (100 ms spacing), frequency ramp from 300 kHz down to operating point, and contactor close when V_out within 5% of target.

**Acceptance criteria:**
- [ ] Phase 1 enables at t=0, Phase 2 at t+100 ms, Phase 3 at t+200 ms
- [ ] Frequency ramp smooth (no glitches in PERxR transitions)
- [ ] Output voltage rises monotonically during soft-start
- [ ] Contactor closes at correct V_out threshold
- [ ] Total LLC soft-start < 1.5 s

---

### Protection Implementation

#### EP-03-008: Configure HRTIM Hardware Fault Inputs
| Field | Value |
|-------|-------|
| **Assignee** | FW, PE |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-001 |
| **Blocks** | EP-03-009 |

**Description:** Configure HRTIM FLT1–FLT5 per [[06-Firmware Architecture]] §7.1:

| Fault Input | Source | Mode | Response |
|------------|--------|------|----------|
| FLT1 | COMP1/2/3 (PFC OCP) | Latch | All PFC outputs → idle |
| FLT2 | COMP4/5 (LLC OCP) | Latch | LLC outputs → idle |
| FLT3 | COMP6 (DC bus OVP) | Latch | All outputs → idle |
| FLT4 | COMP7 (output OVP) | Latch | LLC outputs → idle |
| FLT5 | External (ground fault) | Latch | All outputs → idle |

Configure analog comparators with correct thresholds (DAC or internal reference).

**Acceptance criteria:**
- [ ] FLT1: inject 78 A equivalent signal → PFC outputs go idle within 200 ns
- [ ] FLT3: inject 966 V equivalent signal → all outputs go idle within 1 us
- [ ] Fault ISR fires and sets `g_fault_pending` flag
- [ ] Outputs remain idle until firmware explicitly clears fault
- [ ] All 5 fault inputs tested and latency measured with scope

---

#### EP-03-009: Implement Firmware Fault State Machine
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | L (10 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-008, EP-03-002 |
| **Blocks** | EP-04-008 |

**Description:** Implement `Fault_Enter()`, `Fault_Recovery_Check()`, and `Thermal_Derate_Calc()` per [[06-Firmware-Design/03-Fault State Machine and Recovery]]. Implement fault log ring buffer in flash (256 entries × 12 bytes). Implement fault severity lookup table (24 fault sources). Test retry logic (3 retries with 10 s cooldown).

**Acceptance criteria:**
- [ ] `Fault_Enter()` disables all HRTIM outputs within 1 main-loop tick
- [ ] Fault logged to flash ring buffer (read back via debugger)
- [ ] Critical faults latch (no auto-recovery)
- [ ] Major faults retry up to 3 times then latch
- [ ] `Thermal_Derate_Calc()` returns correct power limit for simulated temperature inputs
- [ ] Diagnostic clear command via CAN resets latched fault

---

#### EP-03-010: Implement Power-On and Shutdown Sequences
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-002, EP-03-005, EP-03-007 |
| **Blocks** | EP-04-001 |

**Description:** Implement `PFC_SoftStart_Begin/Tick()` and `Shutdown_Tick()` per [[06-Firmware-Design/02-Power-On Sequence and Ramp Control]]. PFC soft-start: I_d* linear ramp 0 → rated over 200 ms, anti-windup pre-load, NTC bypass relay at 80% Vbus. Shutdown: reverse sequence with I_out ramp to 0, output disable, contactor open.

**Acceptance criteria:**
- [ ] PFC soft-start completes in < 300 ms (I_d* reaches target)
- [ ] NTC bypass relay engages at correct Vbus threshold
- [ ] Shutdown ramp-down smooth (no voltage spikes)
- [ ] Output contactor opens only after I_out < 0.5 A
- [ ] Total startup <=6 s (measured end-to-end)

---

### Control Foundations

#### EP-03-011: Implement Clarke/Park Transforms and SVM
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-005 |
| **Blocks** | EP-04-001 |

**Description:** Implement forward Clarke (abc → alpha-beta), forward Park (alpha-beta → dq using theta from PLL), inverse Park, and Space Vector Modulation. Use CORDIC co-processor for sin/cos. Verify transforms against MATLAB/Python reference vectors.

**Acceptance criteria:**
- [ ] Clarke transform output matches reference within 0.1% (fixed test vector)
- [ ] Park transform correct for theta = 0, 90, 180, 270 degrees
- [ ] CORDIC sin/cos execution < 50 ns (14 cycles)
- [ ] SVM duty cycles sum to valid range [0,1] for all sectors
- [ ] Inverse Park → SVM → HRTIM duty update completes within ISR budget (< 3 us)

---

#### EP-03-012: Implement PI Controllers with Anti-Windup
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | — |
| **Blocks** | EP-04-001, EP-04-004 |

**Description:** Implement generic PI controller structure with back-calculation anti-windup (tracking time constant Tt = sqrt(Ti/Tp)). Instantiate for: d-axis current PI, q-axis current PI, bus voltage PI, LLC voltage PI, LLC current PI. Configure gains per [[06-Firmware Architecture]] §4.1 and §5.2.

**Acceptance criteria:**
- [ ] PI controller unit-tested with step input (overshoot < 5%, settling < 10 cycles)
- [ ] Anti-windup prevents integrator saturation at output limits
- [ ] Gains configurable at runtime (for tuning via debugger)
- [ ] Execution time < 200 ns per PI instance

---

#### EP-03-013: Implement Neutral Point Balancing
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-003, EP-03-011 |
| **Blocks** | EP-04-002 |

**Description:** Implement `NP_Balance_Update()` per [[06-Firmware-Design/07-Neutral Point Balancing]]. P-controller (K_NP=0.005), zero-sequence injection via SVM offset, ±5% clamp, warning at |V_NP_err| > 20 V for 1 s, fault at > 50 V for 100 ms.

**Acceptance criteria:**
- [ ] V_NP_err computed correctly from V_cap_top − V_cap_bot ADC readings
- [ ] Zero-sequence offset applied to SVM (verified by scope on duty cycles)
- [ ] Clamp at ±5% modulation index verified
- [ ] Warning threshold triggers LED and event log
- [ ] Will be fully tested under load in EP-04

---

### Communications

#### EP-03-014: Implement CAN Protocol — Status and Command Frames
| Field | Value |
|-------|-------|
| **Assignee** | FW-COM |
| **Size** | M (5 days) |
| **Status** | Backlog |
| **Depends on** | EP-02-010 |
| **Blocks** | EP-04-009 |

**Description:** Implement CAN frame encoding/decoding per [[06-Firmware Architecture]] §6.2. Status frame (module → master, 10 ms broadcast): I_out, V_out, fault flags, temperature, module state. Command frame (master → all, 10 ms): V_ref, I_ref, enable flags. Implement CAN watchdog (50 ms warning, 200 ms shutdown).

**Acceptance criteria:**
- [ ] Status frame broadcasts every 10 ms (verified with CAN bus analyzer)
- [ ] Command frame parsed correctly (test with CAN bus tool sending known values)
- [ ] Node ID read from DIP switch and embedded in frame headers
- [ ] CAN watchdog fires at 50 ms (derate) and 200 ms (shutdown) thresholds
- [ ] Bus-off recovery implemented (auto-restart after 128 × 11 bit times)

---

#### EP-03-015: Implement UART Debug Console
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (2 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-001 |
| **Blocks** | — |

**Description:** Implement lightweight UART CLI for debugging: real-time ADC readout, state machine status, PI gain adjustment, fault log dump, HRTIM register peek/poke. Non-blocking transmit via DMA. 115200 baud.

**Acceptance criteria:**
- [ ] `status` command prints: state, Vbus, Iout, Vout, T_sic, T_mag, T_amb
- [ ] `gain <loop> <kp> <ki>` adjusts PI gains at runtime
- [ ] `fault` command dumps fault log ring buffer
- [ ] DMA transmit does not block ISR execution

---

#### EP-03-016: Implement Burst Mode Framework
| Field | Value |
|-------|-------|
| **Assignee** | FW |
| **Size** | S (3 days) |
| **Status** | Backlog |
| **Depends on** | EP-03-006 |
| **Blocks** | EP-06-008 |

**Description:** Implement `Burst_Mode_Tick()` and `HRTIM_BurstMode_Config()` per [[06-Firmware-Design/04-LLC Burst Mode]]. Configure HRTIM burst mode controller registers (BMPER, BMCMPR, BMCR). Implement integrator freeze during idle. Will be fully tested under light load in EP-04 / EP-06.

**Acceptance criteria:**
- [ ] HRTIM burst mode controller registers configured correctly
- [ ] Burst mode sub-state machine transitions (INACTIVE → RUN → IDLE → RUN)
- [ ] LLC PI integrator freezes during BURST_IDLE
- [ ] Load detection during idle (V_out monitoring)
- [ ] Framework compiles and runs; full characterization deferred to EP-06

---

## References

- [[06-Firmware Architecture]] — Peripheral configuration, control loops, CAN protocol
- [[06-Firmware-Design/__init|06-Firmware Design]] — Implementation pseudocode for all firmware subsystems
- [[12-Project-Management/__init|Project Management]] — Phase 2 entry/exit criteria

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — 16 stories |
