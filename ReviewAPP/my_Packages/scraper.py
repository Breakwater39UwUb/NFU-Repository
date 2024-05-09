# https://github.com/MajideND/scraping-reviews-from-googlemaps/blob/main/app.py
import os, re, math, time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from fake_useragent import UserAgent
import pandas as pd
from my_Packages.utils import check_loacal_cache
from datetime import datetime

rating_level_G = [0, 0, 0, 0, 0] # from star 1 to 5, google
rating_level_F = [0, 0, 0, 0, 0] # from star 1 to 5, foodpanda
time_filter = ['年前', '個月前', '週前', '天前']

global webname_filter
invalid_chars = '\n'
invalid_char_pattern = '|'.join(map(re.escape, invalid_chars))
webname_filter = re.compile(invalid_char_pattern)

def get_data(web, t_range):
    global driver
    print('get data...')
    if web == 'Foodpanda':
        return get_foodpanda(web)
    
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
            driver.implicitly_wait(1.5)
            if t_range is None:
                text = data.find_element(
                    By.XPATH, './/div[@class="MyEned"]').text
            
            if t_range is not None:
                # get review time element, ex: "6 個月前"
                time_to_check = data.find_element(
                    By.XPATH, './/span[@class="rsqaWe"]').text
                if valid_time_interval(t_range, time_to_check) == False:
                    continue

            review_time = time_to_check
        except:
            # text = ''
            raise
            # continue
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

        lst_data.append([review_time, score[0], text])

    return lst_data

def get_foodpanda(web):
    global driver
    print('get_foodpanda...')

    xpath = '//div[@class="info-reviews-modal-review-card"]'
    elements = driver.find_elements(By.CLASS_NAME, 'info-reviews-modal-review-card')
    lst_data = []

    for data in elements:
        driver.implicitly_wait(1)
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

def valid_time_interval(time_interval:list[str], to_check:str):
    pos = 0
    time = ''
    valid_num = int(time_interval[0])
    valid_time = time_interval[1]
    valid_interval = time_interval[2]

    # Find date in review text
    list_ = to_check.split()
    # for target in list_:
    #     if time_interval[1] in target:
    #         check_num = int(list_[pos-1])
    #         check_time = target
    #         break
    #     pos += 1

    if list_[1] not in time_interval[1]:
        return False
    
    check_num = int(list_[0])
    check_time = list_[1]

    # review: "time" ago != "valide time" ago
    if check_time != valid_time:
        return False
    if valid_interval == 'after':
        if check_num > valid_num:
            return False
    if valid_interval == 'before':
        if check_num < valid_num:
            return False
    return True

def counter(web):
    print('Jumping to review tab')
    
    global driver
    # driver.implicitly_wait(1)
    result = None
    if web == 'Googlemaps':
        review_btn_xpath = '//div[@class="RWPxGd"]/button[2]'
        class_name_1 = 'jANrlb'
        class_name_2 = 'fontBodySmall'
        x = 0
        try:
            reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            reviewBTN.click()
            driver.implicitly_wait(2)
            result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.CLASS_NAME, class_name_2).text
        except selenium.common.exceptions.StaleElementReferenceException as sere:
            print(sere, sere.args)
        except selenium.common.exceptions.NoSuchElementException as nsee:
            print(nsee, nsee.args)
        else:
            reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            reviewBTN.click()
            result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.CLASS_NAME, class_name_2).text
        finally:
            if result is None:
                return
            result = result.replace(',', '').replace('(', '').replace(')', '').replace('+', '')
            result = result.split(' ')
            result = result[x].split('\n')
            counts = int(int(result[0])/10)+1
            print(counts)
            return counts

    elif web == 'Foodpanda':
        review_btn_xpath = '//*[@id="vendor-details-root"]/main/section[2]/div/div[3]/div[1]/div[2]/button'
        review_btn_name = 'bds-c-btn bds-c-btn-text bds-c-btn--size-small bds-is-idle bds-c-btn--layout-default bds-c-btn--remove-side-spacing zi-surface-base'
        class_name_1 = 'ratings-summary-section'
        class_name_2 = '//*[@id="info-reviews-content"]/div/div/div[1]/div/div/div[1]/div[3]/div'
        x = 1
        try:
            reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            reviewBTN.click()
            driver.implicitly_wait(1)
            xpath = '//*[@id="info-reviews-content"]/div/div/div[1]/div/div/div[1]/div[3]'
            result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.XPATH, xpath).find_element(By.XPATH, class_name_2).text
        except selenium.common.exceptions.StaleElementReferenceException as sere:
            print(sere, sere.args)
        except selenium.common.exceptions.NoSuchElementException as nsee:
            print(nsee, nsee.args)
        else:
            driver.implicitly_wait(2)
            reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            reviewBTN.click()
            xpath = '//*[@id="info-reviews-content"]/div/div/div[1]/div/div/div[1]/div[3]'
            result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.XPATH, xpath).find_element(By.XPATH, class_name_2).text
    
            result = result.replace(',', '').replace('(', '').replace(')', '').replace('+', '')
            result = result.split(' ')
            result = result[x].split('\n')
            return int(int(result[0])/10)+1

def scrolling(counter, web):
    print('scrolling...')

    global driver
    if web == 'Foodpanda':
        # btn_name = 'bds-c-btn bds-c-btn-circular bds-c-btn-circular-contained bds-c-btn-circular--size-medium zi-surface-base bds-c-modal__close-button'
        # btn_path = '/html/body/div[5]/div/div[2]/div/div/div/div/div[1]/button'
        # div_path = '/html/body/div[5]/div/div[2]/div/div/div/div/div[1]'
        # div_name = 'bds-c-btn-cursor bds-c-modal__close-button-cursor'
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
    elif web == 'Googlemaps':
        # # <div class="m6QErb DxyBCb kA9KIf dS8AEf ">
        # scrollable_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
        # # <div class="m6QErb " style> //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]
        # height_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]'
        # element = driver.find_element(By.XPATH, scrollable_xpath)
        # review_block = driver.find_element(By.XPATH, height_xpath)
        # size = element.size
        # w = size['width'] 
        # h = size['height']

        # #Calculate where to click
        # click_place_x = math.floor(w / 2)-1
        # click_place_y = math.floor(h / 2)-1

        # last_h = 0
        # current_h = 0
        # # max_h = 370*counter*10
        # while True:
        #     last_h = review_block.size['height']
        #     ActionChains(driver).move_to_element(element)\
        #         .move_by_offset(click_place_x, click_place_y)\
        #         .click_and_hold().perform()
        #     driver.implicitly_wait(3)
        #     # time.sleep(1)
        #     current_h = review_block.size['height']
        #     if current_h > last_h:
        #         pass
        #     else:
        #         ActionChains(driver).move_to_element(element)\
        #         .move_by_offset(click_place_x, click_place_y)\
        #         .release().perform()
        #         print('Scrolled tp bottom')
        #         return

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
            time.sleep(1)

def write_to_xlsx(data, filename, dir, format):
    filepath = os.path.join(dir, filename) + '.' + format
    print(f'write to {filepath}...')
    cols = ['time','rating', 'comment']
    df = pd.DataFrame(data, columns=cols) # this insert the head
    # df = pd.DataFrame(data) # headless column name
    if format == 'csv':
        df.to_csv(filepath, encoding='utf-8', index=False, header=None)
    
    if format == 'json':
        df.to_json(filepath, orient='records', indent=4, force_ascii=False)
    
    return filepath

def get_reviews(url: str = None,
                webname: str = 'Googlemaps',
                save_path: str = 'SaveData',
                format: str = None,
                time_range: list[str] = None,
                check_cache: bool = False):
    '''
    Get reviews on Googlemap or Foodpanda
    * url: website url at "Overview Tab"
    * webname: It is set by selecting platform
    * save_path: Where the data will be saved
    * format: Filename extension(filename suffix) of saved data
    * time_range: Time range to scrape the reviews
          * None: all the time
          * example:['1', '個月前', 'after']
    * check_cache: Whether to check cache or not
    
    urls to test check_cache
        * https://www.google.com/maps/place/%E5%B0%8F%E8%B1%A1%E9%A4%90%E5%BB%B3/@24.1471015,120.6817869,17z/data=!3m1!4b1!4m6!3m5!1s0x34693d694363448f:0x89413bc624180d69!8m2!3d24.1470966!4d120.6843565!16s%2Fg%2F11b6q1y2q8?authuser=0&entry=ttu
        * https://www.google.com/maps/place/%E6%99%A8%E9%96%93%E5%BB%9A%E6%88%BF%E6%97%A9%E5%8D%88%E9%A4%90+%E8%99%8E%E5%B0%BE%E7%A7%91%E5%A4%A7%E5%BA%97/@23.7037418,120.4346679,19.5z/data=!4m6!3m5!1s0x346eb0aaa1358941:0x2401c8b48788a7d4!8m2!3d23.7035352!4d120.4346529!16s%2Fg%2F11c5rp098z?hl=zh-tw&entry=ttu

    Returns the path of saved file
    '''
    if url is None:
        raise Exception('url is None, string is required')
    elif type(url) is not str:
        raise Exception('url must be a string')

    if format is None:
        format = 'csv'
    elif type(format) is not str:
        raise Exception('format must be a string')
    elif format not in ['csv', 'json']:
        raise Exception('format must be csv or json')
    
    if  time_range is not None:
        if not all(isinstance(elem, str) for elem in time_range):
            raise Exception(f'Argument format required list of strings')
        elif time_range[1] not in time_filter:
            raise Exception(f'Argument format must be one of {time_filter}')

    
    print(f'Find reviews on {url}...')

    try:
        # setup webdriver options
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument("--head")  # show browser or not
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--lang=en-US")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_extension('.\\Data_local\\Mouse-Coordinates.crx')
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'--user-agent={user_agent}')
        global driver
        driver = webdriver.Chrome(options=options)
        # get web from the url
        driver.get(url) # uncomment this line
        
        # wait for web is properly loaded
        try:
            wait = WebDriverWait(driver, timeout=2)
            wait.until(lambda d : driver.is_displayed())
        except:
            pass
        
        # format the web title for further use
        # webTitle = driver.title.replace(' ', '').split('|')[0]
        global webname_filter
        webTitle = webname_filter.sub('', driver.title)
        if check_loacal_cache(query=webTitle, query_dir=save_path, file_type=format) and \
            check_cache:
            cached_path = os.path.join(save_path, webTitle) + f'.{format}'
            print(f'Already cached: {cached_path}')
            return cached_path
        
        # count for scrolling
        counts = counter(driver, webname)

        # scroll to the bottom of the page
        scrolling(driver, counts, webname)

        # get reviews on the web
        data = get_data(driver, webname, time_range)

        # write reviews to csv file
        file = write_to_xlsx(data, webTitle, save_path, format)
        print(f'Your restaurant review file is saved to {file}')
        return file
    # except:
        # print('Failed to scrape web')
    finally:
        driver.quit()
        # os.system("taskkill /f /im chrome.exe")
