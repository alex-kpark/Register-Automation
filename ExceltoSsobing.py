#-*- coding: utf-8 -*-
import xlrd
from collections import OrderedDict
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains

import urllib.request
import requests
import os
import sys
from time import sleep

from register_ssobing import *

#Step1 : 상품등록 페이지까지 이동

id = '#id'
pw = '#pw'

ssobing_login(id, pw)

#Step2 : 엑셀에서 하나씩 돌면서 Register 진행
wb = xlrd.open_workbook('sample_data.xlsx')
sh = wb.sheet_by_index(0)

for rownum in range(1, sh.nrows):
    row_values = sh.row_values(rownum)

    #PlayAuto에 있는 변수 대입
    brand_code = row_values[0]
    name = row_values[1]

    if row_values[4] == '과세':
        tax_bool = True
    else:
        tax_bool = False

    #float형은 iteration 안되므로 int로 변환해주어야 함
    c_price = int(round(row_values[16]))
    detailed_cont = row_values[25]

    #PlayAuto에 없는 변수 정의
    keywords = '값이 없습니다'
    ourside_words = '값이 없습니다'
    cancel_bool = True
    adult_bool = False
    hscode_cont = 'AAA000111'
    ops_name = '사이즈'
    size_val = 'S, M, L, XL'
    r_price = 18810
    min_num = 0
    max_num = 0
    multiple = [False]
    delivery_info = [False, 0]
    sum_content = '값이 없습니다'
    outside_words = '값이 없습니다'
    
    #등록 실행
    brand_classifier()
    product_info(name, sum_content, brand_code, keywords, outside_words, tax_bool, cancel_bool, adult_bool, hscode_cont)
    selling_info(min_num, max_num, multiple)
    size_option(ops_name, size_val, c_price, r_price)
    detailed_exp(detailed_cont)
    delivery(delivery_info)
    final_upload()
    driver.get('http://www.ssobing.com/selleradmin/goods/regist')


