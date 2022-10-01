import os, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'richpanel.settings')

import django
django.setup()
print("Dajngo module initiated")

from subscription.models import Plan, PlanType, Resolution, Device, VideoQuality, UserSubscription
from django.contrib.auth.models import User
UserSubscription(user=User.objects.get(username='admin')).save()
print("Initiated Blank Subscription model for admin user")

device_types = ['Phone', 'Tablet', 'Computer', 'TV']
for device in device_types:
    obj = Device(device_type = device)
    obj.save()
    print("Adding Device Type: ", device)

resolutions = ['480p', '1080p', '4K+HDR']
for res in resolutions:
    obj = Resolution(resolution = res)
    obj.save()
    print("Adding Resolution Type: ", res)

qualities = ['Good', 'Better', 'Best']
for quality in qualities:
    obj = VideoQuality(quality=quality)
    obj.save()
    print("Adding Quality Type: ", quality)

plan_types = ['Mobile', 'Basic', 'Standard', 'Premium']
for t in plan_types:
    obj = PlanType(name=t)
    obj.save()
    print("Adding Plan Type: ", t)

plans = [
    ['Mobile', 100, 1000, 'Good', '480p', ['Phone', 'Tablet']],
    ['Basic', 200, 2000, 'Good', '480p', ['Phone', 'Tablet', 'Computer', 'TV']],
    ['Standard', 500, 5000, 'Better', '1080p', ['Phone', 'Tablet', 'Computer', 'TV']],
    ['Premium', 700, 7000, 'Best', '4K+HDR', ['Phone', 'Tablet', 'Computer', 'TV']],
]

for plan in plans:
    plan_type=PlanType.objects.get(name=plan[0])
    video_quality = VideoQuality.objects.get(quality=plan[3])
    resolution = Resolution.objects.get(resolution=plan[4])
    obj = Plan(plan_type=plan_type, monthly_price=plan[1], yearly_price=plan[2], video_quality=video_quality, resolution=resolution)
    obj.save()
    for device in plan[5]:
        obj.devices.add(Device.objects.get(device_type=device))
        obj.save()
    print("Adding Plans: ", plan)

print("Database Populated")