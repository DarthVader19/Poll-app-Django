from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Poll,User
from .form import CreatePollForm
from .register import CreateUser
import datetime
# Create your views here.

def  home_view(request,*args,**kwargs):
    print(request,args,kwargs)
    return  HttpResponse( "<h1>Hello World</h1>")


def register(request,*args,**kwargs):
    print(request.POST)
    user=''
    if request.method=="POST":
        user=CreateUser(request.POST)
        print(user.is_valid(),user.errors.as_data())
        if user.is_valid():
            user.save()
            # Poll.objects.create(name=request.POST['name'],question='sample question for poll',option_one='one',option_two='two',option_three='three')
            
            print("user saved")
            return redirect('login')

    return render(request,'register.html',{})

def login(request,*args,**kwargs):
    print(request.POST)
    user='anonymous'
    msg=''
    if request.method=="POST":
        mail=request.POST['email']
        pass_=request.POST['password']
        try:
          user=User.objects.get(email=mail)
          if user.email ==mail and user.password==pass_:
                return redirect('home',user.name)
          else:
             raise Exception("user does not exist")
        except:
             msg='Incorrect information. Retry!'
   
    
    context={
        'user':user,
        'err':msg
    }

    return render(request,'login.html',context )


def profile(request,user_name):
    user =User.objects.get(name=user_name)
    try:
        polls = Poll.objects.filter(name=user_name)
    except:
        polls= [{"question":'Polls Not available'}]
    context={
        'user':user,
        'polls':polls,
        'userName':user_name,
    }
    return render(request,'profile.html',context)


def home(request,user_name,**kwargs):
    allpolls = Poll.objects.exclude(name=user_name)
    
    print(user_name)
    try:
        # print(user.__str__())
        polls=Poll.objects.filter(name=user_name)
        user_polls=polls
    except:
        polls=Poll.objects.all()[0]
        user_polls =polls
    
    context={
        "mytext":"the text",
        # "polls":polls,
        'userName':user_name,
        "polls":user_polls,
        "allpolls":allpolls,

           }
    
    return  render(request,'home.html',context)

def create(request,user_name,**kwargs):
    form=CreatePollForm()
    print(request)
    if request.method=="POST":
        data=request.POST.copy()
        data['name']=user_name
        form =CreatePollForm(data)
        # data=form.cleaned_data['question']
        
        if form.is_valid():
            form.save()
            print(data)
            return redirect('home',user_name)
    context={
       'form':form,
       'userName':user_name
    }
    
    return render(request,'create.html',context)

def delete(request,pollid):
    poll = Poll.objects.get(pk=pollid)
    then=poll.time()
    now =datetime.datetime.now()
    duration = now - then.replace(tzinfo=None) 
    diff=divmod(duration.total_seconds(),3600)[0]
    print(diff)
    if diff<=24:  
      poll.delete()
      print('deleted')
    else :
        print('not deleted')
    
    return redirect('home',poll.name)


def vote(request,pollid,user_name):
    poll = Poll.objects.get(pk=pollid)
    if request.method=='POST':
       option=request.POST['poll']
       if option =='option1':
          poll.option_one_count+=1
       if option =='option2':
          poll.option_two_count+=1
       if option =='option3':
          poll.option_three_count+=1
       if option =='option4':
          poll.option_four_count+=1
       poll.save()
       return redirect('results',poll.id,user_name)
    context={
        "mytext":"the text",
        "poll":poll,
        "userName":user_name,
        }
    
    return  render(request,'vote.html',context)

def results(request,pollid,user_name):
    poll= Poll.objects.get(pk=pollid)
    context={
        "poll":poll,
        "userName":user_name
        }
    
    return  render(request,'results.html',context)
