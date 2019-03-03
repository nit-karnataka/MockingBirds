from django.urls import path
from . import views

app_name = 'user_app'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('success_msz_view', views.success_msz_view, name='success_msz_view'),

]
