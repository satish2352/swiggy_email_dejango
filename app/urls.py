from django.contrib import admin
from django.urls import path
from .views import successfully_scrap
from app import views
from django.contrib.auth import views as auth_views
from .forms import (LoginForm,MyPasswordChangeForm,MyPasswordResetForm, MySetPasswordForm)


urlpatterns = [
    path('scrapdata/',successfully_scrap,name='scrapdata'),
    # path('getscrap/', scrap_swiggy_data,name=''),
    # path('chart1/',get_chart,name='chart1'),
    # path('chart2/',chart_data2,name='chart2'),
    path('',views.home,name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),

    path('ReadytoScrap/',views.readytoscrap,name='readytoscrap'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),



    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html')),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
]


urlpatterns+=[
    path('dashboard/',views.dashboard,name='dashboard'),
   path('dashboard/charts',views.charts,name='charts'),
  
]