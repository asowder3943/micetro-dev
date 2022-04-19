from django.urls import include, path
from prototype.views import *

urlpatterns = [
    path('home', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('cage/<int:cage_id>/', cage_measurement, name="cage_measurement"),
    path('experiment/<int:experiment_id>/', experiment_home , name="experiment_home"),
    path('bulk_add/<int:experiment_id>/', bulk_add , name="bulk_add"),
    path('volume_match/<int:experiment_id>/', volume_match , name="volume_match"),
]