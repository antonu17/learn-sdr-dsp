# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Aliasing: equal samples do not imply equal continuous-time signals."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'02-aliasing')
args = parser.parse_args()
if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
for fs, high in [(6000,5000),(48000,47000)]:
    for count in [60,600]:
        t=np.arange(count)/fs
        error=np.max(np.abs(np.cos(2*np.pi*1000*t)-np.cos(2*np.pi*high*t)))
        print(f'Fs={fs}; tones=1000/{high} Hz; N={count}; max difference={error:.3e}')
        assert error < 1e-10
fs=6000
sample_t=np.arange(7)/fs
dense_t=np.linspace(0, .001, 2001)
fig,ax=plt.subplots(figsize=(10,4),layout='constrained')
for f,color,label,marker in [(1000,'#00786d','1 kHz','o'),(5000,'#b85b0b','5 kHz','x')]:
    ax.plot(dense_t*1000,np.cos(2*np.pi*f*dense_t),color=color,label=label)
    ax.plot(sample_t*1000,np.cos(2*np.pi*f*sample_t),marker,ms=9,color=color)
ax.set(xlabel='Time (ms)',ylabel='Amplitude',title='Different signals, identical samples: Fs = 6 kS/s')
ax.grid(alpha=.25);ax.legend()
args.output_dir.mkdir(parents=True,exist_ok=True)
fig.savefig(args.output_dir/'aliasing.png',dpi=160)
# At Fs=8 kS/s the old 1/5 kHz pair no longer aliases.
t=np.arange(60)/8000
assert not np.allclose(np.cos(2*np.pi*1000*t),np.cos(2*np.pi*5000*t))
print('At Fs=8000, the original 1000/5000 Hz pair differs.')
if args.show: plt.show()
plt.close(fig)
