from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.utils import ErrorList


class CheckRequirementsForm(forms.Form):
    SEX_CHOICES = (
        ('m', 'male'),
        ('f', 'female')
    )

    CEFR = (
        ("A1", "Beginner"),
        ("A2", "Elementary"),
        ("B1", "Intermediate"),
        ("B2", "Upper-Intermediate"),
        ("C1", "Advanced"),
        ("C2", "Proficiency"),
    )
    min = MinValueValidator(18)
    max = MaxValueValidator(80)

    name = forms.CharField(label='name', max_length=100, required=True)
    sex = forms.ChoiceField(label='sex', choices=SEX_CHOICES, initial='m', widget=forms.RadioSelect, required=True)
    age = forms.IntegerField(label='age', validators=[min, max], initial=18, required=True)
    english_level = forms.ChoiceField(label='english level', choices=CEFR)

    def clean(self):
        cleaned_data = super().clean()
        sex = cleaned_data.get('sex')
        age = int(cleaned_data.get('age'))
        level = cleaned_data.get('english_level')

        self.is_fit = (sex == 'm' and age >= 20 and level in ['C1', 'C2']) or \
                      (sex == 'f' and age >= 22 and level in ['B2', 'C1', 'C2'])


class AuthForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Please, try again')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords are different')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} is already in use')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password2 = cleaned_data.get('new_password2')

        if new_password != new_password2:
            raise forms.ValidationError('Passwords are different')


class FindCommentsForm(forms.Form):
    text_to_find = forms.CharField(label='find', max_length=200, required=False)
    in_own = forms.BooleanField(required=False)
