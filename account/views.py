from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        #get form value
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #check password
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"That email is being used")
                    return redirect('register')
                else:
                    #ready to register
                    user = User.objects.create_user(username=username, password=password, email=email,first_name=first_name, last_name=last_name)
                    #login after register
                    # auth.login(request,user)

                    user.save()
                    messages.success(request,'you are now registered you can log in')
                    return redirect('login')
        else:
            messages.error(request,"Password do not match")
            return redirect('register')

    else:
        return render(request,'account/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are successfully login')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')

    else:
        return render(request,'account/login.html')


def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    contex = {
        'contacts':user_contact
    }
    return render(request,'account/dashboard.html',contex)

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,'you are log out')
        return redirect('index')
