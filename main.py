from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from smsactivate.api import SMSActivateAPI

import random
import time
import requests


class ProgHub():
    def __init__(self, driver, lang):
        self.driver = driver
        self.lang = lang

    def go_to_test_page(self):
        self.driver.get('https://proghub.ru/tests')

    def parse(self):
        self.go_to_test_page()
        slide_elems = self.driver.find_elements_by_class_name("testCard")
        for elem in slide_elems:
            elem.find_element_by_class_name('title')
            if self.lang in elem.text:
                print(elem.text)


class SmsActivate():

    def __init__(self, api_key, debug_mode=True):
        self.api_key = api_key
        self.debug_mode = debug_mode
        self.sa = sa = SMSActivateAPI(api_key)
        sa.debug_mode = debug_mode  # Optional action. Required for debugging

    def show_balance(self):
        balance = self.sa.getBalance()
        try:
            print("Текущий баланс:" + str(balance))
        except:
            print(balance['message'])

    def request_for_number(self):
        number = self.sa.getNumber(service='ot', country=0)
        try:
            #print(number)
            print(number['phone'])
            return str(number['phone'])[1:]
        except:
            print(number['message'])
            raise Exception


class TestClass():
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    #Переходим на страничку aol
    def went_to_page(self):
        self.driver.get(self.url)

    def enter_reg_info(self, name, surname, mail, psw, phone):
        name_blank = self.driver.find_element_by_id('usernamereg-firstName')
        name_blank.send_keys(name)

        surname_blank = self.driver.find_element_by_id('usernamereg-lastName')
        surname_blank.send_keys(surname)

        mail_blank = self.driver.find_element_by_id('usernamereg-yid')
        mail_blank.send_keys(mail)

        psw_blank = self.driver.find_element_by_id('usernamereg-password')
        psw_blank.send_keys(psw)

        phone_blank = self.driver.find_element_by_id('usernamereg-phone')
        phone_blank.send_keys(phone)

        country_code_select = Select(self.driver.find_element_by_name('shortCountryCode'))
        country_code_select.select_by_value('RU')

        march_select = Select(self.driver.find_element_by_name('mm'))
        rand_num = random.randint(1, 12)
        march_select.select_by_value(str(rand_num))

        year_blank = self.driver.find_element_by_id('usernamereg-year')
        rand_year = random.randint(1980, 2002)
        year_blank.send_keys(rand_year)

        day_blank = self.driver.find_element_by_id('usernamereg-day')
        rand_day = random.randint(1, 29)
        day_blank.send_keys(rand_day)

        continue_click = self.driver.find_element_by_id('reg-submit-button')
        continue_click.click()

    def captcha_check(self):
        if 'https://login.aol.com/account/challenge/recaptcha' in self.driver.current_url:
            return True
        else:
            return False

    def show_curent_userAgent(self):
        return self.driver.execute_script("return navigator.userAgent")

    def sendSmsClick(self):
        name_blank = self.driver.find_element_by_name('sendCode')
        name_blank.click()


def main():
    #sms-activate
    api_key = '4e4ffA2b26f6f68e1e417f2695487f3A'

    #proxy_server = "dina.ltespace.com 14283 do2ayq5m zgdxnxuc"
    proxy_server = ""

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.56 Safari/537.36")
    options.add_argument(f'--proxy-server={proxy_server}')
    driver = webdriver.Chrome(options=options)


    aol_url = 'https://login.aol.com/account/create'
    name = 'Максим'
    surname = 'Романов'
    mail = 'maksimelyyan1'
    password = 'parzival2019'
    phone = '9005993665'

    site_ctrl = TestClass(driver, aol_url)
    site_ctrl.went_to_page()
    req_sms = SmsActivate(api_key=api_key)
    req_sms.show_balance()

    phone = req_sms.request_for_number()
    site_ctrl.enter_reg_info(name, surname, mail, password, phone)
    while site_ctrl.captcha_check():
        print(site_ctrl.driver.current_url)
        time.sleep(10)

    #site_ctrl.sendSmsClick()




    time.sleep(255)




if __name__ == '__main__':
    main()