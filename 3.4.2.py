import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit


class Analytic:
	def __init__(self, file_name, vacancy_name: str):
		self.frame = pd.read_csv(file_name)
		self.chosen_vacancy = vacancy_name.lower()

	def get_file_analytic(self):
		self.frame['year'] = self.frame['published_at'].apply(lambda x: x[:4])
		groups = self.frame.groupby(['year'])
		salary, vacancies_amount, this_vacancy_salary, this_vacancy_amount = {}, {}, {}, {}
		for year, df in groups:
			amount, avg_salary, chosen_vacancy_amount, chosen_vacancy_avg_salary = self.get_year_analytic(df)
			salary[year] = avg_salary
			vacancies_amount[year] = amount
			this_vacancy_salary[year] = chosen_vacancy_avg_salary
			this_vacancy_amount[year] = chosen_vacancy_amount
		return salary, vacancies_amount, this_vacancy_salary, this_vacancy_amount

	def get_year_analytic(self, df: pd.DataFrame):
		df_chosen_vacancy = df[df['name'].str.contains(self.chosen_vacancy, case=False)]
		average_salary = round(df.apply(lambda x: x['salary'] * 0.5, axis=1).mean())
		this_vacancy_salary_average = round(
			df_chosen_vacancy.apply(lambda x: x['salary'] * 0.5, axis=1).mean())
		return df.shape[0], average_salary, df_chosen_vacancy.shape[0], this_vacancy_salary_average

	def get_city_analytics(self):
		rows = self.frame.shape[0]
		cities_count = self.frame['area_name'].value_counts().to_dict()
		cities_share = dict(
			filter(lambda x: x[-1] > 0.01, [(key, round(value / rows, 4)) for key, value in cities_count.items()]))
		groups = self.frame.groupby(['area_name'])
		salary_city = {}
		for city, df in groups:
			if city not in cities_share:
				continue
			salary_city[city] = round(df['salary'].mean())
		return dict(sorted(salary_city.items(), key=lambda x: x[-1], reverse=True)), cities_share


class Report:
	def __init__(self, vacancy_name, salary, amount, this_vacancy_salary, this_vacancy_amount, salary_city=None, share_city=None):
		self.vacancy_name = vacancy_name
		self.salary = salary
		self.amount = amount
		self.this_vacancy_salary = this_vacancy_salary
		self.this_vacancy_amount = this_vacancy_amount
		self.salary_city = salary_city
		self.share_city = share_city

	def generate_pdf(self):
		template = Environment(loader=FileSystemLoader('template')).get_template("pdf_template.html")
		statistic = [
			[year, self.salary[year], self.this_vacancy_salary[year], self.amount[year], self.this_vacancy_amount[year]]
			for year in self.salary]
		pdf_template = template.render({'name': self.vacancy_name, 'statistic': statistic})
		config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
		pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={"enable-local-file-access": ""})


file_name = input('Введите название файла: ')
vacancy_name = input('Введите название профессии: ')
analytic = Analytic(file_name, vacancy_name)
salary, amount, this_vacancy_salary, this_vacancy_amount = analytic.get_file_analytic()
report = Report(vacancy_name, salary, amount, this_vacancy_salary, this_vacancy_amount)
report.generate_pdf()