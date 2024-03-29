import os
import csv
from tabulate import tabulate


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''

    def load_prices(self, file_path):
        files = os.listdir(file_path)
        prices = []
        for file in files:
            if 'price' in file.lower():
                prices.append(file)
                with open(file=file, mode='r', encoding='utf-8') as fl:
                    reader = csv.DictReader(fl, delimiter=',')
                    headers = reader.fieldnames
                    columns = self._search_product_price_weight(headers=headers)
                    for row in reader:
                        product_name = row.get(columns[0])
                        price = row.get(columns[1])
                        weight = row.get(columns[2])
                        price_per_kg = float(price) / float(weight)
                        self.data.append([product_name, price, weight, file, round(price_per_kg, 2)])

    def _search_product_price_weight(self, headers):
        normal_name_columns = ["название", "продукт", "товар", "наименование"]
        normal_price_column = ["цена", "розница"]
        normal_weight_columns = ["фасовка", "масса", "вес"]
        name_column = None
        price_column = None
        weight_column = None

        for header in headers:
            if header.lower() in normal_name_columns:
                name_column = header
            elif header.lower() in normal_price_column:
                price_column = header
            elif header.lower() in normal_weight_columns:
                weight_column = header
        return name_column, price_column, weight_column

    def export_to_html(self, fname='output.html'):
        with open(fname, mode='w', encoding='utf-8') as file:
            file.write("<html><body>")
            self.data = sorted(self.data, key=lambda x: x[0])
            table = tabulate(self.data, headers=['Наименование', 'Цена', 'Вес', 'Файл', 'Цена за кг.'], tablefmt='html')
            file.write(table)
            file.write("</body></html>")
            return self.result

    def find_text(self, text):
        filtered_data = [row for row in self.data if text.lower() in row[0].lower()]
        sorted_data = sorted(filtered_data, key=lambda x: x[4])
        headers = ["№", "Наименование", "Цена", "Вес", "Файл", "Цена за кг."]
        table = [[idx + 1, *row] for idx, row in enumerate(sorted_data)]
        self.result = tabulate(table, headers, tablefmt="grid")


pm = PriceMachine()
pm.load_prices('/Users/aleksandrlytkin/PycharmProjects/practical_test_price_list_analyzer')

while True:
    search_text = input('Введите название товара для поиска (или "exit / выход" для завершения): ')
    if search_text.lower() in ['exit', 'выход']:
        print('the end')
        break
    pm.find_text(search_text)
    print(pm.export_to_html())

