from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(UserProfile)
admin.site.register(Action)
admin.site.register(Femme)
admin.site.register(Problem)