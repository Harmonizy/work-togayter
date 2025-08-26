from django.shortcuts import render

def index(request):
    return render(request, 'Dashboard/home-index.html')
