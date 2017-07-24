from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from rest_framework.authtoken.models import Token


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts_profile')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('accounts_profile')
        else:
            form = UserCreationForm

        return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    api_key = Token.objects.get(user=request.user)

    return render(request, 'accounts/profile.html', {'api_key': api_key})
