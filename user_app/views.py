from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from admin_app.models import *
from sendemailsms import *
from backend.SearchEngine import *
import datetime
import threading


def index_view(request):
    form=SearchForm()
    freq_obj=and_or_search_model.objects.all()[:1]
    for f in freq_obj:
        frequency=f.frequency
        and_or=f.and_or_search
    if request.method == 'POST':
        Engine=SearchEngine('IndexedDatabase')
        SimilarEngine = SimilaritySearchEngine()

        form=SearchForm(request.POST)
        print("printing result")
        pdf_path_list=[]
        similar_paths = []

        print(form.is_valid())
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            email = form.cleaned_data.get('email')
            reg_no=form.cleaned_data.get('reg_no')
            new_query=query_model.objects.create(keywords=keywords, email=email)
            print("keywords",keywords)
            result_list_accurate=Engine.search(keywords, pdf_path_list, operation=and_or.upper())
            result_list_similar=SimilarEngine.search(keywords, pdf_path_list, operation=and_or.upper())

            for pz in result_list_similar:
                similar_paths.append(pz['pdf_path'])


            print("result_list:",result_list_accurate)
            # for pz in result_list:
            #     print(pz['title'],pz['abstract'],pz['pdf_path'],pz['creation_date'])
            for pz in result_list_accurate:
                set_pdf=pdf_indexing_model.objects.create(pdf_title=pz['title'],pdf_abstract=pz['abstract'],pdf_path=pz['pdf_path'],pdf_creation_date=pz['creation_date'])
                assign_pdf=pdf_query_model.objects.create(email=new_query,pdf_path=set_pdf)
                pdf_path_list.append(pz['pdf_path'])
            emailsms=SendEmailSms(fromaddr='pdhindujaa@gmail.com', from_password='!1q2w3e4r5t%', toaddr=[email])
            emailsms.send(pdf_path_list)
            emailsms.send(similar_paths)


            return redirect('user_app:success_msz_view')
        else:
            return render(request,'user_app/user.html',{'form':form})
    return render(request,'user_app/user.html',{'form':form})



def success_msz_view(request):
    return render(request,'user_app/success_msz.html',{})
