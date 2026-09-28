# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3"]
# ///
"""Расчёт конкретных отсчётов косинуса: номер → время → угол → значение."""
import argparse
import math
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fs', type=float, default=48_000, help='Sample rate, samples/s (default: 48000)')
    parser.add_argument('--f', type=float, default=24_000, help='Частота косинуса, Hz (default: 24000)')
    parser.add_argument('--amplitude', type=float, default=1.0, help='Амплитуда (default: 1)')
    parser.add_argument('--phase', type=float, default=0.0, help='Начальная фаза, РАДИАНЫ (default: 0)')
    parser.add_argument('--n', type=int, nargs='+', default=[0, 1, 2, 3], help='Номера отсчётов, начиная с нуля (default: 0 1 2 3)')
    args = parser.parse_args()
    if not all(math.isfinite(v) for v in (args.fs, args.f, args.amplitude, args.phase)):
        parser.error('Частоты, амплитуда и фаза должны быть конечными числами.')
    if args.fs <= 0:
        parser.error('--fs должна быть больше нуля.')
    if any(n < 0 for n in args.n):
        parser.error('--n: используем неотрицательные номера отсчётов.')

    # 1. Номер отсчёта → время в секундах.
    n = np.array(args.n, dtype=np.float64)
    t = n / args.fs
    # 2. Время → угол в радианах (NumPy ожидает именно радианы).
    angle = 2 * np.pi * args.f * t + args.phase
    # 3. Косинус угла → значение сигнала с заданной амплитудой.
    x = args.amplitude * np.cos(angle)

    print(f'Fs = {args.fs:g} samples/s; f = {args.f:g} Hz; A = {args.amplitude:g}; phi = {args.phase:g} rad')
    print('t[n] = n/Fs')
    print('theta[n] = 2*pi*f*n/Fs + phi')
    print('x[n] = A*cos(theta[n])\n')
    print(f'{"n":>8} {"t (us)":>14} {"angle (rad)":>16} {"angle (deg)":>14} {"x[n]":>22}')
    for index, time, theta, value in zip(args.n, t, angle, x):
        print(f'{index:8d} {time*1e6:14.6f} {theta:16.9f} {np.degrees(theta):14.6f} {value:22.12g}')
    print('\nУгол показан с учётом всех оборотов. Значения порядка 1e-16 вместо нуля — округление float64.')


if __name__ == '__main__':
    main()
