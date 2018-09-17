#-*- coding: utf-8 -*-

import xlrd
from collections import OrderedDict
import json

#open workbook
#move to the sheets: sheet_by_inde(0..1..2..3..)
wb = xlrd.open_workbook('smartstore.xls')
sh = wb.sheet_by_index(0)

order_list = []

for rownum in range(1, sh.nrows):
    order = OrderedDict()
    row_values = sh.row_values(rownum)
    order['product_number'] = row_values[0]
    order['order_number'] = row_values[1]
    order['order_date'] = row_values[2]
    order['order_status'] = row_values[3].decode('utf-8')
    order['claim_status'] = row_values[4]
    order['product_name'] = row_values[5]
    order['option_info'] = row_values[6]
    order['amount'] = row_values[7]
    order['customer_name'] = row_values[8]
    order['customer_id'] = row_values[9]

    order_list.append(order)

json_file = json.dumps(order_list)

with open('data.json', 'w') as f:
    f.write(json_file)


'''
#row and column value
first_row = sh.row_values(0)
first_column = sh.col_values(0)

#indi cell
#(row, column)=(0,0)=A1셀
cell_d4 = sh.cell(1,0).value
print(cell_d4)
'''