# https://github.com/MajideND/scraping-reviews-from-googlemaps/blob/main/app.py
import math
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy, ProxyType
import undetected_chromedriver as uc
import pandas as pd
import env

rating_level_G = [0, 0, 0, 0, 0] # from star 1 to 5, google
rating_level_F = [0, 0, 0, 0, 0] # from star 1 to 5, foodpanda
def get_data(driver, web):
    print('get data...')
    if web == 'Foodpanda':
        return get_foodpanda(driver, web)
    
    try:
        # xpath = '//*[@id="ChdDSUhNMG9nS0VJQ0FnSURXdF9fSDFnRRAB"]/span[2]/button'
        xpath = '//button[@class="w8nwRe kyuRq"]'
        more_elemets = driver.find_elements(By.XPATH, xpath)
        for list_more_element in more_elemets:
            list_more_element.click()
    except:
        pass
    
    # xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[1]'
    elements = driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium "]')
    lst_data = []
    for data in elements:
        try:
            text = data.find_element(
                By.XPATH, './/div[@class="MyEned"]').text
        except:
            text = ''
        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[22]/div/div/div[4]/div[1]/span[1]
        score = data.find_element(
            By.XPATH, './/span[@class="kvMYJc"]').get_attribute("aria-label")

        if score[0] == '1':
            rating_level_G[0] += 1
        elif score[0] == '2':
            rating_level_G[1] += 1
        elif score[0] == '3':
            rating_level_G[2] += 1
        elif score[0] == '4':
            rating_level_G[3] += 1
        elif score[0] == '5':
            rating_level_G[4] += 1

        lst_data.append([text, score[0]])

    return lst_data

def get_foodpanda(driver, web):
    print('get_foodpanda...')
    if web == 'Ubereat':
        get_ubereat(driver)
        return

    xpath = '//div[@class="info-reviews-modal-review-card"]'
    elements = driver.find_elements(By.CLASS_NAME, 'info-reviews-modal-review-card')
    lst_data = []
    for data in elements:
        text = data.find_element(
            By.CLASS_NAME, 'info-reviews-modal-description').text
        score = data.find_element(By.XPATH, '//div[@class="info-reviews-modal-card-subtitle"]')
        stars = score\
                .find_elements(By.CLASS_NAME, 'rating--star-type-full')
        rating = len(stars)
        
        if rating == 1:
            rating_level_G[0] += 1
        elif rating == 2:
            rating_level_G[1] += 1
        elif rating == 3:
            rating_level_G[2] += 1
        elif rating == 4:
            rating_level_G[3] += 1
        elif rating == 5:
            rating_level_G[4] += 1
        
        lst_data.append([text, rating])

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
                .click().perform()
            time.sleep(0.02)
            current_h = review_block.size['height']
            if current_h <= last_h:
                print('Scrolled tp bottom')
                return
    # elif web == 'Googlemaps':
    #     # <div class="m6QErb DxyBCb kA9KIf dS8AEf ">
    #     scrollable_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
    #     # <div class="m6QErb " style> //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]
    #     height_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]'
    #     element = driver.find_element(By.XPATH, scrollable_xpath)
    #     review_block = driver.find_element(By.XPATH, height_xpath)
    #     size = element.size
    #     w = size['width'] 
    #     h = size['height']

    #     #Calculate where to click
    #     click_place_x = math.floor(w / 2)-1
    #     click_place_y = math.floor(h / 2)-10

    #     last_h = 0
    #     current_h = 0
    #     max_h = 370*counter*10
    #     while True:
    #         last_h = review_block.size['height']
    #         ActionChains(driver).move_to_element(element)\
    #             .move_by_offset(click_place_x, click_place_y)\
    #             .click_and_hold().perform()
    #         driver.implicitly_wait(3)
    #         current_h = review_block.size['height']
        
    #         if current_h > last_h:
    #             pass
    #         else:
    #             print('Scrolled tp bottom')
    #             return

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
        time.sleep(2)

def write_to_xlsx(data, filename):
    print(f'write to {filename}.csv...')
    dir = '.\Reviews Scraper\data\\'
    filename = filename.replace('/', ' ').replace('\\', ' ')
    filepath = dir + filename + '.csv'
    cols = ["comment", 'rating']
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(filepath, encoding='utf-8', index=False)

def save_ratings(webname):
    if webname == 'Googlemaps':
        total = sum(rating_level_G)
        star_rates = ['0', '0', '0', '0', '0']
        ls = rating_level_G.copy()
            
        for i in range(len(rating_level_G)):
            ls[i] = str(i+1) + ' star: ' + str(ls[i]) + ', rate: ' +\
                    str(int(rating_level_G[i]) / total) + '%' + '\n'
            print(ls[i])
            # star_rates[i] = str(int(rating_level_G[i]) / total)
        open("rating level(Google).txt", "w").writelines(ls)
    else:
        total = sum(rating_level_F)
        star_rates = ['0', '0', '0', '0', '0']
        ls = rating_level_F.copy()

        for i in range(len(rating_level_F)):
            ls[i] = str(i+1) + ' star' + str(ls[i]) + '\n'
            star_rates[i] = str(rating_level_F[i] / total)
        open("rating level(Foodpanda).txt", "w").writelines(star_rates)
        open("rating level(Foodpanda).txt", "a").writelines(ls)


if __name__ == "__main__":
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = "122.117.162.248:1080"
    for pages in env.FPs:
        options = webdriver.ChromeOptions()
        options.add_argument("--headed")  # show browser or not
        options.add_argument("--lang=en-US")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_extension(".\Drivers\Proxy-SwitchyOmega.crx")
        options.add_extension(".\Drivers\\reCAPTCHA-Solver-auto-captcha-bypass.crx")
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'--user-agent={user_agent}')
        # driver = webdriver.Chrome(options=options)
        driver = uc.Chrome(headless=True, use_subprocess=False)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        print(driver.execute_script("return navigator.userAgent;"))
        print(f'scraping {pages}...')
        driver.get(pages)
        try:
            wait = WebDriverWait(driver, timeout=5)
            wait.until(lambda d : driver.is_displayed())
        except:
            pass
        webTitle, webname = set_args(driver)
        driver.save_screenshot('nowsecure.png')

        counts = counter(webname)
        scrolling(counts, webname)

        data = get_data(driver, webname)
        driver.close()

        write_to_xlsx(data, webTitle)
        save_ratings(webname)

    print('Done!')