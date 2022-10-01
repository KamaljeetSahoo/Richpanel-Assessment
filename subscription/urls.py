from django.urls import path
from .views import billingView

urlpatterns = [
    path('', billingView, name="billing"),
]
