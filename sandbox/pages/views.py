from django.shortcuts import render

# Create your views here.

def impressumview(request):
    return render(request,'pages/impressum.html')

def gobdview(request):
    return render(request,'pages/gobd.html')

def revisionssicherheitview(request):
    return render(request,'pages/revisionssicherheit.html')
