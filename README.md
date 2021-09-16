# Testing Amazon Search
## Что это?
Набор тестов для поиска в [Amazon](www.amazon.com) в соответствии с [тестовым планом](https://docs.google.com/document/d/18y8Y3ADwIQt-Hpm5Hypv1R0GF2pyu_Sx/edit?usp=sharing&ouid=104217170957615717630&rtpof=true&sd=true).
## Как запустить эти тесты?(версия для linux)
Для начала необходимо установить selenium для python:
```
pip install selenium==3.14.0
```
Далее установим и настроим ChromeDriver(версию совпадающую с версией вашего chromium можно узнеть по ссылке на  https://sites.google.com/a/chromium.org/chromedriver/downloads):
```
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```
Переместите разархивированный файл с СhromeDriver в нужную папку и разрешите запускать chromedriver как исполняемый файл:
```
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
```
Если установка прошла успешно, то у вас должна выполниться:
```
chromedriver
```
Когда всё установленно можно наконец запустить тесты:
```
pytest -q test.py -v --tb=short
```
## Результат тестирования
| Тип теста | Название функции | Проверка | Результат |
| ------ | ------ | ------ | ------ |
| smoke | test_search_no_param | Производится ли поиск по отделу товара |✅ Без проблем |
|critical path|test_search_filter_color|Производится ли поик по цвету товара|✅ Без проблем|
|extended|test_search_filter_climate_pledge_friendly|Производится ли поиск по экологичности товара|✅ Без проблем|
|extended|test_search_filter_from_our_brands|Производится ли поиск по товарам Amazon|✅ Без проблем|
|extended|test_search_filter_featured_brands|Производится ли поиск по брэндам производителя|✅ Без проблем|
|extended|test_search_filter_packaging_option|Производится ли поиск по наличию эко упаковки|❌ Поиск производится успешно, однако в некоторых случаях на странице не прогружается таблица с указанием вариативности упаковки|
|extended|test_search_filter_customer_review|Производится ли поиск по средней оценке товара|✅ Без проблем|
|extended|test_search_filter_new_arrivals|Производится ли поиск по предположительному времени прибытия товара|✅ Без проблем|
|critical path|test_search_filter_price|Производится ли поиск по цене товара|✅ Без проблем|
|smoke|test_search_with_text_low_case|Производится ли поиск по тексту запроса|✅ Без проблем|
|critical path|test_search_with_text_misspell|Определится ли опечатка в ведённом слове|✅ Без проблем|
|critical path|test_search_with_text_incorrect_layout|Определится ли ошибка раскладки клавиатуры в ведённом слове|❌ Ошибка раскладки клавиатуры не была определена|
|extended|test_search_with_text_trim|Производится ли тримация открывающих и закрывающих пробелов|✅ Без проблем|
|extended|test_search_with_text_large_text|Производится ли урезание большого текста под границы при поиске|❌ Не смотря на то что в тесте результат оказался успешным, при ручной проверке на тексте превышающем текущий сгенерированный Amazon выдаёт ошибку(произвести автоматическое тестирование с таким большим текстом не представляется возможным)|
|extended|test_search_with_text_empty_field|Проверка поиска состоящего из пробелов|✅ Без проблем|

