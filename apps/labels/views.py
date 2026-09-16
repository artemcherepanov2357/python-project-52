from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label

from django.db.models import ProtectedError
from django.shortcuts import redirect


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully created'))
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully updated'))
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        if self.object.tasks.exists():
            messages.error(self.request, _('Cannot delete label'))
            return redirect('labels:list')
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully deleted'))
        return response