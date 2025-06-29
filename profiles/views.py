from django.shortcuts import render
from django.views.generic import DetailView

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