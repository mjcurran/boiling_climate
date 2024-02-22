from django.contrib import admin
from .models import Game, DemographicsQuestion, HumanIntTask, HITAssignment, DemographicsAnswer, EnvironmentalScenario

admin.site.register(Game)
admin.site.register(DemographicsQuestion)
admin.site.register(HumanIntTask)
admin.site.register(HITAssignment)
admin.site.register(EnvironmentalScenario)
admin.site.register(DemographicsAnswer)