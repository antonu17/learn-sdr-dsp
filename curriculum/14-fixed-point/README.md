# 14. Fixed-point DSP

[← Предыдущая часть](../13-agc-pll-alc/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../15-streaming-real-time/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Выбрать разрядности и масштабирование по измеряемой ошибке.

**Предпосылки:** 01–13; рабочие float-модели блоков.

## Будущие уроки

1. Signed integers, two’s complement, диапазон и явно оговорённая Q-format convention.
2. Q1.15: 16 bits всего, включая sign, 15 fractional bits; диапазон [-1, 1−2^-15].
3. Multiplication, bit growth, accumulator width, shifts и rescaling.
4. Overflow: wrap/saturation; truncation/rounding, coefficient quantization и limit cycles.
5. Сравнение float64/complex128, float32/complex64 и 24/16/12/8-bit моделей.

## Python-лаборатория

- Написать модели rounding, saturation и wrap с явной шириной; избегать неявного переполнения NumPy integers.
- Перевести FIR, NCO и mixer в integer-модель; измерить SNR, spurs и запас аккумулятора.
- Повторить трудные сценарии трансивера: сильная помеха, малый сигнал, пик огибающей, IIR feedback.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Для каждого узла указываю signedness, scale, width и правило округления.
- [ ] Отделяю bit-exact arithmetic от приближённой модели quantization через float.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Таблица разрядностей и fixed-point golden reference выбранных блоков.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
