# 09. TX, DUC и reconstruction

[← Предыдущая часть](../08-hilbert-analytic/README.md) · [Карта курса](../../README.md) · [Следующая часть →](../10-modulation-polar/README.md)

Статус: roadmap. Уроки и исполняемые эксперименты предстоит добавить.

## Цель

Собрать передающий тракт до модели выходных samples.

**Предпосылки:** 05–08.

## Будущие уроки

1. Audio/CW/data → complex baseband; уровни и headroom.
2. DUC: interpolation с anti-imaging filtering → complex mixer/NCO.
3. Переход к real IF/RF samples и допустимый частотный план.
4. Модель DAC: zero-order hold, images и reconstruction LPF/BPF.

## Python-лаба

- Собрать SSB TX с baseband при 12 kS/s и выходом 192 kS/s; выбрать IF так, чтобы полезный спектр помещался в Nyquist zone.
- Проверить images до/после interpolation filter и полосу после upconversion.
- Соединить DUC с DDC и восстановить исходное audio с поправкой на задержку и масштаб.

Основной стек: NumPy, SciPy / scipy.signal, Matplotlib. Для каждого эксперимента сохраняем параметры, графики с единицами и короткий вывод. До части 14 используем float64 и complex128, кроме явно выделенных опытов с quantization.

## Критерии готовности

- [ ] Различаю цифровой anti-imaging filter и аналоговый reconstruction filter.
- [ ] Показываю Fs, gain, полосу и запас по уровню на каждой ступени TX.
- [ ] Могу предсказать результат ключевого эксперимента до запуска и объяснить отличие от прогноза.

## Результат для общего проекта

Python TX→RX loopback без физического оборудования.

## Как наполнять раздел

Добавлять уроки рядом с этим README как `01-topic.md`, `02-topic.md` и далее, используя [шаблон](../../templates/lesson.md). Здесь заменить план пунктов ссылками на готовые уроки и отмечать прогресс по критериям. Код, notebooks и результаты размещать по [соглашениям проекта](../../labs/README.md); готовых уроков сейчас нет.
