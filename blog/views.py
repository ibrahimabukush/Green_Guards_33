from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')



def municipality(request):
    return render(request, 'blog/municipality.html')



