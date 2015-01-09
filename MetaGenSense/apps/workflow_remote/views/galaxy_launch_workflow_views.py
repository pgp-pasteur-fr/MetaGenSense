# -*- coding: Utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
#models
from ..models import Workflow ,RunWorkflow, WorkflowData
from MetaGenSense.apps.lims.models import Project, FileInformation

#decorator
from galaxy_views import connection_galaxy
from MetaGenSense.apps.lims.views.project_views import project_required
from django.contrib.auth.decorators import login_required

@connection_galaxy
@project_required
@login_required
def  launch_workflow(request, project, gi):
    """ 
    soumet l'execution du workflow a Galaxy
    """

    project_obj = Project.objects.get(name=project) 
    dataset_map = dict()

    if request.method == 'POST':
        
        #recuperation des variables POST
        wf_launch = request.POST.get('workflow_id')
        hist_id = request.POST.get('hist_id')
        input_submit = request.POST.getlist('inputs')
        
        #recuperation du noms de l'history
        name_history = gi.histories.show_history(hist_id)['name']
    
        
        #recuperation de la key galaxy pour lancer le workflow
        wf_obj = Workflow.objects.get(id=wf_launch)
        wf_key = wf_obj.wf_key
        
        #verification 1er lancement du workflows
        #Sauvegarde dans la base du workflow lancé dans la base de donnée 
        runWf, created = RunWorkflow.objects.get_or_create(name = name_history,
                                                           workflow_id=wf_obj,
                                                           project_id = project_obj,
                                                            )
        
        if not created:
            messages.warning(request,"Workflow has already run, Please create a new history" )
            return redirect('galaxy_history_detail',history_id=hist_id)
        
        

        #recupere les inputs du worflows
        wf = gi.workflows.show_workflow(wf_key)
        i_inputs = wf['inputs'].keys()
        
        #mappe les inputs du workflow avec les id des fichiers soumis par l'utilisateur
        for i, r in zip(i_inputs,input_submit):
            dataset_map[i] = {'id':r,'src':'hda'}                
                

        #donne l'orde a galaxy de lancer le worflow avec les parametres
        gi.workflows.run_workflow(workflow_id=wf_key, history_id=hist_id, dataset_map=dataset_map)
        
        
        """Sauvegarde du workflow lancé dans la base de donnée"""
        #sauvergarde des inputs selectionnés pour lancer le workflow
        compt = 0
        for r in input_submit:
            compt +=1 
            data = gi.datasets.show_dataset(dataset_id= r)
            
            #cree la metadonnée du fichier utiliser avec le workflow
            #TODO trouver un moyen de discriminer les fichiers autre que par le nom
    
            file_info = FileInformation(name=data['name'],
                            format=data['data_type'],
                            type="",
                            size=data['file_size'],
                            author="",
                            #creation_date="",
                            #file_path="",
                            project = project_obj,                     
                            )
            file_info.save()
            
            #sauvegarde avec quel workflow le fichier a été utilisé
            workflowdata = WorkflowData (data = file_info,
                                       id_run_wf = runWf,
                                       input = compt,
                                       output = 0, 
                                       )
            workflowdata.save()
            
            print  workflowdata 
                 
        return redirect('galaxy_history_detail',history_id=hist_id)
        
    return redirect("galaxy_workflow")  
