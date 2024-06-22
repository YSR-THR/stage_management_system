"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#urls.py
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from stage_management_app import views, HodViews, StaffViews, StudentViews
from stage_management_system import settings

urlpatterns = [
    path('demo',views.showDemoPage),
    path('admin/', admin.site.urls),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_course', HodViews.add_course,name="add_course"),
    path('add_course_save', HodViews.add_course_save,name="add_course_save"),
    path('add_student', HodViews.add_student,name="add_student"),
    path('add_student_save', HodViews.add_student_save,name="add_student_save"),
    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_course', HodViews.manage_course,name="manage_course"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('edit_staff/<int:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<int:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<int:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<int:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path("delete_staff/<int:staff_id>",HodViews.delete_staff, name='delete_staff'),
    path("delete_course/<int:course_id>",HodViews.delete_course, name='delete_course'),
    path("delete_subject/<int:subject_id>", HodViews.delete_subject, name='delete_subject'),
    path("delete_student/<int:student_id>",HodViews.delete_student, name='delete_student'),
    # Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('student_home', StudentViews.student_home, name="student_home"),

    # Internship CRUD
    path('add_internship/', HodViews.add_internship, name='add_internship'),
    path('add_internship_save', HodViews.add_internship_save,name="add_internship_save"),

    path('manage_internship/', HodViews.manage_internship, name='manage_internship'),
    path('edit_internship/<int:internship_id>/', HodViews.edit_internship, name='edit_internship'),
    path('edit_internship_save', HodViews.edit_internship_save,name="edit_internship_save"),

    path('delete_internship/<int:internship_id>/', HodViews.delete_internship, name='delete_internship'),
    # Student Preferences
    path('add_student_preference/', HodViews.add_student_preference, name='add_student_preference'),
    path('manage_student_preference/', HodViews.manage_student_preference, name='manage_student_preference'),
    path('edit_student_preference/<int:student_preference_id>/', HodViews.edit_student_preference, name='edit_student_preference'),
    path('delete_student_preference/<int:student_preference_id>/', HodViews.delete_student_preference, name='delete_student_preference'),
    # Staff Preferences
    path('add_staff_preference/', HodViews.add_staff_preference, name='add_staff_preference'),
    path('manage_staff_preference/', HodViews.manage_staff_preference, name='manage_staff_preference'),
    path('edit_staff_preference/<int:staff_preference_id>/', HodViews.edit_staff_preference, name='edit_staff_preference'),
    path('delete_staff_preference/<int:staff_preference_id>/', HodViews.delete_staff_preference, name='delete_staff_preference'),
    # Assignment CRUD
    path('add_assignment/', HodViews.add_assignment, name='add_assignment'),
    path('manage_assignment/', HodViews.manage_assignment, name='manage_assignment'),
    path('edit_assignment/<int:assignment_id>/', HodViews.edit_assignment, name='edit_assignment'),
    path('delete_assignment/<int:assignment_id>/', HodViews.delete_assignment, name='delete_assignment'),
    # Matching and Preferences Submission
    path('match_students/', HodViews.match_students, name='match_students'),
    path('validate_assignments/', HodViews.validate_assignments, name='validate_assignments'),

    # Student Views
    path('submit_preferences/', StudentViews.submit_student_preferences, name='submit_student_preferences'),
    path('manage_preferences/', StudentViews.manage_student_preferences, name='manage_student_preferences'),
    path('assignments/', StudentViews.student_assignments, name='student_assignments'),
    # staff Views
    path('submit_staff_preferences/', StaffViews.submit_staff_preferences, name='submit_staff_preferences'),
    path('manage_staff_preferences/', StaffViews.manage_staff_preferences, name='manage_staff_preferences'),
    path('staff_assignments/', StaffViews.staff_assignments, name='staff_assignments'),
    # HOD Views


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)