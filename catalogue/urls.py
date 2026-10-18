from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('calculator/', views.budget_calculator, name='budget_calculator'),
    path('package/<str:package_type>/<int:pk>/', views.package_detail, name='package_detail'),
    path('quote/', views.request_quote, name='request_quote'),
]
