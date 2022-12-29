from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Models start here

def loginUser(request):
    if request.user.is_authenticated:
        user = request.user
        group = None
        if user.groups.exists():
            group = user.groups.all()[0].name
            if group == "Student":
                return redirect('student/home', user)
            if group == "Teacher":
                return redirect('teacher/home', user)
        else:
            return render(request, 'eduware/error_view.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('pass')
        user = authenticate(request, email=username, password=passw)
        if user is not None:
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == "Student":
                    login(request, user)
                    return redirect('student/home', user)
                if group == "Teacher":
                    login(request, user)
                    return redirect('teacher/home', user)
                elif group == None:
                    return render(request, 'eduware/error_view.html')
        else:
            messages.error(request, "Bad credentials")
            return render(request, 'eduware/login.html')
    else:
        return render(request, 'eduware/login.html')

@login_required
def studentLogin(request):
    user = request.user
    group = user.groups.all()[0].name
    if group == "Teacher":
        return redirect('teacher/home', user)
    else:
        s_course = StudentCourse.objects.filter(student_id = user.id)
        return render(request, 'eduware/studenthomepage.html', { 'course_data' : s_course })

@login_required
def teacherLogin(request):
    user = request.user
    group = user.groups.all()[0].name
    if group == "Student":
        return redirect('student/home', user)
    else:
        course_list = Course.objects.filter(teacher_id = user.id)
        return render(request, 'eduware/teacherhomepage.html', {'teacher_course_data' : course_list})

@login_required
def getChallenges(request):
    course = request.GET.get('course')
    course_challenges = Challenge.objects.filter(course_id = course)
    user = request.user
    group = user.groups.all()[0].name
    if group == "Teacher":
        return render(request, 'eduware/view_challenges_t.html', {'challenge_info' : course_challenges})
    elif group == "Student":
        student = User.objects.get(email = request.user)
        student_in_course = StudentCourse.objects.get(student_id = student.id)
        solution = Solution.objects.filter(student_in_course_id = student_in_course.id)
        context = {'challenge_info' : course_challenges, 'solution_info' : solution}
        return render(request, 'eduware/view_challenges_s.html', context)
    else:
        return redirect('Error')


@login_required
def createChallenge(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group =='Teacher':
            if request.POST:
                form = ChallengeCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('Teacher home page')
            form = ChallengeCreationForm(course_id=request.GET.get('course'))
            context = {'form' : form}
            return render(request, 'eduware/create_Challenge.html', context)
        else:
            return redirect('Error')
    else:
        return redirect('Error')


@login_required
def addSolution(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group == 'Student':
            if request.POST:
                form = AddSolutionForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('Student home page')
            student = User.objects.get(email = request.user)
            student_in_course = StudentCourse.objects.get(student_id = student.id)
            form = AddSolutionForm(student_in_course_id=student_in_course.id, challenge_id=request.GET.get('challenge'))
            challenge = Challenge.objects.get(id = request.GET.get('challenge'))
            context = {'form' : form, 'challenge' : challenge}
            return render(request, 'eduware/add_solution.html', context)
        else:
            return redirect('Error')
    else:
        return redirect('Error')
            
@login_required
def getSolutions(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group == 'Student':
            student = User.objects.get(email = request.user)
            student_in_course = StudentCourse.objects.get(student_id = student.id, course_id= request.GET.get('course'))
            solution = Solution.objects.get(student_in_course_id=student_in_course.id, challenge_id=request.GET.get('challenge'))
            context = {'solution_info' : solution}
            return render(request, 'eduware/get_solutions_s.html', context)
        elif group == 'Teacher':
            challenges = Challenge.objects.filter(course_id =  request.GET.get('course'))
            challenge_ids = []
            for i in challenges:
                challenge_ids.append(i.id)
            solutions = Solution.objects.filter(challenge_id__in=challenge_ids)
            context = {'solutions_list' : solutions}
            return render(request, 'eduware/get_solutions_t.html', context)
        else:
            return redirect('Error')

@login_required
def gradeChallenge(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group == 'Teacher':
            if request.POST:
                request_with_points = request.POST.copy()
                request_with_points.update(
                    {'points' : int(request.POST.get('grade'))/10}
                )
                form = gradeSolutionForm(request_with_points)
                if form.is_valid():
                    form.save()
                    return redirect('Teacher home page')
            solution = Solution.objects.get(id=request.GET.get('solution'))
            form = gradeSolutionForm(solution_id=solution.id, challenge_id=solution.challenge_id)
            context = {'grade_form' : form, 'solution_info' : solution}
            return render(request, 'eduware/grade_solution.html', context)
        else:
            return redirect('Error')

@login_required
def getGrades(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group == 'Teacher':
            challenges = Challenge.objects.filter(course_id=request.GET.get('course'))
            challenge_ids = []
            for i in challenges:
                challenge_ids.append(i.id)
            grades = Grade.objects.filter(challenge_id__in=challenge_ids)
            context = {'grade_info' : grades}
            return render(request, 'eduware/get_grades_t.html', context)
        elif group == 'Student':
            student_in_course = StudentCourse.objects.get(course_id = request.GET.get('course'), student_id = user.id)
            solution = Solution.objects.filter(student_in_course_id = student_in_course.id)
            solution_ids = []
            for i in solution:
                solution_ids.append(i.id)
            grades = Grade.objects.filter(solution_id__in = solution_ids)
            context = {'grade_info' : grades}
            return render(request, 'eduware/get_grades_s.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

def error(request):
    return render(request, 'eduware/error_view.html')

