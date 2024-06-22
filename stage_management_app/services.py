# services.py
"""from .models import StudentPreference, StaffPreference, Assignment, Students, Staffs, Internship
from collections import defaultdict
#import numpy as np

def calculate_weighted_preferences():
    # Calculate weights for student preferences
    for pref in StudentPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.student, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

    # Calculate weights for staff preferences
    for pref in StaffPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.student, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

def calculate_domain_match(student, staff):
    student_domains = set(student.internship_set.values_list('domain', flat=True))
    staff_subjects = set(staff.subjects.all().values_list('name', flat=True))
    match_count = len(student_domains & staff_subjects)
    return match_count / len(student_domains) if student_domains else 0.0

def gale_shapley_algorithm():
    student_prefs = defaultdict(list)
    for pref in StudentPreference.objects.order_by('rank'):
        student_prefs[pref.student_id].append((pref.staff_id, pref.weight))

    staff_prefs = defaultdict(list)
    for pref in StaffPreference.objects.order_by('rank'):
        staff_prefs[pref.staff_id].append((pref.student_id, pref.weight))

    students_free = set(student_prefs.keys())
    staff_capacity = {staff.id: staff.max_students for staff in Staffs.objects.all()}
    staff_assigned = defaultdict(list)
    student_assigned = {}

    while students_free:
        student = students_free.pop()
        prefs = sorted(student_prefs[student], key=lambda x: -x[1])  # Sort by weight descending

        for staff, _ in prefs:
            if len(staff_assigned[staff]) < staff_capacity[staff]:
                staff_assigned[staff].append(student)
                student_assigned[student] = staff
                break
            else:
                # Compare the least preferred currently assigned student with the new one
                least_preferred_student = min(staff_assigned[staff], key=lambda s: next(w for st, w in student_prefs[s] if st == staff))
                least_preferred_weight = next(w for st, w in student_prefs[least_preferred_student] if st == staff)
                new_student_weight = next(w for st, w in student_prefs[student] if st == staff)

                if new_student_weight > least_preferred_weight:
                    staff_assigned[staff].remove(least_preferred_student)
                    staff_assigned[staff].append(student)
                    students_free.add(least_preferred_student)
                    student_assigned[student] = staff
                    break

    # Create and save assignments
    for student, staff in student_assigned.items():
        internship = Internship.objects.filter(student_id=student).first()
        assignment, created = Assignment.objects.get_or_create(student_id=student, staff_id=staff, internship_id=internship.id)
        if created:
            assignment.save()

    return student_assigned"""
"""
# services.py
from collections import defaultdict
from .models import StudentPreference, StaffPreference, Students, Staffs, Internship, Assignment, Subjects

def calculate_weighted_preferences():
    for pref in StudentPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.student, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

    for pref in StaffPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.internship.student_id, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

def calculate_domain_match(student, staff):
    student_internships = Internship.objects.filter(student_id=student)
    staff_subjects = set(Subjects.objects.filter(staff_id=staff.admin).values_list('subject_name', flat=True))
    
    match_score = 0.0
    for internship in student_internships:
        internship_domains = set(internship.domain.split(','))
        common_domains = internship_domains.intersection(staff_subjects)
        match_score += len(common_domains) / len(internship_domains.union(staff_subjects))

    return match_score / len(student_internships) if student_internships else 0.1

def gale_shapley_algorithm():
    students_free = set(Students.objects.all())
    student_prefs = defaultdict(list)
    staff_capacity = {staff: staff.max_students for staff in Staffs.objects.all()}
    staff_assigned = defaultdict(list)
    student_assigned = {}

    for pref in StudentPreference.objects.all():
        student_prefs[pref.student].append((pref.staff, pref.weight))

    for student in student_prefs:
        student_prefs[student].sort(key=lambda x: -x[1])

    while students_free:
        student = students_free.pop()
        if student not in student_assigned:
            preferred_staff = student_prefs[student].pop(0)[0]
            staff_assigned[preferred_staff].append(student)
            student_assigned[student] = preferred_staff

            if len(staff_assigned[preferred_staff]) > staff_capacity[preferred_staff]:
                lowest_rank_student = min(
                    staff_assigned[preferred_staff], 
                    key=lambda s: next(w for st, w in student_prefs[s] if st == preferred_staff)
                )
                staff_assigned[preferred_staff].remove(lowest_rank_student)
                students_free.add(lowest_rank_student)
                del student_assigned[lowest_rank_student]

    for student, staff in student_assigned.items():
        internship = Internship.objects.filter(student_id=student).first()
        Assignment.objects.create(student=student, staff=staff, internship=internship, status='pre-assigned')

    return Assignment.objects.all()
"""
from collections import defaultdict
from .models import StudentPreference, StaffPreference, Students, Staffs, Internship, Assignment, Subjects
def calculate_weighted_preferences():
    for pref in StudentPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.student, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

    for pref in StaffPreference.objects.all():
        domain_match_weight = calculate_domain_match(pref.internship.student_id, pref.staff)
        pref.weight = (1.0 / (pref.rank + 1)) * domain_match_weight
        pref.save()

def calculate_domain_match(student, staff):
    student_internships = Internship.objects.filter(student_id=student)
    staff_subjects = set(Subjects.objects.filter(staff_id=staff.admin).values_list('subject_name', flat=True))
    
    match_score = 0.0
    for internship in student_internships:
        internship_domains = set(internship.domain.split(','))
        common_domains = internship_domains.intersection(staff_subjects)
        match_score += len(common_domains) / len(internship_domains.union(staff_subjects))

    return match_score / len(student_internships) if student_internships else 0.1

def gale_shapley_algorithm():
    students_free = set(Students.objects.all())
    student_prefs = defaultdict(list)
    staff_capacity = {staff: staff.max_students for staff in Staffs.objects.all()}
    staff_assigned = defaultdict(list)
    student_assigned = {}

    # Populate student_prefs with preferences
    for pref in StudentPreference.objects.all():
        student_prefs[pref.student].append((pref.staff, pref.weight))

    # Sort preferences by weight (descending) for each student
    for student in student_prefs:
        student_prefs[student].sort(key=lambda x: -x[1])

    # Debug: Log initial preferences
    print(f"Initial student preferences: {student_prefs}")

    while students_free:
        student = students_free.pop()
        
        # Debug: Log current student being processed
        print(f"Processing student: {student}")

        if student not in student_assigned:
            if student_prefs[student]:
                preferred_staff = student_prefs[student].pop(0)[0]
                staff_assigned[preferred_staff].append(student)
                student_assigned[student] = preferred_staff

                # Debug: Log assignment status
                print(f"Assigned {student} to {preferred_staff}")

                if len(staff_assigned[preferred_staff]) > staff_capacity[preferred_staff]:
                    lowest_rank_student = min(
                        staff_assigned[preferred_staff], 
                        key=lambda s: next((w for st, w in student_prefs[s] if st == preferred_staff), None)
                    )
                    staff_assigned[preferred_staff].remove(lowest_rank_student)
                    students_free.add(lowest_rank_student)
                    del student_assigned[lowest_rank_student]

                    # Debug: Log reassignment status
                    print(f"Reassigned {lowest_rank_student} from {preferred_staff}")

            else:
                # Handle case where student has no preferences left
                print(f"No preferences left for student: {student}")
                # Define your fallback logic here, e.g., assign to a default staff, skip, etc.

    for student, staff in student_assigned.items():
        internship = Internship.objects.filter(student_id=student).first()
        Assignment.objects.create(student=student, staff=staff, internship=internship, status='pre-assigned')

    # Debug: Log final assignments
    final_assignments = Assignment.objects.all()
    print(f"Final assignments: {final_assignments}")

    return final_assignments
