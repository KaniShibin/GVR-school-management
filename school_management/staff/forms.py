from django import forms
from django.contrib.auth import get_user_model
from .models import Staff
from django.forms import DateInput
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

User = get_user_model()

class StaffForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    ROLE_CHOICES = (
        ('office', 'Office Staff'),
        ('librarian', 'Librarian'),
    )
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),label='Date Joined')
    class Meta:
        model = Staff
        fields = ['username', 'password', 'role', 'name', 'gender','mob', 'profile_pic', 'date_joined']
    def clean_mob(self):
        mob = self.cleaned_data.get('mob')
        if mob and User.objects.filter(mob=mob).exists():
            raise ValidationError("This mobile number is already in use.")
        return mob 
    
class StaffUpdateForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    ROLE_CHOICES = (
        ('office', 'Office Staff'),
        ('librarian', 'Librarian'),
    )
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),label='Date Joined')
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Staff
        fields = ['username', 'name', 'gender','mob', 'profile_pic', 'role', 'date_joined']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['name'].initial = self.instance.user.name
            self.fields['gender'].initial = self.instance.user.gender
            self.fields['role'].initial = self.instance.user.role
            self.fields['mob'].initial = self.instance.user.mob