from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib import messages

# Create your views here.
@login_required(login_url='log')
def Home(request):
    return render(request,'home.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def Register(request):
    if 'email' in request.session:
        redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            paswd=request.POST.get('password')
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Already Taken")
                return redirect('reg')
            else:
                user= User.objects.create(username=username,password=paswd)
                user.set_password(paswd)
                user.save()
            #authenticating the user
            
            if user is not None:
                request.session['username']=username
                login(request, user)
                return redirect('home')
           
    return render(request,'Register.html')

def Login(request):
    if 'email' in request.session:
        redirect('home')
    if request.method=='POST':
        username = request.POST.get('username')
        paswd = request.POST.get('password')
        
        user = authenticate(username=username,password=paswd)
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invallid credentials')
    return render(request,'Login.html')

def Logout(request):
    if 'username' in request.session:
        del request.session['username']
        logout(request)
    return redirect('log')