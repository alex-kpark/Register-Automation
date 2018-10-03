#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains

import xlrd
from collections import OrderedDict

from register_ssobing import *

#1 Login 이후 주문 리스트로 이동
id = '#id'
pw = '#pw'

ssobing_login(id, pw)
driver.get("http://www.ssobing.com/selleradmin/order/catalog")

#가능하면 다운로드 받는 폴더 Path 지정 가능하게 세팅하면 좋을 듯

#2 정보 세팅
def download_setting():
    selectall_btn = driver.find_elements_by_xpath("//span[@class='icon-check hand all-check']")

    start = '2018-09-01'
    end = '2018-10-01'

    #시작일을 2017-01-01로 설정, 마감일은 수집하는 날짜로 서버가 자동설정 해줌
    #input에 .send_keys가 아니라 value 값을 바꾸는 javascript를 실행해야 함
    collecting_date = driver.find_elements_by_xpath("//input[@name='regist_date[]']")
    driver.execute_script("arguments[0].setAttribute('value','2017-01-01')", collecting_date[0]) #변경가능

    selectall_btn[0].click() #Before 출고
    selectall_btn[1].click() #After 출고 이후

    start_collect_btn = driver.find_elements_by_xpath("//button[@type='submit']")
    start_collect_btn[0].click()


def download_action():
    pass

    '''
    (전체선택) 다운받을 값 선택
    양식 선택
    다운로드 클릭
    택배 및 4가지 항목 모두 클릭 (Custom 가능하게 디자인)
    다운로드 버튼 클릭
    '''

download_setting()
download_action()
