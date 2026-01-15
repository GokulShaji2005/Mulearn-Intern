from django.db import models
from accounts.models import User
# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    )
  
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

# class Skill(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name
# jobs/models.py




