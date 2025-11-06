from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"init.html")

def about_view(request):
    return render(request,"about.html")