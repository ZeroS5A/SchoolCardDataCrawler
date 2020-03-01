from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db import connection


def demo(request):
    cursor = connection.cursor()
    # cursor.execute("INSERT INTO user (stuId,stuPw) VALUES ('1702021044','09035')")
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    for rs in result:
        print(rs[2])
    return HttpResponse("hello,this is demo1,", result)
