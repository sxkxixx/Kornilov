import pandas as pd
import xmltodict
import grequests

data = pd.read_csv('data/vacancies_dif_currencies.csv',
                   usecols=['salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
filtered_data = data[pd.notnull(data['salary_currency']) & data['salary_currency'].notna()]


def reverse_date(date):
	return f'{date[8:]}/{date[5:7]}/{date[:4]}'


def convert_date(date):
	return f'{date[6:]}-{date[3:5]}'


class Worker:
	def __init__(self, data):
		self.data = data

	def get_currencies_amount(self):
		return self.data['salary_currency'].value_counts().to_dict()

	def get_currencies_code(self):
		return list(map(lambda x: x[0], filter(lambda x: x[-1] > 5000, self.get_currencies_amount().items())))

	def get_currencies_frequencies(self):
		vacancies_amount = self.data.shape[0]
		return {currency: amount / vacancies_amount for currency, amount in self.get_currencies_amount().items()}

	def get_newest_oldest_date(self):
		years_series = pd.to_datetime(self.data['published_at'].apply(lambda x: x[:10]))
		return reverse_date(str(years_series.min())[:10]), reverse_date(str(years_series.max())[:10])

	def get_range_dates(self):
		oldest, newest = self.get_newest_oldest_date()
		return pd.date_range(start=oldest, end=newest, freq='M').strftime('%d/%m/%Y').tolist()

	@property
	def urls(self):
		return [f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}' for date in self.get_range_dates()]

	def get_response(self):
		currencies_code = self.get_currencies_code()
		currencies_code.remove('RUR')
		dct = {'date': []}
		dct.update({code: [] for code in currencies_code})
		response = (grequests.get(url) for url in self.urls)
		for r in grequests.map(response):
			data = xmltodict.parse(r.text)['ValCurs']
			date = convert_date(data['@Date'])
			dct['date'] = dct['date'] + [date]
			currency_value = {code: None for code in currencies_code}
			for currency in data['Valute']:
				code = currency['CharCode']
				if code in currencies_code:
					nominal = float(currency['Nominal'])
					currency_value[code] = round(float(currency['Value'].replace(',', '.')) / nominal, 6)
			for code, value in currency_value.items():
				dct[code] = dct[code] + [value]
		pd.DataFrame(dct).to_csv(path_or_buf='currency_value.csv', index=False, encoding='utf-8-sig')


worker = Worker(filtered_data)
worker.get_response()
