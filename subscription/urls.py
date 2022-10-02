from django.urls import path
from .views import billingView, paymentPage, subscriptionPage, successPayment

urlpatterns = [
    path('', billingView, name="billing"),
    path('yearly/',billingView),
    path('paymentPage/<str:planType>/<str:monthly>/',paymentPage),
    path('viewCurrentPlan/', subscriptionPage, name="currentPlan"),
    path('successPay/<str:monthly>/<str:planType>/', successPayment),
]
