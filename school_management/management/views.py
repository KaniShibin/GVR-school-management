from django.shortcuts import render, redirect
from django.views.generic import CreateView
from management.forms import *
from django.urls import reverse_lazy
from users.models import User
from django.views.generic import DeleteView, ListView
from django.contrib import messages
import os
from django.core.files.storage import default_storage
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from staff.models import Staff
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class AdminCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = User
    form_class = AdminForm
    template_name = 'admin_form.html'
    success_url = reverse_lazy('management:AdminListView')

    def form_valid(self, form):
        admin = form.save(commit=False)
        admin.set_password(form.cleaned_data['password'])
        admin.role='admin'
        admin.save()
        messages.success(self.request, 'Admin successfully created...')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context


class AdminDeleteView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:LoginView')
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.profile_pic and os.path.isfile(self.object.profile_pic.path):
            os.remove(self.object.profile_pic.path)
        self.object.delete()
        messages.success(self.request, 'Admin successfully deleted...')
        referer = request.META.get('HTTP_REFERER', reverse_lazy('management:AdminListView'))
        return HttpResponseRedirect(referer)
    

class AdminListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = User
    template_name = 'admin_list.html'  
    context_object_name = 'admin'  

    def get_queryset(self):
        return User.objects.filter(role="admin").order_by('-name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
        return context
    

class AdminUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = User
    form_class = AdminUpdateForm  
    template_name = 'admin_update.html'  
    success_url = reverse_lazy('management:AdminListView')  

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