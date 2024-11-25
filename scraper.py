import sys
import time

import requests

from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def fix_url(url) -> str:
    url = urlparse(url)

    path = url.path.replace('/dp/', '/product-reviews/')
    return f'{url.scheme}://{url.netloc}{path}'


def open_page(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get(url)

    if not handle_captcha(driver):
        raise Exception("Captcha not solved or captcha error.")

    reviews = WebDriverWait(driver, timeout=120).until(
        ec.visibility_of_element_located((By.ID, 'cm_cr-review_list'))
    )
    for review in reviews.find_elements(By.XPATH, './>div'):
        star_rating = extract_star_rating(review)
        print(review.text)
    print(reviews)

    # driver.implicitly_wait(10)
    time.sleep(100)

def extract_star_rating(review):
    star_element = review.find_element_by_class_name('a-icon-star')
    class_names = star_element.get_attribute('class').split()
    for class_name in class_names:
        if class_name == 'a-star-1':
            return 1
        elif class_name == 'a-star-2':
            return 2
        elif class_name == 'a-star-3':
            return 3
        elif class_name == 'a-star-4':
            return 4
        elif class_name == 'a-star-5':
            return 5

    return -1

def handle_captcha(driver):
    captcha = WebDriverWait(driver, timeout=120).until(
        ec.invisibility_of_element(
            (By.XPATH, '//h4[text()="Enter the characters you see below"]')
        )
    )

    return captcha


def scrape(url):
    open_page(url)

def handle_sign_in():
    pass


if __name__ == '__main__':
    # if sys.argv[1] == 'scrape':
    product_review_url = fix_url('https://www.amazon.com/DEWALT-Jobsite-Compact-4-Inch-DWE7485/dp/B0842QDW95/')
    scrape(product_review_url)