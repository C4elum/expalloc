from django.urls import path
from . import views
app_name = 'professor'

from .views import professor_details, add_project

urlpatterns = [
    path('professor_details/', professor_details, name='professor_details'),
    path('add_project/', add_project, name='add_project'),
     path('accept/<int:allocation_id>/', views.accept_request, name='accept_request'),
    path('decline/<int:allocation_id>/', views.decline_request, name='decline_request'),
    path('student_details/<int:professor_id>/', views.student_details, name='student_details'),
    path('view-resume/<int:student_id>/', views.display_pdf_viewer, name='display_pdf_viewer'),
    path('<int:professor_id>/selected_students/', views.selected_students, name='selected_students'),
]