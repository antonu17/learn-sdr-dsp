# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Show Fourier analysis as a bank of complex frequency probes."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs',type=float,default=8_000,help='Sample rate, samples/s')
parser.add_argument('--samples',type=int,default=32)
parser.add_argument('--tone1',type=float,default=1_000,help='First real tone, Hz')
parser.add_argument('--tone2',type=float,default=2_000,help='Second real tone, Hz')
parser.add_argument('--amplitude2',type=float,default=.5,help='Amplitude of second tone')
parser.add_argument('--wrong-probe',type=float,default=1_500,help='Probe compared with tone1')
parser.add_argument('--show',action='store_true')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'outputs'/'01-frequency-probe')
args=parser.parse_args()

if not np.isfinite(args.fs) or args.fs<=0: parser.error('--fs must be positive and finite.')
if args.samples<4 or args.samples%2: parser.error('--samples must be an even integer of at least 4.')
if not all(np.isfinite(v) for v in (args.tone1,args.tone2,args.amplitude2,args.wrong_probe)): parser.error('All signal parameters must be finite.')
if not all(0<abs(v)<args.fs/2 for v in (args.tone1,args.tone2,args.wrong_probe)): parser.error('Tone and probe magnitudes must be between 0 and Fs/2.')

if not args.show: matplotlib.use('Agg')
import matplotlib.pyplot as plt

n=np.arange(args.samples)
t=n/args.fs

# One complex tone demonstrates why a matching counter-rotation stops moving.
z=np.exp(1j*2*np.pi*args.tone1*t)
matched=z*np.exp(-1j*2*np.pi*args.tone1*t)
wrong=z*np.exp(-1j*2*np.pi*args.wrong_probe*t)

# A real two-tone signal demonstrates a complete bank of manual DFT probes.
x1=np.cos(2*np.pi*args.tone1*t)
x2=args.amplitude2*np.cos(2*np.pi*args.tone2*t)
x=x1+x2

# Dense reference curves show the continuous signal that is being sampled.
t_dense=np.linspace(t[0],t[-1],args.samples*40)
x1_dense=np.cos(2*np.pi*args.tone1*t_dense)
x2_dense=args.amplitude2*np.cos(2*np.pi*args.tone2*t_dense)
x_dense=x1_dense+x2_dense
k=np.arange(-args.samples//2,args.samples//2)
probe_frequencies=k*args.fs/args.samples
X_manual=np.array([np.sum(x*np.exp(-1j*2*np.pi*f*t)) for f in probe_frequencies])
X_fft_shifted=np.fft.fftshift(np.fft.fft(x))
assert np.allclose(X_manual,X_fft_shifted,atol=1e-10)

fig=plt.figure(figsize=(14,8),layout='constrained')
grid=fig.add_gridspec(2,3,height_ratios=[1,1.15])
input_axis=fig.add_subplot(grid[0,0])
matched_axis=fig.add_subplot(grid[0,1])
wrong_axis=fig.add_subplot(grid[0,2])
time_axis=fig.add_subplot(grid[1,0:2])
spectrum_axis=fig.add_subplot(grid[1,2])

input_axis.plot(n,z.real,'o-',label='I');input_axis.plot(n,z.imag,'x--',label='Q')
input_axis.set(xlabel='Sample n',ylabel='Coordinate',title=f'Input complex tone: {args.tone1:g} Hz')
input_axis.grid(alpha=.25);input_axis.legend()

matched_path=np.concatenate(([0j],np.cumsum(matched)))
wrong_path=np.concatenate(([0j],np.cumsum(wrong)))
for axis,path,title,color in (
    (matched_axis,matched_path,f'Matched probe {args.tone1:g} Hz','C2'),
    (wrong_axis,wrong_path,f'Wrong probe {args.wrong_probe:g} Hz','C1'),
):
    axis.plot(path.real,path.imag,'o-',color=color,ms=3)
    axis.arrow(0,0,path[-1].real,path[-1].imag,width=.04,length_includes_head=True,color=color,alpha=.45)
    axis.axhline(0,color='0.72',lw=1);axis.axvline(0,color='0.72',lw=1)
    axis.set(aspect='equal',xlabel='I',ylabel='Q',title=title)
    axis.grid(alpha=.2)
matched_axis.set_aspect('auto')
matched_axis.set_ylim(-1,1)

time_axis.plot(t_dense*1e3,x1_dense,'--',lw=1.2,alpha=.75,label=f'{args.tone1:g} Hz cosine')
time_axis.plot(t_dense*1e3,x2_dense,'--',lw=1.2,alpha=.75,label=f'{args.tone2:g} Hz cosine, amplitude {args.amplitude2:g}')
time_axis.plot(t_dense*1e3,x_dense,color='0.15',lw=2,label='Continuous sum before sampling')
time_axis.stem(t*1e3,x,linefmt='C0-',markerfmt='C0o',basefmt=' ',label='Digital samples of the sum')
time_axis.set(xlabel='Time, ms',ylabel='Amplitude',title='Two real cosines and their sum')
time_axis.grid(alpha=.25)
time_axis.legend(ncols=2,fontsize=8)

spectrum_axis.stem(probe_frequencies,np.abs(X_manual)/args.samples,basefmt=' ')
spectrum_axis.set(xlabel='Probe frequency, Hz',ylabel='|sum| / N',title='Manual probes: DFT result')
spectrum_axis.grid(alpha=.25)

fig.suptitle('A matching complex probe stops a tone; summing reveals the match')

print(f'mean after matching probe ({args.tone1:g} Hz): {np.mean(matched):.6f}')
print(f'mean after wrong probe ({args.wrong_probe:g} Hz): {np.mean(wrong):.6f}')
print('\nStrongest manual DFT probes:')
for idx in np.argsort(np.abs(X_manual))[-6:][::-1]:
    print(f'{probe_frequencies[idx]:9.1f} Hz  magnitude/N={abs(X_manual[idx])/args.samples:.6f}  phase={np.angle(X_manual[idx]):+.4f} rad')
print(f'\nmax |manual DFT - np.fft.fft| = {np.max(np.abs(X_manual-X_fft_shifted)):.3e}')

args.output_dir.mkdir(parents=True,exist_ok=True)
fig.savefig(args.output_dir/'frequency-probe.png',dpi=160)
if args.show: plt.show()
plt.close(fig)
