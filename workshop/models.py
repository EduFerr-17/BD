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

    def __str__(self):

        return f"Dr. {self.nome} - {self.especialidade}"

class Paciente(Pessoa):

    numero_seguranca_social = models.BigIntegerField(unique=True)
    data_registo = models.DateField(auto_now_add=True)

    def __str__(self):

        return f"{self.nome} - NSS: {self.numero_seguranca_social}"

class Consulta(models.Model):

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    motivo = models.TextField()

    def __str__(self):

        return f"Consulta de {self.paciente.nome} com Dr. {self.medico.nome} em {self.data_hora}"


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



