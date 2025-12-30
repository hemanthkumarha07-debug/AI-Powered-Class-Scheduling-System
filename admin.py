from django.contrib import admin
from .models import Instructor, Course, Classroom, TimetableEntry
from .models import TimetableEntry

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(TimetableEntry)
