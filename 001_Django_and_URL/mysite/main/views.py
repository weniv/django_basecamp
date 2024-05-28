from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "main/index.html")


def a(request):
    return render(request, "main/a.html")


def b(request):
    return render(request, "main/b.html")
