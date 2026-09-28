# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Complex tone: one rotating vector, two coordinates I and Q."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs', type=float, default=48_000, help='Sample rate, samples/s')
parser.add_argument('--f', type=float, default=1_000, help='Tone frequency, Hz')
parser.add_argument('--amplitude', type=float, default=1.0)
parser.add_argument('--phase-deg', type=float, default=0.0, help='Initial phase in degrees')
parser.add_argument('--samples', type=int, default=96)
parser.add_argument('--index', type=int, default=8, help='Sample highlighted on the complex plane')
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'01-complex-iq')
args = parser.parse_args()

if not np.isfinite(args.fs) or args.fs <= 0:
    parser.error('--fs must be positive and finite.')
if not all(np.isfinite(v) for v in (args.f, args.amplitude, args.phase_deg)):
    parser.error('Frequency, amplitude and phase must be finite.')
if args.samples < 2:
    parser.error('--samples must be at least 2.')
if not 0 <= args.index < args.samples:
    parser.error('--index must be between 0 and samples-1.')

if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = np.arange(args.samples)
t = n / args.fs
phase = np.deg2rad(args.phase_deg)
theta = 2*np.pi*args.f*t + phase
z = args.amplitude * np.exp(1j*theta)
i = z.real
q = z.imag

assert np.allclose(i, args.amplitude*np.cos(theta))
assert np.allclose(q, args.amplitude*np.sin(theta))
assert np.allclose(np.abs(z), abs(args.amplitude))

fig = plt.figure(figsize=(10, 9), layout='constrained')
grid = fig.add_gridspec(3, 1, height_ratios=[1.25, 1, 1])
plane = fig.add_subplot(grid[0])
wave = fig.add_subplot(grid[1])
polar = fig.add_subplot(grid[2], sharex=wave)

circle = np.linspace(0, 2*np.pi, 600)
radius = abs(args.amplitude)
plane.plot(radius*np.cos(circle), radius*np.sin(circle), color='0.75', label='|z| = amplitude')
plane.plot(i, q, '.', color='0.72', ms=4, label='Complex samples')
k = args.index
plane.arrow(0, 0, i[k], q[k], width=.012*max(radius, 1), length_includes_head=True,
            color='C0', label=f'z[{k}]')
plane.plot(i[k], q[k], 'o', color='C0', ms=8)
plane.plot([0, i[k]], [0, 0], color='C1', lw=2, label='I projection')
plane.plot([i[k], i[k]], [0, q[k]], '--', color='C2', lw=2, label='Q projection')
limit = max(1.15*radius, .5)
plane.set(xlim=(-limit,limit), ylim=(-limit,limit), aspect='equal', xlabel='I = real(z)', ylabel='Q = imag(z)',
          title=f'Sample n={k}: z={i[k]:.4f}{q[k]:+.4f}j')
plane.axhline(0,color='0.7',lw=1); plane.axvline(0,color='0.7',lw=1); plane.grid(alpha=.2); plane.legend(fontsize=9)

wave.plot(t*1e3, i, label='I = cos(theta)', color='C1')
wave.plot(t*1e3, q, label='Q = sin(theta)', color='C2')
wave.plot(t[k]*1e3, i[k], 'o', color='C1'); wave.plot(t[k]*1e3, q[k], 'o', color='C2')
wave.set(ylabel='Coordinate', title='The same rotating vector viewed as two waveforms')
wave.grid(alpha=.25); wave.legend()

polar.plot(t*1e3, np.abs(z), label='abs(z)', color='C0')
polar.plot(t*1e3, np.unwrap(np.angle(z)), label='unwrapped angle(z), rad', color='C3')
polar.set(xlabel='Time (ms)', ylabel='Magnitude / phase', title='Polar description')
polar.grid(alpha=.25); polar.legend()
fig.suptitle(f'z[n] = A exp(j(2 pi f n/Fs + phi)); A={args.amplitude:g}, f={args.f:g} Hz, Fs={args.fs:g}')

print('   n      t (us)   angle (deg)           I           Q        abs(z)  angle(z)')
for idx in range(min(8, args.samples)):
    print(f'{idx:4d} {t[idx]*1e6:11.4f} {np.degrees(theta[idx]):13.4f} {i[idx]:11.6f} {q[idx]:11.6f} {abs(z[idx]):11.6f} {np.angle(z[idx]):9.5f}')

args.output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_dir/'complex-iq.png', dpi=160)
if args.show:
    plt.show()
plt.close(fig)
