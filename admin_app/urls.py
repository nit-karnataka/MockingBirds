from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('admin_index_view', views.admin_index_view, name='admin_index_view'),
    path('admin_dashboard_view', views.admin_dashboard_view, name='admin_dashboard_view'),
    path('admin_signup_view', views.admin_signup_view, name='admin_signup_view'),
    path('admin_login_view', views.admin_login_view, name='admin_login_view'),
    path('add_students_details_view', views.add_students_details_view, name='add_students_details_view'),
    path('update_students_details_email_view', views.update_students_details_email_view, name='update_students_details_email_view'),
    path('update_students_details_view', views.update_students_details_view, name='update_students_details_view'),
    path('log_details_view', views.log_details_view, name='log_details_view'),
    path('admin_settings_view', views.admin_settings_view, name='admin_settings_view'),
    path('deactivate_student_account_view', views.deactivate_student_account_view, name='deactivate_student_account_view'),

]
