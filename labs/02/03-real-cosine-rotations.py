# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Build one real cosine from two conjugate complex rotations."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fs', type=float, default=8_000, help='Sample rate, samples/s')
parser.add_argument('--f', type=float, default=1_000, help='Tone frequency, Hz')
parser.add_argument('--amplitude', type=float, default=1.0, help='Real cosine amplitude')
parser.add_argument('--phase-deg', type=float, default=0.0)
parser.add_argument('--samples', type=int, default=17)
parser.add_argument('--index', type=int, default=1, help='Sample highlighted on the complex plane')
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent/'outputs'/'03-real-cosine-rotations')
args = parser.parse_args()

if not np.isfinite(args.fs) or args.fs <= 0:
    parser.error('--fs must be positive and finite.')
if not np.isfinite(args.f) or not 0 < args.f < args.fs/2:
    parser.error('--f must be between 0 and Fs/2.')
if not np.isfinite(args.amplitude) or not np.isfinite(args.phase_deg):
    parser.error('Amplitude and phase must be finite.')
if args.samples < 2:
    parser.error('--samples must be at least 2.')
if not 0 <= args.index < args.samples:
    parser.error('--index must be between 0 and samples-1.')

if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = np.arange(args.samples)
theta = 2*np.pi*args.f*n/args.fs + np.deg2rad(args.phase_deg)
z_positive = np.exp(1j*theta)
z_negative = np.exp(-1j*theta)
x = args.amplitude*np.cos(theta)
x_from_rotations = args.amplitude*(z_positive+z_negative)/2

assert np.allclose(z_negative,np.conj(z_positive))
assert np.allclose(x,x_from_rotations.real)
assert np.allclose(x_from_rotations.imag,0)

k=args.index
fig=plt.figure(figsize=(11,10),layout='constrained')
grid=fig.add_gridspec(3,1,height_ratios=[1.25,1,1])
plane=fig.add_subplot(grid[0]); q_axis=fig.add_subplot(grid[1]); real_axis=fig.add_subplot(grid[2],sharex=q_axis)

circle=np.linspace(0,2*np.pi,600)
plane.plot(np.cos(circle),np.sin(circle),color='0.8')
z_sum=z_positive[k]+z_negative[k]
z_average=z_sum/2
plane.plot([0,z_sum.real],[0,z_sum.imag],color='C4',lw=10,alpha=.25,label='sum z+ + z-')
plane.arrow(0,0,z_average.real,z_average.imag,width=.015,length_includes_head=True,color='C4',label='average (z+ + z-) / 2')
plane.arrow(0,0,z_positive[k].real,z_positive[k].imag,width=.012,length_includes_head=True,color='C0',label='z+ = exp(+j theta)')
plane.arrow(0,0,z_negative[k].real,z_negative[k].imag,width=.012,length_includes_head=True,color='C1',label='z- = exp(-j theta)')
plane.arrow(z_positive[k].real,z_positive[k].imag,z_negative[k].real,z_negative[k].imag,
            width=.009,length_includes_head=True,color='C1',linestyle='--',alpha=.8,label='translated z- (head-to-tail)')
plane.axhline(0,color='0.72',lw=1);plane.axvline(0,color='0.72',lw=1)
plane.set(xlim=(-2.15,2.15),ylim=(-1.15,1.15),aspect='equal',xlabel='I',ylabel='Q',title=f'Sample n={k}: head-to-tail vector addition, then divide by 2')
plane.grid(alpha=.2);plane.legend(loc='center left',bbox_to_anchor=(1.03,.5))

q_axis.plot(n,z_positive.imag,'o-',label='Q+ = sin(theta)',color='C0')
q_axis.plot(n,z_negative.imag,'x--',label='Q- = -sin(theta)',color='C1')
q_axis.plot(n,(z_positive.imag+z_negative.imag)/2,'.-',label='average Q = 0',color='C4')
q_axis.set(ylabel='Q',title='Vertical coordinates cancel')
q_axis.grid(alpha=.25);q_axis.legend()

real_axis.plot(n,x,'o-',label='A cos(theta)',color='C2')
real_axis.plot(n,x_from_rotations.real,'x--',label='A(z+ + z-) / 2',color='C4')
real_axis.set(xlabel='Sample n',ylabel='Real value',title='The two rotations reconstruct the real cosine')
real_axis.grid(alpha=.25);real_axis.legend()

fig.suptitle(f'A cos(theta) = A/2 exp(+j theta) + A/2 exp(-j theta); A={args.amplitude:g}, f={args.f:g} Hz, Fs={args.fs:g}')

print('   n   angle(deg)            z+                 z-          cosine    reconstructed')
for idx in range(min(8,args.samples)):
    print(f'{idx:4d} {np.degrees(theta[idx]):12.3f} '
          f'{z_positive[idx].real:+.4f}{z_positive[idx].imag:+.4f}j  '
          f'{z_negative[idx].real:+.4f}{z_negative[idx].imag:+.4f}j  '
          f'{x[idx]:12.6f} {x_from_rotations[idx].real:16.6f}')
print(f'\nmax reconstruction error = {np.max(np.abs(x-x_from_rotations)):.3e}')

args.output_dir.mkdir(parents=True,exist_ok=True)
fig.savefig(args.output_dir/'real-cosine-rotations.png',dpi=160)
if args.show:
    plt.show()
plt.close(fig)
