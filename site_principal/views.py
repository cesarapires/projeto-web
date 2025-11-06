from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from functools import wraps

from .forms import VeiculoForm
from .forms import OrdemServicoForm, OrdemServicoCreateForm
from .models.veiculo import Veiculo
from .models.cliente import Cliente
from .models.ordem_servico import OrdemServico
from django.views.decorators.http import require_POST
from .models.ordem_servico import OrdemServico
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'site_principal/index.html')


def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, 'Você saiu com sucesso.')
    return redirect('index')



class NonAdminLoginView(LoginView):
    template_name = 'site_principal/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return self.request.GET.get('next') or '/'
    
    def dispatch(self, request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
                return redirect(reverse('admin_dashboard'))
            return redirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
            return redirect(reverse('admin_dashboard'))
        return redirect(self.get_success_url())


def non_admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
                messages.error(request, 'Esta área é apenas para clientes (não administradores).')
                return redirect('index')
            return view_func(request, *args, **kwargs)

        return redirect('login')

    return _wrapped


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False) and (getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Área administrativa somente para administradores.')
        return redirect('index')

    return _wrapped


@login_required(login_url=reverse_lazy('login'))
@admin_required
def admin_dashboard(request):
    ordens_abertas = OrdemServico.objects.filter(status=OrdemServico.STATUS_ABERTA)
    ordens_andamento = OrdemServico.objects.filter(status=OrdemServico.STATUS_EM_ANDAMENTO)
    ordens_aguardando = OrdemServico.objects.filter(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    ordens_finalizadas = OrdemServico.objects.filter(status=OrdemServico.STATUS_FINALIZADA)

    context = {
        'ordens_abertas': ordens_abertas,
        'ordens_andamento': ordens_andamento,
        'ordens_aguardando': ordens_aguardando,
        'ordens_finalizadas': ordens_finalizadas,
    }
    return render(request, 'site_principal/admin_dashboard.html', context)



@login_required(login_url=reverse_lazy('login'))
@admin_required
def admin_orcamento_create(request):
    if request.method == 'POST':
        form = OrdemServicoCreateForm(request.POST)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.status = OrdemServico.STATUS_AGUARDANDO_APROVACAO
            ordem.save()
            messages.success(request, f'Orçamento criado com sucesso (#{ordem.id}).')
            return redirect('admin_dashboard')
    else:
        form = OrdemServicoCreateForm()
    return render(request, 'site_principal/admin_orcamento_form.html', {'form': form})



@login_required(login_url=reverse_lazy('login'))
@admin_required
def admin_orcamento_detail(request, pk):
    """Retorna um partial HTML com os detalhes da ordem para abrir em modal."""
    ordem = get_object_or_404(OrdemServico, pk=pk)
    return render(request, 'site_principal/admin_orcamento_detail.html', {'ordem': ordem})



@login_required(login_url=reverse_lazy('login'))
@admin_required
def admin_orcamento_edit(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            messages.success(request, f'Orçamento #{ordem.id} atualizado com sucesso.')
            return redirect('admin_dashboard')
    else:
        form = OrdemServicoForm(instance=ordem)
    return render(request, 'site_principal/admin_orcamento_form.html', {'form': form, 'ordem': ordem, 'edit': True})



@login_required(login_url=reverse_lazy('login'))
@admin_required
def admin_orcamento_delete(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        ordem.delete()
        messages.success(request, f'Orçamento #{pk} excluído com sucesso.')
        return redirect('admin_dashboard')
    return render(request, 'site_principal/admin_orcamento_confirm_delete.html', {'ordem': ordem})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_staff = False
            user.is_superuser = False
            user.save()

            Cliente.objects.get_or_create(user=user)
            messages.success(request, 'Cadastro realizado com sucesso. Faça login.')
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'site_principal/register.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
@non_admin_required
def dashboard(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    veiculos = cliente.veiculos.all()

    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente)
    ordens_aguardando = ordens.filter(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    ordens_outros = ordens.exclude(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/dashboard.html', {'veiculos': veiculos, 'ordens_aguardando': ordens_aguardando, 'ordens_outros': ordens_outros})





@login_required(login_url=reverse_lazy('login'))
@non_admin_required
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
@non_admin_required
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
@non_admin_required
def veiculo_delete(request, pk):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    veiculo = get_object_or_404(Veiculo, pk=pk, cliente=cliente)
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo excluído com sucesso.')
        return redirect('dashboard')
    return render(request, 'site_principal/veiculo_confirm_delete.html', {'veiculo': veiculo})


@login_required(login_url=reverse_lazy('login'))
@non_admin_required
def orcamentos_aguardando(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente, status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/orcamentos_list.html', {'ordens': ordens, 'title': 'Orçamentos aguardando aprovação', 'show_approve': True})


@login_required(login_url=reverse_lazy('login'))
@non_admin_required
def orcamentos_outros(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordens = OrdemServico.objects.filter(veiculo__cliente=cliente).exclude(status=OrdemServico.STATUS_AGUARDANDO_APROVACAO)
    return render(request, 'site_principal/orcamentos_list.html', {'ordens': ordens, 'title': 'Todos os orçamentos', 'show_approve': False})


@login_required(login_url=reverse_lazy('login'))
@non_admin_required
@require_POST
def aprovar_orcamento(request, pk):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordem = get_object_or_404(OrdemServico, pk=pk, veiculo__cliente=cliente)

    if ordem.status == OrdemServico.STATUS_AGUARDANDO_APROVACAO:
        ordem.status = OrdemServico.STATUS_EM_ANDAMENTO
        ordem.save()
        messages.success(request, f'Orçamento #{ordem.id} aprovado com sucesso.')
    else:
        messages.info(request, 'Ordem não está aguardando aprovação.')

    next_url = request.META.get('HTTP_REFERER') or reverse('dashboard')
    return redirect(next_url)
