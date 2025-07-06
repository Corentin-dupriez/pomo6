from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from profiles.models import UserProfile


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('profile-edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        result = super().form_valid(form)

        if result.status_code in (302, 303):
            login(self.request, self.object)

        return result