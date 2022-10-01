from django.shortcuts import render

# Create your views here.
def registerView(request):
    return render(request, 'authentication/register.html')

def loginView(request):
    return render(request, 'authentication/login.html')