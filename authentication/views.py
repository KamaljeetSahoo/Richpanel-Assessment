from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from subscription.models import UserSubscription

# Create your views here.
def registerView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            errors = []
            if User.objects.filter(username=username):
                errors.append("Username already exists")
            if User.objects.filter(email=email):
                errors.append("Email already exists")
            try:
                validate_password(password)
            except ValidationError as e:
                errors += e
            if errors:
                context = {
                    'errors': errors,
                }
                return render(request, 'authentication/register.html', context=context)
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                subscription_profile = UserSubscription(user=new_user)
                subscription_profile.save()
                return redirect("login")
        else:
            return render(request, 'authentication/register.html')
    else:
        return redirect("billing")

def loginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = None
            if User.objects.filter(email=email):
                user = authenticate(request, username=User.objects.get(email=email).username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("billing")
                else:
                    context = {
                        'errors': 'Invalid Credentials',
                    }
                    return render(request, 'authentication/login.html', context=context)
            else:
                context = {
                    'errors': 'Invalid Credentials',
                }
                return render(request, 'authentication/login.html', context=context)
        else:
            return render(request, 'authentication/login.html')
    else:
        return redirect("billing")