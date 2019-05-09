from django.urls import path
from myBlog import views

urlpatterns = [
    path('', views.index),
]