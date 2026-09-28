# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy==2.5.3",
#     "matplotlib==3.11.2",
# ]
# ///
"""Lesson 01: cosine, phase, sampling and aliasing. No hardware needed."""
from pathlib import Path
import argparse
import numpy as np
import matplotlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--show', action='store_true', help='Also open plot windows')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent / 'outputs' / '01-sine-sampling')
args = parser.parse_args()
if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Change one parameter at a time, then predict the new plot.
FS = 48_000.0       # samples per second
FREQUENCY = 1_000.0 # cycles per second
AMPLITUDE = 1.0     # normalized amplitude, not volts
PHASE = 0.0        # radians
N = 96             # samples: n = 0 ... 95

def cosine(t, frequency, amplitude=1.0, phase=0.0):
    return amplitude * np.cos(2 * np.pi * frequency * t + phase)

args.output_dir.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
t = np.arange(N, dtype=np.float64) / FS
# Dense grid is only a visual reference, not the ADC samples.
t_ref = np.linspace(0, N / FS, 4001)
x = cosine(t, FREQUENCY, AMPLITUDE, PHASE)

fig, axes = plt.subplots(2, 1, figsize=(10, 6), constrained_layout=True)
axes[0].plot(t_ref * 1e3, cosine(t_ref, FREQUENCY, AMPLITUDE, PHASE), label='Continuous-time reference')
axes[0].stem(t * 1e3, x, linefmt='C1-', markerfmt='C1o', basefmt=' ')
axes[0].set(title=f'{FREQUENCY:g} Hz cosine sampled at {FS:g} samples/s', ylabel='Amplitude', xlabel='Time (ms)')
axes[0].legend()
for phase, label in [(0, 'phase = 0'), (np.pi/2, 'phase = pi/2'), (np.pi, 'phase = pi')]:
    axes[1].plot(t_ref * 1e3, cosine(t_ref, FREQUENCY, AMPLITUDE, phase), label=label)
axes[1].set(title='Same frequency and amplitude, different starting phase', xlabel='Time (ms)', ylabel='Amplitude')
axes[1].legend(ncol=3)
for ax in axes:
    ax.grid(alpha=.25)
fig.savefig(args.output_dir / '01-sampling-phase.png', dpi=160)

fig2, axes2 = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
errors = []
for ax, (high, low) in zip(axes2, [(28_000, 20_000), (47_000, 1_000)]):
    # Same Fs, zero initial phase, short view to make individual samples visible.
    ts = np.arange(16, dtype=np.float64) / FS
    dense = np.linspace(0, ts[-1], 3001)
    ax.plot(dense * 1e3, cosine(dense, high), color='C1', alpha=.7, label=f'{high/1000:g} kHz reference')
    ax.plot(dense * 1e3, cosine(dense, low), color='C0', alpha=.8, label=f'{low/1000:g} kHz reference')
    ax.plot(ts * 1e3, cosine(ts, high), 'o', color='C1', markersize=8, label='High-frequency samples')
    ax.plot(ts * 1e3, cosine(ts, low), 'x', color='black', markersize=6, label='Low-frequency samples')
    ax.set(title=f'{high/1000:g} kHz and {low/1000:g} kHz: identical samples at Fs = 48 kHz', xlabel='Time (ms)', ylabel='Amplitude')
    ax.grid(alpha=.25)
    ax.legend(ncol=2, fontsize=9)
    err = np.max(np.abs(cosine(t, high) - cosine(t, low)))
    errors.append(f'{high:g}/{low:g} Hz max sample difference: {err:.3e}')
    # Numerical check of the alias identity, allowing float64 roundoff.
    assert np.allclose(cosine(t, high), cosine(t, low), rtol=0, atol=1e-11)
fig2.savefig(args.output_dir / '02-aliasing.png', dpi=160)
report = '\n'.join([
    f'Fs={FS:g} samples/s; f={FREQUENCY:g} Hz; A={AMPLITUDE}; phase={PHASE} rad; N={N}',
    f'T={1/FREQUENCY:.9g} s; Ts={1/FS:.9g} s; samples/cycle={FS/FREQUENCY:g}',
    f'Record interval N/Fs={N/FS:.9g} s; last sample time={(N-1)/FS:.9g} s',
    f'First 8 samples: {np.array2string(x[:8], precision=6)}',
    f'NumPy={np.__version__}; Matplotlib={matplotlib.__version__}',
    *errors,
]) + '\n'
(args.output_dir / 'measurements.txt').write_text(report)
print(report)
if args.show:
    plt.show()
plt.close('all')
