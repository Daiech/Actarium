#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from Actarium import settings


class GroupsManager(models.Manager):
    def my_groups(self, user):
        return self.filter(id_creator=user)

class group_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "tipo de grupo: %s " % (self.name)


class groups(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    organization = models.CharField(max_length=150, verbose_name="organization")
    img_group = models.CharField(max_length=150, verbose_name="image", default="img/groups/default.jpg")
    id_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_creator')
    date_joined = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_pro = models.BooleanField(default=False)
    id_group_type = models.ForeignKey(group_type, null=False, related_name='%(class)s_id_group_type')
    slug = models.SlugField(max_length=150, unique=True)
    objects = GroupsManager()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.id_creator)

    def save(self, *args, **kwargs):
        self.slug = "reemplazame"
        super(groups, self).save(*args, **kwargs)
        self.slug = defaultfilters.slugify(self.name) + "-" + defaultfilters.slugify(self.pk)
        super(groups, self).save(*args, **kwargs)  # reemplazado
        
    def is_creator(self, user):
        if self.id_creator == user:
            return True
        else:
            return False

    def get_minutes_by_code(self, **kwargs):
        try:
            return minutes.objects.get(id_group=self.pk, **kwargs)
        except minutes.DoesNotExist:
            return None
        except Exception, e:
            print "Error get_minutes_by_code: %s" % e
            return None


class invitations(models.Model):
    id_user_from = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_from')
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    email_invited = models.CharField(max_length=60, null=False)
    date_invited = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class invitations_groups(models.Model):
    id_user_from = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_from')
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    id_user_invited = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user_invited')
    date_invited = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "from: %s, to: %s, is_active : %s " % (self.id_user_from, self.id_user_invited, self.is_active)


class rel_user_group(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_user_invited = models.ForeignKey(User, blank=True, null=True, default=None, related_name='%(class)s_id_user_invited')
    id_group = models.ForeignKey(groups)
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_convener = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s, %s is_admin: %s " % (self.id_group.name, self.id_user, self.is_admin)

    class Meta:
        ordering = ['-id_group__is_pro', 'id']


class minutes_type_1(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.TextField(blank=True)
    agreement = models.TextField(blank=True)
    agenda = models.TextField(blank=True)
    type_reunion = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return "%s en %s" % (self.date_start, self.location)


class minutes_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    id_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_creator')
    is_public = models.BooleanField(default=False)
    is_customized = models.BooleanField()

    def __unicode__(self):
        return "minutes_type name: %s " % (self.name)


class templates(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    address_template = models.CharField(max_length=150, verbose_name="address_template")
    address_js = models.CharField(max_length=150, verbose_name="address_js")
    id_type = models.ForeignKey(minutes_type,  null=False, related_name='id_minutes_type')
    is_public = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __unicode__(self):
        return "Plantilla: %s " % (self.name)

    def save(self, *args, **kwargs):
        self.slug = "reemplazame"
        super(templates, self).save(*args, **kwargs)
        self.slug = defaultfilters.slugify(self.name) + "-" + defaultfilters.slugify(self.pk)
        super(templates, self).save(*args, **kwargs)


class rel_user_private_templates(models.Model):
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user')
    id_template = models.ForeignKey(templates, null=False, related_name='%(class)s_id_templates')
    date_joined = models.DateTimeField(auto_now=True)


class private_templates(models.Model):
    id_template = models.ForeignKey(templates, null=False, related_name='%(class)s_id_templates')
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user')
    date_joined = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s => %s: by %s" % (self.id_group.name, self.id_template.name, self.id_user.username)

    class Meta:
        unique_together = ('id_template', 'id_group')


class minutes(models.Model):
    id_group = models.ForeignKey(groups, null=False, related_name='%(class)s_id_group')
    id_creator = models.ForeignKey(User, null=False, related_name='%(class)s_id_creator')
    date_created = models.DateTimeField(auto_now=True)
    id_extra_minutes = models.IntegerField(max_length=5)
    id_template = models.ForeignKey(templates,  null=False, related_name='id_minutes_type')
    is_valid = models.BooleanField(default=True)
    is_full_signed = models.BooleanField(default=False)
    code = models.CharField(max_length=150, verbose_name="code")

    def __unicode__(self):
        return "%s,  Extra Minutes: %s" % (self.id_group.name, self.id_extra_minutes)

    def minutesIsValid(self):
        return self.is_valid
    minutesIsValid.admin_order_field = 'date_created'
    minutesIsValid.boolean = True
    minutesIsValid.short_description = 'is valid?'

    def minutesIsFullSigned(self):
        return self.is_full_signed
    minutesIsFullSigned.admin_order_field = 'date_created'
    minutesIsFullSigned.boolean = True
    minutesIsFullSigned.short_description = 'is full signed?'

    class Meta:
        unique_together = ('id_group', 'code')


class reunions(models.Model):
    id_convener = models.ForeignKey(User, null=False, related_name='%(class)s_id_convener')
    date_convened = models.DateTimeField(auto_now=True)
    date_reunion = models.DateTimeField()
    locale = models.CharField(max_length=150, verbose_name="locale")
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    title = models.CharField(max_length=150, verbose_name="title")
    agenda = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)

    def hasMinutes(self):
        try:
            rel_reunion_minutes.objects.get(id_reunion=self.id)
            return True
        except rel_reunion_minutes.DoesNotExist():
            return False
        except Exception:
            return False

    def getMinutes(self):
        try:
            m = rel_reunion_minutes.objects.get(id_reunion=self.id)
            return m.id_minutes
        except rel_reunion_minutes.DoesNotExist():
            return False
        except Exception:
            return False

    def __unicode__(self):
        return "'%s' del '%s'" % (self.date_reunion, self.id_group.name)


class rel_reunion_minutes(models.Model):
    id_reunion = models.ForeignKey(reunions, null=False, related_name='%(class)s_id_reunion')
    id_minutes = models.ForeignKey(minutes, null=False, related_name='%(class)s_id_minutes')


class assistance(models.Model):
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user')
    id_reunion = models.ForeignKey(reunions, null=False, related_name='%(class)s_id_reunion')
    is_confirmed = models.BooleanField(default=False)
    date_confirmed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_user', 'id_reunion')


class rel_user_minutes_assistance(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_minutes = models.ForeignKey(minutes,  null=False, related_name='%(class)s_id_minutes')
    assistance = models.BooleanField(default=False)
    date_assistance = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: assistance %s in %s" % (self.id_user.username, self.assistance, self.id_minutes.code)


class rel_user_minutes_signed(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_minutes = models.ForeignKey(minutes,  null=False, related_name='%(class)s_id_minutes')
    is_signed_approved = models.IntegerField()  # take 0, 1, or 2
    date_joined = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: assistance %s in %s" % (self.id_user.username, self.is_signed_approved, self.id_minutes.code)


# Definicion del modelo para manerjo de roles de usuarios en grupos

class user_role(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.CharField(max_length=150, verbose_name="description")
    date_joined = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)


class groups_permissions(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    code = models.CharField(max_length=150, verbose_name="code")
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)


class rel_role_group_permissions(models.Model):
    id_role = models.ForeignKey(user_role, null=False, related_name='%(class)s_id_role')
    id_group_permission = models.ForeignKey(groups_permissions, null=False, related_name='%(class)s_id_group_permission')


# nueva configuracion para manejo de grupos Pro y finanzas
class packages(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    number_groups_pro = models.IntegerField()
    price = models.CharField(max_length=150, verbose_name="price")
    is_visible = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    time = models.CharField(max_length=3, verbose_name="time")

    def __unicode__(self):
        return "%s" % (self.name)


class billing(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_package = models.ForeignKey(packages,  null=False, related_name='%(class)s_id_package')
    date_request = models.DateTimeField(auto_now=True)
    groups_pro_available = models.IntegerField()
    state = models.CharField(max_length=1, verbose_name="state", default="0")
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    time = models.CharField(max_length=3, verbose_name="time")

    def __unicode__(self):
        return "Factura: %s %s %s" % (self.id_package.name, self.id_user.username, self.state)


class organizations(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    id_admin = models.ForeignKey(User,  null=False, related_name='%(class)s_id_admin')
    logo_address = models.CharField(max_length=150, verbose_name="logo_address")
    description = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_num_members(self):
        return self.id

    def __unicode__(self):
        return "Org: %s" % (self.name)


class groups_pro(models.Model):
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    id_organization = models.ForeignKey(organizations,  null=False, related_name='%(class)s_id_organization')
    id_billing = models.ForeignKey(billing,  null=False, related_name='%(class)s_id_billing')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "Group: %s (%s)" % (self.id_group.name, self.id_group.id_creator)

    def dateOff(self):
        from apps.groups_app.views import dateTimeFormatForm
        import datetime
        return datetime.datetime.now() - self.id_billing.date_end
        # return dateTimeFormatForm(self.id_billing.date_end)


class last_minutes(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    address_file = models.FileField(upload_to=settings.MEDIA_ROOT + "/lastMinutes", max_length=400)
    name_file = models.CharField(max_length=350, verbose_name="name_file")

    def __unicode__(self):
        return "Minutes: %s" % (self.name_file)


class rol_user_minutes(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    id_minutes = models.ForeignKey(minutes, blank=True, null=True, default=None, related_name='%(class)s_id_minutes')
    is_president = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_signer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return "user: %s is_active: %s" % (self.id_user, self.is_active)


class annotations(models.Model):
    """docstring for annotations"""
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_minutes = models.ForeignKey(minutes, blank=True, null=True, default=None, related_name='%(class)s_id_minutes')
    annotation_text = models.TextField(blank=True)
    id_minutes_annotation = models.IntegerField(max_length=5)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class annotations_comments(models.Model):
    """docstring for annotations_comments"""
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_annotation = models.ForeignKey(annotations, blank=True, null=True, default=None, related_name='%(class)s_id_minutes')
    comment = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)


class DNI_type(models.Model):
    short_name = models.CharField(max_length=20, verbose_name="Short Name")
    long_name = models.CharField(max_length=150, verbose_name="Long Name")


class DNI(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    dni_type = models.ForeignKey(DNI_type,  null=False, related_name='%(class)s_dni_type')
    dni_value = models.CharField(max_length=150, verbose_name="dni_value")
    date_added = models.DateTimeField(auto_now=True)


class DNI_permissions(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    date_added = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=1, verbose_name="state", default="0")  # 0: Sin responder,  1:Aceptado, 2:rechazado
    id_requester = models.ForeignKey(User,  null=False, related_name='%(class)s_id_requester')


class rel_group_dni(models.Model):
    id_group = models.ForeignKey(groups,  null=False, related_name='%(class)s_id_group')
    show_dni = models.BooleanField()
    id_admin = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    date_added = models.DateTimeField(auto_now=True)


class rel_minutes_dni(models.Model):
    id_minutes = models.ForeignKey(minutes, null=False, related_name='%(class)s_id_minutes')
    show_dni =  models.BooleanField()
    date_added = models.DateTimeField(auto_now=True)


class minutes_version(models.Model):
    id_minutes = models.ForeignKey(minutes, null=False, related_name='%(class)s_id_minutes')
    id_user_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    full_html = models.TextField()
    date_created = models.DateTimeField(auto_now=True)


class minutes_approver_version(models.Model):
    id_user_approver = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_minutes_version = models.ForeignKey(minutes_version, null=False, related_name='%(class)s_id_minutes')
    date_created = models.DateTimeField(auto_now=True)
    is_signed_approved = models.IntegerField()  # take 0, 1, or 2
