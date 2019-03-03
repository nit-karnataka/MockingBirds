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
from django.utils import timezone
from datetime import datetime


#log_query=log_data_model.objects.create(log=log,short_log=short_log)

def admin_index_view(request):
    form1=LoginForm()
    form2=SignupForm()
    return render(request,'admin_app/admin_index.html',{'form1':form1,'form2':form2})

def admin_signup_view(request):
    if request.method == 'POST':
        form1=LoginForm(request.POST)
        form2=SignupForm(request.POST)
        if form2.is_valid():
            name = form2.cleaned_data.get('name')
            email = form2.cleaned_data.get('email')
            user_obj=User.objects.filter(email=email)
            if user_obj == None:
                raw_password = form2.cleaned_data.get('password')
                user_new = User.objects.create_user(email,email,raw_password)
                user_new.first_name = name
                user_new.save()
                user = authenticate(username=email, password=raw_password)
                login(request, user)
                log="admin signed up for the first time"
                short_log="adminsignup"
                log_query=log_data_model.objects.create(log=log,short_log=short_log)
                return redirect('admin_app:admin_dashboard_view')
            else:
                return redirect('admin_app:admin_index_view')

    return render(request,'admin_app/admin_index.html',{})

def admin_login_view(request):
    print("admin_login_view")
    error_msz=0
    if request.method == 'POST':
        print("nik")
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(username=email, password=password)
        if(user==None):
            error_msz=1
            return redirect('admin_app:admin_index_view')

        print(user)
        if user:
            if user.is_active:
                login(request,user)
                log="admin logged in "
                short_log="adminlogin"
                log_query=log_data_model.objects.create(log=log,short_log=short_log)
                return redirect('admin_app:admin_dashboard_view')
            else:
                return render(request,'admin_app/admin_index.html',{})
        else:
            error_msz=1
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return redirect('admin_app:admin_index_view')
    return render(request,'admin_app/add_students_details_view.html',{'error_msz':error_msz})

def admin_dashboard_view(request):
    return render(request,'admin_app/admin_dashboard.html',{})

def add_students_details_view(request):
    success=0
    error_msz2=0
    form=StudentDetailsForm()
    freq_obj=and_or_search_model.objects.all()[:1]
    print(freq_obj)
    for f in freq_obj:
        frequency=f.frequency
        and_or=f.and_or_search
        print(frequency,and_or)
    if request.method == 'POST':
        Engine=SearchEngine('IndexedDatabase')
        SimilarEngine = SimilaritySearchEngine()
        form=StudentDetailsForm(request.POST)
        print("nikbackput",form.is_valid())
        pdf_path_list=[]
        if form.is_valid():
            new_query=form.save(commit = False)
            new_query.save()
            keywords = form.cleaned_data.get('keywords')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            int_one=int(1)
            print(type(int_one))
            new_student=student_status_model.objects.create(email=new_query,status=int_one)

            log="  new account created for {}".format(name)
            short_log="new_acc_created"
            log_query=log_data_model.objects.create(log=log,short_log=short_log)

            success=1
            old_pdf_list=[]
            similar_paths = []
            print("keywords",keywords)
            result_list_accurate=Engine.search(keywords, old_pdf_list, operation=and_or.upper())

            result_list_similar=SimilarEngine.search(keywords, old_pdf_list, operation=and_or.upper())

            for pz in result_list_similar:
                similar_paths.append(pz['pdf_path'])

            print("result_list:",result_list_accurate)
            # for pz in result_list:
            #     print(pz['title'],pz['abstract'],pz['pdf_path'],pz['creation_date'])
            for pz in result_list_accurate:
                set_pdf=pdf_indexing_model2.objects.create(pdf_title=pz['title'],pdf_abstract=pz['abstract'],pdf_path=pz['pdf_path'],pdf_creation_date=pz['creation_date'])
                assign_pdf=pdf_query_model2.objects.create(email=new_query,pdf_path=set_pdf)
                pdf_path_list.append(pz['pdf_path'])
            log="email sent to {} name={} with pdfs {} for keywords {}".format(email,name,pdf_path_list,keywords)
            short_log="email_pdf"
            log_query=log_data_model.objects.create(log=log,short_log=short_log)

            emailsms=SendEmailSms(fromaddr='pdhindujaa@gmail.com', from_password='!1q2w3e4r5t%', toaddr=[email])
            body = ''
            for res in result_list_accurate:
                body += '{} with {} relevance\n'.format(res['title'], res['relevance'])

            emailsms.send(pdf_path_list)

            emailsms.send(similar_paths)

            return render(request,'admin_app/twobuttons.html',{'form':form,'success':success})
        else:
            error_msz2=1
            return render(request,'admin_app/add_students_details.html',{'form':form,'success':success,'error_msz2':error_msz2})
    return render(request,'admin_app/add_students_details.html',{'form':form,'success':success,'error_msz2':error_msz2})

def update_students_details_email_view(request):
    error_msz3=0
    form=StudentUpdateEmail()
    if request.method == 'POST':
        form=StudentUpdateEmail(request.POST)
        print("nikbackput",form.is_valid())
        if form.is_valid():
            email=request.POST.get('email')
            request.session['email'] = email
            return redirect('admin_app:update_students_details_view')
        else:
            error_msz3=1
    else:
        error_msz3=1
    return render(request,'admin_app/update_students_details_email.html',{'form':form,'error_msz3':error_msz3})

def update_students_details_view(request):
    error_msz4=0
    success=0
    old_keywords=None
    freq_obj=and_or_search_model.objects.all()[:1]
    for f in freq_obj:
        frequency=f.frequency
        and_or=f.and_or_search

    email=request.session.get('email')
    print("session email",email)
    if request.method == 'GET':
        old_keywords=None
        try:
            print("nik1")
            form=StudentDetailsForm(request.GET or None,instance=student_model.objects.get(email=email))
            student_obj=student_model.objects.filter(email=email)
            for x in student_obj:
                old_keywords=x.keywords
            print("nik2",form)
        except:
            print("nik3")
            form=StudentDetailsForm(request.GET or None)
            print("nik3")

    elif request.method == 'POST':
        print("jatin in post")
        Engine=SearchEngine('IndexedDatabase')
        SimilarEngine = SimilaritySearchEngine()

        try:
            form=StudentDetailsForm(request.POST or None,instance=student_model.objects.get(email=email))
            print("form",form)
            student_obj=student_model.objects.filter(email=email)
            for x in student_obj:
                old_keywords=x.keywords
        except:
            form=StudentDetailsForm(request.POST or None)
        pdf_path_list=[]
        print("is valid",form.is_valid())
        if form.is_valid():
            print("jatin log=========",email)
            log="  student details updated for {}".format(email)
            short_log="updated_info"
            log_query=log_data_model.objects.create(log=log,short_log=short_log)
            new_keywords = form.cleaned_data.get('keywords')
            student_details_obj = form.save(commit=False)
            student_details_obj.email = email
            student_details_obj.save()
            success=1
            similar_paths = []

            if old_keywords==None:
                print("keywords",new_keywords)
                result_list_accurate=Engine.search(new_keywords, pdf_path_list, operation=and_or.upper())
                result_list_similar=SimilarEngine.search(keywords, old_pdf_list, operation=and_or.upper())

                print("result_list:",result_list_accurate)
                # for pz in result_list:
                #     print(pz['title'],pz['abstract'],pz['pdf_path'],pz['creation_date'])
                for pz in result_list_accurate:
                    set_pdf=pdf_indexing_model2.objects.create(pdf_title=pz['title'],pdf_abstract=pz['abstract'],pdf_path=pz['pdf_path'],pdf_creation_date=pz['creation_date'])
                    assign_pdf=pdf_query_model2.objects.create(email=student_details_obj,pdf_path=set_pdf)
                    pdf_path_list.append(pz['pdf_path'])

                for pz in result_list_similar:
                    similar_paths.append(pz['pdf_path'])


                emailsms=SendEmailSms(fromaddr='pdhindujaa@gmail.com', from_password='!1q2w3e4r5t%', toaddr=[email])
                emailsms.send(pdf_path_list)

                emailsms.send(similar_paths)

            elif new_keywords !=old_keywords :
                log="  keywords  updated for {} from {} to {}".format(email,old_keywords,new_keywords)
                short_log="updated_keyword"
                log_query=log_data_model.objects.create(log=log,short_log=short_log)
                print("keywords",new_keywords)
                result_list=Engine.search(new_keywords, pdf_path_list, operation=and_or.upper())
                print("result_list:",result_list)
                # for pz in result_list:
                #     print(pz['title'],pz['abstract'],pz['pdf_path'],pz['creation_date'])
                for pz in result_list:
                    set_pdf=pdf_indexing_model2.objects.create(pdf_title=pz['title'],pdf_abstract=pz['abstract'],pdf_path=pz['pdf_path'],pdf_creation_date=pz['creation_date'])
                    assign_pdf=pdf_query_model2.objects.create(email=student_details_obj,pdf_path=set_pdf)
                    pdf_path_list.append(pz['pdf_path'])
                log="email sent to {}  with pdfs {} for keywords {}".format(email,pdf_path_list,new_keywords)
                short_log="update_email_pdf"
                log_query=log_data_model.objects.create(log=log,short_log=short_log)
                emailsms=SendEmailSms(fromaddr='pdhindujaa@gmail.com', from_password='!1q2w3e4r5t%', toaddr=[email])
                emailsms.send(pdf_path_list)

    else:
        error_msz4=1
    return render(request,'admin_app/update_students_details.html',{'form':form,'success':success,'error_msz4':error_msz4})


def admin_settings_view(request):
    success=0
    if request.method == 'GET':
        try:
            print("nik1")
            form=and_or_search(request.GET or None,instance=and_or_search_model.objects.get(email=request.user))
            print("nik2",form)
        except:
            print("nik3")
            form=and_or_search(request.GET or None)
            print("nik4")

    elif request.method == 'POST':
        print("nik5")
        try:
            print("nik6")
            form=and_or_search(request.POST or None,instance=and_or_search_model.objects.get(email=request.user))
        except:
            print("nik7")
            form=and_or_search(request.POST or None)
        print("validity",form.is_valid())
        if form.is_valid():
            and_or_search_obj = form.save(commit=False)
            and_or_search_obj.email = request.user
            and_or_search_obj.save()
            success=1
    return render(request,'admin_app/admin_settings.html',{'form':form})



def deactivate_student_account_view(request):
    form=StudentUpdateEmail()
    success=0
    if request.method == 'POST':
        form=StudentUpdateEmail(request.POST)
        print("nikbackput",form.is_valid())
        if form.is_valid():
            email=request.POST.get('email')
            student_obj=student_model.objects.filter(email=email)
            student_status_model_obj=student_status_model.objects.filter(email=student_obj).update(status=int(0),date_of_query=datetime.now())
            log="  student account deactivated for {}".format(email)
            short_log="deactivated_acc"
            log_query=log_data_model.objects.create(log=log,short_log=short_log)
            return render(request,'admin_app/deactivate_student_account.html',{'form':form,'success':success})
    return render(request,'admin_app/deactivate_student_account.html',{'form':form})


def log_details_view(request):
    #db_obj of registered users
    log_list=[]
    student_model_obj=student_model.objects.all()
    student_status_model_obj=student_status_model.objects.all()
    pdf_query_model2_obj=pdf_query_model2.objects.all()
    log_data_model_obj=log_data_model.objects.all().order_by('-date_of_query')
    for l in log_data_model_obj:
        log_list.append({'log_date':l.date_of_query,'log':l.log})
    return render(request,'admin_app/show_log.html',{'log_list':log_list})
