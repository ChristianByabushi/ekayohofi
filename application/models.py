from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class AccountType(models.TextChoices):
    SUPERVISOR = 'SUPERVISOR', 'Supervisor'
    ADMIN = 'ADMIN', 'Admin'
    COLLECTOR = 'COLLECTOR', 'Collector'
    USER = 'USER', 'User'


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class UserProfile(AbstractUser):
    avatar = models.ImageField(
        upload_to='images/users/', default='static/assets/img/avatar.png')
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, null=True)
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.OTHER)
    account_type = models.CharField(
        max_length=10, choices=AccountType.choices, default=AccountType.USER)
    province = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, null=True, default='Null')
    adresse = models.TextField(default='Not defined') 
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None


class Femme(models.Model):
    MENAGE_CHOICES = [
        ('Bushwira', 'Bushwira'),
        ('Mbobero', 'Mbobero'),
        ('Kagabi', 'Kagabi')
    ]

    GENERE_PROBLEMS = [
        ('Financier', 'Financier'),
        ('Social', 'Social'),
        ('Culturel', 'Culturel'),
        ('Grossesse', 'Grossesse'),
    ]

    APPLIQUER_CHOICES = [
        ('1ère fois', '1ère fois'),
        ('2e fois', '2e fois'),
        ('3e fois', '3e fois')
    ]

    SCOLARITE_CHOICES = [
        ('Jamais scolarisée', 'Jamais scolarisée'),
        ('Primaire', 'Primaire'),
        ('Secondaire', 'Secondaire'),
        ('Universitaire/Supérieur', 'Universitaire/Supérieur')
    ]
    menage = models.CharField(max_length=20, choices=MENAGE_CHOICES)
    appliquer_questionnaire = models.CharField(
        max_length=20, choices=APPLIQUER_CHOICES)
    name_femme = models.CharField(max_length=100)
    numero_tel_femme = models.CharField(max_length=20)
    form_file = models.ImageField(
        upload_to='femme_images/', blank=True, null=True)
    age_femme = models.IntegerField()
    scolarite_femme = models.CharField(
        max_length=50, choices=SCOLARITE_CHOICES)
    genreProbleme = models.CharField(
        max_length=50, null=True, choices=GENERE_PROBLEMS)
    descriptionCasFemme = models.TextField()
    titleCase = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_femme

    def get_image_url(self):
        if self.form_file:
            return self.form_file.url
        return None


class Problem(models.Model):
    GENRE_CHOICES = [
        ('Financier', 'Financier'),
        ('Social', 'Social'),
        ('Culturel', 'Culturel'),
    ]

    PROVINCE_CHOICES = [
        ('Bukavu', 'Bukavu'),
        ('Kabare', 'Kabare'),
        ('Walungu', 'Walungu'),
        ('Fizi', 'Fizi'),
        ('Mwenga', 'Mwenga'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    genre_probleme = models.CharField(max_length=20, choices=GENRE_CHOICES)
    date_probleme = models.DateField()
    date_post = models.DateField(auto_now_add=True)
    time_probleme = models.TimeField()
    titreProbleme = models.TextField(null=False, blank=False)
    description_cas_probleme = models.TextField()
    province_cas_probleme = models.CharField(
        max_length=20, choices=PROVINCE_CHOICES)
    precision_endroit_probleme = models.CharField(max_length=255)
    anticipation_aide = models.TextField()
    acteur_cause_probleme = models.CharField(max_length=255)
    appliquer_questionnaire = models.TextField()
    presumes_acteurs = models.TextField()
    problem_victiomes = models.TextField()
    consequences_problemes = models.TextField()
    images_preuves_probleme = models.ImageField(
        upload_to='problem_images/', blank=True, null=True)

    def __str__(self):
        return self.titreProbleme

    def get_image_url(self):
        if self.images_preuves_probleme:
            return self.images_preuves_probleme.url
        return None


class Action(models.Model):
    BENEFICIARY_CHOICES = [
        ('Infrascture', 'Infrascture'),
        ('soutien-cas-violence', 'Soutien cas de violence'),
        ('incendie', 'Incendie'),
        ('formation', 'Formation'),
        ('construction-batiment', 'Construction Batiment'),
        ('construction-route', 'Construction Routes'),
        ('autres-dons', 'Autres dons'),
    ]

    beneficiary = models.CharField(max_length=255)
    date_action = models.DateField()
    description_action = models.TextField()
    cost_estimated = models.DecimalField(max_digits=10, decimal_places=2)
    action_type = models.CharField(max_length=50, choices=BENEFICIARY_CHOICES)
    image_actions = models.ImageField(
        upload_to='actions/', blank=True, null=True)

    def __str__(self):
        return f"{self.beneficiary} - {self.action_type}"

    def get_image_url(self):
        if self.image_actions:
            return self.image_actions.url
        return None

    def decriptionSliced(self):
        return self.description_action[:100]
