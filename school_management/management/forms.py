from django import forms
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AdminForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), required=True)
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'gender', 'mob', 'profile_pic']
    
    def clean_mob(self):
        mob = self.cleaned_data.get('mob')
        if mob and User.objects.filter(mob=mob).exists():
            raise ValidationError("This mobile number is already in use.")
        return mob


class AdminUpdateForm(forms.ModelForm):

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
