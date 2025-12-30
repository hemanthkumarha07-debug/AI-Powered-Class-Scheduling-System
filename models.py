from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    # Add other relevant fields (ex: email, department)

class Course(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=45)  # Duration in minutes
  # class duration (hours)

class Classroom(models.Model):
    name = models.CharField(max_length=30)

class TimetableEntry(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    date = models.DateField()  # Now includes the date
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_type = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return f"{self.course.name} in {self.classroom.name} ({self.day_of_week} {self.start_time}-{self.end_time})"
