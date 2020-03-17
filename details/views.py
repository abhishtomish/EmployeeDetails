from django.shortcuts import render, redirect
from details.models import Employee
from details.forms import RegistrationForm, AuthenticationForm, AccountUpdateForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()    # if all the data provided are valid it will save the form adding the user to the database.
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            # login(request, account)
            return redirect('login')
        else:
            context['register_form'] = form     # here form is not valid
    else:
        form = RegistrationForm()   # here also form is not valid
    context['register_form'] = form
    return render(request, 'register.html', context)

def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")
    
    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("login")
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email.lower(), password=password)

            if user:
                login(request, user)
                return redirect("login")        
    
    else:
        form = AuthenticationForm()
    
    context['login_form'] = form

    return render(request, 'login.html', context)

def dashboard(request):
    context = {}
    employee = Employee.objects.all()
    context['employee'] = employee
    return render(request, 'dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form = AccountUpdateForm(
				initial= {
					"email": request.user.email,
					"username": request.user.username,
				}
			)
	context['account_form'] = form
	return render(request, 'update.html', context)
