import grequests
import pandas as pd

urls = [
	f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-22T00:00:00&date_to=2022-12-22T08:00:00'
	for page in range(20)]
urls += [
	f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-22T08:00:00&date_to=2022-12-22T16:00:00'
	for page in range(20)]
urls += [
	f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-22T16:00:00&date_to=2022-12-23T00:00:00'
	for page in range(20)]


def parse_vacancy(vacancy):
	name, area_name, published_at = vacancy['name'], vacancy['area']['name'], vacancy['published_at']
	salary_from, salary_to, salary_currency = None, None, None
	salary = vacancy['salary']
	if salary:
		salary_from = salary['from']
		salary_to = salary['to']
		salary_currency = salary['currency']
	return name, salary_from, salary_to, salary_currency, area_name, published_at


responses = (grequests.get(url) for url in urls)
vacancies = []

for response in grequests.map(responses):
	for vacancy in response.json()['items']:
		vacancies.append(parse_vacancy(vacancy))

titles = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']

df = pd.DataFrame(data=vacancies, columns=titles)
df.to_csv('data/api_vacancies.csv', index=False)
print(df.shape[0])
# Получилось 4508 вакансий за 22.12.2022
# Из-за большого размера файла прикрепить его в репозиторий не получается