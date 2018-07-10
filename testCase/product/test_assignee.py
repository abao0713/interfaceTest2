import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp as configHttp

assigneeInfo_xls = common.get_xls("assignee.xls", "assignee_num")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir


@paramunittest.parametrized(*assigneeInfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, case_module, case_num, cookie, token, json_request, json_response,result):
        """
        set params

        :return:
        """
        self.case_module = str(case_module)

        #self.case_name = common.compare_data(case_module).get("case_name")
        #self.case_url = common.compare_data(case_module).get("case_url")
        #self.case_method= common.compare_data(case_module).get("case_method")
        self.case_num = str(case_num)
        self.cookie = str(cookie)
        self.token = str(token)
        self.json_request = json_request
        self.json_response = json_response
        self.result = str(result)
        self.return_data = None
        self.info = None



    def description(self):
        """

        :return:
        """
        self.case_num


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
        case_name = common.compare_data(self.case_module).get("case_name")
        print(case_name)
        self.case_url = common.compare_data(self.case_module).get("case_url")
        case_method= common.compare_data(self.case_module).get("case_method")

        localConfigHttp.set_url(self.case_url)
        localConfigHttp.set_data(self.json_request)

        # set headers
        if self.token == '' or self.token == 'null':
            cookie_token = localReadConfig.get_headers("cookie_v")
        else:
            cookie_token = localReadConfig.get_headers("token_v")
        headers = {"Cookie": "ASSIGNEE_JSESSIONID="+str(cookie_token)}
        headers["Content-Type"] = "application/json;charset=UTF-8"
        localConfigHttp.set_headers(headers)

        if case_method == 'get':
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
                print(self.info)
                # check result
                common.check_result(self.return_data, self.info)
                #
            else:
                msg = self.return_data["msg"]
                logger.debug("接口结果异常：",msg)

    def tearDown(self):
        """

        :return:
        """
        self.log.build_end_line(self.case_num)



if __name__ == '__main__':
    a = ProductInfo()
    a.testGetProductInfo()



