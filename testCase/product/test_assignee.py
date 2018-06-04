import unittest
import paramunittest
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp as configHttp

assigneeInfo_xls = common.get_xls("assignee.xls", "assignee_num")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*assigneeinfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, case_module, case_num, cookie, token, json_request, json_response,result):
        """
        set params

        :return:
        """
        self.case_num = str(case_num)
        self.cookie = str(cookie)
        self.token = str(token)
        self.json_request = json_request
        self.codejson_response = json_response
        self.result = str(result)
        self.response = None
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

    def testGetProductInfo(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('read')

        localConfigHttp.set_url(self.url)
        # set params

        if self.method == 'get':
            param = None
        elif self.params == '':
            param = {}
        else:
            param = 'null'
        localConfigHttp.set_params(param)
        # set headers
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")
        else:
            token = self.token
        headers = {"token": str(token)}
        localConfigHttp.set_headers(headers)
        # get http
        self.response = localConfigHttp.post()
        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            goods_id = common.get_value_from_return_json(self.info, "data", "goods_id")
            self.assertEqual(goods_id, self.goodsId)
        if self.result == '1':
            self.assertEqual(self.info['code'], self.info['code'])
            self.assertEqual(self.info['msg'], self.msg)
if __name__ == '__main__':
    testGetProductInfo()