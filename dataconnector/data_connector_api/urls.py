from django.urls import path
from . import views

urlpatterns = [
    path('wallstreetsurvivor/', views.wallstreetsurvivor_view, name='wallstreetsurvivor_view'),
]