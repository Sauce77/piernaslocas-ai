from django.urls import path

from . import views

app_name = "sesiones"

urlpatterns = [
    path("historial/<str:username>/", views.mostrar_historial, name="historial"),
]