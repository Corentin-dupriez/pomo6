from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse_lazy('profile-edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form) -> HttpResponse:
        result = super().form_valid(form)

        if result.status_code in (302, 303):
            login(self.request, self.object)

        return result