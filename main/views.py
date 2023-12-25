from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegisterForm, PostForm
from .models import Post
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

# Create your views here.

@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            
            
            user_perm = get_user_model().objects.get(id=request.user.id)
            
            if post and (post.author == request.user or user_perm.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id = user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {'posts': posts})
    # return render(request, 'main/home.html', {'badge': badge,'posts': posts})

#############################################
def Customlogout(request):
    logout(request)
    return redirect('login')

#############################################
def CustomSignup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/sign_up.html', {'form': form})  

#############################################

@permission_required('main.add_post', login_url='login')
@login_required(login_url='login')
def CreatePost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'main/create_post.html', {'form':form})