from django.db import models
from django.conf import settings

# Create your models here.
class Staff(models.Model):
    # DEPARTMENT_CHOICES = (
    #     ('office', 'Office Staff'),
    #     ('librarian', 'Librarian'),
    # )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    # department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    date_joined = models.DateField()  # Date of joining the staff
    date_resigned = models.DateField(blank=True, null=True)  # Optional field for resignation date
    is_active = models.BooleanField(default=True)  # To indicate if the staff is active

    def __str__(self):
        return self.user