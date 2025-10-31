from django.shortcuts import render

# Create your views here.
def profile_view(request):
    profile = request.user.profile
    print(profile)
    return render(request, 'profile.html', {'profile':profile})
