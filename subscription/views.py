from django.shortcuts import render, redirect
from .models import Plan, PlanType
from decouple import config
import stripe
stripe.api_key = config('STRIPE_API_KEY')

# Create your views here.
def billingView(request):
    if request.user.is_authenticated:
        plans = Plan.objects.all()
        plan_types = []
        prices =[]
        video_qualities = []
        resolutions = []
        devices = []
        for plan in plans:
            plan_types.append(str(plan.plan_type))
            prices.append(plan.monthly_price)
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
        }
        return render(request, 'subscription/billing.html', context=context)
    return redirect("login")

def paymentPage(request, planType):
    if request.user.is_authenticated:
        selected_plan = PlanType.objects.get(name=planType)
        plan = Plan.objects.get(plan_type=selected_plan)
        intent = stripe.PaymentIntent.create(
            amount=plan.monthly_price*100,
            currency='inr',
            metadata={'integration_check': 'accept_a_payment'},
        )
        context = {
            'client_secret': intent.client_secret,
            'amount': plan.monthly_price*100,
        }
        return render(request, 'subscription/paymentPage.html', context=context)
    return redirect('login')


def subscriptionPage(request):
    if request.user.is_authenticated:
        if request.user.usersubscription:
            context = {
                'subscription': request.user.usersubscription,
            }
            return render(request, 'subscription/viewPlan.html', context=context)
        else:
            return redirect("billing")
    return redirect('login')