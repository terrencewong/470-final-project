from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello Group 4: Here is the empty project site.")
