from django.db import models

class Pessoa(models.Model):
    cc = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=120)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=200)
    telefone = models.BigIntegerField()
    email = models.EmailField(max_length=254, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

    
class Medico(Pessoa):
    numero_medico = models.BigIntegerField(unique=True)
    especialidade = models.CharField(max_length=100)

    consultas = models.ManyToManyField(
        'Consulta',
        through='MedicoConsulta'
    )

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

    def __str__(self):
        return f"Dr. {self.nome} - {self.especialidade}"


class Paciente(Pessoa):
    numero_seguranca_social = models.BigIntegerField(unique=True)
    data_registo = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.nome} (NSS: {self.numero_seguranca_social})"

    

class Consulta(models.Model):
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    data_hora = models.DateTimeField()
    motivo = models.TextField()

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-data_hora']

    def __str__(self):
        return f"Consulta - {self.paciente.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class MedicoConsulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Médico na Consulta'
        verbose_name_plural = 'Médicos nas Consultas'
        unique_together = ['medico', 'consulta']

    def __str__(self):
        return f"{self.medico.nome} - {self.consulta} ({self.role})"

    

class Receita(models.Model):
    id_receita = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

    def __str__(self):
        return f"Receita {self.id_receita}"
    


class Medicamento(models.Model):
    id_medicamento = models.CharField(max_length=50, primary_key=True)
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Medicacao(Receita):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    date = models.DateField()
    
    medicamentos = models.ManyToManyField(
        Medicamento,
        through='ItemMedicacao'
    )

    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['-date']

    def __str__(self):
        return f"Medicação {self.id_receita} - {self.paciente.nome} ({self.date})"


class ItemMedicacao(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    medicacao = models.ForeignKey(Medicacao, on_delete=models.CASCADE)
    dose = models.CharField(max_length=100, blank=True)
    quantidade = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Item de Medicação'
        verbose_name_plural = 'Itens de Medicação'

    def __str__(self):
        return f"{self.medicamento.nome} - {self.dose} x{self.quantidade}"


class Exame(models.Model):
    id_exame = models.CharField(max_length=50, primary_key=True)
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Exames(Receita):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    date = models.DateField()
    
    exames = models.ManyToManyField(
        Exame,
        through='ItemExames',
        related_name='prescricoes'
    )

    class Meta:
        verbose_name = 'Prescrição de Exames'
        verbose_name_plural = 'Prescrições de Exames'
        ordering = ['-date']

    def __str__(self):
        return f"Exames {self.id_receita} - {self.paciente.nome} ({self.date})"


class ItemExames(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    exames = models.ForeignKey(Exames, on_delete=models.CASCADE)
    resultados = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='ImagemExames/', blank=True,null=True)

    class Meta:
        verbose_name = 'Item de Exame'
        verbose_name_plural = 'Itens de Exames'

    def __str__(self):
        return f"{self.exame.nome} - {self.exames}"