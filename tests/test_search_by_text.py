import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from recurring_functions import (no_departments_search,
                                 select_first_product_with_filter)

implicitly_wait = 10


@pytest.fixture(autouse=True)
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(implicitly_wait)
    browser.get("https://www.amazon.com")
    yield browser
    browser.quit()


@pytest.mark.smoke
def test_search_with_text_low_case(browser):
    text_to_search = "python"
    no_departments_search(browser=browser, input_text=text_to_search)

    select_first_product_with_filter(browser)

    text_product = browser.find_element_by_xpath('//span[@id="productTitle"]').text.lower()
    assert text_to_search in text_product


@pytest.mark.cp
def test_search_with_text_misspell(browser):
    text_to_search = "pythom"
    text_to_search_should_be = "python"
    no_departments_search(browser=browser, input_text=text_to_search)

    text_product = browser.find_element_by_xpath('//a[@class="a-size-medium a-link-normal a-text-bold a-text-italic"]').text
    assert text_to_search_should_be == text_product


@pytest.mark.cp
def test_search_with_text_incorrect_layout(browser):
    text_to_search = "знерщт"
    text_to_search_should_be = "python"
    no_departments_search(browser=browser, input_text=text_to_search)

    try:
        text_product = browser.find_element_by_xpath('//a[@class="a-size-medium a-link-normal a-text-bold a-text-italic"]').text
    except NoSuchElementException:
        raise NoSuchElementException('there is no input error message')
    assert text_to_search_should_be == text_product


@pytest.mark.ext
def test_search_with_text_trim(browser):
    text_to_search = " python "
    text_to_search_should_be = "python"
    no_departments_search(browser=browser, input_text=text_to_search)

    text_search = browser.find_element_by_xpath('//span[@class="a-color-state a-text-bold"]').text
    assert f'"{text_to_search_should_be}"' == text_search


@pytest.mark.ext
def test_search_with_text_large_text(browser):
    text_to_search = 'python '*512
    no_departments_search(browser=browser, input_text=text_to_search)

    search_result = browser.find_elements_by_xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]')
    assert bool(search_result)


@pytest.mark.ext
def test_search_with_text_empty_field(browser):
    text_to_search = "    "
    no_departments_search(browser=browser, input_text=text_to_search)

    search_result = browser.find_elements_by_xpath('//span[@class="a-color-state a-text-bold"]')
    assert not bool(search_result)
