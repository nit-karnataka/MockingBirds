from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class student_model(models.Model):
    name = models.CharField(max_length=264,unique=False,blank=True,null=True)
    email=models.EmailField(blank=True, null=True, unique=True)
    research_department_email=models.EmailField()
    research_department_name=models.CharField(max_length=264,unique=False,blank=True,null=True)
    research_department_phone=models.IntegerField(default=91)
    faculty_incharge_email=models.EmailField()
    faculty_incharge_name=models.CharField(max_length=264,unique=False,blank=True,null=True)
    faculty_incharge_phone=models.IntegerField(default=91)
    phone_no=models.IntegerField(default=91)
    research_area=models.CharField(max_length=264,unique=False,blank=True,null=True)
    date_of_tenure_completion=models.DateField(blank=True,null=True)
    keywords = models.TextField(null=True)
    date_of_query=models.DateField(default=datetime.now,blank=True,null=True)

    def __str__(self):
        return str(self.email)
class student_status_model(models.Model):
    email=models.ForeignKey(student_model, on_delete=models.CASCADE)
    status=models.IntegerField(default=1)
    date_of_query=models.DateField(default=datetime.now,blank=True,null=True)

    def __str__(self):
        return str(self.email)

class and_or_search_model(models.Model):
    SEARCH_CHOICES=(('and','and'),('or','or'))
    and_or_search=models.CharField(max_length=5, choices=SEARCH_CHOICES, default='and')
    frequency=models.IntegerField(default=1)
    email=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_query=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)

class pdf_indexing_model2(models.Model):
    pdf_title=models.TextField(unique=False,blank=True,null=True)
    pdf_abstract=models.TextField(unique=False,blank=True,null=True)
    pdf_path=models.TextField(unique=True,blank=True,null=True)
    pdf_creation_date=models.CharField(max_length=264,unique=False,blank=True,null=True)

    def __str__(self):
        return str(self.pdf_path)

class pdf_query_model2(models.Model):
    email=models.ForeignKey(student_model, on_delete=models.CASCADE)
    pdf_path=models.ForeignKey(pdf_indexing_model2, on_delete=models.CASCADE)
    date_of_query=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)


class log_data_model(models.Model):
    date_of_query=models.DateTimeField(default=timezone.now)
    log=models.CharField(max_length=264,unique=False,blank=True,null=True)
    short_log=models.CharField(max_length=264,unique=False,blank=True,null=True)

    def __str__(self):
        return str(self.date_of_query)
