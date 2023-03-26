# Оценка влияния коронавирусной пандемии на доходы банков от кредитования граждан
**Источник данных для датасета**: Отчёт о финансовых результатах(Код формы 0409102, квартальная) с сайта [Банка России](https://cbr.ru).

**Источник рейтинга**: [banki.ru](https://www.banki.ru/banks/ratings).

Датасет сформирован при помощи парсинга отчётных таблиц с сайта Банка России.

## Формирования датасета для текущего исследования
Получение отчётов за 2016, 2019 и 2022 года для топ-10 банков из рейтинга.
```
# python download.py -y 2016 -q 1 --head 10
# python download.py -y 2019 -q 1 --head 10 
# python download.py -y 2022 -q 1 --head 10 
```

Объединение отчётов в один.
```
# python merge.py -d data/ -o 2016-2022_top10_dataset.csv
```

## Использование инструментария для формирования интересующего датасета
Скрипт `download.py` предназначен для скачивания и парсинга отчёта за интересующий отчётный квартал по банкам из рейтинга или номеру лицензии банка.
```
# python download.py -h
usage: download.py [-h] -y YEAR -q QUARTER [--head HEAD] [-b BANK]

Загрузка финансового отчёта(форма 102) для указанных банков за указанный квартал. Рейтинг используется с сайта banki.ru

options:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  Отчётный год
  -q QUARTER, --quarter QUARTER
                        Отчётный квартал
  --head HEAD           Кол-во банков из топа рейтинга
  -b BANK, --bank BANK  Номер лицензии интересующего банка
```

Скрипт `merge.py` позволяет объеденить csv файлы из указанной директории в один большой csv.
```
# python merge.py -h
usage: merge.py [-h] [-d DIR] [-o OUT]

Соединение нескольких датасетов в директории в один

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Путь до директории с csv файлами
  -o OUT, --out OUT  Путь для сохранения результирующего датасета
```