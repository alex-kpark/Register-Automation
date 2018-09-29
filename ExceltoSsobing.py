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
wb = xlrd.open_workbook('final_agatha.xlsx')
sh = wb.sheet_by_index(0)

#sh.nrows
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
    r_price = int(round(row_values[5]))
    detailed_cont = row_values[25]


    #PlayAuto에 없는 변수 정의
    keywords = '아가타'
    cancel_bool = True
    adult_bool = False
    hscode_cont = ''
    min_num = 0
    max_num = 0
    multiple = [False]
    delivery_info = [False, 0]
    sum_content = '아가타'
    outside_words = '아가타'

    ops_name = '사이즈 및 색상'

    #size_Val 정의 (옵션의 종류 선언)
    size_list = ['S', 'M', 'L', 'XL']
    result = []
    for test in row_values[28:32]:
        if test == 'Null':
            tar = result[-1]
            print(tar)
            changed_tar = tar.replace(',', ' ')
            result[-1] = changed_tar
        else: 
            result.append(test + ' ' + size_list[0] + ', ')
            result.append(test + ' ' + size_list[1] + ', ')
            result.append(test + ' ' + size_list[2] + ', ')
            result.append(test + ' ' + size_list[3] + ', ')
    size_val =  "".join(result)

    #inventory(재고) 정의
    
    '''
    #등록 실행
    brand_classifier()
    product_info(name, sum_content, brand_code, keywords, outside_words, tax_bool, cancel_bool, adult_bool, hscode_cont)
    selling_info(min_num, max_num, multiple)
    '''
    color_size(ops_name, size_val, c_price, r_price, inventory)
    '''
    detailed_exp(detailed_cont)
    delivery(delivery_info)
    final_upload()
    driver.get('http://www.ssobing.com/selleradmin/goods/regist')
    '''