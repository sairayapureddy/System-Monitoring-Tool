from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import psutil, os
import PIL.ImageGrab as im
from pymongo import MongoClient

# connect to db
databaseName = "SystemMonitoringDB"
connection = MongoClient()
db = connection[databaseName]


# function to calculate necessary monitoring details and saving them in user collection
def calc_utils_and_update_db(uname):
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory()[2]
    '''Disk Usage of current drive'''
    # disk_usage= psutil.disk_usage('.').percent
    ''' Disk Usage (used hard disk space %, Not read/write usage details) of all drives '''
    total = 0
    used = 0
    for i in psutil.disk_partitions():
        usage = psutil.disk_usage(i.mountpoint)
        total += usage.total
        used += usage.used
    disk_usage = "{0:.1f}".format(used/total * 100)
    img_bytes = im.grab().tobytes()
    db.get_collection(uname).insert({'username': uname, 'date': datetime.today(), 'time': datetime.now().strftime('%H:%M:%S'), "cpu_usage": cpu_usage, "memory_usage": mem_usage, "disk_usage":disk_usage, 'screenshot_bytes': img_bytes})
    return cpu_usage, mem_usage, disk_usage, img_bytes



# View function to handle login

def custom_login(request):
    uname = request.POST.get('username', None)
    pwd = request.POST.get('password', None)
    user = authenticate(username=uname, password=pwd)
    # print('logged user',user)
    if (user is not None) and user.is_authenticated:
        login(request, user)
        return redirect('app_details')
    else:
        print('redirecting to login page')
        return render(request, 'SystemMonitoringApp/login.html', {'error': True})

# View function to respond to polling
def poll(request):
    username = request.user.username
    cpu_usage, mem_usage, disk_usage, img_bytes = calc_utils_and_update_db(username)
    system_details = {"cpu_usage": cpu_usage, "memory_usage": mem_usage, "disk_usage":disk_usage, "time": datetime.now().strftime('%H:%M:%S')}
    return JsonResponse(system_details)


# View function to handle  Signup

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if username not in db.collection_names():
                db.create_collection(username)
            return redirect('app_details')
    else:
        form = UserCreationForm()
    return render(request, 'SystemMonitoringApp/signup.html', {'form': form})

# View function to display sytem monitoring details

@login_required
def details(request):
    username = request.user.username
    cpu_usage, mem_usage, disk_usage, img_bytes = calc_utils_and_update_db(username)
    system_details = {"cpu_usage": cpu_usage, "memory_usage": mem_usage, "disk_usage":disk_usage}
    return render(request, 'SystemMonitoringApp/details.html', {'system_details': system_details})
