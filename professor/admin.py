from django.contrib import admin
from .models import Professor, Project, Allocation, SelectedStudent

admin.site.register(Professor)
admin.site.register(Project)
admin.site.register(Allocation)
admin.site.register(SelectedStudent)