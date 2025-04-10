"""
URL configuration for healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from core.views import add_medicine, delete_medicine, doctor_dashboard, edit_medicine, explain_medicine, health_tips_chatbot, home, issue_medicine, login_view, logout_view, patient_dashboard, patients_list,  recommend_doctor, register_patient, store_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),

    path('logout/', logout_view, name='logout'),

    path('health-tips/', health_tips_chatbot, name='health_tips_chatbot'),
    # path('login/<str:role>/', login_view, name='login'),

    path('recommend/', recommend_doctor, name='recommend_doctor'),
    
    path('explain/', explain_medicine, name='explain_medicine'),
    path('login/<str:role>/', login_view, name='login'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
    path('store/', store_dashboard, name='store_dashboard'),
    path('register/', register_patient, name='register_patient'),
    path('add/', add_medicine, name='add_medicine'),

    path('medicine/delete/<int:id>/', delete_medicine, name='delete_medicine'),
    path('medicine/edit/<int:id>/', edit_medicine, name='edit_medicine'),

    path('store/', store_dashboard, name='store_dashboard'),

    path('patients/', patients_list, name='patients_list'),

]
