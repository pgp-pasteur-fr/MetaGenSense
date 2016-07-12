# -*- coding: Utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from ..models import RunWorkflow


@login_required
def run_workflow_list (request):
    """return  list of run workflows
    """
    run_workflow = RunWorkflow.objects.filter(project_id__subscribers__username=request.user)
    
    return render_to_response("workflows_histories_ajax.html", {'run_workflow_list':run_workflow})
