# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This workspace documents the design of a **30 kW Power Delivery Unit (PDU)** for DC fast EV charging. It is a hardware/power electronics project with an embedded firmware component. The primary deliverables are specifications, research notes, design documentation (Obsidian markdown), and STM32G474RE firmware (C).

## Key Specifications (from `__init.md`)

- **Input:** 3-phase 260–530 VAC, up to 60 A, PF ≥0.99
- **Output:** 150–1000 VDC, 0–100 A, 30 kW constant power
- **Efficiency:** >96% peak; SiC-based designs preferred (>98%)
- **Stacking:** 5 modules via CAN bus → 150 kW total
- **Standards:** IEC 61851-23, UL 2202, CE; OCPP 1.6, ISO 15118

## Repositories

| Repo | Local Path | GitHub |
|------|-----------|--------|
| **pdu-docs** | This workspace (Obsidian vault) | https://github.com/manasXP/pdu-docs |
| **pdu-firmware** | `~/Documents/pdu-firmware` | https://github.com/manasXP/pdu-firmware |

The firmware repo includes `pdu-docs` as a git submodule at `docs/`.

## Workspace Structure

| Path | Purpose |
|------|---------|
| `__init.md` | Project definition and full specifications |
| `docs/` | Structured design documentation |
| `research/` | Research notes, component evaluations, reference designs |
| `CLAUDE.md` | This file — workspace context for Claude Code |

## Firmware Structure (`~/Documents/pdu-firmware`)

| Path | Purpose |
|------|---------|
| `Core/` | STM32 HAL/LL init, main.c, system config |
| `App/StateMachine/` | 10-state application FSM |
| `App/Control/` | PFC dq-frame control, LLC PFM, PI controllers |
| `App/ADC/` | ADC pipeline, DMA, software filters |
| `App/Protection/` | Fault state machine, HRTIM fault inputs, thermal derating |
| `App/CAN/` | CAN protocol, master FSM, 5-module stacking |
| `App/PowerSequence/` | Soft-start, shutdown, burst mode |
| `App/Diagnostics/` | UART CLI, fault logging, calibration |
| `Drivers/` | STM32G4 HAL/LL drivers (vendor) |
| `Makefile` | ARM GCC build (`make all`, `make flash`, `make lint`) |

## Working in This Workspace

- Follow the Obsidian conventions from the vault-level `CLAUDE.md` (wiki links, tags, frontmatter)
- Use `docs/` for structured deliverables (topology analysis, BOM, schematics, control design)
- Use `research/` for component datasheets summaries, vendor comparisons, reference design notes
- Link between notes with `[[Note Name]]` to build a connected knowledge graph
- When creating new notes, consider numbered prefixes in `docs/` for ordering (e.g., `01-Topology/`, `02-Control/`)

## Domain Context

Key technical domains involved:
- **Power electronics:** Vienna rectifier / 3-phase PFC, LLC or phase-shifted full-bridge DC-DC, SiC MOSFETs
- **Control:** Digital control (DSP/MCU), CC/CV charging modes, soft-start, current sharing
- **Communications:** CAN bus (inter-module), OCPP 1.6 (cloud), ISO 15118 (vehicle)
- **Thermal:** Forced-air cooling, thermal derating above 55°C
- **Safety/EMC:** Surge, OVP, OCP, OTP, short-circuit protection; EN 61000-series EMC
