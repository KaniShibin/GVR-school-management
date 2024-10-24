from django import forms
from users.models import User
from librarian.models import *
from student.models import Student


class BookCreateForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category']


class LibraryRecordForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Select Student")
    book = forms.ModelChoiceField(queryset=Book.objects.filter(available='instock'), empty_label="Select Book")

    class Meta:
        model = LibraryRecord
        fields = ['student', 'book']

