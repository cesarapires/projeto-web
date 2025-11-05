from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse


def index(request):
    return render(request, 'site_principal/index.html')


class NonAdminLoginView(LoginView):
    """Login view that blocks admin users (is_staff or is_superuser).

    Uses template `site_principal/login.html`.
    """
    template_name = 'site_principal/login.html'
    # don't auto-redirect authenticated users here; we'll handle them in dispatch
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        """If the user is already authenticated, decide what to do:
        - admins are not allowed and are redirected to index with a message
        - non-admin authenticated users are redirected to the success URL
        - anonymous users are allowed to see the login form
        """
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            # Block admin users from logging in via this page
            if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
                messages.error(request, 'Usuários administradores não podem entrar por esta página.')
                return redirect('index')
            # already-authenticated non-admin -> go to success URL / next
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        # Block admin users from logging in via this page after authentication
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
            messages.error(self.request, 'Usuários administradores não podem entrar por esta página.')
            return redirect('index')
        return super().form_valid(form)

    def get_success_url(self):
        # Respect next param if provided, otherwise go to index
        return self.request.GET.get('next') or '/' 


def register(request):
    """Simple registration view for non-admin users using Django's UserCreationForm.

    After successful registration the user is redirected to the login page with a success message.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # ensure new users are not staff/superuser
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso. Faça login.')
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'site_principal/register.html', {'form': form})
