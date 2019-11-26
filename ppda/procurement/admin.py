from django.contrib import admin
from .models import (
    UserDepartment,
    HeadOfDepartment,
    Member,
    Office,
    OfficeMember,
    Profile,
    ProcurementStage,
    Requisition,
    Details,
    AvailabilityOfFunds
)

admin.site.register(UserDepartment)
admin.site.register(HeadOfDepartment)
admin.site.register(Member)
admin.site.register(Office)
admin.site.register(OfficeMember)
admin.site.register(Profile)
admin.site.register(ProcurementStage)
admin.site.register(Requisition)
admin.site.register(Details)
admin.site.register(AvailabilityOfFunds)
