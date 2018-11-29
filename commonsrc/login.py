import requests

'''在登陆模块创建一个全局session，在其他接口操作时带入登陆时的session，保持session的一致性'''
s = requests.Session()#定义一个全局session
class testlogin():
    def __init__(self):
        self.login_url = "https://robot.zhilingsd.com/api/login?userAccount=aybj&password=Aa123456"
        self.username = "aybj"
        self.password = "Aa123456"
    def test_login(self):
        da={
            "userAccount":self.username,
            "password":self.password}
        response = s.post(self.login_url,json=da)
        info = response.json()
        print(info)
        return s
if __name__ == '__main__':
    a=testlogin()
    a.test_login()