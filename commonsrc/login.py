from readConfig import ReadConfig
import requests
def login_status():
    username = ReadConfig.get_user_info(self,"username")
    password = ReadConfig.get_user_info(self,"password")
    data = {
        'username': username, 'password': password,
        'jCaptchaCode':'','holder':'SPONSOR'
    }
    session = requests.session()
    loginurl = "https://www.mujin.assignee.com/api/login"
    # 具体要接口登录后才可以获得cookies
    result = session.post(loginurl, data=data)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    # return cookies
if __name__ == '__main__':
    print(login_status())