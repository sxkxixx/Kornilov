import csv
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Side


class Salary:
	currency_to_rub = {"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
	                   "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}

	def __init__(self, salary_from, salary_to, salary_currency):
		self.salary_from = float(salary_from)
		self.salary_to = float(salary_to)
		self.salary_currency = salary_currency

	def get_average(self):
		return 0.5 * (self.salary_from + self.salary_to) * self.currency_to_rub[self.salary_currency]


class Vacancy:
	def __init__(self, vacancy):
		self.name = vacancy['name']
		self.salary = Salary(vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_currency'])
		self.area_name = vacancy['area_name']
		self.published_at = vacancy['published_at']

	def get_year(self):
		return int(self.published_at[:4])


class DataSet:
	def __init__(self, file_name, name):
		self.file_name = file_name
		self.vacancy_name = name

	def parse_csv(self):
		salary, amount, this_vacancy_salary, this_vacancy_amount, salary_city, share_city = {}, {}, {}, {}, {}, {}
		count = 0
		with open(self.file_name, encoding='utf-8-sig') as file:
			rows = csv.reader(file)
			titles = next(rows)
			for row in rows:
				if len(row) == len(titles) and all(row):
					vacancy = Vacancy(dict(zip(titles, row)))
					count += 1
					year, city = vacancy.get_year(), vacancy.area_name
					self.append_to_dictionary(salary, year, [vacancy.salary.get_average()])
					self.append_to_dictionary(amount, year, 1)
					self.append_to_dictionary(salary_city, city, [vacancy.salary.get_average()])
					self.append_to_dictionary(share_city, city, 1)
					if self.vacancy_name in vacancy.name:
						self.append_to_dictionary(this_vacancy_salary, year, [vacancy.salary.get_average()])
						self.append_to_dictionary(this_vacancy_amount, year, 1)
			return salary, amount, this_vacancy_salary, this_vacancy_amount, salary_city, share_city, count

	@staticmethod
	def append_to_dictionary(dct, key, summand):
		if key not in dct:
			dct[key] = summand
		else:
			dct[key] += summand

	@staticmethod
	def convert_dct(dct: dict):
		for key, value in dct.items():
			dct[key] = 0 if len(value) == 0 else int(sum(value) / len(value))
		return dct

	def get_formatted_data(self):
		salary, amount, this_vacancy_salary, this_vacancy_amount, salary_city, share_city, count = self.parse_csv()
		for key, value in share_city.items():
			share_city[key] = round(value / count, 4)
		share_city = list(filter(lambda x: x[-1] > 0.01, [(key, value) for key, value in share_city.items()]))
		salary_city = sorted(
			[(key, value) for key, value in self.convert_dct(salary_city).items() if key in dict(share_city)],
			key=lambda x: x[-1], reverse=True)
		return self.convert_dct(salary), amount, self.convert_dct(this_vacancy_salary), this_vacancy_amount, \
		       dict(salary_city[:10]), dict(sorted(share_city, key=lambda x: x[-1], reverse=True)[:10])


class Report:
	def __init__(self, salary, amount, this_vacancy_salary, this_vacancy_amount, salary_city, share_city):
		self.salary = salary
		self.amount = amount
		self.this_vacancy_salary = this_vacancy_salary
		self.this_vacancy_amount = this_vacancy_amount
		self.salary_city = salary_city
		self.share_city = share_city

	def generate_image(self):
		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
		self.vertical_bar(ax1, 'Уровень зарплат по годам', 'Средняя з/п', self.salary, self.this_vacancy_salary)
		self.vertical_bar(ax2, 'Количества вакансий по годам', 'Количество вакансий', self.amount,
		                  self.this_vacancy_amount)

		ax3.set_title('Уровень зарплат по городам', fontsize=8)
		cities = [name.replace('-', '-\n').replace(' ', '\n') for name in reversed(list(self.salary_city.keys()))]
		ax3.barh(cities, list(reversed(list(self.salary_city.values()))), height=0.4, align='center')
		ax3.xaxis.set_tick_params(labelsize=8)
		ax3.yaxis.set_tick_params(labelsize=6)
		ax3.grid(axis='x')

		ax4.set_title('Доля вакансий по городам', fontsize=8)
		summary = sum(self.share_city.values())
		ax4.pie(list(self.share_city.values()) + [1 - summary], labels=list(self.share_city.keys()) + ['Другие'],
		        textprops={'fontsize': 6})

		plt.tight_layout()
		plt.savefig('graph.png')

	def generate_excel(self):
		wb = Workbook()
		font_bold = Font(bold=True)
		side = Side(border_style='thin', color='000000')
		border = Border(left=side, right=side, top=side, bottom=side)
		year_statistics = wb.active
		year_statistics.title = 'Статистика по годам'
		year_data = [['Год', 'Средняя зарплата', f'Средняя зарплата - {dataset.vacancy_name}', 'Количество вакансий',
		              f'Количество вакансий - {dataset.vacancy_name}']]
		for year in self.salary:
			year_data.append([year, self.salary[year], self.this_vacancy_salary[year], self.amount[year],
			                  self.this_vacancy_amount[year]])
		self.fill_excel(year_statistics, year_data)
		city_statistics = wb.create_sheet('Статистика по городам')
		city_data = [['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий']]
		for (city_salary, salary), (share_city, share) in zip(self.salary_city.items(), self.share_city.items()):
			city_data.append([city_salary, salary, '', share_city, share])
		self.fill_excel(city_statistics, city_data)
		for i in range(len(city_data)):
			city_statistics[f'E{i + 2}'].number_format = '0.00%'
		self.set_border(year_statistics, border, year_data, 'ABCDE')
		self.set_border(city_statistics, border, city_data, 'ABDE')
		self.set_column_width(year_data, year_statistics)
		self.set_column_width(city_data, city_statistics)
		self.set_font(font_bold, year_statistics, city_statistics)
		wb.save('report.xlsx')

	@staticmethod
	def vertical_bar(ax, title, legend, data, this_vacancy_data):
		ax.set_title(title, fontsize=8)
		first_bar = ax.bar(np.array(list(data)) - 0.2, data.values(), width=0.4)
		this_name_bar = ax.bar(np.array(list(this_vacancy_data.keys())) + 0.2, this_vacancy_data.values(), width=0.4)
		ax.legend((first_bar, this_name_bar), (legend, f'{legend} - {dataset.vacancy_name}'), fontsize=8)
		ax.set_xticks(list(data.keys()), list(data.keys()), rotation=90)
		ax.xaxis.set_tick_params(labelsize=8)
		ax.yaxis.set_tick_params(labelsize=8)
		ax.grid(axis='y')

	@staticmethod
	def fill_excel(sheet, data):
		for el in data:
			sheet.append(el)

	@staticmethod
	def set_border(sheet, border, data, columns):
		for i in range(1, len(data) + 1):
			for column in columns:
				sheet[f'{column}{i}'].border = border

	@staticmethod
	def set_font(font, *sheets):
		for sheet in sheets:
			for column in 'ABCDE':
				sheet[f'{column}{1}'].font = font

	@staticmethod
	def set_column_width(data, sheet):
		# from https://stackoverflow.com/questions/13197574/openpyxl-adjust-column-width-size
		column_widths = []
		for row in data:
			for i, cell in enumerate(row):
				cell = str(cell)
				if len(column_widths) > i:
					if len(cell) > column_widths[i]:
						column_widths[i] = len(cell)
				else:
					column_widths += [len(cell)]
		for i, column_width in enumerate(column_widths, 1):
			sheet.column_dimensions[get_column_letter(i)].width = column_width + 2


dataset = DataSet('vacancies_by_year.csv', input('Введите название вакансии: '))
report = Report(*dataset.get_formatted_data())
user_choice = input('Вакансии или статистика? ').lower()
if user_choice == 'вакансии':
	report.generate_image()
elif user_choice == 'статистика':
	report.generate_excel()
else:
	print('Неправильная опция')
