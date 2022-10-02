from django.urls import path
from .views import billingView, paymentPage

urlpatterns = [
    path('', billingView, name="billing"),
    path('paymentPage/<str:planType>/',paymentPage),
]
