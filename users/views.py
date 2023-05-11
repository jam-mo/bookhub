from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, ChallengeProgressForm
from .decorators import user_not_authenticated



@user_not_authenticated
def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

        print(form.errors)

    return render(
        request=request,
        template_name='register.html',
        context={'form': form}
    )


@login_required
def custom_logout(request):
    logout(request)
    # messages.info(request, "You've successfully logged out!")
    return redirect("index")

@user_not_authenticated #does job of authenticating user
def custom_login(request):


    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Hello! You have been logged in")
                return redirect('index')

        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={'form': form}
    )

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        challenge_progress = ChallengeProgressForm(request.POST, instance=user)

        if challenge_progress.is_valid():
            challenge_progress.save()
            return redirect('users/profile.html')

    else:
        challenge_progress = ChallengeProgressForm(instance=user)

    context = {'user': user,
               'challenge_progress': challenge_progress}

    return render(request, 'users/profile.html', context)

