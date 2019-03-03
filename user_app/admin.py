from django.contrib import admin
from user_app.models import *
# Register your models here.

admin.site.register(query_model)
admin.site.register(pdf_indexing_model)
admin.site.register(pdf_query_model)
