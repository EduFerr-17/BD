from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import (
    Medico, Paciente, Consulta, Receita, Medicacao, ItemMedicacao,
    Exames, ItemExames, Medicamento, Exame
)

# -------------------------------
# Basic Model Forms
# -------------------------------

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            'cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email',
            'numero_medico', 'especialidade'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email',
            'numero_seguranca_social'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'id_medicamento', 'nome', 
        ]

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = [
            'id_exame', 'nome', 
        ]
       

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'data_hora', 'motivo']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = []  # No fields needed, id_receita is auto-generated


# -------------------------------
# Medicacao + ItemMedicacao Forms
# -------------------------------

class MedicacaoForm(ModelForm):
    class Meta:
        model = Medicacao
        fields = ['paciente', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ItemMedicacaoForm(forms.ModelForm):
    class Meta:
        model = ItemMedicacao
        fields = ('medicamento', 'dose', 'quantidade')
        widgets = {
            'dose': forms.TextInput(attrs={'placeholder': 'e.g., 500mg'}),
            'quantidade': forms.NumberInput(attrs={'min': 1}),
        }


# Inline formset for Medicacao -> ItemMedicacao
ItemMedicacaoFormSet = inlineformset_factory(
    Medicacao,
    ItemMedicacao,
    form=ItemMedicacaoForm,
    extra=0,
    can_delete=True,
    min_num=1,  # Require at least 1 medication
    validate_min=True
)


# -------------------------------
# Exames + ItemExames Forms
# -------------------------------

class ExamesForm(ModelForm):
    class Meta:
        model = Exames
        fields = ['paciente', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ItemExamesForm(forms.ModelForm):
    image = forms.ImageField(
        required=False, #permite adicionar sem imagem
        label="Upload de Imagem", #label
        help_text="Adicionar imagem" #formatos
    )
    class Meta:
        model = ItemExames
        fields = ('exame', 'resultados','imagem')
        widgets = {
            'resultados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Resultados do exame...'}),
        }


# Inline formset for Exames -> ItemExames
ItemExamesFormSet = inlineformset_factory(
    Exames,
    ItemExames,
    form=ItemExamesForm,
    extra=0,
    can_delete=True,
    min_num=1, 
    validate_min=True
)



