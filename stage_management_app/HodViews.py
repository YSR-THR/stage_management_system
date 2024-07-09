#HodViews.py
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import AddStudentForm, EditStudentForm, InternshipForm, StaffPreferenceForm, StudentPreferenceForm, AssignmentForm
from .models import CustomUser, Staffs, Courses, Subjects, Students, Internship, StudentPreference, StaffPreference, Assignment
from .services import gale_shapley_algorithm, calculate_weighted_preferences

def admin_home(request):
    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    internship_count = Internship.objects.all().count()
    staff_count = Staffs.objects.all().count()

    
    subject_list = []
    subjects = Subjects.objects.all()
    for subject in subjects:
        subject_list.append(subject.subject_name)    

    internship_list = []
    internships = Internship.objects.all()
    for internship in internships:
        internship_list.append(internship.topic) 

    # For Saffs
    staff_name_list=[]

    staffs = Staffs.objects.all()
    for staff in staffs:
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        student_name_list.append(student.admin.first_name)


    context={
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "internship_count": internship_count,
        "staff_count": staff_count,
        "subject_list": subject_list,
        "internship_list" : internship_list,
        "staff_name_list": staff_name_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        max_students=request.POST.get("max_students")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.staffs.phone=phone
            user.staffs.max_students=max_students
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            phone=form.cleaned_data["phone"]
            session=form.cleaned_data["session"]
            course_id=form.cleaned_data["course"]

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address=address
                user.students.phone=phone
                user.students.session=session
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                print(f"Error: {e}")  # Log the actual error
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        max_students=request.POST.get("max_students")
        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.phone=phone
            staff_model.max_students=max_students
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['phone'].initial=student.phone
    form.fields['course'].initial=student.course_id.id
    form.fields['session'].initial=student.session
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            phone = form.cleaned_data["phone"]
            session = form.cleaned_data["session"]
            course_id = form.cleaned_data["course"]

            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                student.phone=phone
                student.session=session
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def delete_staff(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    user = staff.admin
    staff.delete()
    user.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))

def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))

def delete_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    try:
        course.delete()
        messages.success(request, "Course deleted successfully!")
    except Exception:
        messages.error(request, "Sorry, some students are assigned to this course already. Kindly change the affected student course and try again.")
    return redirect(reverse('manage_course'))

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subjects, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


##########

#HodView.py

def add_internship(request):
  form = InternshipForm()
  students = Students.objects.all()  # Fetch all students
  return render(request, "hod_template/add_internship_template.html", {"form": form, "students": students})

def add_internship_save(request):
  if request.method != "POST":
    return HttpResponse("Method Not Allowed")
  else:
    form = InternshipForm(request.POST)
    if form.is_valid():
      domain = form.cleaned_data['domain']
      organization_type = form.cleaned_data['organization_type']
      organization_size = form.cleaned_data['organization_size']
      location = form.cleaned_data['location']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']
      duration = form.cleaned_data['duration']
      contacts = form.cleaned_data['contacts']
      topic = form.cleaned_data['topic']
      student_id = form.cleaned_data['student_id']
      additional_comments = form.cleaned_data['additional_comments']
      
      try:
        # Create a new Internship object with form data
        internship = Internship.objects.create(
            domain=domain,
            organization_type=organization_type,
            organization_size=organization_size,
            location=location,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            contacts=contacts,
            topic=topic,
            student_id=student_id,
            additional_comments=additional_comments,
        )
        internship.save()
        messages.success(request, "Successfully Added Internship")
        return HttpResponseRedirect(reverse("add_internship"))
      except Exception as e:
        print(f"Error: {e}")
        messages.error(request, "Failed to Add Internship")
        return HttpResponseRedirect(reverse("add_internship"))
    else:
      return render(request, "hod_template/add_internship_template.html", {"form": form})
    
def manage_internship(request):
    internships = Internship.objects.all()
    return render(request, "hod_template/manage_internship_template.html", {"internships": internships})

def edit_internship(request, internship_id):
    internship = Internship.objects.get(id=internship_id)
    students = Students.objects.all()
    return render(request, "hod_template/edit_internship_template.html", {"internship": internship, "students": students})

def edit_internship_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        internship_id = request.POST.get("internship_id")
        internship = Internship.objects.get(id=internship_id)

        domain = request.POST.get("domain")
        organization_type = request.POST.get("organization_type")
        organization_size = request.POST.get("organization_size")
        location = request.POST.get("location")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        duration = request.POST.get("duration")
        contacts = request.POST.get("contacts")
        topic = request.POST.get("topic")
        student_id = request.POST.get("student")
        additional_comments = request.POST.get("additional_comments")

        try:
            # Update the Internship object with the new data
            internship.domain = domain
            internship.organization_type = organization_type
            internship.organization_size = organization_size
            internship.location = location
            internship.start_date = start_date
            internship.end_date = end_date
            internship.duration = duration
            internship.contacts = contacts
            internship.topic = topic
            internship.student_id_id = student_id
            internship.additional_comments = additional_comments

            internship.save()
            messages.success(request, "Successfully Updated Internship")
            return HttpResponseRedirect(reverse("manage_internship"))
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "Failed to Update Internship")
            return HttpResponseRedirect(reverse("manage_internship"))


def delete_internship(request, internship_id):
    internship = Internship.objects.get(id=internship_id)
    internship.delete()
    messages.success(request, "Successfully Deleted Internship")
    return HttpResponseRedirect(reverse("manage_internship"))

# Student Preferences
def add_student_preference(request):
    if request.method == "POST":
        form = StudentPreferenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Student Preference")
            return redirect('manage_student_preference')
        else:
            messages.error(request, "Failed to Add Student Preference")
    else:
        form = StudentPreferenceForm()
    return render(request, "hod_template/add_student_preference_template.html", {"form": form})

def manage_student_preference(request):
    preferences = StudentPreference.objects.select_related('student__admin', 'staff__admin').all()
    return render(request, "hod_template/manage_student_preference_template.html", {"preferences": preferences})

def edit_student_preference(request, student_preference_id):
    preference = get_object_or_404(StudentPreference, id=student_preference_id)
    if request.method == "POST":
        form = StudentPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited Student Preference")
            return redirect('manage_student_preference')
        else:
            messages.error(request, "Failed to Edit Student Preference")
    else:
        form = StudentPreferenceForm(instance=preference)
    return render(request, "hod_template/edit_student_preference_template.html", {"form": form})

def delete_student_preference(request, student_preference_id):
    preference = get_object_or_404(StudentPreference, id=student_preference_id)
    preference.delete()
    messages.success(request, "Successfully Deleted Student Preference")
    return redirect('manage_student_preference')

# Staff Preferences
def add_staff_preference(request):
    if request.method == "POST":
        form = StaffPreferenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added Staff Preference")
            return redirect('manage_staff_preference')
        else:
            messages.error(request, "Failed to Add Staff Preference")
    else:
        form = StaffPreferenceForm()
    return render(request, "hod_template/add_staff_preference_template.html", {"form": form})

def manage_staff_preference(request):
    staff_preferences = StaffPreference.objects.select_related('staff__admin', 'internship').all()
    return render(request, "hod_template/manage_staff_preference_template.html", {"staff_preferences": staff_preferences})

def edit_staff_preference(request, staff_preference_id):
    staff_preference = get_object_or_404(StaffPreference, id=staff_preference_id)
    if request.method == "POST":
        form = StaffPreferenceForm(request.POST, instance=staff_preference)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited Staff Preference")
            return redirect('manage_staff_preference')
        else:
            messages.error(request, "Failed to Edit Staff Preference")
    else:
        form = StaffPreferenceForm(instance=staff_preference)
    return render(request, "hod_template/edit_staff_preference_template.html", {"form": form})

def delete_staff_preference(request, staff_preference_id):
    staff_preference = get_object_or_404(StaffPreference, id=staff_preference_id)
    staff_preference.delete()
    messages.success(request, "Successfully Deleted Staff Preference")
    return redirect('manage_staff_preference')

def add_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.status = 'pre-assigned'  # Set default status
            assignment.save()
            messages.success(request, "Successfully Added Assignment")
            return HttpResponseRedirect(reverse("manage_assignment"))
        else:
            messages.error(request, "Failed to Add Assignment")
            return HttpResponseRedirect(reverse("add_assignment"))
    else:
        form = AssignmentForm()
    return render(request, "hod_template/add_assignment_template.html", {"form": form})

def manage_assignment(request):
    assignments = Assignment.objects.all()
    return render(request, "hod_template/manage_assignment_template.html", {"assignments": assignments})

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited Assignment")
            return redirect("manage_assignment")
        else:
            messages.error(request, "Failed to Edit Assignment")
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, "hod_template/edit_assignment_template.html", {"form": form, "id": assignment_id})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    messages.success(request, "Successfully Deleted Assignment")
    return redirect("manage_assignment")

def match_students(request):
    calculate_weighted_preferences()
    assignments = gale_shapley_algorithm()
    messages.success(request, "Successfully matched students with staffs.")
    return redirect("manage_assignment")

def validate_assignments(request):
    assignments = Assignment.objects.filter(status='pre-assigned')
    if request.method == 'POST':
        for assignment in assignments:
            assignment.status = 'finalized'
            assignment.save()
        messages.success(request, "Successfully validated assignments.")
    return redirect("manage_assignment")