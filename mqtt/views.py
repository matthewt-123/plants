from django.shortcuts import render
from django.http.response import JsonResponse, Http404
from .helper import run, publish
import threading
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

#THOUGHTS: limit to smvdriver user to prevent accidental location interference
def index(request):
    return render(request, 'mqtt/dashboard.html')

def myurl(request):
    return render(request, 'mqtt/myurl.html', {
        "name": "matthew",
        "day": "today"
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dash_admin"), status=302)
        else:
            return render(request, "mqtt/dashboard_admin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        raise Http404
    
#threading: starts and maintains MQTT subscription in the background, using run(topics) function from helper
thread = threading.Thread(target=run, name="MQTT_Subscribe", daemon=True)
thread.start()
