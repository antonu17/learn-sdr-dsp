# 12. Digital modes и synchronization

[← Предыдущая часть](../11-noise-dynamic-range-nonlinearity/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../13-agc-pll-alc/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Пройти путь от bits к symbols и восстановлению данных при неизвестных времени и частоте.

**Предпосылки:** 04–06, 10–11; carrier recovery углубляется совместно с 13.

## Будущие уроки

1. ASK/FSK/PSK, BPSK/QPSK/QAM, constellation, symbol rate и bit rate.
2. Pulse shaping: raised cosine / root-raised-cosine, matched filter и ISI.
3. Symbol timing recovery, частотная/фазовая ошибка, carrier recovery и Costas loop.
4. FSK/MSK; архитектурная связь с FT8/WSPR без обязательной реализации полного протокола.

## Python-лаба

- Сначала собрать BPSK/QPSK loopback с известной синхронизацией; рисовать constellation и eye diagram.
- Добавить timing offset, carrier offset и AWGN по отдельности; измерить BER.
- После 13 включить recovery loops и сравнить захват и работу после синхронизации.
- Сопоставить спектры pulse shaping и простой FSK/MSK-модели.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Разделяю matched filtering, timing recovery и carrier recovery.
- [ ] Измеряю BER на известных bits и отделяю переходный процесс захвата от steady state.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Учебный цифровой модем с контролируемыми искажениями канала.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
