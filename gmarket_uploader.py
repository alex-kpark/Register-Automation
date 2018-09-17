#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from time import sleep

#For OSX
driver = webdriver.Chrome('/usr/local/bin/chromedriver')

#For Windows
#driver = webdriver.Chrome('C:/Users/PC/AppData/Local/Programs/Python/chromedriver.exe')
driver.get('https://www.esmplus.com/Member/SignIn/LogOn?ReturnValue=-7')

#login
def login(id, pw):

    input_id = driver.find_element_by_xpath("//input[@id='Id']")
    input_pw = driver.find_element_by_xpath("//input[@id='Password']")
    input_id.send_keys(id)
    input_pw.send_keys(pw)
    push_login = driver.find_element_by_xpath("//img[@src='https://pics.esmplus.com/front/btn/btn_login.gif']")
    push_login.click()

    activate_info = driver.find_element_by_xpath("//img[@src='http://pics.esmplus.com/front/common/lnb_depth_2_1.gif']")
    activate_info.click()
    push_activate = driver.find_element_by_xpath("//li[@id='TDM395']")
    push_activate.click()

    #iframe: element를 못잡으면 그 안에 iframe이 형성되어있을 가능성이 높다 or sleep을 주거나
    driver.get('http://www.esmplus.com/Home/Home#HTDM395')
    driver.switch_to_frame("ifm_TDM395")
    
    #sleep을 쓰지 않고 하는 방법은 없을까? #######

def select_market():
    cancel_ac = driver.find_element_by_xpath("//input[@name='regi-nameiac'][@value='false']")
    cancel_gmk = driver.find_element_by_xpath("//input[@name='regi-namegmk'][@value='false']")

    if auc == False and gmk == False:
        cancel_ac.click()
        cancel_ac.click()
    elif auc == False:
        cancel_ac.click()
    elif gmk == False:
        cancel_gmk.click()
    else:
        pass

#category : 브랜드 카테고리 항목을 잘 못잡음
def category(cate_name):
    #검색으로 구현

    search_esm = driver.find_element_by_xpath("//input[@placeholder='ESM 카테고리명 검색']")
    search_esm.send_keys(cate_name)
    esm_click = driver.find_element_by_xpath("//img[@src='http://pics.esmplus.com/front/sell/icon_search.gif']")
    esm_click.click()
    sleep(1)
    esm_result = driver.find_elements_by_xpath("//em[@class='keyword']")
    esm_target = esm_result[4]
    esm_target.click()
    sleep(1)
    print('here is done')

def product_info(name, promo, auc_price, gmk_price):
    prod_name = driver.find_element_by_xpath("//input[@id='txtGoodsNameSearch']")
    prod_name.send_keys(name)
    promo_name = driver.find_element_by_xpath("//input[@id='txtGoodsNamePrmt']")
    promo_name.send_keys(promo)

    if auc == True and gmk == True:
        if auc_price == gmk_price:
            price_slot = driver.find_element_by_xpath("//input[@id='txtGoodsPrice']")
            price_slot.send_keys(ac_price)
    
        else:
            diff_price = driver.find_element_by_xpath("//a[@id='btnGoodsPriceSeparateInsert']")
            diff_price.click()
            auc_slot = driver.find_element_by_xpath("//input[@id='txtGoodsPriceIAC']")
            gmk_slot = driver.find_element_by_xpath("//input[@id='txtGoodsPriceGMKT']")
            auc_slot.send_keys(auc_price)
            gmk_slot.send_keys(gmk_price)

    else:
        price_slot = driver.find_element_by_xpath("//input[@id='txtGoodsPrice']")
        if auc == True and gmk == False:
            price_slot.send_keys(auc_price)
        elif auc == False and gmk == True:
            price_slot.send_keys(gmk_price)
        else:
            pass

def gmk_prod_info(eng, chn, jpn):
    if gmk == False:
        pass
    else:
        eng_name = driver.find_element_by_xpath("//input[@id='txtGoodsNameEng2']")
        chn_name = driver.find_element_by_xpath("//input[@id='txtGoodsNameChn2']")
        jpn_name = driver.find_element_by_xpath("//input[@id='txtGoodsNameJpn2']")

        eng_name.send_keys(eng)
        chn_name.send_keys(chn)
        jpn_name.send_keys(jpn)

def duration(num):

    duration_bar = driver.find_element_by_xpath("//select[@id='sltFixedPriceSellingPeriod']")
    duration_bar.click()

    if num == 90:
        pass

    elif num == 60:
        duration_bar.send_keys(Keys.UP)
    
    elif num == 30:
        duration_bar.send_keys(Keys.UP)
        duration_bar.send_keys(Keys.UP)  
        '''
        elif num == 15:
            print(15)
            i = 1
            while i == 2:
                duration_bar.send_keys(Keys.UP)
                i = i + 1
            print('15success')
        '''
    elif num == 15:
        duration_bar.send_keys(Keys.UP)
        duration_bar.send_keys(Keys.UP)
        duration_bar.send_keys(Keys.UP)    
    
    else:
        pass
    duration_bar.send_keys(Keys.ENTER)

def extra_info(disc_info):
    #discount
    if disc_info[0] == 'n':
        print('none')
        pass
        
    else:
        disc_btn = driver.find_element_by_xpath("//input[@id='chkSellerDiscountIsUsed']")
        disc_btn.click()

        if disc_info[0] == 'm':
            money_amount = driver.find_element_by_xpath("//input[@name='SYIStep3.SellerDiscount.DiscountAmt']")
            money_amount.send_keys(disc_info[1])

        else:
            perc_btn = driver.find_element_by_xpath("//input[@id='SYIStep3_SellerDiscount_DiscountType'][@value='2']")
            perc_btn.click()
            perc_amount = driver.find_element_by_xpath("//input[@name='SYIStep3.SellerDiscount.DiscountAmt']")
            perc_amount.send_keys(disc_info[1])

        if disc_info[2] == 'u': 
            pass

        else:
            dur_btn = driver.find_element_by_xpath("//input[@id='chkSellerDiscountPeriodUsed']")
            dur_btn.click()
            dur_start = driver.find_element_by_xpath("//input[@name='SYIStep3.SellerDiscount.StartDate']")
            dur_end = driver.find_element_by_xpath("//input[@name='SYIStep3.SellerDiscount.EndDate']")
            dur_start.send_keys(disc_info[3])
            dur_end.send_keys(disc_info[4])
        
def exposure_info(deliver_date, deliver_method, ):
    
    move_btn = driver.find_element_by_xpath("//li[@class='menu_item2']")
    move_btn.click()

    #image 연결? : 이미지 연결이 안됨
    '''
    브라우저에서 팝업창으로 넘어가야 하는데, 팝업창을 못잡고 있음
    #product_details
    ebay_writer = driver.find_element_by_xpath("//a[@id='btnNewDesc']")
    ebay_writer.click()

    popup_exit = driver.find_element_by_xpath("//button[@class='slider-roll-button slider-roll-next']")    
    press_exit.click()
    '''

    #상품정보공시 입력 - 카테고리에 따라 value 입력
    product_type = driver.find_element_by_xpath("//select[@name='ddlOfficialNotiGroup']/option[@value='3']")
    product_type.click()

    #발송정책 - 옥션만
    if deliver_date == True:
        #당일배송
        pass
    elif deliver_date == False:
        deliver_auc = driver.find_element_by_xpath("//select[@id='transTypeChoiceIac']/option[@value='357617']")
        deliver_auc.click()
    else:
        pass

    #발송방법
    if deliver_method == 0:
        post_deliv = driver.find_element_by_xpath("//input[@id='rdoCommonDeliveryWayOPTSEL1']")
        try:
            post_deliv.click()
        except Exception as e:
            pass
    elif deliver_method == 1:
        truck_deliv = driver.find_element_by_xpath("//input[@id='rdoCommonDeliveryWayOPTSEL2']")
        truck_deliv.click()
    else:
        direct_deliv = driver.find_element_by_xpath("//input[@id='rdoCommonDeliveryWayOPTSEL3']")


login('#id', '#pw')

auc = True
gmk = True

category(str(unicode('여성가방')))

'''
select_market()

            
gmk_prod_info('English Please',
            '你好',
            'エンジニア')

duration(60)

product_info('제품 이름을 입력해주십시오',
            '프로모션 이름을 입력해주십시오',
            10000,
            15000)

#discount : m - money, p - percentage, n - none / l - limited duration, u - unlimited
extra_info(['m', 1000, 'l', '2018-09-15', '2018-10-20'])


#True/False for 배송일 / 0,1,2 for 발송방법 
exposure_info(False, 0)

'''