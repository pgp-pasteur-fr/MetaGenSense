from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

from project_views import project_required
from ..forms import GpsCoordsForm, SampleForm, GeographicLocationForm
from ..models import Sample, Project, GeographicLocation, GpsCoords


@project_required
@login_required 
def add(request, project):
    """add sample information"""
    

    projects=Project.objects.filter(name=project)
    sample_form = SampleForm(request.POST or None)
    sample_form.fields["project"].queryset = projects
    sample_form.fields["project"].initial = projects[0].id #1st project selected
    
    
    location_form = GeographicLocationForm(request.POST or None)
    gps_form = GpsCoordsForm(request.POST or None)
    
    if sample_form.is_valid():
        sample = sample_form.save(commit= False)
        
        if location_form.is_valid():
            location, created = GeographicLocation.objects.get_or_create(**location_form.cleaned_data)
            sample.location = location
           
        if gps_form.is_valid():
            gps, created = GpsCoords.objects.get_or_create(**gps_form.cleaned_data)
            sample.gps_coords = gps

        sample.save()
        
        return HttpResponseRedirect('/sample/%s' % sample.sample_id)


    return render (request, 'samples/add.html', {
                                               'sample_form': sample_form ,
                                               'location_form':location_form,
                                               'gps_form': gps_form,
                                                })
 
   
@project_required
@login_required 
def detail(request, project, id ):
    """show detail sample"""

    sample = Sample.objects.get(sample_id=id)
    sample_form = SampleForm(instance=sample)
    sample_form.fields["project"].queryset = Project.objects.filter(name=project)
    
    return render(request,'samples/detail.html', {'sample':sample, 'sample_form':sample_form } )


@project_required
@login_required  
def edit(request, project, id ):
    """edit sample"""
    
    sample = Sample.objects.get(sample_id=id)
    sample_form = SampleForm(request.POST or None, instance=sample)
    sample_form.fields["project"].queryset = Project.objects.filter(name=project)
    
    location_form = GeographicLocationForm(instance=sample.location)
    gps_form = GpsCoordsForm(instance=sample.gps_coords)
    
    if request.method == 'POST':         
        if sample_form.is_valid():
            sample_form.save()
           
            return redirect('sample_detail', id=sample.sample_id)
    
    return render(request,'samples/add.html', {'sample':sample,
                                               'sample_form':sample_form,
                                               'location_form':location_form,
                                               'gps_form': gps_form
                                                } )


@project_required
@login_required      
def projectSamplesList(request, project):
    """return the samples list of the  project"""
    
    samples = Sample.objects.filter(project__name = project )        
    return render(request,'samples/list.html',   {'samples': samples} )



@login_required  
def samplesList(request):
    """return list of samples"""

    samples = Sample.objects.filter(project__subscribers__username = request.user )
    
    if request.is_ajax():
        return render_to_response("samples/list_ajax.html", {'samples':samples})
       
    return render(request,'samples/list.html',   {'samples': samples} )
            





