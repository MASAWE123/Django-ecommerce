import os
os.environ['DJANGO_SETTINGS_MODULE']='ecom.settings'
import requests
import json

import django
django.setup()
ZETTATEL_USERID=os.environ.get('ZETTATEL_USERID')
ZETTATEL_PASSWORD =os.environ.get('ZETTATEL_PASSWORD')
ZETTATEL_SENDERID=os.environ.get('ZETTATEL_SENDERID')
phone = ['254707008119']
message = "you order have being received"
def send_sms():
    url = "https://portal.zettatel.com/SMSApi/send"

  
    payload = {
           "userid":ZETTATEL_USERID,
           "password":ZETTATEL_PASSWORD,
           "senderid":ZETTATEL_SENDERID,
           "sendMethod":"quick",
           "msgType":"text",
           "duplicatecheck":"true",
           "sms":[
            {
                "mobile":phone,
                "msg":message
            }
           ]       
           
    }

    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload),timeout=5)
    print("Status Code:",response.status_code)
    print("Response Text:",response.text)
    return response.text

send_sms()