from django.shortcuts import render, redirect
from .models import Post, PostAttachment
from profiles.models import Profile

def home_page(request):
    posts = Post.objects.all()
    for post in posts:
        post.attachments = post.content.all()
    context = {
        'posts':posts,
    }
    return render(request, 'posts/home_page2.html', context)

def post_detail(request, pid):
    post = Post.objects.get(pk = pid)
    post.attachments = post.content.all()
    
    context = {
        'post':post,
    }
    return render(request, 'posts/post_detail2.html', context)

def like_post(request, pfid, pid):
    post = Post.objects.get(pk = pid)
    profile = Profile.objects.get(pk = pfid)
    if not post.likes.contains(profile):
        post.likes.add(profile)
        print(1)
    else:
        post.likes.remove(profile)
        print(-1)
    return redirect('post_detail', pid = pid)


from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def post_new(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        attachments = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Profile.objects.get(user_id = request.user.pk)
            post.save()

            for image in attachments:
                post_att = PostAttachment.objects.create(image = image)
                post.content.add(post_att)
            return redirect('post_detail', pid= post.pk)
    context = {
        'form':form
    }
    return render(request, 'posts/post_new.html', context)

from django.http import Http404

def check_if_user_is_author():
    def decorator(function):
        def wrapper(request,*args, **kwargs):
            try:
                profile = Profile.objects.get(pk = request.user.pk)
                post_author = Post.objects.get(pk = kwargs['pid']).author
                if profile == post_author:
                    return function(request, *args, **kwargs)
                raise Http404
            except:
                return redirect('/')
        return wrapper
    return decorator

@check_if_user_is_author()
def post_edit(request, pid):
    post = Post.objects.get(pk = pid)
    post_att = post.content.all()
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST,instance=post)
        attachments = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            for image in attachments:
                att = PostAttachment.objects.create(image = image)
                post.content.add(att)
            chosen = request.POST.getlist('attachments')
            print(chosen)
            for att_id in chosen:
                PostAttachment.objects.get(pk=int(att_id)).delete()
            return redirect('post_detail', pid= post.pk)
    context = {
        'form':form,
        'post_att':post_att
    }
    return render(request, 'posts/post_edit.html', context)