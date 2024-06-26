# https://github.com/MajideND/scraping-reviews-from-googlemaps/blob/main/app.py
import os, math, time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from fake_useragent import UserAgent
import pandas as pd
from my_Packages import utils
from my_Packages.utils import (
    check_loacal_cache,
    get_review_abs_time,
    valid_time_interval,
    create_dir,
    Debug_Logger
)
from my_Packages.db_update import(
    check_exist_table,
    get_top_review
)

info_logger = Debug_Logger('Scraper_modules', 20, 'INFO.log')
debug_logger = Debug_Logger('Scraper_modules', 10, 'DEBUG.log')

def get_data(web, t_range):
    global driver
    info_logger.log('Get reviews from web.')
    if web == 'Foodpanda':
        return get_foodpanda(web)
    
    try:
        # xpath = '//*[@id="ChdDSUhNMG9nS0VJQ0FnSURXdF9fSDFnRRAB"]/span[2]/button'
        xpath = '//button[@class="w8nwRe kyuRq"]'
        more_elemets = driver.find_elements(By.XPATH, xpath)
        for list_more_element in more_elemets:
            list_more_element.click()
    except:
        # debug_logger.log('', 30)
        raise
    
    # xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[1]'
    elements = driver.find_elements(By.XPATH, './/div[@class="jftiEf fontBodyMedium "]')
    lst_data = []

    if check_exist_table(web):
        newest_review = get_top_review(web)
    else:
        newest_review = None
    for data in elements:
        try:
            driver.implicitly_wait(1.5)
            
            # Review content, string
            text = data.find_element(By.XPATH, './/div[@class="MyEned"]').text
            text = utils.comma_filter.sub('，', text)
            
            # Add function to check if current review is duplicated from newest data in database.
            # if current review is duplicated, break loop.
            if newest_review is not None and text == newest_review:
                break

            # get review time element, ex: "6 個月前"
            time_to_check = data.find_element(
                By.XPATH, './/span[@class="rsqaWe"]').text
            
            if t_range is not None:
                if valid_time_interval(t_range, time_to_check) == False:
                    continue
            # Review time, string
            review_time = get_review_abs_time(time_to_check)
        except:
            # text = ''
            raise
            # continue
        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[8]/div[22]/div/div/div[4]/div[1]/span[1]
            
        score = data.find_element(
            By.XPATH, './/span[@class="kvMYJc"]').get_attribute("aria-label")

        lst_data.append([review_time, score[0], text])

    return lst_data

def get_foodpanda(web):
    global driver
    info_logger.log('get_foodpanda...')

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
        
        lst_data.append([text, rating])

    return lst_data

def counter(web):
    global driver
    # driver.implicitly_wait(1)
    result = None
    if web == 'Googlemaps':
        review_btn_xpath = '//div[@class="RWPxGd"]/button[2]'
        class_name_1 = 'jANrlb '
        class_name_2 = 'fontBodySmall'
        x = 0
        try:
            # TODO: Change print statement to logging or delete
            info_logger.log('Jumping to review tab.')
            reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            reviewBTN.click()
            driver.implicitly_wait(2)
            result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.CLASS_NAME, class_name_2).text
            
            # click newest button
            # driver.execute_script('document.getElementsByClassName("g88MCb S9kvJb ")[2].click();')
            # time.sleep(0.1)
            # driver.execute_script('document.getElementsByClassName("fxNQSd")[1].click();')
            # print('Clicking sort by newest button')
            # xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button'
            # order_btn = driver.find_element(By.XPATH, xpath)
            # order_btn.click()
            # time.sleep(0.5)
            # drop_menu = driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
            # drop_menu.click()
            # time.sleep(2)
            # order_btn = driver.find_elements(By.XPATH, '//button[@class="g88MCb S9kvJb"]')
            # order_btn[2].click()
            # time.sleep(0.5)
            # drop_menu = driver.find_elements(By.XPATH, '//button[@class="fxNQSd"]')[1]
            # drop_menu.click()
            # time.sleep(1.5)
        except selenium.common.exceptions.StaleElementReferenceException as sere:
            debug_logger.log((sere, sere.args), 30)
        except selenium.common.exceptions.NoSuchElementException as nsee:
            debug_logger.log((nsee, nsee.args), 30)
        except:
            raise
        else:
            pass
            # reviewBTN = driver.find_element(By.XPATH, review_btn_xpath)
            # reviewBTN.click()
            # result = driver.find_element(By.CLASS_NAME, class_name_1).find_element(By.CLASS_NAME, class_name_2).text

            # xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button'
            # order_btn = driver.find_element(By.XPATH, xpath)
            # order_btn.click()
            # time.sleep(0.5)
            # drop_menu = driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
            # drop_menu.click()
            # time.sleep(2)
        finally:
            if result is None:
                return 1
            result = result.replace(',', '').replace('(', '').replace(')', '').replace('+', '')
            result = result.split(' ')
            result = result[x].split('\n')
            counts = int(int(result[0])/10)+1
            info_logger.log(f'{counts} pages.')
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
            debug_logger.log((sere, sere.args), 30)
        except selenium.common.exceptions.NoSuchElementException as nsee:
            debug_logger.log((nsee, nsee.args), 30)
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
    info_logger.log('Scrolling...')

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
                info_logger.log('Scrolled to bottom')
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
        
        # last_height = driver.execute_script('return document.getElementsByClassName("dS8AEf")[0].scrollHeight;', scrollable_div)
        for _i in range(counter+1):
        # while True:
            try:
                driver.execute_script(
                    'document.getElementsByClassName("dS8AEf")[0].scrollTop\
                    = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
                    scrollable_div
                )

                # scrolling = driver.execute_script(
                #     'document.getElementsByClassName("dS8AEf")[0].scrollTop\
                #     = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
                #     scrollable_div
                # )
                # WebDriverWait(driver, 5).until(
                #     lambda driver: driver.execute_script('return document.getElementsByClassName("dS8AEf")[0].scrollHeight;', scrollable_div) > last_height
                # )

                # scroll_height = driver.execute_script('return document.getElementsByClassName("dS8AEf")[0].scrollHeight;', scrollable_div)

                time.sleep(1)
            except selenium.common.exceptions.StaleElementReferenceException as sere:
                time.sleep(2)
                debug_logger.log((sere, sere.args), 30)
                continue
            except selenium.common.exceptions.TimeoutException as te:
                debug_logger.log((te, te.args), 30)
                continue
            except:
                raise
        # for _i in range(counter):
        #     try:
        #         scrolling = driver.execute_script(
        #             'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
        #             scrollable_div
        #         )
        #     except:
        #         pass
        #     time.sleep(1)

def write_to_xlsx(data, filename, dir, format):
    '''Write reviews into formatted file

    data: list of reviews
    filename: web title
    dir: parameter from get_review, default: 'SaveData'
    format: 'csv' or 'json'
    '''
    # create directory named by title if not exists
    sub_dir = create_dir(filename)
    # save file into this directory
    filepath = os.path.join(sub_dir, filename) + '.' + format
    info_logger.log(f'Write to {filepath}...')
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
                format: str = 'json',
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
    >>> ex: 'SaveData\虎尾小籠包(虎尾站)-Google地圖\虎尾小籠包(虎尾站)-Google地圖.json'

    Saved review format
    ```json
    {
        "time":"2024/05",
        "rating":"5",
        "comment":"氣氛：5"
    }
    ```
    '''
    if url is None:
        raise Exception('url is None, string is required')
    elif type(url) is not str:
        raise Exception('url must be a string')

    if format not in ['csv', 'json']:
        raise Exception('format must be csv or json')
    
    if  time_range is not None:
        if not all(isinstance(elem, str) for elem in time_range):
            raise Exception(f'Argument format required list of strings')
        elif time_range[1] not in utils.time_filter_zh:
            raise Exception(f'Argument format must be one of {utils.time_filter_zh}')

    try:
        # setup webdriver options
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument("--head")  # show browser or not
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--lang=en-US")
        # options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US',
        #                                           'profile.managed_default_content_settings.images': 2})
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
        webTitle = utils.webname_filter.sub('', driver.title)
        if check_cache:
            cached_path = check_loacal_cache(query=webTitle, query_dir=save_path, file_type=format)
            # cached_path = os.path.join(save_path, webTitle) + f'.{format}'
            info_logger.log(f'Already cached: {cached_path}')

            if cached_path is not None:
                return cached_path

        info_logger.log(f'Scraping {webTitle}...')

        # count for scrolling
        counts = counter(webname)

        # scroll to the bottom of the page
        scrolling(counts, webname)

        # get reviews on the web
        data = get_data(webname, time_range)

        # write reviews to csv file
        file = write_to_xlsx(data, webTitle, save_path, format)
        info_logger.log(f'Your restaurant review file is saved to {file}')
        return file
    # TODO: catch more exceptions
    except:
        # print('Failed to scrape web')
        raise
    finally:
        driver.close()
        driver.quit()
        # os.system("taskkill /f /im chrome.exe")
