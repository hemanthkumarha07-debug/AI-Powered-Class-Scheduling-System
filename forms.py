from django import forms
from .models import Instructor, Course, Classroom

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['name']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'instructor', 'duration']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name']
