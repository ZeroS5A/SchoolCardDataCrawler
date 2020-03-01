import json
import requests
from lxml import etree

# for i in result:
#     content = etree.tostring(i, encoding='utf-8', pretty_print=True, method="html").decode('utf-8')
#     print(content)

# for i,word in enumerate(content1):
#     print(word)
#     dict[head[]]


# 提取消费数据
def drawExpendData(content):
    # 数据清洗：
    html = etree.HTML(content, etree.HTMLParser())
    head = html.xpath('//tr[@class="bl"]/td/text()')
    # contains()
    content = html.xpath('//tr[contains(@class,"listbg")]/td/text()')

    dataList = []
    # 循环内容的长度
    for i in range(0, len(content)):
        # 判断内容的学号是学号时，进入赋值到字典，且商户不为‘支付宝’（为空会扰乱循环）
        if content[i] == content[2] and content[i + 1] != '支付宝转账' and content[i + 1] != '补助':
            # 设置k为-2，即学号前2，为日期开始
            k = -2
            tempDict = {}
            # 进入循环赋值字典与值
            for j in range(0, 9):
                # strip为删除空格
                tempDict[head[j]] = content[i + k].strip()
                k += 1

            # 加入字典列表，并向前移动7位置
            dataList.append(tempDict)
            i += 7
    # json转换
    # jsonArr = json.dumps(dataList, ensure_ascii=False)
    return dataList


# 是否有下一页
def hasNextPage(content):
    html = etree.HTML(content, etree.HTMLParser())
    page = html.xpath('//a[@href="javascript:button14_Onclick();"]/text()')
    if len(page) == 0:
        return False
    else:
        print("下一页")
        return True


# 获取所有数据
def getAllData(content, headers):
    dataList = []
    page = 2

    url = 'http://10.0.101.44/accountconsubBrows.action'

    while True:
        # 打印捉取的内容
        dataList += drawExpendData(content)
        # print(dataList)
        if hasNextPage(content):

            params = {
                'pageNum': page
            }

            content = requests.get(url, headers=headers, params=params).content.decode(encoding="gbk")
            page += 1
        else:
            break

    return dataList


# Cookie是否过期
def hasCookie(headers):
    url = 'http://10.0.101.44/accounthisTrjn.action'
    content = requests.get(url, headers=headers).content.decode(encoding="gbk")
    html = etree.HTML(content, etree.HTMLParser()).xpath('//p[@class="biaotou"]/text()')
    if len(html) == 0:
        return True
    else:
        return False

# content = open('../resources/result.html', 'r').read()
# getAllData(content)


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'Cookie': 'JSESSIONID=F7F300FEBEF1B1619B297D51E9E2EBEE'
# }
# if hasCookie(headers=headers):
#     print("access")
