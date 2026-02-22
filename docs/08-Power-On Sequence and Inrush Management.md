---
tags: [PDU, inrush, pre-charge, contactor, soft-start, power-sequencing]
created: 2026-02-22
status: draft
---

# Power-On Sequence and Inrush Management — 30 kW PDU

> [!summary] Key Numbers
> Peak inrush (worst-case, 530 VAC, 25°C NTC): **~71 A per phase** through 10 Ω NTC. NTC bypass relay engages at T ≈ 3 s. Total startup to READY: **≤6 s**. Output contactor: 1000 VDC / 100 A rated. Upstream breaker recommendation: **63 A Type D MCB**.

## 1. Design Constraints

From [[__init]]:

| Parameter | Specification |
|-----------|--------------|
| Input voltage | 260–530 VAC, 3-phase + PE |
| Input current | ≤60 A per module |
| Output voltage | 150–1000 VDC |
| Output current | 0–100 A |
| Soft start time | ≤6 s |
| Operating temperature | −30°C to +55°C full load |
| Standards | IEC 61851-23, UL 2202, CE |

### 1.1 Upstream Breaker Assumption

**Recommendation: 63 A Type D MCB (miniature circuit breaker)**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Rating | 63 A | Matches 60 A max input current with standard breaker step |
| Trip curve | Type D | Instantaneous magnetic trip at 10–20× rated (630–1260 A). Type C (5–10×, 315–630 A) risks nuisance trips during NTC inrush |
| Breaking capacity | 10 kA | Standard for industrial 3-phase supply |
| Poles | 3P or 3P+N | 3-phase supply to PDU |

Type D is preferred over Type C because the NTC-limited inrush peak (~75 A per phase at 530 VAC) is only 1.2× the breaker rating — well below the Type D magnetic trip threshold of 630 A. Type B or C breakers at 63 A would also not nuisance-trip at 75 A peak (their magnetic thresholds start at 189 A and 315 A respectively), but Type D provides the widest margin for cold-start scenarios and capacitor charging transients.

### 1.2 DC Bus Capacitance

From [[07-BOM and Cost Analysis]] §5:

| Component | Specification | Qty | Per-Rail C (µF) |
|-----------|--------------|-----|-----------------|
| Main electrolytic | Nichicon UBY 450 V, 470 µF, 125°C | 4 (2 per rail, series) | 235 |
| Midpoint balance | 450 V, 100 µF, 125°C electrolytic | 2 (1 per rail) | 100 |
| Film snubber | EPCOS B32778 500 V, 20 µF polypropylene | 2 (across full bus) | ~10 (equiv.) |

**Per-rail capacitance (rail-to-midpoint):** ~345 µF

**Stored energy at 800 V bus** (400 V per rail):

$$E_{bus} = 2 \times \frac{1}{2} C_{rail} V_{rail}^2 = 2 \times \frac{1}{2} \times 345 \times 10^{-6} \times 400^2 = 55.2 \text{ J}$$

At maximum bus voltage (920 V, 460 V per rail):

$$E_{bus,max} = 2 \times \frac{1}{2} \times 345 \times 10^{-6} \times 460^2 = 73.1 \text{ J}$$

### 1.3 EMI Filter X-Capacitors

From [[05-EMI Filter Design]] §4.3: Total X-capacitance across phase pairs = **9.6 µF** (3 × 2.2 µF Cx1 + 3 × 1.0 µF Cx2). These charge at power-on but store relatively little energy compared to the DC bus:

$$E_{Xcap} = \frac{1}{2} \times 9.6 \times 10^{-6} \times (530\sqrt{2})^2 = 2.7 \text{ J (at 530 VAC)}$$

## 2. Inrush Current Analysis

At initial power-on, the Vienna PFC MOSFETs are OFF. The SiC Schottky diodes (STPSC40H12C) form an uncontrolled 3-phase bridge rectifier that charges the DC bus capacitors. Without current limiting, the peak inrush could exceed 1000 A and weld contacts or trip breakers.

### 2.1 Worst-Case Inrush (25°C, 530 VAC)

The peak inrush occurs when power is applied at the instant of maximum line-to-line voltage:

$$V_{pk} = 530 \times \sqrt{2} = 749.5 \text{ V}$$

With NTC thermistors (10 Ω cold resistance per phase) in the current path:

$$I_{peak} = \frac{V_{pk}}{R_{NTC} + R_{wiring}} = \frac{750}{10 + 0.5} \approx 71 \text{ A per phase}$$

At 260 VAC (minimum input):

$$I_{peak,min} = \frac{260 \times \sqrt{2}}{10.5} = \frac{368}{10.5} \approx 35 \text{ A per phase}$$

### 2.2 Cold-Start Inrush (−30°C, 530 VAC)

NTC thermistors exhibit higher resistance at lower temperatures. For a typical 10 Ω (at 25°C) power NTC, the resistance at −30°C is approximately 15–22 Ω (depending on the B-constant of the selected part, typically B = 3000–4000 K).

Using R_NTC(−30°C) ≈ 18 Ω (conservative mid-estimate):

$$I_{peak,cold} = \frac{750}{18 + 0.5} \approx 41 \text{ A per phase}$$

Lower inrush at cold start (safer for breaker coordination) but slower DC bus charging — see §8 for cold-start timing verification.

### 2.3 I²t Budget vs. Breaker Trip Curve

For a 63 A Type D MCB:
- **Thermal trip:** at 1.3× rated (82 A) → trips in ~60 min. NTC inrush of 71 A is below this threshold.
- **Magnetic trip:** 10–20× rated (630–1260 A) → instantaneous (<10 ms). NTC-limited inrush is well below this.

The NTC inrush I²t during the ~3 s pre-charge phase:

$$I^2 t \approx 40^2 \times 3 = 4{,}800 \text{ A}^2\text{s (RMS estimate)}$$

This is well within the Type D 63 A breaker's thermal let-through of >10,000 A²s. **No nuisance trip expected.**

### 2.4 X-Capacitor Charging Contribution

The 9.6 µF X-caps charge through the NTCs simultaneously with the DC bus. Each X-cap is connected line-to-line, so charging current flows through two NTCs in series (one per phase). Per phase pair: τ = 2 × R_NTC × C_pair = 2 × 10 × 3.2 µF ≈ 64 µs. Peak X-cap charging current is V_LL_pk / (2 × R_NTC) = 750 / 20 ≈ 37 A, but this transient decays in <0.5 ms. Total X-cap energy is only 2.7 J vs. 55–73 J for the DC bus — negligible contribution to the overall inrush budget.

## 3. Input Pre-Charge Circuit

### 3.1 Topology

Three NTC thermistors (one per phase, in series with each AC line) limit inrush current during startup. A bypass relay shorts out the NTCs once the DC bus is charged to eliminate ongoing conduction losses.

> [!info] Physical Location
> The NTC thermistors, bypass relays, and associated RC snubbers are located on the **[[07-PCB-Layout/Power-Entry/__init|Power Entry board]]** (PE-CONT-01), not on the AC-DC board. This separates wear items and inrush heat dissipation from the EMI filter and power stage. See [[07-PCB-Layout/00-Board Partitioning]] for the 5-board architecture.

```
L1 ──[NTC_A]──┬──────── To EMI filter ── To PFC
              │
L2 ──[NTC_B]──┤
              │       ┌─────────────┐
L3 ──[NTC_C]──┤       │ Bypass relay│
              └───────┤ (N.O. 3-pole│────── Bypass to input side of NTCs
                      │ 60A, 600VAC)│
                      └─────────────┘
                        Coil: 24 VDC from aux supply
```

> [!note] The bypass relay uses a single 3-pole (or 3× single-pole) normally-open relay that shorts all three NTCs simultaneously. This avoids phase imbalance during the transition.

### 3.2 NTC Selection

| Parameter | Value |
|-----------|-------|
| Resistance at 25°C | 10 Ω ± 20% |
| Maximum steady-state current | ≥60 A (before bypass) — N/A, bypassed within 3 s |
| Maximum surge current | ≥80 A for 3 s |
| Energy rating (single pulse) | ≥100 J |
| Resistance at −30°C | ~15–22 Ω (B ≈ 3500 K) |
| Resistance self-heated (at 20 A, 3 s) | ~2–4 Ω |
| Package | Disc or block, ≥15 mm diameter |

**NTC resistance vs. temperature (B = 3500 K):**

| Temperature (°C) | R_NTC (Ω) | I_peak at 530 VAC (A) |
|------------------|-----------|----------------------|
| −30 | ~18 | ~41 |
| 0 | ~14 | ~52 |
| 25 | 10 | ~71 |
| 55 | ~7 | ~98 |

> [!warning] At 55°C ambient, NTC cold resistance drops to ~7 Ω, increasing inrush peak to ~98 A. This is still well below the Type D 63 A breaker magnetic trip (630 A), but self-heating is more aggressive. Verify NTC energy rating covers the hot-ambient worst case.

**Candidate NTC parts:**

| Part | R₂₅ (Ω) | Max Energy (J) | I_max (A) | Notes |
|------|----------|----------------|-----------|-------|
| Ametherm SL32 10R015 | 10 | 150 | 15 A steady | Disc, 32 mm, common in PFC |
| Vishay NTCALUG02A103G | 10 | 80 | — | SMD power NTC, multiple in parallel |
| Amphenol/GE CL-260 | 10 | 120 | 10 A steady | Disc, 25 mm |

The Ametherm SL32 10R015 is preferred for its high energy rating (150 J) and widespread use in 3-phase PFC designs. See [[07-BOM and Cost Analysis]] §4 for NTC and relay cost and procurement details.

### 3.3 Bypass Relay

| Parameter | Value |
|-----------|-------|
| Type | Normally open, 3-pole (or 3 × single-pole) |
| Contact rating | ≥60 A, 600 VAC |
| Coil voltage | 24 VDC (from auxiliary supply) |
| Coil power | ~3 W |
| Contact material | AgSnO₂ (arc-resistant) |
| Mechanical life | ≥100,000 operations |
| Electrical life | ≥10,000 operations at 60 A |

**Candidate relay parts:**

| Part | Rating | Coil | Notes |
|------|--------|------|-------|
| Panasonic HE-D relay (HE1AN-Q-DC24V) | 75 A / 600 VAC, 1-pole | 24 VDC, 2.5 W | Use 3× for 3-pole; compact |
| TE Connectivity LEV200 | 200 A / 900 VDC | 24 VDC, 3 W | Overkill for AC bypass but very robust |
| Hongfa HF2160 | 80 A / 600 VAC, 1-pole | 24 VDC, 2 W | Cost-effective, common in EV chargers |

> [!tip] Three individual single-pole relays (e.g., 3× Panasonic HE1AN) are often preferred over a single 3-pole relay for PCB layout flexibility and availability.

### 3.4 Pre-Charge Timing

The DC bus charges through the NTC-limited bridge rectifier. The time constant depends on the effective NTC resistance and total bus capacitance.

**Simplified RC charging model** (per rail, approximating the 3-phase rectifier as a DC source at ~0.95 × V_LL_peak):

$$\tau = R_{NTC,eff} \times C_{rail} \approx 10 \times 345 \times 10^{-6} = 3.45 \text{ ms}$$

In practice, the 3-phase rectifier charges the bus in pulses (6× per grid cycle at 50 Hz = 3.3 ms between pulses). The bus reaches 90% of the rectified voltage within **~2–3 s** including the pulsed nature of charging and NTC self-heating.

**Pre-charge complete criterion:** V_bus > 90% of expected rectified voltage (V_LL_peak × 0.9 ≈ 675 V at 530 VAC). Firmware monitors V_bus via ADC.

### 3.5 Arc Suppression

When the bypass relay closes, the NTC is carrying current (typically 20–40 A at the moment of bypass). The relay contacts must handle the make-under-load condition. An RC snubber (100 Ω + 47 nF, 630 VAC rated) across each relay contact is recommended to suppress contact arcing and extend relay life.

## 4. Output Contactor

### 4.1 Purpose

The output contactor isolates the DC output bus (150–1000 VDC, 0–100 A) from the vehicle/cable until:
1. The PDU is fully operational (PFC and LLC regulated)
2. The charging session is authorized (via CAN command from charger controller)

> [!info] Physical Location
> The output contactor (and optional pre-charge circuit) is located on the **[[07-PCB-Layout/Power-Entry/__init|Power Entry board]]** (PE-CONT-01), in the DC Output Zone. The contactor coil is driven by the Controller board via signal harness S4.

It also provides **safety disconnect** on fault conditions (OVP, OCP, ground fault) and prevents back-feed from the vehicle battery into the PDU.

### 4.2 Specifications

| Parameter | Requirement |
|-----------|------------|
| Rated voltage | ≥1000 VDC |
| Rated current | ≥100 A continuous |
| Coil voltage | 24 VDC (from auxiliary supply) |
| Coil power | ~5 W |
| Breaking capacity | ≥100 A at 1000 VDC (adequate for fault current) |
| Contact resistance | <1 mΩ (to keep I²R < 10 W at 100 A) |
| Auxiliary contacts | 1 NO (for contactor state verification / welding detection) |
| Mechanical life | ≥100,000 operations |
| Electrical life | ≥10,000 operations at rated current |

**Contact resistance verification:**

$$P_{contact} = I^2 \times R_c = 100^2 \times 0.001 = 10 \text{ W at 100 A}$$

This 10 W is already accounted for in [[04-Thermal Budget]] §2.3 (output contactor: 5 W nominal, up to 10 W at max current).

### 4.3 Candidate Parts

| Part | Voltage | Current | Coil | Contact R | Notes |
|------|---------|---------|------|-----------|-------|
| TE EV200HAANA | 1000 VDC | 200 A | 24 VDC, 4 W | <0.3 mΩ | Industry standard for EV charging; HVIL option |
| Gigavac GX16BA | 1000 VDC | 150 A | 24 VDC, 3 W | <0.5 mΩ | Compact hermetically sealed |
| Panasonic AEV14024 | 900 VDC | 120 A | 24 VDC, 4.5 W | <0.5 mΩ | **Unsuitable** — 900 V < 1000 VDC spec. Listed for reference only; do not use at full output range |

The TE EV200 is the preferred choice for its 1000 VDC rating, low contact resistance, and proven track record in DC fast charging systems.

### 4.4 Output Pre-Charge (Optional)

If the connected vehicle or cable has significant capacitance (>100 µF), closing the output contactor at full LLC output voltage could cause an inrush spike that welds the contactor contacts.

**Mitigation:** A pre-charge resistor (100–500 Ω, 50 W) in parallel with the output contactor via a small auxiliary relay. Sequence: close aux relay → charge vehicle caps through resistor (~100 ms) → close main contactor → open aux relay.

For most CCS/CHAdeMO deployments, cable capacitance is <10 µF and this circuit is unnecessary. **Decision: omit for Rev 1; add if field testing reveals contactor welding.**

### 4.5 Contactor Feedback and Welding Detection

The output contactor must include an auxiliary contact that reports its actual state to the MCU. The firmware verifies:
- **Contactor opens when commanded:** Aux contact should open within 20 ms of coil de-energization. If not → contactor welded → latch fault, alert operator.
- **Contactor does not close unexpectedly:** Aux contact monitored continuously. Unexpected closure → immediate fault.

## 5. Startup Sequence

### 5.1 Timing Diagram

```
Phase:  NTC Pre-charge │ Bypass │ PFC Soft-Start │ LLC Soft-Start │Out│
        ◄── ~3 s ─────►◄ 0.2s ►◄──── 0.8 s ────►◄──── 1.5 s ───►◄──►
 ──────────────────────────────────────────────────────────────────────►
t=0                   t≈3.0   t≈3.2            t≈4.0            t≈5.5 t≈5.7

V_bus   0V ─────────── 675V ──── 800V (regulated) ────────────────────
V_out   0V ────────────────────── 0V ────────── ramp to target ─ target
NTC     [conducting]   [bypassed] ────────────────────────────────────
Relay   [open]         [closed] ──────────────────────────────────────
PFC     [off]          [off]     [soft-start]   [regulating] ────────
LLC     [off]          [off]     [off]          [soft-start]  [reg.] ─
Contactor [open]       [open]    [open]         [open]       [closed]─

                                                                 READY
```

### 5.2 Detailed Sequence

| Step | Time | Action | Criterion / Notes |
|------|------|--------|-------------------|
| **T0** | 0 s | AC power applied. NTC limits inrush. DC bus charges through uncontrolled bridge rectifier. | Auxiliary supply starts from rectified AC (flyback). |
| **T1** | ~0.5 s | Auxiliary 24 V supply stable. MCU boots, HRTIM DLL calibration, ADC self-calibration. | MCU reads V_bus via ADC to monitor pre-charge. |
| **T2** | ~3.0 s | V_bus reaches 90% of V_rectified (~675 V at 530 VAC). Firmware commands bypass relay closed. | Threshold: V_bus > 0.9 × V_in_peak. NTC bypassed. |
| **T3** | ~3.2 s | PFC soft-start begins. SRF-PLL locks to grid (pre-lock ramp ~100 ms). I_d* ramps from 0 to rated over 200 ms (per [[06-Firmware Architecture]] §4.3). DC bus regulated to target (700–920 V). | PLL must achieve lock before current loop enables. |
| **T4** | ~4.0 s | PFC stable and regulating. LLC soft-start begins: f_sw starts at f_max (300 kHz, minimum gain) and ramps down toward f_r (~150 kHz) over 1–1.5 s (per [[06-Firmware Architecture]] §5). | LLC output voltage rises gradually. |
| **T5** | ~5.5 s | LLC output voltage reaches target (within ±2% of setpoint). CC/CV loop takes over. Firmware commands output contactor closed. | Contactor auxiliary contact verified within 20 ms. |
| **T6** | ~5.7 s | System READY. CAN status frame reports RUN state. Charger controller may begin charging session. | Total startup ~5.7 s — within ≤6 s spec with 0.3 s margin. |

> [!note] The ≤6 s budget allocates ~55% to passive NTC pre-charge and ~45% to active PFC/LLC soft-start, with ~0.3 s margin. At lower input voltages (260 VAC), pre-charge is faster (lower V_bus target) but PFC soft-start may take slightly longer due to higher current demand.

## 6. Shutdown and Fault Sequences

### 6.1 Normal Shutdown

Triggered by charger controller (CAN command) or operator.

| Step | Time (relative) | Action |
|------|-----------------|--------|
| 1 | 0 ms | Receive shutdown command. LLC begins frequency ramp toward f_max (reduce output). |
| 2 | 200–500 ms | LLC output current drops to <5 A. Output contactor opens. |
| 3 | 500 ms | PFC disabled (HRTIM outputs idle). DC bus discharges through internal bleed resistors. |
| 4 | 1 s | Bypass relay opens (NTC re-inserted for next startup). |
| 5 | 2–5 s | DC bus bleeds to <60 V (safe voltage per IEC 61851-23). System enters IDLE state. |

### 6.2 Emergency Fault (OCP / OVP)

From [[06-Firmware Architecture]] §7.1 — hardware protection via HRTIM fault inputs, <200 ns response:

| Step | Time | Action |
|------|------|--------|
| 1 | 0 ns | Hardware comparator trips (COMP1–7). HRTIM fault blanking forces all PWM outputs idle. |
| 2 | <200 ns | All switching stops. No further energy delivered to load. |
| 3 | 1 ms | Fault ISR executes. Output contactor commanded open. |
| 4 | 5–15 ms | Output contactor opens (mechanical delay). |
| 5 | 20 ms | PFC disabled. Bypass relay opens. Fault code logged. |
| 6 | — | System latched in FAULT state. Requires manual reset or CAN clear command. |

### 6.3 CAN Timeout

From [[06-Firmware Architecture]] §6.3:

| Condition | Response |
|-----------|----------|
| No command frame for 50 ms | Derate to 50% rated current (gradual ramp-down over 50 ms) |
| No command frame for 200 ms | Full shutdown: LLC off → contactor open → PFC off → FAULT state |

### 6.4 Grid Loss / Phase Loss

From [[06-Firmware Architecture]] §7.2: SRF-PLL detects grid frequency deviation >±5 Hz within 20 ms.

| Step | Time | Action |
|------|------|--------|
| 1 | 0 ms | Phase loss detected by PLL (frequency deviation or V_phase < threshold). |
| 2 | 20 ms | LLC disabled immediately (prevent over-current from unbalanced PFC). |
| 3 | 25 ms | Output contactor opens. |
| 4 | 30 ms | PFC disabled. System enters controlled shutdown. |
| 5 | — | DC bus energy supplies auxiliary supply briefly; bus bleeds down. |

## 7. Auxiliary Power Supply

The auxiliary supply must be operational **before** the main DC bus is established, since it powers the relay coils, contactor coil, gate drivers, and MCU that orchestrate the startup sequence.

### 7.1 Requirements

| Parameter | Value |
|-----------|-------|
| Input source | Rectified AC from input (after EMI filter, before PFC) |
| Output voltages | 24 VDC (relays, contactor, fans) + 12 VDC or 3.3 VDC (MCU, gate drivers) |
| Power budget | See below |
| Startup time | <500 ms from AC applied |
| Topology | Standalone flyback (wide-input, 300–750 VDC from rectified 3-phase) |

### 7.2 Power Budget

| Consumer | Power (W) | Notes |
|----------|----------|-------|
| Bypass relay coil (3-pole) | 3 | From [[04-Thermal Budget]] §2.3 |
| Output contactor coil | 5 | From [[04-Thermal Budget]] §2.3 |
| Gate drivers (6 × STGAP2SiC) | 3 | ~0.5 W each at switching frequency |
| MCU (STM32G474RE + LDOs) | 2 | From [[04-Thermal Budget]] §2.1 |
| CAN transceiver + interface | 0.5 | SN65HVD230 |
| NTC signal conditioning | 0.5 | 4 NTC circuits |
| Fan PWM controller | 1 | Before fans spin up |
| **Minimum startup budget** | **~15 W** | |
| Fans (after startup, 3 × 5 W) | 15 | Full speed; not needed at T0 |
| **Full operating budget** | **~30 W** | |

The existing BOM includes a 30 W auxiliary SMPS module (12/24 V, $15 per [[07-BOM and Cost Analysis]] §9). This is adequate.

### 7.3 Startup Dependency Chain

```
AC Applied → Rectified AC available (~10 ms, first half-cycle)
         → Aux flyback starts → 24V/12V stable (~200–500 ms)
         → MCU boots, ADC/HRTIM init (~100 ms)
         → NTC pre-charge begins (MCU monitors V_bus)
         → ... (remainder of startup sequence per §5)
```

> [!important] The auxiliary supply is the first active circuit in the power-on sequence. Its input must be connected directly to the rectified AC bus (through the NTC + EMI filter path), not from the regulated PFC bus which doesn't exist yet.

## 8. Cold-Start Verification (−30°C)

### 8.1 NTC Behavior at −30°C

At −30°C, the NTC resistance increases to ~18 Ω (from 10 Ω at 25°C). This has two effects:
1. **Lower peak inrush current:** ~41 A vs. ~71 A at 25°C — **safer for breaker coordination**
2. **Slower DC bus charging:** higher R × C time constant

### 8.2 Charging Time Estimate

With R_NTC = 18 Ω at −30°C and C_rail = 345 µF:

$$\tau_{cold} = 18 \times 345 \times 10^{-6} = 6.2 \text{ ms (per pulse)}$$

The 3-phase rectifier delivers ~6 charging pulses per grid cycle (at 50 Hz = 20 ms). Each pulse has a duration of ~3 ms. The bus charges incrementally over many grid cycles.

**Estimated time to 90% of V_rectified at −30°C: ~4–5 s** (vs. ~3 s at 25°C).

This leaves only 1–2 s for PFC + LLC soft-start. The startup budget is tight:

| Phase | Time at 25°C | Time at −30°C | Notes |
|-------|-------------|---------------|-------|
| Aux supply + MCU boot | 0.5 s | 0.7 s | Crystal oscillator may start slower |
| NTC pre-charge | 2.5 s | 4.0 s | Higher NTC resistance |
| PFC soft-start | 0.8 s | 0.8 s | Not temperature-dependent |
| LLC soft-start | 1.5 s | 1.5 s | Not temperature-dependent |
| Contactor close | 0.2 s | 0.2 s | |
| **Total** | **~5.5 s** | **~7.2 s** | **Exceeds 6 s spec at −30°C** |

> [!warning] Cold-start at −30°C may exceed the 6 s startup spec by ~1 s
> **Mitigations (choose one or combine):**
> 1. **Lower the pre-charge threshold** from 90% to 80% of V_rectified at cold start — saves ~1 s. PFC soft-start can manage the remaining bus charging.
> 2. **Use a lower-value NTC** (5 Ω at 25°C, ~9 Ω at −30°C) — faster charging but higher inrush at 55°C ambient (~130 A peak). May need to verify breaker coordination at hot ambient.
> 3. **Accept 7 s at −30°C** — IEC 61851-23 does not specify a hard startup time limit at extreme cold; the 6 s spec is self-imposed.
> 4. **Begin PFC soft-start earlier** (at 70% V_rectified) — PFC control loop can handle the remaining charging while actively regulating. Requires careful tuning of the bus voltage ramp to avoid current overshoot.

### 8.3 Electrolytic Capacitor ESR at −30°C

Electrolytic capacitor ESR increases significantly at low temperatures (typically 3–5× at −30°C vs. 25°C for 125°C-rated parts). This does **not** limit the charging rate (NTC dominates the impedance) but does increase capacitor heating during ripple current after startup. The Nichicon UBY series (125°C rated) specifies ESR at −40°C — verify this value does not cause excessive voltage ripple during initial PFC operation.

### 8.4 Breaker Coordination at −30°C

At −30°C, inrush is ~41 A peak — **less** than the 63 A breaker continuous rating. No risk of nuisance trip at cold start.

## 9. Design Risks and Open Items

| # | Risk / Item | Severity | Status | Mitigation |
|---|-------------|----------|--------|------------|
| 1 | Output contactor welding (inrush into vehicle caps) | Medium | Open | Monitor aux contact; add output pre-charge in Rev 2 if needed |
| 2 | NTC thermal runaway at repeated hot starts (55°C, rapid cycling) | Low | Open | Verify NTC energy rating for 10 starts in 10 min; consider active pre-charge (PFC linear mode) for Rev 2 |
| 3 | Cold-start timing exceeds 6 s at −30°C | Medium | Open | Lower pre-charge threshold or accept extended startup — see §8.2 |
| 4 | Auxiliary supply startup delay at −30°C | Low | Open | Verify flyback startup time with cold electrolytic input caps |
| 5 | Bypass relay contact degradation (arc on make) | Low | Planned | RC snubber across contacts; specify AgSnO₂ contacts |
| 6 | Contactor coil power at cold start (increased coil resistance) | Low | Open | 24 VDC coil at −30°C: copper resistance drops → coil current increases slightly. Verify driver can supply. |
| 7 | NTC derating at 55°C ambient (lower cold resistance) | Low | Open | Verify I²t at R_NTC = 7 Ω, I_peak ≈ 98 A. Breaker still safe (<<630 A magnetic trip). |
| 8 | DC bus bleed-down time after shutdown | Low | Open | Verify V_bus < 60 V within 5 s per IEC 61851-23 §6.3.1. Add active discharge circuit if passive bleed is too slow. |

## 10. References

### Internal Documents

- [[__init]] — PDU specifications: ≤6 s soft-start, −30°C to +55°C, 60 A input, 100 A output
- [[01-Topology Selection]] — Vienna PFC + LLC architecture, DC bus voltage range, inrush note (§3.4)
- [[04-Thermal Budget]] — Relay and contactor power dissipation (§2.3), capacitor thermal limits (§4.3)
- [[05-EMI Filter Design]] — NTC/relay specifications (§7), X-cap values (§4.3), EMI filter BOM (§9)
- [[06-Firmware Architecture]] — Soft-start ramp (§4.3, §7.3), HRTIM fault response (§7.1), CAN timeout (§6.3), PLL phase-loss detection (§7.2)
- [[07-BOM and Cost Analysis]] — DC bus capacitor values (§5), NTC and relay costs (§4), auxiliary supply (§9)
- [[07-PCB-Layout/Power-Entry/__init|Power Entry Board]] — Physical home for NTCs, bypass relays, output contactor (PE-CONT-01)
- [[07-PCB-Layout/00-Board Partitioning]] — 5-board architecture, P1a/P1b/P3a/P3b interface definitions, S4 signal harness

### External Standards and References

- IEC 61851-23 — DC EV charging: system startup, safety disconnect, and de-energization requirements
- IEC 60947-4-1 — Contactor and relay ratings for industrial applications
- EN 60898-1 — MCB trip curves (Type B, C, D definitions)
- TE Connectivity EV200 datasheet — DC contactor specifications
- Ametherm SL32 datasheet — Power NTC thermistor R-T curves and energy ratings

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft |
