from typing import Any, Iterable
from django.db import models
import uuid
from django.conf import settings
import os
import json
import sys

def default_json():
    return {}

class BusinessModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Game(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    question = models.TextField(blank=True)
    keywords = models.JSONField(default=default_json)

class DemographicsQuestion(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=100)
    question_type = models.CharField(max_length=50)
    options = models.JSONField(default=default_json)

class DemogrphicsQuestionChoices(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(DemographicsQuestion, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100)

class HumanIntTask(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hit_id = models.CharField(max_length=64, blank=True)
    hit_type_id = models.CharField(max_length=64, blank=True)
    turk_submit_to = models.CharField(max_length=100, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hit_layout_id = models.CharField(max_length=64, blank=True)
    hit_layout_parameters = models.JSONField(default=default_json)
    assignment_duration_seconds = models.IntegerField(default=3600)
    auto_approval_delay_seconds = models.IntegerField(default=3600)
    lifetime_seconds = models.IntegerField(default=3600)
    max_assignments = models.IntegerField(default=500)
    qualification_requirements = models.JSONField(default=default_json)
    assignment_review_policy = models.JSONField(default=default_json)
    hit_review_policy = models.JSONField(default=default_json)
    requester_annotation = models.CharField(max_length=100, blank=True)
    unique_request_token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    reward = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default="Assignable") # Assignable, Unassignable, Reviewable

class HITAssignment(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hit = models.ForeignKey(HumanIntTask, on_delete=models.CASCADE)
    worker_id = models.CharField(max_length=64)
    assignment_id = models.CharField(max_length=100)
    turk_submit_to = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, blank=True)  # Submitted, Approved, or Rejected
    answer = models.JSONField(default=default_json)
    scenario_order = models.JSONField(default=default_json)
    
class DemographicsAnswer(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(HITAssignment, on_delete=models.CASCADE)
    demographics_question = models.ForeignKey(DemographicsQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, blank=True)


class EnvironmentalScenario(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(blank=True)
    scenario = models.JSONField(default=default_json)
    
class RoundSelection(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(HITAssignment, on_delete=models.CASCADE)
    scenario = models.ForeignKey(EnvironmentalScenario, on_delete=models.CASCADE)
    round = models.IntegerField(default=1)
    crop = models.BooleanField(default=False)
    technology = models.BooleanField(default=False)
    eor_water_availability = models.CharField(max_length=50)
    eor_crop_income = models.FloatField(default=0.0)
    eor_profit = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)


class AttentionCheckQuestion(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    question_type = models.CharField(max_length=50)
    

class AttentionCheck(BusinessModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(HITAssignment, on_delete=models.CASCADE)
    scenario = models.ForeignKey(EnvironmentalScenario, on_delete=models.CASCADE)
    after_round = models.IntegerField()
    question = models.ForeignKey(AttentionCheckQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    valid_response = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)