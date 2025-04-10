from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('store', 'Medical Store'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    age = models.IntegerField(default=30)

class DoctorFee(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    fee = models.IntegerField(default=0)

class PatientRecord(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_records')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_records')
    age = models.PositiveIntegerField()
    disease = models.CharField(max_length=200)
    medicines = models.TextField()
    date = models.DateField(default=timezone.now)


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return self.name