import sys
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
# import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
# from google_auth_oauthlib.flow import Flow

import google.oauth2.credentials
import google_auth_oauthlib.flow

from .info_functions import  (
    get_order_info,
    get_restaurant_info,
    get_customer_info,
    extract_item_details,
    extract_order_summary)

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
    data_obj = []
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
    
    # messages = []

# Request a list of all the messages
    result = service.users().messages().list(userId='me').execute()
    # result = service.users().messages().list(userId='me', q='in:inbox after:2024/02/13 before:2024/02/14').execute()
    # print("REquered messages betweeen dates :",result)
    # messages = result.get('messages')

    # GEt all messages obj 
    # messages = []
    # while 'messages' in result:
    #     # messages.extend(result['messages'])
    #     if 'nextPageToken' in result:
    #         page_token = result['nextPageToken']
    #         result = service.users().messages().list(userId='me', pageToken=page_token).execute()
    #     else:
    #         last_message = result.get('messages').pop() 
    #         txt = service.users().messages().get(userId='me', id=last_message['id']).execute()  # Get the full data of the last message
    #         payload = txt['payload']
    #         headers = payload.get('headers')
    #         for d in headers:
    #             if d['name'] == 'Date':
    #                 print(f"Date of the last email: {d['value']}")
    #         break    messages = []
    tokencount= 0
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

                
        # print("____________last_message of messages +++++++++++++> ", last_message)

    print("lenght of all mail++++++++++++++++++++++++++++>>>>>>>> ", len(list_messages))
    # print(messages)
    # '155729a36263a3c4'}, {'id': '1557292d6144a9e5', 'threadId': '1557292d6144a9e5'}, {'id': '155582c72f1164f7', 'threadId': '155582c72f1164f7'}, {'id': '15554c8850a36a85', 'threadId': '15554c8850a36a85'}, {'id': '15554c884030fb47', 'threadId': '15554c8850a36a85'}, {'id': '155196fef74b6050', 'threadId': '155196fef74b6050'}, {'id': '155196fee96098c7', 'threadId': '155196fee96098c7'}, {'id': '155196fed473b6e7', 'threadId': '155196fed473b6e7'}]
    print((f"Date of the last email: {first_mail_date}------> for {last_message}"))



# start_date = datetime.strptime('2024/02/13', '%Y/%m/%d').date()
# end_date = date.today()
    

    delta = dt.timedelta(days=1)
    start_date = datetime.strptime('2024/02/10', '%Y/%m/%d').date()
    # model_dates = SearchedDate.objects.filter(user=request.user).first().till_date
    # print(model_dates)
  
    end_date = date.today()
    while start_date <= end_date:
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
                print(subject)
                print(sender)

                # The Body of the message is in Encrypted format. So, we have to decode it.
                parts = payload.get('parts')
                if parts:
                    body_text, body_html = extract_message_body(parts)

                    # can change the condition here
                    if 'swiggy' in subject.lower():
                        print("Subject: ", subject)
                        print("From: ", sender)
                        

                        order_info_dict ={}
                        soup = BeautifulSoup(body_html, 'html.parser')

                        # print(extract_order_summary(soup))
                        order_info_dict['order_data'] = get_order_info(soup)
                        order_info_dict['restaurant'] = get_restaurant_info(soup)
                        order_info_dict['customer_info']= get_customer_info(soup)
                        order_info_dict['item_details'] = extract_item_details(soup)
                        order_info_dict['order_summary'] = extract_order_summary(soup)

                        data_obj.append(order_info_dict)

                        # print(data_obj)

            except Exception as e:
                # Handle the exception and print the details
                print(f"An exception occurred: {str(e)}") 
        start_date += delta
    return data_obj



            

