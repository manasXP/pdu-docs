#!/usr/bin/env python3
"""
LLC Half-Bridge — ngspice Frequency Sweep
Runs ngspice at multiple frequencies, extracts gain, compares to FHA.
Produces: llc_spice_vs_fha.png
"""

import subprocess
import math
import re
import os
import tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM_DIR = "/Users/manaspradhan/Library/Mobile Documents/iCloud~md~obsidian/Documents/ClaudeNotes/__Workspaces/PDU/sim"

# Design parameters
Lr = 43e-6
Cr = 26e-9
Lm = 258e-6
Ln = Lm / Lr
fr = 1 / (2 * math.pi * math.sqrt(Lr * Cr))
fr2 = fr / math.sqrt(1 + 1/Ln)
Vbus = 750  # design center bus voltage
Vhalf = Vbus / 2

# Operating points to simulate: (Rac, label)
# We'll sweep frequency at a few Rac values
load_cases = [
    (116.7, "600V/10kW (Q=0.35)"),
    (207.5, "800V/10kW (Q=0.20)"),
    (324.2, "1000V/10kW (Q=0.13)"),
    (29.2,  "300V/10kW (Q=1.39)"),
]

# Frequency points (100k to 300k in 20 steps)
fs_points = np.linspace(80e3, 300e3, 45)


def llc_gain_fha(fn, Q, Ln):
    num = fn**2 * (Ln - 1)
    term1 = (fn**2 * Ln - 1)**2
    term2 = fn**2 * (fn**2 - 1)**2 * Ln**2 * Q**2
    denom = math.sqrt(term1 + term2)
    return abs(num / denom) if denom != 0 else float('inf')


def run_ngspice(fsw, Rac):
    """Run a single ngspice transient simulation, return (v_out_rms, v_in_rms)."""
    period = 1.0 / fsw
    halfp = period / 2.0
    # Number of cycles for settling: at least 50 cycles
    n_settle = max(60, int(0.15e-3 * fsw))  # at least 150µs worth
    t_settle = n_settle * period
    t_meas = 20 * period  # measure over 20 cycles
    t_total = t_settle + t_meas
    dt = period / 50  # 50 points per cycle

    netlist = f"""\
* LLC single-point simulation
.title LLC at fs={fsw/1e3:.1f}kHz Rac={Rac:.1f}

Vsq in 0 PULSE(-{Vhalf} {Vhalf} 0 1n 1n {halfp} {period})
L_r in mid 43u IC=0
C_r mid out 26n IC=0
L_m out 0 258u IC=0
R_ac out 0 {Rac}

.tran {dt} {t_total} {t_settle} {dt} UIC

.meas tran v_out_rms RMS V(out) from={t_settle} to={t_total}
.meas tran v_in_rms RMS V(in) from={t_settle} to={t_total}

.end
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False, dir='/tmp') as f:
        f.write(netlist)
        tmpfile = f.name

    try:
        result = subprocess.run(
            ['ngspice', '-b', tmpfile],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr

        v_out = None
        v_in = None
        for line in output.split('\n'):
            if 'v_out_rms' in line.lower() and '=' in line:
                m = re.search(r'=\s*([\d.eE+-]+)', line)
                if m:
                    v_out = float(m.group(1))
            if 'v_in_rms' in line.lower() and '=' in line:
                m = re.search(r'=\s*([\d.eE+-]+)', line)
                if m:
                    v_in = float(m.group(1))

        return v_out, v_in
    except Exception as e:
        return None, None
    finally:
        os.unlink(tmpfile)


# ── Run sweeps ─────────────────────────────────────────────────
print("=" * 70)
print("LLC Half-Bridge — ngspice Time-Domain Frequency Sweep")
print("=" * 70)
print(f"Lr={Lr*1e6:.0f}µH  Cr={Cr*1e9:.0f}nF  Lm={Lm*1e6:.0f}µH  Ln={Ln:.0f}")
print(f"Vbus={Vbus}V  fr={fr/1e3:.1f}kHz  fr2={fr2/1e3:.1f}kHz")
print()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("LLC Gain: ngspice Time-Domain vs FHA Analytical\n"
             f"Lr={Lr*1e6:.0f}µH  Cr={Cr*1e9:.0f}nF  Lm={Lm*1e6:.0f}µH  "
             f"Ln={Ln:.0f}  Vbus={Vbus}V",
             fontsize=12, fontweight='bold')

colors = ['steelblue', 'green', 'darkorange', 'red']
Z0 = math.sqrt(Lr / Cr)

for idx_load, (Rac, label) in enumerate(load_cases):
    Q = Z0 / Rac
    color = colors[idx_load]
    print(f"── {label}  (Rac={Rac:.1f}Ω, Q={Q:.3f}) ──")

    spice_fn = []
    spice_gain = []
    fha_fn_arr = np.linspace(0.5, 2.5, 500)
    fha_gain_arr = [llc_gain_fha(fn, Q, Ln) for fn in fha_fn_arr]

    for i, fsw in enumerate(fs_points):
        fn = fsw / fr
        v_out, v_in = run_ngspice(fsw, Rac)
        if v_out is not None and v_in is not None and v_in > 0:
            gain = v_out / v_in
            spice_fn.append(fn)
            spice_gain.append(gain)
            print(f"  fs={fsw/1e3:6.1f}kHz  fn={fn:.3f}  "
                  f"Vout_rms={v_out:.2f}  Vin_rms={v_in:.2f}  "
                  f"M_spice={gain:.4f}  M_fha={llc_gain_fha(fn, Q, Ln):.4f}")
        else:
            print(f"  fs={fsw/1e3:6.1f}kHz  fn={fn:.3f}  FAILED")

    # Plot on left: all curves
    ax = axes[0]
    ax.plot(fha_fn_arr, fha_gain_arr, '-', color=color, linewidth=1.5,
            label=f'FHA {label}', alpha=0.8)
    if spice_fn:
        ax.plot(spice_fn, spice_gain, 'o', color=color, markersize=4,
                label=f'SPICE {label}', alpha=0.7)

    print()

# Left plot formatting
ax = axes[0]
ax.axvline(x=1.0, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=fr2/fr, color='red', linestyle='--', alpha=0.5, label='ZVS boundary')
ax.set_xlabel("Normalized Frequency fn = fs/fr")
ax.set_ylabel("Voltage Gain M")
ax.set_title("Gain Curves — FHA (lines) vs SPICE (dots)")
ax.set_xlim(0.5, 2.2)
ax.set_ylim(0, 2.0)
ax.legend(fontsize=6, ncol=2)
ax.grid(True, alpha=0.3)

# Right plot: error between FHA and SPICE at design-center load
ax = axes[1]
Rac_dc = 116.7
Q_dc = Z0 / Rac_dc
fha_fn_fine = np.linspace(0.5, 2.5, 500)
fha_gain_fine = [llc_gain_fha(fn, Q_dc, Ln) for fn in fha_fn_fine]

# Re-run SPICE at design center for error plot
spice_fn_dc = []
spice_err = []
for fsw in fs_points:
    fn = fsw / fr
    v_out, v_in = run_ngspice(fsw, Rac_dc)
    if v_out is not None and v_in is not None and v_in > 0:
        gain_spice = v_out / v_in
        gain_fha = llc_gain_fha(fn, Q_dc, Ln)
        if gain_fha > 0.01:
            err_pct = (gain_spice - gain_fha) / gain_fha * 100
            spice_fn_dc.append(fn)
            spice_err.append(err_pct)

if spice_fn_dc:
    ax.plot(spice_fn_dc, spice_err, 'o-', color='steelblue', markersize=5)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between([0.5, 2.5], -5, 5, color='green', alpha=0.1, label='±5% band')

ax.set_xlabel("Normalized Frequency fn = fs/fr")
ax.set_ylabel("SPICE vs FHA Error (%)")
ax.set_title(f"FHA Accuracy — Design Center (Rac={Rac_dc}Ω, Q={Q_dc:.2f})")
ax.set_xlim(0.5, 2.2)
ax.set_ylim(-20, 20)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{SIM_DIR}/llc_spice_vs_fha.png", dpi=150)
print(f"Plot saved: {SIM_DIR}/llc_spice_vs_fha.png")
print()
print("=" * 70)
print("NGSPICE SWEEP COMPLETE")
print("=" * 70)
