from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import io
import argparse

quarters = {
    1: "-01-01",
    2: "-04-01",
    3: "-07-01",
    4: "-10-01"
}

class Bank:
    def __init__(self, rating, name, regnum):
        self.rating = rating
        self.name = name
        self.regnum = regnum

    def __str__(self):
        return f"Rating: {self.rating} Name: {self.name} RegNum: {self.regnum}"


def parse_ratings(ratings_csv):
    reader = csv.reader(io.StringIO(
        ratings_csv.decode('windows-1251')), delimiter=';')
    res = []
    for row in reader:
        if len(row) == 0 or not row[0].isnumeric():
            continue
        res.append(Bank(
            int(row[0]),
            row[2],
            int(row[3])
        ))
    return res

def normalize_str(string):
    return ''.join(c for c in string if c.isprintable())


def save_table(table, bank, regnum, date, rating=0):
    with open(f'data/{bank}_{date}_data.csv', 'w', newline='') as f:
        writter = csv.writer(f, delimiter=';', quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)
        writter.writerow(['Банк', 'Номер лицензии банка', 'Место в рейтинге', 'Дата отчёта', 'Наименование статей', 'Символы',
                         'Суммы в рублях от операций в рублях', 'Суммы в рублях от операций в ин. валюте и драг. металлах', 'Всего'])
        for i, row in enumerate(table.find_all('tr')):
            cells = row.find_all('td')

            if len(cells) != 6:
                continue

            if len(cells[2].get_text()) == 5:
                writter.writerow([
                    bank,
                    regnum,
                    rating,
                    date,
                    normalize_str(cells[1].get_text().strip()),
                    normalize_str(cells[2].get_text()).strip().replace(" ", ""),
                    normalize_str(cells[3].get_text()).strip().replace(" ", ""),
                    normalize_str(cells[4].get_text()).strip().replace(" ", ""),
                    normalize_str(cells[5].get_text()).strip().replace(" ", "")
                ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Загрузка финансового отчёта(форма 102) для указанных банков за указанный квартал. Рейтинг используется с сайта banki.ru')
    parser.add_argument('-y', '--year', type=int,
                        help='Отчётный год', required=True)
    parser.add_argument('-q', '--quarter', type=int,
                        help='Отчётный квартал', required=True)
    parser.add_argument('--head', type=int,
                        help='Кол-во банков из топа рейтинга', required=False)
    parser.add_argument('-b', '--bank', type=int,
                        help='Номер лицензии интересующего банка', required=False)
    args = parser.parse_args()

    if args.quarter not in quarters:
        print("Укажите валидный отчётный квартал")
        os.exit(-1)
    
    date = str(args.year) + quarters[args.quarter]
    
    if args.bank != None:
        print(f"Получение отчёта для {args.bank}")
        page_html = urlopen(
            f'https://cbr.ru/banking_sector/credit/coinfo/f102/?regnum={args.bank}&dt={date}').read()

        print(f"Обработка отчёта для {args.bank}")
        soup = BeautifulSoup(page_html, 'html.parser')
        save_table(soup.find_all('table')[0], args.bank, args.bank, date)
        exit(0)

    banks = parse_ratings(
        urlopen('https://www.banki.ru/banks/ratings/export.php').read())
    print(f"Получен рейтинг на {len(banks)} банков")

    for bank in banks:
        if args.head != None and bank.rating > args.head:
            break
        if args.bank != None and bank.regnum != args.bank:
            continue
        print(f"Получение отчёта для {bank.name}(рейтинг {bank.rating})")
        page_html = urlopen(
            f'https://cbr.ru/banking_sector/credit/coinfo/f102/?regnum={bank.regnum}&dt={date}').read()

        print(f"Обработка отчёта для {bank.name}")
        soup = BeautifulSoup(page_html, 'html.parser')
        save_table(soup.find_all('table')[0], bank.name, bank.regnum, date, rating=bank.rating)
