from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from collections import Counter
from .forms import *
import pandas as pd

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
        student_in_course = StudentCourse.objects.get(student_id = student.id, course_id=course)
        solution = Solution.objects.filter(student_in_course_id = student_in_course.id)
        challenge_ids = [challenge.id for challenge in course_challenges]
        completed_solutions = Solution.objects.filter(student_in_course_id = student_in_course.id, challenge_id__in = challenge_ids)
        completed_challenges_ids = [solution.challenge_id for solution in completed_solutions]
        context = {'challenge_info' : course_challenges, 'solution_info' : solution, 'completed_challenges': completed_challenges_ids}
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
            challenge_ids = [challenge.id for challenge in challenges]
            solutions = Solution.objects.filter(challenge_id__in=challenge_ids)
            solutions_ids = [solution.id for solution in solutions]
            grades = Grade.objects.filter(solution_id__in=solutions_ids)
            graded_students = [grade.solution.student_in_course.student.id for grade in grades]
            context = {'solutions_list' : solutions, 'graded_students': graded_students}
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
def calculateDecils(request):
    user = request.user
    if user.groups.exists():
        group = user.groups.all()[0].name
        if group == 'Teacher':
            # The solutions for a challenge are recovered and the ids are saved in a list for getting the grades
            solutions = Solution.objects.filter(challenge_id = request.GET.get('challenge'))
            if len(solutions) < 10:
                return redirect('decilsErrorView')
            challenge = Challenge.objects.get(id = request.GET.get('challenge'))
            solution_ids = []
            for i in solutions:
                solution_ids.append(i.id)
                
            #The grades are obtained based on the recovered solutions. A list of ranges is created for the dataframe
            #and the grades are saved to a list
            grades = Grade.objects.filter(solution_id__in = solution_ids)
            grades_list = []
            ranges = [range(0, 11, 1), range(10, 21, 1), range(20, 31, 1), range(30, 41, 1), range(40, 51, 1),
                      range(50, 61, 1), range(60, 71, 1), range(70, 81, 1), range(80, 91, 1), range(90, 101, 1)]
            for i in grades:
                grades_list.append(i.grade)

            # To find how many times the grades are repeated, we make use of the counter function from python and 
            # define two external lists for separating the grades and the frequence the grades were repeated without losing 
            # the order.
            counter = Counter(grades_list)
            internal_grade_list = []
            internal_occurrences_list = []
            for i in range(10, 101, 10):
                internal_grade_list.append(i)
                if counter.get(i) == None:
                    internal_occurrences_list.append(0)
                else:
                    internal_occurrences_list.append(counter.get(i))

            # The dataframe is created and an extra column is created for the cumulative frequence.
            dframe = pd.DataFrame({ 'ranges' : ranges,
                                    'grades' : internal_grade_list,
                                    'f' :  internal_occurrences_list})
            dframe['F'] = dframe['f'].cumsum()
            print(dframe)

            # The cumulative sum is separated in a list to evaluate the nine positions for the decils.
            # The positions are calculated with the folowing formula: kn/10
            # k = number of decil/positions
            # n = Sum of all frequencies 
            cumsum_list = list(dframe['F'])
            positions = []
            for i in range(1, 10, 1):
                positions.append((i * sum(internal_occurrences_list))/10)
            
            # The decils are calculated going through the positions previously calculated and seeing if they
            # are between two values of the cumulative frequence. If the condition is satisfied, the rows of each
            # position are extracted to get the correspondent data that will be used to calculate each decil,
            # the formula used for this is the following:
            # decil(position) = Inferior limit (second row) + 
            # amplitude * (position - prev cumulative freq value(prev)/actual cumulative freq value - prev).
            decils = []
            for i in positions:
                for j in range(0, 9, 1):
                    if cumsum_list[j] <= i < cumsum_list[j+1]:
                        first_row = dframe.iloc[j]
                        second_row = dframe.iloc[j+1]
                        amplitude = int(10)
                        fi_min_1 = int(first_row.F)
                        fi = int(second_row.F)
                        Li = int(second_row.ranges[0])
                        decil = 0
                        decil = Li + amplitude * (i - fi_min_1)/(fi - fi_min_1)
                        decils.append(decil)
            students_in_decils = []
            for i in grades:
                if i.grade > decils[-1]:
                    students_in_decils.append(f"{i.solution.student_in_course.student.name + ' is in centil 10'}")
                elif i.grade < decils[0]:
                    students_in_decils.append(f"{i.solution.student_in_course.student.name + ' is in centil 1'}")
                else:
                    for j in range(0, 9, 1):
                        if decils[j] <= i.grade < decils[j+1]:
                            students_in_decils.append(f"{i.solution.student_in_course.student.name + ' is in centil ' + str(j+2) }")
            students_in_decils = pd.DataFrame({'student_location' : students_in_decils,
                                'grades' : grades_list
                                })
            divisions = []
            i =0
            while len(divisions) != 9:
                if i == 0:
                   divisions.append(f"{str(0) + ' - ' + str(decils[i])}")
                   divisions.append(f"{str(decils[i]) + ' - ' + str(decils[i+1])}")
                else:
                   divisions.append(f"{str(decils[i]) + ' - ' + str(decils[i+1])}")
                i = i+1
            divisions.append(f"{str(decils[-1]) + ' - ' + str(100)}")
            print(students_in_decils)

            context ={'challenge_info' : challenge,
                      'frequences_dataframe' : dframe,
                      'decil_divisions' : divisions,
                      'students_decils' : students_in_decils}
            return render(request, 'eduware/calculate_decils.html', context)
        else:
            return redirect('Error')

@login_required
def decilsErrorView(request):
    return render(request, 'eduware/data_error.html')

@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

def error(request):
    return render(request, 'eduware/error_view.html')

