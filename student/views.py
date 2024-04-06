from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from professor.models import Professor,Project, Allocation
from .models import Student, Notification
from django.contrib import messages
from django.http import HttpResponse
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
            
#             form.save()
#             return redirect('add_student')  # Redirect to the same page after successful submission
#     else:
#         form = StudentForm()
#     return render(request, 'student/add_student.html', {'form': form})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            student = form.save(commit=False)
            student.user = current_user
            student.save()

            return redirect('student:professors_list')  # Redirect to the professors list page after successful submission
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def professors_list(request):
    professors = Professor.objects.all()
    current_user = request.user  # Assuming the current user is the student
    unseen_notifications_count = Notification.objects.filter(user=current_user, read=False).count()
    return render(request, 'student/professors_list.html', {'professors': professors, 'unseen_notifications_count': unseen_notifications_count})

# def professor_detail(request, professor_id):
#     professor = Professor.objects.get(id=professor_id)
#     projects = Project.objects.filter(professor=professor)
#     return render(request, 'student/professor_detail.html', {'professor': professor, 'projects': projects})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'student/project_detail.html', {'project': project})


from .forms import SendRequestForm  # Import the form for sending the request

def professor_detail(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    projects = Project.objects.filter(professor=professor)
    student = get_object_or_404(Student, user=request.user)  # Assuming 'user' is the ForeignKey to CustomUser in Student model
    request_sent = Allocation.objects.filter(professor=professor, student=student).exists()
    # If you have a form for sending the request, you can instantiate it here
    #send_request_form = SendRequestForm()  # Replace with your actual form class
    if request_sent:
        send_request_form = None  # No form if request has already been sent
        allocation = Allocation.objects.get(professor=professor, student=student)

    else:
        allocation = None
        send_request_form = SendRequestForm()  # Instantiate the form for sending the request
    return render(request, 'student/professor_detail.html', {
        'professor': professor,
        'projects': projects,
        'send_request_form': send_request_form, 
        'allocation': allocation  # Pass the form to the template
    })


# from .forms import SendRequestForm

# def professor_detail(request, professor_id):
#     professor = get_object_or_404(Professor, id=professor_id)
#     projects = Project.objects.filter(professor=professor)
#     student = get_object_or_404(Student, user=request.user)  # Assuming 'user' is the ForeignKey to CustomUser in Student model
#     request_sent = Allocation.objects.filter(professor=professor, student=student).exists()

#     if request_sent:
#         # If a request has already been sent, retrieve the allocation
#         allocation = Allocation.objects.get(professor=professor, student=student)
#         send_request_form = None  # No form if request has already been sent
#     else:
#         # If a request has not been sent, instantiate the send request form
#         allocation = None
#         send_request_form = SendRequestForm()  # Instantiate the form for sending the request

#     return render(request, 'student/professor_detail.html', {
#         'professor': professor,
#         'projects': projects,
#         'send_request_form': send_request_form,  # Pass the form to the template
#         'request_sent': request_sent,
#         'allocation': allocation  # Pass the allocation to the template
#     })


# def professor_detail(request, professor_id):
#     professor = get_object_or_404(Professor, id=professor_id)
#     projects = professor.project_set.all()
    
#     # Check if a request has already been sent by the current user
#     student = get_object_or_404(Student, user=request.user)
#     request_sent = Allocation.objects.filter(professor=professor, student=student).exists()
    
#     # If a request has been sent, retrieve the allocation
#     allocation = Allocation.objects.filter(professor=professor, student=student).first()
    
#     # Conditionally instantiate the form based on the request status
#     if request_sent:
#         send_request_form = None  # No form if request has already been sent
#     else:
#         send_request_form = SendRequestForm()  # Instantiate the form for sending the request

#     context = {
#         'professor': professor,
#         'projects': projects,
#         'send_request_form': send_request_form,
#         'request_sent': request_sent,
#         'allocation': allocation  # Pass the allocation to the template
#     }

#     return render(request, 'student/professor_detail.html', context)


# def send_request(request, professor_id):
#     if request.method == 'POST':
#         # Process the form submission to create an instance in the Allocation model
#         # For example:
#         # Retrieve the professor object
#         professor = Professor.objects.get(id=professor_id)
        
#         # Create an instance in the Allocation model
#         allocation = Allocation.objects.create(professor=professor, student=request.user.student, selected=False)
        
#         # Redirect back to the professor detail page after sending the request
#         return redirect('professor:professor_detail', professor_id=professor_id)
#     else:
#         # Handle the case when the form is accessed via a GET request
#         return redirect('professor:professor_detail', professor_id=professor_id)




def send_request(request, professor_id):
    if request.method == 'POST':
        professor = get_object_or_404(Professor, id=professor_id)
        student = get_object_or_404(Student, user=request.user)
        
        # Create an instance in the Allocation model
        allocation = Allocation.objects.create(professor=professor, student=student, selected=False)
        messages.success(request, 'Your request has been sent successfully!')

        return render(request, 'student/professor_detail.html', {
            'professor': professor,
            'success_message': 'Your request has been sent successfully!'
        })
        # Redirect back to the professor detail page after sending the request
        return redirect('student:professor_detail', professor_id=professor_id)
    else:
        # Handle the case when the form is accessed via a GET request
        return redirect('student:professor_detail', professor_id=professor_id)
   

def send_request_success(request, professor_id):
    # You can customize this view to display a success message or perform other actions after the request is sent
    professor = Professor.objects.get(id=professor_id)
    return render(request, 'professor/send_request_success.html', {'professor': professor})

def notifications(request):
    # Fetch notifications for the current student
    current_user = request.user  # Assuming the current user is the student
    notifications = Notification.objects.filter(user=current_user)
    notifications.update(read=True)
    # Render the notifications in a template
    return render(request, 'student/notifications.html', {'notifications': notifications})