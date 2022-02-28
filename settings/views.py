from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from oauth.services import UserProfileService


def home(request):
    """serve 200 at /"""
    return HttpResponse(
        "Hey there! Just another strukturen backend.", content_type="text/plain"
    )


@login_required
def account(request):
    """renders a basic user account view"""
    return TemplateResponse(request, "account.html", {"user": request.user})
