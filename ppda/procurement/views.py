from django.shortcuts import render, redirect
from .models import (
    HeadOfDepartment,
    User,
    UserDepartment,
    Member,
    Requisition,
    Details
    )
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import json

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
    """
        Function returns all the members in a particular user department.
    """
    members = Member.objects.all()
    user_departments = UserDepartment.objects.all()
    context = {
        'members':members,
        'user_departments':user_departments
    }
    return render(request, "procurement/members-table.html", context)


@login_required
def part1_requisition(request):
    """
        Route responsible for storing the first information of the requisition form.
        After renders a template with the next part of the requisition form.

    """
    if request.method == "POST":
        code_of_pde = request.POST['code_of_pde']
        financial_year = request.POST['financial_year']
        sequence_number = request.POST['reference_number']
        works = request.POST['procurement-type']
        subject_of_procurement = request.POST['subject']
        plan_reference = request.POST['plan_reference']
        location = request.POST['location']
        date_required = request.POST['date_required']
        requisition = Requisition(
            reference_number = sequence_number,
            financial_year = financial_year,
            pde_code = code_of_pde,
            sequence_number = sequence_number,
            requisition_type = works,
            subject = subject_of_procurement,
            plan_reference = plan_reference,
            delivery_location = location,
            date_required = date_required
        )
        requisition.save()
        context = {
            "requisition": requisition
        }
        return render(request,"procurement/requisition-page-part2.html",context) 
    else:
        return render(request,"procurement/requisition-form-1.html")

@login_required
def part2_requisition(request):
    """
        This route function handles the second part of the requisition form i.e Details section.
        Once done it redirects the current user to the last section of the requisition form.
    """
    if request.method == "POST":
        pass
    else:
        return render(request,"procurement/requisition-page-part2.html")

@login_required
def back_to_requisition_part1(request):
    """
        This routing function takes you back to the first part(i.e section) of the requisition form.
        With the details of that initiated requisition.
    """
    if request.method == "GET":
        part1_details = request.GET['partial_info'].split(" ")
        if part1_details != ['']: # checks if the part1_details list is empty i.e ['']
            context = {
                "code_of_pde": part1_details[2],
                "financial_year":part1_details[1],
                "sequence_number":part1_details[3],
                "works":part1_details[4],
                "subject_of_procurement":part1_details[5],
                "reference":part1_details[6],
                "location":part1_details[7],
                "date_required":part1_details[8]  
            }
            return render(request, "procurement/requisition-form-1.html", context)
        else:
            return render(request, "procurement/requisition-form-1.html")

    elif request.method == "POST":
        code_of_pde = request.POST['code_of_pde']
        financial_year = request.POST['financial_year']
        sequence_number = request.POST['reference_number']
        works = request.POST['procurement-type']
        subject_of_procurement = request.POST['subject']
        plan_reference = request.POST['plan_reference']
        location = request.POST['location']
        date_required = request.POST['date_required']

        requisition = Requisition.objects.get(sequence_number=sequence_number)
        requisition.financial_year = financial_year
        requisition.pde_code = code_of_pde
        requisition.requisition_type = works
        requisition.subject = subject_of_procurement
        requisition.plan_reference = plan_reference
        requisition.delivery_location = location
        requisition.date_required = date_required
        requisition.save()

        context = {
            "requisition": requisition
        }
        return render(request,"procurement/requisition-page-part2.html",context) 

    else:
         return render(request,"procurement/requisition-page-part2.html")


@login_required
def ajax_filter(request):
    """
    This routing function commits all the neccessary details of a particular 
    requisition basing on the sequence number of the requisition.
    """
    if request.is_ajax():
        requisition_sequence_number = request.POST["seq_num"]
        requisition_details = json.loads(request.POST["details"])
        requisition = Requisition.objects.get(sequence_number=requisition_sequence_number)
        for detail in requisition_details:
            details = Details(
                item_name = detail["item_name"],
                description = detail["description"],
                quantity = detail["quantity"],
                unit_of_measure = detail["unit_of_measure"],
                estimated_cost = detail["estimated_cost"],
                currency = detail["currency"],
                market_price = detail["market_price"],
                requisition_id = requisition
            )
            details.save()
        return JsonResponse({
            "success": True,
            "sequence_number": requisition_sequence_number,
            "requisition_details": requisition_details,
            "url": reverse('procurement:part3_requisition'),
        })
    return JsonResponse({ "success": False })

@login_required
def part3_requisition(request):
    """
        This routing function handles the third i.e (last section) of the requisition form.
    """         
    if request.method == "POST":
        print(">>>>>>>>>>>>>>>>>>>>>>>")
        return render(request, "procurement/t.html")
    elif request.method == "GET":
        print("XXXXXXXXXXXXXXXXXXXX")
        return render(request, "procurement/requisition-page-part3.html")
    else:
        return render(request, "procurement/requisition-page-part3.html")

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
