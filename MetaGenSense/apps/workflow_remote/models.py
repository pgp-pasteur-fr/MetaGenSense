# -*- coding: utf-8 -*-
from django.db import models

from MetaGenSense.apps.lims.models import User, FileInformation, Project
from django.conf import settings

class GalaxyUser(models.Model):
    """
    Modèle pour stocker l'API key de Galaxy de l'utilisateur de MetaGenSense  
    """
    user = models.OneToOneField(User, primary_key=True)
    api_key = models.CharField(max_length=100,blank=True)

    def galaxy_url(self):
        return settings.GALAXY_SERVER_URL

    def __unicode__(self):
        return self.user.username
    
    class Meta:
        db_table = 'GALAXY_USER'


class Workflow(models.Model):
    """
    Modèle qui stock le nom du workflow et ça clé définit par le gestionnaire de workflows.
    Le worflows étant déja descrit par celui-ci
    """
    
    name = models.CharField(max_length=100,blank=True, unique=True)
    wf_key = models.CharField(max_length=100,blank=True)
    comments = models.TextField(max_length=255,null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'WORKFLOW'


class RunWorkflow(models.Model):
    """
    Modèle qui permet une tracabilité entre les données et le workflow utilisé
    """
    
    date = models.DateField(auto_now_add=True, blank=True )
    name = models.CharField(max_length=100,blank=True, unique=True)
    workflow_id = models.ForeignKey(Workflow)
    comments = models.TextField(max_length=255,null=True, blank=True)

    project_id =  models.ForeignKey(Project) #Lims
    
    def __unicode__(self):
        return "%s, launched at %s" %(self.name,self.date)
    
    class Meta:
        db_table = 'RUN_WORKFLOW'


class WorkflowData(models.Model):
    """
    Gestion des données d'entrées et de sorties pour l'execution d'un workflow
    """
    
    data = models.ForeignKey(FileInformation)
    id_run_wf = models.ForeignKey(RunWorkflow)
    
    input = models.IntegerField(blank=True)
    output = models.IntegerField(blank=True)
    
    class Meta:
        db_table = 'WORKFLOW_DATA'
        
    def __unicode__(self):
        return self.data.name
       
    def parent_folder(self):
        return self.data.parent_folder()
    
          
    
    
