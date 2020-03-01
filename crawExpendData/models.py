from django.utils import timezone

from django.db import models

# Create your models here.
# 数据库表映射,写完后应该检查setting里的app install有没有添加这个应用


class USER(models.Model):
    userId = models.CharField(max_length=100, primary_key=True)
    cardId = models.IntegerField(default=0)
    stuId = models.CharField(max_length=20)
    stuPw = models.CharField(max_length=20)
    cookie = models.CharField(max_length=50)

    # def __str__(self):
    #     return "<'userId':{userId},'cardId':{cardId},'stuId':{stuId}>"\
    #         .format(userId=self.userId, cardId=self.cardId, stuId=self.stuId)


class EXPEND(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    userId = models.ForeignKey("USER", to_field='userId', on_delete=models.CASCADE)
    expendId = models.IntegerField(default=0)
    expendTime = models.DateTimeField(default=timezone.now)
    stuId = models.CharField(max_length=20)
    stuName = models.CharField(max_length=20)
    expendType = models.CharField(max_length=20)
    shopName = models.CharField(max_length=50)
    expendMoney = models.FloatField(default=0)
    vacancy = models.FloatField(default=0)

    class Mate:
        unique_together = ("stuId", "expendTime")

# 使用以下命令，创建数据库迁移文件
# python manage.py makemigrations

#
# python manage.py migrate
