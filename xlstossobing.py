#-*- coding: utf-8 -*-

import xlrd
from collections import OrderedDict
import json

from register_ssobing import *

'''
1. Main()함수에 Excel File넣으면
    - Excel파일 len()만큼 돌면서 반복
    - register 파일에서 정의되어있는 변수에 값 들을 다 넣어주고
    - register 파일 activate
    - 그리고 돌아옴
    - try.. except Exception as e 구문으로 만들면서 에러체크

'''


id = 'id'
pw = 'pw'

register_ssobing()

'''
ssobing_login(id, pw)

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
'''