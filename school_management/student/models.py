from django.db import models
from django.conf import settings

# Create your models here.
class Student(models.Model):

    STANDARD_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    
    DIVISION_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    )
    
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    profile_pic = models.ImageField(upload_to='student Picture')
    mob = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1 , choices=GENDER_CHOICES)
    roll_number = models.CharField(max_length=20)
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES)
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES)

    def __str__(self):
        return f"{self.name})"
    

class FeesHistory(models.Model):

    STATUS_CHOICES = (
        ('due', 'Due'),
        ('paid', 'Paid'),
    )

    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    amount = models.FloatField()
    due_date = models.DateField()
    payment_date = models.DateTimeField(null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)


class FeeDetails(models.Model):

    STANDARD_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES)
    amount = models.FloatField()
    due_date = models.DateField()
    def __str__(self):
        return f"Fee for Standard {self.standard} - Amount: {self.amount}"