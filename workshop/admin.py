from django.contrib import admin
from .models import (
    Medico, Paciente, Consulta, MedicoConsulta,
    Receita, Medicamento, Medicacao, ItemMedicacao,
    Exame, Exames, ItemExames
)


# -------------------------------
# Inline Admins
# -------------------------------

class MedicoConsultaInline(admin.TabularInline):
    model = MedicoConsulta
    extra = 1
    fields = ['medico', 'role']


class ItemMedicacaoInline(admin.TabularInline):
    model = ItemMedicacao
    extra = 1
    fields = ['medicamento', 'dose', 'quantidade']


class ItemExamesInline(admin.TabularInline):
    model = ItemExames
    extra = 1
    fields = ['exame', 'resultados']


# -------------------------------
# Main Model Admins
# -------------------------------

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['cc', 'nome', 'numero_medico', 'especialidade', 'email', 'telefone']
    search_fields = ['nome', 'numero_medico', 'especialidade', 'email', 'cc']
    list_filter = ['especialidade']
    ordering = ['nome']
    
    fieldsets = (
        ('Informação Pessoal', {
            'fields': ('cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email')
        }),
        ('Informação Profissional', {
            'fields': ('numero_medico', 'especialidade')
        }),
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['cc', 'nome', 'numero_seguranca_social', 'email', 'telefone', 'data_registo']
    search_fields = ['nome', 'numero_seguranca_social', 'email', 'cc']
    list_filter = ['data_registo']
    ordering = ['nome']
    readonly_fields = ['data_registo']
    
    fieldsets = (
        ('Informação Pessoal', {
            'fields': ('cc', 'nome', 'data_nascimento', 'morada', 'telefone', 'email')
        }),
        ('Informação do Paciente', {
            'fields': ('numero_seguranca_social', 'data_registo')
        }),
    )


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['id', 'paciente', 'data_hora', 'motivo_resumo']
    search_fields = ['paciente__nome', 'motivo']
    list_filter = ['data_hora']
    ordering = ['-data_hora']
    date_hierarchy = 'data_hora'
    
    inlines = [MedicoConsultaInline]
    
    fieldsets = (
        ('Informação da Consulta', {
            'fields': ('paciente', 'data_hora', 'motivo')
        }),
    )
    
    def motivo_resumo(self, obj):
        return obj.motivo[:50] + '...' if len(obj.motivo) > 50 else obj.motivo
    motivo_resumo.short_description = 'Motivo'


@admin.register(MedicoConsulta)
class MedicoConsultaAdmin(admin.ModelAdmin):
    list_display = ['id', 'medico', 'consulta', 'role']
    search_fields = ['medico__nome', 'consulta__paciente__nome']
    list_filter = ['role']


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['id_medicamento', 'nome']
    search_fields = ['nome', 'id_medicamento']
    ordering = ['nome']


@admin.register(Medicacao)
class MedicacaoAdmin(admin.ModelAdmin):
    list_display = ['id_receita', 'paciente', 'date']
    search_fields = ['paciente__nome']
    list_filter = ['date']
    ordering = ['-date']
    date_hierarchy = 'date'
    
    inlines = [ItemMedicacaoInline]
    
    fieldsets = (
        ('Informação da Receita', {
            'fields': ('paciente', 'date')
        }),
    )


@admin.register(ItemMedicacao)
class ItemMedicacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'medicacao', 'medicamento', 'dose', 'quantidade']
    search_fields = ['medicamento__nome', 'medicacao__paciente__nome']
    list_filter = ['medicamento']


@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ['id_exame', 'nome']
    search_fields = ['nome', 'id_exame']
    ordering = ['nome']


@admin.register(Exames)
class ExamesAdmin(admin.ModelAdmin):
    list_display = ['id_receita', 'paciente', 'date']
    search_fields = ['paciente__nome']
    list_filter = ['date']
    ordering = ['-date']
    date_hierarchy = 'date'
    
    inlines = [ItemExamesInline]
    
    fieldsets = (
        ('Informação da Receita de Exames', {
            'fields': ('paciente', 'date')
        }),
    )


@admin.register(ItemExames)
class ItemExamesAdmin(admin.ModelAdmin):
    list_display = ['id', 'exames', 'exame', 'resultados_resumo']
    search_fields = ['exame__nome', 'exames__paciente__nome']
    list_filter = ['exame']
    
    def resultados_resumo(self, obj):
        if obj.resultados:
            return obj.resultados[:50] + '...' if len(obj.resultados) > 50 else obj.resultados
        return '(sem resultados)'
    resultados_resumo.short_description = 'Resultados'


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['id_receita']
    ordering = ['-id_receita']