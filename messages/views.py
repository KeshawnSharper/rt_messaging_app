from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.core.cache import cache


 
# Establishing the connection

conn = psycopg2.connect(
    database="rt_messaging_app",
    user='ksharper09',
    password='JavaScript101',
    host='rt-messaging-app-be.cpqo00kq2d0v.us-east-2.rds.amazonaws.com',
    port=5432
)

@csrf_exempt
def messages(request,email=None):
    if request.method == "GET":
        if email != None:
            cache_string = "get_messages_for"+email
        else:
            cache_string = 'get_all_messages'
        cached = cache.get(cache_string)
        if cached != None:
            return JsonResponse(cached, safe=False)
        result = []
        cursor = conn.cursor()
        if email is None:
            cursor.execute("""SELECT * FROM Messages;""")
        else:
            cursor.execute("""SELECT * FROM Messages WHERE receiver_email=%s OR sender_email=%s;""",(email,email))
        fetched = cursor.fetchall()
        print("fetched",fetched)
        for ele in fetched:
            result.append({"id":ele[3],"text":ele[0],"receiver_email":ele[1],"sender_email":ele[2],"date_sent":ele[4]})
        conn.commit()
        fetched = result
        cache.set(cache_string, result, timeout=3600)


        return JsonResponse(result, safe=False)
    
    
    if request.method == "POST":
        cursor = conn.cursor()
        print(request.body)
        body = json.loads(request.body)
        cache.delete_many(['get_all_messages',"get_messages_for"+body["receiver_email"],"get_messages_for"+body["sender_email"]])
        cursor.execute("""INSERT INTO Messages (text,receiver_email,sender_email,date_sent) VALUES (%s,%s,%s,%s)""",(body["text"],body["receiver_email"],body["sender_email"],datetime.now()))
        conn.commit()
        cursor.execute(""" SELECT * FROM Messages ORDER BY id DESC LIMIT 1 """)
        ele = cursor.fetchone()
        conn.commit()
        print(ele)
        return JsonResponse({"id":ele[3],"text":ele[0],"receiver_email":ele[1],"sender_email":ele[2],"date_sent":ele[4]}, safe=False)
    

    if request.method == "DELETE":
        cursor = conn.cursor()
        print(request.body)
        body = json.loads(request.body)
        cursor.execute("""DELETE FROM Messages WHERE id =%s""",([body["id"]]))
        conn.commit()
        fetched = {}
        return HttpResponse("Message Deleted!")
    
    if request.method == "PUT":
        cursor = conn.cursor()
        print(request.body)
        body = json.loads(request.body)
        cursor.execute("""UPDATE Messages SET text =%s WHERE id=%s""",(body["text"],body["id"]))
        conn.commit()
        fetched = {}
        return HttpResponse("Message updated!")


    