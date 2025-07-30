from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from profiles.forms import ProfileEditForm
from profiles.models import UserProfile

class ProfileView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile-details.html'

    def get_object(self, **kwargs) -> UserProfile:
        return self.model.objects.get(user_id=int(self.kwargs.get('pk')))

class ProfileEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/profile-edit.html'
    form_class = ProfileEditForm

    def test_func(self) -> bool:
        user_profile = self.get_object()
        return user_profile.user == self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})