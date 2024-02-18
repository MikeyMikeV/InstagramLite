from django.shortcuts import render
from .models import Profile
from posts.models import Post

def profile_detail(request, uid):
    profile = Profile.objects.get(user_id = uid)
    posts = Post.objects.filter(author_id = profile.pk)
    for post in posts:
        post.attachments = post.content.all()
    context = {
        'profile':profile,
        'posts':posts,
    }
    return render(request,'profiles/detail.html', context)