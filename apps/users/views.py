# apps/users/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomUserCreationForm

from django.db.models import ProtectedError


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully registered'))
        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user != self.get_object():
            messages.error(request, _("You don't have permission to change"))
            return redirect('users:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully updated'))
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user != self.get_object():
            messages.error(request, _("You don't have permission to change"))
            return redirect('users:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, _('User successfully deleted'))
            return response
        except ProtectedError:
            messages.error(
                self.request,
                _('Cannot delete user because they are assigned to tasks'),
            )
            return redirect('users:list')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, _('You are logged out'))
        return response