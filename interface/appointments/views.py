from django.shortcuts import render
from django.http import HttpResponse

def index():
    #print("do I appear?")
    return HttpResponse("<h1>This one does definetly appear</h1>")