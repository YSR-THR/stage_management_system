#forms.py
from django import forms
from stage_management_app.models import Courses, StudentPreference, StaffPreference, Internship, Assignment, Students, Staffs,CustomUser

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mot de passe", max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Prénom", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Nom de famille", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Nom d'utilisateur", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Adresse", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Téléphone", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    courses = Courses.objects.all()
    course_list = [(course.id, course.course_name) for course in courses]
    course = forms.ChoiceField(label="Formation", choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    session = forms.DateField(label="Session", widget=DateInput(attrs={"class": "form-control"}))

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Prénom", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Nom de famille", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Nom d'utilisateur", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Adresse", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Téléphone", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    courses = Courses.objects.all()
    course_list = [(course.id, course.course_name) for course in courses]
    course = forms.ChoiceField(label="Formation", choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    session = forms.DateField(label="Session", widget=DateInput(attrs={"class": "form-control"}))

class InternshipForm(forms.ModelForm):
    student_id = forms.ModelChoiceField(queryset=Students.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Internship
        fields = ['domain', 'organization_type', 'organization_size', 'location', 'start_date', 'end_date', 'duration', 'contacts', 'topic', 'student_id', 'additional_comments']
        labels = {
            'domain': 'Domaine',
            'organization_type': 'Type d\'organisation',
            'organization_size': 'Taille de l\'organisation',
            'location': 'Lieu',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'duration': 'Durée (en semaines)',
            'contacts': 'Contacts',
            'topic': 'Sujet',
            'student_id': 'Étudiant',
            'additional_comments': 'Commentaires supplémentaires',
        }
        widgets = {
            'domain': forms.TextInput(attrs={"class": "form-control"}),
            'organization_type': forms.TextInput(attrs={"class": "form-control"}),
            'organization_size': forms.TextInput(attrs={"class": "form-control"}),
            'location': forms.TextInput(attrs={"class": "form-control"}),
            'start_date': DateInput(attrs={"class": "form-control"}),
            'end_date': DateInput(attrs={"class": "form-control"}),
            'duration': forms.NumberInput(attrs={"class": "form-control"}),
            'contacts': forms.TextInput(attrs={"class": "form-control"}),
            'topic': forms.Textarea(attrs={"class": "form-control"}),
            'additional_comments': forms.Textarea(attrs={"class": "form-control"}),
        }


class StudentPreferenceForm(forms.ModelForm):
    class Meta:
        model = StudentPreference
        fields = ['student', 'staff', 'rank']
        labels = {
            'student': 'Étudiant',
            'staff': 'Tuteur',
            'rank': 'Rang',
        }
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(StudentPreferenceForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['student'].initial = student
            self.fields['student'].widget = forms.HiddenInput()
        self.fields['staff'].queryset = Staffs.objects.all()


class StaffPreferenceForm(forms.ModelForm):
    staff = forms.ModelChoiceField(queryset=Staffs.objects.all(), required=True, label="Tuteur")
    internship = forms.ModelChoiceField(queryset=Internship.objects.all(), required=True, label="Sujet de stage")

    class Meta:
        model = StaffPreference
        fields = ['staff', 'internship', 'rank']
        labels = {
            'staff': 'Personnel',
            'internship': 'Sujet de stage',
            'rank': 'Rang',
        }
    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)  # Get the staff instance from kwargs
        super().__init__(*args, **kwargs)
        self.fields['internship'].queryset = Internship.objects.all()  # Set the queryset for internship choices
        self.staff_instance = staff  # Store the staff instance for later use
        if self.staff_instance:
            self.fields['staff'].initial = self.staff_instance
            self.fields['staff'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        internship = cleaned_data.get("internship")
        if internship:
            cleaned_data['student'] = internship.student_id  # Assuming internship has a student_id field
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.staff_instance:
            instance.staff = self.staff_instance  # Assign the staff instance to the StaffPreference instance
        if commit:
            instance.save()
        return instance


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['student', 'staff', 'internship']
        labels = {
            'student': 'Étudiant',
            'staff': 'Tuteur',
            'internship': 'Stage',
        }
        widgets = {
            'student': forms.Select(attrs={"class": "form-control"}),
            'staff': forms.Select(attrs={"class": "form-control"}),
            'internship': forms.Select(attrs={"class": "form-control"}),
}
