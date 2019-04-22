import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp
import warnings

assigneeInfo_xls = common.get_xls("test_ho.xlsx", "api")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir
@paramunittest.parametrized(*assigneeInfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, No, Api_name, Host, Request_url, Method, Request_data_type,Request_data,Return_data,Check_data,Result):
        """
        set params
        :return:
        """
        self.No = No
        self.Api_name = Api_name
        self.Host = str(Host)
        self.Request_url = str(Request_url)
        self.Method = Method
        self.Request_data_type = Request_data_type
        self.Request_data = Request_data
        print(type(self.Request_data))
        self.Return_data = None
        self.Result = None
        self.dicts = {}
    def description(self):
        """
        :return:
        """
        self.Api_name
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
        localConfigHttp.set_url(self.Host,self.Request_url)
        if self.Request_data_type == 'json':

            Request_data = json.dumps(self.Request_data)
            localConfigHttp.set_data(Request_data)
            if self.No != 'No':
                if self.Method == 'get':
                    # get http
                    self.response = localConfigHttp.get()
                    self.info = json.loads(self.json_response)
                    print(self.info)
                    # check result
                    if common.check_result(self.return_data, self.info):
                        self.dicts[self.No] = 1
                    else:
                        self.dicts[self.No] = 0

                else:
                    # post http
                    # response.setContentType("charset=utf-8”)

                    self.response = localConfigHttp.post()
                    if self.response["code"] == 0:
                        self.info = json.loads(self.response)
                        self.log.write_result(self.info)
                        self.dicts[self.No] = 1
                        # check result
                        # common.check_result(self.return_data, self.info)
                        #

                    else:
                        msg = self.response["msg"]
                        code = self.response["code"]
                        self.logger.debug(msg)
                        print(msg)
                        self.log.build_case_line(self.Api_name, msg)
                        self.dicts[self.No] = 0
            print(self.dicts)
        else:
            self.logger.debug('非json入参')


    def tearDown(self):
        """
        :return:
        """
        self.log.build_end_line(self.Api_name)



if __name__ == '__main__':
    a = ProductInfo()
    a.testGetProductInfo()

