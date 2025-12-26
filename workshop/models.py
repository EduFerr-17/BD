from django.db import models

class Pessoa(models.Model):

    cc = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=120)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=200)
    telefone = models.BigIntegerField()
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):

        return self.nome
    
class Medico(Pessoa):
    
    numero_medico = models.BigIntegerField(unique=True)
    especialidade = models.CharField(max_length=100)

    consultas = models.ManyToManyField(
        'Consulta',
        through='MedicoConsulta'
    )

class Paciente(Pessoa):

    numero_seguranca_social = models.BigIntegerField(unique=True)
    data_registo = models.DateField(auto_now_add=True)

    

class Consulta(models.Model):

    
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE,
        related_name='consultas'
    )

    data_hora = models.DateTimeField()
    motivo = models.TextField()


class MedicoConsulta(models.Model):  # Middle table for many-to-many
    field_0 = models.CharField(max_length=50, primary_key=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True)  # e.g., "Primary", "Specialist"
    

class Receita(models.Model):

    id_receita = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Receita {self.id_receita}"
    


class Medicamento(models.Model):
    field_0 = models.CharField(max_length=50, primary_key=True)
    nome = models.CharField(max_length=200)

class Medicacao(Receita):
    field_0 = models.CharField(max_length=50, primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Define the many-to-many relationship
    medicamentos = models.ManyToManyField(
        Medicamento,
        through='ItemMedicacao'
    )

class ItemMedicacao(models.Model):  # The middle table
    field_0 = models.CharField(max_length=50, primary_key=True)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    medicacao = models.ForeignKey(Medicacao, on_delete=models.CASCADE)
    dose = models.CharField(max_length=100, blank=True)
    quantidade = models.IntegerField(default=1)


class Exame(models.Model):
    field_0 = models.CharField(max_length=50, primary_key=True)
    nome = models.CharField(max_length=200)

class Exames(Receita):
    field_0 = models.CharField(max_length=50, primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Define the many-to-many relationship
    exames = models.ManyToManyField(
        Exame,
        through='ItemExames'
    )

class ItemExames(models.Model):  # The middle table
    field_0 = models.CharField(max_length=50, primary_key=True)
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    exames = models.ForeignKey(Exames, on_delete=models.CASCADE)
    resultados = models.TextField(blank=True)



