import requests,json
class test_login():
    def __init__(self):
        self.login_url = "http://admin.hopo.com.cn/api/v1/user/login"
        self.username = "hdp"
        self.password = "13267881403"
    def test_ho(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"
                   }
        da={
            "account":"hdp",
            "password":"13267881403"
        }
        #da=json.loads(da)
        response = requests.post(self.login_url,headers=headers,data=da,verify=False)
        info = response.json()
        token=info["content"]["access_token"]
        print(token)
        return token
if __name__ == '__main__':
    a=test_login()
    a.test_ho()