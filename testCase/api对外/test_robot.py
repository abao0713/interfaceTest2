import time
import hashlib
from commonsrc import configHttp
import xlrd
import json

s=int(time.time()*1000)#当前时间对应reqCode，timestamp
e=str(s)
print(s)#reqCode，timestamp两个值相等
h='Aa1234567'+e+e
m= hashlib.md5()#加密
m.update(h.encode(encoding='utf-8')) #生成加密串，其中h是要加密的字符串，对应sign字段
print (m.hexdigest())

def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print(end_time - start_time)

    return wrapper
class test():
