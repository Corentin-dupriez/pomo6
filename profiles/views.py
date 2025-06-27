from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def register_view(request):
    return render(request, template_name='registration/register.html')