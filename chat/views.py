from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView

from adverts.models import Advertisement
from chat.models import Thread, Message

class ThreadListView(LoginRequiredMixin, ListView):
    model = Thread
    context_object_name = 'threads'
    paginate_by = 10
    template_name = 'chat/thread-list-page.html'
    login_url = reverse_lazy('login')

    def get_queryset(self) -> QuerySet:
        return Thread.objects.filter(participants=self.request.user).order_by('-created_at')


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'chat/thread-details.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update({'messages': Message.objects.filter(thread=self.get_object())})
        return super().get_context_data(**kwargs)

    def get_object(self, **kwargs):
        return Thread.objects.filter(pk=self.kwargs['pk']).prefetch_related('orders').first()


class ThreadRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        advert = Advertisement.objects.get(pk=self.kwargs['advert_id'])
        chat = Thread.objects.filter(advert_id=advert.pk).filter(participants=self.request.user).first()

        if not chat:
            chat = Thread.objects.create(advert_id=self.kwargs['advert_id'])
            chat.participants.add(self.request.user, advert.user)
            chat.save()

        return reverse_lazy('thread-detail', kwargs={'pk': chat.pk})