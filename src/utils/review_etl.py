
import json

import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

class ReviewScraper():
    def __init__(self):
        self.driver = self.__get_driver()

    def __get_driver(self,debug=False):
        options = Options()

        if not debug:
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
        else:
            options.add_argument("--window-size=1366,768")
            options.add_argument('--no-sandbox')

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-US")
        driv_path = '../config/webdrivers/chromedriver.exe'
        input_driver = webdriver.Chrome(options=options, executable_path=driv_path)

        return input_driver
    def __sort_review(self):
        wait = WebDriverWait(self.driver, 10)

        menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-value=\'Sort\']')))
        menu_bt.click()
        time.sleep(1)
        recent_rating_bt = self.driver.find_elements_by_xpath('//li[@role=\'menuitemradio\']')[1]
        recent_rating_bt.click()
        time.sleep(1)
        print('Reviews Sorted')

    def __goto_review(self):
        links = self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.rating.moreReviews\']')
            # print(links)
        for l in links:
            # print("Element is visible? " + str(l.is_displayed()))
            l.click()
            time.sleep(2)

    def __scroll(self):
        # reviews_divs = self.driver.find_elements_by_class_name('section-scrollbox')
        # reviews_divs[-1].click()
        scrollable_div = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')
        prev_scroll_height = None
        while True:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                                  scrollable_div)
            last_height = (self.driver.execute_script("return arguments[0].scrollTop", scrollable_div))

            scroll_height = (self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div))

            if scroll_height == prev_scroll_height:
                # print('End of Scrolling')
                break
            prev_scroll_height = scroll_height
            time.sleep(1)

    def __expand_reviews(self):
        links = self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.review.expandReview\']')
        for l in links:
            l.click()
            time.sleep(0.5)
            # print('Review Expanded')

    def url_setup(self,url):
        self.driver.get(url)
        time.sleep(2)
        self.__goto_review()
        self.__sort_review()

    def get_reviews_block(self, offset,cbg):

        # scroll to load reviews

        self.__scroll()

        self.__expand_reviews()

        resp = BeautifulSoup(self.driver.page_source, 'html.parser')

        rblock = resp.find_all('div', class_='ODSEW-ShBeI NIyLF-haAclf gm2-body-2')
        parsed_reviews = []
        for index, review in enumerate(rblock):
            if index >= offset:
                parsed_reviews.append(self.parse_review(review,cbg))
                # print(self.parse_review(review,cbg))

        return parsed_reviews

    # def parse_fname(self, fpath):


    def get_reviews(self, N, url,cbg,place_id):
        self.url_setup(url)

        n = 0
        all_revs = []

        while (n < N):

            reviews = self.get_reviews_block( n,cbg)

            for r in reviews:
                all_revs.append(r)
            dpath = '../data/outputs/reviews/'
            os.makedirs(dpath, exist_ok=True)
            fpath = dpath + str(cbg)+ '_' + place_id + '.json'
            with open(fpath, 'w') as outfile:
                json.dump(all_revs, outfile, indent=4)
            n += len(reviews)
        return all_revs

    def filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace("\\","")
        return strOut

    def parse_review(self,result,cbg):

        rev_item = {}
        rev_item['user_name'] = (result['aria-label'])
        rev_item['review_id'] = result['data-review-id']
        user_link = result.find('div', class_='ODSEW-ShBeI-content').find('a', class_="ODSEW-ShBeI-t1uDwd-hSRGPd")[
            'href']
        rev_item['user_id'] = [int(s) for s in user_link.split('/') if s.isdigit()][0]
        rev_item['rating'] = (result.find('span', class_='ODSEW-ShBeI-H1e3jb')["aria-label"].split(' stars')[0])

        dt = (result.find('span', class_='ODSEW-ShBeI-RgZmSc-date').text)
        dt = dt.replace('a ', '1 ')
        dt = dt.replace('an ', '1 ')
        value, unit = re.search(r'(\d+) (\w+) ago', dt).groups()

        if not unit.endswith('s'): unit += 's'
        delta = relativedelta(**{unit: int(value)})
        rev_item['review_date'] = datetime.now() - delta

        rev_item['review'] = result.find('span', class_='ODSEW-ShBeI-text').text

        user_info = result.find('div', class_='ODSEW-ShBeI-VdSJob')
        if user_info:

            if 'style' in user_info.find('span').attrs:
                rev_item['local_guide'] = 'No'

            else:
                rev_item['local_guide'] = 'Yes'
            n_reviews = user_info.find_all('span')[1].text
            rev_item['user_reviews'] = int(re.findall(r'(\d+)', n_reviews)[0])

        user_pics = result.find('div', class_='ODSEW-ShBeI-Jz7rA')
        n_pics = 0
        if user_pics:
            n_pics = len(user_pics.find_all('button'))
        rev_item['user_pictures'] = n_pics
        rev_item['cbg'] = cbg

        return rev_item

    def get_place_data(self,url):

        self.driver.get(url)

        # ajax call also for this section
        time.sleep(2)
        place = {}
        resp = BeautifulSoup(self.driver.page_source, 'html.parser')
        try:
            place['overall_rating'] = float(resp.find('div', class_='gm2-display-2').text.replace(',', '.'))
        except:
            place['overall_rating'] = 'NOT FOUND'

        try:
            place['n_reviews'] = int(self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.reviewChart.moreReviews\']')[0].text.split(' ')[0])
        except:
            place['n_reviews'] = 0

        return place