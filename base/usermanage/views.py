from django.shortcuts import render , redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from .models import Profile, Relation
from random import randint

#pip install kavenegar
#from kavenegar import *




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

    is_following = False
    relation = Relation.objects.filter(from_user = request.user , to_user = user)
    if relation.exists():
        is_following = True

    context = {
        'user': user ,
        'posts' : posts,
        'is_following' : is_following
    }
    return render(request, 'usermanage/dashboard.html', context)



@login_required
def edit_profile(request):
    the_user = get_object_or_404(User, id = request.user.id )
    if request.method == 'POST' :
        form = EditProfileForm(request.POST, instance=the_user.profile)
        if form.is_valid():
            form.save()
            the_user.email = form.cleaned_data['email']
            the_user.save()
            messages.success(request, 'you Edit Profile seccessfully', 'success')
            return redirect('usermanage:dashboard', the_user.id)
    else :
        form = EditProfileForm(instance=the_user.profile, initial={'email': request.user.email})
    context = {
        'form' : form
    }
    return render(request,'usermanage/edit_profile.html',context)



def phone_login(request):
    if request.method == 'POST' :
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = f'0{form.cleaned_data["phone"]}'
            rand_num = randint(1000,9999)
            # kavenegar
            """
            api = KavenegarAPI('55555')
            params = {
                'sender' : '' ,
                'receptor' : phone ,
                'message' : rand_num
            }
            api.sms_send(params)
            """
            #test and print in Terminal
            print(rand_num)

            return redirect('usermanage:verify', phone, rand_num )
    else :
        form = PhoneLoginForm()
    context = {
        'form' : form
    }
    return render(request, 'usermanage/phone_login.html', context)



# Verify Phone Login
def verify(request, phone, rand_num):
    if request.method == 'POST' :
        form = VerifyCodeForm(request.POST)
        if form.is_valid() :
            if rand_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone= phone)
                user = get_object_or_404(User, profile = profile)
                login(request, user)
                messages.success(request,'logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'your code is wrong', 'warning')
    else : 
        form = VerifyCodeForm()
    context = {
        'form' : form
    }
    return render(request, 'usermanage/verify.html', context)



def follow(request):
    pass



def unfollow(request):
    pass





