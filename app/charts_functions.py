from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum,F
from django.db.models.functions import TruncDay,TruncDate,TruncMonth,TruncWeek
from .models import Restaurant, Customer, Order, Item, Payment
from django.utils import timezone
from django.db.models import Sum, Avg
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncHour
from django.http import JsonResponse
from django.db.models import Q
def date_time_chart_data(request):
    day_data = Order.objects.annotate(date=TruncDate('order_placed_at')).values('date').annotate(count=Count('id')).order_by('date')

    # Count the orders for each week
    week_data = Order.objects.annotate(week=TruncWeek('order_placed_at')).values('week').annotate(count=Count('id')).order_by('week')

    # Count the orders for each month
    month_data = Order.objects.annotate(month=TruncMonth('order_placed_at')).values('month').annotate(count=Count('id')).order_by('month')

    # Convert the data to the required format
    formatted_day_data = [{'x': item['date'].isoformat(), 'y': item['count']} for item in day_data]
    formatted_week_data = [{'x': item['week'].isoformat(), 'y': item['count']} for item in week_data]
    formatted_month_data = [{'x': item['month'].isoformat(), 'y': item['count']} for item in month_data]

    return formatted_day_data, formatted_week_data, formatted_month_data

def orders_by_status(request, startdate, enddate):
    if startdate and enddate:
        orders_by_status = Order.objects.filter(customer__user=request.user, order_placed_at__range=(startdate, enddate)).values('order_status').annotate(count=Count('id'))
    else:
        orders_by_status = Order.objects.filter(customer__user=request.user).values('order_status').annotate(count=Count('id'))
    orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
    # print(orders_by_status_dict)
    return orders_by_status_dict 


def quantity_by_item(request, startdate, enddate):
    if startdate and enddate :
        orders = Order.objects.filter(customer__user=request.user, order_placed_at__range=(startdate, enddate))
    else:
        orders = Order.objects.filter(customer__user=request.user)
    quantity_by_item = Item.objects.filter(order__in=orders).values('iname').annotate(quantity=Sum('quantity'))
    quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}
    # print(quantity_by_item_dict)
    return quantity_by_item_dict


def orders_over_time(request, startdate, enddate):
    if startdate and enddate:
        data = Order.objects.filter(customer__user=request.user, order_placed_at__range=(startdate, enddate)).annotate(date=TruncDay('order_placed_at')).values('date').annotate(c=Count('id')).values('date', 'c')
    else:
        data = Order.objects.filter(customer__user=request.user).annotate(date=TruncDay('order_placed_at')).values('date').annotate(c=Count('id')).values('date', 'c')
    # print(data)
    return list(data)

def order_summary(request,startdate,enddate):
    if startdate and enddate:
        orders_query = Order.objects.filter(customer__user=request.user)
        total_orders = orders_query.filter(order_placed_at__range=(startdate,enddate)).count()
        total_amount = orders_query.filter(order_placed_at__range=(startdate,enddate)).aggregate(total_amount=Sum('order_total'))['total_amount'] or 0
        average_amount = orders_query.filter(order_placed_at__range=(startdate,enddate)).aggregate(average_amount=Avg('order_total'))['average_amount'] or 0
    else:
        orders_query = Order.objects.filter(customer__user=request.user)
        total_orders = orders_query.count()
        total_amount = orders_query.aggregate(total_amount=Sum('order_total'))['total_amount'] or 0
        average_amount = orders_query.aggregate(average_amount=Avg('order_total'))['average_amount'] or 0
    print(total_amount,total_orders,average_amount)
    return {'total_orders': total_orders,'total_amount':total_amount,'average_amount':average_amount}


def get_past_7_days_data():
    # Get today's date
    today = datetime.now().date() + timedelta(days=1)

    # Calculate the date 7 days ago
    past_7_days = today - timedelta(days=7)
    # print(f"past_7_days{past_7_days}")

    return today, past_7_days
def get_past_30_days_data():
    # Get today's date
    today = (datetime.now().date() + timedelta(days=1))
    past_30_days= (today - timedelta(days=30))
    return today, past_30_days

def top_5_restaurant_data(request,startdate,enddate):
    if startdate and enddate:
        order_query = Order.objects.filter(order_placed_at__range=(startdate, enddate), customer__user=request.user)
    else:
        order_query = Order.objects.filter(customer__user=request.user)
    
    res_data = (order_query.values('restaurant__rname')
            .annotate(total_orders=Count('restaurant__rname'),
                      total_amount=Sum('order_total'),
                      avg_amount=Avg('order_total'))
            .order_by('-total_orders')[:5])
    
    return list(res_data)

def top_5_Items(request,startdate,enddate):

    print("Top 5 enddate ===>",enddate)
    current_user = request.user
    if startdate and enddate:
        item_query = Item.objects.filter(order__order_placed_at__range=(startdate, enddate), order__customer__user=current_user)
    else:
        item_query = Item.objects.filter(order__customer__user = current_user)

    top_items = (item_query.values('iname')
        .annotate(total_orders=Count('iname'),
                    total_amount=Sum('price'),
                    avg_order_amount=Avg('price'))
        .order_by('-total_orders')[:5])
    return list(top_items)
    

# def order_hourly_count(request,):
#     user = request.user

# # Initialize an empty list to store the results for each time interval
#     hour_interval = []
#     order_count = []
#     # Assuming the user is authenticated, you can get the user from the request
#     for hour in range(24):
#     # Calculate the end hour for the current time interval
#         end_hour = (hour + 1) % 24  # Wraps around to 0 for the last interval (23-0)

#         # Create a filter for the current time interval
#         filter_condition = Q(
#             customer__user=user,
#             order_placed_at__hour__gte=hour,
#             order_placed_at__hour__lt=end_hour
#         )

#         # Get the count of orders for the current time interval
#         order_count.append(Order.objects.filter(filter_condition).count())
#         hour_interval.append(f'{hour:02d}-{end_hour:02d}')

#     # Print or use the results as needed
#     return {'hour_interval':hour_interval,'order_count':order_count}



def order_hourly_count(request,startdate,enddate):
    current_user = request.user
    
    
    # Initialize an empty list to store the results for each time interval
    hour_interval = []
    order_count = []

    for hour in range(24):
    # Calculate the end hour for the current time interval
        end_hour = (hour + 1) % 24  # Wraps around to 0 for the last interval (23-0)

        if startdate and enddate:
            order_count.append(Order.objects.filter(Q(
                order_placed_at__range=(startdate, enddate),customer__user=current_user,
                order_placed_at__hour__gte=hour,
                order_placed_at__hour__lt=end_hour
            )).count())
        else:
            order_count.append(Order.objects.filter(Q(
                customer__user=current_user,
                order_placed_at__hour__gte=hour,
                order_placed_at__hour__lt=end_hour
            )).count())

        hour_interval.append(f'{hour:02d}-{end_hour:02d}')
        
    print(hour_interval,order_count)
    # Print or use the results as needed
    return {'hour_interval':hour_interval,'order_count':order_count}




    






