from django.shortcuts import render, redirect
from .models import (
    HeadOfDepartment,
    User,
    UserDepartment,
    Member,
    Requisition,
    Details,
    Description,
    RequisitionStatus,
    AvailabilityOfFunds
    )
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import json
from datetime import datetime
from django.contrib import messages
import os

def pending(request,requisitions):
    if request.user.profile.role == "member" or request.user.profile.role == "hod":
        reqs = [
                req for req in requisitions if( 
                    request.user.profile.member.user_department_id.department_name == 
                    req.user_department_id.department_name ) and (
                        req.member_confirmation == False or 
                        req.hod_confirmation == False or
                        req.date_of_submission == None
                    )
            ]
        return len(reqs)
    else:
        reqs = [
            req for req in requisitions if(
                req.member_confirmation and 
                req.hod_confirmation and
                req.date_of_submission and
                req.accepted == False and 
                req.rejected == False
            )
        ]
        return len(reqs)

def my_redirect(request):
    """
        Function responsible for logging in users.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.warning(request, f"User {username} doesn't exist!")
            return redirect("login")

    else:
        return redirect("login")

@RequisitionStatus           
@login_required
def index(request,requisitions):
    if request.method == "GET":
        context = {
            "pending_count": pending(request,requisitions)
        }

        return render(request, "procurement/HOD-base.html", context)
    else:
        return render(request, "procurement/HOD-base.html")

@login_required
def pdu(request):
    return render(request, "procurement/pdu-page.html")

@RequisitionStatus
@login_required
def new_requisition(request, requisitions):
    context = {
        'pending_count': pending(request,requisitions)
    }
    return render(request, "procurement/requisition-form-1.html",context)

@RequisitionStatus
@login_required
def members(request, requisitions):
    """
        Function returns all the members in a particular user department.
    """
    members = Member.objects.all()
    user_departments = UserDepartment.objects.all()
    context = {
        'pending_count': pending(request,requisitions),
        'members':members,
        'user_departments':user_departments
    }
    return render(request, "procurement/members-table.html", context)

@RequisitionStatus
@login_required
def part1_requisition(request, requisitions):
    """
        Route responsible for storing the first information of the requisition form.
        After renders a template with the next part of the requisition form.

    """
    if request.method == "POST":
        # First get the initiator of the procurement from the member table.
        initiator = Member.objects.get(username=request.user.username)
        department = initiator.user_department_id

        if initiator:
            # Then store part of the requisition data.
            code_of_pde = request.POST['code_of_pde']
            financial_year = request.POST['financial_year']
            works = request.POST['procurement-type']
            subject_of_procurement = request.POST['subject']
            plan_reference = request.POST['plan_reference']
            location = request.POST['location']
            date_required = request.POST['date_required']
            requisition = Requisition(
                financial_year = financial_year,
                pde_code = code_of_pde,
                requisition_type = works,
                subject = subject_of_procurement,
                plan_reference = plan_reference,
                delivery_location = location,
                date_required = date_required,
                initiation = datetime.now(),
                initiator = initiator,
                user_department_id = department
            )
            requisition.save()
            context = {
                "requisition": requisition,
                "pending_count": pending(request,requisitions)
            }
            return render(request,"procurement/requisition-page-part2.html",context) 

        else:

            messages.warning(request,"Please fill the requisiton form to initiate the procurement process")
            context = {
                'pending_count': pending(request,requisitions)
            }
            return render(request,"procurement/requisition-form-1.html")
    else:
        context = {
            'pending_count': pending(request,requisitions)
        }
        return render(request,"procurement/requisition-form-1.html",context)

# @RequisitionStatus
@login_required
def back_to_requisition_part1(request, id):
    """
        This routing function takes you back to the first part(i.e section) of the requisition form.
        With the details of that initiated requisition.
    """
    if request.method == "GET":
        code_pde = request.GET["pde_code"]
        financial_year = request.GET["financial_year"]
        works = request.GET["works"]
        subject = request.GET["subject"]
        plan_reference = request.GET["plan_reference"]
        delivery_location = request.GET["delivery_location"]
        date_required = request.GET["date_required"]
        if works: # checks if the part1_details is  not empty
            context = {
                "requisition_id":id,
                "code_of_pde": code_pde,
                "financial_year":financial_year,
                "works":works,
                "subject_of_procurement":subject,
                "reference":plan_reference,
                "location":delivery_location,
                "date_required":date_required
            }
            return render(request, "procurement/requisition-form-1.html", context)

        else:
            messages.warning(request, "No details found")
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

        requisition = Requisition.objects.get(id=id)
        requisition.sequence_number = sequence_number
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
        return render(request,"procurement/requisition-page-part2.html", context)

@login_required
def add_requisition_detail(request,id):
    """
        This routing function commits all the neccessary details of a particular 
        requisition basing on the sequence number of the requisition.
    """
    if request.method == "POST":
        requisition = Requisition.objects.get(id=id)
        if id:
            if requisition.requisition_type == "Supplies" or requisition.requisition_type == "Services":
                currency = request.POST["currency"]
                item = request.POST["item"]
                specifications = request.POST["specifications"]
                terms_of_reference = request.FILES["terms_of_reference"]
                quantity = request.POST["quantity"]
                unit_of_measure = request.POST["unit-of-measure"]
                estimated_cost = request.POST["estimated-cost"]
                market_price = request.POST["market-price"]

                description = Description(
                                    specification = specifications,
                                    terms_of_reference = terms_of_reference 
                                )
                description.save()

                details = Details(
                                item_name = item,
                                quantity = quantity,
                                unit_of_measure = unit_of_measure,
                                estimated_cost = estimated_cost,
                                currency = currency,
                                market_price = market_price,
                                requisition_id = requisition,
                                requisition_description_id = description
                            )
                details.save()

                all_details = Details.objects.all()
                estimated_total_cost = [(detail.estimated_cost) for detail in all_details]
                context = {
                    "requisition":requisition,
                    "all_details" : all_details,
                    "estimated_total_cost": sum(estimated_total_cost)
                }

                return render(request,"procurement/requisition-page-part2.html",context) 

            else:
                currency = request.POST["currency"]
                item = request.POST["item"]
                specifications = request.POST["specifications"]
                terms_of_reference = request.POST["file"]
                scope_of_works = request.POST["file_scope"]
                quantity = request.POST["quantity"]
                unit_of_measure = request.POST["unit-of-measure"]
                estimated_cost = request.POST["estimated-cost"]
                market_price = request.POST["market-price"]

                description = Description(
                                    specification = specifications,
                                    terms_of_reference = terms_of_reference,
                                    scope_of_works = scope_of_works

                                )
                description.save()

                details = Details(
                                item_name = item,
                                quantity = quantity,
                                unit_of_measure = unit_of_measure,
                                estimated_cost = estimated_cost,
                                currency = currency,
                                market_price = market_price,
                                requisition_id = requisition,
                                requisition_description_id = description
                            )
                details.save()
                all_details = Details.objects.all()
                estimated_total_cost = [(detail.estimated_cost) for detail in all_details]
                context = {
                    "requisition":requisition,
                    "all_details" : all_details,
                    "estimated_total_cost": sum(estimated_total_cost)
                }

                return render(request,"procurement/requisition-page-part2.html",context) 


@login_required
def delete_details(request,id):
    """
        This route is used to delete requisition details
    """
    if request.method == "GET":
        details = Details.objects.get(id=id)
        if details:  
            requisition = Requisition.objects.get(id=details.requisition_id.id)
            if details.requisition_id.requisition_type == "Supplies":
                os.remove("media/"+str(details.requisition_description_id.terms_of_reference))
                details.delete()
                all_details = Details.objects.all()
                estimated_total_cost = [(detail.estimated_cost) for detail in all_details]
                context = {
                    "requisition":requisition,
                    "all_details" : all_details,
                    "estimated_total_cost": sum(estimated_total_cost)
                }

                return render(request,"procurement/requisition-page-part2.html",context) 

            else:
                os.remove("media/"+str(details.requisition_description_id.terms_of_reference))
                os.remove("media/"+str(details.requisition_description_id.scope_of_works))
                details.delete()
                all_details = Details.objects.all()
                estimated_total_cost = [(detail.estimated_cost) for detail in all_details]
                context = {
                    "requisition":requisition,
                    "all_details" : all_details,
                    "estimated_total_cost": sum(estimated_total_cost)
                }

                return render(request,"procurement/requisition-page-part2.html",context) 
        else:
            all_details = Details.objects.all()
            estimated_total_cost = [(detail.estimated_cost) for detail in all_details]
            context = {
                    "requisition":requisition,
                    "all_details" : all_details,
                    "estimated_total_cost": sum(estimated_total_cost)
                }
            messages.warning(request,f"details with {details.id} does not exist!")
            return render(request,"procurement/requisition-page-part2.html",context) 



@login_required
def ajax_filter(request):
    """
    This routing function commits all the neccessary details of a particular 
    requisition basing on the sequence number of the requisition.
    """
    if request.is_ajax():
        member_confirmation = request.POST["member_confirmation"]
        if member_confirmation == "true": # confirm that member agreed to the following requisition at hand.
            requisition_id = request.POST["requisition_id"]
            if requisition_id: # check if requisition id exists.
                requisition = Requisition.objects.get(id=requisition_id)
                requisition.member_confirmation = True
                requisition.member_confirmation_date = datetime.now()
                requisition.save()

                return JsonResponse({
                        "success": True,
                        "url": reverse('procurement:view_requisitions'),
                    })
            else:
                return JsonResponse({"success": False})

    return JsonResponse({ "success": False })

@login_required
def view_requisitions(request):
    """
        This is where the hod or user department member can view  requisitions that are
        pending i.e those that need member or hod approval and those submitted to 
        the accounting officer for confirmation for availability of funds.
    """

    if request.method == "GET":
        pending = []
        submitted = []
        requisitions = Requisition.objects.filter().order_by('-initiation')
        for requisition in requisitions:
            if (request.user.profile.member.user_department_id.department_name == 
                requisition.user_department_id.department_name):
                if (requisition.member_confirmation == False or 
                    requisition.hod_confirmation == False or
                    requisition.date_of_submission == None
                    ):
                    details = Details.objects.filter(requisition_id=requisition).all()
                    pending.append((requisition,details))
                    
                elif (requisition.member_confirmation and 
                    requisition.hod_confirmation and 
                    requisition.date_of_submission and 
                    requisition.accepted == False and
                    requisition.rejected == False
                    ):
                    details = Details.objects.filter(requisition_id=requisition).all()
                    submitted.append((requisition,details))
                    
                else:
                    print(requisition)
        context = {
            "pending": pending,
            "pending_count": len(pending),
            "submitted": submitted
        }

        return render(request, "procurement/all-requisitions-page.html", context)

    else:
        return render(request, "procurement/all-requisitions-page.html")

@login_required
def hod_confirmation(request):
    """
        Route used by hod to confirm requisition.
    """
    if request.is_ajax():
        if request.method == "POST":
            requisition_id = request.POST["requisition_id"]
            if requisition_id:
                requisition = Requisition.objects.get(id=int(requisition_id))
                requisition.hod_confirmation = True
                requisition.hod_confirmation_date = datetime.now()
                requisition.date_of_submission = datetime.now()
                requisition.save()

                return JsonResponse({
                        "success": True,
                        "url": reverse('procurement:view_requisitions'),
                    })
            else:
                return JsonResponse({"success": False})
        
        else:
            return JsonResponse({
                        "success": True,
                        "url": reverse('procurement:view_requisitions'),
                    })
    else:
        return JsonResponse({"success": False})


@login_required
def addMember(request):  
    """
        The hod uses this route to add members.
    """
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


# Accounting officer routes
@login_required
def confirm_availability_funds(request):
    """
        This route displays all requisitions submitted to the Accounting Officer.
    """

    if request.method == "GET":
        reqs = Requisition.objects.all().order_by('-initiation')
        yet_to_be_confirmed = []
        for requisition in reqs:
            if (requisition.member_confirmation and 
                requisition.hod_confirmation and
                requisition.date_of_submission and
                requisition.accepted == False and 
                requisition.rejected == False
                ):
                    yet_to_be_confirmed.append(requisition)

        context = {
            "req_count": len(yet_to_be_confirmed),
            "yet_to_be_confirmed": yet_to_be_confirmed,
        }
        return render(request,"procurement/accounting-officer/accounting-officer-page.html", context)

@login_required  
def requisition_more_details(request, id, count):
    """
        This route displays more details of a particular requisition.
    """
    if request.method == "GET":
        requisition = Requisition.objects.get(id=id)
        details = Details.objects.filter(requisition_id=requisition)
        estimated_total_cost = [(detail.estimated_cost) for detail in details]
        context = {
                "req_count": count,
                "requisition": requisition,
                "details": details,
                "estimated_total_cost": sum(estimated_total_cost)
        }
        return render(request, "procurement/accounting-officer/requisition-details-page.html", context)

@login_required
def reject_requisition(request):
    """
        This route function is used by the Accounting Officer to reject a requisition based on a reason.
    """
    if request.is_ajax():
        if request.method == "POST":
            requisition_id = request.POST["requisition_id"]
            reason = request.POST["reason"]
            requisition = Requisition.objects.get(id=requisition_id)
            requisition.rejected = True
            requisition.reason_for_rejection = reason
            requisition.save()

            return JsonResponse({
                        "success": True,
                        "url": reverse('procurement:confirm_availability_funds'),
                    })
    else:
        return JsonResponse({"success": False})

@login_required
def confirm_requisition(request, id):
    """
        This is the routing function used by the Accounting Officer to confirm the availbility of funds.
    """
    if request.method == "POST":
        if id:
            requisition = Requisition.objects.get(id=id)
            vote_no = request.POST["vote_no"]
            programme = request.POST["programme"]
            sub_programme = request.POST["sub_programme"]
            item = request.POST["item_name"]
            balance_remaining = request.POST["balance_remaining"]
            confirmation = AvailabilityOfFunds(
                vote_no = vote_no,
                programme = programme,
                sub_programme = sub_programme,
                item = item,
                balance_remaining = balance_remaining,
                req_id = requisition
            )
            requisition.ao_confirmation = True
            requisition.ao_confirmation_date = datetime.now()
            requisition.accepted = True
            confirmation.save()
            requisition.save()

            messages.success(request, f"Confirmation of requisition with subject of procurement {requisition.subject} was a success!.")
            return redirect("procurement:confirm_availability_funds")

        else:
            messages.warning(request,f"Requisition with id {id} does not exists!.")
            return redirect("procurement:confirm_availability_funds")

    else:
        return redirect("procurement:confirm_availability_funds")

                
