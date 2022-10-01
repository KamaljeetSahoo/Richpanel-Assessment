from django.shortcuts import render, redirect
from .models import Plan

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