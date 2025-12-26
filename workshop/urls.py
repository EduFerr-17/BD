from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('patient/', views.PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctor/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('consulta/<int:pk>/', views.PatientConsultaDetailView.as_view(), name='consulta_detail'),
    path('medicacoes/', views.PatientMedicacaoListView.as_view(), name='patient_medicacoes'),
    path('exames/', views.PatientExamesListView.as_view(), name='patient_exames'),
    path('schedule/', views.ScheduleConsultaView.as_view(), name='schedule_consulta'),
    path('create_medicacao/', views.CreateMedicacaoView.as_view(), name='create_medicacao'),
    path('update_exame/<int:pk>/', views.UpdateExameResultsView.as_view(), name='update_exame'),
]