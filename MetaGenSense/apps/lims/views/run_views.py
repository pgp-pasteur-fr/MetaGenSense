from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import RunForm
from ..models import Run, LibraryPreparation
from project_views import project_required


@project_required
@login_required
def add(request, project):
    """add Run information"""
    
    run_form = RunForm(request.POST or None)
    # selectionne et revois dans le formulaire uniquement les libraries prep du project
    run_form.fields["lib_prep"].queryset = LibraryPreparation.objects.filter(sample__project__name=project)
    
    if run_form.is_valid():
        run = run_form.save()
        run_form = run_form.cleaned_data
        for lib in run_form['lib_prep']:
            lib.run = run
            lib.save()
        
        return redirect('run_detail', run_id=run.run_id)
 
    return render (request, 'run/add.html', {'run_form': run_form })


@project_required
@login_required
def edit (request, project, run_id):   
    """edit run"""

    run = get_object_or_404(Run, run_id=run_id)
    run_form = RunForm(request.POST or None, instance=run)
    
    # selectionne et revois dans le formulaire uniquement les libraries prep du project
    run_form.fields["lib_prep"].initial = LibraryPreparation.objects.filter(run=run).values_list('id', flat=True)  # list selected 
    run_form.fields["lib_prep"].queryset = LibraryPreparation.objects.filter(sample__project__name=project)
    
    if request.method == 'POST':
        
        if run_form.is_valid():
            run_form.save()
            run_form = run_form.cleaned_data
            for lib in run_form['lib_prep']:
                lib.run = run
                lib.save()
           
            return redirect('run_detail', run_id=run.run_id)
        
    return render(request, 'run/add.html', {'run_form': run_form})


@project_required
@login_required
def detail (request, project, run_id):
    """display run information"""
    
    run = get_object_or_404(Run, run_id=run_id)
    run_form = RunForm(instance=run)
    run_form.fields["lib_prep"].queryset = LibraryPreparation.objects.filter(sample__project__name=project)
    run_form.fields["lib_prep"].initial = LibraryPreparation.objects.filter(run=run).values_list('id', flat=True)  # list selected 
 
    return render(request, 'run/detail.html', {'run_form':run_form, })


@project_required
@login_required
def projectRunList(request, project):
    """return la liste des run sans librairy ou avec au moins une librairy du project """  
        
    run_list = Run.objects.filter(Q(librarypreparation__sample__project__name=project) | Q(librarypreparation=None)).distinct()
    # run_list = Run.objects.filter( librarypreparation__sample__project__name = project)
    
    return render(request, 'run/list.html', {'runs':run_list })
    

