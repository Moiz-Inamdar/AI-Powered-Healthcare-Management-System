import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login

from core.forms import MedicineForm
from .models import Profile, DoctorFee, PatientRecord, Medicine, User
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control




def logout_view(request):
    logout(request)
    return redirect('home')  

def home(request):
    return render(request, 'core/home.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Profile  # Assuming you have a Profile model



def login_view(request, role):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.profile.role == role:
            login(request, user)
            return redirect(f'{role}_dashboard')
        return render(request, 'core/login.html', {'role': role, 'error': 'Invalid credentials'})
    return render(request, 'core/login.html', {'role': role})
from .models import DoctorFee  # make sure this is imported


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/doctor/')
def doctor_dashboard(request):
    patients = PatientRecord.objects.filter(doctor=request.user)

    fee_record = DoctorFee.objects.filter(doctor=request.user).first()
    total_earnings = 0
    if fee_record:
        total_earnings = fee_record.fee * 200  # ₹500 per patient

    return render(request, 'core/doctor_dashboard.html', {
        'patients': patients,
        'total_earnings': total_earnings
    })



def register_patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        disease = request.POST['disease']
        medicines = request.POST['medicines']

        patient_user, created = User.objects.get_or_create(username=name, defaults={'password': 'default123'})
        if created:
            patient_user.set_password('default123')
            patient_user.save()
            Profile.objects.create(user=patient_user, role='patient')

        PatientRecord.objects.create(
        doctor=request.user,
        patient=patient_user,
        age=age,
        disease=disease,
        medicines=medicines,
        date=timezone.now()
        )


        fee, created = DoctorFee.objects.get_or_create(doctor=request.user, defaults={'fee': 0})
        fee.fee += 1
        fee.save()

        return redirect('doctor_dashboard')

    return render(request, 'core/register_patient.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/patient/')
def patient_dashboard(request):
    records = PatientRecord.objects.filter(patient=request.user)
    return render(request, 'core/patient_dashboard.html', {'records': records})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/store/')
def store_dashboard(request):
    medicines = Medicine.objects.all()
    return render(request, 'core/store_dashboard.html', {'medicines': medicines})


# core/views.py

from django.shortcuts import render, redirect
from .models import Medicine

def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if not name or not quantity:
            return render(request, 'add_medicine.html', {'error': 'All fields are required'})

        try:
            quantity = int(quantity)
        except ValueError:
            return render(request, 'add_medicine.html', {'error': 'Quantity must be a number'})

        try:
            medicine = Medicine.objects.get(name=name)
            medicine.quantity += quantity
        except Medicine.DoesNotExist:
            medicine = Medicine(name=name, quantity=quantity)

        medicine.save()
        return redirect('store_dashboard')  # or any success page

    return render(request, 'core/add_medicine.html')



def issue_medicine(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        medicine_name = request.POST.get('medicine')
        quantity = request.POST.get('quantity')

        if not username or not medicine_name or not quantity:
            return render(request, 'issue_medicine.html', {'error': 'All fields are required'})

        try:
            quantity = int(quantity)
        except ValueError:
            return render(request, 'issue_medicine.html', {'error': 'Quantity must be a number'})

        try:
            patient = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'issue_medicine.html', {'error': 'Patient not found'})

        try:
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            return render(request, 'issue_medicine.html', {'error': 'Medicine not found'})

        if medicine.quantity < quantity:
            return render(request, 'issue_medicine.html', {'error': 'Not enough stock available'})

        # Reduce quantity and save
        medicine.quantity -= quantity
        medicine.save()

        # Save issued record (if you have a model for issued medicine, you can use that here)

        return redirect('store_dashboard')

    return render(request, 'core/issue_medicine.html')

import requests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import os
import requests

@csrf_exempt
@login_required
def explain_medicine(request):
    explanation = ""
    if request.method == 'POST':
        medicine_name = ', '.join([m.strip() for m in request.POST.get('medicine_name', '').split(',') if m.strip()])

        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"  # better smaller model
        headers = {
            "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
        }

        prompt = f"What is the use of {medicine_name}?"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.3,
                "return_full_text": False
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and 'generated_text' in result[0]:
                explanation = result[0]['generated_text'].strip()
            else:
                explanation = "Could not fetch right now, you can ask your doctor."
        else:
            explanation = "Could not fetch right now, you can ask your doctor."

    return render(request, 'core/explanation.html', {'explanation': explanation})

import requests
from django.shortcuts import render






def query_huggingface(symptoms, age):
    import requests

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {
    "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
}

    prompt = f"""
You are a medical assistant. A {age}-year-old patient is experiencing the following symptoms: {symptoms}.
Respond with the most suitable doctor specialization ONLY.
Examples: Cardiologist, Pulmonologist, Dermatologist, Neurologist.
Just return the specialization name. Do not include explanations or other text.
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 15,
            "temperature": 0.3,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text'].strip()
    return "General Physician"




from django.shortcuts import render, redirect
from transformers import pipeline

def recommend_doctor(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        
        # Replace this with your own age-fetching logic
        record = PatientRecord.objects.filter(patient=request.user).order_by('-date').first()

        if record:
            age = record.age
        else:
            age = 30  # default age if not found

        recommendation = query_huggingface(symptoms, age)

      

        return render(request, 'core/doctor_recommendation.html', {'recommendation': recommendation})



def get_health_tip(question):
    import requests

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {
    "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
}

    prompt = f"""
You are a health assistant. Based on the question below, respond with **only 1-2 short health tips** in simple language.
Avoid numbering or listing too many items.explain in short para.

Question: {question}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            # "max_new_tokens": 100,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text'].strip() + "**Please consult a healthcare provider for accurate advice.**"

    return "Please consult a healthcare provider for accurate advice."
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

@csrf_exempt
def health_tips_chatbot(request):
    if request.method == "POST":
        question = request.POST.get("question")
        if question:
            tips = get_health_tip(question)
        else:
            tips = "Please enter your question."
        
        return render(request, "core/doctor_recommendation.html", {
            "tips": tips,
            "recommendation": request.session.get("last_recommendation", "Not available")
        })
    return redirect("patient_dashboard")


# Delete Medicine
@login_required(login_url='/login/store/')
def delete_medicine(request, id):
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, id=id)
        medicine.delete()
    return redirect('store_dashboard')

# Edit (Rename / Update) Medicine
@login_required(login_url='/login/store/')
def edit_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('store_dashboard')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'core/edit_medicine.html', {'form': form, 'medicine': medicine})




from django.shortcuts import render
  # Assuming you have a Patient model that stores patient details

def patients_list(request):
    # Fetch all patients along with their prescribed medicines
    patients = PatientRecord.objects.all().order_by('-date')  # You can order them by the date they were created or any other field
    return render(request, 'core/patients_list.html', {'patients': patients})


# git add .
# git commit -m "Updated HTML file"
# git push origin main
