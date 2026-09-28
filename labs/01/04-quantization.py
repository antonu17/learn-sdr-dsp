# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Uniform bipolar ADC model: samples -> integer codes -> quantized values."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np


def quantize_bipolar(x: np.ndarray, bits: int):
    """Quantize normalized input to signed N-bit codes over [-1, 1)."""
    step = 2.0 / (2**bits)
    code_min = -(2 ** (bits - 1))
    code_max = 2 ** (bits - 1) - 1
    codes = np.rint(x / step).astype(np.int64)
    codes = np.clip(codes, code_min, code_max)
    values = codes.astype(np.float64) * step
    return codes, values, step


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs', type=float, default=48_000, help='Sample rate, samples/s')
parser.add_argument('--f', type=float, default=1_000, help='Cosine frequency, Hz')
parser.add_argument('--amplitude', type=float, default=0.7)
parser.add_argument('--phase', type=float, default=0.0, help='Phase in radians')
parser.add_argument('--samples', type=int, default=96)
parser.add_argument('--bits', type=int, nargs='+', default=[3, 8])
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'04-quantization')
args = parser.parse_args()

if not np.isfinite(args.fs) or args.fs <= 0:
    parser.error('--fs must be a positive finite number.')
if not np.isfinite(args.f) or args.f < 0:
    parser.error('--f must be a non-negative finite number.')
if not np.isfinite(args.amplitude) or not np.isfinite(args.phase):
    parser.error('Amplitude and phase must be finite.')
if args.samples < 4:
    parser.error('--samples must be at least 4.')
if any(bits < 2 or bits > 24 for bits in args.bits):
    parser.error('Use bit widths from 2 to 24.')

if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = np.arange(args.samples)
t = n / args.fs
x = args.amplitude * np.cos(2*np.pi*args.f*t + args.phase)
dense_t = np.linspace(0, t[-1], max(2001, args.samples * 40))
dense_x = args.amplitude * np.cos(2*np.pi*args.f*dense_t + args.phase)

fig, axes = plt.subplots(len(args.bits) + 1, 1, figsize=(10, 3.1*(len(args.bits)+1)),
                         sharex=True, layout='constrained')
if len(args.bits) == 0:
    axes = np.array([axes])

errors = []
for ax, bits in zip(axes[:-1], args.bits):
    codes, q, step = quantize_bipolar(x, bits)
    error = q - x
    errors.append((bits, error))
    ax.plot(dense_t*1e3, dense_x, color='0.68', lw=1.2, label='Input cosine')
    ax.plot(t*1e3, x, '.', color='C0', ms=5, label='Ideal samples')
    ax.step(t*1e3, q, where='mid', color='C1', lw=1.5, label=f'{bits}-bit quantized')
    ax.plot(t*1e3, q, 'o', color='C1', ms=4)
    ax.set(ylabel='Amplitude', title=f'{bits} bit: step = {step:g}; codes {codes.min()} ... {codes.max()}')
    ax.grid(alpha=.25)
    ax.legend(loc='upper right', fontsize=9, ncol=3)
    rms = np.sqrt(np.mean(error**2))
    print(f'{bits:2d} bit: step={step:.9g}; RMS error={rms:.9g}; max |error|={np.max(np.abs(error)):.9g}')
    print(f'  first 12 codes:  {codes[:12]}')
    print(f'  first 12 values: {np.array2string(q[:12], precision=6)}')

for bits, error in errors:
    axes[-1].plot(t*1e3, error, label=f'{bits} bit')
axes[-1].axhline(0, color='0.45', lw=1)
axes[-1].set(xlabel='Time (ms)', ylabel='Quantized − ideal', title='Quantization error')
axes[-1].grid(alpha=.25)
axes[-1].legend()
fig.suptitle(f'f = {args.f:g} Hz; Fs = {args.fs:g} samples/s; A = {args.amplitude:g}')

args.output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_dir/'quantization.png', dpi=160)
if args.show:
    plt.show()
plt.close(fig)
