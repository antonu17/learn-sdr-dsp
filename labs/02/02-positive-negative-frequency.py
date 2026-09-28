# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Compare positive and negative complex frequencies."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs', type=float, default=8_000, help='Sample rate, samples/s')
parser.add_argument('--f', type=float, default=1_000, help='Positive frequency magnitude, Hz')
parser.add_argument('--samples', type=int, default=17)
parser.add_argument('--index', type=int, default=3, help='Sample highlighted on complex planes')
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'02-positive-negative-frequency')
args = parser.parse_args()

if not np.isfinite(args.fs) or args.fs <= 0:
    parser.error('--fs must be positive and finite.')
if not np.isfinite(args.f) or not 0 < args.f < args.fs/2:
    parser.error('--f must be between 0 and Fs/2.')
if args.samples < 2:
    parser.error('--samples must be at least 2.')
if not 0 <= args.index < args.samples:
    parser.error('--index must be between 0 and samples-1.')

if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = np.arange(args.samples)
theta = 2*np.pi*args.f*n/args.fs
z_positive = np.exp(1j*theta)
z_negative = np.exp(-1j*theta)

assert np.allclose(z_negative, np.conj(z_positive))
assert np.allclose(z_positive.real, z_negative.real)
assert np.allclose(z_positive.imag, -z_negative.imag)

k = args.index
circle = np.linspace(0, 2*np.pi, 600)
fig, axes = plt.subplots(2, 2, figsize=(11, 9), layout='constrained')

for ax, z, title, color in (
    (axes[0,0], z_positive, '+f: counter-clockwise', 'C0'),
    (axes[0,1], z_negative, '-f: clockwise', 'C1'),
):
    ax.plot(np.cos(circle), np.sin(circle), color='0.78')
    ax.plot(z.real, z.imag, 'o-', color=color, alpha=.55, ms=4)
    ax.arrow(0, 0, z[k].real, z[k].imag, width=.012, length_includes_head=True, color=color)
    ax.plot(z[k].real, z[k].imag, 'o', color=color, ms=8)
    ax.axhline(0,color='0.72',lw=1); ax.axvline(0,color='0.72',lw=1)
    ax.set(xlim=(-1.15,1.15),ylim=(-1.15,1.15),aspect='equal',xlabel='I',ylabel='Q',title=title)
    ax.grid(alpha=.2)

axes[1,0].plot(n, z_positive.real, 'o-', label='Re{z+} = cos(theta)', color='C0')
axes[1,0].plot(n, z_negative.real, 'x--', label='Re{z-} = cos(-theta)', color='C1')
axes[1,0].set(xlabel='Sample n',ylabel='I',title='Real parts coincide exactly')
axes[1,0].grid(alpha=.25); axes[1,0].legend()

axes[1,1].plot(n, np.unwrap(np.angle(z_positive)), 'o-', label='angle(z+)', color='C0')
axes[1,1].plot(n, np.unwrap(np.angle(z_negative)), 'x--', label='angle(z-)', color='C1')
axes[1,1].set(xlabel='Sample n',ylabel='Unwrapped phase, rad',title='Opposite phase slopes')
axes[1,1].grid(alpha=.25); axes[1,1].legend()

step_deg = 360*args.f/args.fs
fig.suptitle(f'Positive and negative complex frequency: f={args.f:g} Hz, Fs={args.fs:g}, step=±{step_deg:g}°/sample')

print(f'Phase step: +{step_deg:g} deg/sample and -{step_deg:g} deg/sample')
print('   n   angle +f   angle -f        I(+f)       Q(+f)        I(-f)       Q(-f)')
for idx in range(min(8,args.samples)):
    print(f'{idx:4d} {np.degrees(theta[idx]):10.3f} {-np.degrees(theta[idx]):10.3f} '
          f'{z_positive[idx].real:12.6f} {z_positive[idx].imag:12.6f} '
          f'{z_negative[idx].real:12.6f} {z_negative[idx].imag:12.6f}')
print(f'\nmax |Re(z+) - Re(z-)| = {np.max(np.abs(z_positive.real-z_negative.real)):.3e}')
print(f'max |z- - conj(z+)|   = {np.max(np.abs(z_negative-np.conj(z_positive))):.3e}')

args.output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_dir/'positive-negative-frequency.png', dpi=160)
if args.show:
    plt.show()
plt.close(fig)
