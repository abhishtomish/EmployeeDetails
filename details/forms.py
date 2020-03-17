from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from details.models import Employee

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Enter a valid emil address')
    CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    class Meta:
        model = Employee
        fields = ('email', 'username','date_of_birth','gender','dept_name', 'is_nri', 'password1', 'password2')


class AuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ('email', 'password')

    def clean(self):
        email = ''
        password = ''
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")
    
class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Employee
		fields = ('email', 'username')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Employee.objects.exclude(pk=self.instance.pk).get(email=email)
			except Employee.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Employee.objects.exclude(pk=self.instance.pk).get(username=username)
			except Employee.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.' % username)


