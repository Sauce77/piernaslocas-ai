from django.urls import path

from . import views

app_name = "sesiones"

urlpatterns = [
    path("", views.mostar_rutinas, name="rutinas"),
    path("historial/<str:username>/", views.mostrar_historial, name="historial"),
]