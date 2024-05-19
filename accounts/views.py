from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'registration/login.html'

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('main:dashboard')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'registration/profile.html', {'form': form})