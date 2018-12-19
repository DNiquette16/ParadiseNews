from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout
from accounts.forms import MyRegistrationForm
# Create your views here.

def make_account_view(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect("home")

	else:
		form = MyRegistrationForm()
	return render(request, 'accounts/make-account.html', {'form':form})
def signin_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('profile')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/signin.html', {'form':form})

def logout_view(request):# we need to create a logout button to create a post call
	logout(request) 
	return redirect('home')

'''

<form class = "logout-link" action = "{% url 'accounts:logout'%}" method = "post">
</form>
'''