#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import xlrd
from collections import OrderedDict

# 변수정의

smart_id = '#'
smart_pw = '#'

#login

chrome_options = webdriver.ChromeOptions()

prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "http://www.ssobing.com"
}

chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--disable-features=EnableEphemeralFlashPermission")

#For OSX
#chrome_path = '/usr/local/bin/chromedriver'
chrome_path = 'C:/Users/ALEXa/AppData/Local/Programs/Python/chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

#네이버는 바로 로그인하면 CAPCHA를 요청하므로 여러번 PATH를 거쳐서 들어가야 함
def download_smartstore(id, pw):
    driver.get("https://sell.smartstore.naver.com/#/home/about")

    time.sleep(2)

    smart_login = driver.find_element_by_xpath("//a[@class='btn btn-primary']")
    smart_login.click()

    time.sleep(1)
    driver.get("https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523")
    time.sleep(1)

    input_id = driver.find_element_by_xpath("//input[@id='id']")
    input_pw = driver.find_element_by_xpath("//input[@id='pw']")
    input_id.send_keys(id)
    input_pw.send_keys(pw)

    time.sleep(2)
    login_btn = driver.find_element_by_xpath("//input[@class='btn_global']")
    login_btn.click()

    time.sleep(1)
    driver.get("https://sell.smartstore.naver.com/#/naverpay/manage/order")
    driver.maximize_window()

    #날짜선택 미구현

    driver.switch_to_frame("__naverpay")
    download_excel = driver.find_element_by_xpath("//button[@type='button'][@class='npay_btn_common size_medium type_basic btn_excel _click(nmp.seller_admin.order.manage.simple.excelDownload()) _stopDefault']")
    download_excel.click()
    
download_smartstore(smart_id, smart_pw)