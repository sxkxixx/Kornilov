import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit


class Analytic:
	def __init__(self, file_name, vacancy_name: str, area_name: str):
		self.frame = pd.read_csv(file_name)
		self.chosen_vacancy = vacancy_name.lower()
		self.chosen_area_name = area_name

	def get_city_simple_analytic(self):
		rows = self.frame.shape[0]
		cities_count = self.frame['area_name'].value_counts().to_dict()
		cities_share = dict(
			filter(lambda x: x[-1] > 0.01, [(key, round(value / rows, 4)) for key, value in cities_count.items()]))
		groups = self.frame.groupby(['area_name'])
		salary_city = {city: round(df['salary'].mean()) for city, df in groups if city in cities_share}
		return dict(sorted(salary_city.items(), key=lambda x: x[-1], reverse=True)[:10]), dict(
			list(cities_share.items())[:10])

	def get_chosen_area_vacancy_analytic(self):
		data = self.frame[(self.frame['area_name'] == self.chosen_area_name) & (
			self.frame['name'].str.contains(self.chosen_vacancy, case=False))]
		data['year'] = data['published_at'].apply(lambda x: x[:4])
		groups = data.groupby(['year'])
		avg_salary, amount = {}, {}
		for year, df in groups:
			avg_salary[year] = round(df['salary'].mean())
			amount[year] = df.shape[0]
		return avg_salary, amount


class Report:
	def __init__(self, vacancy_name, area_name, salary_city, share_city, city_vacancy_salary,
	             city_vacancy_vacancies_amount):
		self.vacancy_name = vacancy_name
		self.area_name = area_name
		self.salary_city = salary_city
		self.share_city = share_city
		self.city_vacancy_salary = city_vacancy_salary
		self.city_vacancy_vacancies_amount = city_vacancy_vacancies_amount

	def generate_pdf(self):
		template = Environment(loader=FileSystemLoader('template')).get_template("pdf_template.html")
		statistic_by_year = [[year, self.city_vacancy_salary[year], self.city_vacancy_vacancies_amount[year]] for year
		                     in self.city_vacancy_vacancies_amount]
		pdf_template = template.render(
			{'name': self.vacancy_name, 'city': self.area_name, 'statistic_by_year': statistic_by_year,
			 'statistic_by_city_salary': self.salary_city.items(), 'statistic_by_share_city': self.share_city.items()})
		config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
		pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={"enable-local-file-access": ""})


# statistic_by_city_salary
# statistic_by_share_city
# file_name = input('Введите название файла: ')
# vacancy_name = input('Введите название профессии: ')
# area_name = input('Введите название региона: ')
analytic = Analytic('data/converted_dif_currencies.csv', 'Аналитик', 'Екатеринбург')
salary_city, share_city = analytic.get_city_simple_analytic()
avg_salary, amount = analytic.get_chosen_area_vacancy_analytic()
report = Report('Аналитик', 'Екатеринбург', salary_city, share_city, avg_salary, amount)
report.generate_pdf()
