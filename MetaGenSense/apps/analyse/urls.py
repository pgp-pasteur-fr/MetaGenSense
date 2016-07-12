from django.conf.urls import patterns, url
from django.contrib import admin

from views import list_files, display, delete_file_info, download

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^analyse/$', list_files, name='analyse'),                
     url(r'^analyse/(?P<project>[\w|\W-]+)/$', list_files, name='project_analyse'),
     url(r'^analyse/(?P<project>[\w|\W-]+)/(?P<id>[\w-]+)/download', download, name='analyse_file_download'),
     url(r'^analyse/(?P<project>[\w|\W-]+)/(?P<id>[\w-]+)/delete$', delete_file_info, name='file_info_confirm_delete'),
     url(r'^analyse/(?P<project>[\w|\W-]+)/(?P<id>[\w-]+)$', display, name='analyse_file_display'),
          
     #url(r'^analyse/(?P<path>.*)$', 'django.views.static.serve', {
     #       'document_root': settings.MEDIA_ROOT+'/analyse/', 'show_indexes': True})       
      )