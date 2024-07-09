# StaffViews.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StaffPreferenceForm
from .models import StaffPreference, Staffs, Students, Assignment, Internship
from django.contrib.auth.decorators import login_required

def staff_home(request):
    if request.user.user_type != '2':  # Ensure it's a staff
     return redirect('staff_home')

    staff = Staffs.objects.get(admin=request.user)
    internships = Internship.objects.all()  # Fetch all internships
    return render(request, "staff_template/staff_home_template.html",{'staff':staff,'internships': internships})

def submit_staff_preferences(request):
    if request.user.user_type != '2':  # Ensure it's a staff
        return redirect('staff_home')

    staff = Staffs.objects.get(admin=request.user)
    internships = Internship.objects.all()  # Fetch all internships

    if request.method == 'POST':
        form = StaffPreferenceForm(request.POST, staff=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted Preference")
            return redirect('manage_staff_preferences')
        else:
            messages.error(request, "Failed to Submit Preference")
    else:
        form = StaffPreferenceForm(staff=staff)

    return render(request, 'staff_template/submit_staff_preferences.html', {'form': form, 'internships': internships})

@login_required
def manage_staff_preferences(request):
    staff = Staffs.objects.get(admin=request.user.id)
    staff_preferences = StaffPreference.objects.filter(staff=staff)
    internships = Internship.objects.all()  # Fetch all internships for display
    return render(request, 'staff_template/manage_staff_preferences.html', {'staff_preferences': staff_preferences, 'internships': internships})

def staff_assignments(request):
    staff = Staffs.objects.get(admin=request.user.id)
    assignments = Assignment.objects.filter(staff=staff, status='finalized')
    return render(request, 'staff_template/staff_assignments.html', {'assignments': assignments})

""""
#StaffViews.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StaffPreferenceForm
from .models import StaffPreference, Staffs, Students, Assignment,Internship
from django.contrib.auth.decorators import login_required

def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")


def submit_staff_preferences(request):
    if request.user.user_type != '2':  # Ensure it's a staff
        return redirect('staff_home')

    staff = Staffs.objects.get(admin=request.user)
    internships = Internship.objects.all()  # Fetch all internships

    if request.method == 'POST':
        form = StaffPreferenceForm(request.POST, staff=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted Preference")
            return redirect('manage_staff_preferences')
        else:
            messages.error(request, "Failed to Submit Preference")
    else:
        form = StaffPreferenceForm(staff=staff)

    return render(request, 'staff_template/submit_staff_preferences.html', {'form': form, 'internships': internships})

@login_required
def manage_staff_preferences(request):
    staff = Staffs.objects.get(admin=request.user.id)
    staff_preferences = StaffPreference.objects.filter(staff=staff)
    internships = Internship.objects.all()  # Fetch all internships for display
    return render(request, 'staff_template/manage_staff_preferences.html', {'staff_preferences': staff_preferences, 'internships': internships})

def staff_assignments(request):
    staff = Staffs.objects.get(admin=request.user.id)
    assignments = Assignment.objects.filter(staff=staff, status='finalized')
    return render(request, 'staff_template/staff_assignments.html', {'assignments': assignments})
"""