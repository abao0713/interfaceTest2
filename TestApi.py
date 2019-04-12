# -*- coding:utf-8 -*-
import time
import hashlib
import json
import unittest
from commonsrc import configHttp


localConfigHttp = configHttp.ConfigHttp()
def hash_robot():
    s = int(time.time() * 1000)  # 当前时间对应reqCode，timestamp
    timestamp = str(s)
    h = 'Aa1234567' + timestamp + timestamp
    print(h)
    m = hashlib.md5()  # 加密
    m.update(h.encode(encoding='utf-8'))  # 生成加密串，其中h是要加密的字符串，对应sign字段
    sign = m.hexdigest()
    return timestamp,sign

class test_robot(unittest.TestCase):
    @classmethod  # 这里的装饰器@classmethod必须有，标识为一个类方法
    def setUpClass(cls):
        """setUpClass为类的初始化方法，在整个类运行前执行只执行一次"""
        global baseurl
        baseurl = 'https://www.zhiling.robotsh.com'

    @classmethod
    def tearDownClass(cls):
        """和setUpclass类似，在调用整个类测试方法完成后执行一次"""
        pass
    #催记导出
    def test5_caseinfo(self):

        timestamp,sign = hash_robot()
        # 数据
        data = {'batchId': 2704,
                'offset' : 1,
                'limit' : 6
                }
        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data
                 }
        #self.param = self.param1.encode('utf-8')
        request_url = '/api/api/task/exportMark'
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("催记导出接口正常")
        else:
            print("催记导出接口异常")
            print(self.return_data["msg"])
    #外呼结果查询
    def test4_result(self):
        request_url = '/api/api/task/exportApiCallRecord'
        timestamp, sign = hash_robot()
        # 数据
        data = {'batchName': 'ybj556325862',
                'billCode': 'TE-ybj-0219-0794'

                }
        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("外呼结果查询接口正常")
        else:
            print("外呼结果查询接口异常")
            print(self.return_data["msg"])

    #新建批次
    def test1_import(self):
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/importBatch'
        global aname
        aname = 'ybj'+timestamp

        ainfo = [{
			'billCode':'api-YBJ-20190403-0953',
			'productName':'现金贷',
			'productType':'信用卡',
			'creditCardType':'金卡',
			'customerCode':'0056',
			'loanInstitution':'招行',
			'borrowerName':'袁韩韩',
			'borrowerAge':'53',
			'borrowerGender':'男',
			'borrowerIdnumber':'440881199805148016',
			'borrowerPhone':'13686821736',
			'borrowerAccount':'8015',
			'borrowerCard':'8015',
			'divideNum':'3',
			'openCardDate':'2018-05-05',
			'isFirst':'是',
			'currency':'人民币',
			'overdueDay':'10',
			'overdueDate':'2018-10-05',
			'limitRepayDate':'2019-12-01',
			'bankPhone':'0755-26742656',
			'commitMoney':'6500',
			'caseProvince':'广东',
			'caseCity':'深圳',
			'registeredProvince':'广东',
			'registeredCity':'深圳',
			'educationLevel':'本科',
			'yearIncome':'100w',
			'creditLine':'15',
			'cashAmount':'15',
			'applyCreditScore':'150',
			'behaviorScore':'100',
			'marriageStatus':'已婚',
			'normalRepayCount':'1',
			'underCommitCount':'1',
			'aboveCommitCount':'1',
			'contact1Name':'李化',
			'contact1Tel':'13686821736',
			'contact1Relation':'朋友一',
			'contact2Name':'',
			'contact2Tel':'',
			'contact2Relation':'',
			'contact3Name':'',
			'contact3Tel':'',
			'contact3Relation':''
		}]

        data = {'taskName': aname,#批次名称
                'callLines': '22',#线路数
                'strategyCode': 'SG000002',#策略编号
                'batchType': '信用卡',#产品类型
                'startDate': '',#开始日期
                'startTime': '09:30',#每日开始时间
                'endTime' : '21:00',#每日结束时间
                'executeTime': [{'beginTime':'09:02',
                                 'endTime': '10:12'},
                                {'beginTime': '14:10',
                                 'endTime': '20:12'}
                                ],
                'caseInfos' :ainfo#案件信息
                }

        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("新建批次案件导入接口正常")
        else:
            print("新建批次案件导入接口异常")
            print(self.return_data["msg"])
    #案件还款
    def test6_hunan(self):
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/importRepay'
        # 数据

        data1 = [{'billCode':'api-YBJ-20190403-0953','latestRepayMoney':'2345',
                  'latestRepayDate':'2019-04-10'}]
        data = {'repayCases': data1, 'batchName': aname}


        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("案件还款接口正常")
        else:
            print("案件还款接口异常")
            print(self.return_data["msg"])

    #批量洗号任务上报
    def test2_clean(self):
        global clean_name
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/cleanAPIUpload'
        # 数据
        data = {'phoneList': ['15270239931','13008921160','13011960942']}



        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data

                 }

        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("批量洗号任务上报接口正常")
            clean_name = self.return_data["data"]
            print(clean_name)
        else:
            print("批量洗号任务上报接口异常")
            print(self.return_data["msg"])

    #批量洗号结果查询
    def test3_check(self):

        timestamp, sign = hash_robot()
        request_url = '/api/api/task/getCleanResult'
        # 数据
        data = {'proId': clean_name}

        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': data

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("批量洗号结果查询接口正常")
        else:
            print("批量洗号结果查询接口异常")
            print(self.return_data["msg"])

    #批次暂停
    def test7_pause(self):
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/pauseBatch'
        # 数据

        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': aname

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("批次暂停接口正常")
        else:
            print("批次暂停接口异常")
            print(self.return_data["msg"])
    #重启批次
    def test8_start(self):
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/continueBatch'
        # 数据

        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': aname

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("批次重启接口正常")
        else:
            print("批次重启接口异常")
            print(self.return_data["msg"])

    #通过批次名称取消批次
    #@unittest.skip
    def test9_end(self):
        timestamp, sign = hash_robot()
        request_url = '/api/api/task/stopBatch'
        # 数据

        param = {'reqCode': timestamp,
                 'accountName': 1223,
                 'timestamp': timestamp,
                 'sign': sign,
                 'data': aname

                 }
        localConfigHttp.set_url(baseurl, request_url)
        headers = {'content-type': 'application/json'}
        localConfigHttp.set_headers(headers)
        param = json.dumps(param)
        print(param)
        localConfigHttp.set_data(param)
        self.return_data = localConfigHttp.post()
        print(self.return_data)
        if self.return_data["code"] == 0:
            print("取消批次接口正常")
        else:
            print("取消批次接口异常")
            print(self.return_data["msg"])












if __name__ == "__main__":
    unittest.main()