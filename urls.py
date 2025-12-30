from django.urls import path
from .views import (
    home,
    add_instructor, list_instructors, edit_instructor, delete_instructor,
    add_course, list_courses, edit_course, delete_course,
    add_classroom, list_classrooms, edit_classroom, delete_classroom,
    generate_timetable_view, timetable_view,
    timetable_matrix_all_classes, timetable_matrix_classroom,
)
from .views import (
    # ... other imports ...,
    timetable_by_instructor_boxed,
)

urlpatterns = [
    path('', home, name='home'),

    # Instructor CRUD
    path('add-instructor/', add_instructor, name='add_instructor'),
    path('instructors/', list_instructors, name='list_instructors'),
    path('instructors/<int:pk>/edit/', edit_instructor, name='edit_instructor'),
    path('instructors/<int:pk>/delete/', delete_instructor, name='delete_instructor'),

    # Course CRUD
    path('add-course/', add_course, name='add_course'),
    path('courses/', list_courses, name='list_courses'),
    path('courses/<int:pk>/edit/', edit_course, name='edit_course'),
    path('courses/<int:pk>/delete/', delete_course, name='delete_course'),

    # Classroom CRUD
    path('add-classroom/', add_classroom, name='add_classroom'),
    path('classrooms/', list_classrooms, name='list_classrooms'),
    path('classrooms/<int:pk>/edit/', edit_classroom, name='edit_classroom'),
    path('classrooms/<int:pk>/delete/', delete_classroom, name='delete_classroom'),

    # Timetable Generation and Flat View
    path('generate-timetable/', generate_timetable_view, name='generate_timetable'),
    path('timetable/', timetable_view, name='timetable'),

    # Boxed Matrix Timetable (all classes and per class)
    path('timetable-matrix/all/', timetable_matrix_all_classes, name='timetable_matrix_all'),
    path('timetable-matrix/classroom/<int:classroom_id>/', timetable_matrix_classroom, name='timetable_matrix_classroom'),
    path('timetable-by-instructor-boxed/', timetable_by_instructor_boxed, name='timetable_by_instructor_boxed'),
]
