#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters

class group_type(models.Model):
    name = models.CharField(max_length = 150, verbose_name="name")
    description = models.TextField(blank = True)
    date_added = models.DateTimeField()
    
    def __unicode__(self):
        return "%s "%(self.name)

class groups(models.Model):
    name = models.CharField(max_length = 150, verbose_name="name")
    organization = models.CharField(max_length = 150, verbose_name="organization")
    img_group = models.CharField(max_length = 150, verbose_name="image",default="img/groups/default.jpg")
    id_creator = models.ForeignKey(User,  null=True, related_name='%(class)s_id_creator')
    date_joined = models.DateTimeField(auto_now=True)
    description = models.TextField(blank = True)
    is_active = models.BooleanField(default=True)
    id_group_type = models.ForeignKey(group_type, null=True, related_name = '%(class)s_id_group_type')
    slug = models.SlugField(max_length=150,unique=True)
    
    def __unicode__(self):
        return "%s "%(self.name)
    
    def save(self,*args,**kwargs):
        self.slug = "reemplazame"
        super(groups,self).save(*args,**kwargs)
        self.slug = defaultfilters.slugify(self.name)+"-"+defaultfilters.slugify(self.pk)
        super(groups,self).save(*args,**kwargs)#reemplazado
    
class invitations(models.Model):
    id_user_from = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user_from')
    id_user_to = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user_to')
    id_group = models.ForeignKey(groups)
    date_invited = models.DateTimeField()
    is_active = models.BooleanField()
    
    
class rel_user_group(models.Model):
    id_user = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    
class admin_group(models.Model):
    id_user = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups,  null=True, related_name='%(class)s_id_group')
    date_assigned = models.DateTimeField()
    
class minutes_type_1(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.TextField(blank = True)
    agenda =  models.TextField(blank = True)
    agreement = models.TextField(blank = True)
    
class minutes_type(models.Model):
    name = models.CharField(max_length = 150 , verbose_name = "name")
    descritpion = models.TextField(blank = True)
    date_added = models.DateTimeField()
    id_creator = models.ForeignKey(User,  null=True, related_name='%(class)s_id_creator')
    is_public = models.BooleanField()
    is_customized = models.BooleanField()
    
    def __unicode__(self):
        return "%s "%(self.name)
    
class minutes(models.Model):
    id_creator = models.ForeignKey(User,  null=True, related_name='%(class)s_id_creator')    
    date_created = models.DateTimeField()
    id_group = models.ForeignKey(groups,  null=True, related_name='%(class)s_id_group')
    id_extra_minutes = models.ForeignKey(minutes_type_1,  null=True, related_name='%(class)s_id_extra_minutes')
    id_type = models.ForeignKey(minutes_type,  null=True, related_name='id_minutes_type')
    is_public = models.BooleanField()
    is_full_signed = models.BooleanField()
    code = models.IntegerField()
    
    
class feddback(models.Model):
    id_user = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user')
    title = models.CharField(max_length = 150, verbose_name="title")
    comment = models.TextField(blank = True)
    date = models.DateTimeField()
    
    def __unicode__(self):
        return "%s "%(self.title)
    
class action(models.Model):
    name = models.CharField(max_length = 150, verbose_name = "name")
    description = models.TextField(blank = True)
    date_created = models.DateTimeField()
    
    def __unicode__(self):
        return "%s "%(self.name)
    
class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=True, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(action,  null=True, related_name='%(class)s_id_action')
    date_done = models.DateTimeField()
    
