# Результаты выполнения тестов
## Результат doctests
![img_1.png](img/img_11.png)
## Результат unittest
![img_2.png](img/img_12.png)


# Результаты профилирования кода:
### В программе представлены 5 функций для парсинга даты
* test_datetime_strptime
![img_1.png](img/img_1.png)
* test_parsing_with_slices
![img_2.png](img/img_2.png)
* test_parsing_with_format
![img_3.png](img/img_3.png)
* test_parsing_dateutil_parse....
![img_4.png](img/img_4.png)
* test_parsing_with_split
* ![img_5.png](img/img_5.png)
### Вывод: Функция "test_parsing_with_slices" показала наилучший результат на большом объеме данных. Использование библиотек приводит к большим трудозатратам

# Результат профилирование кода обработки csv-чанков
## Без многопроцессорности
![img_6.png](img/img_6.png)
## С многопроцессорностью
![img_7.png](img/img_7.png)
## С использованием concurrent.futures.ProcessPoolExecutor()
![img.png](img/img_8.png)

# 3.3.1
## Частотность валют в файле vacancies_dif_currencies.csv
![img.png](img/img_9.png)
## Дата публикации самой старой и самой новой вакансии!
![img_2.png](img/img_10.png)
## Результат задания 3.3.1 в csv
![img.png](img/img_13.png)

# Задание 3.4.2, пример PDF-отчета
![img.png](img/img_14.png)
# Задание 3.4.3, пример PDF-отчета
![img.png](img/img_15.png)