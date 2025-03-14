from datetime import datetime
from http.client import HTTPResponse
from lib2to3.fixes.fix_input import context

from django.db.models.fields import return_None
from django.shortcuts import render,HttpResponse
from django.template.context_processors import request

from .models import Employee, Role, Deparment
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')



def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request,'view_all_emp.html', context)


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name = first_name, last_name = last_name, salary = salary, bonus = bonus, phone = phone, dept_id = dept, role_id = role, hire_date = datetime.now())
        new_emp.save()
        return HttpResponse('Employee Added Successful')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse('Exception Ocured!!')




def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Remove Successfully")
        except:
            return HttpResponse("Please Enter a Valid emp_id")
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request,'remove_emp.html', context)



def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        # Get all employees initially
        emps = Employee.objects.all()

        # Apply filters based on input values
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__contains =dept)
        if role:
            emps = emps.filter(role__name__contains=role)

        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')
