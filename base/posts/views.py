from django.shortcuts import render, get_object_or_404

from .models import Post

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


