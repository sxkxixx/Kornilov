# Результаты выполнения тестов
## Результат doctests
![img_1.png](testing_result/img_1.png)
## Результат unittest
![img_2.png](testing_result/img_2.png)


# Результаты профилирования кода:
### В программе представлены 5 функций для парсинга даты
* test_datetime_strptime
![img_1.png](profiling_results/img_1.png)
* test_parsing_with_slices
![img_2.png](profiling_results/img_2.png)
* test_parsing_with_format
![img_3.png](profiling_results/img_3.png)
* test_parsing_dateutil_parse....
![img_4.png](profiling_results/img_4.png)
* test_parsing_with_split
* ![img_5.png](profiling_results/img_5.png)
## Вывод: Функция "test_parsing_with_slices" показала наилучший результат на большом объеме данных
## Использование библиотек приводит к большим трудозатратам

# Результат профилирование кода обработки csv-чанков
## Без многопроцессорности
![img_6.png](profiling_results/img_6.png)
## С многопроцессорностью
![img_7.png](profiling_results/img_7.png)
