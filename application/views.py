import json
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import SignUpForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


@login_required
def index(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def handleWomen(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def collectiondata(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def boiteSuggestion(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def agentsAmis(request):
    return render(request, 'welcome/tableau-de-bord.html')


User = get_user_model()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        province = data['province']
        city = data['city']
        role = data['role']
        email = data['email']
        password = data['password']

        if not (name and province and city and role and email and password):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
                province=province,
                city=city,
                role=role
            )
            return JsonResponse({'message': f'Votre compte a été créé avec succès, le username est vore adresse mail : (${user.username}) !'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return render(request, "account/signup.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error_message = 'Utilisateur ou mot de passe incorrect'
            return render(request, 'account/login.html', {'error_message': error_message})
    return render(request, "account/login.html")
