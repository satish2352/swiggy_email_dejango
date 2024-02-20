import sys
from .models import SearchedDate
# sys.path.append(r'C:\Users\vijay.c\Desktop\sumago\day 1\New folder')
from django.shortcuts import render,redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import datetime as dt
from bs4 import BeautifulSoup
import re
from .models import SearchedDate
from datetime import datetime,date
from django.utils import timezone
import pytz
# import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
# from google_auth_oauthlib.flow import Flow
from dateutil import parser
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
from django.db import IntegrityError
from .models import Restaurant, Customer, Order, Item, Payment


from .info_functions import  (
    get_order_info,
    get_restaurant_info,
    get_customer_info,
    extract_item_details,
    extract_order_summary)



def Scrap_data_add(request,data):
        # Check if any field contains 'not found'
    if 'not found' in data['restaurant']['restaurant_name'].lower() or \
        'not found' in data['restaurant']['restaurant_address'].lower() or \
        'not found' in data['customer_info']['customer_name'].lower() or \
        'not found' in data['customer_info']['customer_address'].lower() or \
        'not found' in data['order_data']['Order No:'].lower() or \
        'not found' in data['order_data']['Order placed at:'].lower() or \
        'not found' in data['order_data']['Order delivered at:'].lower() or \
        'not found' in data['order_data']['Order Status'].lower() or \
        'not found' in str(data['order_summary']['Order Total']).lower():
        return None
        
    # Check if the Customer object exists, if not create a new one
    customer, created = Customer.objects.get_or_create(
        user = request.user,
        cname=data['customer_info']['customer_name'],
        caddress=data['customer_info']['customer_address']
    )
    print('customer created', created)
    
    # Create and save the Restaurant object
    restaurant, created = Restaurant.objects.get_or_create(
        rname=data['restaurant']['restaurant_name'],
        raddress=data['restaurant']['restaurant_address']
    )
    print('restaurant created',created)
    # Create and save the Order object
    order_placed_at = datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order placed at:'].lower() else None
    order_delivered_at = datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order delivered at:'].lower() else None


    
    try: 
        order , order_created = Order.objects.get_or_create(
        restaurant = restaurant,
        order_number=data['order_data']['Order No:'],
        order_placed_at=order_placed_at,
        order_delivered_at=order_delivered_at,
        order_status=data['order_data']['Order Status'],
        customer=customer,
        order_total=data['order_summary']['Order Total']
    )
        if not order_created:
            return None
        
        for item in data['item_details']:
            if 'not found' in item[0].lower() or 'not found' in str(item[1]).lower() or 'not found' in str(item[2]).lower():
                continue
            items_added ,item_created= Item.objects.get_or_create(
                order=order,
                iname=item[0],
                quantity=item[1],
                price=item[2]
            )
        order_summary = data.get('order_summary', {})  # Get order_summary if exists, otherwise empty dictionary
        payment_data, payment_created = Payment.objects.get_or_create(
            order=order,
            payment_method='Unknown',  # Update this as per your data
            items_total=order_summary.get('Item Total', 0.0),
            packing_charges=order_summary.get('Order Packing Charges', 0.0),
            platform_fee=order_summary.get('Platform fee', 0.0),
            delivery_partner_fee=order_summary.get('Delivery partner fee', 0.0),
            discount_applied=order_summary.get('Discount Applied', 0.0),
            taxes=order_summary.get('Taxes', 0.0),
            order_total=order_summary.get('Order Total', 0.0)
        )
    except IntegrityError as e:
        print("errorr as ",e)
        return None

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def extract_message_body(parts):
    body_text = ""
    body_html = ""

    for part in parts:
        if part.get('body') and part['body'].get('data'):
            data = part['body']['data'].replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data).decode('utf-8')

            # Append both text and HTML versions
            body_text += BeautifulSoup(decoded_data, 'html.parser').get_text()
            body_html += decoded_data

    return body_text, body_html

# start_date = datetime.strptime('2024/01/01', '%Y/%m/%d').date()
# end_date = date.today()

def getEmails(request):
    count=0
    creds = None
    # token_file_path = os.path.join(os.getcwd(), 'tokens', 'token.pickle')
    # if os.path.exists(r'tokens\token.pickle'):
    if os.path.exists(f'tokens/{request.user}.pickle'):
        print('token path exist')
        
        with open(f'tokens/{request.user}.pickle', 'rb') as token:
            print("rb mode token file as token if exist token path")
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        print("executed if not creds or not valid")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\vijay.c\Desktop\sumago\day 1\New folder\project\credentials.json', SCOPES)
                # r'C:\Users\vijay.c\Downloads\credentials.json', SCOPES)
            flow.redirect_uri = 'http://127.0.0.1:8000/registration/oauth2callback'

            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open(f'tokens/{request.user}.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    profile = service.users().getProfile(userId='me').execute()
    total_emails = profile['messagesTotal']
    print(f'Total emails: {total_emails}')

    date_model_instance = SearchedDate.objects.get(user=request.user) # SEARCHEDDATE MODEL INSTANCE
    # print(date_model_instance)

    result = service.users().messages().list(userId='me').execute()
    tokencount= 0
    if not date_model_instance.check_updated:
        while 'messages' in result:
            # messages.extend(result['messages'])
            if 'nextPageToken' in result:
                print("Has next token",tokencount)
                tokencount += 1
                page_token = result['nextPageToken']
                result = service.users().messages().list(userId='me', pageToken=page_token).execute()
            else:
                # print('reslult of last token', result)
                list_messages = result.get('messages')
                # print(list_messages)
                while list_messages :
                    last_message = list_messages.pop()  # Get the last message
                    # last_message2 = list_messages.pop(0)  # Get the last message
                    # print("this is laast_message1",last_message)
                    # print("this is laast_message2",last_message2)
                    txt = service.users().messages().get(userId='me', id=last_message['id']).execute()
                    payload = txt.get('payload',None)
                    if payload:
                        headers = payload.get('headers',None)
                        if headers:
                            for d in headers:
                                if d['name'] == 'Date':
                                    first_mail_date = d['value']
                                    # print(last_msg_date)
                                    break
                        else:
                            continue
                        break
                    else:
                        continue
                break
        # date_model_instance = SearchedDate.objects.get(user=request.user) # SEARCHEDDATE MODEL INSTANCE
        last_mail_date_obj = parser.parse(str(first_mail_date)).date()
        date_model_instance.till_date = last_mail_date_obj
        date_model_instance.check_updated = True
        date_model_instance.save()

# start_date = datetime.strptime('2024/02/13', '%Y/%m/%d').date()
# end_date = date.today()
    

    delta = dt.timedelta(days=1)
    if date_model_instance.from_date:
        start_date = date_model_instance.from_date
    else:
        start_date = date_model_instance.till_date
    
  
    end_date = date.today()
    while start_date <= end_date + delta:
        query = f'after:{(start_date - delta).strftime("%Y/%m/%d")} before:{start_date.strftime("%Y/%m/%d")}'
        result = service.users().messages().list(userId='me', q=query).execute()
        
        messages = result.get('messages', [])

    
        for msg in messages:
            # print("msg ------------------------------------------------------------>>>>>>",msg)
            count += 1
            print(count)
            print(f"AFTER{start_date - delta}  Before:: {start_date}")
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            # print("txt",txt)
            # Use try-except to avoid any Errors
            try: 
                # Get value of 'payload' from dictionary 'txt'
                payload = txt.get('payload')
                if not payload:
                    continue

                headers = payload.get('headers')
                if not headers:
                    continue
                for d in headers:
                    if d['name'] == 'Date':
                        print(f"Date of the email: {d['value']}")

                # Look for Subject and Sender Email in the headers
                subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
                sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
                print("subject of mail :: ", subject)
                print('sender of mail ::',sender)

                # The Body of the message is in Encrypted format. So, we have to decode it.
                # if payload.get('mimeType') == 'text/plain':
                #     body = payload.get('body')
                #     data = body.get('data')
                #     print()
                #     if data:
                #         text = base64.urlsafe_b64decode(data).decode()
                #         print('text','--------------------->',text)

                # parts = payload.get('parts')
                if 'swiggy' in subject.lower():
                    print("subject of mail inif: ", subject)
                    print("sender of mail inif: ", sender)

                    if 'swiggy' in subject.lower():
                        parts = payload.get('parts')
                        if parts:
                            body_text, body_html = extract_message_body(parts)
                            

                    # if payload.get('mimeType') == 'text/html':
                    #     body = payload.get('body')
                    #     data = body.get('data')
                    #     if data:
                    #         body_html = base64.urlsafe_b64decode(data).decode()

                    #         if body_html:
                    #             print("BODY_HTML  READING",)


                    # body_text, body_html = extract_message_body(parts)
                            # body_html = html
                            # print("subject of mail inif: ", subject)
                            # print("sender of mail inif: ", sender)

                
                            # can swiggy email subject here.
                            # print("Subject.lower() -->",subject.lower())
                            # if 'swiggy' in subject.lower():
                                # print("Subject: ", subject)
                                # print("From: ", sender)
                                

                            order_info_dict ={}
                            soup = BeautifulSoup(body_html, 'html.parser')

                            # print(extract_order_summary(soup))
                            order_info_dict['order_data'] = get_order_info(soup)
                            order_info_dict['restaurant'] = get_restaurant_info(soup)
                            order_info_dict['customer_info']= get_customer_info(soup)
                            order_info_dict['item_details'] = extract_item_details(soup)
                            order_info_dict['order_summary'] = extract_order_summary(soup)

                            # data_obj.append(order_info_dict)
                            Scrap_data_add(request,order_info_dict)
                            order_info_dict={}

                        # print(data_obj)

            except Exception :
                # Handle the exception and print the details
                print(f"An exception occurred: {str(Exception)}") 
        start_date += delta

        # date_model_instance = SearchedDate.objects.get(user=request.user) # SEARCHEDDATE MODEL INSTANCE
        # UPDATE FROM_DATE WITH START_DATE
        date_model_instance.from_date = (start_date-delta)
        date_model_instance.save()
    return True



            

