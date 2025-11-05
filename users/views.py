from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.urls import reverse
# from allauth.account.utils import se
from allauth.account.models import EmailAddress

# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')
    return render(request, 'users/profile.html', {'profile':profile})

@login_required
def profile_edit_view(request):
    form = ProflileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProflileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'users/profile_edit.html', {'form': form, 'onboarding': onboarding})

@login_required
def profile_settings_view(request):
    return render(request, 'users/profile_settings.html')

@login_required
def profile_email_change(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            # check if it exists
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} already exists!")
                return redirect('profile-settings')

            form.save()
            send_email_confirmation(request, email)
            return redirect('profile-settings')
        else:
            messages.warning(request, "form is not valid")
            return redirect('profile-settings')

    return redirect('home')

def send_email_confirmation(request, email):
    email_obj, created = EmailAddress.objects.get_or_create(
        user=request.user,
        email=email,
        defaults={'primary': True}
    )

    # Mark it unverified (in case user changed email)
    email_obj.verified = False
    email_obj.save()

    # Send confirmation email
    email_obj.send_confirmation(request)

@login_required
def profile_email_verify(request):
    send_email_confirmation(request, request.user.email)
    return redirect('profile-settings')

def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, how sad...(no)')
        return redirect('home')

    return render(request, 'users/profile_delete.html')

