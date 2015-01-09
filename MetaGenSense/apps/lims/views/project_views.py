from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse , Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from ..forms import ProjectForm
from ..models import Project, Sample


def auth_project(project, user):
    """controle if user can access to project information"""
    import warnings
    warnings.warn("function %s is deprecated" % __name__)
    
    if not project:
        return HttpResponseRedirect('project_list')
    my_project = get_object_or_404(Project, name=project) 
      
    if not my_project.contains(user):
        """user is not authorized to consult this page and it stay invisible"""
        raise Http404
    return my_project


def project_required(func):
    """control if user can access to project information"""
    def wrapper(request, project=None, *args, **kwargs):
        if request.user.is_authenticated():
            
            if not project:
                project = request.session.get('current_project')
                if not project:
                    return redirect('project_list')
            
            if request.user.project_subscriptions.filter(name__contains=project) :
                return func(request, project, *args, **kwargs)
        """user is not authorized to consult this page and it stay invisible"""
        
        raise PermissionDenied
        
    return  wrapper 
    

@login_required
def add (request):
    """ create new project
    """
    project_form = ProjectForm(request.POST or None)
    
    if project_form.is_valid():
        new_project = project_form.save()
           
        return HttpResponseRedirect('../projects')
    
    # customize the object representations    
    project_form.fields['subscribers'].label_from_instance = lambda obj: "%s %s" % (obj.last_name or obj.username, obj.first_name)
    
    return render(request, 'projects/add.html', {'project_form': project_form })


@login_required    
@csrf_protect   
def projectsSubscribed(request):     
        """ Affiche les projets l'utilisateur
        """        
        if request.user.is_authenticated():
            
            if request.is_ajax(): 
                selproject = request.POST.get('select_project')
                try:
                    project = Project.objects.get(name=selproject)
                    if project.contains(request.user):
                        request.session['current_project'] = selproject
                        return HttpResponse(selproject)
                except:
                    selproject = '' 
                    return HttpResponse({"project": selproject})
                      
            subscribed = request.user.project_subscriptions.all()
            return render (request, 'projects/list.html', {"projects_list": subscribed})
        else:
            return HttpResponseRedirect('/profile')
        
           
        
@login_required
@project_required
def detail(request, project):
    """ Affiche le detail du projet de l'utilisateur """  

    samples = Sample.objects.filter(project__name=project)
    request.session['current_project'] = project
    project_obj = Project.objects.get(name=project)
    
    return render(request, 'projects/detail.html', {'project': project_obj,
                                                 'samples_list':samples})

