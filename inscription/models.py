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

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None


class Partenaires(models.Model):
    nomPartenaires = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partenaires/institution/', null=True)


class ImagesCollections(models.Model):
    nomCollectionImages = models.CharField(null=False)
    imageCollected = models.ImageField(
        null=False, upload_to='images/Collections/')


class Institution(models.Model):
    nomInstitution = models.CharField()
    dateCreation = models.CharField(null=False)
    imagesPresentation = models.ManyToManyField(ImagesCollections)
    PrefetOugestionnaire = models.OneToOneField(UserProfile, null=False,
                                                on_delete=models.CASCADE)
    proviseur = models.CharField(null=True)
    # nombresSections=models.CharField() field to be calculated
    partenaires = models.ManyToManyField(Partenaires)
    # nombresProfesseurs = models.CharField() field to be calculated before the asignments of accounts to teachers


class AnneeScolaire(models.Model):
    debutAnnee = models.DateField(null=False)
    finAnnee = models.DateField(null=False)
    description = models.TextField(null=True)


class Option(models.Model):
    nomOption = models.CharField(max_length=100)
    ChefOption = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    debutCreation = models.DateField(null=False)


class Classe (models.Model):
    nomClasse = models.CharField(max_length=50)
    optionClasse = models.OneToOneField(
        Option, on_delete=models.CASCADE, null=False)
    titulaire = models.OneToOneField(
        UserProfile, null=False, on_delete=models.CASCADE)


class Eleve(models.Model):
    nomEleve = models.CharField(max_length=100)
    post_nom = models.CharField(max_length=100)
    nom_pere = models.CharField(max_length=100)
    background = models.CharField(max_length=300)
    nom_de_la_mere = models.CharField(max_length=100)
    dateNaissance = models.DateField(max_length=100)
    genre = models.CharField(
        max_length=50, choices=[
            ('Masculin', 'Masculin'),
            ('Feminin', 'Feminin'),
        ])

    def get_image_url(self):
        if self.form_file:
            return self.form_file.url
        return None


class ClasseAnneAcademique(models.Model):
    descriptionAnnee = models.TextField()
    elevesInscrits = models.ManyToManyField(Eleve)
    anneeScolaire = models.OneToOneField(
        AnneeScolaire, on_delete=models.CASCADE)
    classe = models.OneToOneField(Classe, on_delete=models.CASCADE)
    titulaire = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, null=False)
    chefDeClasse = models.OneToOneField(Eleve, on_delete=models.SET_NULL, null=True) 
