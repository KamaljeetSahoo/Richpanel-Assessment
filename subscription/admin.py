from django.contrib import admin
from .models import  PlanType, VideoQuality, Resolution, Device, Plan

# Register your models here.
admin.site.register(PlanType)
admin.site.register(VideoQuality)
admin.site.register(Resolution)
admin.site.register(Device)
admin.site.register(Plan)