from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddPostForm


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
        pass
    else :
        form = AddPostForm()
    context = {
        'form' : form
    }
    return render(request, 'posts/add_post.html', context) 



"""
        form = AddPostForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None :
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('posts:all_posts')
            else :
                messages.error(request, 'wrong username or password', 'error')   
    """