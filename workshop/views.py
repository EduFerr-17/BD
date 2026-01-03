from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, CreateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .models import Paciente, Medico, Consulta, Medicacao, ItemMedicacao, Exames, ItemExames, Medicamento, Exame
from .forms import (
    MedicacaoForm, ItemMedicacaoFormSet,
    ExamesForm, ItemExamesFormSet,
    ConsultaForm, MedicoForm, PacienteForm, MedicamentoForm, ExameForm
)

# -------------------------------
# Home View
# -------------------------------
class HomeView(TemplateView):
    template_name = 'home.html'


# -------------------------------
# Patient Views
# -------------------------------



class PatientDashboardView(View):
    template_name = 'patient_dashboard.html'
    
    def get(self, request):
        # Get all patients for the dropdown
        pacientes = Paciente.objects.all().order_by('nome')
        
        # Get selected patient ID from query parameter
        patient_cc = request.GET.get('patient_cc')  # Changed from patient_id
        
        context = {
            'pacientes': pacientes,
            'selected_patient': None,
            'consultas': [],
            'medicacoes': [],
            'exames': []
        }
        
        if patient_cc:
            # Get the selected patient using cc field
            try:
                selected_patient = Paciente.objects.get(cc=patient_cc)
            except Paciente.DoesNotExist:
                selected_patient = None
                # You might want to add an error message here
            
            if selected_patient:
                # Filter data by selected patient
                consultas = Consulta.objects.filter(paciente=selected_patient)
                medicacoes = Medicacao.objects.filter(paciente=selected_patient)
                exames = Exames.objects.filter(paciente=selected_patient)
                
                context.update({
                    'selected_patient': selected_patient,
                    'consultas': consultas,
                    'medicacoes': medicacoes,
                    'exames': exames
                })
        
        return render(request, self.template_name, context)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get selected patient from query parameter
        patient_cc = self.request.GET.get('patient_cc')
        selected_patient = None
        
        if patient_cc:
            try:
                selected_patient = Paciente.objects.get(cc=patient_cc)
                
                # Get counts for selected patient
                context['consultas_count'] = Consulta.objects.filter(paciente=selected_patient).count()
                context['medicacoes_count'] = Medicacao.objects.filter(paciente=selected_patient).count()
                context['exames_count'] = Exames.objects.filter(paciente=selected_patient).count()
                
                # Get recent consultations (last 5)
                context['recent_consultas'] = Consulta.objects.filter(
                    paciente=selected_patient
                ).order_by('-data_hora')[:5]
                
            except Paciente.DoesNotExist:
                pass
        
        # Get general statistics for empty state
        context['total_patients'] = Paciente.objects.count()
        
        # Get today's consultations count
        today = date.today()
        context['recent_consultas_total'] = Consulta.objects.filter(
            data_hora__date=today
        ).count()
        
        context['selected_patient'] = selected_patient
        
        return context


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
        formset = ItemMedicacaoFormSet(queryset=ItemMedicacao.objects.none())
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset
        })

    def post(self, request):
        form = MedicacaoForm(request.POST)
        formset = ItemMedicacaoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            medicacao = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.medicacao = medicacao
                item.save()
            formset.save_m2m()  # Save many-to-many relationships
            return redirect('doctor_dashboard')
        
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset
        })


class UpdateMedicacaoView(View):
    template_name = 'update_medicacao.html'

    def get(self, request, pk):
        medicacao = get_object_or_404(Medicacao, pk=pk)
        form = MedicacaoForm(instance=medicacao)
        formset = ItemMedicacaoFormSet(instance=medicacao)
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset, 
            'medicacao': medicacao
        })

    def post(self, request, pk):
        medicacao = get_object_or_404(Medicacao, pk=pk)
        form = MedicacaoForm(request.POST, instance=medicacao)
        formset = ItemMedicacaoFormSet(request.POST, instance=medicacao)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('doctor_dashboard')
        
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset, 
            'medicacao': medicacao
        })


# -------------------------------
# Exames Views
# -------------------------------
class CreateExamesView(View):
    template_name = 'create_exames.html'

    def get(self, request):
        form = ExamesForm()
        formset = ItemExamesFormSet(queryset=ItemExames.objects.none())
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset
        })

    def post(self, request):
        form = ExamesForm(request.POST)
        formset = ItemExamesFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            exames = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.exames = exames
                item.save()
            formset.save_m2m()
            return redirect('doctor_dashboard')
        
        return render(request, self.template_name, {
            'form': form, 
            'formset': formset
        })


class UpdateExameView(View):
    template_name = 'update_exames.html'

    def get(self, request, pk):
        exame_obj = get_object_or_404(Exames, pk=pk)
        form = ExamesForm(instance=exame_obj)
        formset = ItemExamesFormSet(instance=exame_obj)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'exame_obj': exame_obj
        })

    def post(self, request, pk):
        exame_obj = get_object_or_404(Exames, pk=pk)
        form = ExamesForm(request.POST, instance=exame_obj)
        formset = ItemExamesFormSet(request.POST, instance=exame_obj)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('doctor_dashboard')
        
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'exame_obj': exame_obj
        })


class UpdateExameResultsView(UpdateView):
    model = ItemExames
    template_name = 'update_exame_results.html'
    fields = ['resultados']
    success_url = reverse_lazy('doctor_dashboard')
    context_object_name = 'item_exame'

class ExamesDetailView(DetailView):
    model = Exames
    template_name = 'exames_detail.html'
    context_object_name = 'exame'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all exam items for this Exames instance
        exam_items = ItemExames.objects.filter(exames=self.object)
        context['exam_items'] = exam_items
        return context

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


class CreateMedicamentoView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'create_medicamento.html'
    success_url = reverse_lazy('admin_dashboard')

class UpdateMedicamentoView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'update_medicamento.html'
    pk_url_kwarg = 'id_medicamento'
    success_url = reverse_lazy('admin_dashboard')
    context_object_name = 'medicamento'

class CreateExameView(CreateView):
    model = Exame
    form_class = ExameForm
    template_name = 'create_exame.html'
    success_url = reverse_lazy('admin_dashboard')

class UpdateExameView(UpdateView):
    model = Exame
    form_class = ExameForm
    template_name = 'update_exame.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('admin_dashboard')
    context_object_name = 'exame'


class MedicoListView(ListView):
    model = Medico
    template_name = 'list_medicos.html'
    context_object_name = 'medicos'


class PacienteListView(ListView):
    model = Paciente
    template_name = 'list_pacientes.html'
    context_object_name = 'pacientes'


class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'list_medicamentos.html'
    context_object_name = 'medicamentos'

class ExameListView(ListView):
    model = Exame
    template_name = 'list_exame.html'
    context_object_name = 'exame'