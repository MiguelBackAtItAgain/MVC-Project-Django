from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('pass')
        user = authenticate(request, email=username, password=passw)
        if user is not None:
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == "Student":
                    login(request, user)
                    return redirect('student/home')
                elif group == "Teacher":
                    login(request, user)
                    return redirect('teacher/home')
            return redirect('home')
        else:
            messages.error(request, "Bad credentials")
            return render(request, 'eduware/login.html')
    else:
        return render(request, 'eduware/login.html')

@login_required
def studentLogin(request):
    return render(request, 'eduware/studenthomepage.html')

@login_required
def teacherLogin(request):
    return render(request, 'eduware/teacherhomepage.html')

@login_required
def logoutUser(request):
    logout(request)
    return render(request, 'eduware/login.html')

