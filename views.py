from django.shortcuts import render, redirect, get_object_or_404
from .models import Instructor, Course, Classroom, TimetableEntry
from .forms import InstructorForm, CourseForm, ClassroomForm
from .schedule_utils import generate_weekly_timetable

# --- Period/day config for boxed view ---
PERIODS = [
    ("08:30-09:30", "P1"),
    ("09:30-10:30", "P2"),
    ("11:00-12:00", "P3"),
    ("12:00-13:00", "P4"),
    ("13:00-14:00", "LUNCH"),
    ("14:00-15:00", "P5"),
    ("15:00-16:00", "P6"),
    ("16:00-17:00", "P7"),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# --- Dashboard Home ---
def home(request):
    return render(request, 'scheduler/home.html')

# --- Instructor CRUD ---
def add_instructor(request):
    form = InstructorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_instructors')
    return render(request, 'scheduler/add_instructor.html', {'form': form})

def edit_instructor(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    form = InstructorForm(request.POST or None, instance=instructor)
    if form.is_valid():
        form.save()
        return redirect('list_instructors')
    return render(request, 'scheduler/edit_instructor.html', {'form': form})

def delete_instructor(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == "POST":
        instructor.delete()
        return redirect('list_instructors')
    return render(request, 'scheduler/delete_instructor.html', {'instructor': instructor})

def list_instructors(request):
    instructors = Instructor.objects.all().order_by('name')
    return render(request, 'scheduler/list_instructors.html', {'instructors': instructors})

# --- Course CRUD ---
def add_course(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_courses')
    return render(request, 'scheduler/add_course.html', {'form': form})

def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('list_courses')
    return render(request, 'scheduler/edit_course.html', {'form': form})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect('list_courses')
    return render(request, 'scheduler/delete_course.html', {'course': course})

def list_courses(request):
    courses = Course.objects.all().order_by('name')
    return render(request, 'scheduler/list_courses.html', {'courses': courses})

# --- Classroom CRUD ---
def add_classroom(request):
    form = ClassroomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_classrooms')
    return render(request, 'scheduler/add_classroom.html', {'form': form})

def edit_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    form = ClassroomForm(request.POST or None, instance=classroom)
    if form.is_valid():
        form.save()
        return redirect('list_classrooms')
    return render(request, 'scheduler/edit_classroom.html', {'form': form})

def delete_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == "POST":
        classroom.delete()
        return redirect('list_classrooms')
    return render(request, 'scheduler/delete_classroom.html', {'classroom': classroom})

def list_classrooms(request):
    classrooms = Classroom.objects.all().order_by('name')
    return render(request, 'scheduler/list_classrooms.html', {'classrooms': classrooms})

# --- Timetable Generation & Main Flat View ---
def generate_timetable_view(request):
    if request.method == "POST":
        generate_weekly_timetable()
        return redirect('timetable')
    return render(request, 'scheduler/generate_timetable.html')

def timetable_view(request):
    entries = TimetableEntry.objects.all().order_by('date', 'classroom__name', 'start_time')
    return render(request, 'scheduler/timetable.html', {'entries': entries})

# --- Boxed Timetable for ALL Classes ---
def timetable_matrix_all_classes(request):
    classrooms = Classroom.objects.all().order_by('name')
    tables = []
    for classroom in classrooms:
        grid = {day: {p[0]: None for p in PERIODS} for day in DAYS}
        entries = TimetableEntry.objects.filter(classroom=classroom)
        for entry in entries:
            for period_label, _ in PERIODS:
                p_start, p_end = period_label.split('-')
                if str(entry.start_time)[:5] == p_start and str(entry.end_time)[:5] == p_end:
                    grid[entry.day_of_week][period_label] = entry
        tables.append({'classroom': classroom, 'grid': grid})
    return render(request, 'scheduler/timetable_matrix_all.html', {
        'tables': tables, 'periods': PERIODS, 'days': DAYS,
    })

# --- (Optional) Boxed Timetable for ONE Class ---
def timetable_matrix_classroom(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    grid = {day: {p[0]: None for p in PERIODS} for day in DAYS}
    entries = TimetableEntry.objects.filter(classroom=classroom)
    for entry in entries:
        for period_label, _ in PERIODS:
            p_start, p_end = period_label.split('-')
            if str(entry.start_time)[:5] == p_start and str(entry.end_time)[:5] == p_end:
                grid[entry.day_of_week][period_label] = entry
    return render(request, 'scheduler/timetable_matrix.html', {
        'grid': grid,
        'classroom': classroom,
        'periods': PERIODS,
        'days': DAYS,
    })
def timetable_by_instructor_boxed(request):
    from .models import Instructor, TimetableEntry, Classroom
    PERIODS = [
        ("08:30-09:30", "P1"),
        ("09:30-10:30", "P2"),
        ("11:00-12:00", "P3"),
        ("12:00-13:00", "P4"),
        ("13:00-14:00", "LUNCH"),
        ("14:00-15:00", "P5"),
        ("15:00-16:00", "P6"),
        ("16:00-17:00", "P7"),
    ]
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    instructors = Instructor.objects.all().order_by('name')
    tables = []
    for instructor in instructors:
        grid = {day: {p[0]: None for p in PERIODS} for day in DAYS}
        entries = TimetableEntry.objects.filter(course__instructor=instructor)
        for entry in entries:
            for period_label, _ in PERIODS:
                p_start, p_end = period_label.split('-')
                if str(entry.start_time)[:5] == p_start and str(entry.end_time)[:5] == p_end:
                    grid[entry.day_of_week][period_label] = entry
        tables.append({'instructor': instructor, 'grid': grid})
    return render(request, 'scheduler/timetable_by_instructor_boxed.html', {
        'tables': tables, 'periods': PERIODS, 'days': DAYS,
    })
