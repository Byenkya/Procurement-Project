from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class HeadOfDepartment(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    signature = models.ImageField(upload_to='images/', null=True, verbose_name="")
    def __str__(self):
        return " ".join([self.first_name,self.last_name,self.email,self.telephone])

class UserDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    hod = models.OneToOneField(
        HeadOfDepartment,
        on_delete=models.CASCADE,
        primary_key=False
    )
    
    def __str__(self):
        return self.department_name 

class Member(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    username = models.CharField(max_length=15, default="", unique=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    signature = models.ImageField(upload_to='images/', null=True, verbose_name="")
    user_department_id = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.first_name,self.last_name])

class Office(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def  __str__(self):
        return self.name

class OfficeMember(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    signature = models.ImageField(upload_to='images/', null=True, verbose_name="")
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.first_name,self.last_name,str(self.email),self.telephone])
 
class Profile(models.Model):
    user = models.OneToOneField(User,unique=False,on_delete=models.CASCADE)
    hod = models.ForeignKey(HeadOfDepartment, blank=True, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey(Member, blank=True, on_delete=models.CASCADE,null=True)
    office_member_id = models.ForeignKey(OfficeMember,blank=True, on_delete=models.CASCADE,null=True) 

    def __str__(self):
        return str(self.user)
        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class ProcurementStage(models.Model):
    id = models.AutoField(primary_key=True)
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    description = models.CharField(max_length=200)

    def __str__(self):
        return " ".join([self.stage_name,self.state,self.description])

class Requisition(models.Model):
    id = models.AutoField(primary_key=True)
    reference_number = models.CharField(max_length=15)
    financial_year = models.CharField(max_length=4)
    pde_code = models.CharField(max_length=10)
    sequence_number = models.CharField(max_length=10,unique=True)
    requisition_type = models.CharField(max_length=10)
    subject = models.CharField(max_length=10)
    plan_reference = models.CharField(max_length=10)
    delivery_location = models.CharField(max_length=10)
    date_required = models.DateField()
    initiation = models.DateField(blank=True,null=True)
    member_confirmation = models.BooleanField(blank=True,null=True)
    hod_confirmation = models.BooleanField(blank=True,null=True)
    member_confirmation_date = models.DateField(blank=True,null=True)
    hod_confirmation_date = models.DateField(blank=True,null=True)
    date_of_submission = models.DateField(blank=True,null=True)
    user_department_id = models.ForeignKey(UserDepartment,blank=True,null=True,on_delete=models.CASCADE)
    initiator = models.ForeignKey(Member,blank=True,null=True,on_delete=models.CASCADE)
    procurement_stage = models.ForeignKey(ProcurementStage,blank=True,null=True,on_delete=models.CASCADE)

    def  __str__(self):
        return " ".join([
                self.reference_number,
                self.financial_year,
                self.pde_code,
                self.sequence_number,
                self.requisition_type,
                self.subject,
                self.plan_reference,
                self.delivery_location,
                str(self.date_required),
                str(self.initiation),
                str(self.member_confirmation),
                str(self.hod_confirmation),
                str(self.member_confirmation_date),
                str(self.hod_confirmation_date),
                str(self.date_of_submission)
                ])

class Details(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_of_measure = models.IntegerField()
    estimated_cost = models.IntegerField()
    currency = models.CharField(max_length=10)
    market_price = models.IntegerField()
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE)

    def  __str__(self):
        return " ".join([
                self.item_name,
                self.description,
                str(self.quantity),
                str(self.unit_of_measure),
                str(self.estimated_cost),
                self.currency,
                str(self.market_price)])
        