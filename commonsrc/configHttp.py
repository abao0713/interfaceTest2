import requests
import readConfig as readConfig
from commonsrc.Log import MyLog as Log
from commonsrc.login import testlogin
import requests,json


localReadConfig = readConfig.ReadConfig()
s = testlogin().test_login()

class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0
        #self.cookies = get_login_cookies()
        #localConfigHttp.set_cookies(self.cookies)
    def set_url(self, host,url):
        """
        set url
        :param: interface url
        :return:
        """
        #self.url = scheme+'://'+host+url
        self.url = host+url
        return self.url
    def set_cookies(self,cookies):
        """

        :return:
        """
        self.cookies=cookies

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header


    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param


    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        requests.packages.urllib3.disable_warnings()
        try:
            return_data = s.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return return_data
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        requests.packages.urllib3.disable_warnings()
        try:

            return_data = s.post(self.url, headers=self.headers,  data=self.data, verify=False,timeout=float(timeout))
            # response.raise_for_status()
            info = return_data.json()

            return info

        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        requests.packages.urllib3.disable_warnings()
        try:
            response = s.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        requests.packages.urllib3.disable_warnings()
        try:
            response =s.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    a = ConfigHttp()
    b=a.set_url("/api/assignee/messageReminder/unread")
    print(b)