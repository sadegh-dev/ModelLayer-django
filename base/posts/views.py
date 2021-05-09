from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddPostForm
from django.utils.text import slugify




def all_posts(request):
    
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'posts/all_posts.html',context)

def post_detail(request, year, month, day, slug):

    the_post = get_object_or_404( Post, created__year = year, created__month = month, created__day = day, slug = slug )
    context = {
        'post' : the_post
    }

    return render(request,'posts/post_detail.html', context)



@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'your post submitted', 'success')
            return redirect('usermanage:dashboard', request.user.id)
    else :
        form = AddPostForm()
    context = {
        'form' : form ,
    }
    return render(request, 'posts/add_post.html', context) 
