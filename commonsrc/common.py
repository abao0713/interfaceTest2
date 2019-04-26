import requests
import readConfig as readConfig
import os
import yaml
from assertpy import assert_that
import xlrd
from xlutils3.copy import copy
import re

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
    #保存cookies

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
        if sheet.row_values(i)[0] != u'case_module':
            cls.append(sheet.row_values(i))
#    print(cls)
    return cls
def get_case_yaml(case_yaml):
    """
    accept yaml data
    :param a:
    :param b:
    :return:
    """
    yaml_data=[]
    xlsPath = os.path.join(proDir, "testFile", case_yaml)
    print(xlsPath)
    # open xls file
    with open(xlsPath,'r',encoding="UTF-8") as file:

        try:
            alldata = yaml.load(file)
            for data in alldata:
                if "request" in data:
                    #print(alldata[data])
                    yaml_data.append(alldata[data])

        except:
            print("hhhhh")

        print(yaml_data)

    return yaml_data

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


def checkfail(name1,name2):
    if name1==name2:
        print("牛逼")
    else:
        print("哈哈")


def check_result(response={}, hope_response={}, value=0):

    # 当value=0时只校验key

    if value == 0:

        for n1 in hope_response:

            # print "n1:",n1

            # 如果值是字典类型

            if isinstance(hope_response[n1], dict):

                # print "dict"

                if not check_result(response=response.get(n1),hope_response=hope_response[n1]):
                    checkfail(response.get(n1), hope_response[n1])

                    return False

                    #print('{},{}'.format(hope_response[n1], response[n1]))

            elif isinstance(hope_response[n1], list):

                # print "list"

                for hope_index, hope_listValue in enumerate(hope_response[n1]):

                    #print ("hope_index:",hope_index)

                    #print ("hope_listValue:",hope_listValue)

                    for response_index, response_listValue in enumerate(response[n1]):

                        #print ("response_index:",response_index)

                        #print ("response_listValue:",response_listValue)

                        if isinstance(hope_listValue, dict):

                            check_result(response=response[n1][response_index],
                                                                          hope_response=hope_response[n1][
                                                                              response_index])

                        else:

                            try:

                                print("hope_listValue:", hope_listValue, type(hope_listValue))

                                print("response_listValue:", response_listValue, type(response_listValue))

                                assert_that(hope_response[n1][hope_index]).is_equal_to(response[n1][hope_index])

                            except AssertionError as ex:

                                checkfail(response=response[n1][hope_index],hope=hope_response[n1][hope_index])

                                raise Exception('Expected <%s> to be not equal to <%s>, but was not.' % (
                                hope_response[n1][hope_index], response[n1][hope_index]))

            else:

                # 当时sring类型

                try:

                    #assert_that(response).contains_key(n1)
                    assert  n1 in response

                    print("n1:", n1)


                except (AssertionError, TypeError) as ex:

                    checkfail(name1=response, name2=n1)

                    raise Exception('%s <%s> is not dict-like: missing keys()' % (response, n1))





    # 校验key和value

    else:

        try:



            assert_that(hope_response).is_equal_to(response)

        except AssertionError as ex:

            checkfail(response, hope_response)

            raise Exception('Expected <%s> to be not equal to <%s>, but was not.' % (response, hope_response))

    return True

 # 向某个单元格写入数据
def write_data(filepath,row, col, value):
    data = xlrd.open_workbook(filepath)  # 打开指定的excel文件
    data_copy = copy(data)  # 复制原文件使的文件可以改动
    sheet = data_copy.get_sheet(0)  # 取得复制文件的sheet对象
    sheet.write(row, col, value)  # 在某一单元格写入value
    data_copy.save(filepath)  # 保存文件
    #输入值可以知道值在excel的位置
def local(filepath,sheet_name,str):
    """

    :param filepath: 文件地址
    :param sheet_name: 表单名称
    :param str: 需要查询的字符
    :return: 返回行和列值
    """
    data = xlrd.open_workbook(filepath)
    sheet = data.sheet_by_name(sheet_name)  # 名字的方式
    nrows = sheet.nrows  # 行
    ncols = sheet.ncols  # 列
    for i in range(nrows):
        for j in range(ncols):
            if str == sheet.cell(i, j).value:
                return i,j
    #lng = table.cell(i, 3).value  # 获取i行3列的表格值
    #lat = table.cell(i, 4).value  # 获取i行4列的表格值



if __name__ == "__main__":
    check_result(response={}, hope_response={}, value=0)
