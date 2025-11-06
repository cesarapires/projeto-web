from django import forms

from .models.veiculo import Veiculo
from .models.ordem_servico import OrdemServico


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
        # não expomos o status aqui: será definido pelo backend como "aguardando aprovação"
        fields = ['veiculo', 'km_atendimento', 'observacoes', 'valor_total']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'km_atendimento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quilometragem atendida (opcional)'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações do orçamento'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Valor total'}),
        }
