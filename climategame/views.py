from django.shortcuts import render
import random
import json
from .models import *

# if a worker is previewing a task the assignment_id will be "ASSIGNMENT_ID_NOT_AVAILABLE"
# make sure we don't save any data in that case
previewId = "ASSIGNMENT_ID_NOT_AVAILABLE"

def intro(request):
    hit_id = request.GET.get('hitId', None)
    assignment_id = request.GET.get('assignmentId', None)
    turk_submit_to = request.GET.get('turkSubmitTo', None)
    workerId = request.GET.get('workerId', None)

    hits = HumanIntTask.objects.filter(hit_id=hit_id)
    if hits.count() == 1:
        hit_assignment_uuid = previewId
        if assignment_id != previewId:
            # we have a worker taking the task so create the assignment
            # randomize scenarios and put in scenario_order column of HITAssignment
            scenarios_list = []
            scenarios = EnvironmentalScenario.objects.all()
            if scenarios.count() == 0:
                for i in [5, 15, 25, 45, 75]:
                    scenario = EnvironmentalScenario(name="Scenario " + str(i), scenario={"rain": i})
                    scenario.save()
                scenarios = EnvironmentalScenario.objects.all()

            for s in scenarios:
                scenarios_list.append(str(s.id))
            random.shuffle(scenarios_list)
            hit_assignment, created = HITAssignment.objects.get_or_create(hit=hits[0], worker_id=workerId, 
                                                                          assignment_id=assignment_id, 
                                                                          scenario_order=json.dumps(scenarios_list))
            hit_assignment_uuid = hit_assignment.id
        # vars other than assignment_id are for debug only
        return render(request, 'climategame/intro.html', {'assignment_uuid': hit_assignment_uuid, 'hit_id': hit_id, 'assignment_id': assignment_id, 'turk_submit_to': turk_submit_to, 'worker_id': workerId})
    else:
        return render(request, 'climategame/assignment_error.html')

def instructions(request, assignment_uuid):
    # somehow these query parameters are being carried over from the intro page
    # @TODO validate that the assignment is legit.  Handle preview requests
    
    assignment = HITAssignment.objects.get(id=assignment_uuid)
    if assignment is not None:
        return render(request, 'climategame/instructions.html', {'assignment_uuid': assignment_uuid})
    else:
        return render(request, 'climategame/assignment_error.html')
    
        
def demographics_survey(request, assignment_uuid):
    assignment = HITAssignment.objects.get(id=assignment_uuid)
    # @TODO validate that the assignment is legit.  Handle preview requests
    if request.method == 'GET':
        if assignment is not None:
            questions = DemographicsQuestion.objects.all()
            if assignment_uuid != previewId:
                return render(request, 'climategame/demographics.html', {'assignment_uuid': assignment_uuid, 'questions': questions})
            else:
                return render(request, 'climategame/demographics.html', {'assignment_uuid': previewId, 'questions': questions})
        else:
            return render(request, 'climategame/assignment_error.html')
        
    if request.method == 'POST':
        #this starts the new game
        if assignment is not None:
            for key in request.POST:
                if key != "csrfmiddlewaretoken":
                    question = DemographicsQuestion.objects.get(id=key)
                    if question is not None:
                        answer = request.POST[key]
                        demographics_answer = DemographicsAnswer(assignment=assignment, demographics_question=question, answer=answer)
                        demographics_answer.save()
            # create a new game round here
            scenario_order = json.loads(assignment.scenario_order)
            scenario = EnvironmentalScenario.objects.get(id=scenario_order[0])
            game_round, created = RoundSelection.objects.get_or_create(assignment=assignment, scenario=scenario, round=1)
            return render(request, 'climategame/game.html', {'assignment_uuid': assignment_uuid, 'round': 1, 'current_year': game_round, 'previous_year': game_round})
        else:
            return render(request, 'climategame/assignment_error.html')
        
def game(request, assignment_uuid):
    # submit round data and go the to next round
    assignment = HITAssignment.objects.get(id=assignment_uuid)
    
    if request.method == 'GET':
        # for if the user has to reload the page for some reason?
        # try to find the most recent round
        latest_round = RoundSelection.objects.filter(assignment=assignment).order_by('-timestamp').first()
        if assignment is not None and latest_round is not None:
            if latest_round.round > 1:
                previous_round = RoundSelection.objects.get(assignment=assignment, round=latest_round.round-1)
            return render(request, 'climategame/game.html', {'assignment_uuid': assignment_uuid, 'round': latest_round.round, 'current_year': latest_round, 'previous_year': previous_round})
            #return render(request, 'climategame/game.html', {'assignment_uuid': assignment_uuid, 'round': latest_round.round, 'current_year': latest_round})
        else:
            return render(request, 'climategame/assignment_error.html')
        
    if request.method == 'POST':
        if assignment is not None:
            round = request.POST['round']
            crop = request.POST['crop'] # bool
            technology = request.POST['technology'] # bool
            game_round = RoundSelection.objects.get(assignment=assignment, round=round)
            if game_round is not None:
                game_round.crop = crop
                game_round.technology = technology
                game_round.save()
                # @TODO check round number in case we are done with the scenario, or need to insert an attention check
                new_round, created = RoundSelection.objects.get_or_create(assignment=assignment, round=round+1)
                return render(request, 'climategame/game.html', {'assignment_uuid': assignment_uuid, 'round': new_round.round, 'current_year': new_round, 'previous_year': game_round})
            else:
                return render(request, 'climategame/assignment_error.html')
        else:
            return render(request, 'climategame/assignment_error.html')