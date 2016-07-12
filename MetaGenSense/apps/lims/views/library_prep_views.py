from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from project_views import project_required
from ..forms import LibraryPreparationForm
from ..models import LibraryPreparation, Sample


@project_required
@login_required
def add(request, project):
    """add sample_prep information"""
    
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

@project_required
@login_required    
def detail(request, project, library_id) :
    """show detail sample"""
    
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

@project_required
@login_required
def projectLibraryPrepList(request, project):
    """return the samples list of the  project"""
    
    libs_prep = LibraryPreparation.objects.filter(sample__project=my_project)
    return render(request, 'library_prep/list.html', {'libraries':libs_prep}) 

