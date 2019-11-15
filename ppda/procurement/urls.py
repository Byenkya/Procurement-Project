from django.urls import path
from . import views
app_name = "procurement"
urlpatterns = [
    path('', views.index, name='index'),
    path('my_redirect/',views.my_redirect, name="my_redirect"),
    path('members/', views.members, name="members"),
    path('addMember/', views.addMember, name="addMember"),
    path('removeMember/', views.removeMember, name="removeMember"),
    path('requisition/', views.new_requisition, name="new_requisition"),
    path('user_department', views.user_department, name="user_department"),
    path('pdu', views.pdu, name="pdu"),
    path('accounting_officer', views.accounting_officer, name="accounting_officer")
]