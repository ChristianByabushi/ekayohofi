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
    path("collect-donnees/femmes/", views.femmes, name="femme"),
    path("faq/", views.handleWomen, name="faq"),
    path("mon-profile/", views.profile, name="profile"),
    path("dons/", views.handleWomen, name="dons"),
    path("collect-donnees/problems/", views.problems, name="problems"),
    path("collect-donnees/actions/", views.actions, name="actions"),
    path("collect-donnees/download/action-excel-data/",
         views.action_download_excel, name="actionExcelData"),
    path("rapports/", views.boiteSuggestion, name="rapports"),
    path("agents-ekayehofi/", views.agents, name="utilisateurs"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.login,
         name="login"),
    path("sign-up/", views.signup,
         name="signup"),

    # path("", views.messaging, name="contact-us"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
