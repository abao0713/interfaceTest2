from commonsrc import common
from commonsrc import configHttp
import readConfig as readConfig

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("userCase.xlsx", "login")
localAddAddress_xls = common.get_xls("userCase.xlsx", "addAddress")


# login
def get_login_cookies():
    host = localReadConfig.get_http("url")
    headers = {"Host": "www.mujin.assignee.com",
               "Connection": "keep-alive",
               "Content-Length": "2",
               "Accept": "application/json, text/plain, */*",
               "Origin": "https://www.mujin.assignee.com"

               }
    data = {"username":1222,"password":"Aa123456","jCaptchaCode":"","holder":"SPONSOR"

    }

    response = requests.post(host + "/api/login", data=data, headers=headers,
                             verify=False)
    info = response.json()
    cookie=response.cookies.get_dict()
    print("登录状态:",info["msg"])

    return cookie["ASSIGNEE_JSESSIONID"]

# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = common.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header
    header = {'token': token}
    localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()


