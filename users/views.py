from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.cache import cache
import json


 
# Establishing the connection

conn = psycopg2.connect(
    database="rt_messaging_app",
    user='ksharper09',
    password='JavaScript101',
    host='rt-messaging-app-be.cpqo00kq2d0v.us-east-2.rds.amazonaws.com',
    port=5432
)

@csrf_exempt
def users(request,email=None):
        if request.method == "GET":
            cached = cache.get('users')
            if cached != None:
                 return JsonResponse(cached, safe=False)
            result = []
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM Users;""")
            fetched = cursor.fetchall()
            for ele in fetched:
                result.append({"id":ele[0],"display_name":ele[1],"email":ele[2],"image":ele[3]})
            conn.commit()
            fetched = result
            cache.set('users', result, timeout=3600)

            return JsonResponse(result, safe=False)
    
    
        if request.method == "POST":
            cursor = conn.cursor()
            print(request.body)
            body = json.loads(request.body)
            cursor.execute("""INSERT INTO Users (display_name,email,image) VALUES (%s,%s,%s)""",(body["display_name"],body["email"],body["image"]))
            conn.commit()
            cursor.execute(""" SELECT * FROM Users ORDER BY id DESC LIMIT 1 """)
            ele = cursor.fetchone()
            conn.commit()
            cache.delete("users")
            return JsonResponse({"id":ele[0],"display_name":ele[1],"email":ele[2],"image":ele[3]}, safe=False)
            
        if request.method == "DELETE":
            cursor = conn.cursor()
            print(request.body)
            body = json.loads(request.body)
            cursor.execute("""DELETE FROM Users WHERE id =%s""",([body["id"]]))
            conn.commit()
            fetched = {}
            return HttpResponse("User Deleted!")
