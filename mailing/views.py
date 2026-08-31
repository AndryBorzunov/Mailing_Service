from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import JsonResponse

from mailing.forms import (
    DispatchForm,
    RecipientMailForm,
    MessageForm,
    DispatchModeratorForm,
)
from mailing.models import Dispatch, RecipientMail, Message, Attempt
from mailing.services import (
    get_mailings_from_cache,
    get_mailings_from_cache_owner,
    send_mailing,
)


class MailingSummaryView(ListView):
    template_name = "mailing/summary.html"
    context_object_name = "dispatch"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Собираем статистику
        context["dispatch_count"] = Dispatch.objects.count()
        context["dispatch_active_count"] = Dispatch.objects.filter(
            status="Запущена"
        ).count()
        context["recipient_mails_count"] = RecipientMail.objects.count()

        return context

    def get_queryset(self):
        # Возвращаем пустой queryset, так как основной список не нужен
        return Dispatch.objects.none()


def process_command(request):
    if request.method == "POST":
        command = request.POST.get("command")
        mailing_id = request.POST.get("mailing_id")

        if command == "send_mailing" and mailing_id:
            try:
                mailing_id = int(mailing_id)
                send_mailing(mailing_id)
            except Exception as e:
                print(f"Ошибка: {str(e)}")

    return redirect("mailing:dispatch_list")


def health(request):
    return JsonResponse({"status": "ok", "service": "mailing-service"})


class DispatchListView(LoginRequiredMixin, ListView):
    model = Dispatch

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_stop_dispatch"):
            return get_mailings_from_cache()
        else:
            return get_mailings_from_cache_owner(owner=self.request.user)


class DispatchDetailView(DetailView):
    model = Dispatch

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # пересчет и сохранение статуса
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
        if user.has_perm("mailing.can_stop_dispatch"):
            return DispatchModeratorForm
        raise PermissionDenied


class DispatchDeleteView(DeleteView, LoginRequiredMixin):
    model = Dispatch
    success_url = reverse_lazy("mailing:dispatch_list")

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            return super().form_valid(form)
        raise PermissionDenied


class RecipientMailListView(ListView):
    model = RecipientMail

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_stop_dispatch"):
            return RecipientMail.objects.all()
        else:
            return RecipientMail.objects.filter(owner=self.request.user)


class RecipientMailDetailView(DetailView, LoginRequiredMixin):
    model = RecipientMail


class RecipientMailCreateView(CreateView, LoginRequiredMixin):
    model = RecipientMail
    form_class = RecipientMailForm
    success_url = reverse_lazy("mailing:recipient_mails")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()

        return super().form_valid(form)


class RecipientMailUpdateView(UpdateView, LoginRequiredMixin):
    model = RecipientMail
    form_class = RecipientMailForm
    success_url = reverse_lazy("mailing:recipient_mails")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return RecipientMailForm
        raise PermissionDenied


class RecipientMailDeleteView(DeleteView, LoginRequiredMixin):
    model = RecipientMail
    success_url = reverse_lazy("mailing:dispatch_list")

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            return super().form_valid(form)
        raise PermissionDenied


class MessageListView(ListView, LoginRequiredMixin):
    model = Message

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_stop_dispatch"):
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView, LoginRequiredMixin):
    model = Message


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(DeleteView, LoginRequiredMixin):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            return super().form_valid(form)
        raise PermissionDenied


class AttemptListView(ListView, LoginRequiredMixin):
    model = Attempt

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_stop_dispatch"):
            return Attempt.objects.all()
        else:
            # attempts = Attempt.objects.all()
            mailings = Dispatch.objects.filter(owner=self.request.user)
            return Attempt.objects.filter(mailing__in=mailings)
