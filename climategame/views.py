from django.shortcuts import render
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
            # we have a worker taking the task so log the assignment
            hit_assignment, created = HITAssignment.objects.get_or_create(hit=hits[0], worker_id=workerId, assignment_id=assignment_id)
            hit_assignment_uuid = hit_assignment.id

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
    if assignment is not None:
        if assignment_uuid != previewId:
            return render(request, 'climategame/demographics.html', {'assignment_uuid': assignment_uuid})
        else:
            return render(request, 'climategame/demographics.html', {'assignment_uuid': previewId})
    else:
        return render(request, 'climategame/assignment_error.html')