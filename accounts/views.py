from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from profiles.models import UserProfile


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        UserProfile.objects.create(
            user = self.object,
            description= 'There is no description yet.'
        )
        return response