from django.urls import path
from myUsers import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('setpassword', views.set_password),
    path('getuserinfo', views.get_user_info),
]