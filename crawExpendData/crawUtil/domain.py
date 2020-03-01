import requests
from lxml import etree
from crawExpendData.crawUtil.drawAccount import getAllData

# 获取cookie


def getCookie():
    url = 'http://10.0.101.44/homeLogin.action'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }

    response = requests.get(url, headers=headers)

    cookie = requests.utils.dict_from_cookiejar(response.cookies)['JSESSIONID']
    # print("获取的Cookie：", cookie)
    return cookie


# 获取验证码
def getImage(headers):
    getImgUrl = 'http://10.0.101.44/getCheckpic.action?rand=6068.183442310069'

    response = requests.get(getImgUrl, headers=headers)

    # 写入数据-获取验证码图片
    # with open("resources/1.png", 'wb')as f:
    #     f.write(response.content)

    return response.content


# 登录
def login(headers, name, passwd, rand):
    print("请输入验证码结果")
    # rand = input()

    loginUrl = 'http://10.0.101.44/loginstudent.action'

    getAccountUrl = 'http://10.0.101.44/accounthisTrjn.action'

    loginParams = {
        'name': name,
        'userType': '1',
        'passwd': passwd,
        'loginType': '2',
        'rand': rand
    }

    requests.get(loginUrl, headers=headers, params=loginParams)

    response = requests.get(getAccountUrl, headers=headers)

    html = etree.HTML(response.content, etree.HTMLParser())
    result = html.xpath('//option[1]/@value')
    print("获取的账号是：", result[0])
    return result[0]


# 爬取信息
def getData(headers, account, startDate, endDate):
    print("正在爬取···")

    url1 = 'http://10.0.101.44/accounthisTrjn1.action'
    url2 = 'http://10.0.101.44/accounthisTrjn2.action'
    url3 = 'http://10.0.101.44/accounthisTrjn3.action'

    params = {

        'account': account,
        'inputObject': 'all',
        'Submit': '+%C8%B7+%B6%A8+',

        'inputStartDate': startDate,
        'inputEndDate': endDate
    }

    requests.get(url1, headers=headers, params=params)

    requests.get(url2, headers=headers, params=params)

    response = requests.get(url3, headers=headers, params=params)

    # 写入数据
    # with open("resources/result.html", 'wb')as f:
    #     f.write(response.content)

    # 爬取所有数据
    print("结束")
    return getAllData(content=response.content.decode(encoding="gbk"), headers=headers)


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'Cookie': 'JSESSIONID='+getCookie()
# }
#
# getImage(headers=headers)
#
# getData(headers=headers, account=login(headers=headers), startDate='20191001', endDate='20191030')
