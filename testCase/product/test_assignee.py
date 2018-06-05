import unittest
import paramunittest
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp as configHttp

assigneeInfo_xls = common.get_xls("assignee.xls", "assignee_num")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir


@paramunittest.parametrized(*assigneeinfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, case_module, case_num, cookie, token, json_request, json_response,result):
        """
        set params

        :return:
        """
        self.case_name,self.case_url,self.case_method = str(common.compare_data(case_module))
        self.case_num = str(case_num)
        self.cookie = str(cookie)
        self.token = str(token)
        self.json_request = json_request
        self.json_response = json_response
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
        url = self.case_url

        localConfigHttp.set_url(url)
        localConfigHttp.set_params(self.json_request)
        # set headers
        if self.token == '' or self.token == 'null':
            cookie_token = localReadConfig.get_headers("cookie_v")
        else:
            cookie_token = localReadConfig.get_headers("tooken_v")
        headers = {"Cookie": "ASSIGNEE_JSESSIONID="+str(cookie_token)}
        localConfigHttp.set_headers(headers)
        if self.case_method == 'get':
            # get http
            self.response = localConfigHttp.get()
            # check result
            self.checkResult()
        else:
            # post http
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

    def _cmp(fix_data, return_data):
        """  函数递归，判断fix字典是否和return字典的部分内容一样

        :param fix_data: 正确的字典数据
        :param return_data: 返回的自动数据
        :return:
        """
        for n1 in fix_data:
            if isinstance(fix_data[n1], dict):  # 如果n1是字典数据，进入递归判断
                if not SHTestCase._cmp(fix_data[n1], return_data.get(n1)):
                    return False

            elif isinstance(fix_data[n1], list):  # 如果n1是列表数据，进入递归判断
                for num, n3 in enumerate(fix_data[n1]):
                    for num1, n4 in enumerate(return_data[n1]):
                        if not return_data[n1]:
                            raise '{}返回数据为空'.format(n1)
                        if SHTestCase._cmp(fix_data[n1][num], return_data[n1][num1]):
                            SHTestCase.judge = True  # 当存在相同数据，judge为真，结束该轮循环；否则，由于递归，judge自动为假，
                            break
                    if not SHTestCase.judge:  # 结束子循环后，judge没有为真，则可以判断数据不一致，返回False
                        return False

            else:
                if fix_data[n1] == return_data.get(n1):  # 对非字典和列表的数据，进入判断
                    continue
                else:
                    SHTestCase.temp_data['error_data'] = '{}:{} , {}:{}'.format(n1, fix_data[n1], n1,
                                                                                return_data.get(n1))
                    return False
        SHTestCase.judge = False
        SHTestCase.temp_data['error_data'] = ''
        return True






if __name__ == '__main__':
    testGetProductInfo()