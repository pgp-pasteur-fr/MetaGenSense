# -*- coding: utf-8 -*-
import zipfile
from os import path, remove

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms.widgets import SelectMultiple
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from MetaGenSense.apps.lims.models import FileInformation
from MetaGenSense.apps.lims.views.project_views import project_required
from MetaGenSense.apps.workflow.models import WorkflowData
from MetaGenSense.apps.workflow.views.galaxy_views import connection_galaxy


@login_required
@project_required 
@connection_galaxy
def list_files(request, project=None, gi=None):
    """ affiche la liste des fichiers sauvegarder par l'utilisateur """
      
    class PersonalPathForm(forms.Form):
        """fichier dans le repertoire personnel d'export d'output"""
        
        _path = path.join(settings.WK_EXPORT_DIR, gi.roles)   
        personal_files = forms.FilePathField(path=_path , match=project + '_.*',
                                             widget=SelectMultiple)
        
    personal_export_files = PersonalPathForm()
    
    # return les fichiers savegardés dans la base de données
    metadata_files = WorkflowData.objects.filter(data__project__name=project)
    
    return render(request, 'data_files/list.html', { 'files': metadata_files,
                                                     'personal_export_files': personal_export_files})



@login_required
@project_required   
def display(request, project, id):
    """affiche le contenu du fichier via le navigateur de l'utilisateur"""
    
      
    file_obj = get_object_or_404(FileInformation, pk=id)
    
    # decompress le contenu si besoin
    content = ""
    if zipfile.is_zipfile(file_obj.file_path.path):
        # Open zip file
        zipcontent = zipfile.ZipFile(file_obj.file_path.path, 'r')
        # list filenames
        for name in zipcontent.namelist():
            content = zipcontent.open(name)  
              
    else:
        content = open(file_obj.file_path.path)
    
    return StreamingHttpResponse(content)



@login_required
@project_required   
def download(request, project, id):
    """telechargement a partir du serveur de MetaGenSense"""
    
    mfile = get_object_or_404(FileInformation, pk=id)
    
    response = StreamingHttpResponse(open(mfile.file_path.path))
    response['Content-Length'] = mfile.size
    response['Content-Disposition'] = 'attachment; filename=%s' % mfile
    
    return response

@login_required
@project_required  
def delete_file_info(request, project, id):
    """delete file from server and all information in a database""" 
    
    mfile = get_object_or_404(FileInformation, pk=id)
    
    if request.POST:         
        if request.POST.get("confirm") == 'yes' :
            remove(mfile.file_path.path)
            mfile.delete()
    
        return redirect ('analyse')

    return render(request, 'data_files/file_confirm_delete.html', {'object':mfile })
  
  
  
