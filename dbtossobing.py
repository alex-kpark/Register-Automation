from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import json
import ast
from register_ssobing import *

#Step1 : Get Data from 4seller site
web_url = 'https://4seller.azurewebsites.net/ItemModelRegistrations/Details/4?json=1'

def get_html(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text
    return html

rawdata = get_html(web_url)

#Step2 : Serialize to make it as json
azuretojson = json.loads(rawdata)
prod_data = azuretojson["상품정보json"]

#(1)전체 모든 파일이 담겨있는 json (type은 dict로 정의되어있음)
initial_dict_data = json.loads(prod_data)

#(2)items 들이 담겨있는 json
#items 처음 시작하는 곳 부터 [] 시작하기 전까지 끊어냄
item_list_data = initial_dict_data["items"]
item_dict_data = ast.literal_eval(str(item_list_data[0])[0:502] + '}')

#(3)items 중에서 contents에 관련된 내용
#contents attribute이 시작하는 곳에서 알아서 인덱싱해놓음 (세부 항목만 알 수 있게 처리)
cont_start = str(item_list_data).find("'contentDetails'")
cont_end = str(item_list_data).find("detailType")
contents_str_data = '{' + str(item_list_data[0])[cont_start+19 : cont_end-4] + "}"
contents_dict_data = ast.literal_eval(contents_str_data)

def adult_transform():
    obj = item_dict_data["adultOnly"]
    if obj == 'EVERYONE':
        result = False
    else:
        result = True
    return result

#Step3 : 변수 대입(Coupang -> Ssobing)
name = initial_dict_data["displayProductName"]
legit_price = item_dict_data["originalPrice"]
disc_price = item_dict_data["salePrice"]
detailed_cont = contents_dict_data["content"]
brand_code = item_dict_data["barcode"]
a = initial_dict_data["productGroup"]
keywords = '값이 없습니다'
ourside_words = '값이 없습니다'
tax_bool = True
cancel_bool = True
adult_bool = adult_transform()
hscode_cont = 'AAA000111'
min_num = 0
max_num = item_dict_data["maximumBuyCount"]
multiple = [False]
delivery_info = [False, initial_dict_data["deliveryCharge"]]
sum_content = '값이 없습니다'
outside_words = '값이 없습니다'
id = '#id'
pw = '#pw'

#Step4 : 실행
ssobing_login(id, pw)
brand_classifier('여성의류')
product_info(name, sum_content, brand_code, keywords, outside_words, tax_bool, cancel_bool, adult_bool, hscode_cont)
selling_info(min_num, max_num, multiple)
delivery([False,0,5,10000,15000,0,0])
detailed_exp(detailed_cont)
price(legit_price, disc_price)
delivery(delivery_info)
final_upload()