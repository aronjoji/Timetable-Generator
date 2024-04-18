from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Assuming 'home' is a named URL pattern for the homepage.
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login_page.html')
    else:
        # Render the login page.
        return render(request, 'login_page.html')

def home(request):
    userid = request.user
    details = Frequency.objects.filter(user=userid)
    context = {'details':details}
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        teacher_name = request.POST.get('teacher_name')
        frequency = int(request.POST.get('frequency'))

        # Save subject, teacher, and frequency to database
        subject = Subject.objects.create(name=subject_name, user = userid)
        teacher = Teacher.objects.create(name=teacher_name, user = userid)
        Frequency.objects.create(subject=subject, teacher=teacher, frequency=frequency, user = userid)

    return render(request, 'home.html', context)

def register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'user/user_register.html')
        else:
            user = User.objects.create_user(
                username=uname,
                password=passw,
            )
            # Add a success message
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('register')
    else:
        return render(request, "register.html")


from django.shortcuts import render
from .models import Subject, Teacher, Frequency
import random


# def generate_timetable(request):
#     # Get all subjects and teachers
#     subjects = Subject.objects.all()
#     teachers = Teacher.objects.all()
    
#     # Initialize timetable data structure
#     timetable = [[None] * 8 for _ in range(5)]  # 5 days, 8 periods
    
#     # Populate timetable randomly based on available subjects and teachers
#     for day in range(5):
#         for period in range(8):
#             # Randomly select a subject-teacher pair
#             subject_teacher = random.choice(Frequency.objects.all())
#             subject = subject_teacher.subject
#             teacher = subject_teacher.teacher
            
#             # Assign subject and teacher to the timetable slot
#             timetable[day][period] = {'subject': subject.name, 'teacher': teacher.name}
    
#     # Render timetable using template
#     return render(request, 'generate_timetable.html', {'timetable': timetable})


from django.shortcuts import render
from .models import Subject, Teacher, Frequency
import random

# def generate_timetable(request):
#     # Get all subjects and teachers
#     subjects = Subject.objects.all()
#     teachers = Teacher.objects.all()
    
#     # Initialize timetable data structure
#     timetable = [[None] * 8 for _ in range(5)]  # 5 days, 8 periods
    
#     # Create a list of subject-teacher pairs based on their frequencies
#     subject_teacher_pairs = []
#     for subject in subjects:
#         # Get all frequency instances for this subject
#         frequencies = Frequency.objects.filter(subject=subject)
#         for frequency_instance in frequencies:
#             subject_teacher_pairs.extend([(frequency_instance.subject, frequency_instance.teacher)] * frequency_instance.frequency)
    
#     # Shuffle the subject-teacher pairs to randomize placement
#     random.shuffle(subject_teacher_pairs)
    
#     # Populate timetable randomly based on available subject-teacher pairs
#     current_day = 0
#     current_period = 0
#     for subject, teacher in subject_teacher_pairs:
#         # Check if we need to move to the next day
#         if current_period >= 8:
#             current_day += 1
#             current_period = 0
        
#         # Check if we've reached the end of the timetable
#         if current_day >= 5:
#             break
        
#         # Assign subject and teacher to the timetable slot
#         timetable[current_day][current_period] = {'subject': subject.name, 'teacher': teacher.name}
        
#         # Move to the next period
#         current_period += 1
    
#     # Render timetable using template
#     return render(request, 'generate_timetable.html', {'timetable': timetable})



def SignOut(request):
     logout(request)
     return redirect('login_page')


def edit_timetable(request, pk):
    timetable = get_object_or_404(Frequency, pk=pk)
    if request.method == 'POST':
        # Retrieve form data from POST request
        subject_name = request.POST.get('subject_name')
        teacher_name = request.POST.get('teacher_name')
        frequency = request.POST.get('frequency')
        
        # Update related objects (Subject and Teacher)
        timetable.subject.name = subject_name
        timetable.teacher.name = teacher_name
        
        # Update frequency
        timetable.frequency = frequency
        
        # Save the related objects and frequency
        timetable.subject.save()
        timetable.teacher.save()
        timetable.save()
        
        # Redirect to a success URL after successful update
        return redirect('home')
    else:
        context = {'timetable': timetable}
        return render(request, 'edit_timetable.html', context)
    



def delete_tt(request,pk):
    tt = get_object_or_404(Frequency, pk=pk)
    tt.delete() 
    return redirect(home)



import random

def generate_timetable(request):
    userid = request.user.pk
    # Get all subjects and teachers
    subjects = Subject.objects.filter(user=userid)
    teachers = Teacher.objects.filter(user=userid)
    
    # Get the total number of subjects
    total_subjects = len(subjects)
    
    # Define maximum allowed subjects and maximum allowed frequency
    max_subjects = 25  # Maximum number of subjects based on 5 days, 8 periods
    max_frequency = 25  # Maximum frequency based on 5 days
    
    # Check if the total number of subjects exceeds the maximum allowed value
    if total_subjects > max_subjects:
        message = "Can't Generate: Exceeded maximum subjects count."
        return render(request, 'generate_timetable.html', {'message': message})
    
    # Calculate total frequency count
    total_frequency_count = sum(f.frequency for f in Frequency.objects.filter(user=userid))
    
    # Check if the total frequency count exceeds the maximum allowed value
    if total_frequency_count > max_frequency:
        message = "Can't Generate: Exceeded maximum frequency count."
        return render(request, 'generate_timetable.html', {'message': message})
    
    # Initialize timetable data structure
    timetable = [[None] * 5 for _ in range(5)]  # 5 days, 8 periods
    
    # Create a list of subject-teacher pairs based on their frequencies
    subject_teacher_pairs = []
    for subject in subjects:
        # Get all frequency instances for this subject
        frequencies = Frequency.objects.filter(subject=subject, user=userid)
        for frequency_instance in frequencies:
            subject_teacher_pairs.extend([(frequency_instance.subject, frequency_instance.teacher)] * frequency_instance.frequency)
    
    # Shuffle the subject-teacher pairs to randomize placement
    random.shuffle(subject_teacher_pairs)
    
    # Check if the total number of subject-teacher pairs exceeds the capacity of the timetable
    if len(subject_teacher_pairs) > (5 * 5):
        message = "Can't Generate: Exceeded timetable capacity with given subjects and frequencies."
        return render(request, 'generate_timetable.html', {'message': message})
    
    # Populate timetable randomly based on available subject-teacher pairs
    current_day = 0
    current_period = 0
    for subject, teacher in subject_teacher_pairs:
        # Check if we need to move to the next day
        if current_period >= 5:
            current_day += 1
            current_period = 0
        
        # Check if we've reached the end of the timetable
        if current_day >= 5:
            break
        
        # Assign subject and teacher to the timetable slot
        timetable[current_day][current_period] = {'subject': subject.name, 'teacher': teacher.name}
        
        # Move to the next period
        current_period += 1
    
    # Render timetable using template
    return render(request, 'generate_timetable.html', {'timetable': timetable})
