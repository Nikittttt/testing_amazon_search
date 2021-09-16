from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

clearly_wait = 10


def open_departments_in_search(browser, departments):
    open_select_departments = browser.find_element_by_xpath('//div[@class="nav-search-facade"]//..')
    open_select_departments.click()
    select_departments = Select(browser.find_element_by_xpath('//select[@id="searchDropdownBox"]'))
    select_departments.select_by_value(departments)

    button_search = browser.find_element_by_xpath('//input[@id="nav-search-submit-button"]')
    button_search.click()

    WebDriverWait(browser, clearly_wait).until((
        EC.presence_of_element_located((By.XPATH, '//span[text()[contains(.,"Department")]]')))
    )


def no_departments_search(browser, input_text):
    input_search = browser.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
    input_search.send_keys(input_text)

    button_search = browser.find_element_by_xpath('//input[@id="nav-search-submit-button"]')
    button_search.click()


def select_first_product_with_filter(browser):
    WebDriverWait(browser, clearly_wait).until((
        EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))
    )
    first_product = browser.find_element_by_xpath('//div[@data-component-type="s-search-result"]/div/span/div/div/div[2]/div/h2/a')
    first_product.click()

    WebDriverWait(browser, clearly_wait).until((
        EC.presence_of_element_located((By.XPATH, '//span[@id="productTitle"]')))
    )


def get_info_about_product_from_table(browser, param_to_search):
    WebDriverWait(browser, clearly_wait).until((
        EC.presence_of_element_located((By.XPATH, '//table[@class="a-keyvalue prodDetTable"]')))
    )
    param_value = browser.find_element_by_xpath('//table[@class="a-keyvalue prodDetTable"]'
                                                f'//th[text()[contains(.,"{param_to_search}")]]'
                                                '//../td').text
    return param_value

