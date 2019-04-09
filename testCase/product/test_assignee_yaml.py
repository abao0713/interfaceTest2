import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp
from commonsrc import login

assigneeInfo_yaml = common.get_case_yaml("assignee.yaml")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir
@paramunittest.parametrized(*assigneeInfo_yaml)
class ProductInfo(unittest.TestCase):
    def setParameters(self, name, url, method, headers, json, result):
        """
        set params
        :return:
        """
        self.name = str(name)
        self.url = str(url)
        self.method = str(method)
        self.headers = headers
        self.json = json
        self.result = str(result)
        self.return_data = None
        self.info = None
    def description(self):
        """
        :return:
        """
        self.name
    def setUp(self):
        """
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
    def testGetProductInfo(self):
        """
        test body
        :return:
        """
        # set url
        localConfigHttp.set_url(self.url)
        if self.method == 'get':
            # get http
            localConfigHttp.set_params(params)
            self.response = localConfigHttp.get()
            self.info = json.loads(self.json)
            print(self.info)
            # check result
            common.check_result(self.result, self.info)
        else:
            # post http
            #response.setContentType("charset=utf-8”)
            localConfigHttp.set_data(self.json)
            self.return_data = localConfigHttp.post()
            if self.return_data["code"] == 0:
                self.info = json.loads(self.json)
                print(self.info)
                # check result
                common.check_result(self.return_data, self.info)
                #
            else:
                msg = self.return_data["msg"]
                print("接口结果异常：",msg)
    def tearDown(self):
        """
        :return:
        """
        self.log.build_end_line(self.name)



if __name__ == '__main__':
    a = ProductInfo()
    a.testGetProductInfo()



