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

#엑셀 돌면서 URL타다가
wb = xlrd.open_workbook('upload_target.xlsx')
sh = wb.sheet_by_index(0)

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

for rownum in range(1, sh.nrows):
    row_values = sh.row_values(rownum)
    driver.get(row_values[24])

    #images Directory는 원하는 곳으로 지정 가능
    url = driver.find_element_by_xpath("//img[@style='-webkit-user-select: none;cursor: zoom-in;']").get_attribute("src")
    save_name = 'images/image_'+str(rownum)+'.jpg'
    urllib.request.urlretrieve(url, save_name)