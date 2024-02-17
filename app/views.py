from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.urls import reverse
from .scrap import getEmails
from django.http import HttpResponse
from .models import Restaurant, Customer, Order, Item, Payment
from datetime import datetime
from django.db.models import Count, Sum, Avg
from django.contrib import messages
from .charts_functions import orders_by_status,quantity_by_item, orders_over_time,get_past_7_days_data,order_summary,get_past_30_days_data,top_5_restaurant_data,top_5_Items
from .forms import (CustomerRegistrationForm)
from django.utils import timezone
from django.db import IntegrityError
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

login_required
def dashboard(request):
    if not request.user.is_authenticated :
       messages.warning(request,'Login to access the scraping functionality')
       return redirect('login')
    enddate_inclusive = None
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    get_week_bool = request.GET.get('lastweek')
    get_month_bool = request.GET.get("last30days")
    print("EEEnd DDAtee ===>",enddate)
    
    if startdate and enddate:
        enddate_inclusive = datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1)
        print('enddate_inclusive',enddate_inclusive)
    elif get_week_bool == 'true':
       enddate_inclusive, startdate = get_past_7_days_data()
       startdate = str(startdate)
       enddate = str(enddate_inclusive - timedelta(days=1))
       print(f"get_week_bool--> enddate__{enddate}")
    elif get_month_bool == 'true':
       enddate_inclusive, startdate = get_past_30_days_data()
       startdate = str(startdate)
       enddate = str(enddate_inclusive - timedelta(days=1))
       
    try:
        chart_data = {
            'chart_1': {'orders_by_status_data': orders_by_status(request,startdate,enddate_inclusive)},
            'chart_2' : {'quantity_by_item_data':quantity_by_item(request,startdate,enddate_inclusive)},
            'chart_3' : {'orders_over_time':orders_over_time(request,startdate,enddate_inclusive)},
            'ordersummary': order_summary(request,startdate,enddate_inclusive),
            'top_res': top_5_restaurant_data(request,startdate,enddate),
            'top_item': top_5_Items(request,startdate,enddate_inclusive)
            }
            
        print('chart_data----->',chart_data)
    

        return render(request, 'bootstrap_templates/dashboard.html', {'chart_data': chart_data,'startdate': startdate,'enddate':enddate})
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)
        # return render(request, 'error.html', {'error_message': error_message})


login_required
def scrap_swiggy_data(request):

    return render(request,'app/scrap.html')


login_required
def successfully_scrap(request):
    received_data = getEmails(request)  # received_data contains the list with data
    # print(received_data)

    # for data in received_data:
    #     # Check if any field contains 'not found'
    #     if 'not found' in data['restaurant']['restaurant_name'].lower() or \
    #        'not found' in data['restaurant']['restaurant_address'].lower() or \
    #        'not found' in data['customer_info']['customer_name'].lower() or \
    #        'not found' in data['customer_info']['customer_address'].lower() or \
    #        'not found' in data['order_data']['Order No:'].lower() or \
    #        'not found' in data['order_data']['Order placed at:'].lower() or \
    #        'not found' in data['order_data']['Order delivered at:'].lower() or \
    #        'not found' in data['order_data']['Order Status'].lower() or \
    #        'not found' in str(data['order_summary']['Order Total']).lower():
    #         continue

    #     # Check if the Customer object exists, if not create a new one
    #     customer, created = Customer.objects.get_or_create(
    #         user = request.user,
    #         cname=data['customer_info']['customer_name'],
    #         caddress=data['customer_info']['customer_address']
    #     )
    #     print('customer created', created)
        
    #     # Create and save the Restaurant object
    #     restaurant, created = Restaurant.objects.get_or_create(
    #         rname=data['restaurant']['restaurant_name'],
    #         raddress=data['restaurant']['restaurant_address']
    #     )
    #     print('restaurant created',created)
    #     # Create and save the Order object
    #     order_placed_at = datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order placed at:'].lower() else None
    #     order_delivered_at = datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order delivered at:'].lower() else None


        
    #     try: 
    #         order , order_created = Order.objects.get_or_create(
    #         restaurant = restaurant,
    #         order_number=data['order_data']['Order No:'],
    #         order_placed_at=order_placed_at,
    #         order_delivered_at=order_delivered_at,
    #         order_status=data['order_data']['Order Status'],
    #         customer=customer,
    #         order_total=data['order_summary']['Order Total']
    #     )
    #         if not order_created:
    #            continue
            
    #         for item in data['item_details']:
    #             if 'not found' in item[0].lower() or 'not found' in str(item[1]).lower() or 'not found' in str(item[2]).lower():
    #                 continue
    #             items_added ,item_created= Item.objects.get_or_create(
    #                 order=order,
    #                 iname=item[0],
    #                 quantity=item[1],
    #                 price=item[2]
    #             )
    #         order_summary = data.get('order_summary', {})  # Get order_summary if exists, otherwise empty dictionary
    #         payment_data, payment_created = Payment.objects.get_or_create(
    #             order=order,
    #             payment_method='Unknown',  # Update this as per your data
    #             items_total=order_summary.get('Item Total', 0.0),
    #             packing_charges=order_summary.get('Order Packing Charges', 0.0),
    #             platform_fee=order_summary.get('Platform fee', 0.0),
    #             delivery_partner_fee=order_summary.get('Delivery partner fee', 0.0),
    #             discount_applied=order_summary.get('Discount Applied', 0.0),
    #             taxes=order_summary.get('Taxes', 0.0),
    #             order_total=order_summary.get('Order Total', 0.0)
    #         )
    #     except IntegrityError as e:
    #         print("errorr as ",e)
    #         continue

    return redirect(reverse('dashboard'))

login_required
def change_password(request):
 return render(request, 'app/changepassword.html')
    
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,'Congratulations! Registration Successfully')
   return redirect(reverse('login'))
  return render(request,'app/customerregistration.html',{'form':form})
 
login_required 
def readytoscrap(request):
    if request.user.is_authenticated:
        return render(request,'app/readytoscrap.html')
    else:
        messages.warning(request,'Login to access scrapping functionality')
        return redirect(reverse('login'))
    
def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    else:
        return render(request,'app/home.html')
    
@login_required
def charts(request):   
    
    enddate_inclusive = None
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')
    get_week_bool = request.GET.get('lastweek')
    get_month_bool = request.GET.get("last30days")
    # print("EEEnd DDAtee ===>",enddate)
    
    if startdate and enddate:
        enddate_inclusive = datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1)
        print('enddate_inclusive',enddate_inclusive)
    elif get_week_bool == 'true':
       enddate_inclusive, startdate = get_past_7_days_data()
       startdate = str(startdate)
       enddate = str(enddate_inclusive - timedelta(days=1))
       print(f"get_week_bool--> enddate__{enddate}")
    elif get_month_bool == 'true':
       enddate_inclusive, startdate = get_past_30_days_data()
       startdate = str(startdate)
       enddate = str(enddate_inclusive - timedelta(days=1))
       
    try:
        chart_data = {
            'chart_1': {'orders_by_status_data': orders_by_status(request,startdate,enddate_inclusive)},
            'chart_2' : {'quantity_by_item_data':quantity_by_item(request,startdate,enddate_inclusive)},
            'chart_3' : {'orders_over_time':orders_over_time(request,startdate,enddate_inclusive)},
            'ordersummary': order_summary(request,startdate,enddate_inclusive),
            'top_res': top_5_restaurant_data(request,startdate,enddate),
            'top_item': top_5_Items(request,startdate,enddate_inclusive)
            }
            
        print('chart_data----->',chart_data)
       
        return render(request, 'bootstrap_templates/charts.html', {'chart_data': chart_data,'startdate': startdate,'enddate':enddate})
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)
