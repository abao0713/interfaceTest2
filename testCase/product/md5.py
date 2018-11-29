import time
import hashlib
import xlrd
import json
s=int(time.time()*1000)
e=str(s)
print(s)
h='Aa123456'+e+e
print(h)
m= hashlib.md5()
m.update(h.encode(encoding='utf-8')) #生成加密串，其中h是要加密的字符串
print (m.hexdigest())


data = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\api.xlsx')
table = data.sheets()[0]
# print(table)
# nrows = table.nrows #行数
# ncols = table.ncols #列数
# c1=arange(0,nrows,1)
# print(c1)

start = 1  # 开始的行
end = 10  # 结束的行


list_values = []
for x in range(start, end):

    row = table.cell_value(x,0)
    a=int(row)
    list_values.append(a)
# print(list_values)
data_json = json.dumps(list_values)
print(list_values)
print(data_json)