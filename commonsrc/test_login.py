
import requests,json
class test_login():
    def __init__(self):
        self.login_url = "http://admin.hopo.com.cn/api/v1/user/login"
        self.login_url_fu = "http://admin.hopo.com.cn/abc_admin/v1/admin_user/user_sign"
        self.username = "hdp"
        self.funame = "ybj"
        self.password = "13267881403"
        self.fuword = "ybj123456"
    def test_ho(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"
                   }
        da={
            "account":self.username,
            "password":self.password
        }
        #da=json.loads(da)
        response = requests.post(self.login_url,headers=headers,data=da,verify=False)
        print("login failure print as follows" + response.text)
        #print(response.text)
        info = response.json()
        if info["error_code"] ==0:

            token=info["content"]["access_token"]
            print(token)
            return token
    def test_fu(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"
                   }
        da={
            "user_name":self.funame,
            "password":self.fuword
        }
        #da=json.loads(da)
        re = requests.options(self.login_url, headers=headers)
        #print(re.status_code)
        response = requests.post(self.login_url_fu,headers=headers,data=da,verify=False)
        print("login failure print as follows"+response.text)
        info = response.json()
        if info["error_code"] ==0:

            token=info["content"]["token"]
            print(token)
            return token
if __name__ == '__main__':
    a=test_login()
    a.test_fu()