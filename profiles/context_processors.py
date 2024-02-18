from .models import Profile

def profile_processor(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = request.user.pk)
    return {'profile':profile}