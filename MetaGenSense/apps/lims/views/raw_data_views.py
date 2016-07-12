from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from project_views import project_required
from ..forms import RawDataForm, UploadFileForm
from ..models import RawData, LibraryPreparation, FileInformation


@project_required
@login_required
def add(request, project=None):
    """add raw file informations"""
    
    raw_data_form = RawDataForm(request.POST or None)
    raw_data_form.fields['raw_data_file'].queryset = FileInformation.objects.filter(project__name=project)
    raw_data_form.fields['library_preparation'].queryset = LibraryPreparation.objects.filter(sample__project__name=project)  
    
    if raw_data_form.is_valid():
        # raw_data = raw_data_form.cleaned_data        
        # library = LibraryPreparation.objects.get(library_id=raw_data['library_preparation'])
        raw_data_form.save()
        return redirect('raw_data_list')

    return render (request, 'data_files/raw_data/add.html', {
                                               'raw_data_form':raw_data_form,
                                                })
   

@project_required
@login_required
def detail(request, project, pk):
    """display raw data information"""
    
    raw_data = RawData.objects.get(pk=pk)
    raw_data_form = RawDataForm(instance=raw_data)
    raw_data_form.fields['raw_data_file'].queryset = FileInformation.objects.filter(project__name=project)
    raw_data_form.fields['library_preparation'].queryset = LibraryPreparation.objects.filter(sample__project__name=project)  

    return render(request, 'data_files/raw_data/detail.html', {'raw_data_form':  raw_data_form,
                                                                'raw_data':raw_data, }
                                                                )

@project_required
@login_required
def edit(request, project, pk):
    """edit raw data information"""
    
    raw_data = RawData.objects.get(pk=pk)
    raw_data_form = RawDataForm(request.POST or None, instance=raw_data)
    raw_data_form.fields['raw_data_file'].queryset = FileInformation.objects.filter(project__name=project)
    raw_data_form.fields['library_preparation'].queryset = LibraryPreparation.objects.filter(sample__project__name=project)  
    
    if raw_data_form.is_valid():
        raw_data_form.save()
        return redirect('raw_data_detail', pk=raw_data.pk)
    
    return render(request, 'data_files/raw_data/add.html', {'raw_data_form': raw_data_form,
                                                            'raw_data':raw_data, })


@project_required
@login_required
def projectRawDataList(request, project):
         
    raw_data_list = RawData.objects.filter(library_preparation__sample__project__name=project)

    return render(request, 'data_files/raw_data/list.html', {'raw_data_list':raw_data_list}) 






def handle_uploaded_file(f, path):
    
    with open(path + f.name, 'w+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        
    
def uploadFile (request):
    """upload file """   
 
    upload_readform = UploadFileForm()
    
    # Handle file upload                 
    if request.method == "POST":             
        form = UploadFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print request.FILES['fileread']
            handle_uploaded_file(request.FILES['fileread'].path, "/tmp/")
            
            return render (request, 'success_upload.html', {'file_uploaded':request.FILES.get('fileread')})

        else:
            return HttpResponseRedirect('/upload')
                            
    return render (request, 'upload_file.html', {"upload_readform": upload_readform})

