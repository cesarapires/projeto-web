from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import VeiculoForm
from .models.veiculo import Veiculo
from .models.cliente import Cliente
from .models.ordem_servico import OrdemServico
from django.views.decorators.http import require_POST
from .models.ordem_servico import OrdemServico
from django.views.decorators.http import require_POST


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
            # create Cliente profile for this user
            Cliente.objects.get_or_create(user=user)
            messages.success(request, 'Cadastro realizado com sucesso. Faça login.')
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'site_principal/register.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
    """Dashboard simples listando veículos do cliente."""
    # ensure cliente exists
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    veiculos = cliente.veiculos.all()
    # ordens de serviço relacionadas aos veículos deste cliente
    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente)
    ordens_aguardando = ordens.filter(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    ordens_outros = ordens.exclude(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/dashboard.html', {'veiculos': veiculos, 'ordens_aguardando': ordens_aguardando, 'ordens_outros': ordens_outros})





@login_required(login_url=reverse_lazy('login'))
def veiculo_create(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.cliente = cliente
            veiculo.save()
            messages.success(request, 'Veículo criado com sucesso.')
            return redirect('dashboard')
    else:
        form = VeiculoForm()
    return render(request, 'site_principal/veiculo_form.html', {'form': form, 'create': True})


@login_required(login_url=reverse_lazy('login'))
def veiculo_edit(request, pk):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    veiculo = get_object_or_404(Veiculo, pk=pk, cliente=cliente)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso.')
            return redirect('dashboard')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'site_principal/veiculo_form.html', {'form': form, 'create': False, 'veiculo': veiculo})


@login_required(login_url=reverse_lazy('login'))
def veiculo_delete(request, pk):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    veiculo = get_object_or_404(Veiculo, pk=pk, cliente=cliente)
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo excluído com sucesso.')
        return redirect('dashboard')
    return render(request, 'site_principal/veiculo_confirm_delete.html', {'veiculo': veiculo})


@login_required(login_url=reverse_lazy('login'))
def orcamentos_aguardando(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente, status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/orcamentos_list.html', {'ordens': ordens, 'title': 'Orçamentos aguardando aprovação', 'show_approve': True})


@login_required(login_url=reverse_lazy('login'))
def orcamentos_outros(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente).exclude(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/orcamentos_list.html', {'ordens': ordens, 'title': 'Todos os orçamentos', 'show_approve': False})


@login_required(login_url=reverse_lazy('login'))
@require_POST
def aprovar_orcamento(request, pk):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordem = get_object_or_404(OrdemServico, pk=pk, veiculo__cliente=cliente)
    # só permitir aprovar se estiver aguardando aprovação
    if ordem.status == OrdemServico.STATUS_AGUARDANDO_APROVACAO:
        ordem.status = OrdemServico.STATUS_EM_ANDAMENTO
        ordem.save()
        messages.success(request, f'Orçamento #{ordem.id} aprovado com sucesso.')
    else:
        messages.info(request, 'Ordem não está aguardando aprovação.')
    # redireciona de volta à página anterior ou dashboard
    next_url = request.META.get('HTTP_REFERER') or reverse('dashboard')
    return redirect(next_url)
