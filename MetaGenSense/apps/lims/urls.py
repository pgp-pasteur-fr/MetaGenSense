from django.conf.urls import patterns, url
from django.views.generic import ListView, TemplateView

from models import FileInformation
from views import sample_views, project_views, library_prep_views, run_views, raw_data_views

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
								
	url(r'^lims', login_required(TemplateView.as_view(template_name='lims.html')),name='lims'),
	
	#--- PROJECT ---#
	url(r'^projects/$', project_views.projectsSubscribed, name='project_list'),
	url(r'^projects/add$', project_views.add, name='project_add'),
	url(r'^project/(?P<project>[\w|\W]+)$', project_views.detail,name='project_detail' ),
		
	#--- SAMPLE ---#
	url(r'^sample/add$',sample_views.add, name='sample_add'),
	url(r'^sample/add_success$',sample_views.add),
	url(r'^sample/(?P<id>[\w-]+)$', sample_views.detail, name='sample_detail'),
	url(r'^sample/(?P<id>[\w-]+)/edit$', sample_views.edit, name='sample_edit'),
	url(r'^samples/$', sample_views.samplesList, name= 'sample_list' ),#AJAX
	url(r'^(?P<project>[\w|\W]+)/sample_list/$', sample_views.projectSamplesList, name='project_sample_list' ),
	
	#--- LIBRARY PREP ---#
	url(r'^library_prep/add$',library_prep_views.add ,name='library_prep_add') ,
	url(r'^library_prep/(?P<library_id>[\w-]+)$',library_prep_views.detail,name='library_prep_detail'),
	url(r'^library_prep/(?P<library_id>[\w-]+)/edit$', library_prep_views.edit,name='library_prep_edit'),
	url(r'^(?P<project>[\w|\W]+)/library_prep_list/$', library_prep_views.projectLibraryPrepList, name='project_library_prep_list' ),
	
	#---NGS RUN ---#
	url(r'^run/add$',run_views.add, name='run_add'),
	url(r'^run/(?P<run_id>[\w-]+)$', run_views.detail, name='run_detail'),
	url(r'^run/(?P<run_id>[\w-]+)/edit$',run_views.edit, name='run_edit'),
	url(r'^(?P<project>[\w|\W]+)/run_list/$', run_views.projectRunList, name='project_run_list' ),

	
	#--- RAW DATA ---#
	url(r'^raw_data/add/$', raw_data_views.add, name="raw_data_add"),
	url(r'^raw_data/(?P<pk>[\w-]+)$',raw_data_views.detail,name='raw_data_detail'),
	url(r'^raw_data/(?P<pk>[\w-]+)/edit$', raw_data_views.edit,name='raw_data_edit'),
	url(r'^(?P<project>[\w|\W]+)/raw_data_list/$', raw_data_views.projectRawDataList, name='project_raw_data_list' ),

	#--- DATA --- # 
	url(r'^data_files/$', ListView.as_view(model = FileInformation, template_name='data_files/list.html',), name="data_files_list"),
	url(r'^new_data$',TemplateView.as_view(template_name='new_data.html'),name='new_data'),	
	
	
	url(r'^upload/$',raw_data_views.uploadFile ),
	
	
	)
	