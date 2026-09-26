# 04. LTI, convolution, FIR и IIR

[← Предыдущая часть](../03-fourier-dft-fft/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../05-multirate/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Перейти от отклика на импульс к фильтру с измеримыми характеристиками.

**Предпосылки:** 01–03.

## Будущие уроки

1. Линейность, time invariance, impulse response и superposition.
2. Convolution вручную, delay line и difference equations.
3. FIR: taps, cutoff, transition band, stopband attenuation, group delay.
4. Frequency response; windowed sinc и Parks–McClellan.
5. IIR: feedback, z-transform по необходимости, poles/zeros, stability, biquads/SOS, Butterworth и Chebyshev.

## Python-лаборатория

- Написать convolution и FIR с delay line; сравнить с np.convolve и scipy.signal.lfilter.
- Спроектировать CW-фильтр 300–500 Hz и SSB-фильтр примерно 2.4 kHz с явно указанными границами полос.
- Сравнить FIR/IIR по АЧХ, ФЧХ, group delay, impulse/step response и стоимости вычислений.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Задаю passband, stopband, ripple и attenuation до выбора taps.
- [ ] Объясняю задержку FIR, устойчивость IIR и обработку начального состояния.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Набор фильтров RX и утилита проверки frequency response.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
