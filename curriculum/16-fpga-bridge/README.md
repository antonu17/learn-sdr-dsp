# 16. FPGA bridge

[← Предыдущая часть](../15-streaming-real-time/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../17-python-hf-transceiver/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Перенести понятные DSP-блоки в HDL, используя Python как golden reference.

**Предпосылки:** 14–15 и проверенные Python-модели из 06/17.

## Будущие уроки

1. Clock, registers, combinational logic, pipeline, latency и throughput.
2. Fixed-point HDL, DSP48/BRAM, valid/ready, reset, clock domains и CDC/FIFO.
3. Последовательность переноса: NCO → mixer → FIR → CIC → DDC.
4. Test vectors, HDL simulation, выравнивание latency и bit-exact comparison.
5. Опциональный этап на Arty A7; ADC/DAC и RF frontend только после проверки моделей.

## Python-лаба

- Экспортировать входы и ожидаемые outputs из integer Python-модели.
- Сравнить HDL simulation с reference на импульсе, тоне, случайных данных и предельных уровнях.
- Добавить паузы потока и проверить handshakes, порядок samples и reset.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Объясняю расхождения с reference и отделяю latency от численной ошибки.
- [ ] Для выбранного DDC показываю resource/timing budget; аппаратная плата не обязательна для HDL simulation.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Один проверенный HDL DSP-тракт с Python test vectors.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
