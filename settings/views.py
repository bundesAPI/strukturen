from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    """serve 200 at /"""
    return HttpResponse(
        "Hey there! Just another strukturen backend.", content_type="text/plain"
    )
