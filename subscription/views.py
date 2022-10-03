from django.shortcuts import render, redirect
from .models import Plan, PlanType
from decouple import config
import stripe
from .utils import process_date
from datetime import datetime, timedelta
stripe.api_key = config('STRIPE_API_KEY')

# Create your views here.
def billingView(request):
    if request.user.is_authenticated:
        url = request.get_full_path()
        plans = Plan.objects.all()
        plan_types = []
        prices =[]
        yearlyPrices = []
        video_qualities = []
        resolutions = []
        devices = []
        for plan in plans:
            plan_types.append(str(plan.plan_type))
            prices.append(plan.monthly_price)
            yearlyPrices.append(plan.yearly_price)
            video_qualities.append(str(plan.video_quality))
            resolutions.append(str(plan.resolution))
            d = []
            for device in plan.devices.all():
                d.append(str(device))
            devices.append(d)
        
        context = {
            'plan_types': plan_types,
            'prices': prices,
            'video_qualities': video_qualities,
            'resolutions': resolutions,
            'devices': devices,
            'yearlyPrices': yearlyPrices,
        }
        if str(url) == "/yearly/":
            return render(request, 'subscription/billingYearly.html', context=context)
        return render(request, 'subscription/billing.html', context=context)
    return redirect("login")

def paymentPage(request, planType, monthly):
    if request.user.is_authenticated:
        selected_plan = PlanType.objects.get(name=planType)
        plan = Plan.objects.get(plan_type=selected_plan)
        if monthly == 'monthly':
            amount = plan.monthly_price*100
        else:
            amount = plan.yearly_price*100
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            metadata={'integration_check': 'accept_a_payment'},
        )
        context = {
            'client_secret': intent.client_secret,
            'amount': amount,
            'price': amount//100,
            'planType': planType,
            'monthly': monthly,
        }
        return render(request, 'subscription/paymentPage.html', context=context)
    return redirect('login')

def successPayment(request, monthly, planType):
    if request.user.is_authenticated:
        print(monthly, planType)
        selected_plan = PlanType.objects.get(name=planType)
        plan = Plan.objects.get(plan_type=selected_plan)
        if monthly == "monthly":
            sub = request.user.usersubscription
            sub.subscribed = True
            sub.plan = plan
            sub.cancelled = False
            sub.subscription_date = datetime.now()
            sub.expiration_date = datetime.now() + timedelta(30)
            sub.save()
        if monthly == "yearly":
            sub = request.user.usersubscription
            sub.subscribed = True
            sub.plan = plan
            sub.cancelled = False
            sub.subscription_date = datetime.now()
            sub.expiration_date = datetime.now() + timedelta(365)
            sub.save()
        return redirect("currentPlan")
    return redirect("login")


def subscriptionPage(request):
    if request.user.is_authenticated:
        if request.user.usersubscription.subscribed:
            time = request.user.usersubscription.expiration_date - request.user.usersubscription.subscription_date
            print(time)
            if str(time) == "30 days, 0:00:00":
                monthly = 'monthly'
            else:
                monthly = 'yearly'
            sub_date = process_date(request.user.usersubscription.subscription_date)
            exp_date = process_date(request.user.usersubscription.expiration_date)
        
            context = {
                "sub_date":sub_date,
                "exp_date":exp_date,
                'subscription': request.user.usersubscription,
                'time' : time,
                'monthly': monthly,                
            }
            return render(request, 'subscription/viewPlan.html', context=context)
        else:
            return redirect("billing")
    return redirect('login')

def cancelSubscription(request):
    if request.user.is_authenticated:
        sub = request.user.usersubscription
        sub.cancelled = True
        sub.save()
        return redirect("currentPlan")
    return redirect("login")