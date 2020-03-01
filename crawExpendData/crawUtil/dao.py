import time

from crawExpendData.models import EXPEND, USER


def insertExpend(dataList, userId):

    for js in dataList:
        # 时间相关的转换
        timeArray = time.strptime(js["交易发生时间"], "%Y/%m/%d %H:%M:%S")
        expendTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 写入数据
        expend = EXPEND(id=expendTime+js['学号'], expendTime=expendTime, stuId=js["学号"], stuName=js['姓名'], expendType=js['交易类型'],
                        shopName=js['商户名称'], expendMoney=js['交易额'], vacancy=js['现有余额'], expendId=js['次数'])
        expend.userId = USER(userId=userId)
        expend.save()
    return None