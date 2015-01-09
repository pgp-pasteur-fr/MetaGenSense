from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django.forms.widgets import DateInput

from models import Sample, LibraryPreparation, Project, FileInformation, GeographicLocation, GpsCoords, Run, RawData, User


class ProjectForm(ModelForm):  
     
    date = forms.DateField(widget=DateInput(attrs={"id":"id_creation_date"}))
    subscribers = forms.ModelMultipleChoiceField(queryset=User.objects.order_by('last_name'),
                                                 widget=FilteredSelectMultiple("Subscribers",
                                                                               False,
                                                                               attrs={'rows':'10'}
                                                                               ))

    class Meta:
        model = Project
        exclude =('id',)
        
class RunForm(ModelForm):   
    
        
    lib_prep = forms.ModelMultipleChoiceField(queryset=LibraryPreparation.objects.none(),
                                              label=('Libraries'),
                                              widget=FilteredSelectMultiple("Libraries", False, attrs={'rows':'10'}))
    class Meta:
        model = Run
        exclude = ('id',)

class LibraryPreparationForm(ModelForm):
    
    class Meta:
        model = LibraryPreparation
        exclude = ('id', 'run')
                        
                
class SampleForm(ModelForm):
    
    
    class Meta:
        model = Sample
        exclude = ('location', 'gps_coords')
                      

class FileInformationForm(ModelForm):
        
    class Meta:
        model = FileInformation
        fields = ('name', 'format', 'type', 'file_path')
        

class RawDataForm(ModelForm):
        
    raw_data_file = forms.ModelChoiceField(queryset=FileInformation.objects.none(), label="File name")    
    
    class Meta:
        model = RawData
        fields = ('raw_data_file', 'library_preparation', 'comments')


class GeographicLocationForm(ModelForm):      
       
    class Meta:
        model = GeographicLocation
        exclude =('id',)

class GpsCoordsForm(ModelForm):      
       
    class Meta:
        model = GpsCoords
        exclude = ('location',)

class RawDataListForm(forms.Form):
    
    rawdata = forms.ModelMultipleChoiceField(queryset=RawData.objects.all())



class UploadFileForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False)
    fileread = forms.FileField(label='read', widget=forms.FileInput())

class QuickAnalysisForm(forms.Form):
    
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    fileread = forms.FileField(label='FastQ', widget=forms.FileInput())
    creation_date = forms.DateField(widget=AdminDateWidget, required=True)
    
    # widgets = {'creation_date':AdminDateWidget(attrs={"type":"date"}),}

             
