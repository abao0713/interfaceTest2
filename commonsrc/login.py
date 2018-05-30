from readConfig import ReadConfig
import requests
def login_status(self):
    self.username = ReadConfig.get_user_info("username")
    self.password = ReadConfig.get_user_info("password")
    data = {
        username: 'username', password: 'password'
    }
    session = requests.session()
    loginurl = "http://xxx.com/login"
    # 具体要接口登录后才可以获得cookies
    result = session.post(loginurl, data=data)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return cookies
