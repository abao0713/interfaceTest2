import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp
import warnings

assigneeInfo_xls = common.get_xls("assignee.xls", "api")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir
@paramunittest.parametrized(*assigneeInfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, No, api_name, HOST, request_url, method, request_data_type,request_data,return_data,check_data,result):
        """
        set params
        :return:
        """
        self.No = No
        self.api_name = api_name
        self.HOST = str(HOST)
        self.request_url = str(request_url)
        self.method = method
        self.request_data_type = request_data_type
        self.request_data = request_data.encode('utf-8')
        print(self.request_data)
        self.return_data = None
        self.result = None
    def description(self):
        """
        :return:
        """
        self.api_name
    def setUp(self):
        """
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        warnings.simplefilter("ignore", ResourceWarning)
    def testGetProductInfo(self):
        """
        test body
        :return:
        """
        localConfigHttp.set_url(self.HOST,self.request_url)
        localConfigHttp.set_data(self.request_data)
        if self.No !='No':
            if self.method == 'get':
                # get http
                self.response = localConfigHttp.get()
                self.info = json.loads(self.json_response)
                print(self.info)
                # check result
                common.check_result(self.return_data, self.info)

            else:
                # post http
                #response.setContentType("charset=utf-8”)

                self.return_data = localConfigHttp.post()
                if self.return_data["code"] == 0:
                    self.info = json.loads(self.json_response)
                    self.log.write_result(self.info)
                    # check result
                    #common.check_result(self.return_data, self.info)
                    #

                else:
                    msg = self.return_data["msg"]
                    code = self.return_data["code"]
                    self.logger.debug(msg)
                    self.log.build_case_line(self.api_name,msg)

    def tearDown(self):
        """
        :return:
        """
        self.log.build_end_line(self.api_name)



if __name__ == '__main__':
    a = ProductInfo()
    a.testGetProductInfo()



