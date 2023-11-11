from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
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
            name=request.POST.get('name')
            email=request.POST.get('email')
            paswd=request.POST.get('password')
            if User.objects.filter(username = name).exists():
                messages.info(request,"Username Already Taken")
                return redirect('reg')
            elif User.objects.filter(email = email).exists():
                 messages.info(request,"Email Already Taken")
                 return redirect('reg')
            else:
                user= User.objects.create(username=name,password=paswd,email=email)
                user.set_password(paswd)
                user.save()
            #authenticating the user
            
            if user is not None:
                request.session['email']=email
                login(request, user)
                return redirect('home')
           
    return render(request,'Register.html')

def Login(request):
    if 'email' in request.session:
        redirect('home')
    if request.method=='POST':
        email = request.POST.get('email')
        paswd = request.POST.get('password')
        
        user = authenticate(email=email,password=paswd)
        if user is not None:
            login(request,user)
            request.session['email']=email
            return redirect('home')
        else:
            messages.error(request,'Invallid credentials')
    return render(request,'Login.html')
