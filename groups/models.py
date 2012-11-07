#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters


class group_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s " % (self.name)


class groups(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    organization = models.CharField(max_length=150, verbose_name="organization")
    img_group = models.CharField(max_length=150, verbose_name="image", default="img/groups/default.jpg")
    id_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_creator')
    date_joined = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    id_group_type = models.ForeignKey(group_type, null=False, related_name='%(class)s_id_group_type')
    slug = models.SlugField(max_length=150, unique=True)

    def __unicode__(self):
        return "%s " % (self.name)

    def save(self, *args, **kwargs):
        self.slug = "reemplazame"
        super(groups, self).save(*args, **kwargs)
        self.slug = defaultfilters.slugify(self.name) + "-" + defaultfilters.slugify(self.pk)
        super(groups, self).save(*args, **kwargs)  # reemplazado


class invitations(models.Model):
    id_user_from = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_from')
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    email_invited = models.CharField(max_length=60, null=False)
    date_invited = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class rel_user_group(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)


class admin_group(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    date_assigned = models.DateTimeField(auto_now=True)


class minutes_type_1(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.TextField(blank=True)
    agreement = models.TextField(blank=True)
    agenda = models.TextField(blank=True)


class minutes_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    descritpion = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    id_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_creator')
    is_public = models.BooleanField()
    is_customized = models.BooleanField()

    def __unicode__(self):
        return "%s " % (self.name)


class minutes(models.Model):
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    date_created = models.DateTimeField(auto_now=True)
    id_extra_minutes = models.ForeignKey(minutes_type_1,  null=True, related_name='%(class)s_id_extra_minutes')
    id_type = models.ForeignKey(minutes_type,  null=False, related_name='id_minutes_type')
    is_valid = models.BooleanField(default=True)
    is_full_signed = models.BooleanField(default=False)
    code = models.CharField(max_length=150, verbose_name="code")

    def __unicode__(self):
        return "id_group: %s, %s, %s" % (self.id_group, date_created, id_extra_minutes)

class reunions(models.Model):
    id_convener = models.ForeignKey(User, null=False, related_name='%(class)s_id_convener')
    date_convened = models.DateTimeField(auto_now=True)
    date_reunion = models.DateTimeField()
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    agenda = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s : %s"%(self.date_reunion,self.id_group)

class rel_reunion_minutes(models.Model):
    id_reunion = models.ForeignKey(reunions, null=False, related_name='%(class)s_id_reunion')
    id_minutes = models.ForeignKey(minutes, null=False, related_name='%(class)s_id_minutes')
    
    
class assistance(models.Model):
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user')
    id_reunion = models.ForeignKey(reunions, null=False, related_name='%(class)s_id_reunion')
    is_comfirmed = models.BooleanField(default=False)
    date_comfirmed = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = ('id_user', 'id_reunion')


class feddback(models.Model):
    id_user = models.ForeignKey(User, null=True, related_name='%(class)s_id_user')
    title = models.CharField(max_length=150, verbose_name="title")
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return "%s "%(self.title)


class action(models.Model):
    name = models.CharField(max_length = 150, verbose_name = "name")
    description = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s "%(self.name)


class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(action,  null=False, related_name='%(class)s_id_action')
    date_done = models.DateTimeField(auto_now = True)
