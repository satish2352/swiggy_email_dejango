import sys
# sys.path.append(r'C:\Users\vijay.c\Desktop\sumago\day 1\New folder')
from django.shortcuts import render,redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
import re
from datetime import datetime
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
            # flow.redirect_uri='https://swiggyscraper.pythonanywhere.com/oauth2callback'
            # print("flow--------------->", flow)
            # creds = flow.run_local_server(port=0)
    #         creds = flow.run_local_server(
    # host='localhost',
    # port=8088,
    # authorization_prompt_message='Please visit this URL: {url}',
    # success_message='The auth flow co.',
    # open_browser=True)
            
   

# Required, call the from_client_secrets_file method to retrieve the client ID from a
# client_secret.json file. The client ID (from that file) and access scopes are required. (You can
# also use the from_client_config method, which passes the client configuration as it originally
# appeared in a client secrets file but doesn't access the file itself.)
    
            # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            #             # r'C:\Users\vijay.c\Desktop\sumago\day 1\New folder\project\credentials.json', SCOPES)
            #             r'C:\Users\vijay.c\Desktop\sumago\day 1\New folder\project\credentials.json', SCOPES)

        # Required, indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        # flow.redirect_uri = 'https://www.example.com/oauth2callback'
            # flow.redirect_uri = 'http://127.0.0.1:8000/'

        # Generate URL for request to Google's OAuth 2.0 server.
            
        # Use kwargs to set optional request parameters.
            # authorization_url, state = flow.authorization_url(
            # # Recommended, enable offline access so that you can refresh an access token without
            # # re-prompting the user for permission. Recommended for web server apps.
            # access_type='offline',
            # # Optional, enable incremental authorization. Recommended as a best practice.
            # include_granted_scopes='true',
            # # Recommended, state value can increase your assurance that an incoming connection is the result
            # # of an authentication request.
            # state=24,
            # # Optional, if your application knows which user is trying to authenticate, it can use this
            # # parameter to provide a hint to the Google Authentication Server.
            # # login_hint='hint@example.com',
            # # Optional, set prompt to 'consent' will prompt the user for consent
            # prompt='consent')

            # flow.redirect_uri(authorization_url)
            creds = flow.run_local_server(port=0)
            # creds = redirect(authorization_url)
            # creds = flow.run_console()
                    
            # print("this is the url requeired -----> ",authorization_url)
            # print("creds-accesses--------->",creds)

        # Save the access token in token.pickle file for the next run
        with open(f'tokens/{request.user}.pickle', 'wb') as token:
                pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    print('service-------------->', service)

    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt.get('payload')
            if not payload:
                continue

            headers = payload.get('headers')
            if not headers:
                continue

            # Look for Subject and Sender Email in the headers
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
            sender = next((d['value'] for d in headers if d['name'] == 'From'), None)

            # The Body of the message is in Encrypted format. So, we have to decode it.
            parts = payload.get('parts')
            if parts:
                body_text, body_html = extract_message_body(parts)

                count += 1
                print(count)
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
        
    return data_obj



            

