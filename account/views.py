from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
import random
from.models import UserOTP



# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        password1 = request.POST.get("password")
        password2 = request.POST.get("Confirm_password")

        if not User.objects.filter(username=username).exists():
            if password1 == password2:
                User.objects.create_user(
                    username=username, first_name=name, password=password1
                )
                messages.success(request, "Account created successfully")
                return redirect("login")
            else:
                messages.error(request, "Password does not match")
        else:
            messages.error(request, "Username already exists")

    return render(request, "register.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        user = User.objects.filter(username=username)
        if user:
            subject = 'Password Reset'
            otp = random.randint(1000,9999)
            message = f'Here is your one Time Password - {otp}'
            from_mail = 'ajaisvraj7907@gmail.com'
            to_mail = user.first().email

            try:
                user_otp = UserOTP.objects.get(fk_user = user.first())
                user_otp.otp = otp
                user_otp.save()

            except:
                UserOTP.objects.create(
                    otp = otp,
                    fk_user = user.first()
                )
            
            send_mail(
                subject,
                message,
                from_mail,
                [to_mail],
                fail_silently=False,
            )
            
            return redirect('verify_otp',user.first().id)
       
    else:

        messages.error(request,'The given username dose not exist !')
    return render(request,'forgot.html')


def verify_otp(request,id):

    user=User.objects.get(id=id)

    if request.method == 'POST':
        user_otp = UserOTP.objects.get(fk_user=user)
        submitted_otp = request.POST.get('otp')
        if user_otp.otp == submitted_otp:
            return redirect('password_change',user.id)
        messages.error(request,'Invalid OTP !!')
    return render(request,'otp_verify.html',{'user':User})


def password_change(request,id):
    return render(request,'password_change.html')
