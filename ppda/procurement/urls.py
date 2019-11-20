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
    path('part1_requisition', views.part1_requisition, name="part1_requisition"),
    path('back_to_requisition_part1/', views.back_to_requisition_part1, name="back_to_requisition_part1"),
    path('part2_requisition/', views.part2_requisition, name="part2_requisition"),
    path('part3_requisition/', views.part3_requisition, name="part3_requisition"),
    path('ajax_filter', views.ajax_filter, name="ajax_filter"),
    path('pdu', views.pdu, name="pdu"),
    path('accounting_officer', views.accounting_officer, name="accounting_officer")
]