# https://github.com/MajideND/scraping-reviews-from-googlemaps/blob/main/app.py
import math
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import pandas as pd
import env
import subprocess
import sys

def get_data(driver, web):
    print('get data...')
    if web == 'Foodpanda':
        return get_foodpanda(driver, web)
    
    try:
        xpath = '//*[@id="ChdDSUhNMG9nS0VJQ0FnSUNtem9hZ3RBRRAB"]/span[2]/button'
        more_elemets = driver.find_elements(By.XPATH, xpath)
        for list_more_element in more_elemets:
            list_more_element.click()
    except:
        pass
    
    # xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[1]'
    elements = driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium "]')
    lst_data = []
    for data in elements:
        name = data.find_element(
            By.XPATH, './/div[@class="d4r55 "]').text
        try:
            text = data.find_element(
                By.XPATH, './/div[@class="MyEned"]').text
        except:
            text = ''
        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[22]/div/div/div[4]/div[1]/span[1]
        score = data.find_element(
            By.XPATH, './/span[@class="kvMYJc"]').get_attribute("aria-label")
        ago = data.find_element(
            By.XPATH, './/span[@class="rsqaWe"]').text

        lst_data.append([name + " from GoogleMaps", text, score[0], ago])

    return lst_data

def get_foodpanda(driver, web):
    print('get get_foodpanda...')
    if web == 'Ubereat':
        get_ubereat(driver)
        return

    xpath = '//div[@class="info-reviews-modal-review-card"]'
    elements = driver.find_elements(By.CLASS_NAME, 'info-reviews-modal-review-card')
    lst_data = []
    for data in elements:
        name = data.find_element(
            By.CLASS_NAME, 'info-reviews-modal-reviewer-name').text
        text = data.find_element(
            By.CLASS_NAME, 'info-reviews-modal-description').text
        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[22]/div/div/div[4]/div[1]/span[1]
        score = data.find_element(By.XPATH, '//div[@class="info-reviews-modal-card-subtitle"]')
        stars = score\
                .find_elements(By.CLASS_NAME, 'rating--star-type-full')
        ago = score.find_element(
            By.CLASS_NAME, 'vendor-info-modal-review-date').text

        lst_data.append([name + " from Foodpanda", text, len(stars), ago])

    return lst_data

def get_ubereat(driver):
    print('Getting Ubeeeerrrerrer')

def set_args(driver):
    'return (title, webname)'
    args = (driver.title.replace(' ', '').split('|')[0],)
    if 'maps' in driver.current_url:
        args += ('Googlemaps',)
    elif 'foodpanda' in driver.current_url:
        args += ('Foodpanda',)
    return args

def counter(web):
    print('Jumping to review tab')
    if web == 'Googlemaps':
        review_btn_xpath = '//div[@class="RWPxGd"]/button[2]'
        class_name_1 = 'jANrlb'
        class_name_2 = 'fontBodySmall'
        x = 0
        reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
        reviewBTN.click()
        result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.CLASS_NAME, class_name_2).text
    elif web == 'Foodpanda':
        review_btn_xpath = '//*[@id="vendor-details-root"]/main/section[2]/div/div[3]/div[1]/div[2]/button'
        review_btn_name = 'bds-c-btn bds-c-btn-text bds-c-btn--size-small bds-is-idle bds-c-btn--layout-default bds-c-btn--remove-side-spacing zi-surface-base'
        class_name_1 = 'ratings-summary-section'
        class_name_2 = '//*[@id="info-reviews-content"]/div/div/div[1]/div/div/div[1]/div[3]/div'
        x = 1
        reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
        reviewBTN.click()
        time.sleep(1)
        xpath = '//*[@id="info-reviews-content"]/div/div/div[1]/div/div/div[1]/div[3]'
        result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.XPATH, xpath).find_element(By.XPATH, class_name_2).text
    
    result = result.replace(',', '').replace('(', '').replace(')', '').replace('+', '')
    result = result.split(' ')
    result = result[x].split('\n')
    return int(int(result[0])/10)+1

def scrolling(counter, web):
    print('scrolling...')
    if web == 'Foodpanda':
        btn_name = 'bds-c-btn bds-c-btn-circular bds-c-btn-circular-contained bds-c-btn-circular--size-medium zi-surface-base bds-c-modal__close-button'
        btn_path = '/html/body/div[5]/div/div[2]/div/div/div/div/div[1]/button'
        div_path = '/html/body/div[5]/div/div[2]/div/div/div/div/div[1]'
        div_name = 'bds-c-btn-cursor bds-c-modal__close-button-cursor'
        element = driver.find_element(By.CLASS_NAME, 'bds-c-modal__content-window')
        review_block = driver.find_element(By.CLASS_NAME, 'info-reviews-block')
        size = element.size
        w = size['width'] 
        h = size['height']

        #Calculate where to click
        click_place_x = math.floor(w / 2)-1
        click_place_y = math.floor(h / 2)-20

        last_h = review_block.size['height']
        current_h = 0
        while True:
            ActionChains(driver).move_to_element(element)\
                .move_by_offset(click_place_x, click_place_y)\
                .click_and_hold().perform()
            time.sleep(0.02)
            current_h = review_block.size['height']
            if current_h <= last_h:
                print('Scrolled tp bottom')
                return

    scrollable_div = driver.find_element(
        By.XPATH, '//div[@class="lXJj5c Hk4XGb "]')
    
    for _i in range(counter):
        try:
            scrolling = driver.execute_script(
                'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
                scrollable_div
            )
        except:
            pass
        time.sleep(3)

def write_to_xlsx(data, filename):
    print(f'write to {filename}.csv...')
    dir = '.\Google Maps Reviews Scraper\\'
    filepath = dir + filename + '.csv'
    cols = ["name", "comment", 'rating', 'time']
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(filepath, encoding='utf-8')

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    for pkg in env.packages:
        install(pkg)

    for pages in env.URLs:
        print(f'scraping {pages}...')
        options = webdriver.ChromeOptions()
        options.add_argument("--head")  # show browser or not
        options.add_argument("--lang=en-US")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'--user-agent={user_agent}')
        driver = webdriver.Chrome(options=options)
        driver.get(pages)
        try:
            wait = WebDriverWait(driver, timeout=2)
            wait.until(lambda d : driver.is_displayed())
        except:
            pass
        webTitle, webname = set_args(driver)
        time.sleep(3)

        counts = counter(webname)
        scrolling(counts, webname)

        data = get_data(driver, webname)
        driver.close()

        write_to_xlsx(data, webTitle)
        print('Done!')