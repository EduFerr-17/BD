from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Paciente, Medico, Consulta, Medicacao, Exames, ItemExames, MedicoConsulta
from django import forms

# Home View

class HomeView(TemplateView):
    template_name = 'home.html'

# Patient Views

class PatientDashboardView(ListView):
    model = Consulta
    template_name = 'patient_dashboard.html'
    context_object_name = 'consultas'

    def get_queryset(self):
        return Consulta.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicacoes'] = Medicacao.objects.all()
        context['exames'] = Exames.objects.all()
        return context

class PatientConsultaDetailView(DetailView):
    model = Consulta
    template_name = 'consulta_detail.html'

class PatientMedicacaoListView(ListView):
    model = Medicacao
    template_name = 'patient_medicacoes.html'
    context_object_name = 'medicacoes'

class PatientExamesListView(ListView):
    model = Exames
    template_name = 'patient_exames.html'
    context_object_name = 'exames'

# Doctor Views

class DoctorDashboardView(ListView):
    model = Paciente
    template_name = 'doctor_dashboard.html'
    context_object_name = 'pacientes'

class ScheduleConsultaView(CreateView):
    model = Consulta
    template_name = 'schedule_consulta.html'
    fields = ['paciente', 'data_hora', 'motivo']
    success_url = reverse_lazy('doctor_dashboard')

    def form_valid(self, form):
        consulta = form.save()
        # For simplicity, no medico assigned
        return super().form_valid(form)

class CreateMedicacaoView(CreateView):
    model = Medicacao
    template_name = 'create_medicacao.html'
    fields = ['paciente', 'date']
    success_url = reverse_lazy('doctor_dashboard')

class UpdateExameResultsView(UpdateView):
    model = ItemExames
    template_name = 'update_exame_results.html'
    fields = ['resultados']
    success_url = reverse_lazy('doctor_dashboard')

# Create your views here.
