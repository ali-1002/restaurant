from django.shortcuts import render
from django.http import HttpResponse

def dd(request):
    return HttpResponse('Hello')