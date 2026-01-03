# populate_medical_data.py
import os
import django
import random
from datetime import date, datetime, timedelta
from faker import Faker

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SNS.settings')
django.setup()

# Now import your models
from workshop.models import (
    Medico, Paciente, Consulta, MedicoConsulta,
    Medicamento, Medicacao, ItemMedicacao,
    Exame, Exames, ItemExames
)

# Initialize Faker for English data
fake = Faker('en_US')

def create_medications():
    """Create 5 medications"""
    medications_data = [
        ('PARA500', 'Paracetamol 500mg'),
        ('IBU400', 'Ibuprofen 400mg'),
        ('AML05', 'Amoxicillin 500mg'),
        ('SERT25', 'Sertraline 25mg'),
        ('ATOR20', 'Atorvastatin 20mg'),
    ]
    
    medications = []
    for med_id, name in medications_data:
        med = Medicamento.objects.create(
            id_medicamento=med_id,
            nome=name
        )
        medications.append(med)
        print(f'  Created medication: {name}')
    
    return medications

def create_exams():
    """Create 4 medical exams"""
    exams_data = [
        ('HEMO01', 'Complete Blood Count'),
        ('GLIC02', 'Fasting Blood Glucose'),
        ('COL03', 'Total Cholesterol'),
        ('UREIA04', 'Urea and Creatinine'),
    ]
    
    exams = []
    for exam_id, name in exams_data:
        exam = Exame.objects.create(
            id_exame=exam_id,
            nome=name
        )
        exams.append(exam)
        print(f'  Created exam: {name}')
    
    return exams

def create_doctors():
    """Create 7 doctors"""
    specialties = [
        'Cardiology', 'Dermatology', 'Pediatrics', 'Orthopedics',
        'Neurology', 'Psychiatry', 'General Medicine'
    ]
    
    doctors = []
    for i in range(7):
        # Generate unique ID and doctor number
        id_num = 10000000 + i
        while Medico.objects.filter(cc=id_num).exists():
            id_num += 100
        
        doctor_num = 5000 + i
        while Medico.objects.filter(numero_medico=doctor_num).exists():
            doctor_num += 1
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        doctor = Medico.objects.create(
            cc=id_num,
            nome=f"{first_name} {last_name}",
            data_nascimento=fake.date_of_birth(minimum_age=30, maximum_age=65),
            morada=fake.address().replace('\n', ', ')[:200],
            telefone=910000000 + i,
            email=f'doctor{i+1}@hospital.com',
            numero_medico=doctor_num,
            especialidade=random.choice(specialties)
        )
        doctors.append(doctor)
        print(f'  Created doctor: Dr. {doctor.nome} - {doctor.especialidade}')
    
    return doctors

def create_patients():
    """Create 15 patients"""
    patients = []
    for i in range(15):
        # Generate unique ID
        id_num = 20000000 + i
        while Paciente.objects.filter(cc=id_num).exists():
            id_num += 100
        
        ssn = 250000000 + i
        while Paciente.objects.filter(numero_seguranca_social=ssn).exists():
            ssn += 1
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        patient = Paciente.objects.create(
            cc=id_num,
            nome=f"{first_name} {last_name}",
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
            morada=fake.address().replace('\n', ', ')[:200],
            telefone=920000000 + i,
            email=f'patient{i+1}@email.com',
            numero_seguranca_social=ssn
        )
        patients.append(patient)
        print(f'  Created patient: {patient.nome} (SSN: {patient.numero_seguranca_social})')
    
    return patients

def create_consultations(patients, doctors):
    """Create 10 consultations"""
    reasons = [
        'Persistent headache',
        'Annual check-up',
        'Back pain',
        'Respiratory problems',
        'Routine consultation',
        'Medication control',
        'Post-operative follow-up',
        'Abdominal pain',
        'High fever',
        'Skin problems'
    ]
    
    roles = ['Primary Doctor', 'Assistant', 'Specialist', 'Observer']
    
    consultations = []
    start_date = datetime.now() - timedelta(days=60)
    
    for i in range(10):
        patient = random.choice(patients)
        
        # Create random date within last 60 days
        days_ago = random.randint(0, 60)
        consult_date = start_date + timedelta(days=days_ago)
        hour = random.randint(9, 17)  # 9 AM to 5 PM
        minute = random.choice([0, 15, 30, 45])
        appointment_time = consult_date.replace(hour=hour, minute=minute)
        
        consultation = Consulta.objects.create(
            paciente=patient,
            data_hora=appointment_time,
            motivo=random.choice(reasons)
        )
        
        # Assign 1-3 doctors to each consultation
        num_doctors = random.randint(1, 3)
        consultation_doctors = random.sample(doctors, min(num_doctors, len(doctors)))
        
        for j, doctor in enumerate(consultation_doctors):
            role = 'Primary Doctor' if j == 0 else random.choice(roles[1:])
            MedicoConsulta.objects.create(
                medico=doctor,
                consulta=consultation,
                role=role
            )
        
        consultations.append(consultation)
        print(f'  Created consultation: {patient.nome} on {appointment_time.strftime("%m/%d/%Y %H:%M")}')
    
    return consultations

def create_medication_prescriptions(patients, medications):
    """Create medication prescriptions"""
    for i in range(8):  # Create 8 medication prescriptions
        patient = random.choice(patients)
        
        # Random date within last 30 days
        days_ago = random.randint(1, 30)
        prescription_date = date.today() - timedelta(days=days_ago)
        
        prescription = Medicacao.objects.create(
            paciente=patient,
            date=prescription_date
        )
        
        # Add 1-3 medications to the prescription
        num_meds = random.randint(1, 3)
        selected_meds = random.sample(medications, min(num_meds, len(medications)))
        
        for medication in selected_meds:
            doses = ['1 tablet', '2 tablets', '500mg', '1 capsule', '10ml']
            ItemMedicacao.objects.create(
                medicamento=medication,
                medicacao=prescription,
                dose=random.choice(doses),
                quantidade=random.randint(1, 3)
            )
        
        print(f'  Created medication prescription for {patient.nome} on {prescription_date}')

def create_exam_prescriptions(patients, exams):
    """Create exam prescriptions"""
    for i in range(6):  # Create 6 exam prescriptions
        patient = random.choice(patients)
        
        # Random date within last 30 days
        days_ago = random.randint(1, 30)
        prescription_date = date.today() - timedelta(days=days_ago)
        
        exam_prescription = Exames.objects.create(
            paciente=patient,
            date=prescription_date
        )
        
        # Add 1-2 exams to the prescription
        num_exams = random.randint(1, 2)
        selected_exams = random.sample(exams, min(num_exams, len(exams)))
        
        for exam in selected_exams:
            results_options = [
                'Results within normal parameters',
                'Awaiting results',
                'Slightly elevated values',
                'Pending results',
                ''
            ]
            ItemExames.objects.create(
                exame=exam,
                exames=exam_prescription,
                resultados=random.choice(results_options)
            )
        
        print(f'  Created exam prescription for {patient.nome} on {prescription_date}')

def main():
    """Main function to populate the database"""
    print("=" * 50)
    print("POPULATING MEDICAL DATABASE")
    print("=" * 50)
    
    # Clear existing data (in reverse order of dependencies)
    print("\nClearing existing data...")
    ItemMedicacao.objects.all().delete()
    Medicacao.objects.all().delete()
    ItemExames.objects.all().delete()
    Exames.objects.all().delete()
    MedicoConsulta.objects.all().delete()
    Consulta.objects.all().delete()
    Medicamento.objects.all().delete()
    Exame.objects.all().delete()
    Paciente.objects.all().delete()
    Medico.objects.all().delete()
    print("All existing data cleared.\n")
    
    # Create data
    print("Creating medications...")
    medications = create_medications()
    
    print("\nCreating exams...")
    exams = create_exams()
    
    print("\nCreating doctors...")
    doctors = create_doctors()
    
    print("\nCreating patients...")
    patients = create_patients()
    
    print("\nCreating consultations...")
    create_consultations(patients, doctors)
    
    print("\nCreating medication prescriptions...")
    create_medication_prescriptions(patients, medications)
    
    print("\nCreating exam prescriptions...")
    create_exam_prescriptions(patients, exams)
    
    print("\n" + "=" * 50)
    print("DATABASE POPULATION COMPLETE")
    print("=" * 50)
    print("\nCreated:")
    print(f"  - {Medicamento.objects.count()} medications")
    print(f"  - {Exame.objects.count()} exams")
    print(f"  - {Medico.objects.count()} doctors")
    print(f"  - {Paciente.objects.count()} patients")
    print(f"  - {Consulta.objects.count()} consultations")
    print(f"  - {MedicoConsulta.objects.count()} doctor-consultation relationships")
    print(f"  - {Medicacao.objects.count()} medication prescriptions")
    print(f"  - {ItemMedicacao.objects.count()} prescription items")
    print(f"  - {Exames.objects.count()} exam prescriptions")
    print(f"  - {ItemExames.objects.count()} exam items")

if __name__ == '__main__':
    main()