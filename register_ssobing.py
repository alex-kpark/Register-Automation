#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains

import urllib.request
import requests

import os
from time import sleep

import xlrd
from collections import OrderedDict
import json

# In case of chrome 69
# https://stackoverflow.com/questions/52185371/allow-flash-content-in-chrome-69-running-via-chromedriver/52254172

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

def ssobing_login(id, pw):
    driver.get('http://www.ssobing.com/selleradmin/login/index')

    input_id = driver.find_element_by_xpath("//input[contains(@name, 'main_id')]")
    input_pw = driver.find_element_by_xpath("//input[contains(@name, 'main_pwd')]")

    input_id.send_keys(id)
    input_pw.send_keys(pw)

    login = driver.find_element_by_xpath("//input[contains(@class, 'submit_btn')]")
    login.send_keys(Keys.ENTER)

    driver.get('http://www.ssobing.com/selleradmin/goods/regist')

def brand_classifier(sex):
    category_btn = driver.find_element_by_xpath("//button[contains(@id, 'categoryConnectPopup')]")
    category_btn.click()
    sleep(3)

    if sex == '남':
        #남성 티셔츠
        misc_btn = driver.find_element_by_xpath("//option[contains(@value, 'A001')]")
        misc_btn.click()
        sleep(3)

        secondary = driver.find_element_by_xpath("//option[contains(@value, 'A0010003')]")
        secondary.click()
        sleep(3)

        third = driver.find_element_by_xpath("//option[contains(@value, 'A00100030002')]")
        third.click()
        sleep(3)
        
    else:
        #여성 티셔츠
        misc_btn = driver.find_element_by_xpath("//option[contains(@value, 'A001')]")
        misc_btn.click()
        sleep(3)

        secondary = driver.find_element_by_xpath("//option[contains(@value, 'A0010001')]")
        secondary.click()
        sleep(3)

        third = driver.find_element_by_xpath("//option[contains(@value, 'A00100010003')]")
        third.click()
        sleep(3)

    #정확하게 tag달아서 지정해주어야 함, 여러 Element가 검색되었어서 오류 발생
    category_fin = driver.find_element_by_xpath("//button[@id='categoryConnect'][@onclick='this.form.submit();']")
    category_fin.send_keys(Keys.ENTER)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()  

def product_info(name, sum_content, brand_code, keywords, outside_words, tax_bool,
                cancel_bool, adult_bool, hscode_cont):

    name_place = driver.find_element_by_xpath("//input[contains(@name, 'goodsName')]")
    name_place.send_keys(name)

    summary = driver.find_element_by_xpath("//input[contains(@name, 'summary')]")
    summary.send_keys(sum_content)

    brand_idx = driver.find_element_by_xpath("//input[contains(@name, 'purchaseGoodsName')]")
    brand_idx.send_keys(brand_code)

    search_words = driver.find_element_by_xpath("//input[contains(@onkeyup, 'calculate_input_byte(this);')]")
    search_words.send_keys(keywords)

    openmarket_words = driver.find_element_by_xpath("//input[contains(@name, 'openmarket_keyword')]")
    openmarket_words.send_keys(outside_words)

    #taxation
    #과세면 True, 비과세면 False
    tax = driver.find_element_by_xpath("//input[contains(@value, 'tax')]")
    nontax = driver.find_element_by_xpath("//input[contains(@value, 'exempt')]")
    check_alert = driver.find_element_by_xpath("//input[contains(@name, 'tax_chk')]")
    if tax_bool == True:
        pass
    else:
        nontax.click()
    check_alert.click()

    #Cancel Contract
    #청약철회불가 가능하면 True, 아니면 False
    check_cancel = driver.find_element_by_xpath("//input[contains(@name, 'cancel_type')]")
    if cancel_bool == True:
        check_cancel.click()
    else:
        pass
    
    #Adult Product
    #19세 이상만 구입 가능하면 True, 아니면 False
    check_adult = driver.find_element_by_xpath("//input[contains(@name, 'adult_goods')]")
    if adult_bool == True:
        check_adult.click()
    else:
        pass

    #HSCODE
    hscodeplace = driver.find_element_by_xpath("//input[contains(@name, 'hscode')]")
    hscodeplace.send_keys(hscode_cont)

def selling_info(min_num, max_num, multiple):
    
    #Minimum amount
    unlimit_min = driver.find_element_by_xpath("//input[@name='minPurchaseLimit'][@value='unlimit']")
    limit_min = driver.find_element_by_xpath("//input[@name='minPurchaseLimit'][@value='limit']")

    if min_num >= 1:
        limit_min.click()
        min_content = driver.find_element_by_xpath("//input[@name='minPurchaseEa']")        
        min_content.send_keys(min_num)
    else:
        pass

    #Maximum amount : unlimited == 0, limited == number input
    unlimit_max = driver.find_element_by_xpath("//input[@name='maxPurchaseLimit'][@value='unlimit']")
    limit_max = driver.find_element_by_xpath("//input[@name='maxPurchaseLimit'][@value='limit']")

    if max_num == 0:
        pass
    else:
        limit_max.click()
        max_content = driver.find_element_by_xpath("//input[@name='maxPurchaseEa']")
        max_content.send_keys(max_num)

    #Multiple Purchase multiple = [Bool, cond_num, obj_num, 'p' or 'w(won)']
    multiple_check = driver.find_element_by_xpath("//input[@name='multiDiscountUse']")
    if multiple[0] == True:
        multiple_check.click()
        
        cond_num = driver.find_element_by_xpath("//input[@name='multiDiscountEa']")
        obj_num = driver.find_element_by_xpath("//input[@name='multiDiscount']")
        cond_num.send_keys(multiple[1])
        obj_num.send_keys(multiple[2])
        
        if multiple[3] == 'p':
            multiple_unit = driver.find_element_by_xpath("//select[@name='multiDiscountUnit']")
            multiple_unit.send_keys(Keys.DOWN)
        else:
            pass
    else:
        pass

    #Skip for 재고변화에 따른 상품 판매 여부    

def essential_option():
    pass

def color_size(ops_name, size_val, c_price, r_price, inventory):
    size_allow = driver.find_element_by_xpath("//input[@name='optionUse'][@value='1']")
    size_allow.click()

    create_size = driver.find_element_by_xpath("//button[@id='optionMake']")
    create_size.send_keys(Keys.ENTER)

    windows = driver.window_handles
    driver.switch_to_window(windows[1])
    sleep(2)

    create_ops = driver.find_element_by_xpath("//button[@id='optionMake']")
    sleep(2)
    create_ops.click()

    ops_var = driver.find_element_by_xpath("//input[@name='optionMakeName[]'][@class='line']")
    ops_var.send_keys(ops_name)

    ops_val = driver.find_element_by_xpath("//input[@name='optionMakeValue[]']")
    ops_val.send_keys(size_val)

    sleep(1)
    ops_select = driver.find_element_by_xpath("//button[@id='gdoptioncodemakebtn']")
    sleep(2)
    ops_select.click()
    
    alert = driver.switch_to_alert()
    alert.accept()

    cons_prices = driver.find_elements_by_xpath("//input[@name='consumer_price']")
    for cons in cons_prices:
        cons.send_keys(c_price)    

    real_prices = driver.find_elements_by_xpath("//input[@name='price']")
    for reals in real_prices:
        reals.send_keys(r_price)

    #먼저 Indexing을 만들고, 그 Index를 따라가면서 실행
    inventories = driver.find_elements_by_xpath("//input[@name='stock']")
    index_list = list(range(0,len(inventory)))
    for i in index_list:
        inventories[i].send_keys(inventory[i])

    essential_ops = driver.find_element_by_xpath("//input[@name='frequently'][@value='1']")
    essential_ops.click()

    sleep(1)
    save_sizes = driver.find_element_by_xpath("//button[@id='setTmpSeq']")
    save_sizes.click()

    driver.switch_to_window(windows[0])
    sleep(2)

# Needs to be fixed
def image_upload():
    
    '''
    urllib.request.urlretrieve('https://s3-ap-northeast-2.amazonaws.com/gmp01/1196/prod/S258FCDADF9C/upload_a6ddc0523f3032b771497dba704b9fe7.jpg', path_to_image)
    driver.find_element_by_xpath("//object[@id='uploaderUploader']").send_keys(path_to_image)
    
    base_dir = 'C:/Users/ALEXa/Desktop/AutomateRegister/sample_image/'
    path_to_image = os.path.join(base_dir, 'upload_img.jpg')
    '''
    image_btn = driver.find_element_by_xpath("//button[@class='batchImageMultiRegist']")
    image_btn.click()    
    test = driver.window_handles
    driver.switch_to_window(test[1])

    driver.find_element_by_xpath("//object[@id='uploaderUploader']").click()

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get('http://www.ssobing.com/selleradmin/goods_process/upload_file_multi')
    
    response = requests.post(url='http://www.ssobing.com/selleradmin/goods_process/upload_file_multi/', data={'Filedata':'C:\\store\\1.jpg'})
    print(response)
    print(response.status_code)

    print('success')

    '''
    1) http://www.ssobing.com/selleradmin/goods_process/upload_file_multi
    2) POST 요청으로 파일을 실어 보냄
    3) 세션이 살아있을 때 하므로, 열렸을 때 크롬에서 바로 보내줌 

    http://php.net/manual/kr/features.file-upload.post-method.php
    
    그래도 안되면 AutoIT 이용해서 등록
    '''

def detailed_exp(detailed_cont):
    
    register_dexp = driver.find_element_by_xpath("//span[@id='goodscontentsbtn']")
    register_dexp.click()
    sleep(3)

    check_html = driver.find_element_by_xpath("//div[@id='tx_switchertoggle1']")
    check_html.click()
    sleep(3)

    cont_area = driver.find_element_by_xpath("//textarea[@id='tx_canvas_source1']")
    cont_area.send_keys(detailed_cont)

    cont_save = driver.find_element_by_xpath("//button[@onclick='view_editor_save()']")
    cont_save.click()

    alert = driver.switch_to_alert()
    alert.accept()


def delivery(delivery_info):
    
    '''
    delivery info : [True/False for 기본배송비정책/개별배송비정책,
    n1, : 고정배송비
    n2, n3, n4, n5, :포장단위별
    n6, n7 : 조건부무료
    ]
    '''
    if delivery_info[0] == True:
        pass
    else:
        indi_delivery = driver.find_element_by_xpath("//input[@name='shippingPolicy'][@value='goods']")
        indi_delivery.click()

        #고정배송(갯수와 상관없이)
        #포장 최대단위는 상품n1개, 배송비n2원 / 포장단위별 추가배송비 n3원
        #합이 n1원 이상이면 무료, 미만이면 선불 n2원
        #배송정책 관련된 숫자만 두고, 나머지는 0처리

        #원래 None이 아니라 0이었음
        if delivery_info[1] != None:
            fixed_fee = driver.find_element_by_xpath("//input[@name='unlimitShippingPrice']")
            fixed_fee.send_keys(delivery_info[1])

        elif delivery_info[2] != 0 and delivery_info[3] != 0 and delivery_info[4] != 0:
            
            ship_btn = driver.find_element_by_xpath("//input[@name='goodsShippingPolicy'][@value='limit']")
            ship_btn.click()

            ship_unit = driver.find_element_by_xpath("//input[@name='limitShippingEa']")
            ship_fee = driver.find_element_by_xpath("//input[@name='limitShippingPrice']")
            extra_fee = driver.find_element_by_xpath("//input[@name='limitShippingSubPrice']")

            ship_unit.send_keys(delivery_info[3])
            ship_fee.send_keys(delivery_info[4])
            extra_fee.send_keys(delivery_info[5])

        else:

            cond_btn = driver.find_element_by_xpath("//input[@name='goodsShippingPolicy'][@value='limit']")
            cond_btn.click()

            cond_unit = driver.find_element_by_xpath("//input[@name='ifpayFreePrice']")
            cond_price = driver.find_element_by_xpath("//input[@name='ifpayDeliveryCost']")

            cond_unit.send_keys(delivery_info[6])
            cond_price.send_keys(delivery_info[7])

def price(legit_price, disc_price):
    legitimate_price = driver.find_element_by_xpath("//input[@name='consumerPrice[]']")
    legitimate_price.send_keys(legit_price)

    discounted_price = driver.find_element_by_xpath("//input[@name='price[]']")
    discounted_price.send_keys(disc_price)

def final_upload():
    #save_info = driver.find_element_by_xpath("//span[@class='btn large black']/button[@onclick='goods_save('view')']")
    save_info = driver.find_element_by_xpath("//ul[@class='page-buttons-right']")
    save_info.click()

    save_submit = driver.find_element_by_xpath("//button[@id='openDialogLayerConfirmYesBtn']")
    save_submit.click()

    okay_submit = driver.find_element_by_xpath("//input[@value='확인']")
    okay_submit.click()
