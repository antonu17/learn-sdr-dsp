# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Nyquist boundary: the samples retain A*cos(phase), not A and phase separately."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs', type=float, default=48_000, help='Sample rate in samples/s')
parser.add_argument('--f', type=float, default=24_000, help='Tone frequency in Hz')
parser.add_argument('--samples', type=int, default=96)
parser.add_argument('--show', action='store_true')
parser.add_argument('--reference', action='store_true', help='Overlay the original cosine on a dense time grid')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'03-nyquist')
args = parser.parse_args()
if not np.isfinite(args.fs) or args.fs <= 0 or not np.isfinite(args.f) or args.f < 0:
    parser.error('Fs must be positive and f non-negative; both must be finite.')
if args.samples < 4:
    parser.error('Use at least 4 samples.')
if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = np.arange(args.samples)
t = n / args.fs
# This curve comes from the known input formula, not interpolation of samples.
reference_t = None
if args.reference:
    reference_points = max(2001, int(np.ceil(t[-1] * args.f * 80)) + 1)
    if reference_points > 2_000_000:
        parser.error('Reference curve is too large; reduce --samples or --f.')
    reference_t = np.linspace(0, t[-1], reference_points)
phases = np.deg2rad([0, 60, 90])
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True, layout='constrained')
for ax, phase, degrees in zip(axes, phases, [0, 60, 90]):
    x = np.cos(2*np.pi*args.f*t + phase)
    if reference_t is not None:
        reference_x = np.cos(2*np.pi*args.f*reference_t + phase)
        ax.plot(reference_t*1e3, reference_x, color='C1', lw=1.2,
                alpha=.85, label='Original cosine (dense reference)', zorder=1)
    markers, stems, _ = ax.stem(t*1e3, x, linefmt='C0-', markerfmt='C0o', basefmt=' ',
                                label='Samples' if args.reference else None)
    markers.set_zorder(3)
    stems.set_zorder(2)
    if args.reference:
        ax.legend(loc='upper right', fontsize=9)
    ax.set(ylabel='Sample value', ylim=(-1.12, 1.12), title=f'A = 1; phase = {degrees} degrees')
    ax.grid(alpha=.25)
    print(f'phase={degrees:2d} degrees; first 8 samples: {np.array2string(x[:8], precision=6, suppress_small=True)}')
axes[-1].set_xlabel('Time (ms)')
fig.suptitle(f'f = {args.f:g} Hz; Fs = {args.fs:g} samples/s')
args.output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_dir/'nyquist-phases.png', dpi=160)

# Two physically different tones give the same samples exactly at Fs/2.
angle = np.pi*n
a = np.cos(angle + np.pi/3)  # amplitude 1, phase 60 degrees
b = .5*np.cos(angle)        # amplitude 0.5, phase 0 degrees
assert np.allclose(a,b,rtol=0,atol=1e-10)
print(f'At Fs/2: A=1, phase=60° vs A=0.5, phase=0°; max difference={np.max(np.abs(a-b)):.3e}')
# This identity depends on exact Fs/2; slightly below it, all three phases remain observable.
if args.show:
    plt.show()
plt.close(fig)
