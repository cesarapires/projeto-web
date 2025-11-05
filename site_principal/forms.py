from django import forms

from .models.veiculo import Veiculo


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
