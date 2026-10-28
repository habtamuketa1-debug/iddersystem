from django.urls import path
from .views import custom_login_view, iddir_dashboard, financial_report_view, member_portal_view

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('', iddir_dashboard, name='dashboard'),
    path('financial-report/', financial_report_view, name='financial_report'),
    path('audit-report/', financial_report_view, name='audit_report'),  # <--- ይህንን መስመር ይጨምሩ
    path('portal/', member_portal_view, name='member_portal'),
]