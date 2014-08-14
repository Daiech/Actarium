#encoding:utf-8
from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from libs.generic_managers import GenericManager

from libs.thumbs import ImageWithThumbsField
from uuslug import uuslug
from datetime import datetime  

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


class OrganizationsManager(GenericManager):
    def get_by_slug(self, slug):
        return self.get_active_or_none(slug=slug)


class Organizations(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="org_slug")
    description = models.TextField(blank=True, max_length=100)
    image_path = ImageWithThumbsField(upload_to="orgs_img", sizes=settings.ORG_IMAGE_SIZE, verbose_name="org_image", null=True, blank=True, default=settings.ORG_IMAGE_DEFAULT)
    
    is_archived = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = OrganizationsManager()

    def get_short_icon(self):
        """it should return a 50x50 icon"""
        return self.image_path.url_50x50

    @models.permalink
    def get_absolute_url(self):
        return ('show_org', (), {'slug_org': self.slug})

    def get_num_members(self):
        return self.organizationsuser_organization.filter(role__code="is_member", is_active=True).count()

    def get_group(self, **kwargs):
        return self.get_groups().filter(**kwargs).first()

    def get_groups(self):
        return self.groups_org.filter(is_active=True)

    def get_my_groups(self, user):
        return [g for g in self.get_groups() if rel_user_group.objects.get_rel(user, g)]

    def delete_from_all_approvers_list(self, user):
        """Elimina a user de todas las listas de comisión aprobatoria"""
        list_minutes_full_signeded = [] #  Lista con todas las actas que pasaron a estar aprobadas y que deben ser notificadas al correo de todos los miembros
        for ug in self.get_my_groups(user):
            for m in ug.minutes_id_group.filter(is_full_signed=False):
                a = m.rel_user_minutes_signed_id_minutes.all()
                for approve in a.filter(id_user=user, is_signed_approved=False):
                    approve.delete()
                count = 0
                for ap in a:
                    count = count + 1 if ap.is_signed_approved else count
                if count == a.count(): # "esta acta se debe aprobar (full signed = True)"
                    m.set_full_signed()
                    list_minutes_full_signeded.append(m) # Agregar a la lista para que se notifique
        return list_minutes_full_signeded

    def delete_from_all_groups(self, user):
        for ug in self.get_my_groups(user):
            for rel in ug.rel_user_group_set.filter(id_user=user):
                rel.delete() ## Elimina todas las relaciones de un usuario en un grupo

    def has_user_role(self, user, role):
        qs = self.organizationsuser_organization.filter(role__code=role, user=user, is_active=True)
        if qs.count() > 0:
            return True
        else:
            return False

    def get_members(self):
        return self.organizationsuser_organization.get_members()

    def delete_role(self, user, **kwargs):
        for arg in kwargs:
            role = OrganizationsRoles.objects.get_or_none(code=str(arg), is_active=True)
            if role:
                obj = OrganizationsUser.objects.get_or_none(user=user, organization=self, role=role)
                if obj:
                    obj.is_active = False
                    obj.save()
                else:
                    print "Este man no tiene ese rol:", role
                    return False

    def set_role(self, user, **kwargs):
        objs_created = 0
        roles_not_added = []
        for arg in kwargs:
            role = OrganizationsRoles.objects.get_or_none(code=str(arg), is_active=True)
            if role:
                obj, created = OrganizationsUser.objects.get_or_create(user=user, organization=self, role=role)
                if created:
                    objs_created += 1
                obj.is_active = True
                obj.save()
                print obj, "////////////"
            else:
                roles_not_added.append(str(arg))          
        if objs_created < len(kwargs):
            print "[WARNING] NO SE ASIGNARON TODOS LOS ROLES"
            print "Roles not added", roles_not_added
            #error log

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(Organizations, self).save(*args, **kwargs)

    def is_expired(self):
        from datetime import date
        org = self.organizationservices_organization.all()[0]
        date_expiration = org.service.date_expiration
        days_apart_delta = date_expiration - date.today()
        days_apart = days_apart_delta.days
        if days_apart < 0:
            return True
        else:
            return False

    is_expired = property(is_expired)

    def __unicode__(self):
        return self.name


class GroupsManager(GenericManager):
    def get_group(self, **kwargs):
        g = self.get_or_none(is_active=True, **kwargs)
        if g:
            return g
        else:
            raise Http404


class Groups(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Nombre"))
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True)
    image_path = ImageWithThumbsField(upload_to="groups_img", sizes=settings.GROUP_IMAGE_SIZE, verbose_name=_("Imagen"), null=True, blank=True, default=settings.GROUP_IMAGE_DEFAULT)

    organization = models.ForeignKey(Organizations, null=False, related_name='%(class)s_org')

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = GroupsManager()

    def get_num_members(self):
        """Calculate from relations"""
        return rel_user_group.objects.filter(id_group=self).count()
    
    def get_num_minutes(self):
        return self.minutes_id_group.count()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.organization)
    
    @models.permalink
    def get_absolute_url(self):
        return ('show_home', (), {'slug_group': self.slug})

    def get_short_icon(self):
        """it should return a 50x50 icon"""
        return self.image_path.url_50x50()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(Groups, self).save(*args, **kwargs)  # reemplazado
        
    def is_creator(self, user):
        if self.id_creator == user:
            return True
        else:
            return False

    def get_minutes_by_code(self, **kwargs):
        from apps.groups_app.models import minutes
        try:
            return minutes.objects.get(id_group=self.pk, **kwargs)
        except minutes.DoesNotExist:
            return None
        except Exception, e:
            print "Error get_minutes_by_code: %s" % e
            return None
    
    def get_slug_last_template(self):
        minute = self.minutes_id_group.last()
        if minute:
            return minute.id_template.slug
        return ""



class RelUserGroupManager(GenericManager):
    def get_rel(self, user, group):
        return self.filter(id_user=user, id_group=group, is_active=True)
    def get_all_members_active(self):
        return self.filter(is_active=True, is_member=True)


class rel_user_group(models.Model):
    """Relaciona roles a un usuario con un grupo"""
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_user_invited = models.ForeignKey(User, blank=True, null=True, default=None, related_name='%(class)s_id_user_invited')
    id_group = models.ForeignKey(Groups)
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_convener = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)


    objects = RelUserGroupManager()

    def __unicode__(self):
        return "%s, %s is_admin: %s " % (self.id_group.name, self.id_user, self.is_admin)


class OrganizationsRoles(models.Model):
    code = models.CharField(max_length=100, verbose_name=_(u"Código"))
    name = models.CharField(max_length=150, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.name)
    
    objects = GenericManager()


class OrganizationsUserManager(GenericManager):

    def get_members(self):
        users = []
        for u in self.get_all_active().filter(role__code="is_member").order_by("-user__is_active", "user__username"):
            users.append(u.user.id)
        return User.objects.filter(id__in=users).order_by("-is_active", "username")

    def get_org(self, **kwargs):
        for k,v in kwargs.iteritems():
            kwargs["organization__" + k] = v
            del kwargs[k]
        orgs = self.filter(**kwargs)
        if orgs:
            return orgs[0].organization
        else:
            return None

    def get_orgs_by_role_code(self, role, is_archived=False):
        orgs = []
        for org in self.filter(role__code=role, is_active=True): # OrganizationsUser objects
            orgs.append(org.organization.id)
        return Organizations.objects.filter(id__in=orgs, is_active=True, is_archived=is_archived) # Organizations Objects


class OrganizationsUser(models.Model):    
    user = models.ForeignKey(User, related_name='%(class)s_user')
    role = models.ForeignKey(OrganizationsRoles, related_name='%(class)s_role')
    organization = models.ForeignKey(Organizations, related_name='%(class)s_organization')

    objects = OrganizationsUserManager()
    
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "@%s %s in %s" % (self.user, self.role.code, self.organization)

    class Meta:
        unique_together = ('user', 'role', 'organization')
