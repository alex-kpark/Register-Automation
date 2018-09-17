from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains

from time import sleep

#Login 
driver = webdriver.Chrome('C:/Users/PC/AppData/Local/Programs/Python/chromedriver.exe')
driver.get('http://www.ssobing.com/selleradmin/login/index')

id = 'InputIdHere'
pw = 'InputPasswordHere'

input_id = driver.find_element_by_xpath("//input[contains(@name, 'main_id')]")
input_pw = driver.find_element_by_xpath("//input[contains(@name, 'main_pwd')]")

input_id.send_keys(id)
input_pw.send_keys(pw)

login = driver.find_element_by_xpath("//input[contains(@class, 'submit_btn')]")
login.send_keys(Keys.ENTER)

driver.get('http://www.ssobing.com/selleradmin/goods/regist')

action = action_chains.ActionChains(driver)

def brand_classifier(a):
    category_btn = driver.find_element_by_xpath("//button[contains(@id, 'categoryConnectPopup')]")
    category_btn.click()
    sleep(3)

    misc_btn = driver.find_element_by_xpath("//option[contains(@value, 'B002')]")
    misc_btn.click()
    sleep(3)

    female_bag = driver.find_element_by_xpath("//option[contains(@value, 'B0020009')]")
    female_bag.click()
    sleep(3)

    tote_bag = driver.find_element_by_xpath("//option[contains(@value, 'B00200090004')]")
    tote_bag.click()
    sleep(3)

    action.send_keys(Keys.COMMAND+Keys.ALT+'i')

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
    #청약철회 가능하면 True, 아니면 False
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

    #Multiple Purchase multiple = [Bool, cond_num, obj_num2, 'p' or 'w(won)']
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

        if delivery_info[1] != 0:
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

def final_upload():
    #save_info = driver.find_element_by_xpath("//span[@class='btn large black']/button[@onclick='goods_save('view')']")
    save_info = driver.find_element_by_xpath("//ul[@class='page-buttons-right']")
    save_info.click()

    save_submit = driver.find_element_by_xpath("//button[@id='openDialogLayerConfirmYesBtn']")
    save_submit.click()

brand_classifier('여성의류')

product_info('샘플 이름을 입력합니다',
            '설명을 입력합니다',
            '브랜드코드를 입력합니다',
            '검색어1을 입력',
            '외부검색1을 입력',
            False,
            True,
            True,
            178272
            )
selling_info(3,10, [True, 4, 10, 'p'])
delivery([False,0,5,10000,15000,0,0])

final_upload()