from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------
    # Home
    # -------------------------------
    path('', views.HomeView.as_view(), name='home'),

    # -------------------------------
    # Patient
    # -------------------------------
    path('patient/', views.PatientDashboardView.as_view(), name='patient_dashboard'),
    path('patient/dashboard/', views.PatientDashboardView.as_view(), name='patient_dashboard'),
    path('consulta/<int:pk>/', views.PatientConsultaDetailView.as_view(), name='consulta_detail'),
    path('medicacoes/', views.PatientMedicacaoListView.as_view(), name='patient_medicacoes'),
    path('exames/', views.PatientExamesListView.as_view(), name='patient_exames'),
    # -------------------------------
    # Doctor
    # -------------------------------
    path('doctor/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctor/consulta/new/', views.ScheduleConsultaView.as_view(), name='schedule_consulta'),
    path('consulta/<int:pk>/edit/', views.UpdateConsultaView.as_view(), name='update_consulta'),

    path('exames/new/', views.CreateExamesView.as_view(), name='create_exames'),
    path('exames/<int:pk>/edit/', views.UpdateExameView.as_view(), name='update_exames'),
    path('exames/item/<int:pk>/edit/', views.UpdateExameResultsView.as_view(), name='update_exame_results'),

    path('medicacao/new/', views.CreateMedicacaoView.as_view(), name='create_medicacao'),
    path('medicacao/<int:pk>/edit/', views.UpdateMedicacaoView.as_view(), name='update_medicacao'),

    #--------------------------------
    #Exams
    #--------------------------------
    path('exames/detail/<int:pk>/', views.ExamesDetailView.as_view(), name='exames_detail'),

    #--------------------------------
    #medications
    #--------------------------------

    path('medicacao/detail/<int:pk>/', views.MedicacaoDetailView.as_view(), name='medicacao_detail'),


    # -------------------------------
    # Administration
    # -------------------------------
    path('administration-panel/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # --- Medico ---
    path('administration/medico/create/', views.CreateMedicoView.as_view(), name='create_medico'),
    path('administration/medico/<int:cc>/edit/', views.UpdateMedicoView.as_view(), name='update_medico'),
    path('administration/medicos/', views.MedicoListView.as_view(), name='list_medicos'),

    # --- Paciente ---
    path('administration/paciente/create/', views.CreatePacienteView.as_view(), name='create_paciente'),
    path('administration/paciente/<int:cc>/edit/', views.UpdatePacienteAdminView.as_view(), name='update_paciente'),
    path('administration/pacientes/', views.PacienteListView.as_view(), name='list_pacientes'),

    path('administration/medicamento/create/', views.CreateMedicamentoView.as_view(), name='create_medicamento'),
    path('administration/medicamento/<str:id_medicamento>/edit/', views.UpdateMedicamentoView.as_view(), name='update_medicamento'),
    path('administration/medicamentos/', views.MedicamentoListView.as_view(), name='list_medicamento'),

    path('administration/exame/create/', views.CreateExameView.as_view(), name='create_exame'),
    path('administration/exame/<int:pk>/edit/', views.UpdateExameView.as_view(), name='update_exame'),
    path('administration/exame/', views.ExameListView.as_view(), name='list_exame'),
]