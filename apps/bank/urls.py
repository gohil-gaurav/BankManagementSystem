from django.urls import path
from . import views, manager_views

app_name = 'bank'

urlpatterns = [
    # User routes
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('transaction/<int:transaction_id>/download/', views.download_transaction_pdf, name='download_transaction_pdf'),
    
    # Manager authentication
    path('manager/login/', manager_views.manager_login_view, name='manager_login'),
    path('manager/register/', manager_views.manager_register_view, name='manager_register'),
    path('manager/logout/', manager_views.manager_logout_view, name='manager_logout'),
    
    # Manager dashboard
    path('manager/dashboard/', manager_views.manager_dashboard_view, name='manager_dashboard'),
    
    # User supervision
    path('manager/users/', manager_views.manager_users_view, name='manager_users'),
    path('manager/user/<int:user_id>/', manager_views.manager_user_detail_view, name='manager_user_detail'),
    
    # Account monitoring
    path('manager/accounts/', manager_views.manager_accounts_view, name='manager_accounts'),
    path('manager/account/<int:account_id>/', manager_views.manager_account_detail_view, name='manager_account_detail'),
    path('manager/account/<int:account_id>/freeze/', manager_views.manager_freeze_account_view, name='manager_freeze_account'),
    path('manager/account/<int:account_id>/unfreeze/', manager_views.manager_unfreeze_account_view, name='manager_unfreeze_account'),
    
    # Transaction monitoring
    path('manager/transactions/', manager_views.manager_transactions_view, name='manager_transactions'),
    path('manager/approvals/', manager_views.manager_pending_approvals_view, name='manager_pending_approvals'),
    path('manager/transaction/<int:transaction_id>/approve/', manager_views.manager_approve_transaction_view, name='manager_approve_transaction'),
    path('manager/transaction/<int:transaction_id>/reject/', manager_views.manager_reject_transaction_view, name='manager_reject_transaction'),
    
    # Reports
    path('manager/reports/', manager_views.manager_reports_view, name='manager_reports'),
]
