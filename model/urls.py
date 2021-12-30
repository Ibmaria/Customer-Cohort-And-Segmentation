from django.urls import path
from . import views
import os
from model.dashapps import app1,app2,app3
urlpatterns=[

path('', views.home, name='home'),

]