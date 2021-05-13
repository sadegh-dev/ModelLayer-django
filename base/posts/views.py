from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddPostForm, EditPostForm
from django.utils.text import slugify




def all_posts(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'posts/all_posts.html',context)



def post_detail(request, year, month, day, slug):
    the_post = get_object_or_404( Post, created__year = year, created__month = month, created__day = day, slug = slug )
    #way 1
    #comments = Comment.objects.filter(post = the_post, is_reply = False)
    #way 2 - best
    comments = the_post.postcomments.all()

    context = {
        'post' : the_post,
        'comments' : comments
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



@login_required
def edit_post(request, post_id):
    the_post = get_object_or_404(Post, id = post_id)
    if the_post.user.id == request.user.id :
        if request.method == 'POST':
            form = AddPostForm(request.POST, instance= the_post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request, 'your post submitted', 'success')
                return redirect('usermanage:dashboard', request.user.id)
        else:
            form = EditPostForm(instance=the_post)
        context = {
            'form' : form
        }
        return render(request, 'posts/edit_post.html', context)
    else:
        return redirect('posts:all_posts')



@login_required
def delete_post(request, post_id):
    the_post = get_object_or_404(Post, id = post_id)
    if request.user.id == the_post.user.id :
        the_post.delete()
        messages.success(request, 'the post has deleted successfully', 'success')
    return redirect('posts:all_posts')




