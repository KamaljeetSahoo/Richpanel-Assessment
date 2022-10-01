from django.shortcuts import render, redirect

# Create your views here.
def billingView(request):
    if request.user.is_authenticated:
        return render(request, 'subscription/billing.html')
    return redirect("login")