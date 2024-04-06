
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfessorForm, ProjectForm
from .models import Professor, Allocation, SelectedStudent
from student.models import Student ,Notification
from django.core.mail import send_mail

# @login_required(login_url='explo_project:login')
# def professor_details(request):
#     if request.method == 'POST':
#         form = ProfessorForm(request.POST)
#         if form.is_valid():
#             current_user = request.user
#         professor = Professor(user_id=current_user.id)
        
#         if form.is_valid():
#             professor = form.save(commit=False)

#             professor.save()
#             return redirect('professor:professor_details/')  # Redirect to home or another page after details are filled
#     else:
#         form = ProfessorForm()

#     return render(request, 'professor/professor_details.html', {'form': form})


# def professor_details(request):
#     if request.method == 'POST':
#         form = ProfessorForm(request.POST)
#         if form.is_valid():
#             current_user = request.user
#             professor = Professor(user=current_user)
#             professor.name = form.cleaned_data['name']
#             professor.department = form.cleaned_data['department']
#             professor.expertise = form.cleaned_data['expertise']
#             professor.minimum_cgpa = form.cleaned_data['minimum_cgpa']
#             professor.selection_method = form.cleaned_data['selection_method']
#             professor.save()
#             return redirect('professor:student_details')  # Redirect to another page after details are filled
#     else:
#         form = ProfessorForm()

#     return render(request, 'professor/professor_details.html', {'form': form})

def professor_details(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            current_user = request.user
            professor = form.save(commit=False)
            professor.user = current_user
            professor.save()
            return redirect('professor:add_project')  # Redirect to Add Project page
    else:
        form = ProfessorForm()

    return render(request, 'professor/professor_details.html', {'form': form})




from .models import Professor
from django.shortcuts import get_object_or_404

# def add_project(request):
    

#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             professor = get_object_or_404(Professor, user=request.user)
#             project = form.save(commit=False)
#             project.professor = professor
#             project.save()

#             if 'add_another' in request.POST:
#                 return redirect('professor:add_project')  # Redirect to Add Project page to add another project
#             else:
#                 return redirect('professor:student_details')  # Redirect to Student Details page if adding later
#     else:
#         form = ProjectForm()

#     return render(request, 'professor/add_project.html', {'form': form})


from .models import Professor
from django.shortcuts import get_object_or_404

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            professor = get_object_or_404(Professor, user=request.user)
            project = form.save(commit=False)
            project.professor = professor
            project.save()

            if 'add_another' in request.POST:
                return redirect('professor:add_project')  # Redirect to Add Project page to add another project
            else:
                return redirect('professor:student_details', professor_id=professor.id) # Redirect to Student Details page if adding later
    else:
        form = ProjectForm()

    return render(request, 'professor/add_project.html', {'form': form})



# def student_details(request):
#     # Example student data
#     students = [
#         {'name': 'John Doe', 'rollNo': '123', 'cgpa': '3.8', 'interest': 'Computer Science', 'resume': 'john_doe_resume.pdf'},
#         {'name': 'John Doe', 'rollNo': '123', 'cgpa': '3.8', 'interest': 'Computer Science', 'resume': 'john_doe_resume.pdf'},
        
#         # Add more students as needed
#     ]

#     context = {'students': students}
#     return render(request, 'professor/student_details.html', context)

# def student_details(request, professor_id):
#     professor = Professor.objects.get(id=professor_id)
#     allocations = Allocation.objects.filter(professor=professor, selected=True)
#     students_data = []
#     for allocation in allocations:
#         student = allocation.student
#         student_data = {
#             'name': student.name,
#             'branch': student.branch,
#             'cgpa': student.cgpa,
#             'document_url': student.document.url,  # Assuming 'document' is the field for student resume
#             'accept_url': f'/accept/{allocation.id}/',  # URL to accept the student
#             'decline_url': f'/decline/{allocation.id}/',  # URL to decline the student
#         }
#         students_data.append(student_data)

#     context = {
#         'professor': professor,
#         'students_data': students_data,
#     }
#     return render(request, 'professor/student_details.html', context)



def student_details(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    allocations = Allocation.objects.filter(professor=professor, selected=False)
    sort_by = request.GET.get('sort_by')  # Get the sorting option from the query parameters
    if sort_by == 'cgpa':
        allocations = allocations.order_by('-student__cgpa')  # Sort by CGPA in descending order
    # Add additional sorting options as needed
    context = {
        'professor': professor,
        'allocations': allocations,
    }

    if not allocations.exists():
        context['no_allocations'] = True 
    return render(request, 'professor/student_details.html', context)

def accept_request(request, allocation_id):
    allocation = get_object_or_404(Allocation, id=allocation_id)
    allocation.selected = True
    allocation.save()

    selected_student = SelectedStudent(student=allocation.student, professor=allocation.professor)
    selected_student.save()

    # subject = 'Your request has been accepted'
    message = 'Dear {}, your request has been accepted by Professor {}.'.format(allocation.student.name, allocation.professor.name)
    # from_email = 'anita.murmu.cse22@itbhu.ac.in'  # Replace with your email address
    # to_email = allocation.student.email
    # send_mail(subject, message, from_email, [to_email])


    notification = Notification(user=allocation.student.user, message=message)
    notification.save()

    # Redirect to the student details page after accepting the request
    return redirect('professor:student_details', professor_id=allocation.professor.id)

def decline_request(request, allocation_id):
    allocation = get_object_or_404(Allocation, id=allocation_id)
    allocation.delete()  # Delete the allocation to decline the request
    # Redirect to the student details page after declining the request
    return redirect('professor:student_details', professor_id=allocation.professor.id)



# def display_pdf_viewer(request, student_id):
#     # Retrieve the student object from the database
#     student = Student.objects.get(pk=student_id)

#     # Construct the file path using the upload_location function
#     file_path = upload_location(student, student.document.name)

#     # Perform any additional logic needed to display the PDF file
#     # For example, you can render a template with the file_path
#     return render(request, 'pdf_viewer.html', {'file_path': file_path})


# def display_pdf_viewer(request, student_id):
#     # Retrieve the student object from the database
#     student = get_object_or_404(Student, pk=student_id)

#     # Construct the file path using the document field of the student
#     file_path = request.build_absolute_uri(student.document.url)


#     # Perform any additional logic needed to display the PDF file
#     # For example, you can render a template with the file_path
#     return render(request, 'professor/pdf_viewer.html', {'file_path': file_path})


def display_pdf_viewer(request, student_id):
    # Retrieve the student object from the database
    student = get_object_or_404(Student, pk=student_id)

    # Construct the file path using the document field of the student
    file_path = request.build_absolute_uri(student.document.url)

    return render(request, 'professor/pdf_viewer.html', {'file_path': file_path})


def selected_students(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    selected_students = SelectedStudent.objects.filter(professor=professor)

    return render(request, 'professor/selected_students.html', {'professor': professor, 'selected_students': selected_students})