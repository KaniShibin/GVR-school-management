from django import forms
from .models import Student, FeeDetails
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
User = get_user_model()

class StudentForm(forms.ModelForm):

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
    
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=3, required=True, validators=[MinLengthValidator(1), MaxLengthValidator(3)],widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll number'}))
    standard = forms.ChoiceField(choices=STANDARD_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    division = forms.ChoiceField(choices=DIVISION_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Student
        fields = ['name',  'gender','roll_number', 'standard', 'division', 'mob', 'profile_pic']

    def clean_mob(self):
        mob = self.cleaned_data.get('mob')
        if mob and Student.objects.filter(mob=mob).exists():
            raise ValidationError("This mobile number is already in use.")
        return mob
    

class StudentUpdateForm(forms.ModelForm):

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
    
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    mob = forms.CharField(max_length=10, required=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    profile_pic = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=3, required=True, validators=[MinLengthValidator(1), MaxLengthValidator(3)], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll number'}))
    standard = forms.ChoiceField(choices=STANDARD_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    division = forms.ChoiceField(choices=DIVISION_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['name', 'gender', 'roll_number', 'standard', 'division', 'mob', 'profile_pic']

    


class FeeForm(forms.ModelForm):
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
    standard = forms.ChoiceField(choices=STANDARD_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    due_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))
    
    class Meta:
        model = FeeDetails
        fields = ['standard', 'amount', 'due_date']
