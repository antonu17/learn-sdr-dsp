# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Compute a four-sample DFT by hand and compare its cost with FFT."""
import argparse
import time
from pathlib import Path

import matplotlib
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs',type=float,default=8_000,help='Sample rate, samples/s')
parser.add_argument('--max-power',type=int,default=12,help='Largest N=2**max_power in the timing sweep')
parser.add_argument('--repeats',type=int,default=5,help='Repeats per N; keep the fastest')
parser.add_argument('--show',action='store_true')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'outputs'/'02-dft-manual-fft')
args=parser.parse_args()

if not np.isfinite(args.fs) or args.fs<=0: parser.error('--fs must be positive and finite.')
if args.max_power<6 or args.max_power>16: parser.error('--max-power must be between 6 and 16.')
if args.repeats<1: parser.error('--repeats must be at least 1.')

if not args.show: matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Part 1: N=4 DFT computed by hand, using a matrix of the same probe exponentials
# from the previous lesson, then checked against np.fft.fft.
N=4
n=np.arange(N)
x=np.cos(2*np.pi*n/N)  # one full cycle across 4 samples: [1, 0, -1, 0]

k=np.arange(N)
W=np.exp(-1j*2*np.pi*np.outer(k,n)/N)  # row k, column n: probe for bin k at sample n
X_manual=W@x

X_fft=np.fft.fft(x)
assert np.allclose(X_manual,X_fft,atol=1e-10)

freqs=np.fft.fftfreq(N,d=1/args.fs)
freqs_shifted=np.fft.fftshift(freqs)
X_shifted=np.fft.fftshift(X_manual)

print(f'x[n] = {np.round(x,3)}')
print('\nnp.fft.fft order (k=0, positive bins, then negative bins):')
print(f'{"k":>3} {"freq, Hz":>10} {"X[k]":>18}')
for kk,f,val in zip(k,freqs,X_manual):
    print(f'{kk:>3} {f:>10.1f} {val.real:>+8.3f}{val.imag:+7.3f}j')

print('\nAfter fftshift, same bins in ascending frequency order:')
for f,val in zip(freqs_shifted,X_shifted):
    print(f'{f:>10.1f} Hz  X = {val.real:+.3f}{val.imag:+.3f}j')

print(f'\nmax |manual DFT matrix - np.fft.fft| = {np.max(np.abs(X_manual-X_fft)):.3e}')

# Part 2: time the same computation two ways as N grows.
# "Manual" means the DFT-by-definition matrix multiply, still O(N^2).
powers=np.arange(6,args.max_power+1)
sizes=2**powers
manual_times=[]
fft_times=[]
for size in sizes:
    n_s=np.arange(size)
    x_s=np.cos(2*np.pi*3*n_s/size)
    best_manual=np.inf
    best_fft=np.inf
    for _ in range(args.repeats):
        t0=time.perf_counter()
        W_s=np.exp(-1j*2*np.pi*np.outer(n_s,n_s)/size)
        _=W_s@x_s
        best_manual=min(best_manual,time.perf_counter()-t0)

        t0=time.perf_counter()
        _=np.fft.fft(x_s)
        best_fft=min(best_fft,time.perf_counter()-t0)
    manual_times.append(best_manual)
    fft_times.append(best_fft)
manual_times=np.array(manual_times)
fft_times=np.array(fft_times)

print('\nTiming sweep (best of repeats):')
print(f'{"N":>7} {"manual, s":>12} {"fft, s":>12} {"speedup":>10}')
for size,tm,tf in zip(sizes,manual_times,fft_times):
    print(f'{size:>7} {tm:>12.5f} {tf:>12.5f} {tm/tf:>9.1f}x')

fig,(ax_bins,ax_time)=plt.subplots(1,2,figsize=(12,5),layout='constrained')

ax_bins.stem(freqs_shifted,np.abs(X_shifted))
ax_bins.set(xlabel='Frequency, Hz',ylabel='|X[k]|',title='Four-sample DFT, magnitude by bin')
ax_bins.grid(alpha=.25)

ax_time.loglog(sizes,manual_times,'o-',label='Manual DFT matrix, O(N^2)')
ax_time.loglog(sizes,fft_times,'s-',label='np.fft.fft, O(N log N)')
ax_time.set(xlabel='N, samples',ylabel='Best time, s',title='Same numbers, different cost')
ax_time.grid(alpha=.25,which='both')
ax_time.legend()

fig.suptitle('DFT by definition vs FFT: identical results, different growth')

args.output_dir.mkdir(parents=True,exist_ok=True)
fig.savefig(args.output_dir/'dft-manual-fft.png',dpi=160)
if args.show: plt.show()
plt.close(fig)
