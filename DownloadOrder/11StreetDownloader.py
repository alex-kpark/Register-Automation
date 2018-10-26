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

ebay_id = '#'
ebay_pw = '#'

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

def login_street(id, pw):
    
    driver.get("https://login.11st.co.kr/login/Login.tmall?returnURL=http%3A%2F%2Fwww.11st.co.kr%2Fhtml%2Fmain.html&xfrom=")
    time.sleep(2)

    input_id = driver.find_element_by_xpath("//input[@id='loginName']")
    input_pw = driver.find_element_by_xpath("//input[@id='passWord']")

    input_id.send_keys(id)
    input_pw.send_keys(pw)

    login_btn = driver.find_element_by_xpath("//input[@class='btn_login']")
    login_btn.click()

    time.sleep(2)
    driver.get("http://soffice.11st.co.kr/Index.tmall")

#판매완료 데이터 대상
def move_street():

    driver.get("https://soffice.11st.co.kr/escrow/SaleEndList.tmall")

    #날짜 선택 기능 미구현

    search_btn = driver.find_element_by_xpath("//button[@class='defbtn_lar ladtype defbtn_seh']")
    search_btn.click()
    time.sleep(2)

    excel_btn = driver.find_element_by_xpath("//a[@class='defbtn_lsm dtype6 btn_exceld']")
    excel_btn.click()




login_street(ebay_id, ebay_pw)
move_street()