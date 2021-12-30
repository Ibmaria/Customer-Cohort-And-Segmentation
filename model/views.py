from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd 
# Create your views here.


@login_required(login_url='login')
def home(request):
	return render(request,'model/index.html')

