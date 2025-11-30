from django.urls import path
from . import views

urlpatterns = [
    path('flow/', views.flow_endpoint, name='flow_endpoint'),
    path('health/', views.health_check, name='health_check'),
]
