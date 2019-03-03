from django.db import models
from django.utils import timezone

# Create your models here.
class query_model(models.Model):
    keywords = models.TextField(null=True)
    email=models.CharField(max_length=264,unique=False,blank=True,null=True)
    date_of_query=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.keywords)


class pdf_indexing_model(models.Model):
    pdf_title=models.TextField(unique=False,blank=True,null=True)
    pdf_abstract=models.TextField(unique=False,blank=True,null=True)
    pdf_path=models.TextField(unique=False,blank=True,null=True)
    pdf_creation_date=models.CharField(max_length=264,unique=False,blank=True,null=True)

    def __str__(self):
        return str(self.pdf_path)

class pdf_query_model(models.Model):
    email=models.ForeignKey(query_model, on_delete=models.CASCADE)
    pdf_path=models.ForeignKey(pdf_indexing_model, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)
