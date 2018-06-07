import requests
import readConfig as readConfig
import os
import xlrd
try:
    from xml.etree import ElementTree as ElementTree
except ImportError:
    from xml.etree import cElementTree as ElementTree
from commonsrc import configHttp as configHttp
from commonsrc.Log import MyLog as Log
import json


localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0


def get_visitor_token():
    """
    create a token for visitor
    :return:
    """

    host = localReadConfig.get_http("url")
    headers ={"Host": "www.mujin.assignee.com","Connection": "keep-alive","Content-Length": "2",
              "Accept": "application/json, text/plain, */*",
              "Origin": "https://www.mujin.assignee.com"}

    headers["Cookie"] = "ASSIGNEE_JSESSIONID="+localReadConfig.get_headers("cookie_v")
    response = requests.post(host+"/api/assignee/call/getLoginInfo",data=json.dumps({}),headers=headers,verify=False)
    info = response.json()
    if info["code"] == 0:
        token = info["data"]["tokencode"]
        print("获取token值的状态：",info["msg"])
        logger.debug("Create token:%s" % (token))
        return token
    else:
        msg = info["msg"]
        print(msg)
        return "abcdefg"

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


def set_visitor_token_to_config():
    """
    set cookie that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("token_v", token_v)

def set_login_cookie_to_config():
    """
    set cookie that created for visitor to config
    :return:
    """
    cookie_v = get_login_cookies()
    localReadConfig.set_headers("cookie_v", cookie_v)
#***************************compare_data*************************************8
def compare_data(case_module):

    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', 'program.xls')
    print(xlsPath)
    # open xls file
    with xlrd.open_workbook(xlsPath) as file:
        # get sheet by name
        sheet = file.sheet_by_name('assignee_module')
        nrows = sheet.nrows
        print(nrows)
        ncols = sheet.ncols   #列
        print(ncols)
        dic={}
        for i in range(0,nrows):
            for j in range(0,ncols):
                if (case_module == str(sheet.cell(i,j).value)):
                    print("在第%s行，第%s列"%(i+1,j+1))
                    a = i
                    b = j
                    break


        #i = i + 1
       # i
        #j = j + 1
        #j
        dic["case_name"] = sheet.cell(a,b-2).value
        dic["case_url"] = sheet.cell(a, b-1 ).value
        dic["case_method"] = sheet.cell(a,b+1).value
        logger.info("正在执行%s模块的测试"%dic["case_name"])
    return dic





def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    # 可以显示中文
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
# ****************************** read testCase excel ********************************



def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    print(xls_name)
    # open xls file
    file = xlrd.open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    print(cls)
    return cls

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/api/' + '/'.join(url_list)
    print(url)
    return url
def get_url_from_excel():
    url_list = []
    url_path = os.path.join(proDir,'testFile','case',)
    return url
#********************************核对结果是否正确******************************
def checkresult(json_response, return_data):
    """  函数递归，判断fix字典是否和return字典的部分内容一样

    :param fix_data: 正确的字典数据
    :param return_data: 返回的自动数据
    :return:
        """
    judge = False
    temp_data = dict()

    if isinstance(return_data,dict):
        return_data = json.loads(return_data)

    for key in json_response.keys():
        if isinstance(json_response[key], dict):  # 如果key是字典数据，进入递归判断
            if not checkresult(json_response[key], return_data[key]):
                return False

        elif isinstance(json_response[key], list):  # 如果key是数据，进入递归判断
            for num, n3 in enumerate(json_response[key]):
                for num1, n4 in enumerate(return_data[n]):
                    if not return_data[key]:
                        raise '{}返回数据为空'.format(key)
                    if checkresult(json_response[key][num], return_data[key][num1]):
                        judge = True  # 当存在相同数据，judge为真，结束该轮循环；否则，由于递归，judge自动为假，
                        break
                if not judge:  # 结束子循环后，judge没有为真，则可以判断数据不一致，返回False
                    return False

        else:
            if json_response[key] == return_data["key"]:  # 对非字典和列表的数据，进入判断
                continue
            else:
                temp_data['error_data'] = '{}:{} , {}:{}'.format(key, json_response[key], key,
                                                                                return_data.get(key))
                return False

        judge = False
    temp_data['error_data'] = ''

    return True








if __name__ == "__main__":
    compare_data("cs-20180601-002")