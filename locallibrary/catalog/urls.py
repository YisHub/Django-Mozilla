from django.urls import path
from . import views

urlpatterns = [
    path('mi-url/', views.mi_vista, name='mi_vista'),
]