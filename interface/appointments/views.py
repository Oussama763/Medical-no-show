from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def index_next(request):
    return HttpResponse("<h1>this is the next page</h1>")