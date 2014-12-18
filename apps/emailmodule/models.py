from django.db import models
from django.contrib.auth.models import User
from apps.groups_app.models import Groups


class email_admin_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"tipo de admin: %s " % (self.name)


class email(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    email_type = models.CharField(max_length=150, verbose_name="email_type")
    admin_type = models.ForeignKey(email_admin_type, null=False, related_name='%(class)s_id_email_type')
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"tipo de correo: %s " % (self.name)


class email_group_permissions(models.Model):
    id_group = models.ForeignKey(Groups, null=False, related_name='%(class)s_id_group')
    id_email_type = models.ForeignKey(email, null=False, related_name='%(class)s_id_email_type')
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_from')
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now=True)


class email_global_permissions(models.Model):
    id_email_type = models.ForeignKey(email, null=False, related_name='%(class)s_id_email_type')
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_from')
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now=True)
