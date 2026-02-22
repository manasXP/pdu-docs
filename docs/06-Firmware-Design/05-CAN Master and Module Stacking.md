---
tags: [PDU, firmware, CAN, stacking, master-slave, current-sharing, STM32G474]
created: 2026-02-22
---

# 05 – CAN Master and Module Stacking

> [!note] Scope
> This document covers the **master module firmware**: election, enable sequencing, current redistribution on fault, failover behavior, and diagnostic CAN frames. For CAN physical layer, frame structure, and droop-based current sharing, see [[06-Firmware Architecture]] §6. For fault classification and severity levels referenced here, see [[03-Fault State Machine and Recovery]].

---

## 1. Master Election

### 1.1 v1.0 Policy: Static Election

In v1.0 firmware, the master is determined at power-on by hardware configuration:

| Parameter | Value |
|-----------|-------|
| Election method | Lowest node ID (DIP switch) |
| Node ID range | 0x00–0x0F (4-bit, set by DIP or resistor-coded GPIO) |
| Master node | Node with lowest ID present on bus |
| Dynamic re-election | **Not supported in v1.0** |
| Fallback on master loss | Slaves derate and shutdown (no auto-promotion) |

### 1.2 Discovery Phase

At startup, the master candidate (lowest ID) performs a bus scan:

```
Master candidate (ID=0):
  t=0 ms:    Send DISCOVERY_REQ (broadcast)
  t=0..500:  Collect DISCOVERY_RSP from all nodes
  t=500 ms:  Build module table, assign roles
  t=510 ms:  Send MASTER_ANNOUNCE with module count
```

```c
typedef struct {
    uint8_t  node_id;
    uint8_t  fw_version_major;
    uint8_t  fw_version_minor;
    uint8_t  hw_revision;
    uint16_t power_rating_w;    /* 30000 for standard module */
    uint8_t  state;             /* APP_STANDBY expected */
    bool     present;
} ModuleInfo_t;

#define MAX_MODULES  5
static ModuleInfo_t g_module_table[MAX_MODULES];
static uint8_t      g_num_modules;
static bool         g_is_master;
```

---

## 2. Master State Machine

The master runs an additional FSM layered on top of the application state machine (see [[01-Application State Machine]]).

```
                    ┌───────────┐
                    │   INIT    │  (500 ms bus discovery)
                    └─────┬─────┘
                          │ discovery complete
                          v
                   ┌──────────────┐
                   │  ENABLE_SEQ  │  (sequential module startup)
                   └──────┬───────┘
                          │ all modules in RUN
                          v
                    ┌───────────┐
                    │    RUN    │  (normal current sharing)
                    └─────┬─────┘
                          │ module fault detected
                          v
                   ┌──────────────┐
                   │  FAULT_MGMT  │  (redistribute, notify upstream)
                   └──────┬───────┘
                          │ redistributed OR capacity exceeded
                          v
                    ┌───────────┐      ┌──────────┐
                    │    RUN    │  OR  │ SHUTDOWN  │ (if total capacity < demand)
                    └───────────┘      └──────────┘
```

### 2.1 Master FSM States

| State | Duration | Actions |
|-------|----------|---------|
| INIT | 500 ms | Broadcast DISCOVERY_REQ, collect responses, build module table |
| ENABLE_SEQ | ~1 s (200 ms × N modules) | Send ENABLE_CMD to modules sequentially |
| RUN | Indefinite | Broadcast I_ref/V_ref every 10 ms, monitor status, compute I_avg |
| FAULT_MGMT | < 100 ms | Redistribute current, notify charger controller, log event |
| SHUTDOWN | ~2 s | Sequential disable (LIFO), notify upstream |

---

## 3. Module Enable/Disable Sequencing

### 3.1 Enable Sequence (Ramp-Up)

Modules are enabled one at a time with 200 ms spacing to stagger inrush and prevent bus voltage dip.

```
Time (ms)  0     200    400    600    800   1000
           │      │      │      │      │      │
Module 0   ├──EN──┤──SS──┤─RUN──┤──────┤──────┤
Module 1   │      ├──EN──┤──SS──┤─RUN──┤──────┤
Module 2   │      │      ├──EN──┤──SS──┤─RUN──┤
Module 3   │      │      │      ├──EN──┤──SS──┤─RUN──
Module 4   │      │      │      │      ├──EN──┤──SS──┤─RUN──
           │      │      │      │      │      │
           └──────┴──────┴──────┴──────┴──────┘
                   Total: ~2 s for 5 modules
```

Each module goes through its own `PLL_LOCK → SOFT_START_PFC → SOFT_START_LLC → RUN` sequence internally. The master waits for each module to report `RUN` status before enabling the next.

### 3.2 Disable Sequence (Ramp-Down)

Modules are disabled in **LIFO order** (last enabled, first disabled) with a 30-second minimum on-time to prevent rapid cycling of output contactors.

| Rule | Value | Rationale |
|------|-------|-----------|
| Disable order | LIFO (highest ID first) | Deterministic, avoids contactor wear |
| Minimum on-time | 30 s | Contactor lifecycle (100,000 cycles) |
| Power threshold for disable | P_total < (N−1) × P_rated × 0.85 | 15% hysteresis to prevent module toggling |
| Power threshold for enable | P_total > (N−1) × P_rated × 0.95 | Enable when approaching capacity |

### 3.3 Module Selection Algorithm

```c
void Master_ModuleSelection(float p_demand_w)
{
    uint8_t n_needed = (uint8_t)ceilf(p_demand_w / P_MODULE_RATED);
    if (n_needed > g_num_modules) n_needed = g_num_modules;
    if (n_needed < 1) n_needed = 1;

    /* Enable: lowest ID first */
    for (uint8_t i = 0; i < n_needed; i++) {
        if (g_module_table[i].state != APP_RUN && g_module_table[i].present) {
            if (Module_OnTime(i) == 0 || Module_OnTime(i) > 30000) {
                CAN_SendEnableCmd(g_module_table[i].node_id);
            }
        }
    }

    /* Disable: highest ID first (LIFO) */
    for (int8_t i = g_num_modules - 1; i >= (int8_t)n_needed; i--) {
        if (g_module_table[i].state == APP_RUN) {
            if (Module_OnTime(i) > 30000) {  /* 30 s min on-time */
                CAN_SendDisableCmd(g_module_table[i].node_id);
            }
        }
    }
}
```

---

## 4. Current Redistribution on Fault

When a module reports a fault, the master redistributes its current share among remaining healthy modules.

### 4.1 Worked Example: 5 → 4 Modules

**Initial state:** 5 modules, 100 A total (20 A each), V_out = 750 V

```
Event: Module 4 reports FAULT_PFC_OCP_HW (critical)

Step 1: Master receives fault status from Module 4
  - Module 4 state → FAULT (outputs already idle)
  - N_active: 5 → 4

Step 2: Capacity check
  - Remaining capacity: 4 × 100 A = 400 A (max)
  - Required current: 100 A (current demand)
  - 100 A / 400 A = 25% utilization → OK

Step 3: Redistribute
  - New I_ref per module: 100 A / 4 = 25 A each
  - ΔI per module: +5 A (25% increase)
  - Ramp time: apply over 100 ms (50 A/s ramp rate)

Step 4: Notify charger controller
  - Send PDU_Fault frame: fault_type=PFC_OCP, module_id=4
  - Update PDU_Status: N_active=4, P_available=120 kW
```

### 4.2 Capacity Exceeded Scenario

If the remaining modules cannot supply the demanded current:

```
Event: Module 3 also faults (3 modules remain)

Remaining capacity: 3 × 100 A = 300 A
Demanded current: 133 A at 750 V (100 kW session)

300 A > 133 A → still OK, but power limited to 90 kW

If demand were 400 A at 375 V (150 kW session):
  300 A < 400 A → OVER-CAPACITY
  Action: Notify charger controller to renegotiate with vehicle
          (reduce I_target to 300 A via OCPP/ISO 15118)
```

### 4.3 Redistribution Pseudocode

```c
void Master_Redistribute(void)
{
    /* Count active (RUN or DERATE) modules */
    uint8_t n_active = 0;
    for (uint8_t i = 0; i < g_num_modules; i++) {
        if (g_module_table[i].state == APP_RUN ||
            g_module_table[i].state == APP_DERATE) {
            n_active++;
        }
    }

    if (n_active == 0) {
        /* All modules faulted — emergency shutdown */
        CAN_SendUpstream_SystemFault();
        return;
    }

    /* Calculate new per-module reference */
    float i_total = g_charger_setpoint.i_target;
    float i_per_module = i_total / (float)n_active;

    /* Check capacity */
    float i_max_total = (float)n_active * I_MODULE_MAX;
    if (i_total > i_max_total) {
        /* Over-capacity: clamp and notify */
        i_per_module = I_MODULE_MAX;
        CAN_SendUpstream_CapacityReduced(i_max_total);
    }

    /* Broadcast updated setpoint */
    g_master_cmd.i_ref = i_per_module;
    CAN_BroadcastCommand(&g_master_cmd);

    /* Log redistribution event */
    EventLog_Write(EVT_REDISTRIBUTE, n_active, i_per_module);
}
```

---

## 5. Failover Behavior (v1.0)

### 5.1 Slave Behavior on Master Loss

| Elapsed Time | Slave Action |
|-------------|-------------|
| 0–50 ms | Normal operation (within CAN jitter budget) |
| 50 ms | Derate to 50% rated current |
| 200 ms | Controlled shutdown (SHUTDOWN state) |

### 5.2 No Auto-Promotion (v1.0 Limitation)

In v1.0, if the master module fails, no slave promotes itself to master. This is a deliberate simplification:
- Avoids split-brain scenarios
- Simplifies CAN arbitration
- Master module should be physically accessible for replacement

> [!warning] v2.0 consideration
> Future firmware should implement master auto-promotion: second-lowest node ID takes over after 500 ms master absence, re-discovers remaining modules, and resumes operation. This requires a consensus protocol to prevent split-brain.

### 5.3 Master Self-Monitoring

The master monitors its own health. If the master's power stage faults, it continues running the master FSM (CAN coordination) while its own power outputs are disabled:

```c
void Master_SelfFault(uint8_t fault_id)
{
    /* Disable own power stage */
    Fault_Enter(fault_id);

    /* Continue master role — redistribute among remaining slaves */
    g_module_table[g_self_id].state = APP_FAULT;
    Master_Redistribute();

    /* Master FSM continues running in main loop */
    /* (CAN broadcast, module monitoring still active) */
}
```

---

## 6. Diagnostic CAN Frames

Extended frames for commissioning, debugging, and field service.

### 6.1 Frame Definitions

| Message ID | Name | Direction | DLC | Rate |
|-----------|------|-----------|-----|------|
| 0x700 + NodeID | DISCOVERY_REQ | Master → All | 0 | On demand |
| 0x710 + NodeID | DISCOVERY_RSP | Slave → Master | 8 | On demand |
| 0x720 + NodeID | FAULT_LOG_REQ | Master → Slave | 2 | On demand |
| 0x730 + NodeID | FAULT_LOG_RSP | Slave → Master | 8 | On demand (multi-frame) |
| 0x740 + NodeID | FW_VERSION_REQ | Master → Slave | 0 | On demand |
| 0x750 + NodeID | FW_VERSION_RSP | Slave → Master | 8 | On demand |
| 0x760 + NodeID | CAL_DATA_REQ | Master → Slave | 2 | On demand |
| 0x770 + NodeID | CAL_DATA_RSP | Slave → Master | 8 | On demand |
| 0x780 | DIAG_CLEAR_FAULTS | Master → All | 1 | On demand |

### 6.2 Fault Log Read-Out Protocol

```
Master                              Slave (Node 3)
  │                                     │
  ├── FAULT_LOG_REQ (start_idx=0) ────> │
  │                                     │
  │ <── FAULT_LOG_RSP (entries 0-3) ──  │  (4 × 12 bytes, fragmented)
  │ <── FAULT_LOG_RSP (entries 4-7) ──  │
  │ <── FAULT_LOG_RSP (entries 8-11) ── │
  │ <── FAULT_LOG_RSP (count=0, END) ── │  (no more entries)
  │                                     │
```

Each response carries up to 4 `FaultLogEntry_t` entries (48 bytes). CAN FD data phase (64-byte payload) accommodates this; for classic CAN 2.0 (8-byte payload), entries are sent one per frame.

### 6.3 FW Version Response

```c
/* FW_VERSION_RSP payload (8 bytes) */
typedef struct __attribute__((packed)) {
    uint8_t  fw_major;       /* e.g., 1 */
    uint8_t  fw_minor;       /* e.g., 0 */
    uint16_t fw_build;       /* e.g., 142 */
    uint8_t  hw_revision;    /* PCB revision (A=1, B=2, ...) */
    uint8_t  node_id;
    uint16_t power_rating;   /* Watts / 100 (e.g., 300 = 30 kW) */
} FwVersionRsp_t;
```

---

## 7. Stacking Startup Timing Diagram

Complete system startup from AC power-on to 150 kW delivery (5 modules):

```
Time (s) 0    0.5    1.0    1.5    2.0    2.5    3.0    3.5    4.0    5.0    6.0
         │     │      │      │      │      │      │      │      │      │      │
Master   ├─INIT┤─DISC─┤                                                       │
         │     │500ms │                                                        │
         │     │      ├──ENABLE_SEQ────────────────────┤                       │
         │     │      │                                │                       │
Mod 0    │     │      ├─EN──┤─PLL─┤─PFC─┤─LLC─┤──RUN──┤──────────────────────│
Mod 1    │     │      │     ├─EN──┤─PLL─┤─PFC─┤─LLC─┤─RUN─┤                  │
Mod 2    │     │      │     │     ├─EN──┤─PLL─┤─PFC─┤─LLC─┤─RUN─┤            │
Mod 3    │     │      │     │     │     ├─EN──┤─PLL─┤─PFC─┤─LLC─┤─RUN─┤      │
Mod 4    │     │      │     │     │     │     ├─EN──┤─PLL─┤─PFC─┤─LLC─┤─RUN──│
         │     │      │     │     │     │     │     │     │     │      │      │
         └─────┴──────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──────┴──────┘
                Total system startup: ~5-6 s (individual module ~3 s + stagger)
```

---

## 8. Pseudocode: `Master_ModuleControl_Tick()`

Called at 100 Hz (10 ms) from main loop when `g_is_master == true`.

```c
typedef enum {
    MASTER_INIT       = 0,
    MASTER_ENABLE_SEQ = 1,
    MASTER_RUN        = 2,
    MASTER_FAULT_MGMT = 3,
    MASTER_SHUTDOWN   = 4,
} MasterState_t;

static MasterState_t g_master_state = MASTER_INIT;
static uint8_t       g_enable_idx;

void Master_ModuleControl_Tick(void)
{
    uint32_t now = HAL_GetTick();

    /* Process incoming status frames from all modules */
    Master_ProcessStatusFrames();

    switch (g_master_state) {

    case MASTER_INIT:
        /* Discovery phase: broadcast and collect */
        if (!g_discovery_sent) {
            CAN_SendDiscoveryReq();
            g_discovery_sent = true;
            g_discovery_start = now;
        }
        if ((now - g_discovery_start) >= 500) {
            g_num_modules = Master_CountPresent();
            if (g_num_modules > 0) {
                g_enable_idx = 0;
                g_master_state = MASTER_ENABLE_SEQ;
            }
        }
        break;

    case MASTER_ENABLE_SEQ:
        /* Enable modules one by one, 200 ms apart */
        if (g_enable_idx < g_num_modules) {
            ModuleInfo_t *m = &g_module_table[g_enable_idx];
            if (m->state == APP_STANDBY) {
                CAN_SendEnableCmd(m->node_id);
                m->state = APP_PLL_LOCK;  /* expected next state */
            } else if (m->state == APP_RUN) {
                /* Module started successfully, enable next after 200 ms */
                g_enable_idx++;
                g_enable_timer = now;
            }
            /* Wait 200 ms between enables */
            if (g_enable_idx > 0 && (now - g_enable_timer) < 200) {
                break;  /* wait */
            }
        } else {
            /* All modules running */
            g_master_state = MASTER_RUN;
        }
        break;

    case MASTER_RUN:
        /* Normal operation: broadcast setpoints every 10 ms */
        Master_ComputeCurrentSharing();
        CAN_BroadcastCommand(&g_master_cmd);
        Master_ModuleSelection(g_charger_setpoint.p_demand);

        /* Check for module faults */
        for (uint8_t i = 0; i < g_num_modules; i++) {
            if (g_module_table[i].state == APP_FAULT &&
                g_module_table[i].prev_state != APP_FAULT) {
                g_master_state = MASTER_FAULT_MGMT;
                break;
            }
        }
        break;

    case MASTER_FAULT_MGMT:
        Master_Redistribute();
        /* Return to RUN (with fewer modules) or SHUTDOWN */
        uint8_t n_active = Master_CountActive();
        if (n_active > 0) {
            g_master_state = MASTER_RUN;
        } else {
            g_master_state = MASTER_SHUTDOWN;
            CAN_SendUpstream_SystemFault();
        }
        break;

    case MASTER_SHUTDOWN:
        /* Disable modules in LIFO order */
        for (int8_t i = g_num_modules - 1; i >= 0; i--) {
            if (g_module_table[i].state == APP_RUN) {
                CAN_SendDisableCmd(g_module_table[i].node_id);
                break;  /* one at a time */
            }
        }
        if (Master_CountActive() == 0) {
            CAN_SendUpstream_SystemOff();
        }
        break;
    }
}
```

---

## References

- [[06-Firmware Architecture]] — CAN physical layer (§6.1), frame structure (§6.2), current sharing strategy (§6.3)
- [[01-Application State Machine]] — State definitions, CAN timeout transitions (this sub-folder)
- [[03-Fault State Machine and Recovery]] — Fault severity classification, fault log structure (this sub-folder)

---

## Revision History

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| 0.1 | 2026-02-22 | Manas Pradhan | Initial draft — static master, 5-module stacking |
