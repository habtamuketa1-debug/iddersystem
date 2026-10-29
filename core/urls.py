from django.urls import path
from .views import (
    custom_login_view, 
    iddir_dashboard, 
    financial_report_view, 
    member_portal_view,
    add_member_view  # አዲሱን ቪው ማካተት
)

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('', iddir_dashboard, name='dashboard'),
    path('financial-report/', financial_report_view, name='financial_report'),
    path('audit-report/', financial_report_view, name='audit_report'),
    path('portal/', member_portal_view, name='member_portal'),
    path('add-member/', add_member_view, name='add_member'),
]