#!/usr/bin/env python3
"""
LLC Resonant Converter — FHA Gain Curve Analysis
PDU 30 kW DC-DC Stage (per phase: 10 kW)

Parameters from 02-Magnetics Design.md:
  Lr = 43 µH, Cr = 26 nF, Lm = 258 µH
  n = 2 (Ns/Np), fr = 150 kHz
  Ln = Lm/Lr = 6, Q varies with load

Outputs:
  1. Gain curves M(fn) at multiple Q values
  2. Gain at each operating point (200–1000 V)
  3. ZVS boundary check
  4. Saved plot: llc_gain_curves.png
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Design Parameters ──────────────────────────────────────────────
Lr = 43e-6       # resonant inductance (H)
Cr = 26e-9       # resonant capacitance (F)
Lm = 258e-6      # magnetizing inductance (H)
n  = 2.0         # turns ratio Ns/Np
Po_phase = 10e3  # power per phase (W)

Ln = Lm / Lr     # inductance ratio
fr = 1 / (2 * math.pi * math.sqrt(Lr * Cr))  # series resonant freq
Z0 = math.sqrt(Lr / Cr)                       # characteristic impedance
fr2 = fr / math.sqrt(1 + 1/Ln)                # parallel resonant freq

print("=" * 65)
print("LLC Resonant Tank — FHA Gain Curve Verification")
print("=" * 65)
print(f"Lr  = {Lr*1e6:.1f} µH")
print(f"Cr  = {Cr*1e9:.1f} nF")
print(f"Lm  = {Lm*1e6:.0f} µH")
print(f"Ln  = Lm/Lr = {Ln:.2f}")
print(f"n   = {n:.1f}")
print(f"Z0  = {Z0:.2f} Ω")
print(f"fr  = {fr/1e3:.1f} kHz  (series resonance)")
print(f"fr2 = {fr2/1e3:.1f} kHz  (parallel resonance — ZVS boundary)")
print()


# ── LLC Gain Function ──────────────────────────────────────────────
def llc_gain(fn, Q, Ln):
    """
    FHA voltage gain of LLC resonant converter.
    fn = fs/fr (normalized frequency)
    Q  = Z0 / Rac
    Ln = Lm / Lr
    """
    num = fn**2 * (Ln - 1)
    term1 = (fn**2 * Ln - 1)**2
    term2 = fn**2 * (fn**2 - 1)**2 * Ln**2 * Q**2
    denom = math.sqrt(term1 + term2)
    if denom == 0:
        return float('inf')
    return abs(num / denom)


def llc_gain_array(fn_arr, Q, Ln):
    return np.array([llc_gain(f, Q, Ln) for f in fn_arr])


# ── Operating Points ───────────────────────────────────────────────
# (Vo, Po_phase, Vbus) — from 02-Magnetics Design §2.3
operating_points = [
    ("200 V (min, derated)",   200,  6667, 650),
    ("300 V (low, 10 kW)",     300, 10000, 700),
    ("400 V (mid-low)",        400, 10000, 700),
    ("600 V (design center)",  600, 10000, 750),
    ("800 V (nominal)",        800, 10000, 800),
    ("1000 V (max)",          1000, 10000, 850),
]

print("── Operating Point Verification ─────────────────────────────")
print(f"{'Point':<26} {'Vo':>5} {'Vbus':>5} {'M_req':>6} {'Rac':>7}"
      f" {'Q':>6} {'fn_est':>7} {'fs_est':>8} {'M_actual':>9}")
print("-" * 95)

op_results = []
for label, Vo, Po, Vbus in operating_points:
    M_req = Vo / (n * Vbus / 2)
    Rac = (8 * n**2 / math.pi**2) * (Vo**2 / Po)
    Q_op = Z0 / Rac

    # Find fn that gives M = M_req by numerical search
    fn_search = np.linspace(0.5, 3.0, 10000)
    gains = llc_gain_array(fn_search, Q_op, Ln)
    idx = np.argmin(np.abs(gains - M_req))
    fn_found = fn_search[idx]
    M_actual = gains[idx]
    fs_found = fn_found * fr

    op_results.append({
        'label': label, 'Vo': Vo, 'Po': Po, 'Vbus': Vbus,
        'M_req': M_req, 'Rac': Rac, 'Q': Q_op,
        'fn': fn_found, 'fs': fs_found, 'M_actual': M_actual
    })

    zvs_ok = "ZVS" if fn_found > fr2/fr else "NO-ZVS"
    print(f"{label:<26} {Vo:>5} {Vbus:>5} {M_req:>6.3f} {Rac:>7.1f}"
          f" {Q_op:>6.3f} {fn_found:>7.3f} {fs_found/1e3:>7.1f}k {M_actual:>9.3f}"
          f"  {zvs_ok}")

print()

# ── ZVS Boundary Analysis ─────────────────────────────────────────
print("── ZVS Boundary Check ───────────────────────────────────────")
fn_zvs_limit = fr2 / fr
print(f"ZVS lost below fn = {fn_zvs_limit:.4f}  (fs = {fr2/1e3:.1f} kHz)")
print()

for r in op_results:
    margin = (r['fn'] - fn_zvs_limit) / fn_zvs_limit * 100
    status = "OK" if r['fn'] > fn_zvs_limit else "WARNING — ZVS LOST"
    print(f"  {r['label']:<26}  fn = {r['fn']:.3f}  "
          f"margin = {margin:+.1f}%  [{status}]")

# Check the 1000V point more carefully
print()
r1000 = [r for r in op_results if r['Vo'] == 1000][0]
if r1000['fn'] < fn_zvs_limit * 1.05:
    print("  ⚠  1000 V point has <5% margin to ZVS boundary!")
    print("     Mitigations: raise Vbus_max to 870 V, or reduce Ln to 5")
    # Calculate with Vbus = 870
    M_870 = 1000 / (n * 870 / 2)
    print(f"     At Vbus=870V: M_req = {M_870:.3f} → more margin")

print()

# ── Peak Gain Capability ──────────────────────────────────────────
print("── Peak Gain (M_max) at Key Q Values ────────────────────────")
fn_fine = np.linspace(0.5, 3.0, 20000)
for Q_test in [0.1, 0.2, 0.35, 0.5, 1.0, 1.5, 2.0]:
    gains_test = llc_gain_array(fn_fine, Q_test, Ln)
    M_max = np.max(gains_test)
    fn_at_max = fn_fine[np.argmax(gains_test)]
    print(f"  Q = {Q_test:.2f}  →  M_max = {M_max:.3f}  at fn = {fn_at_max:.3f}"
          f"  (fs = {fn_at_max*fr/1e3:.0f} kHz)")

print()

# ── Plot 1: Gain Curves for Multiple Q ────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("LLC Resonant Converter — FHA Gain Curve Verification\n"
             f"Lr={Lr*1e6:.0f}µH  Cr={Cr*1e9:.0f}nF  Lm={Lm*1e6:.0f}µH  "
             f"Ln={Ln:.1f}  n={n:.0f}  fr={fr/1e3:.0f}kHz",
             fontsize=12, fontweight='bold')

# Top-left: M vs fn for multiple Q
ax = axes[0, 0]
fn_plot = np.linspace(0.55, 2.5, 2000)
q_values = [0.1, 0.2, 0.35, 0.5, 0.8, 1.0, 1.5, 2.0]
colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(q_values)))

for Q_val, color in zip(q_values, colors):
    M_plot = llc_gain_array(fn_plot, Q_val, Ln)
    ax.plot(fn_plot, M_plot, color=color, linewidth=1.5, label=f"Q={Q_val:.2f}")

ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='M=1 (resonance)')
ax.axvline(x=1.0, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=fn_zvs_limit, color='red', linestyle='--', alpha=0.7, label=f'ZVS limit (fn={fn_zvs_limit:.3f})')
ax.set_xlabel("Normalized Frequency fn = fs/fr")
ax.set_ylabel("Voltage Gain M")
ax.set_title("Gain Curves — M(fn) at Various Q")
ax.set_ylim(0, 2.5)
ax.set_xlim(0.55, 2.5)
ax.legend(fontsize=7, ncol=2)
ax.grid(True, alpha=0.3)

# Top-right: Operating points on the gain plane
ax = axes[0, 1]
for Q_val in [0.13, 0.20, 0.35, 0.79, 1.40, 2.10]:
    M_plot = llc_gain_array(fn_plot, Q_val, Ln)
    ax.plot(fn_plot, M_plot, linewidth=1, alpha=0.4, color='steelblue')

for r in op_results:
    marker = 'o' if r['fn'] > fn_zvs_limit else 'x'
    color = 'green' if r['fn'] > fn_zvs_limit * 1.05 else ('orange' if r['fn'] > fn_zvs_limit else 'red')
    ax.plot(r['fn'], r['M_actual'], marker, color=color, markersize=10, markeredgewidth=2)
    ax.annotate(f"{r['Vo']}V", (r['fn'], r['M_actual']),
                textcoords="offset points", xytext=(8, 5), fontsize=8)

ax.axvline(x=fn_zvs_limit, color='red', linestyle='--', alpha=0.7, label='ZVS boundary')
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=1.0, color='gray', linestyle=':', alpha=0.5)
ax.set_xlabel("Normalized Frequency fn = fs/fr")
ax.set_ylabel("Voltage Gain M")
ax.set_title("Operating Points on Gain Plane")
ax.set_ylim(0, 2.0)
ax.set_xlim(0.55, 2.5)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Bottom-left: Switching frequency vs output voltage
ax = axes[1, 0]
vo_list = [r['Vo'] for r in op_results]
fs_list = [r['fs']/1e3 for r in op_results]
ax.plot(vo_list, fs_list, 'o-', color='steelblue', linewidth=2, markersize=8)
ax.axhline(y=fr/1e3, color='green', linestyle='--', alpha=0.7, label=f'fr = {fr/1e3:.0f} kHz')
ax.axhline(y=fr2/1e3, color='red', linestyle='--', alpha=0.7, label=f'fr2 = {fr2/1e3:.0f} kHz (ZVS limit)')
ax.axhline(y=300, color='orange', linestyle=':', alpha=0.5, label='fs_max = 300 kHz')
ax.axhline(y=100, color='orange', linestyle=':', alpha=0.5, label='fs_min = 100 kHz')
ax.fill_between([150, 1050], fr2/1e3, fr2/1e3*0.9, color='red', alpha=0.1)
ax.set_xlabel("Output Voltage Vo (V)")
ax.set_ylabel("Switching Frequency fs (kHz)")
ax.set_title("Switching Frequency vs Output Voltage")
ax.set_xlim(150, 1050)
ax.set_ylim(80, 320)
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Bottom-right: Q factor vs output voltage
ax = axes[1, 1]
q_list = [r['Q'] for r in op_results]
ax.plot(vo_list, q_list, 's-', color='darkorange', linewidth=2, markersize=8)
ax.set_xlabel("Output Voltage Vo (V)")
ax.set_ylabel("Quality Factor Q")
ax.set_title("Load Q vs Output Voltage")
ax.set_xlim(150, 1050)
ax.grid(True, alpha=0.3)

# Add Rac on secondary y-axis
ax2 = ax.twinx()
rac_list = [r['Rac'] for r in op_results]
ax2.plot(vo_list, rac_list, '^--', color='purple', linewidth=1.5, markersize=6, alpha=0.7)
ax2.set_ylabel("Rac (Ω)", color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

plt.tight_layout()
out_dir = "/Users/manaspradhan/Library/Mobile Documents/iCloud~md~obsidian/Documents/ClaudeNotes/__Workspaces/PDU/sim"
plt.savefig(f"{out_dir}/llc_gain_curves.png", dpi=150)
print(f"Plot saved: {out_dir}/llc_gain_curves.png")

# ── Plot 2: Detailed ZVS Region ──────────────────────────────────
fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
fn_detail = np.linspace(0.85, 1.15, 2000)

for Q_val, color in zip([0.13, 0.20, 0.35], ['blue', 'green', 'orange']):
    M_det = llc_gain_array(fn_detail, Q_val, Ln)
    ax.plot(fn_detail, M_det, color=color, linewidth=2, label=f"Q={Q_val:.2f}")

ax.axvline(x=fn_zvs_limit, color='red', linewidth=2, linestyle='--', label=f'ZVS boundary fn={fn_zvs_limit:.4f}')
ax.axvline(x=1.0, color='gray', linestyle=':', alpha=0.5, label='fn=1 (resonance)')

# Mark 800V and 1000V points
for r in op_results:
    if r['Vo'] in [800, 1000]:
        ax.plot(r['fn'], r['M_actual'], 'o', markersize=12, markeredgewidth=2,
                markeredgecolor='black', markerfacecolor='yellow')
        ax.annotate(f"{r['Vo']}V\nfn={r['fn']:.3f}\nfs={r['fs']/1e3:.0f}kHz",
                    (r['fn'], r['M_actual']),
                    textcoords="offset points", xytext=(15, -10), fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='black'))

ax.set_xlabel("Normalized Frequency fn = fs/fr", fontsize=12)
ax.set_ylabel("Voltage Gain M", fontsize=12)
ax.set_title("LLC Gain — ZVS Region Detail (800V–1000V Operating Points)\n"
             f"Lr={Lr*1e6:.0f}µH  Lm={Lm*1e6:.0f}µH  Ln={Ln:.0f}  fr={fr/1e3:.0f}kHz",
             fontsize=11)
ax.set_ylim(0.8, 1.5)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{out_dir}/llc_zvs_detail.png", dpi=150)
print(f"Plot saved: {out_dir}/llc_zvs_detail.png")

# ── Sensitivity: Ln = 5 alternative ──────────────────────────────
print()
print("── Sensitivity: Ln = 5 (alternative) ────────────────────────")
Ln5 = 5
Lm5 = Ln5 * Lr
fr2_5 = fr / math.sqrt(1 + 1/Ln5)
print(f"  Lm = {Lm5*1e6:.0f} µH, fr2 = {fr2_5/1e3:.1f} kHz")

for r in op_results:
    if r['Vo'] in [800, 1000]:
        gains5 = llc_gain_array(fn_search, r['Q'], Ln5)
        idx5 = np.argmin(np.abs(gains5 - r['M_req']))
        fn5 = fn_search[idx5]
        margin5 = (fn5 - fr2_5/fr) / (fr2_5/fr) * 100
        print(f"  {r['Vo']}V: fn={fn5:.3f}, fs={fn5*fr/1e3:.0f} kHz, "
              f"ZVS margin={margin5:+.1f}%")

print()
print("=" * 65)
print("VERIFICATION COMPLETE")
print("=" * 65)
