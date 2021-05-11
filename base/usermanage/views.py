from django.shortcuts import render , redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post



def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None :
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect('posts:all_posts')
            else :
                messages.error(request, 'wrong username or password', 'error')     
    else :
        form = UserLoginForm()
    context = {
        'form' : form
    }
    return render(request, 'usermanage/login.html', context)



def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],cd['email'],cd['password'])
            login(request, user)
            messages.success(request, 'you registered successfully', 'success')
            return redirect('posts:all_posts')
    else:
        form = UserRegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'usermanage/register.html', context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'you logout seccessfully', 'success')
    return redirect('posts:all_posts')



def user_dashboard(request, user_id):
    user = get_object_or_404(User, id = user_id)
    posts = Post.objects.filter(user = user) 
    context = {
        'user': user ,
        'posts' : posts
    }
    return render(request, 'usermanage/dashboard.html', context)







