"""Payment_Gateway_Integration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from PaymentGatewayIntegration import views

urlpatterns = [
    path('PaymentGatewayIntegration/', include('PaymentGatewayIntegration.urls')),
    path('admin/', admin.site.urls),
    path('on_form_submit',views.onformsubmit),
    path('', views.index, name='index'),
    path('create-paypal-transaction',views.createpaypalorder),
    path('capture-paypal-transaction',views.capturepaypalorder),
    path('get-paypal-transaction',views.getpaypaltransactiondetails),
    path('success-page',views.getsuccesspage),
    path('failure-page',views.getfailurepage)
]
