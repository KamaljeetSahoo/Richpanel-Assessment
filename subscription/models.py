from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlanType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class VideoQuality(models.Model):
    quality = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.quality

class Resolution(models.Model):
    resolution = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.resolution

class Device(models.Model):
    device_type = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.device_type

class Plan(models.Model):
    plan_type = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    monthly_price = models.IntegerField()
    yearly_price = models.IntegerField()
    video_quality = models.ForeignKey(VideoQuality, on_delete=models.CASCADE)
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Device)

    def __str__(self) -> str:
        return str(self.plan_type)+'_'+str(self.video_quality)
    
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)
    cancelled = models.BooleanField(default=False)
    subscription_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)