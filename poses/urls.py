from django.urls import path
from . import views


app_name = "poses"

urlpatterns = [
    path('submit/', views.BatchPoseAPIView.as_view(), name="submit"),
    path('capturar/ejercicio_1', views.capturar_ejercicio_1, name='capturar_ejercicio_1'),
    path('capturar/ejercicio_2', views.capturar_ejercicio_2, name='capturar_ejercicio_2'),
    path('capturar/ejercicio_3', views.capturar_ejercicio_3, name='capturar_ejercicio_3'),
]