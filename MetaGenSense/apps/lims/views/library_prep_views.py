from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import LibraryPreparationForm 
from ..models import LibraryPreparation, Sample
from project_views import auth_project
from project_views import project_required


def add(request):
    """add sample_prep information"""
    
    project = request.session.get('current_project')
    auth_project(project, request.user)
    
    lib_prep_form = LibraryPreparationForm(request.POST or None)
    lib_prep_form.fields["sample"].queryset = Sample.objects.filter(project__name=project)

   
    if lib_prep_form.is_valid():
        
        lib_prep = lib_prep_form.save()
        return render (request, 'library_prep/add.html', {
                                                          'lib_prep_form': lib_prep_form ,
                                                          'success':True,
                                                          'library_prep':lib_prep,
                                                          })
    
    return render (request, 'library_prep/add.html', {
                                               'lib_prep_form': lib_prep_form ,
                                                })
    
def detail(request, library_id):
    """show detail sample"""
    
    project = request.session.get('current_project')
    auth_project (project, request.user)
    
    lib_prep = LibraryPreparation.objects.get(library_id=library_id)
    library_prep_form = LibraryPreparationForm(instance=lib_prep)
    library_prep_form.fields["sample"].queryset = Sample.objects.filter(project__name=project)
    
    return render(request, 'library_prep/detail.html', {'lib_prep_form':library_prep_form,
                                                      'lib_prep':lib_prep })


@project_required
@login_required
def edit(request, project, library_id):
    """edit sample prep"""
       
    library_prep = LibraryPreparation.objects.get(library_id=library_id)
    library_prep_form = LibraryPreparationForm(request.POST or None, instance=library_prep)
    
    # selectionne et revois dans le formulaire uniquement les echantillons du project
    library_prep_form.fields["sample"].queryset = Sample.objects.filter(project__name=project)
    
    if request.method == 'POST':
          
        if library_prep_form.is_valid():
            library_prep_form.save()
           
            return redirect('library_prep_detail', library_id=library_prep.library_id)
        
    return render(request, 'library_prep/add.html', {'lib_prep_form':library_prep_form })


def projectLibraryPrepList(request, project):
    """return the samples list of the  project"""
    
    my_project = auth_project (project, request.user)
    
    if request.user.is_authenticated():
        
        libs_prep = LibraryPreparation.objects.filter(sample__project=my_project)
 
        return render(request, 'library_prep/list.html', {'libraries':libs_prep}) 
                                                           




