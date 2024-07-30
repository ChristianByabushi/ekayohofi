from django.template import RequestContext
from django import forms
from django.http import HttpResponseBadRequest
from django.utils.timezone import datetime  # important if using timezones
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from .models import Femme
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
import django_excel as excel
import csv


@login_required
def profile(request):
    return render(request, 'profile/index.html')


@login_required
def index(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def handleWomen(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def utilisateurs(request):
    return render(request, 'account/utilisateurs.html')


@login_required
def actions(request):
    if request.method == 'POST':
        beneficiary = request.POST.get('beneficiary')
        date_action = request.POST.get('dateAction')
        description_action = request.POST.get('descriptionAction')
        cost_estimated = request.POST.get('costEstimated')
        action_type = request.POST.get('actionType')
        image_action = request.FILES.get('image_action')

        # Check if the uploaded file is an image
        if image_action:
            if not image_action.content_type.startswith('image/'):
                return JsonResponse({'message': 'Erreur : Le fichier doit \être une image.'}, status=400)

        if not (date_action and cost_estimated and action_type and description_action and beneficiary):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)

        new_action = Action(
            beneficiary=beneficiary,
            date_action=date_action,
            description_action=description_action,
            cost_estimated=cost_estimated,
            action_type=action_type
        )

        new_action.save()
        return JsonResponse({'message': 'Action enregistrée avec sucssès'})
    else:
        actions = Action.objects.all().order_by('-date_action')
        paginator = Paginator(actions, 5)

        page_number = request.GET.get('page')
        actionsEntries = paginator.get_page(page_number)

        context = {
            'actionsEntries': actionsEntries,
            'is_supervisor': request.user.groups.filter(name='supervisor').exists(),
        }
    return render(request, 'collectdata/actions.html', context)


@csrf_exempt
def create_femme(request):
    if request.method == 'POST':
        menage = request.POST.get('menage')
        appliquer_questionnaire = request.POST.get('appliquerQuestionnaire')
        name_femme = request.POST.get('nameFemme')
        numero_tel_femme = request.POST.get('numeroTelFemme')
        form_file = request.FILES.get('formFile')
        age_femme = request.POST.get('ageFemme')
        scolarite_femme = request.POST.get('scolariteFemme')

        if not (menage and appliquer_questionnaire and name_femme and numero_tel_femme and age_femme and scolarite_femme):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)

        try:
            femme = Femme.objects.create(
                menage=menage,
                appliquer_questionnaire=appliquer_questionnaire,
                name_femme=name_femme,
                numero_tel_femme=numero_tel_femme,
                form_file=form_file,
                age_femme=age_femme,
                scolarite_femme=scolarite_femme
            )
            return JsonResponse({'message': 'Femme created successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)


def action_download_excel(request):
    actions = Action.objects.all()

    column_names = ['ID', 'Beneficiary', 'Description',
                    'Action Type', 'CoutEstime', 'DateAction']
    data = [[action.id, action.beneficiary, action.description_action, action.action_type,
             action.cost_estimated, action.date_action] for action in actions]
    file_name = f"actions_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}"
    sheet = excel.pe.Sheet([column_names]+data)
    return excel.make_response(sheet, 'csv', file_name=file_name)


def pdf_download_excel(request):
    actions = Action.objects.all()
    column_names = ['ID', 'Beneficiary',
                    'Action Type', 'Cost Estimated', 'Date Action']
    data = [[action.id, action.beneficiary, action.action_type,
             action.cost_estimated, action.date_action] for action in actions]
    return excel.make_response_from_array([column_names] + data, "xlsx", file_name=f"actions{datetime.today()}.xlsx")


@login_required
def femmes(request):
    if request.method == 'POST':
        # Extracting form data
        menage = request.POST.get('menage')
        appliquer_questionnaire = request.POST.get('appliquerQuestionnaire')
        name_femme = request.POST.get('nameFemme')
        numero_tel_femme = request.POST.get('numeroTelFemme')
        form_file = request.FILES.get('formFile')
        age_femme = request.POST.get('ageFemme')
        scolarite_femme = request.POST.get('scolariteFemme')
        genre_probleme = request.POST.get('genreProbleme')
        description_cas_femme = request.POST.get('descriptionCasFemme')
        titleCase = request.POST.get('titleCase')

        # Check if required fields are present
        if not (menage and appliquer_questionnaire and name_femme and numero_tel_femme and age_femme and scolarite_femme and genre_probleme and description_cas_femme):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)

        # Check if the uploaded file is an image
        if form_file:
            if not form_file.content_type.startswith('image/'):
                return JsonResponse({'message': 'Erreur : Le fichier doit \être une image.'}, status=400)

        # Save to the database
        Femme.objects.create(
            menage=menage,
            appliquer_questionnaire=appliquer_questionnaire,
            name_femme=name_femme,
            numero_tel_femme=numero_tel_femme,
            form_file=form_file,
            age_femme=age_femme,
            scolarite_femme=scolarite_femme,
            genreProbleme=genre_probleme,
            titleCase=titleCase,
            descriptionCasFemme=description_cas_femme,
            user=request.user
        )

        return JsonResponse({'message': f'Les infos sur la femme : {name_femme} ont été enregistrées avec succes.'}, status=201)

    else:
        selected_user_id = request.GET.get('userCollector')
        selected_user_object = None
        if request.user.groups.filter(name='collecter').exists():
            entries = Femme.objects.filter(user=request.user)
            # if the user is not a collector
        else:
            entries = Femme.objects.all()
            if selected_user_id:
                entries = entries.filter(user_id=selected_user_id)
                selected_user_object = UserProfile.objects.get(
                    pk=selected_user_id)

        is_supervisor = request.user.groups.filter(name='supervisor').exists()

        paginator = Paginator(entries, 5)
        page_number = request.GET.get('page')
        femmes_entries = paginator.get_page(page_number)
        context = {
            'femmesEntries': femmes_entries,
            'Allusers': UserProfile.objects.all(),
            'is_supervisor': is_supervisor,
            'selected_user_object': selected_user_object
        }
        return render(request, 'collectdata/femmes.html', context)


@login_required
def collectiondata(request):
    return render(request, 'welcome/tableau-de-bord.html')


@login_required
def boiteSuggestion(request):

    if request.method == 'POST':
        topic = request.POST.get('topic')
        message = request.POST.get('message')

        # Check if required fields are present
        if not (topic and message):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)

        # Save to the database
        Sugestion.objects.create(
            topic=topic,
            message=message
        )
        return JsonResponse({'message': f'Information sur {topic} envoyée avec succès'}, status=201)
    else:

        context = {
            'is_supervisor': request.user.groups.filter(name='supervisor').exists(),
            'sugestions': Sugestion.objects.all()
        }

    return render(request, 'suggestion/index.html', context)


@login_required
def agents(request):
    context = {
        'utilisateurs': UserProfile.objects.all()
    }
    return render(request, 'account/utilisateurs.html', context)


def problems(request):
    if request.method == 'POST':
        genre_probleme = request.POST.get('genreProbleme')
        date_probleme = request.POST.get('dateProblem')
        time_probleme = request.POST.get('dateProblemTime')
        titreProbleme = request.POST.get('titreProbleme')
        description_cas_probleme = request.POST.get('descriptionCasProblem')
        province_cas_probleme = request.POST.get('provinceCasProblem')
        precision_endroit_probleme = request.POST.get(
            'precisionEndroitProblem')
        anticipation_aide = request.POST.get('anticipationAide')
        acteur_cause_probleme = request.POST.get('acteurCauseProbleme')
        appliquer_questionnaire = request.POST.get('appliquerQuestionnaire')
        presumes_acteurs = request.POST.get('presumesActeurs')
        problem_victiomes = request.POST.get('problemVictiomes')
        consequences_problemes = request.POST.get('consequencesProblemes')
        images_preuves_probleme = request.FILES.get('imagesPreuvesProblem')

        problemData = Problem(
            user=request.user,
            genre_probleme=genre_probleme,
            date_probleme=date_probleme,
            titreProbleme=titreProbleme,
            time_probleme=time_probleme,
            description_cas_probleme=description_cas_probleme,
            province_cas_probleme=province_cas_probleme,
            precision_endroit_probleme=precision_endroit_probleme,
            anticipation_aide=anticipation_aide,
            acteur_cause_probleme=acteur_cause_probleme,
            appliquer_questionnaire=appliquer_questionnaire,
            presumes_acteurs=presumes_acteurs,
            problem_victiomes=problem_victiomes,
            consequences_problemes=consequences_problemes,
            images_preuves_probleme=images_preuves_probleme,
        )
        problemData.save()
        return JsonResponse({'message': 'Informations sur le problème créé avec succès.'}, status=201)
    else:
        selected_user_id = request.GET.get('userCollector')
        selected_user_object = None
        if request.user.groups.filter(name='collecter').exists():
            entries = Problem.objects.filter(user=request.user)
            # if the user is not a collector
        else:
            entries = Problem.objects.all()
            if selected_user_id:
                entries = entries.filter(user_id=selected_user_id)
                selected_user_object = UserProfile.objects.get(
                    pk=selected_user_id)

        is_supervisor = request.user.groups.filter(name='supervisor').exists()

        paginator = Paginator(entries, 5)
        page_number = request.GET.get('page')
        problem_entries = paginator.get_page(page_number)
        context = {
            'problemEntries': problem_entries,
            'Allusers': UserProfile.objects.all(),
            'is_supervisor': is_supervisor,
            'selected_user_object': selected_user_object
        }
        return render(request, 'collectdata/problems.html', context)


User = get_user_model()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        title = data['title']
        province = data['province']
        city = data['city']
        role = data['role']
        email = data['email']
        username = data['username']
        phone = data['phone']
        password = data['password']

        if not (name and title and province and city and role and email and password):
            return JsonResponse({'message': 'Erreur : Tous les champs sont requis.'}, status=400)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                title=title,
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
