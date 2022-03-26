from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): # if the form has the reqired fields

            # When using a django form, cleaned data is needed to
            # fetch the value from the request

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0] #the username is the first half of the email address

            user = Account.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect ('register')

    else:
        form = RegistrationForm()
    context = {
        'form':form,
               }


    return render (request, 'accounts/register.html', context)

''' Login view method, if the user logins successfully, take them to their
    dashboard, else request that they attempt to login again, either way
    a message appears, "a succesful login" message or a "failed login" message'''

def login (request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email, password = password) # returns the user object

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect ('dashboard')
        else:
            messages.error(request, "Invalid login credentials") # failed login details
            return redirect ('login')

    return render (request, 'accounts/login.html')


''' Logs out view method, logs the user out,
    displays a logout message, a user can only login
    to the system if the user is logged out '''

@login_required(login_url = 'login')
def logout (request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect ('login')

'''to view the dashboard, a user must be logged in
'''

@login_required(login_url = 'login')
def dashboard (request):
    return render(request, 'accounts/dashboard.html')
