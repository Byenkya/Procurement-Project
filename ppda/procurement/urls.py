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
    path('part1_requisition', views.part1_requisition, name="part1_requisition"),
    path('back_to_requisition_part1/<int:id>', views.back_to_requisition_part1, name="back_to_requisition_part1"),
    path('add_requisition_detail/<int:id>',views.add_requisition_detail , name="add_requisition_detail"),
    path('delete_details/<int:id>', views.delete_details, name="delete_details"),
    path('ajax_filter', views.ajax_filter, name="ajax_filter"),
    path('view_requisitions', views.view_requisitions, name="view_requisitions"),
    path('hod_confirmation', views.hod_confirmation, name="hod_confirmation"),
    path('confirm_availability_funds', views.confirm_availability_funds, name="confirm_availability_funds"),
    path('requisition_more_details/<int:id>/<int:count>', views.requisition_more_details, name='requisition_more_details'),
    path('reject_requisition', views.reject_requisition, name="reject_requisition"),
    path('confirm_requisition/<int:id>',views.confirm_requisition, name="confirm_requisition"),
    path('pdu', views.pdu, name="pdu")
] 