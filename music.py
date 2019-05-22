import requests
import xlrd
import time,json
import hashlib


filePath = 'E:\Auto_Test\ybj20190320.xlsx'
print(filePath)
headers = {
    'Content-Type': "application/json"
    }


# 1、打开文件
data = xlrd.open_workbook(filePath)

# 2、获取sheet对象
table = data.sheet_by_index(0)
nrows = table.nrows#行数
for i in range(1,nrows):
    value = table.cell(i, 0).value
    print(value)
    name = value.split('=')[-1]
    url =value.split('?')[0]
    s = int(time.time() * 1000)  # 当前时间对应reqCode，timestamp
    timestamp = str(s)
    print(s)  # reqCode，timestamp两个值相等
    h = 'Aa1234567' + timestamp + timestamp
    m = hashlib.md5()  # 加密
    m.update(h.encode(encoding='utf-8'))  # 生成加密串，其中h是要加密的字符串，对应sign字段
    sign = m.hexdigest()
    param = {"data":name}

    data = {'reqCode': timestamp,
             'accountName': "1223",
             'timestamp': timestamp,
             'sign': sign
             }
    return_data = requests.request("POST", url, data=json.dumps(data), headers=headers, params=param,verify=False)
#    print(return_data.text)
    with open('E:\工作文档\工作资料\music\%s' % name, 'wb') as f:
        f.write(return_data.content)
    print('下载完成')



    """
    info = return_data.json()
    if info['code'] == 0:
        with open('E:\工作文档\工作资料\music\%s'%name, 'wb') as f:
            f.write(return_data.content)
        print('下载完成')
    else:
        print(info["msg"])"""