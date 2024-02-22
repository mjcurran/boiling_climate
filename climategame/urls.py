from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("intro/", intro, name="intro"),
    path("instructions/<uuid:assignment_uuid>/", instructions, name="instructions"),
    path("demographics/<uuid:assignment_uuid>/", demographics_survey, name="demographics"),
    path("game/<uuid:assignment_uuid>/", game, name="game"),
]