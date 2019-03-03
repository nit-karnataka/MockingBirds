from __future__ import absolute_import, unicode_literals
from celery import task

from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.contrib.auth.decorators import login_required
from sendemailsms import *
from backend.SearchEngine import *
from IndexDatabase import Indexer


@task()
def Task_schedular_view():
    indexer = Indexer('IndexedDatabase')
    indexer.add('new_pdfs')

    tmp_indexer = Indexer('TmpDatabase')
    tmp_indexer.add('new_pdfs')

    Engine=SearchEngine('TmpDatabase')

    old_pdf_list=[]
    print("result_list:",result_list)
    db_obj=student_model.objects.all()
    freq_obj=and_or_search_model.objects.all()[:1]
    for f in freq_obj:
        frequency=f.frequency
        and_or=f.and_or_search
    for stud in db_obj:
        old_keywords=stud.keywords
        pdf_query_model2_obj=pdf_query_model2.objects.filter(email=stud)
        for q in pdf_query_model2_obj:
            pdf_obj=q.pdf_path
            old_pdf_list.append(pdf_obj.pdf_title)

    result_list=Engine.search(old_keywords, old_pdf_list, operation=and_or.upper())
    for pz in result_list:
        set_pdf=pdf_indexing_model2.objects.create(pdf_title=pz['title'],pdf_abstract=pz['abstract'],pdf_path=pz['pdf_path'],pdf_creation_date=pz['creation_date'])
        assign_pdf=pdf_query_model2.objects.create(email=student_details_obj,pdf_path=set_pdf)
        pdf_path_list.append(pz['pdf_path'])
    emailsms=SendEmailSms(fromaddr='pdhindujaa@gmail.com', from_password='!1q2w3e4r5t%', toaddr=[email])
    emailsms.send(pdf_path_list)
