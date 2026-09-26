# DSP: от сигнала к собственному HF-трансиверу

Учебный маршрут на русском языке. Конечная цель — самостоятельно спроектировать DSP-часть HF-трансивера, объяснить математику каждого блока, собрать полную модель TX/RX в Python и подготовить её перенос в real-time DSP/FPGA. Финальный инженерный ориентир — понимать решения и компромиссы конструкций QMX/uSDX.

**Сейчас это curriculum/roadmap, а не готовый учебник.** Созданы планы 18 частей и структура для будущих уроков. Исполняемых лабораторных, готового трансивера и HDL пока нет. Основа — согласованный план из беседы «Изучение цифровой обработки сигналов».

## Общая карта

```text
signals → sampling → complex/IQ → Fourier/FFT → filters
                                                   ↓
                                                multirate
                                                   ↓
                         RX: NCO → mixer → DDC → demodulation
                                                   ↕
                         TX: modulation → interpolation → DUC
                                                   ↓
                         noise / nonlinearity / synchronization / feedback
                                                   ↓
                         complete Python transceiver (собираем постепенно)
                                                   ↓
                         fixed-point → streaming → FPGA bridge
                                                   ↓
                         QMX/uSDX analysis → собственная архитектура
```

Математика появляется по мере необходимости: тригонометрия и Euler → комплексные проекции и DFT → convolution → z-transform и feedback. Для старта достаточно базового Python; умение работать с массивами осваиваем в лабораториях.

## Части курса

| № | Раздел |
|---|---|
| 01 | [Сигналы, sampling и quantization](curriculum/01-signals-sampling-quantization/README.md) |
| 02 | [Комплексные числа и I/Q](curriculum/02-complex-iq/README.md) |
| 03 | [Fourier, DFT и FFT](curriculum/03-fourier-dft-fft/README.md) |
| 04 | [LTI, convolution, FIR и IIR](curriculum/04-lti-convolution-fir-iir/README.md) |
| 05 | [Multirate DSP](curriculum/05-multirate/README.md) |
| 06 | [Mixers, NCO и DDC](curriculum/06-mixers-nco-ddc/README.md) |
| 07 | [Demodulation: CW, AM, FM и SSB](curriculum/07-demodulation/README.md) |
| 08 | [Hilbert transform и analytic signals](curriculum/08-hilbert-analytic/README.md) |
| 09 | [TX, DUC и reconstruction](curriculum/09-tx-duc/README.md) |
| 10 | [Модуляция и polar representation](curriculum/10-modulation-polar/README.md) |
| 11 | [Noise, dynamic range и nonlinearity](curriculum/11-noise-dynamic-range-nonlinearity/README.md) |
| 12 | [Digital modes и synchronization](curriculum/12-digital-modes-synchronization/README.md) |
| 13 | [Feedback DSP: AGC, PLL и ALC](curriculum/13-agc-pll-alc/README.md) |
| 14 | [Fixed-point DSP](curriculum/14-fixed-point/README.md) |
| 15 | [Streaming и real-time architecture](curriculum/15-streaming-real-time/README.md) |
| 16 | [FPGA bridge](curriculum/16-fpga-bridge/README.md) |
| 17 | [Полный Python HF transceiver](curriculum/17-python-hf-transceiver/README.md) |
| 18 | [Архитектурный разбор QMX/uSDX](curriculum/18-qmx-usdx-analysis/README.md) |

## Как проходить

Основной порядок — 01–15. Часть 17 служит сквозным проектом: первый RX после 06–08, TX/RX loopback после 09, затем шум, управление, fixed-point и streaming. Номер 17 сохраняет место итогового проекта в согласованном плане; проходить FPGA перед Python-трансивером не нужно. После рабочей модели можно перейти к 16, затем к 18.

У SSB два прохода: в 07 изучаем приём и обзор методов, в 08 разбираем Hilbert/analytic signal и возвращаемся к phasing/Weaver. В 12 сначала используем известную синхронизацию, затем совместно с PLL/Costas loop из 13 добавляем восстановление carrier. Это убирает циклические предпосылки.

Фиксированного расписания нет. Переходим дальше, когда можем объяснить блок своими словами, предсказать эксперимент и подтвердить результат измерением.

## Принципы лаборатории

- Максимум работы на компьютере: Python + NumPy + SciPy / scipy.signal + Matplotlib. Физическое оборудование не требуется для основной части курса.
- Сначала интуиция, затем необходимая математика, эксперимент и вывод. FPGA/ADC/DAC/RF-практика — поздний этап.
- Базовые сигналы — float64, комплексные — complex128. Ранний quantizer — отдельная модель ADC; весь тракт переводим в fixed-point только в 14.
- Convolution, FIR delay line, phase accumulator и базовые rate converters сначала делаем самостоятельно, затем сверяем с библиотекой. FFT используем готовую после короткой ручной DFT.
- Смотрим waveform и spectrum; по задаче добавляем PSD, phase, I/Q, constellation, eye diagram и impulse response. До 03 достаточно временных графиков.
- Фиксируем Fs, units, amplitude/full scale, длительность, window/normalization, random seed и ожидаемый результат. Различаем dBFS, dBm и PSD.
- Используем допустимые IF/baseband-модели. Указание HF carrier в настройках само по себе не позволяет дискретизировать её произвольно низким Fs.
- Реальное audio I/O и sounddevice — опциональное позднее расширение; исходные данные сначала синтетические.

## Контрольные точки

- [ ] После 01–03: объясняю aliasing, I/Q и нормировку спектра.
- [ ] После 04–06: проектирую filter и DDC 192 → 12 kS/s с обоснованным anti-alias filtering.
- [ ] После 07–10: собираю SSB TX/RX loopback и измеряю unwanted sideband suppression.
- [ ] После 11–13: объясняю ограничения шума/перегрузки, работу digital modem и feedback loops.
- [ ] После 14–15: выбираю widths и проверяю сохранение состояния на границах блоков.
- [ ] Проект 17: воспроизводимая модель трансивера с таблицей интерфейсов и измерениями.
- [ ] После 16: выбранный HDL-блок соответствует Python golden reference.
- [ ] После 18: обосновываю собственную архитектуру и сравниваю её с конкретными версиями QMX/uSDX.

## Структура материалов

```text
README.md                       общая карта и критерии
curriculum/01-.../README.md      roadmap отдельной части
curriculum/01-.../01-topic.md    будущий урок (ещё не создан)
templates/lesson.md             шаблон урока
labs/README.md                  соглашения для будущего кода и результатов
notes/README.md                 журнал обучения и открытых вопросов
```

Следующий шаг — добавить первый урок «Синусоида → sampling → phase → aliasing» в часть 01 по [шаблону урока](templates/lesson.md), с первым Python-экспериментом и графиками Matplotlib.
