import json
import time

from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection

from .crawUtil.dao import insertExpend
from .crawUtil.drawAccount import hasCookie
from .models import USER, EXPEND
from crawExpendData.crawUtil.domain import *

# Create your views here.
from .util.getOpenId import getOpenId


def selectUser(request):
    userId = request.GET['userId']
    print(userId)

    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM user WHERE userId='"+userId+"'")
    # result = cursor.fetchall()
    # for rs in result:
    #     print(rs[2])
    # return HttpResponse("hello,this is demo1,"+userId)

    # user = USER(userId=userId, stuId='170202', stuPw='0903')
    # user.save()
    # 获取ORM信息
    user = USER.objects.filter().values()
    print(list(user))
    # 转换成json返回
    return JsonResponse(list(user), safe=False)


# def insertExpend(request):
#     dataList = request.body.decode("utf-8")
#     # 通过json.load,把json解码成字典
#     jsonArr = json.loads(dataList)
#     for js in jsonArr:
#         # 时间相关的转换
#         timeArray = time.strptime(js["交易发生时间"], "%Y/%m/%d %H:%M:%S")
#         expendTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#         # 写入数据
#         expend = EXPEND(id=expendTime+js['学号'], expendTime=expendTime, stuId=js["学号"], stuName=js['姓名'], expendType=js['交易类型'],
#                         shopName=js['商户名称'], expendMoney=js['交易额'], vacancy=js['现有余额'], expendId=js['次数'])
#         expend.userId = USER(userId='user1')
#         expend.save()
#     return HttpResponse("success")


def getImageCode(request):
    cookie = getCookie()
    userId = getOpenId(request.headers['Authorization'])
    if userId:
        user = USER.objects.get(userId=userId)
        # 更新cookie
        if user.userId:
            user.cookie = cookie
            user.save()
        else:
            user = USER(userId=userId, cookie=cookie)
            user.save()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'JSESSIONID=' + cookie
        }
        imageCode = getImage(headers=headers)
        return HttpResponse(imageCode, content_type='image/png')
    else:
        return HttpResponse("badToken")


def setStuData(request):
    userId = getOpenId(request.headers['Authorization'])
    if userId:
        print(userId)
        stuId = request.GET['stuId']
        stuPw = request.GET['stuPw']
        user = USER(userId=userId, stuId=stuId, stuPw=stuPw)
        user.save()
        return HttpResponse("success")
    else:
        return HttpResponse("badToken")


def stuLogin(request):
    userId = getOpenId(request.headers['Authorization'])
    if userId:
        rand = request.GET['rand']
        user = USER.objects.get(userId=userId)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'JSESSIONID=' + user.cookie
        }
        user.cardId = login(headers=headers, name=user.stuId, passwd=user.stuPw, rand=rand)
        user.save()

        return HttpResponse("success")
    else:
        return HttpResponse("badToken")


def drawData(request):
    userId = getOpenId(request.headers['Authorization'])
    # 判断是否拿到了openid
    if userId:
        startDate = request.GET['startDate']
        endDate = request.GET['endDate']
        user = USER.objects.get(userId=userId)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'JSESSIONID=' + user.cookie
        }
        if hasCookie(headers=headers):
            dataList = getData(headers=headers, account=user.cardId, startDate=startDate, endDate=endDate)
            # 写库
            insertExpend(dataList=dataList, userId=userId)

            return JsonResponse(dataList, safe=False)
        else:
            return HttpResponse("badCookie")
    else:
        return HttpResponse("badToken")


def redisTest(request):
    userId = getOpenId(request.headers['Authorization'])
    user = USER.objects.get(userId=userId)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Cookie': 'JSESSIONID=' + user.cookie
    }
    if hasCookie(headers=headers):
        return HttpResponse("success")
    else:
        return HttpResponse("error")
