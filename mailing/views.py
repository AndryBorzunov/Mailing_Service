from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from mailing.forms import DispatchForm
from mailing.models import Dispatch


class DispatchListView(ListView):
    model = Dispatch


class DispatchDetailView(DetailView):
    model = Dispatch


class DispatchCreateView(CreateView):
    model = Dispatch
    form_class = DispatchForm
    success_url = reverse_lazy("mailing:dispatch_list")

    def form_valid(self, form):
        dispatch = form.save()
        user = self.request.user
        dispatch.owner = user
        dispatch.save()

        return super().form_valid(form)



#def mailing_list(request):
#    mailings = Dispatch.objects.all()
#    print(mailings)
#    context = { "mailings": mailings }
#    return render(request, 'dispatch_list.html', context)

