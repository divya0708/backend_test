# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from users.models import *
import uuid
import ast


@csrf_exempt
def adding_user_details(request):
    status = ''
    status_code = ''
    message = ''
    data = dict()

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        user_id = requestData.get("user_id",None)
        user_name = requestData.get("user_name",None)
        timezone = requestData.get("timezone",None)
        activity_period = requestData.get(u"activity_period", None)
        # {"Activity_Period":{"1":{"start_time":"Feb 1 2020  1:33PM","end_time":"Feb 1 2020 1:54PM"},"2":{"start_time":"Mar 1 2020  11:11AM","end_time":"Mar 1 2020 2:00PM"},"3":{"start_time":"Mar 16 2020  5:33PM","end_time":"Mar 16 2020 8:02PM"}}}

        primary_key=uuid.uuid4()
        create_user,created=User.objects.get_or_create(user_id=user_id,user_name=user_name,\
            timezone=timezone,defaults={"primary_key":primary_key})

        if created:
            
            if activity_period != None and activity_period != '':
                activity_period = ast.literal_eval(str(activity_period))
                activity_period = activity_period['Activity_Period']
                for key,value in activity_period.items():
                    ActivityPeriod.objects.create(user=create_user, start_time=value["start_time"], end_time=value["end_time"])
            
            data.update({"primary_key":primary_key})
            status = "Success"
            message = "User added successfully"
            status_code = 200

        else:
            status = "Failed"
            message = "User already exists"
            status_code = 409

    except:
        status = "Failed"
        message = "Try Again Later"
        status_code = 400

    return JsonResponse({"status":status,"data":data,"message":message,"status_code":status_code}, status=status_code)

###############################################

@csrf_exempt
def getting_user_details(request):
    status = ''
    status_code = ''
    message = ''
    data = dict()
    activity = list()

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        primary_key = requestData.get(u"primary_key", None)
        user_id = requestData.get(u"user_id", None)
        user_name = requestData.get(u"user_name", None)
        # Enter any one from primary_key, user_id, user_name
        if primary_key != None:
            user_details=User.objects.get(primary_key=primary_key)
        if user_id != None:
            user_details=User.objects.get(user_id=user_id)
        if user_name != None:
            user_details=User.objects.get(user_name=user_name)

        try:
            activity_details=ActivityPeriod.objects.filter(user=user_details)
            print(activity_details)
            for i in activity_details:
                activity.append({"start_time":i.start_time,"end_time":i.end_time})
            data.update({"id":user_details.user_id, "real_name":user_details.user_name, "tz":user_details.timezone,\
                "activity_periods":activity})

            status = "Success"
            message = "User details"
            status_code = 200

        except Exception as e:
            status = "Failed"
            message = "User details does not exist"
            status_code = 404

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400

    return JsonResponse({"status":status,"data":data,"message":message,"status_code":status_code}, status=status_code)