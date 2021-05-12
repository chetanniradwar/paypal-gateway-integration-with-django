from django.urls import path
from . import views
urlpatterns =[path('PaymentGatewayIntegration', views.index ,name='index'),
]