from django import forms
from .models import Denuncia


class DenunciaForm(forms.ModelForm):
    """Formulário público para envio de denúncias com consentimento explícito."""

    # LGPD - Consentimento (Art. 7º, I e Art. 8º) e Finalidade (Art. 6º, I):
    # exige ciência explícita do titular sobre o uso exclusivo para apuração.
    consentimento = forms.BooleanField(
        required=True,
        label='Li e concordo com o tratamento dos dados informados exclusivamente para apuração desta denúncia.',
    )

    class Meta:
        model = Denuncia
        fields = [
            'categoria',
            'empresa_envolvida',
            'data_aproximada',
            'descricao',
            'contato_denunciante',
        ]
        widgets = {
            'data_aproximada': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Descreva o ocorrido sem incluir dados pessoais desnecessários de terceiros.',
                }
            ),
            'empresa_envolvida': forms.TextInput(
                attrs={'placeholder': 'Nome da empresa ou organização envolvida'}
            ),
            'contato_denunciante': forms.TextInput(
                attrs={'placeholder': 'Opcional: e-mail ou telefone (deixe em branco para anonimato)'}
            ),
        }


class ConsultaProtocoloForm(forms.Form):
    """Formulário público para consulta de status apenas pelo número de protocolo."""

    protocolo = forms.CharField(
        max_length=20,
        label='Número do Protocolo',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: DS-A1B2C3D4'}),
    )


class AlterarStatusForm(forms.ModelForm):
    """Formulário restrito ao apurador para atualizar o status da denúncia."""

    class Meta:
        model = Denuncia
        fields = ['status']
