# -*- coding: utf-8 -*-
from datetime import datetime    
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def get_file_path(instance, filename):
    # make the filepath include the signed in username
    print "inst: %s" % instance.__dict__.keys()
    print "inst_path:%s" % instance._path
    print "file: %s" % filename
    
    if instance._path:
        return "%s/%s/%s" % (settings.MEDIA_ROOT, instance._path, filename)
    return "%s/%s" % (settings.MEDIA_ROOT, filename)


        
# Lims.core models        
class Project(models.Model):
    """ """
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    date = models.DateField(auto_now_add=True, null=True, blank=True) 
    context = models.CharField(max_length=255L)
    comments = models.TextField(max_length=255L, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name="project_subscriptions")
     
    def __unicode__(self):
        return self.name

    def all_samples(self, Sample):
        return Sample.objects.filter(project_fk=self)
    
    def contains(self, User):
        # take User object return True if the user is subscriber
        return self in User.project_subscriptions.all()
    

class FileInformation(models.Model):
    """ """
    _path = ''
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255L, blank=True)
    format = models.CharField(max_length=255L, null=True, blank=True)
    type = models.CharField(max_length=255L, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    author = models.CharField(max_length=255L, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True, default=datetime.now)
    file_path = models.FileField(upload_to=get_file_path, max_length=255L, null=True, blank=True) 
    project = models.ForeignKey(Project)
           
    def __unicode__(self):
        return '%s' % (self.name)
    
    def save(self, *arg, **kargs):
        
        if not self.size:
            self.size = self.file_path.size
                
        if not self.name:
            self.name = self.file_path.name
        
        if not self.format:
            self.format = os.path.splitext(self.file_path.path)[1]    
 
        
        super(FileInformation, self).save(*arg, **kargs)
        
    def parent_folder(self):
        try :
            if self.file_path:
                return self.file_path.path.rsplit(os.sep, 2)[1]
            else: 
                return "Metadata"  # pas de fichier associer
            
        except IndexError:
            return os.sep
        
        
    def set_path(self, path):        
        self._path = path

    
    class Meta:
        db_table = 'FILE_INFORMATION'         
        
    

class GeographicLocation(models.Model):
    """ """
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(max_length=255, null=True, blank=True)
    
    class Meta:
        unique_together = ("country", "city", "district", "province")
    
    def __unicode__(self): 
        return '%s, %s, %s' % (self.country, self.city, self.district)


class GpsCoords(models.Model):
    
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey(GeographicLocation, null=True, blank=True)
    gps_latitude = models.FloatField(null=True, blank=True)  # D.d
    gps_longitude = models.FloatField(null=True, blank=True)  # D.d
    gps_altitude = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Gps Coords'
        
                        
class Sample(models.Model):
    """ """
    
    project = models.ForeignKey(Project)
    sample_id = models.CharField(unique=True, max_length=32)
    sampling_date = models.DateTimeField(null=True, blank=True)
    reception_date = models.DateTimeField(null=True, blank=True)
    host_origin = models.CharField(max_length=255, null=True, blank=True)
    sample_origin = models.CharField(max_length=255, null=True, blank=True)
    extraction_type = models.CharField(max_length=255, null=True, blank=True)
    extraction_method = models.CharField(max_length=255, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    concentration = models.CharField(max_length=25, null=True, blank=True,)
    assay_method = models.CharField(max_length=25, null=True, blank=True)
    gene_target = models.CharField(max_length=25, null=True, blank=True)
    cycle_threshold = models.FloatField(null=True, blank=True)
    
    location = models.ForeignKey(GeographicLocation, null=True, blank=True)
    gps_coords = models.ForeignKey(GpsCoords, null=True, blank=True)
    
    comments = models.TextField(max_length=255, null=True, blank=True)
    
        
    def __unicode__(self):
        return self.sample_id
    
    
class Technology(models.Model):
    """ """ 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
            
    def __unicode__(self):
        return self.name
  

class Run(models.Model):
    """ """
    id = models.AutoField(primary_key=True)
    run_id = models.CharField(unique=True, max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    device = models.CharField(max_length=255)
    single_end = models.BooleanField(default=False)
    paired_end = models.BooleanField(default=False)
    mate_pair = models.BooleanField(default=False)
    theoretical_read_length = models.IntegerField(null=True, blank=True)
    multiplex = models.BooleanField(default=False)
    comments = models.TextField(max_length=255, null=True, blank=True)
    
    def nb_sample_multiplex(self):
        
        return '%s' % (LibraryPreparation.objects.filter(run=self).count())
    
    def __unicode__(self):
            return '%s' % (self.run_id)
        
        
class LibraryPreparation(models.Model):
    """ """
    
    id = models.IntegerField(primary_key=True) 
    library_id = models.CharField(unique=True, max_length=25, null=True, blank=True)
    technology = models.ForeignKey(Technology, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    sample = models.ForeignKey(Sample)
    library_protocol = models.CharField(max_length=128, null=True, blank=True)
    version_protocol = models.CharField(max_length=12, null=True, blank=True)
    insert_size = models.IntegerField(null=True, blank=True)
    index = models.CharField(max_length=100)
    sample_quantity_used = models.FloatField(null=True, blank=True)
    librairy_concentration = models.FloatField(null=True, blank=True)
    run = models.ForeignKey(Run, null=True, blank=True)
    comments = models.TextField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'LIBRARY_PREPARATION'
        
    def __unicode__(self):
        return '%s' % (self.library_id)
    

class RawData(models.Model): 
    """ """
    
    raw_data_file = models.OneToOneField(FileInformation, related_name='rawdata_info')
    library_preparation = models.ForeignKey(LibraryPreparation, null=True, blank=True)
    comments = models.TextField(max_length=255, null=True, blank=True)


    def __unicode__(self):
        return '%s/%s' % (self.library_preparation.library_id, self.raw_data_file.name)

    
    
    
    
    
    
    
    
    
    
