# -*- coding: Utf-8 -*-
from ..models import GalaxyUser
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, ListView


from ..libs.galaxyModule import SBWGalaxyInstance
from django.conf import settings

class galaxy_user_update(SuccessMessageMixin, UpdateView):
    
    model = GalaxyUser
    template_name = "galaxy/user.html"
    fields = ['api_key', ]
    success_url = 'account'
    success_message = "%(api_key)s Api key was updated successfully"
    
    def get_object(self, queryset=None):
            return get_object_or_404(GalaxyUser, user=self.request.user)
        
        
        
class galaxy_users(ListView):
    """Methode qui permet de recuperer la liste des utilisateur de galaxy pour la gestions des droits unix
    """
    model = GalaxyUser
    template_name = "galaxy/users_list.html"
    fields = ['username', ]
    content_type = 'text/plain'
    
    def get_queryset(self):
        "Verifie si l'api key entree par l'utilisateur est valide"
        galaxy_users = GalaxyUser.objects.exclude(api_key__isnull=True)
        l = []
        for user in galaxy_users :
          
            gi = SBWGalaxyInstance(url=settings.GALAXY_SERVER_URL, key=user.api_key)
            try:
                gu_info = gi.users.get_current_user()
                l.append(gu_info['username'])
            except:
                pass
          
        return set(l)
    
    
        
 
 
 
 
 
 
 
 
 
 
 
