from django import forms

from .models.veiculo import Veiculo
from .models.ordem_servico import OrdemServico
from .models.peca import Peca
from .models.servico_executado import ServicoExecutado


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'marca', 'ano', 'km_atual', 'renavam', 'chassi', 'cor', 'observacoes']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC-1234'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo do veículo'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca/ fabricante'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ano'}),
            'km_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quilometragem atual'}),
            'renavam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RENAVAM'}),
            'chassi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chassi'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cor'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações (opcional)'}),
        }


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        # Form usado para edição/uso administrativo — inclui status
        fields = ['veiculo', 'km_atendimento', 'observacoes', 'valor_total', 'status']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'km_atendimento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quilometragem atendida (opcional)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações do orçamento'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Valor total'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class OrdemServicoCreateForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        # usado para criação via admin_dashboard — não expõe status ao criar
        fields = ['veiculo', 'km_atendimento', 'observacoes', 'valor_total']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'km_atendimento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quilometragem atendida (opcional)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações do orçamento'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Valor total'}),
        }


class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['nome', 'codigo', 'fabricante', 'preco_unitario', 'estoque_atual']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da peça'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código interno or OEM'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabricante'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade disponível'}),
        }


class ServicoExecutadoForm(forms.ModelForm):
    class Meta:
        model = ServicoExecutado
        fields = ['descricao', 'funcionario_id', 'valor', 'duracao_estimada_horas', 'data_execucao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do serviço'}),
            'funcionario_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ID do funcionário (opcional)'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'duracao_estimada_horas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Horas estimadas'}),
            'data_execucao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
