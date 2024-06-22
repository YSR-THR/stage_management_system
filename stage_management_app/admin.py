from django.contrib import admin
from .models import (
    CustomUser,
    AdminHOD,
    Staffs,
    Courses,
    Subjects,
    Students,
    Internship, 
    Assignment, 
    StudentPreference, 
    StaffPreference
)

# Register each model
admin.site.register(CustomUser)
admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Internship)
admin.site.register(Assignment)
admin.site.register(StudentPreference)
admin.site.register(StaffPreference)