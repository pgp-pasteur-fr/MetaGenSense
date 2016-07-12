from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

# from views import create_account

urlpatterns = patterns('',
                       # url(r'^profile/$',login_required(TemplateView.as_view(template_name="profile.html"))),
                       # url(r'^create_account/$', create_account),
                       url(r'^login/$', login, {'template_name': "login.html"}),
                       url('logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}),
                       url(r'^success', TemplateView.as_view(template_name='success.html'))
                       )
