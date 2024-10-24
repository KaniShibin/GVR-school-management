from django.shortcuts import render
from librarian.models import *
from librarian.forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.views import View
from staff.models import *
from django.contrib.auth.mixins import LoginRequiredMixin


class BookCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = Book
    form_class = BookCreateForm  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('librarian:BookListView')  

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff            
        return context
    

class BookListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = Book
    template_name = 'book_list.html'  
    context_object_name = 'books'  

    def get_queryset(self):
        return Book.objects.all().order_by('title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Book.CATEGORY_CHOICES  
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    
    def post(self, request):
        search_book = request.POST.get('searchbox')
        query = Book.objects.all().order_by('title')
        if search_book:
            query = query.filter(title__icontains=search_book)
        html = render_to_string('book_filter_sorting.html', {'books': query})
        return JsonResponse({'html': html})

    
class BookSearchAutocompleteView(View):
    def get(self, request):
        term = request.GET.get('term', '')
        books = Book.objects.filter(title__icontains=term)
        results = [{'id': book.id, 'title': book.title} for book in books]
        return JsonResponse(results, safe=False)


class BookDeleteView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:LoginView')
    model = Book
    template_name = '/' 
    success_url = reverse_lazy('librarian:BookListView')  
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book successfully deleted.')
        return super().delete(request, *args, **kwargs)


class BookUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = Book
    form_class = BookCreateForm  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('librarian:BookListView') 

    def form_valid(self, form):
        messages.success(self.request, 'Book successfully updated.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class LibraryRecordCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = LibraryRecord
    form_class = LibraryRecordForm
    template_name = 'library_record_form.html'
    success_url = reverse_lazy('librarian:LibraryRecordListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.all()
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    
    def form_valid(self, form):
        form.instance.borrowed_date = timezone.now()
        book_id = form.cleaned_data['book'].id  
        Book.objects.filter(id=book_id).update(available="outofstock")
        return super().form_valid(form)
 

def get_division(request):
    standard = request.GET['standard']
    divisions = Student.objects.filter(standard=standard).values('division').distinct()
    if divisions.exists():
        return render(request, 'get_divsion.html', {'division': divisions})
    else:
        return JsonResponse({'no_divisions': True})
    

def get_student(request):
    standard = request.GET.get('standard') 
    division = request.GET.get('division')
    students = Student.objects.filter(standard=standard, division=division)
    if students.exists():
        return render(request, 'get_student.html', {'students': students})
    else:
        return JsonResponse({'no_student': True})


class LibraryRecordListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = LibraryRecord
    template_name = "libraryrecord_listview.html"
    context_object_name = 'library'

    def get_queryset(self):
        return LibraryRecord.objects.all().order_by('-borrowed_date')
    
    def post(self, request, *args, **kwargs):
        status = request.POST.get('status')
        book_id = request.POST.get('book_id')
        record_id = request.POST.get('record_id')
        if status == "In":
            Book.objects.filter(id=book_id).update(available="instock")
            LibraryRecord.objects.filter(id=record_id).update(lend_date=timezone.now())
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        table_body = render_to_string('library_record_table_body.html', context)
        search_book = request.POST.get('searchbox')
        query= LibraryRecord.objects.all().order_by('-borrowed_date')
        if search_book:
            query = query.filter(book__title__icontains=search_book).exclude(lend_date__isnull=False)
        html = render_to_string('library_records_filter_sorting.html', {'library': query})
        return JsonResponse({'message': 'Status updated', 'table_body': table_body, 'html': html})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    
    
class LibraryRecordSearchAutocompleteView(View):    
    def get(self, request):
        term = request.GET.get('term', '')
        books = Book.objects.filter(title__icontains=term, available="outofstock")
        results = [{'id': book.id, 'title': book.title} for book in books]
        return JsonResponse(results, safe=False)


class LibraryRecordDeleteView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:LoginView')
    model = LibraryRecord
    template_name = '/' 
    success_url = reverse_lazy('librarian:LibraryRecordListView')  
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Library Record successfully deleted.')
        return super().delete(request, *args, **kwargs)

