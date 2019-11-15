from django.shortcuts import render, redirect
from .models import HeadOfDepartment, User, UserDepartment, Member
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def my_redirect(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)

        try:
            if request.user.profile.hod:
                return redirect('index')
        except:
            try:
                if request.user.profile.member:
                    return redirect('procurement:user_department')
            except:
                try:
                    if request.user.profile.office_member_id:
                        office = request.user.profile.office_member_id.office_id.name
                        if office == "AO":
                            return redirect('procurement:accounting_officer')
                        else:
                            return redirect('procurement:pdu')
                except:
                    return redirect("index")
@login_required
def index(request):
    return render(request, "procurement/HOD-base.html")

@login_required
def user_department(request):
    return render(request, "procurement/user-department-page.html")

@login_required
def pdu(request):
    return render(request, "procurement/pdu-page.html")

@login_required
def accounting_officer(request):
    return render(request, "procurement/accounting-officer-page.html")

@login_required
def new_requisition(request):
    return render(request, "procurement/requisition-form-1.html")

@login_required
def members(request):
    members = Member.objects.all()
    user_departments = UserDepartment.objects.all()
    context = {
        'members':members,
        'user_departments':user_departments
    }
    return render(request, "procurement/members-table.html", context)

@login_required
def addMember(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        first_name = post_data['first_name']
        last_name = post_data['last_name']
        username = post_data["username"]
        email = post_data['email']
        telephone = post_data['number']
        signature = post_data['file']
        department = UserDepartment.objects.get(department_name=post_data['department'])
        member = Member(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            telephone=telephone,
            signature=signature,
            user_department_id=department
        )
        member.save()

        user = User.objects.create_user(
            username=username,
            email=email,
            password="123"
        )

        user.first_name = first_name
        user.last_name = last_name
        user.profile.member = member
        user.save()
        members = Member.objects.all()
        user_departments = UserDepartment.objects.all()
        context = {
            'members':members,
            'user_departments':user_departments
        }
        return render(request, "procurement/members-table.html",context)
        
@login_required
def removeMember(request):
    if request.method == "GET":
        member_id = request.GET['id']
        member = Member.objects.get(id=member_id)
        User.objects.filter(username=member.username).delete()
        member.delete()
        members = Member.objects.all()
        user_departments = UserDepartment.objects.all()
        context = {
            'members':members,
            'user_departments':user_departments
        }
        return render(request, "procurement/members-table.html",context)
