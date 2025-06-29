from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from profiles.forms import ProfileEditForm
from profiles.models import UserProfile


# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def register_view(request):
    return render(request, template_name='registration/register.html')

class ProfileView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile-details.html'

    def get_object(self, **kwargs):
        return self.model.objects.get(user_id=int(self.kwargs.get('pk')))

class ProfileEditView(UpdateView):
    model = UserProfile
    template_name = 'profiles/profile-edit.html'
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})