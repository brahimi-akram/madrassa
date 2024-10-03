from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .utils import *

# Create your views here.
def home(request):
    if request.user.is_staff:
        return render(request,"home.html")
    return redirect("add_form")

@never_cache
def add_form(request):
    if request.method== 'GET':
        levels= Level.objects.all()
        if request.user.is_staff:
            return render(request,'add_form.html',{'levels':levels})
        else:
            return render(request,"add_form_parent.html",{"levels":levels})
    else:
        student = Student()
        student.confirmed = False
        if request.user.is_staff:
            student.num = int(request.POST.get('student_id'))
            student.situation = request.POST.get('situation')
            student.confirmed = True
            teacher_name = request.POST.get('teacher_name')
            try:
                teacher = Teacher.objects.get(name = teacher_name)
            except:
                teacher = Teacher()
                teacher.name = teacher_name
                teacher.save()
            student.teacher = teacher
        student.level = Level.objects.get(pk=int(request.POST.get('level_id')))
        student.first_name = request.POST.get('student_name')
        student.last_name = request.POST.get('student_last_name')
        student.date_birth = request.POST.get('date_birth')
        student.adress = request.POST.get('adress')
        student.level_year = int(request.POST.get('level_year'))
        try:
            parent = Parent.objects.get(name=request.POST.get('parent_name'))
        except:
            parent = Parent()
            parent.name = request.POST.get('parent_name')
            parent.phone = request.POST.get('parent_phone')
            parent.save()
        student.parent=parent
        student.save()
        if request.user.is_staff:

            generate_doc(student.id)
            return redirect('list_student')
        else:
            return redirect('show_barecode',student.id)
    
def show_barecode(request,student_id):
    return render (request,"code.html",{"student_id":student_id})    

@csrf_exempt
def get_form(request):
    if request.user.is_staff:
        if request.method == "GET":
            to_be_confirmed = Student.objects.filter(confirmed = False)
            return render(request,"get_form.html" ,{"students":to_be_confirmed})
        else:
            id = int(request.POST.get('student_code'))
            return redirect("update_form",id)
    return render(request,"home.html")

def update_form(request,id):
    if request.user.is_staff:
        student = Student.objects.get(id = id)
        if request.method == 'GET':
            return render(request,"update_form.html",{"student":student})
        else : 
            student.num = int(request.POST.get('student_id'))
            teacher_name = request.POST.get('teacher_name')
            try:
                teacher = Teacher.objects.get(name = teacher_name)
            except:
                teacher = Teacher()
                teacher.name = teacher_name
                teacher.save()
            student.teacher = teacher
            student.situation = request.POST.get('situation')
            student.level = Level.objects.get(pk=int(request.POST.get('level_id')))
            student.first_name = request.POST.get('student_name')
            student.last_name = request.POST.get('student_last_name')
            student.date_birth = request.POST.get('date_birth')
            student.adress = request.POST.get('adress')
            student.level_year = int(request.POST.get('level_year'))
            student.parent.name = request.POST.get('parent_name')
            student.parent.phone = request.POST.get('parent_phone')
            student.parent.save()
            student.confirmed = True
            student.save()
            generate_doc(student.id)
            return redirect("list_student")
    return render(request,"home.html")

def list_student(request):
    students = Student.objects.filter(confirmed = True)
    return render (request,"list_student.html",{"students":students})