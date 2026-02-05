from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transactions_view, name='transactions'),
]
