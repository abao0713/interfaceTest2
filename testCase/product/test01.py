import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp as configHttp

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
    #   用例执行前登录服务器
        common.get_login_cookies()
        common.set_login_cookie_to_config()
    def testGetProductInfo(self):
        """
        test body
        :return:
        """




        # set url
        localConfigHttp.set_url(self.url)
        # set headers
        cookie_token = localReadConfig.get_headers("cookie_v")
        headers = {"Cookie": "ASSIGNEE_JSESSIONID="+str(cookie_token)}
        headers["Content-Type"] = "application/json;charset=UTF-8"
        localConfigHttp.set_headers(headers)

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



