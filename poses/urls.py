from django.urls import path
from . import views


app_name = "poses"

urlpatterns = [
    path('submit/', views.BatchPoseAPIView.as_view(), name="submit"),
]