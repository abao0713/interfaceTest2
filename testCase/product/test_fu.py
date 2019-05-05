import unittest
import paramunittest
import json
from commonsrc import common
from commonsrc.Log import MyLog
import readConfig as readConfig
from commonsrc import configHttp
import warnings,os
import xlrd
from xlutils3.copy import copy
from commonsrc.test_login import test_login
import time


assigneeInfo_xls = common.get_xls("test_fus.xls", "api")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
proDir = readConfig.proDir
@paramunittest.parametrized(*assigneeInfo_xls)
class ProductInfofu(unittest.TestCase):
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
        self.Return_data = None
        self.Result = None
        print(self.Api_name)
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

    def testGetProductInfofu(self):
        """
        test body
        :return:
        """
        localConfigHttp.set_url(self.Host,self.Request_url)
        if self.No != 'No':

            a = test_login()
            token = a.test_fu()
            time.sleep(3)

            headers = {"content-type": "application/x-www-form-urlencoded",
                       "Authorization":token}
            Request_data = json.loads(self.Request_data)
            #Request_data = json.dumps(self.Request_data)
            localConfigHttp.set_headers(headers)
            localConfigHttp.set_data(Request_data)
            if self.No != 'No':
                if self.Method == 'get':
                    # get http
                    self.response = localConfigHttp.get()
                    if self.response.status_code != 201:
                        httpcode = self.response.status_code
                        value = "http"+str(httpcode)
                        result = "http"+str(httpcode)
                        print(self.response.content.decode(encoding='utf-8'))
                    #self.info = json.loads(self.json_response)

                    else:
                        self.info = self.response.content.decode(encoding='utf-8')
                        self.info = json.loads(self.info)

                        print(self.response.content.decode(encoding='utf-8'))
                        if self.info["error_code"] == 0:
                            msg = self.info["msg"]
                            value = msg
                            result = 1
                        else:
                            msg = self.info["msg"]
                            code = self.info["error_code"]
                            self.logger.debug(msg)
                            print(msg + 'cg')
                            self.log.build_case_line(self.Api_name, msg)
                            value = msg
                            result = code

                    # check result
                    """
                    if common.check_result(self.Return_data, self.response):
                        value = 1
                        result = 1
                    else:
                        value = 0
                        result = 0
                """
                else:
                    # post http
                    # response.setContentType("charset=utf-8��)

                    return_data = localConfigHttp.post()
                    if return_data.status_code != 201:
                        httpcode = return_data.status_code
                        result = "http"+str(httpcode)
                        value = "http"+str(httpcode)
                    else:

                        self.response = return_data.json()

                        if self.response["error_code"] == 0:
                            msg = self.response["msg"]
                            value = msg
                            self.info = self.response
                            print(self.info)
                            #self.log.write_result(msg)

                            result = 1
                            # check result
                            # common.check_result(self.return_data, self.info)
                            #

                        else:
                            msg = self.response["msg"]
                            code = self.response["error_code"]
                            self.logger.debug(msg)
                            print(msg+'cg')
                            self.log.build_case_line(self.Api_name, msg)
                            value = msg
                            result = code

            print(value,result)
            #xlsPath = os.path.join(proDir, "testFile", 'case', 'test_ho.xlsx')
            filepath = os.path.join(proDir, "testFile", 'case', 'test_fus_result.xls')
            #filepath = os.path.join(proDir, "testFile", 'case', 'test_ho.xlsx')
            i, j = common.local(filepath=filepath, sheet_name='api', str=self.No)  # ��λ��ѯ�ֶ��ڵڼ��еڼ���
            data = xlrd.open_workbook(filepath)  # ��ָ����excel�ļ�
            data_copy = copy(data)  # ����ԭ�ļ�ʹ���ļ����ԸĶ�
            sheet = data_copy.get_sheet(0)  # ȡ�ø����ļ���sheet����
            sheet.write(i, j+9, result)  # ��ĳһ��Ԫ��д��value
            sheet.write(i,j+7,value)
            #filepath = os.path.join(proDir, "testFile", 'case', 'test_ho_result.xlsx')
            data_copy.save(filepath)  # �����ļ�


        else:
            self.logger.debug('no json is')


    def tearDown(self):
        """
        :return:
        """
        self.log.build_end_line(self.Api_name)


if __name__ == '__main__':

    a = ProductInfofu()
    a.testGetProductInfofu()


