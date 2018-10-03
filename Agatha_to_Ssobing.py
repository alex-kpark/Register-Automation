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

'''
#구현내용
- Excel의 행(row)을 돌면서 안에 있는 정보들을 하나하나 넣어줌
- 제품마다 색상 x 사이즈 개수만큼 옵션을 생성하고, 그 옵션의 재고를 파악해 재고 수량까지 반영
- 한국에서 사입한 제품이므로 HSCODE는 ''(빈 값)을 넣어주었음

#주의사항
- Ssobing은 DB에서 상품명이 똑같으면 업로드 되지 않음 (SET에 대해서는 이름을 다르게 설정해주어야 함)
- 정보를 올릴 Excel File에 변화가 생기면, 새로 파일을 만들어서 저장해주어야 함
'''

#Step1 : 상품등록 페이지까지 이동

id = '#id'
pw = '#pw'

ssobing_login(id, pw)

#Step2 : 엑셀에서 하나씩 돌면서 Register 진행
wb = xlrd.open_workbook('upload_target.xlsx')
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
    r_price = int(round(row_values[5]))
    detailed_cont = row_values[25]

    #PlayAuto에 없는 변수 정의
    keywords = '아가타'
    cancel_bool = False
    adult_bool = False
    hscode_cont = ''
    min_num = 0
    max_num = 0
    multiple = [False]
    delivery_info = [False, 0]
    sum_content = '아가타'
    outside_words = '아가타'

    ops_name = '사이즈 및 색상'
    sex = row_values[48]

    #size_Val 정의 (옵션의 종류 선언)
    size_list = ['S', 'M', 'L', 'XL']
    result = []
    for color in row_values[28:32]:
        if color == 'Null':
            tar = result[-1]
            changed_tar = tar.replace(',', ' ')
            result[-1] = changed_tar
        else: 
            result.append(color + ' ' + size_list[0] + ', ')
            result.append(color + ' ' + size_list[1] + ', ')
            result.append(color + ' ' + size_list[2] + ', ')
            result.append(color + ' ' + size_list[3] + ', ')
    size_val =  "".join(result)

    #inventory(재고) 정의
    inven_list = []
    for tb_val in row_values[32:47]:
        if tb_val == '':
            pass
        else:
            tb_integ = int(round(tb_val))
            inven_list.append(tb_integ)

    inventory = inven_list

    #등록 실행
    brand_classifier(sex)
    sleep(1)
    product_info(name, sum_content, brand_code, keywords, outside_words, tax_bool, cancel_bool, adult_bool, hscode_cont)
    sleep(1)
    selling_info(min_num, max_num, multiple)    
    sleep(1)
    color_size(ops_name, size_val, c_price, r_price, inventory)
    sleep(1)
    detailed_exp(detailed_cont)
    sleep(1)
    delivery(delivery_info)
    sleep(1)
    final_upload()
    print(rownum)
    
    #곧바로 Register로 가버리면 페이지 중간으로 Load되어서 Brand Classifier가 WebElement를 못잡음. 그래서 메인페이지 한번 이동했다가 다시 Register로 이동
    driver.get('http://www.ssobing.com/selleradmin/main/index')
    driver.get('http://www.ssobing.com/selleradmin/goods/regist')
    sleep(1)
    ActionChains(driver).send_keys(Keys.UP)
    ActionChains(driver).send_keys(Keys.UP)


