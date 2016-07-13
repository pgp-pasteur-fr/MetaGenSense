from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, RedirectView

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'MetaGenSense.views.home', name='home'),
    # url(r'^MetaGenSense/', include('MetaGenSense.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
       
    # Uncomment the next line to enable the admin:
    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps':sitemaps}),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^$',RedirectView.as_view(url='home/'), name='home'),
                       url(r'^home/$',login_required(TemplateView.as_view(template_name="home.html"))),

                       url(r'^', include('MetaGenSense.apps.usermanagement.urls')),
                       url(r'^', include('MetaGenSense.apps.lims.urls')),
                       url(r'^', include('MetaGenSense.apps.workflow.urls')),
                       url(r'^', include('MetaGenSense.apps.analyse.urls')),
                       url(r'^about$', TemplateView.as_view(template_name='about.html'),name='about'),
                       url(r'^WIP', TemplateView.as_view(template_name='WIP.html'),name='WIP')

                       , )