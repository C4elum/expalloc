from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from student.models import Student

class Professor(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'), 
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True) 
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    expertise = models.CharField(max_length=255)
    minimum_cgpa = models.FloatField(default=0.0)
    selection_method = models.CharField(
        max_length=20,
        choices=[
            ('CGPA', 'CGPA Basis'),
            ('FCFS', 'First-Come, First-Served'),
        ],
        default='CGPA'
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    max_students = models.PositiveIntegerField(default=5)


    def str(self):
        return self.title

class Allocation(models.Model):
    #project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True, blank=True)
    selected = models.BooleanField(default=False)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} -  {self.professor.name}"

class SelectedStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    selection_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Selected by {self.professor.name}"