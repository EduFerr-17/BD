from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .models import Paciente, Medico, Consulta, Medicacao, ItemMedicacao, Exames, ItemExames
from .forms import (
    MedicacaoForm, ItemMedicacaoFormSet,
    ExamesForm, ItemExamesFormSet,
    ConsultaForm, MedicoForm, PacienteForm
)

# -------------------------------
# Home View
# -------------------------------
class HomeView(TemplateView):
    template_name = 'home.html'


# -------------------------------
# Patient Views
# -------------------------------
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
    context_object_name = 'consulta'


class PatientMedicacaoListView(ListView):
    model = Medicacao
    template_name = 'patient_medicacoes.html'
    context_object_name = 'medicacoes'


class PatientExamesListView(ListView):
    model = Exames
    template_name = 'patient_exames.html'
    context_object_name = 'exames'


# -------------------------------
# Doctor Views
# -------------------------------
class DoctorDashboardView(ListView):
    model = Paciente
    template_name = 'doctor_dashboard.html'
    context_object_name = 'pacientes'


class ScheduleConsultaView(View):
    template_name = 'schedule_consulta.html'

    def get(self, request):
        form = ConsultaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
        return render(request, self.template_name, {'form': form})


# -------------------------------
# Medicacao Views
# -------------------------------
class CreateMedicacaoView(View):
    template_name = 'create_medicacao.html'

    def get(self, request):
        form = MedicacaoForm()
        formset = ItemMedicacaoFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request):
        form = MedicacaoForm(request.POST)
        formset = ItemMedicacaoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            medicacao = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.medicacao = medicacao
                item.save()
            return redirect('doctor_dashboard')
        return render(request, self.template_name, {'form': form, 'formset': formset})


class UpdateMedicacaoView(View):
    template_name = 'update_medicacao.html'

    def get(self, request, pk):
        medicacao = get_object_or_404(Medicacao, pk=pk)
        form = MedicacaoForm(instance=medicacao)
        formset = ItemMedicacaoFormSet(instance=medicacao)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'medicacao': medicacao})

    def post(self, request, pk):
        medicacao = get_object_or_404(Medicacao, pk=pk)
        form = MedicacaoForm(request.POST, instance=medicacao)
        formset = ItemMedicacaoFormSet(request.POST, instance=medicacao)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('doctor_dashboard')
        return render(request, self.template_name, {'form': form, 'formset': formset, 'medicacao': medicacao})


# -------------------------------
# Exames Views
# -------------------------------
class CreateExameView(View):
    template_name = 'create_exame.html'

    def get(self, request):
        form = ExamesForm()
        formset = ItemExamesFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request):
        form = ExamesForm(request.POST)
        formset = ItemExamesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            exames = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.exames = exames
                item.save()
            return redirect('doctor_dashboard')
        return render(request, self.template_name, {'form': form, 'formset': formset})


class UpdateExameResultsView(UpdateView):
    model = ItemExames
    template_name = 'update_exame_results.html'
    fields = ['resultados']
    success_url = reverse_lazy('doctor_dashboard')
    context_object_name = 'item_exame'


# -------------------------------
# Update Consulta
# -------------------------------
class UpdateConsultaView(UpdateView):
    model = Consulta
    template_name = 'update_consulta.html'
    fields = ['data_hora', 'motivo']
    success_url = reverse_lazy('doctor_dashboard')
    context_object_name = 'consulta'


# -------------------------------
# Administration Views
# -------------------------------
class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard.html'


class CreateMedicoView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'create_medico.html'
    success_url = reverse_lazy('admin_dashboard')


class UpdateMedicoView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'update_medico.html'
    pk_url_kwarg = 'cc'
    success_url = reverse_lazy('admin_dashboard')
    context_object_name = 'medico'


class CreatePacienteView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'create_paciente.html'
    success_url = reverse_lazy('admin_dashboard')


class UpdatePacienteAdminView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'update_paciente.html'
    pk_url_kwarg = 'cc'
    success_url = reverse_lazy('admin_dashboard')
    context_object_name = 'paciente'


class MedicoListView(ListView):
    model = Medico
    template_name = 'list_medicos.html'
    context_object_name = 'medicos'


class PacienteListView(ListView):
    model = Paciente
    template_name = 'list_pacientes.html'
    context_object_name = 'pacientes'