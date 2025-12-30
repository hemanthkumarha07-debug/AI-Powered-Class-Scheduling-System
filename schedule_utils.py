from scheduler.models import TimetableEntry, Classroom, Course
from datetime import time, datetime, timedelta
import random
from collections import defaultdict

PERIODS = [
    ("08:30-09:30", "P1"),
    ("09:30-10:30", "P2"),
    ("11:00-12:00", "P3"),
    ("12:00-13:00", "P4"),
    ("14:00-15:00", "P5"),
    ("15:00-16:00", "P6"),
    ("16:00-17:00", "P7"),
]
SATURDAY_PERIODS = [("08:30-09:30", "P1"), ("09:30-10:30", "P2")]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def get_week_dates():
    today = datetime.today().date()
    monday = today - timedelta(days=today.weekday())
    week_dates = {}
    for idx, day in enumerate(DAYS):
        week_dates[day] = monday + timedelta(days=idx)
    return week_dates

def generate_weekly_timetable():
    TimetableEntry.objects.all().delete()
    classrooms = list(Classroom.objects.all().order_by('name'))
    week_dates = get_week_dates()
    all_courses = list(Course.objects.all())
    
    print(f"Generating timetable for {len(classrooms)} classrooms and {len(all_courses)} courses...")
    
    for day in DAYS:
        print(f"  Scheduling {day}...")
        
        # Daily tracking - NO SUBJECT REPEATS PER CLASSROOM
        classroom_used_courses = defaultdict(set)      # classroom_id -> used courses TODAY
        classroom_free_slot = {}                       # classroom_id -> free period
        instructor_schedule = defaultdict(list)        # instructor_id -> [(start_time, classroom_id)]
        
        # Assign exactly ONE free slot per classroom (random position)
        day_periods = SATURDAY_PERIODS[:] if day == "Saturday" else PERIODS[:]
        for classroom in classrooms:
            free_periods = day_periods[:]
            random.shuffle(free_periods)
            classroom_free_slot[classroom.id] = free_periods[0]
        
        # Fill REMAINING slots (all except 1 free slot)
        for classroom in classrooms:
            classroom_id = classroom.id
            free_period = classroom_free_slot[classroom_id]
            
            # Available periods = all except free slot
            available_periods = [p for p in day_periods if p != free_period]
            random.shuffle(available_periods)
            
            for period_label, _ in available_periods:
                p_start, p_end = period_label.split('-')
                start_time = time.fromisoformat(p_start)
                end_time = time.fromisoformat(p_end)
                
                # Get UNUSED courses for this classroom today
                unused_courses = [c for c in all_courses if c not in classroom_used_courses[classroom_id]]
                if not unused_courses:
                    continue  # No more unique subjects available
                
                random.shuffle(unused_courses)
                
                for course in unused_courses:
                    instructor_id = course.instructor.id
                    
                    # Check instructor not busy at this exact time (across ALL classrooms)
                    instructor_busy = any(
                        abs((start_time.hour * 60 + start_time.minute) - 
                           (prev_time.hour * 60 + prev_time.minute)) <= 30
                        for prev_time, _ in instructor_schedule[instructor_id]
                    )
                    
                    if instructor_busy:
                        continue
                    
                    # SUCCESS: Schedule (unique subject + instructor available)
                    TimetableEntry.objects.create(
                        classroom=classroom,
                        course=course,
                        day_of_week=day,
                        date=week_dates[day],
                        start_time=start_time,
                        end_time=end_time
                    )
                    
                    # Track usage
                    classroom_used_courses[classroom_id].add(course)
                    instructor_schedule[instructor_id].append((start_time, classroom_id))
                    break  # Next period
        
        print(f"  {day}: {len([c for c in classroom_used_courses.values() if c])} unique subjects scheduled")
    
    print("✅ Timetable generated successfully!")
    print(f"📊 Summary: {len(classrooms)} classrooms, {len(all_courses)} courses")
