# StudentViews.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentPreferenceForm
from .models import StudentPreference, Students, Staffs, Assignment, Subjects
from django.contrib.auth.decorators import login_required

def student_home(request):
    if request.user.user_type != '3':  # Ensure it's a student
        return redirect('student_home')

    student = Students.objects.get(admin=request.user)

    staffs = Staffs.objects.all()
    for staff in staffs:
        staff.subjects = Subjects.objects.filter(staff_id=staff.admin.id)
    return render(request, "student_template/student_home_template.html",{'staffs':staffs,'student':student})

def submit_student_preferences(request):
    if request.user.user_type != '3':  # Ensure it's a student
        return redirect('student_home')

    student = Students.objects.get(admin=request.user)

    # Fetch all staffs
    staffs = Staffs.objects.all()

    # Attach subjects to each staff instance
    for staff in staffs:
        staff.subjects = Subjects.objects.filter(staff_id=staff.admin.id)

    if request.method == 'POST':
        form = StudentPreferenceForm(request.POST, student=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted Preference")
            return redirect('manage_student_preferences')
        else:
            messages.error(request, "Failed to Submit Preference")
    else:
        form = StudentPreferenceForm(student=student)

    return render(request, 'student_template/submit_student_preferences.html', {'form': form, 'staffs': staffs})

def manage_student_preferences(request):
    student = Students.objects.get(admin=request.user.id)
    student_preferences = StudentPreference.objects.filter(student=student)
    return render(request, 'student_template/manage_student_preferences.html', {'student_preferences': student_preferences})

def student_assignments(request):
    student = Students.objects.get(admin=request.user.id)
    assignments = Assignment.objects.filter(student=student, status='finalized')
    return render(request, 'student_template/student_assignments.html', {'assignments': assignments})

""""
#StudentViews.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentPreferenceForm
from .models import StudentPreference, Students, Staffs, Assignment,Subjects
from django.contrib.auth.decorators import login_required

def student_home(request):
    return render(request,"student_template/student_home_template.html")


# StudentViews.py

def submit_student_preferences(request):
    if request.user.user_type != '3':  # Ensure it's a student
        return redirect('student_home')

    student = Students.objects.get(admin=request.user)

    # Fetch all staffs
    staffs = Staffs.objects.all()

    # Attach subjects to each staff instance
    for staff in staffs:
        staff.subjects = Subjects.objects.filter(staff_id=staff.admin.id)

    if request.method == 'POST':
        form = StudentPreferenceForm(request.POST, student=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted Preference")
            return redirect('student_template/manage_student_preferences')
        else:
            messages.error(request, "Failed to Submit Preference")
    else:
        form = StudentPreferenceForm(student=student)

    return render(request, 'student_template/submit_student_preferences.html', {'form': form, 'staffs': staffs})

def manage_student_preferences(request):
    student = Students.objects.get(admin=request.user.id)
    student_preferences = StudentPreference.objects.filter(student=student)
    return render(request, 'student_template/manage_student_preferences.html', {'student_preferences': student_preferences})

def student_assignments(request):
    student = Students.objects.get(admin=request.user.id)
    assignments = Assignment.objects.filter(student=student, status='finalized')
    return render(request, 'student_template/student_assignments.html', {'assignments': assignments})

"""