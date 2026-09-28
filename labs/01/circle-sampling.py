# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
"""Cosine as the horizontal coordinate of a rotating point; sampling snapshots."""
from pathlib import Path
import argparse
import numpy as np
import matplotlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--show', action='store_true')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent / 'outputs' / 'circle-sampling')
args = parser.parse_args()
if not args.show:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

F = 1000.0
FS = 6000.0
n = np.arange(7)
t = n / FS
samples = np.cos(2*np.pi*F*t)
fig, (circle, wave) = plt.subplots(1, 2, figsize=(11, 5))
fig.subplots_adjust(bottom=.24, wspace=.38, top=.82)
phi = np.linspace(0, 2*np.pi, 600)
circle.plot(np.cos(phi), np.sin(phi), color='0.65')
circle.axhline(0, color='0.7', lw=1)
circle.axvline(0, color='0.7', lw=1)
circle.set(xlim=(-1.3, 1.3), ylim=(-1.3, 1.3), aspect='equal', xlabel='Horizontal coordinate = cos(angle)', ylabel='Vertical coordinate = sin(angle)', title='Rotating point on a unit circle')
circle.set_xticks([-1, 0, 1]); circle.set_yticks([-1, 0, 1])
radius, = circle.plot([], [], color='C0', lw=2)
projection, = circle.plot([], [], '--', color='C1')
point, = circle.plot([], [], 'o', color='C0', ms=9)
foot, = circle.plot([], [], 's', color='C1', ms=8)
angle_label = circle.text(.03, .96, '', transform=circle.transAxes, va='top')
dense_t = np.linspace(0, 1/F, 600)
wave.plot(dense_t*1000, np.cos(2*np.pi*F*dense_t), color='C0')
wave.stem(t*1000, samples, linefmt='C1-', markerfmt='C1o', basefmt=' ')
selected, = wave.plot([], [], 's', color='C3', ms=10)
wave.set(xlabel='Time (ms)', ylabel='Sample value', title='1 kHz cosine, sampling at 6 kS/s', ylim=(-1.3, 1.3))
wave.grid(alpha=.25)
heading = fig.suptitle('')
control = fig.add_axes([.2, .08, .6, .04])
slider = Slider(control, 'Sample n', 0, 6, valinit=1, valstep=1)

def update(value):
    k = int(value)
    theta = 2*np.pi*F*k/FS
    x, y = np.cos(theta), np.sin(theta)
    radius.set_data([0,x],[0,y])
    projection.set_data([x,x],[0,y])
    point.set_data([x],[y]); foot.set_data([x],[0])
    selected.set_data([1000*k/FS],[x])
    angle_label.set_text(f'Angle: {theta*180/np.pi:.0f} degrees')
    heading.set_text(f'n = {k}     time = {1000*k/FS:.3f} ms     sample = {x:.3f}')
    fig.canvas.draw_idle()

slider.on_changed(update)
update(1)
args.output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_dir / 'circle-sampling.png', dpi=160)
assert np.allclose(samples, [1, .5, -.5, -1, -.5, .5, 1])
print('Samples at 60-degree steps:', np.round(samples, 3))
if args.show:
    plt.show()
plt.close(fig)
