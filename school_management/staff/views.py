from django.shortcuts import render, get_object_or_404 , redirect

from staff.models import *
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from staff.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
import os
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class StaffListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('users:LoginView')
    model = Staff
    template_name = 'staff_list.html'  # Path to your list template
    context_object_name = 'staff_list'  # Name of the context variable
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            # if user.role == "librarian":
            #     librarian = Student.objects.filter(user=user).first()
            #     context['librarian'] = librarian
            #     context['staff'] = None
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
                # context['librarian'] = None
        # else:
        #     context['student'] = 0
        #     context['staff'] = 0
            
        return context


# class StaffUpdateView(UpdateView):
#     model = Staff
#     form_class = StaffForm  # Assuming you have a StaffForm
#     template_name = 'staff_form.html'  # Path to your form template
#     success_url = reverse_lazy('staff-list')  # Redirect to the staff list after updating

#     def get_object(self):
#         return get_object_or_404(Staff, pk=self.kwargs['pk'])  # Get the staff member by primary key
    

class StaffCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('users:LoginView')
    model = Staff
    form_class = StaffForm
    template_name = 'staff_form.html'
    success_url = reverse_lazy('staff:StaffListView')

    def form_valid(self, form):
        user = User(
            username=form.cleaned_data['username'],
            mob=form.cleaned_data.get('mob'),
            role= form.cleaned_data.get('role'),  # Set the user's role if needed
            profile_pic=form.cleaned_data.get('profile_pic'),
            name = form.cleaned_data.get('name'),
            gender = form.cleaned_data.get('gender')
        )
        user.set_password(form.cleaned_data['password'])  # Set the password
        user.save()  # Save the user instance

        # Create staff instance
        staff = form.save(commit=False)
        staff.user = user
        staff.save()

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            # if user.role == "librarian":
            #     librarian = Student.objects.filter(user=user).first()
            #     context['librarian'] = librarian
            #     context['staff'] = None
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
                # context['librarian'] = None
        # else:
        #     context['student'] = 0
        #     context['staff'] = 0
            
        return context
    

class StaffUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:LoginView')
    model = Staff
    form_class = StaffUpdateForm
    template_name = 'staff_update.html'
    success_url = reverse_lazy('staff:StaffListView')
    def get_object(self, queryset=None):
        return super().get_object(queryset)
    def form_valid(self, form):
        unit = form.save(commit=False)

        # Update user profile
        user = unit.user  # Access the associated User instance
        user.username = form.cleaned_data['username']
        user.mob = form.cleaned_data.get('mob')
        user.role = form.cleaned_data.get('role')
        user.gender = form.cleaned_data.get('gender')
        user.name = form.cleaned_data.get('name')

        # Handle profile picture deletion if changed
        # Handle profile picture update
        new_profile_pic = form.cleaned_data.get('profile_pic')
        if new_profile_pic:
            # Check if there's an existing profile picture to delete
            if user.profile_pic:  # Access the profile_pic from the User instance
                old_file_path = user.profile_pic.path
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)  # Delete the old profile picture

            user.profile_pic = new_profile_pic  # Update to the new profile picture

        user.save()  # Save the updated User instance

        # Save the staff instance
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
            # if user.role == "librarian":
            #     librarian = Student.objects.filter(user=user).first()
            #     context['librarian'] = librarian
            #     context['staff'] = None
            if user.role != "staff":
                staff = Staff.objects.filter(user=user).first()
                context['staff'] = staff
                # context['librarian'] = None
        # else:
        #     context['student'] = 0
        #     context['staff'] = 0
            
        return context
    
class StaffDeleteView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:LoginView')
    model = Staff
    template_name = '/'  # Template for confirmation page
    success_url = reverse_lazy('staff:StaffListView')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Attempt to delete the profile picture if it exists
        if self.object.user.profile_pic and os.path.isfile(self.object.user.profile_pic.path):
            try:
                os.remove(self.object.user.profile_pic.path)
            except Exception as e:
                messages.error(self.request, f'Error deleting profile picture: {e}')
        
        # Save the user instance to delete later
        user = self.object.user

        # Delete the staff instance
        self.object.delete()

        # Now delete the associated user instance
        user.delete()
        messages.success(self.request, 'Staff member successfully deleted.')

        # Redirect back to the referring page or a default view
        referer = request.META.get('HTTP_REFERER', self.success_url)
        return HttpResponseRedirect(referer)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['staff'] = self.object
    #     return context