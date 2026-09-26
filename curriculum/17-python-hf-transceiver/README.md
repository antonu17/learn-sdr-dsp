# 17. Полный Python HF transceiver

[← Предыдущая часть](../16-fpga-bridge/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../18-qmx-usdx-analysis/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Объединить блоки в воспроизводимую модель RX/TX и обосновать архитектуру.

**Предпосылки:** Первый RX после 06–08; TX loopback после 09; полный проект после 11–15. FPGA не требуется.

## Будущие уроки

1. Требования: режимы, полезная полоса, Fs, уровни, latency и метрики качества.
2. RX: input samples → DDC → channel filter → demodulator → audio; AGC в обоснованной точке.
3. TX: audio/CW/data → modulator → interpolation/filtering → DUC → output samples.
4. Channel: AWGN, interferers, offsets и nonlinearity; границы моделей ADC/DAC.
5. Интеграция float, fixed-point и streaming; измерения между любыми блоками.

## Python-лаборатория

- Этап A: CW/AM RX; этап B: SSB TX→channel→RX; FM как дополнительный режим.
- Этап C: шум/помехи, AGC и метрики; этап D: integer и streaming варианты.
- Составить таблицу всех интерфейсов: dtype, real/complex, Fs, bandwidth, full scale, state и delay.
- Проверить desired/unwanted sideband, SNR, alias/image suppression и поведение при перегрузке.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Воспроизвожу end-to-end сценарий из сохранённой конфигурации и seed.
- [ ] Объясняю каждый блок и подтверждаю требования измерениями, а не только видом графика.
- [ ] Явно обозначаю IF/baseband simulation: HF tuning metadata не заменяет корректный RF sampling plan.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Главный итоговый проект: software-defined transceiver simulator с отчётом об измерениях.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
