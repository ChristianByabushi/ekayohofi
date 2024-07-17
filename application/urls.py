from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.index, name="index"),
    path("collect-donnees/", views.collectiondata, name="collectiondata"),
    path("boites-a-suggestion/", views.boiteSuggestion, name="boiteSuggestion"),
    path("assistances/", views.handleWomen, name="assistances"),
    path("femmes/", views.handleWomen, name="women"),
    path("faq/", views.handleWomen, name="faq"),
    path("dons/", views.handleWomen, name="dons"),
    path("crimes/", views.handleWomen, name="crimes"),
    path("rapports/", views.boiteSuggestion, name="rapports"),
    path("agents-amis-mama-ni-mama/", views.agentsAmis, name="agentAmis"), 
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.login,
         name="login"),
    path("sign-up/", views.signup,
         name="signup"),
    # path("", views.messaging, name="contact-us"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
