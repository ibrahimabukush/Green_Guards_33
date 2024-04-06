from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,LoginForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Contact,Feedback
def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email.endswith('@org.il'):
                form.save()
                return redirect('login')  
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.email.endswith('@org.il'):
                    return redirect('municipality')
                else:
                    return redirect('blog-home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('login')
    else:
        form = LoginForm(request)
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile if hasattr(request.user, 'profile') else None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if profile:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        else:
            p_form = ProfileUpdateForm(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            if profile:
                p_form.save()
            else:
                profile = p_form.save(commit=False)
                profile.user = request.user
                profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if profile:
            p_form = ProfileUpdateForm(instance=profile)
        else:
            p_form = ProfileUpdateForm()

    # Check if the email domain ends with 'org.il'
    if request.user.email.endswith('@org.il'):
        return render(request, 'users/municipality_profile.html', {'u_form': u_form, 'p_form': p_form})

    context = {
        'u_form': u_form, 
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        report = request.POST.get('report')
        data=Contact(name=name,email=email,report=report)
        data.save()
        messages.success(request, 'Thank you for contacting us! We appreciate your interest in our environmental initiatives.')
        return redirect('contact')  
    return render(request, 'users/contact.html')


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        stars = request.POST.get('stars')
        text = request.POST.get('text')
        stars = int(stars)
        data = Feedback(name=name, stars=stars, text=text)
        data.save()
        messages.success(request, 'Thank you for sharing your thoughts with us! We truly appreciate your feedback.')
        return redirect('feedback')  
    return render(request, 'users/feedback.html')