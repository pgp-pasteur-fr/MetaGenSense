from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from views.galaxy_views import workflow_datasets, galaxydir_to_dataset, galaxy_history_detail, download_file
from views.galaxy_views import export_output, save_file_information, galaxy_history_list, get_galaxy_dataset,remove_library_dataset
from views.galaxy_launch_workflow_views import launch_workflow
from views.run_workflow import run_workflow_list
from views.galaxy_user_views import galaxy_user_update, galaxy_users

from django.conf import settings

print settings.WORKFLOW_MANAGEMENT_SYSTEM

urlpatterns = patterns('',
    #url(r'^workflows/$', Launch_workflow.as_view(),name='workflows'),
    url(r'^workflows/$', RedirectView.as_view(url= settings.WORKFLOW_MANAGEMENT_SYSTEM.lower()+'/' ),name='workflows'),
    url(r'^workflows/run_workflow_list/$', run_workflow_list, name="run_workflow_list"  ),
    
    #url to use galaxy
    url(r'^workflows/galaxy/$', workflow_datasets, name="galaxy_workflow"),
    url(r'^workflows/galaxy/import_galaxydir/$', galaxydir_to_dataset, name="import_galaxydir"),
    url(r'^workflows/galaxy/remove_library_dataset/(?P<dataset_id>[\w-]+)$', remove_library_dataset, name="remove_library_dataset"), 
    url(r'^workflows/galaxy/launch/$',launch_workflow, name='galaxy_workflow_launch'),
    url(r'^workflows/galaxy/account', galaxy_user_update.as_view(), name="galaxy_account"),
    url(r'^workflows/galaxy/users', galaxy_users.as_view(), name="galaxy_users"),
    url(r'^workflows/galaxy/download/(?P<file_id>[\w-]+)$',download_file, name="galaxy_download_file"),
    url(r'^workflows/galaxy/export/(?P<file_id>[\w-]+)$', export_output, name="galaxy_export_output"),
    url(r'^workflows/galaxy/save/(?P<file_id>[\w-]+)$', save_file_information, name="galaxy_save_file"),
    url(r'^workflows/galaxy/histories/$', galaxy_history_list,name="galaxy_history_list"),
    url(r'^workflows/galaxy/history/(?P<history_id>[\w-]+)$', galaxy_history_detail, name="galaxy_history_detail"),
    
    #AJAX
    url(r'^workflows/galaxy_dataset/', get_galaxy_dataset, name="galaxy_dataset"),
    )

    
    
