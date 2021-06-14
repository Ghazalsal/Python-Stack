from django.shortcuts import redirect, render, HttpResponse
from wall_app.models import User,Message,Comment
from django.contrib import messages
import bcrypt

def index(request):
    if 'user' in request.session:
        return redirect('/success')
    return render(request,'index.html')

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        conf_password = request.POST['conf_password']
        if password == conf_password:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user= User.objects.create(first_name=first_name,last_name=last_name,email=email, password=pw_hash)
            if 'user' not in request.session:
                request.session['user']=user.id
                request.session['first_name']= first_name
                request.session['last_name']=last_name
                
            messages.success(request, "Registration/Login successfully updated")
            return redirect('/success')
        else:
            return redirect('/')

def login(request):
    if request.method=="POST":
        users = User.objects.get(email=request.POST['email'])
        errors={}
        if users:
            if 'user' not in request.session:
                request.session['user']=users.id
                request.session['first_name']= users.first_name
                request.session['password']=users.last_name
        if users:
            if bcrypt.checkpw(request.POST['password'].encode(), users.password.encode()):
                    return redirect('/success')
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

def welcome(request):
    if 'user' in request.session:
        contet={
            'first_name':request.session['first_name'],
            'message': Message.objects.all(),
            'comment':Comment.objects.all(),
        }
        return render(request,'welcome.html',contet)

def logout(request):
    if 'user' in request.session:
        request.session.clear()
    return redirect('/')



def post_msg(request):
    if request.method=='POST':
        message=Message.objects.create(message_text=request.POST['message_text'],
            user = User.objects.get(id=request.session['user']))
    return redirect('/success')

def post_comm(request,id):
    if request.method=='POST':
        comment=Comment.objects.create(comment_text=request.POST['comment_text'],
            user = User.objects.get(id=request.session['user']), message=Message.objects.get(id=id))
        
    return redirect('/success')