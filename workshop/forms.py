from django import forms
from .models import Medico, Paciente, Consulta, Receita

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email', 'numero_medico', 'especialidade']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email', 'numero_seguranca_social']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'data_hora', 'motivo']

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['id_receita']
        