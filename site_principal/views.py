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
from .forms import PecaForm
from .forms import ServicoExecutadoForm
from .forms import PecaUtilizadaForm
from .models.veiculo import Veiculo
from .models.cliente import Cliente
from .models.ordem_servico import OrdemServico
from .models.peca import Peca
from .models.servico_executado import ServicoExecutado
from .models.peca_utilizada import PecaUtilizada
from django.db import transaction
from decimal import Decimal
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
    # Permite renderizar a versão completa passando ?full=1 na querystring
    full = str(request.GET.get('full', '')).lower() in ('1', 'true', 'yes')
    context = {'ordem': ordem, 'standalone': full}
    return render(request, 'site_principal/admin_orcamento_detail.html', context)



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

@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_list(request):
    pecas = Peca.objects.all()
    return render(request, 'site_principal/admin_peca_list.html', {'pecas': pecas})

@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_create(request):
    if request.method == 'POST':
        form = PecaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Peça criada com sucesso.')
            return redirect('peca_list')
    else:
        form = PecaForm()
    return render(request, 'site_principal/admin_peca_form.html', {'form': form, 'create': True})

@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_edit(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == 'POST':
        form = PecaForm(request.POST, instance=peca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Peça atualizada com sucesso.')
            return redirect('peca_list')
    else:
        form = PecaForm(instance=peca)
    return render(request, 'site_principal/admin_peca_form.html', {'form': form, 'create': False, 'peca': peca})

@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_delete(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == 'POST':
        peca.delete()
        messages.success(request, 'Peça excluída com sucesso.')
        return redirect('peca_list')
    return render(request, 'site_principal/admin_peca_confirm_delete.html', {'peca': peca})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def servico_create(request, ordem_pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    if request.method == 'POST':
        form = ServicoExecutadoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.ordem_servico = ordem
            with transaction.atomic():
                servico.save()
                # recalcula o total a partir das linhas relacionadas para evitar erros de arredondamento
                ordem.recalculate_valor_total()
            messages.success(request, 'Serviço adicionado com sucesso à ordem.')
            # Redireciona para o admin_dashboard e solicita que o front abra o modal da ordem criada
            from django.urls import reverse
            dashboard_url = reverse('admin_dashboard')
            return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    else:
        form = ServicoExecutadoForm()
    return render(request, 'site_principal/admin_servico_form.html', {'form': form, 'ordem': ordem, 'create': True})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_utilizada_create(request, ordem_pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    if request.method == 'POST':
        form = PecaUtilizadaForm(request.POST)
        if form.is_valid():
            peca_uso = form.save(commit=False)
            peca_uso.ordem_servico = ordem
            # if valor_unitario not provided, default from peca
            if not peca_uso.valor_unitario or peca_uso.valor_unitario == Decimal('0.00'):
                peca_uso.valor_unitario = peca_uso.peca.preco_unitario
            with transaction.atomic():
                peca_uso.save()
                # recalcula o total a partir dos serviços e peças relacionados
                ordem.recalculate_valor_total()
            messages.success(request, 'Peça adicionada com sucesso à ordem.')
            from django.urls import reverse
            dashboard_url = reverse('admin_dashboard')
            return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    else:
        form = PecaUtilizadaForm()
    # passar lista de peças (id -> preco_unitario) para o template preencher o valor automaticamente
    pecas_list = list(Peca.objects.values('id', 'preco_unitario'))
    return render(request, 'site_principal/admin_peca_utilizada_form.html', {'form': form, 'ordem': ordem, 'create': True, 'pecas_list': pecas_list})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_utilizada_edit(request, ordem_pk, pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    peca_uso = get_object_or_404(PecaUtilizada, pk=pk, ordem_servico=ordem)
    if request.method == 'POST':
        form = PecaUtilizadaForm(request.POST, instance=peca_uso)
        if form.is_valid():
            old_total = peca_uso.valor_total or Decimal('0.00')
            peca_new = form.save(commit=False)
            # ensure valor_unitario fallback
            if not peca_new.valor_unitario or peca_new.valor_unitario == Decimal('0.00'):
                peca_new.valor_unitario = peca_new.peca.preco_unitario
            # compute new total via model.save
            with transaction.atomic():
                peca_new.save()
                ordem.recalculate_valor_total()
            messages.success(request, 'Peça atualizada com sucesso.')
            from django.urls import reverse
            dashboard_url = reverse('admin_dashboard')
            return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    else:
        form = PecaUtilizadaForm(instance=peca_uso)
    pecas_list = list(Peca.objects.values('id', 'preco_unitario'))
    return render(request, 'site_principal/admin_peca_utilizada_form.html', {'form': form, 'ordem': ordem, 'create': False, 'peca_uso': peca_uso, 'pecas_list': pecas_list})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def peca_utilizada_delete(request, ordem_pk, pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    peca_uso = get_object_or_404(PecaUtilizada, pk=pk, ordem_servico=ordem)
    if request.method == 'POST':
        with transaction.atomic():
            peca_uso.delete()
            ordem.recalculate_valor_total()
        messages.success(request, 'Peça removida com sucesso.')
        from django.urls import reverse
        dashboard_url = reverse('admin_dashboard')
        return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    return render(request, 'site_principal/admin_peca_utilizada_confirm_delete.html', {'peca_uso': peca_uso, 'ordem': ordem})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def servico_edit(request, ordem_pk, pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    servico = get_object_or_404(ServicoExecutado, pk=pk, ordem_servico=ordem)
    if request.method == 'POST':
        form = ServicoExecutadoForm(request.POST, instance=servico)
        if form.is_valid():
            servico_new = form.save(commit=False)
            with transaction.atomic():
                servico_new.save()
                # recalcula o total depois da alteração
                ordem.recalculate_valor_total()
            messages.success(request, 'Serviço atualizado com sucesso.')
            from django.urls import reverse
            dashboard_url = reverse('admin_dashboard')
            return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    else:
        form = ServicoExecutadoForm(instance=servico)
    return render(request, 'site_principal/admin_servico_form.html', {'form': form, 'ordem': ordem, 'create': False, 'servico': servico})


@login_required(login_url=reverse_lazy('login'))
@admin_required
def servico_delete(request, ordem_pk, pk):
    ordem = get_object_or_404(OrdemServico, pk=ordem_pk)
    servico = get_object_or_404(ServicoExecutado, pk=pk, ordem_servico=ordem)
    if request.method == 'POST':
        with transaction.atomic():
            servico.delete()
            # recalcula total após remoção
            ordem.recalculate_valor_total()
        messages.success(request, 'Serviço excluído com sucesso.')
        from django.urls import reverse
        dashboard_url = reverse('admin_dashboard')
        return redirect(f"{dashboard_url}?open_order={ordem.pk}")
    return render(request, 'site_principal/admin_servico_confirm_delete.html', {'servico': servico, 'ordem': ordem})

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
def cliente_orcamento_detail(request, pk):
    """Partial usado no modal do cliente: mostra detalhes da ordem e serviços executados (somente leitura)."""
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    ordem = get_object_or_404(OrdemServico, pk=pk, veiculo__cliente=cliente)
    return render(request, 'site_principal/cliente_orcamento_detail.html', {'ordem': ordem})





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
