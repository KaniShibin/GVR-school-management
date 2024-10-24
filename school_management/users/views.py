from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.views import View
from users.forms import *
from users.models import User
import os
from django.views.generic.edit import UpdateView
from staff.models import Staff
from student.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin,TemplateView) :
    login_url = reverse_lazy('users:LoginView')
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
            else:
                context['staff'] = None
        return context
    

class LoginView(FormView):
    template_name = 'common/login_page.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('users:HomeView')

    def form_valid(self, form):
        user = form.get_user()
        print("User   ", user)
        login(self.request, user)
        messages.success(self.request, 'Login was successfull...Welcome...')
        return super().form_valid(form)
    

class LogoutView(View) :
    def get(self, request) :
        logout(request)
        return redirect(reverse_lazy('users:IndexView'))
    

class UserChangePasswordView(LoginRequiredMixin,FormView):
    login_url = reverse_lazy('users:LoginView')
    template_name = 'password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:LogoutView')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.user 
        new_password = form.cleaned_data['new_password1']

        user.set_password(new_password)
        user.save()
        logout(self.request)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff   
        return context


class AdminProfileUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = User
    form_class = AdminProfileUpdateForm 
    template_name = 'admin_profile_update.html'  
    success_url = reverse_lazy('users:HomeView')  

    def form_valid(self, form):
        unit = form.save(commit=False)
        if unit.pk:  
            old_instance = User.objects.get(pk=unit.pk)
            if old_instance.profile_pic and old_instance.profile_pic.name != unit.profile_pic.name:
                old_file_path = old_instance.profile_pic.path
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)        
        unit.save()
        messages.success(self.request, 'Updated successfully!')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user     
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class StaffProfileUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = Staff
    form_class = StaffProfileUpdateForm
    template_name = 'staff_profile_update.html'
    success_url = reverse_lazy('users:HomeView')

    def get_object(self, queryset=None):
        return super().get_object(queryset)
    
    def form_valid(self, form):
        unit = form.save(commit=False)
        user = unit.user  
        user.username = form.cleaned_data['username']
        user.mob = form.cleaned_data.get('mob')
        user.gender = form.cleaned_data.get('gender')
        user.name = form.cleaned_data.get('name')
        new_profile_pic = form.cleaned_data.get('profile_pic')
        if new_profile_pic:
            if user.profile_pic:  
                old_file_path = user.profile_pic.path
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)  

            user.profile_pic = new_profile_pic  
        user.save()  
        unit.save()
        messages.success(self.request, 'Updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user      
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    

class AdminLoginView(FormView):
    template_name = 'admin_login_page.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('users:HomeView')

    def form_valid(self, form):
        user = form.get_user()
        if user.role == "admin":
            login(self.request, user)
            messages.success(self.request, 'Login was successful... Welcome...')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    

class LibrarianLoginView(FormView):
    template_name = 'librarian_login_page.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('users:HomeView')

    def form_valid(self, form):
        user = form.get_user()
        if user.role == "librarian":
            login(self.request, user)
            messages.success(self.request, 'Login was successful... Welcome...')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class StaffLoginView(FormView):
    template_name = 'staff_login_page.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('users:HomeView')

    def form_valid(self, form):
        user = form.get_user()
        if user.role == "office":
            login(self.request, user)
            messages.success(self.request, 'Login was successful... Welcome...')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    

class IndexView(TemplateView):
    template_name = "common/index.html"
