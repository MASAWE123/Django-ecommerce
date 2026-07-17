import os
os.environ['DJANGO_SETTINGS_MODULE']='ecom.settings'
import django
django.setup()

Brevo_api=os.environ.get("Brevo_api")

from brevo import Brevo
from brevo.transactional_emails import(
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)


to_email ="larsonmwai45@gmail.com"
customer_name="masawe"
def send_email(to_email,customer_name):
    client= Brevo(api_key=Brevo_api)
    print("API Key:", Brevo_api)
    try:
        response = client.transactional_emails.send_transac_email(
            subject="Payment Received",
            html_content=f"""
            <h2>Thank you for shopping with us!</h2>

            <p>Hello <b>{customer_name}</b>,</p>

            <p>Your payment has been received successfully.</p>

            <p>We appreciate your business.</p>
            """,

            sender = SendTransacEmailRequestSender(
                name ="masawe",
                email ="masawe@masawe.store"
            ),
   
        to =[
            SendTransacEmailRequestToItem(
                email=to_email,
                name =customer_name
            )
        ]
    )
        print(response)
        return response
    except Exception as e:
        print(e)
 

send_email(to_email,customer_name)