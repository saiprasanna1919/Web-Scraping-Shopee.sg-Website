from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
from time import sleep
import pandas as pd


delivery_list = []


def parse(url):
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default')

    chrome_options.add_argument("disable-infobars")
    chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })

    browser = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    browser.get(url)
    delay = 5 
    try:
        a = ActionChains(browser)
        try:
            element_to_select = browser.find_element("xpath",'//*[local-name()="svg" and @class="shopee-svg-icon icon-arrow-down"]')
            a.move_to_element(element_to_select).click().perform()
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        
            soup = BeautifulSoup(html, "html.parser")
            tree = etree.HTML(str(soup))
            txt = tree.xpath('//div[@class="shopee-drawer__contents"]//div[@class="AAaUS1"]')
            result = []
            for i in txt:
                result.append(i.text)
            status = ','.join(result)
            delivery_list.append(status)

        except:
            delivery_list.append("No item")
    except TimeoutException:
        print ("Loading took too much time!-Try again")

    browser.close()

def main():
    df = pd.read_excel('E-commerce URL.xlsx')
    for i in df['URLS']:
        parse(i)

    df['code'] = pd.Series(delivery_list)
    df.to_excel('final.xlsx')

main()

