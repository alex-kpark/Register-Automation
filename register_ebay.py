#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

#For OSX
#driver = webdriver.Chrome('/usr/local/bin/chromedriver')

#For Windows
driver = webdriver.Chrome('C:/Users/PC/AppData/Local/Programs/Python/chromedriver.exe')
driver.get('https://www.esmplus.com/Member/SignIn/LogOn?ReturnValue=-7')

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

def category(cate_name):
    search_esm = driver.find_element_by_xpath("//input[@placeholder='ESM 카테고리명 검색']")
    search_esm.send_keys(cate_name)
    esm_click = driver.find_element_by_xpath("//img[@src='http://pics.esmplus.com/front/sell/icon_search.gif']")
    esm_click.click()
    sleep(1)
    esm_result = driver.find_elements_by_xpath("//em[@class='keyword']")
    esm_target = esm_result[4]
    esm_target.click()
    sleep(1)

    press_keys = ActionChains(driver)

    auc_cates = driver.find_elements_by_xpath("//select[@style='width: 160px;']")
    auc_cates[0].find_element_by_xpath("//option[contains(text(), '가방/패션잡화')]").click()
    auc_cates[1].click()
    press_keys.key_down(Keys.DOWN).perform()
    press_keys.key_down(Keys.ENTER).perform()
    sleep(2)
    auc_cates[2].click()
    press_keys.key_down(Keys.DOWN).perform()
    press_keys.key_down(Keys.ENTER).perform()
    sleep(3)    
    
    gmk_ops = driver.find_elements_by_xpath("//select[@style='width: 215px;']/option[@value='[object Object]']")
    gmk_ops[3].click()
    sleep(2)

    gmk_cates = driver.find_elements_by_xpath("//select[@style='width: 215px;']")    
    gmk_cates[1].click()
    press_keys.key_down(Keys.DOWN).perform()
    sleep(2)
    press_keys.key_down(Keys.ENTER).perform()
    sleep(1)

    gmk_min = driver.find_element_by_xpath("//select[@style='width: 214px;']")
    gmk_min.click()
    press_keys.key_down(Keys.DOWN).perform()
    sleep(2)
    press_keys.key_down(Keys.ENTER).perform()
    sleep(1)

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
        
def exposure_info(deliver_date, deliver_method, product_detail):
    
    move_btn = driver.find_element_by_xpath("//li[@class='menu_item2']")
    move_btn.click()

    #image input 가져온 다음에 로컬에 있는 주소를 넣어주면 됨
    image_regi = driver.find_element_by_xpath("//input[@name='btnSelectFile']")
    image_regi.send_keys("C:/Users/PC/Desktop/AutomateRegister/image.jpeg")

    #상품세부정보
    info_btn = driver.find_element_by_xpath("//a[@id='btnNewDesc']")
    info_btn.click()

    test = driver.window_handles
    
    for i in range(0,3):
        try:
            driver.switch_to_window(test[i])
            close_ebaypop = driver.find_element_by_xpath("//button[@class='slider-roll-button slider-roll-next']")
            
            for t in range(0,9):
                close_ebaypop.click()

            start_write = driver.find_element_by_class_name('layer-close-button')
            sleep(3)
            start_write.click()
            section_write = driver.find_element_by_xpath("//div[@class='ee-contents']")
            section_write.send_keys(product_detail)
            save_write = driver.find_element_by_xpath("//button[@id='btnSave']")
            save_write.click()
            save_end = driver.find_element_by_xpath("//button[@class='ee-button ee-button-positive']")
            save_end.click()

            window_before = driver.window_handles[0]
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_before)
            
        except Exception as e:
            print('fail')

    driver.switch_to_frame("ifm_TDM395")
    
    #상품정보공시 입력 - 카테고리에 따라 value 입력
    product_type = driver.find_element_by_xpath("//select[@id='ddlOfficialNotiGroup']/option[@value='3']")
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
        direct_deliv.click()

def legal_info(prod_type, expect_deliv, fabric, color, size, importer, nation, caution, assurance, respons):
    areas = driver.find_elements_by_xpath("//textarea[@name='noti_item_value']")
    areas[0].send_keys(prod_type)
    areas[1].send_keys(expect_deliv)
    areas[2].send_keys(fabric)
    areas[3].send_keys(color)
    areas[4].send_keys(size)
    areas[5].send_keys(importer)
    areas[6].send_keys(nation)
    areas[7].send_keys(caution)
    areas[8].send_keys(assurance)
    areas[9].send_keys(respons)
    print('success')

def finish():
    driver.find_element_by_xpath("//li[@class='menu_item3']").click()
    driver.find_element_by_xpath("//li[@class='menu_item4']").click()
    finish_btn = driver.find_element_by_xpath("//img[@src='http://pics.esmplus.com/front/sell/syi_save.gif']")
    finish_btn.click()
    
    finish_attempt = driver.window_handles[2]
    driver.switch_to_window(finish_attempt)
    driver.find_element_by_xpath("//label[@id='lbConfirmForGoodsImage']").click()
    driver.find_element_by_xpath("//label[@id='lblConfirmForGoodsName']").click()
    driver.find_element_by_xpath("//label[@id='lblConfirmForSellerDiscount']").click()
    driver.find_element_by_xpath("//label[@id='lblConfirmForGoodsPrice']").click()

    final_btn = driver.find_element_by_xpath("//img[@src='http://pics.esmplus.com//front/sell/btn_final_confirm.gif']")
    final_btn.click()


#Activate from here
login('pineapples', 'joejoe11!!')

auc = True
gmk = True

select_market()

category('여성가방')

product_info('제품명',
            '프로모션',
            10000,
            15000)

gmk_prod_info('English Please',
            '你好',
            'エンジニア')

duration(60)

#discount : m - money, p - percentage, n - none / l - limited duration, u - unlimited
extra_info(['m', 1000, 'l', '2018-09-22', '2018-10-20'])

exposure_info(False, 0, '상품의 자세한 정보를 이곳에 입력해주세요')

legal_info('종류를 입력해주세요',
            '기간을 입력해주세요',
            '소재를 입력해주세요',
            '색상을 입력해주세요',
            '크기를 입력해주세요',
            '제조사를 입력해주세요',
            '생산지를 입력해주세요',
            '조심히 다루어주세요',
            '고객의 과실 시 환불 불가',
            '010-0000-0000')

finish()
