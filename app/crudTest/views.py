from django.shortcuts import render
from crudTest.utils import fetch_all


def mainView(request):
    products = fetch_all()
    return render(request, 'index.html', context={'products': products})