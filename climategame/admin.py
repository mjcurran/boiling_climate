from django.contrib import admin
from .models import Game, DemographicsQuestion, HumanIntTask, HITAssignment, DemographicsAnswer

admin.site.register(Game)
admin.site.register(DemographicsQuestion)
admin.site.register(HumanIntTask)
admin.site.register(HITAssignment)