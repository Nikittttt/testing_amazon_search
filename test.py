import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from func import (open_departments_in_search,
                  no_departments_search,
                  select_first_product_with_filter,
                  get_info_about_product_from_table,
                  clearly_wait)

implicitly_wait = 10


@pytest.fixture(autouse=True)
def browser():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(implicitly_wait)
    browser.get("https://www.amazon.com")
    yield browser
    browser.quit()


class TestSearch:

    @pytest.mark.smoke
    def test_search_no_param(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        departments_search = browser.find_element_by_xpath('//div[@class="fst-h1-st pageBanner"]/h1/b').text
        assert 'Arts and Crafts' == departments_search

    @pytest.mark.cp
    def test_search_filter_color(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        color_select = browser.find_element_by_xpath('//span[text()[contains(.,"Color")]]//..//../ul/li')
        name_color = color_select.get_attribute("title")
        color_select.click()

        select_first_product_with_filter(browser)

        color_product = get_info_about_product_from_table(browser, "Color")
        assert name_color in color_product

    @pytest.mark.ext
    def test_search_filter_climate_pledge_friendly(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        climate_pledge_friendly_filter = browser.find_element_by_xpath('//span[text()[contains(.,"Climate Pledge Friendly")]]//..//../ul/li/span')
        climate_pledge_friendly_filter.click()

        select_first_product_with_filter(browser)

        climate_pledge_friendly_text = browser.find_element_by_xpath('//a[@class="a-link-normal climatePledgeFriendlyATF"]/span/span').text
        assert climate_pledge_friendly_text == "Climate Pledge Friendly"

    @pytest.mark.ext
    def test_search_filter_from_our_brands(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        from_our_brands_filter = browser.find_element_by_xpath('//span[text()[contains(.,"From Our Brands")]]//..//../ul/li/span')
        from_our_brands_filter.click()

        select_first_product_with_filter(browser)

        climate_pledge_friendly_text = browser.find_element_by_xpath('//span[@class="a-size-small aok-float-left ac-badge-rectangle"]').text
        assert climate_pledge_friendly_text == "Amazon's\nChoice"

    @pytest.mark.ext
    def test_search_filter_featured_brands(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        featured_brands_filter = browser.find_element_by_xpath('//span[text()[contains(.,"Featured Brands")]]//..//../ul/li/span')
        name_of_brand = featured_brands_filter.text
        featured_brands_filter.click()

        select_first_product_with_filter(browser)

        manufacturer_product = get_info_about_product_from_table(browser, "Manufacturer")
        try:
            brand_product = get_info_about_product_from_table(browser, "Brand")
        except NoSuchElementException:
            brand_product = ""
        assert name_of_brand in [manufacturer_product, brand_product]

    @pytest.mark.ext
    def test_search_filter_packaging_option(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        packaging_option_filter = browser.find_element_by_xpath('//span[text()[contains(.,"Packaging Option")]]//..//../ul/li/span')
        packaging_option_filter.click()

        select_first_product_with_filter(browser)

        WebDriverWait(browser, clearly_wait).until((
            EC.presence_of_element_located((By.XPATH, '//table[@id="tabular-buybox-container"]')))
        )
        packaging_text = browser.find_elements_by_xpath('//table[@id="tabular-buybox-container"]'
                                                        '//span[@class="a-truncate-cut"]'
                                                        '//span[@class="a-color-tertiary tabular-buybox-label"]')[-1].text

        assert packaging_text == "Packaging"

    @pytest.mark.ext
    def test_search_filter_customer_review(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        customer_review_filter = browser.find_element_by_xpath('//span[text()[contains(.,"Avg. Customer Review")]]//..//../ul/li/span/a/div')
        min_star = int(customer_review_filter.get_attribute('aria-label').split()[0])
        customer_review_filter.click()

        select_first_product_with_filter(browser)

        current_star_filter = float(browser.find_element_by_xpath('//span[@id="acrPopover"]').get_attribute("title").split()[0])
        assert current_star_filter >= min_star

    @pytest.mark.ext
    def test_search_filter_new_arrivals(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        new_arrivals_filter = browser.find_element_by_xpath('//span[text()[contains(.,"New Arrivals")]]//..//../ul/li/span/a/span')
        delta_days = datetime.timedelta(days=int(new_arrivals_filter.text.split()[1]))
        new_arrivals_filter.click()

        select_first_product_with_filter(browser)

        current_arrival_days = browser.find_element_by_xpath('//div[@id="mir-layout-DELIVERY_BLOCK-slot-DELIVERY_MESSAGE"]/b').text

        date_with_delta = datetime.datetime.now()+delta_days
        year = str(date_with_delta.year)
        maximum_date_for_delta = datetime.datetime.strptime(year+current_arrival_days.split('-')[1], "%Y %b %d")
        assert maximum_date_for_delta <= date_with_delta

    @pytest.mark.cp
    def test_search_filter_price(self, browser):
        open_departments_in_search(browser=browser, departments="search-alias=arts-crafts-intl-ship")

        price_filter = browser.find_element_by_xpath('//span[text()[contains(.,"Price")]]//..//../ul/li/span/a/span')
        price = price_filter.text
        if "Under" in price:
            min_price = None
            max_price = int(price.split('$')[1])
        elif "Above" in price:
            min_price = int(price.split()[0].replace('$', ''))
            max_price = None
        else:
            price = price.splite(' to ')
            min_price = int(price[0].replace('$', ''))
            max_price = int(price[1].replace('$', ''))
        price_filter.click()

        select_first_product_with_filter(browser)

        current_price = browser.find_element_by_xpath('//span[@id="price_inside_buybox"]').text
        current_price = float(current_price.replace('$', ''))

        if not min_price:
            assert current_price <= max_price
        elif not max_price:
            assert min_price <= current_price
        else:
            assert min_price <= current_price <= max_price

    @pytest.mark.smoke
    def test_search_with_text_low_case(self, browser):
        text_to_search = "python"
        no_departments_search(browser=browser, input_text=text_to_search)

        select_first_product_with_filter(browser)

        text_product = browser.find_element_by_xpath('//span[@id="productTitle"]').text.lower()
        assert text_to_search in text_product

    @pytest.mark.cp
    def test_search_with_text_misspell(self, browser):
        text_to_search = "pythom"
        text_to_search_should_be = "python"
        no_departments_search(browser=browser, input_text=text_to_search)

        text_product = browser.find_element_by_xpath('//a[@class="a-size-medium a-link-normal a-text-bold a-text-italic"]').text
        assert text_to_search_should_be == text_product

    @pytest.mark.cp
    def test_search_with_text_incorrect_layout(self, browser):
        text_to_search = "знерщт"
        text_to_search_should_be = "python"
        no_departments_search(browser=browser, input_text=text_to_search)

        try:
            text_product = browser.find_element_by_xpath('//a[@class="a-size-medium a-link-normal a-text-bold a-text-italic"]').text
        except NoSuchElementException:
            raise NoSuchElementException('there is no input error message')
        assert text_to_search_should_be == text_product

    @pytest.mark.ext
    def test_search_with_text_trim(self, browser):
        text_to_search = " python "
        text_to_search_should_be = "python"
        no_departments_search(browser=browser, input_text=text_to_search)

        text_search = browser.find_element_by_xpath('//span[@class="a-color-state a-text-bold"]').text
        assert f'"{text_to_search_should_be}"' == text_search

    @pytest.mark.ext
    def test_search_with_text_large_text(self, browser):
        text_to_search = 'python '*512
        no_departments_search(browser=browser, input_text=text_to_search)

        search_result = browser.find_elements_by_xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]')
        assert bool(search_result)

    @pytest.mark.ext
    def test_search_with_text_empty_field(self, browser):
        text_to_search = "    "
        no_departments_search(browser=browser, input_text=text_to_search)

        search_result = browser.find_elements_by_xpath('//span[@class="a-color-state a-text-bold"]')
        assert not bool(search_result)
