from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount
from .forms import SignupForm
from .models import CustomUser
from student.models import Student
from professor.models import Professor
from allauth.socialaccount.models import SocialAccount

def home(request):
    return render(request, 'users/home.html')

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             if user.role == CustomUser.ROLE_NONE:
#                 return render(request, 'choose_role.html', {'user_id': user.id})
#             elif user.role == CustomUser.ROLE_STUDENT:
#                 student = Student(user=user)
#                 student.save()
#                 return redirect('student_profile')
#             elif user.role == CustomUser.ROLE_PROFESSOR:
#                 professor = Professor(user=user)
#                 professor.save()
#                 return redirect('professor_profile')
#     else:
#         form = SignupForm()

#     google_account = None
#     if request.user.is_authenticated:
#         google_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        

#     return render(request, 'users/signup.html', {'form': form, 'google_account': google_account})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == CustomUser.ROLE_NONE:
                return render(request, 'choose_role.html', {'user_id': user.id})
            elif user.role == CustomUser.ROLE_STUDENT:
                # student = Student(user=user)
                # student.save()
                return reverse('student:add_student')
            elif user.role == CustomUser.ROLE_PROFESSOR:
                # professor = Professor(user=user)
                # professor.save()
                return reverse('professor:professor_details')
    else:
        form = SignupForm()

    google_account = None
    if request.user.is_authenticated:
        google_account = SocialAccount.objects.filter(user=request.user, provider='google').first()

    return render(request, 'users/signup.html', {'form': form, 'google_account': google_account})

# def choose_role(request, user_id):
#     user = CustomUser.objects.get(id=user_id)
    
#     if request.method == 'POST':
#         role = request.POST.get('role')
#         if role in [CustomUser.ROLE_STUDENT, CustomUser.ROLE_PROFESSOR]:
#             user.role = role
#             user.save()
            
#             if user.role == CustomUser.ROLE_STUDENT:
#                 student = Student(user=user)
#                 student.save()
#                 return redirect('student:student_details')
#             elif user.role == CustomUser.ROLE_PROFESSOR:
#                 professor = Professor(user=user)
#                 professor.save()
#                 return redirect('professor:professor_details')
    
#     return render(request, 'users/choose_role.html', {'user': user})

# def choose_role(request, user_id):
#     user = CustomUser.objects.get(id=user_id)
    
#     if request.method == 'POST':
#         role = request.POST.get('role')
#         if role in [CustomUser.ROLE_STUDENT, CustomUser.ROLE_PROFESSOR]:
#             user.role = role
#             user.save()
            
#             if user.role == CustomUser.ROLE_STUDENT:
#                 # student = Student(user=user)
#                 # student.save()
#                 return reverse('student:add_student')
#             elif user.role == CustomUser.ROLE_PROFESSOR:
#                 # professor = Professor(user=user)
#                 # professor.save()
#                 return reverse('professor:professor_details')
    
#     return render(request, 'users/choose_role.html', {'user': user})


def choose_role(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in [CustomUser.ROLE_STUDENT, CustomUser.ROLE_PROFESSOR]:
            user.role = role
            user.save()
            
            if user.role == CustomUser.ROLE_STUDENT:
                # Redirect to the URL for adding a student
                return redirect('student:add_student')
            elif user.role == CustomUser.ROLE_PROFESSOR:
                # Redirect to the URL for adding professor details
                return redirect('professor:professor_details')
    
    return render(request, 'users/choose_role.html', {'user': user})



# def login_redirect(request):
#     if request.user.is_authenticated:
#         if request.user.role == CustomUser.ROLE_STUDENT:
#             return redirect('student_profile')
#         elif request.user.role == CustomUser.ROLE_PROFESSOR:
#             return redirect('professor_profile')
#     return redirect('home')  # Redirect to a default page if role is not defined

# def student_profile(request):
#     # Logic to retrieve and display student profile
#     return render(request, 'users/student_profile.html')

# def professor_profile(request):
#     # Logic to retrieve and display professor profile
#     return render(request, 'users/professor_profile.html')
