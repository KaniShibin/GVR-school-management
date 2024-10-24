from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from users.models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator
from staff.models import *
from student.models import Student


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label="Confirm Password")

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', 'New password and Confirm password must match.')
        return cleaned_data


class AdminProfileUpdateForm(forms.ModelForm):

    GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    )

    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'mob', 'profile_pic']


class StaffProfileUpdateForm(forms.ModelForm):

    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
   
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),label='Date Joined')

    class Meta:
        model = Staff
        fields = ['username', 'name', 'gender','mob', 'profile_pic', 'date_joined']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['name'].initial = self.instance.user.name
            self.fields['gender'].initial = self.instance.user.gender
            # self.fields['profile_pic'].initial = self.instance.user.profile_pic
            self.fields['mob'].initial = self.instance.user.mob


class StudentProfileUpdateForm(forms.ModelForm):

    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    STANDARD_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    
    DIVISION_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    )
    
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=3, required=True, validators=[MinLengthValidator(1), MaxLengthValidator(3)], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll number'}))
    standard = forms.ChoiceField(choices=STANDARD_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    division = forms.ChoiceField(choices=DIVISION_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['username', 'name', 'gender', 'roll_number', 'standard', 'division', 'mob', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['name'].initial = self.instance.user.name
            self.fields['gender'].initial = self.instance.user.gender
            self.fields['mob'].initial = self.instance.user.mob
