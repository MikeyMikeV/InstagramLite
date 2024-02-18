from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from profiles.models import Profile
from django.templatetags.static import static

# Create your views here.
def create_user(request):
    if request.method != 'POST':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile.objects.create(user = user, tag = user.username)
            profile.profile_pic = 'profile_default.jpg'
            profile.save()
            send_activation_mail(user,request)
            return redirect('/')
    context = {
        'form':form
    }
    return render(request, 'registration/create_user.html',context)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import TokenGenerator

account_activation_token = TokenGenerator()

def send_activation_mail(user,request):
    current_site = get_current_site(request)
    mail_subject = 'Activation link has been sent to your email'
    message = render_to_string(
        'registration/acc_activation_email.html',
        {
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user)
        }
    )
    email = EmailMessage(mail_subject,message, to = [user.email])
    email.send()

from django.contrib.auth.models import User
from django.http import HttpResponse

def activate(request,uid,token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        # user = authenticate(
        #     username = user.username,
        #     password = user.password,
        # )
        # login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalide!')
