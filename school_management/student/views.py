from django.shortcuts import render, redirect
from student.models import Student, FeeDetails, FeesHistory
from student.forms import StudentForm, StudentUpdateForm, FeeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib import messages
import os
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from staff.models import Staff
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class StudentCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html' 
    success_url = reverse_lazy('student:StudentListView')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff  
        return context
    
    def form_valid(self, form):
        student = form.save(commit=False)
        student.save()          
        fee_details = FeeDetails.objects.filter(standard=student.standard).first()
        if fee_details:  
            feehistory = FeesHistory(
                student=student,  
                amount=fee_details.amount,  
                due_date=fee_details.due_date,  
                status='due'  
            )
            feehistory.save() 
        return super().form_valid(form)


class StudentListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = Student
    template_name = 'student_list.html'  
    context_object_name = 'student_list'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class StudentUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = Student
    form_class = StudentUpdateForm
    template_name = 'student_update.html'
    success_url = reverse_lazy('student:StudentListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    
    def form_valid(self, form):
        unit = form.save(commit=False)
        unit.save()
        messages.success(self.request, 'Updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating.')
        return self.render_to_response(self.get_context_data(form=form))
    

class StudentDeleteView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:LoginView')
    model = Student
    template_name = '/' 
    success_url = reverse_lazy('student:StudentListView')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.profile_pic and os.path.isfile(self.object.profile_pic.path):
            try:
                os.remove(self.object.profile_pic.path)
            except Exception as e:
                messages.error(self.request, f'Error deleting profile picture: {e}')        
        user = getattr(self.object, 'user', None)
        if user:
            user.delete()  
        self.object.delete()
        messages.success(self.request, 'Student and associated user successfully deleted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', self.success_url))


class FeeCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = FeeDetails
    form_class = FeeForm
    template_name = 'fee_create.html'  
    success_url = reverse_lazy('student:FeeDetailsListView') 

    def form_valid(self, form):
        messages.success(self.request, 'Fee details created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the fee details.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class FeeDetailsListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = FeeDetails
    template_name = 'fee_details_list.html'  
    context_object_name = 'fee_details_list' 

    def get_queryset(self):
        return FeeDetails.objects.all() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class FeeDetailsUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = FeeDetails
    form_class = FeeForm  
    template_name = 'fee_details_update.html'  
    success_url = reverse_lazy('student:FeeDetailsListView') 

    def form_valid(self, form):
        messages.success(self.request, 'Updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)  
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    

class FeeHistoryListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = FeesHistory
    template_name = 'fee_history_list.html'  
    context_object_name = 'fee_history_list'  

    def get_queryset(self):
        return FeesHistory.objects.all().order_by('-student__standard')  

    def post(self, request, *args, **kwargs):
        status = request.POST.get('status')
        record_id = request.POST.get('record_id')
        if status == "In":
            FeesHistory.objects.filter(id=record_id).update(status="paid", payment_date=timezone.now())
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        table_body = render_to_string('feeshistory_table_body.html', context)
        return JsonResponse({'message': 'Status updated', 'table_body': table_body})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context