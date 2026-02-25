from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import DispatchForm
from mailing.models import Dispatch


class DispatchListView(ListView):
    model = Dispatch


class DispatchDetailView(DetailView):
    model = Dispatch

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        obj.update_status() # пересчет и сохранение статуса
        obj.save()
        return obj


class DispatchCreateView(CreateView, LoginRequiredMixin):
    model = Dispatch
    form_class = DispatchForm
    success_url = reverse_lazy("mailing:dispatch_list")

    def form_valid(self, form):
        dispatch = form.save()
        user = self.request.user
        dispatch.owner = user
        dispatch.update_status()
        dispatch.save()

        return super().form_valid(form)


class DispatchUpdateView(UpdateView, LoginRequiredMixin):
    model = Dispatch
    form_class = DispatchForm
    success_url = reverse_lazy("mailing:dispatch_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return DispatchForm
        raise PermissionDenied


class DispatchDeleteView(DeleteView, LoginRequiredMixin):
    model = Dispatch
    success_url = reverse_lazy("mailing:dispatch_list")

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            return super().form_valid(form)
        raise PermissionDenied
