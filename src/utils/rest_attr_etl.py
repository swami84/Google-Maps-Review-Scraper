
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class rest_attr():
    def __init__(self):
        self.driver = self.__get_driver()

    def __get_driver(self, debug=False):
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

    def get_rest_info(self, cbg,place_id, rest_name, rest_add):


        url = 'https://www.google.com/search?q=' + rest_name + ' ' + rest_add


        self.driver.get(url)
        time.sleep(1)
        rest_dict = {}
        rest_dict['cbg'] = cbg
        rest_dict['place_id'] = place_id
        response = BeautifulSoup(driver.page_source, 'html.parser')
        for res in response.find_all('a', href=True):
            if 'maps.google' in res['href']:
                map_url = res['href']
        self.driver.get(map_url)
        for res in self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.rating.category\']'):
            rest_dict['rest_type'] = res[0].text
        for res in self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.rating.moreReviews\']'):
            rest_dict['no_of_reviews'] = int(res.text.split(' reviews')[0].replace(',', ''))
        resp = BeautifulSoup(self.driver.page_source, 'html.parser')
        for res in resp.find_all('span', jsinstance="*1"):
            rest_dict['price_range_$'] = len(res.text.split('·')[1])
        for res in self.driver.find_elements_by_xpath('//button[starts-with (@jsaction,\'pane.attributes.expand\')]'):
            rest_summary_text = res.text.split('\n')
            rest_dict['rest_summary'] = rest_summary_text[0]
            rest_dict['rest_labels'] = [lab for lab in rest_summary_text[1:] if lab != '·']
        for res in resp.find_all('div', class_="O9Q0Ff-NmME3c-Utye1-Fq92xe O9Q0Ff-NmME3c-Utye1-Fq92xe-visible"):
            rest_pop_time = (res.find_all('div', class_ = 'O9Q0Ff-NmME3c-Utye1-ZMv3u O9Q0Ff-NmME3c-Utye1-ZMv3u-SfQLQb-V67aGc'))
            for r in rest_pop_time:
                if 'at' in r['aria-label']:
                    time_int = r['aria-label'].split('at ')[1].replace('.','')
                    rest_dict[time_int] = r['aria-label'].split('%')[0]

        return rest_dict