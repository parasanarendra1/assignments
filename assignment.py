import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

test_criteria = [
    {"highlight": "Bestseller", "brand": "Chanel", "type": "Eau de Parfum", "sale": "Yes", "gift_for": "Women",
     "for_whom": "Women", "new": "No", "limited": "No"},
    {"highlight": "New Arrivals", "brand": "Dior", "type": "Eau de Toilette", "sale": "No", "gift_for": "Men",
     "for_whom": "Men", "new": "Yes", "limited": "No"},
]


@pytest.fixture(scope="module")
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.get("https://www.douglas.de/de")
    yield browser
    browser.quit()


def accept_cookies(browser):
    try:
        consent_button = browser.find_element(By.CSS_SELECTOR, ".sc-dcJsrY.eIFzaz")
        consent_button.click()
    except:
        pass


@pytest.mark.parametrize("criteria", test_criteria)
def test_filter_products(setup_driver, criteria):
    browser = setup_driver
    accept_cookies(browser)

    perfume_section = browser.find_element(By.XPATH, "(//font[contains(text(),'PERFUME')])[1]")
    perfume_section.click()

    filters = {
        "highlight": criteria["highlight"],
        "brand": criteria["brand"],
        "type": criteria["type"],
        "sale": criteria["sale"],
        "gift_for": criteria["gift_for"],
        "for_whom": criteria["for_whom"],
        "new": criteria["new"],
        "limited": criteria["limited"],
    }

    for key, value in filters.items():
        try:
            filter_option = browser.find_element(By.XPATH,
                                                 f"(//*[name()='svg'][@class='PtbKk9ogBoi2GdnLM7lW Q2V8KxgHDakQ2L3catrp DjinSukHaeYE56Dx86Jc'])[1], '{value}')]")
            filter_option.click()
        except:
            pass

    products = browser.find_elements(By.XPATH, "(//div[@data-testid='classificationClassName'])[1]")
    assert len(products) > 0, "No products matched the filters."
