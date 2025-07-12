from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo_app import models
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email_id = request.POST.get('inp')
        pwd = request.POST.get('pwd')
        print(fnm , email_id, pwd)
        my_user = User.objects.create_user(fnm,email_id,pwd)
        my_user.save()
        return redirect('/loginn')

    return render(request,'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm , pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        print(userr)
        if userr is not None:
            print(userr)
            login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/loginn')

    return render(request,'login.html')

def todo(request):
    if request.method=='POST':
        title = request.POST.get('title')
        print(title)
        obj = models.Todoo(title=title,user = request.user)
        obj.save()
        res = models.Todoo.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage',{'res' : res})
    res = models.Todoo.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res' : res})

def edit_todo(request,srno):
    if request.method=='POST':
        title = request.POST.get('title')
        print(title)
        obj = models.Todoo.objects.get(srno=srno)
        print(obj.title,'old')
        obj.title=title
        obj.save()
        return redirect('/todopage')
    obj = models.Todoo.objects.get(srno=srno)
    print(obj.title,'outside')
    return render(request,'edit_todo.html', {'obj': obj})

def delete_todo(request,srno):
    obj = models.Todoo.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('loginn')
