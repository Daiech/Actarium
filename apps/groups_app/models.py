#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.conf import settings
from django.http import Http404
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from uuslug import uuslug
from actarium_apps.organizations.models import Groups
from libs.generic_managers import GenericManager
from libs.thumbs import ImageWithThumbsField
from south.modelsinspector import add_introspection_rules
add_introspection_rules(
    [
        (
            (ImageWithThumbsField, ),
            [],
            {
                "verbose_name": ["verbose_name", {"default": None}],
                "name":         ["name",         {"default": None}],
                "width_field":  ["width_field",  {"default": None}],
                "height_field": ["height_field", {"default": None}],
                "sizes":        ["sizes",        {"default": None}],
            },
        ),
    ],
    ["^libs\.thumbs\.ImageWithThumbsField",])


class MinutesManager(GenericManager):
    def get_minute(self, **kwargs):
        m = self.get_or_none(**kwargs)
        if m:
            return m
        else:
            raise Http404

class AssistanceManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None

class CommissionManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None    



class minutes_type_1(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.TextField(blank=True)
    agreement = models.TextField(blank=True)
    agenda = models.TextField(blank=True)
    type_reunion = models.CharField(max_length=150, blank=True)

    extra1 = models.TextField(blank=True, null=True)
    extra2 = models.TextField(blank=True, null=True)
    extra3 = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s en %s" % (self.date_start, self.location)


class minutes_type(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    id_creator = models.ForeignKey(User,  null=False, related_name='%(class)s_id_creator')
    is_public = models.BooleanField(default=False)
    is_customized = models.BooleanField()

    def __unicode__(self):
        return u"minutes_type name: %s " % (self.name)


class templates(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Nombre"))
    logo = ImageWithThumbsField(upload_to="client_logos", sizes=settings.CLIENT_LOGO_SIZE, verbose_name=_(u"Logo"), null=True, blank=True, default=settings.CLIENT_LOGO_DEFAULT, help_text=_(u"La imagen debe ser superior a 200x70 px"))
    address_template = models.CharField(max_length=150, verbose_name=_(u"Dirección del HTML"))
    address_js = models.CharField(max_length=150, verbose_name=_(u"Dirección del JS"))
    address_css = models.CharField(max_length=150, default="groups/minutesTemplates/empty_style.css", verbose_name=_(u"Dirección del CSS"))
    address_css4pdf = models.CharField(max_length=150, default="pdfmodule/default_css4pdf.css", verbose_name=_(u"Dirección del CSS para exportar a PDF"))
    id_type = models.ForeignKey(minutes_type,  null=False, related_name='id_minutes_type', verbose_name=_("Tipo de plantilla"))
    is_public = models.BooleanField(default=True, verbose_name=_(u"Es pública?"), help_text=_(u"Las plantillas públicas las puede usar cualquier usuario"))
    date_joined = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True, help_text=_(u"Se le agregará un identificador único después de guardado."))

    def show_logo(self):
        return u'<img src="{}" alt="{}" >'.format(self.logo.url_110x40, self.name)
    show_logo.allow_tags = True

    def __unicode__(self):
        return u"Plantilla: %s " % (self.name)

    class Meta:
        verbose_name = "Templates: Plantilla"
        verbose_name_plural = "Templates: Plantillas"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(templates, self).save(*args, **kwargs)


class rel_user_private_templates(models.Model):
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user', verbose_name=_(u"Usuario"))
    id_template = models.ForeignKey(templates, null=False, related_name='%(class)s_id_templates', verbose_name=_(u"Plantilla"))
    date_joined = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Templates: Relación Usuario-plantilla_privada"
        verbose_name_plural = "Templates: Relación Usuario-plantilla_privada"


class private_templates(models.Model):
    id_template = models.ForeignKey(templates, null=False, related_name='%(class)s_id_templates')
    id_group = models.ForeignKey(Groups, null=False, related_name='%(class)s_id_group')
    id_user = models.ForeignKey(User, null=False, related_name='%(class)s_id_user')
    date_joined = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s => %s: by %s" % (self.id_group.name, self.id_template.name, self.id_user.username)

    class Meta:
        verbose_name = "Templates: Relación Grupo-plantilla_privada"
        verbose_name_plural = "Templates: Relación Grupo-plantilla_privada"
        unique_together = ('id_template', 'id_group')


class minutes(models.Model):
    id_group = models.ForeignKey(Groups, null=False, related_name='%(class)s_id_group')
    id_creator = models.ForeignKey(User, null=False, related_name='%(class)s_id_creator')
    date_created = models.DateTimeField(auto_now_add=True)
    id_extra_minutes = models.IntegerField(max_length=5)
    id_template = models.ForeignKey(templates,  null=False, related_name='id_minutes_type')
    is_valid = models.BooleanField(default=True)
    is_full_signed = models.BooleanField(default=False)
    code = models.CharField(max_length=150, verbose_name="code")

    objects = MinutesManager()

    def get_data_as_json(self):
        """Retorna los datos de un Acta. Busca que tipo de acta es para retornar los datos correctos."""
        id_minutes_type = self.id_template.id_type.pk
        if id_minutes_type == 1: #reinion
            try:
                data = minutes_type_1.objects.get(id=self.id_extra_minutes)
                minutes_data = {
                    "date_start": data.date_start,
                    "date_end": data.date_end,
                    "location": data.location,
                    "agreement": data.agreement,
                    "agenda": data.agenda,
                    "type_reunion": data.type_reunion,
                    "code": self.code,
                    "extra1": data.extra1,
                    "extra2": data.extra2,
                    "extra3": data.extra3,
                }
            except minutes_type_1.DoesNotExist:
                minutes_data = None
        elif id_minutes_type == 2:  # para actas antiguas
            try:
                data = last_minutes.objects.get(id=self.id_extra_minutes)
                minutes_data = {
                    "address_file": MEDIA_URL + "lastMinutes/" + str(data.address_file).split("/")[len(str(data.address_file).split("/")) - 1],
                    "name_file": data.name_file}
            except last_minutes.DoesNotExist:
                minutes_data = None
        elif id_minutes_type == 3:
            print "NO hay tres tipos de actas todavia"
        return minutes_data

    def minutesIsValid(self):
        return self.is_valid
    minutesIsValid.admin_order_field = 'date_created'
    minutesIsValid.boolean = True
    minutesIsValid.short_description = 'is valid?'

    def minutesIsFullSigned(self):
        return self.is_minute_full_signed()
    minutesIsFullSigned.admin_order_field = 'date_created'
    minutesIsFullSigned.boolean = True
    minutesIsFullSigned.short_description = 'is full signed?'

    def set_full_signed(self):
        self.is_full_signed = True
        self.save()

    def is_minute_full_signed(self):
        all_signs = rel_user_minutes_signed.objects.filter(id_minutes=self)
        if all_signs:
            total = all_signs.aggregate(total=Sum("is_signed_approved"))
            if total["total"] == all_signs.count():
                return True
            else:
                return False

    def get_commision_email_list(self, **kwargs):
        '''Retorna una lista con los correos de la comisión aprobatoria.'''
        try:
            group_list = self.rel_user_minutes_signed_id_minutes.filter(**kwargs)
            mails = []
            for member in group_list:
                mails.append(member.id_user.email)
            return mails
        except:
            return None

    def show_dni(self):
        try:
            rgd = rel_minutes_dni.objects.get(id_minutes=self)
            return rgd.show_dni
        except:
            return False

    def get_president_and_secretary(self):
        from apps.groups_app.minutes import getPresidentAndSecretary
        member_president, member_secretary = getPresidentAndSecretary(self.id_group, self)
        try:
            _dni_president = DNI.objects.get(id_user=member_president.id_user)
            president = {"user": member_president, "dni": _dni_president.dni_value, "dni_type": _dni_president.dni_type.short_name}
        except:
            president = {"user": member_president, "dni": "", "dni_type": ""}
        try:
            _dni_secretary = DNI.objects.get(id_user=member_secretary.id_user)
            secretary = {"user": member_secretary, "dni": _dni_secretary.dni_value, "dni_type": _dni_secretary.dni_type.short_name}
        except:
            secretary = {"user": member_secretary, "dni": "", "dni_type": ""}
        return president, secretary

    def get_list_signers(self):
        from apps.groups_app.minutes import getMembersSigners
        m_signers = getMembersSigners(self.id_group, self)
        list_ms = []
        list_temp = []
        i = 0
        for m in m_signers:
            try:
                _dni = DNI.objects.get(id_user=m.id_user)
                list_temp.append({"signer": m, "dni": _dni.dni_value, "dni_type": _dni.dni_type.short_name})
            except:
                list_temp.append({"signer": m, "dni": "", "dni_type": ""})
            if i >= 1:
                i = 0
                list_ms.append(list_temp)
                list_temp = []
            else:
                i = i + 1
        if i == 1:
            list_ms.append(list_temp)
        return list_ms

    def render_as_string(self):
        from apps.groups_app.minutes import getMembersAssistance
        m_assistance, m_no_assistance = getMembersAssistance(self.id_group, self)
        president, secretary = self.get_president_and_secretary()
        ctx = {
                "URL_BASE": settings.URL_BASE,
                "newMinutesForm": self.get_data_as_json(),
                "group": self.id_group,
                "members_selected": m_assistance,
                "members_no_selected": m_no_assistance,
                "members_signers": self.get_list_signers(),
                "url_logo": self.id_template.logo.url,
                "president": president,
                "secretary": secretary,
                "show_dni": self.show_dni(),
                "template": self.id_template
            }
        return render_to_string(self.id_template.address_template, ctx)

    def get_css4pdf(self):
        return render_to_string(self.id_template.address_css4pdf)

    @models.permalink
    def get_absolute_url(self):
        return ('show_minute', (), {'slug_group': self.id_group.slug, 'minutes_code': self.code})

    def save(self):
        self.code = self.code.replace(" ","-")
        super(minutes, self).save()
    
    def __unicode__(self):
        return u"Code: %s, Extra Minutes: %s" % (self.code, self.id_extra_minutes)

    class Meta:
        unique_together = ('id_group', 'code')

    

    def get_total_tasks(self):
        return self.lastminutestasks_minutes.get_tasks().count()
        

    def get_total_tasks_done(self):
        lms =  self.lastminutestasks_minutes.get_tasks()
        done = 0
        for lm in lms:
            if lm.task.status_code == "TER":
                done += 1
        return done

    def get_total_tasks_due(self):
        lms =  self.lastminutestasks_minutes.get_tasks()
        due = 0
        for lm in lms:
            if lm.task.status_code == "VEN":
                due += 1
        return due

    def get_tasks_progress(self):
        total = self.get_total_tasks()
        done = self.get_total_tasks_done()
        if total == 0:
            return 0
        percentage = int(round(100*float(done)/float(total)))
        return percentage

class reunions(models.Model):
    id_convener = models.ForeignKey(User, null=False, related_name='%(class)s_id_convener')
    date_convened = models.DateTimeField(auto_now=True)
    date_reunion = models.DateTimeField()
    locale = models.CharField(max_length=150, verbose_name="locale")
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
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
        return u"'%s' del '%s'" % (self.date_reunion, self.id_group.name)


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
    objects = AssistanceManager()

    def __unicode__(self):
        return u"%s: assistance %s in %s" % (self.id_user.username, self.assistance, self.id_minutes.code)


class rel_user_minutes_signed(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_minutes = models.ForeignKey(minutes,  null=False, related_name='%(class)s_id_minutes')
    is_signed_approved = models.IntegerField()  # take 0, 1, or 2
    date_joined = models.DateTimeField(auto_now=True)
    objects = CommissionManager()

    def __unicode__(self):
        return u"%s signed %s in minutes: %s" % (self.id_user.username, self.is_signed_approved, self.id_minutes.code)


class last_minutes(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    address_file = models.FileField(upload_to=settings.MEDIA_ROOT + "/lastMinutes", max_length=400)
    name_file = models.CharField(max_length=350, verbose_name="name_file")

    def __unicode__(self):
        return u"Minutes: %s" % (self.name_file)


class rol_user_minutes(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    id_minutes = models.ForeignKey(minutes, blank=True, null=True, default=None, related_name='%(class)s_id_minutes')
    is_president = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_signer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    objects = GenericManager()

    def set_assistance(self):
        if self.id_minutes:
            assistance_obj, created = rel_user_minutes_assistance.objects.get_or_create(id_user=self.id_user, id_minutes=self.id_minutes)
            if assistance_obj:
                assistance_obj.assistance = self.is_assistant
                assistance_obj.save()

    def change_commission(self):
        if self.id_minutes:
            if self.is_approver:
                commission_obj = rel_user_minutes_signed.objects.get_or_none(id_user=self.id_user, id_minutes=self.id_minutes)
                if commission_obj:
                    commission_obj.is_signed_approved = True
                    commission_obj.save()
                else:
                    rel_user_minutes_signed.objects.create(id_user=self.id_user, id_minutes=self.id_minutes, is_signed_approved=False)
            else:
                commission_obj = rel_user_minutes_signed.objects.get_or_none(id_user=self.id_user, id_minutes=self.id_minutes)
                if commission_obj:
                    commission_obj.delete()
            ifs = "is_minute_full_signed:", self.id_minutes.is_minute_full_signed()
            if ifs:
                self.id_minutes.set_full_signed = True
                self.id_minutes.save()


    def get_minutes_signed(self):
        try:
            signed = self.id_minutes.rel_user_minutes_signed_id_minutes.get(id_user=self.id_user)
        except Exception, e:
            print e
            signed = None
        if signed:
            return signed.is_signed_approved
        else:
            return None
    
    def __unicode__(self):
        return u"user: %s is_active: %s" % (self.id_user, self.is_active)


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
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    date_added = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=1, verbose_name="state", default="0")  # 0: Sin responder,  1:Aceptado, 2:rechazado
    id_requester = models.ForeignKey(User,  null=False, related_name='%(class)s_id_requester')


class rel_group_dni(models.Model):
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
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
