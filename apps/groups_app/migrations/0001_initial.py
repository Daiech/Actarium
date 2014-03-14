# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organizations'
        db.create_table(u'groups_app_organizations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_path', self.gf('libs.thumbs.ImageWithThumbsField')(name='image_path', sizes=((50, 50), (100, 100)), default='img/groups/default.jpg', max_length=100, blank=True, null=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizations_id_admin', to=orm['auth.User'])),
            ('is_archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['Organizations'])

        # Adding model 'Groups'
        db.create_table(u'groups_app_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_path', self.gf('libs.thumbs.ImageWithThumbsField')(name='image_path', sizes=((50, 50), (100, 100)), default='img/groups/default.jpg', max_length=100, blank=True, null=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups_org', to=orm['groups_app.Organizations'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['Groups'])

        # Adding model 'invitations'
        db.create_table(u'groups_app_invitations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitations_id_user_from', to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitations_id_group', to=orm['groups_app.Groups'])),
            ('email_invited', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('date_invited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'groups_app', ['invitations'])

        # Adding model 'invitations_groups'
        db.create_table(u'groups_app_invitations_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitations_groups_id_user_from', to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitations_groups_id_group', to=orm['groups_app.Groups'])),
            ('id_user_invited', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invitations_groups_id_user_invited', to=orm['auth.User'])),
            ('date_invited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'groups_app', ['invitations_groups'])

        # Adding model 'rel_user_group'
        db.create_table(u'groups_app_rel_user_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_group_id_user', to=orm['auth.User'])),
            ('id_user_invited', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rel_user_group_id_user_invited', null=True, blank=True, to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groups_app.Groups'])),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_secretary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_superadmin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_convener', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_user_group'])

        # Adding model 'minutes_type_1'
        db.create_table(u'groups_app_minutes_type_1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agreement', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agenda', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type_reunion', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['minutes_type_1'])

        # Adding model 'minutes_type'
        db.create_table(u'groups_app_minutes_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id_creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_type_id_creator', to=orm['auth.User'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_customized', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'groups_app', ['minutes_type'])

        # Adding model 'templates'
        db.create_table(u'groups_app_templates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('address_template', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('address_js', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('id_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='id_minutes_type', to=orm['groups_app.minutes_type'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
        ))
        db.send_create_signal(u'groups_app', ['templates'])

        # Adding model 'rel_user_private_templates'
        db.create_table(u'groups_app_rel_user_private_templates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_private_templates_id_user', to=orm['auth.User'])),
            ('id_template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_private_templates_id_templates', to=orm['groups_app.templates'])),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_user_private_templates'])

        # Adding model 'private_templates'
        db.create_table(u'groups_app_private_templates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='private_templates_id_templates', to=orm['groups_app.templates'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='private_templates_id_group', to=orm['groups_app.Groups'])),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='private_templates_id_user', to=orm['auth.User'])),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['private_templates'])

        # Adding unique constraint on 'private_templates', fields ['id_template', 'id_group']
        db.create_unique(u'groups_app_private_templates', ['id_template_id', 'id_group_id'])

        # Adding model 'minutes'
        db.create_table(u'groups_app_minutes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_id_group', to=orm['groups_app.Groups'])),
            ('id_creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_id_creator', to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id_extra_minutes', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('id_template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='id_minutes_type', to=orm['groups_app.templates'])),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_full_signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'groups_app', ['minutes'])

        # Adding unique constraint on 'minutes', fields ['id_group', 'code']
        db.create_unique(u'groups_app_minutes', ['id_group_id', 'code'])

        # Adding model 'reunions'
        db.create_table(u'groups_app_reunions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_convener', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reunions_id_convener', to=orm['auth.User'])),
            ('date_convened', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_reunion', self.gf('django.db.models.fields.DateTimeField')()),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reunions_id_group', to=orm['groups_app.Groups'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('agenda', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'groups_app', ['reunions'])

        # Adding model 'rel_reunion_minutes'
        db.create_table(u'groups_app_rel_reunion_minutes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_reunion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_reunion_minutes_id_reunion', to=orm['groups_app.reunions'])),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_reunion_minutes_id_minutes', to=orm['groups_app.minutes'])),
        ))
        db.send_create_signal(u'groups_app', ['rel_reunion_minutes'])

        # Adding model 'assistance'
        db.create_table(u'groups_app_assistance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assistance_id_user', to=orm['auth.User'])),
            ('id_reunion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assistance_id_reunion', to=orm['groups_app.reunions'])),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_confirmed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['assistance'])

        # Adding unique constraint on 'assistance', fields ['id_user', 'id_reunion']
        db.create_unique(u'groups_app_assistance', ['id_user_id', 'id_reunion_id'])

        # Adding model 'rel_user_minutes_assistance'
        db.create_table(u'groups_app_rel_user_minutes_assistance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_minutes_assistance_id_user', to=orm['auth.User'])),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_minutes_assistance_id_minutes', to=orm['groups_app.minutes'])),
            ('assistance', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_assistance', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_user_minutes_assistance'])

        # Adding model 'rel_user_minutes_signed'
        db.create_table(u'groups_app_rel_user_minutes_signed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_minutes_signed_id_user', to=orm['auth.User'])),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_minutes_signed_id_minutes', to=orm['groups_app.minutes'])),
            ('is_signed_approved', self.gf('django.db.models.fields.IntegerField')()),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_user_minutes_signed'])

        # Adding model 'user_role'
        db.create_table(u'groups_app_user_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['user_role'])

        # Adding model 'groups_permissions'
        db.create_table(u'groups_app_groups_permissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['groups_permissions'])

        # Adding model 'rel_role_group_permissions'
        db.create_table(u'groups_app_rel_role_group_permissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_role_group_permissions_id_role', to=orm['groups_app.user_role'])),
            ('id_group_permission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_role_group_permissions_id_group_permission', to=orm['groups_app.groups_permissions'])),
        ))
        db.send_create_signal(u'groups_app', ['rel_role_group_permissions'])

        # Adding model 'packages'
        db.create_table(u'groups_app_packages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('number_groups_pro', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'groups_app', ['packages'])

        # Adding model 'billing'
        db.create_table(u'groups_app_billing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='billing_id_user', to=orm['auth.User'])),
            ('id_package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='billing_id_package', to=orm['groups_app.packages'])),
            ('date_request', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('groups_pro_available', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'groups_app', ['billing'])

        # Adding model 'groups_pro'
        db.create_table(u'groups_app_groups_pro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups_pro_id_group', to=orm['groups_app.Groups'])),
            ('id_organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups_pro_id_organization', to=orm['groups_app.Organizations'])),
            ('id_billing', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='groups_pro_id_billing', null=True, to=orm['groups_app.billing'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'groups_app', ['groups_pro'])

        # Adding model 'last_minutes'
        db.create_table(u'groups_app_last_minutes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_minutes_id_user', to=orm['auth.User'])),
            ('address_file', self.gf('django.db.models.fields.files.FileField')(max_length=400)),
            ('name_file', self.gf('django.db.models.fields.CharField')(max_length=350)),
        ))
        db.send_create_signal(u'groups_app', ['last_minutes'])

        # Adding model 'rol_user_minutes'
        db.create_table(u'groups_app_rol_user_minutes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rol_user_minutes_id_user', to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rol_user_minutes_id_group', to=orm['groups_app.Groups'])),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rol_user_minutes_id_minutes', null=True, blank=True, to=orm['groups_app.minutes'])),
            ('is_president', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_secretary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_approver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_assistant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_signer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'groups_app', ['rol_user_minutes'])

        # Adding model 'annotations'
        db.create_table(u'groups_app_annotations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='annotations_id_user', to=orm['auth.User'])),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='annotations_id_minutes', null=True, blank=True, to=orm['groups_app.minutes'])),
            ('annotation_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id_minutes_annotation', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'groups_app', ['annotations'])

        # Adding model 'annotations_comments'
        db.create_table(u'groups_app_annotations_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='annotations_comments_id_user', to=orm['auth.User'])),
            ('id_annotation', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='annotations_comments_id_minutes', null=True, blank=True, to=orm['groups_app.annotations'])),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'groups_app', ['annotations_comments'])

        # Adding model 'DNI_type'
        db.create_table(u'groups_app_dni_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'groups_app', ['DNI_type'])

        # Adding model 'DNI'
        db.create_table(u'groups_app_dni', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dni_id_user', to=orm['auth.User'])),
            ('dni_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dni_dni_type', to=orm['groups_app.DNI_type'])),
            ('dni_value', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['DNI'])

        # Adding model 'DNI_permissions'
        db.create_table(u'groups_app_dni_permissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dni_permissions_id_user', to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dni_permissions_id_group', to=orm['groups_app.Groups'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('id_requester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dni_permissions_id_requester', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'groups_app', ['DNI_permissions'])

        # Adding model 'rel_group_dni'
        db.create_table(u'groups_app_rel_group_dni', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_group_dni_id_group', to=orm['groups_app.Groups'])),
            ('show_dni', self.gf('django.db.models.fields.BooleanField')()),
            ('id_admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_group_dni_id_user', to=orm['auth.User'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_group_dni'])

        # Adding model 'rel_minutes_dni'
        db.create_table(u'groups_app_rel_minutes_dni', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_minutes_dni_id_minutes', to=orm['groups_app.minutes'])),
            ('show_dni', self.gf('django.db.models.fields.BooleanField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['rel_minutes_dni'])

        # Adding model 'minutes_version'
        db.create_table(u'groups_app_minutes_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_minutes', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_version_id_minutes', to=orm['groups_app.minutes'])),
            ('id_user_creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_version_id_user', to=orm['auth.User'])),
            ('full_html', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groups_app', ['minutes_version'])

        # Adding model 'minutes_approver_version'
        db.create_table(u'groups_app_minutes_approver_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user_approver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_approver_version_id_user', to=orm['auth.User'])),
            ('id_minutes_version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minutes_approver_version_id_minutes', to=orm['groups_app.minutes_version'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_signed_approved', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'groups_app', ['minutes_approver_version'])


    def backwards(self, orm):
        # Removing unique constraint on 'assistance', fields ['id_user', 'id_reunion']
        db.delete_unique(u'groups_app_assistance', ['id_user_id', 'id_reunion_id'])

        # Removing unique constraint on 'minutes', fields ['id_group', 'code']
        db.delete_unique(u'groups_app_minutes', ['id_group_id', 'code'])

        # Removing unique constraint on 'private_templates', fields ['id_template', 'id_group']
        db.delete_unique(u'groups_app_private_templates', ['id_template_id', 'id_group_id'])

        # Deleting model 'Organizations'
        db.delete_table(u'groups_app_organizations')

        # Deleting model 'Groups'
        db.delete_table(u'groups_app_groups')

        # Deleting model 'invitations'
        db.delete_table(u'groups_app_invitations')

        # Deleting model 'invitations_groups'
        db.delete_table(u'groups_app_invitations_groups')

        # Deleting model 'rel_user_group'
        db.delete_table(u'groups_app_rel_user_group')

        # Deleting model 'minutes_type_1'
        db.delete_table(u'groups_app_minutes_type_1')

        # Deleting model 'minutes_type'
        db.delete_table(u'groups_app_minutes_type')

        # Deleting model 'templates'
        db.delete_table(u'groups_app_templates')

        # Deleting model 'rel_user_private_templates'
        db.delete_table(u'groups_app_rel_user_private_templates')

        # Deleting model 'private_templates'
        db.delete_table(u'groups_app_private_templates')

        # Deleting model 'minutes'
        db.delete_table(u'groups_app_minutes')

        # Deleting model 'reunions'
        db.delete_table(u'groups_app_reunions')

        # Deleting model 'rel_reunion_minutes'
        db.delete_table(u'groups_app_rel_reunion_minutes')

        # Deleting model 'assistance'
        db.delete_table(u'groups_app_assistance')

        # Deleting model 'rel_user_minutes_assistance'
        db.delete_table(u'groups_app_rel_user_minutes_assistance')

        # Deleting model 'rel_user_minutes_signed'
        db.delete_table(u'groups_app_rel_user_minutes_signed')

        # Deleting model 'user_role'
        db.delete_table(u'groups_app_user_role')

        # Deleting model 'groups_permissions'
        db.delete_table(u'groups_app_groups_permissions')

        # Deleting model 'rel_role_group_permissions'
        db.delete_table(u'groups_app_rel_role_group_permissions')

        # Deleting model 'packages'
        db.delete_table(u'groups_app_packages')

        # Deleting model 'billing'
        db.delete_table(u'groups_app_billing')

        # Deleting model 'groups_pro'
        db.delete_table(u'groups_app_groups_pro')

        # Deleting model 'last_minutes'
        db.delete_table(u'groups_app_last_minutes')

        # Deleting model 'rol_user_minutes'
        db.delete_table(u'groups_app_rol_user_minutes')

        # Deleting model 'annotations'
        db.delete_table(u'groups_app_annotations')

        # Deleting model 'annotations_comments'
        db.delete_table(u'groups_app_annotations_comments')

        # Deleting model 'DNI_type'
        db.delete_table(u'groups_app_dni_type')

        # Deleting model 'DNI'
        db.delete_table(u'groups_app_dni')

        # Deleting model 'DNI_permissions'
        db.delete_table(u'groups_app_dni_permissions')

        # Deleting model 'rel_group_dni'
        db.delete_table(u'groups_app_rel_group_dni')

        # Deleting model 'rel_minutes_dni'
        db.delete_table(u'groups_app_rel_minutes_dni')

        # Deleting model 'minutes_version'
        db.delete_table(u'groups_app_minutes_version')

        # Deleting model 'minutes_approver_version'
        db.delete_table(u'groups_app_minutes_approver_version')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'groups_app.annotations': {
            'Meta': {'object_name': 'annotations'},
            'annotation_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'annotations_id_minutes'", 'null': 'True', 'blank': 'True', 'to': u"orm['groups_app.minutes']"}),
            'id_minutes_annotation': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations_id_user'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'groups_app.annotations_comments': {
            'Meta': {'object_name': 'annotations_comments'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_annotation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'annotations_comments_id_minutes'", 'null': 'True', 'blank': 'True', 'to': u"orm['groups_app.annotations']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations_comments_id_user'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'groups_app.assistance': {
            'Meta': {'unique_together': "(('id_user', 'id_reunion'),)", 'object_name': 'assistance'},
            'date_confirmed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_reunion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assistance_id_reunion'", 'to': u"orm['groups_app.reunions']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assistance_id_user'", 'to': u"orm['auth.User']"}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'groups_app.billing': {
            'Meta': {'object_name': 'billing'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_request': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'groups_pro_available': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing_id_package'", 'to': u"orm['groups_app.packages']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing_id_user'", 'to': u"orm['auth.User']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'groups_app.dni': {
            'Meta': {'object_name': 'DNI'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dni_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_dni_type'", 'to': u"orm['groups_app.DNI_type']"}),
            'dni_value': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.dni_permissions': {
            'Meta': {'object_name': 'DNI_permissions'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_permissions_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_requester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_permissions_id_requester'", 'to': u"orm['auth.User']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_permissions_id_user'", 'to': u"orm['auth.User']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'groups_app.dni_type': {
            'Meta': {'object_name': 'DNI_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'groups_app.groups': {
            'Meta': {'object_name': 'Groups'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'image_path'", 'sizes': '((50, 50), (100, 100))', 'default': "'img/groups/default.jpg'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups_org'", 'to': u"orm['groups_app.Organizations']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'groups_app.groups_permissions': {
            'Meta': {'object_name': 'groups_permissions'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'groups_app.groups_pro': {
            'Meta': {'object_name': 'groups_pro'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_billing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groups_pro_id_billing'", 'null': 'True', 'to': u"orm['groups_app.billing']"}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups_pro_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups_pro_id_organization'", 'to': u"orm['groups_app.Organizations']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'groups_app.invitations': {
            'Meta': {'object_name': 'invitations'},
            'date_invited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email_invited': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_id_user_from'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'groups_app.invitations_groups': {
            'Meta': {'object_name': 'invitations_groups'},
            'date_invited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_groups_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_groups_id_user_from'", 'to': u"orm['auth.User']"}),
            'id_user_invited': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_groups_id_user_invited'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'groups_app.last_minutes': {
            'Meta': {'object_name': 'last_minutes'},
            'address_file': ('django.db.models.fields.files.FileField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_minutes_id_user'", 'to': u"orm['auth.User']"}),
            'name_file': ('django.db.models.fields.CharField', [], {'max_length': '350'})
        },
        u'groups_app.minutes': {
            'Meta': {'unique_together': "(('id_group', 'code'),)", 'object_name': 'minutes'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_id_creator'", 'to': u"orm['auth.User']"}),
            'id_extra_minutes': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'id_minutes_type'", 'to': u"orm['groups_app.templates']"}),
            'is_full_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'groups_app.minutes_approver_version': {
            'Meta': {'object_name': 'minutes_approver_version'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_approver_version_id_minutes'", 'to': u"orm['groups_app.minutes_version']"}),
            'id_user_approver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_approver_version_id_user'", 'to': u"orm['auth.User']"}),
            'is_signed_approved': ('django.db.models.fields.IntegerField', [], {})
        },
        u'groups_app.minutes_type': {
            'Meta': {'object_name': 'minutes_type'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_type_id_creator'", 'to': u"orm['auth.User']"}),
            'is_customized': ('django.db.models.fields.BooleanField', [], {}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'groups_app.minutes_type_1': {
            'Meta': {'object_name': 'minutes_type_1'},
            'agenda': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'agreement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type_reunion': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'groups_app.minutes_version': {
            'Meta': {'object_name': 'minutes_version'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'full_html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_version_id_minutes'", 'to': u"orm['groups_app.minutes']"}),
            'id_user_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_version_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.organizations': {
            'Meta': {'object_name': 'Organizations'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizations_id_admin'", 'to': u"orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'image_path'", 'sizes': '((50, 50), (100, 100))', 'default': "'img/groups/default.jpg'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'groups_app.packages': {
            'Meta': {'object_name': 'packages'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number_groups_pro': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'groups_app.private_templates': {
            'Meta': {'unique_together': "(('id_template', 'id_group'),)", 'object_name': 'private_templates'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_templates'", 'to': u"orm['groups_app.templates']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.rel_group_dni': {
            'Meta': {'object_name': 'rel_group_dni'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_group_dni_id_user'", 'to': u"orm['auth.User']"}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_group_dni_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'show_dni': ('django.db.models.fields.BooleanField', [], {})
        },
        u'groups_app.rel_minutes_dni': {
            'Meta': {'object_name': 'rel_minutes_dni'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_minutes_dni_id_minutes'", 'to': u"orm['groups_app.minutes']"}),
            'show_dni': ('django.db.models.fields.BooleanField', [], {})
        },
        u'groups_app.rel_reunion_minutes': {
            'Meta': {'object_name': 'rel_reunion_minutes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_reunion_minutes_id_minutes'", 'to': u"orm['groups_app.minutes']"}),
            'id_reunion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_reunion_minutes_id_reunion'", 'to': u"orm['groups_app.reunions']"})
        },
        u'groups_app.rel_role_group_permissions': {
            'Meta': {'object_name': 'rel_role_group_permissions'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group_permission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_role_group_permissions_id_group_permission'", 'to': u"orm['groups_app.groups_permissions']"}),
            'id_role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_role_group_permissions_id_role'", 'to': u"orm['groups_app.user_role']"})
        },
        u'groups_app.rel_user_group': {
            'Meta': {'object_name': 'rel_user_group'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groups_app.Groups']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_group_id_user'", 'to': u"orm['auth.User']"}),
            'id_user_invited': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rel_user_group_id_user_invited'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_convener': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_secretary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superadmin': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'groups_app.rel_user_minutes_assistance': {
            'Meta': {'object_name': 'rel_user_minutes_assistance'},
            'assistance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_assistance': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_minutes_assistance_id_minutes'", 'to': u"orm['groups_app.minutes']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_minutes_assistance_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.rel_user_minutes_signed': {
            'Meta': {'object_name': 'rel_user_minutes_signed'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_minutes_signed_id_minutes'", 'to': u"orm['groups_app.minutes']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_minutes_signed_id_user'", 'to': u"orm['auth.User']"}),
            'is_signed_approved': ('django.db.models.fields.IntegerField', [], {})
        },
        u'groups_app.rel_user_private_templates': {
            'Meta': {'object_name': 'rel_user_private_templates'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_private_templates_id_templates'", 'to': u"orm['groups_app.templates']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_private_templates_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.reunions': {
            'Meta': {'object_name': 'reunions'},
            'agenda': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_convened': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_reunion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_convener': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reunions_id_convener'", 'to': u"orm['auth.User']"}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reunions_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'groups_app.rol_user_minutes': {
            'Meta': {'object_name': 'rol_user_minutes'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rol_user_minutes_id_group'", 'to': u"orm['groups_app.Groups']"}),
            'id_minutes': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rol_user_minutes_id_minutes'", 'null': 'True', 'blank': 'True', 'to': u"orm['groups_app.minutes']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rol_user_minutes_id_user'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_approver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_assistant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_president': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_secretary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_signer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'groups_app.templates': {
            'Meta': {'object_name': 'templates'},
            'address_js': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'address_template': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'id_minutes_type'", 'to': u"orm['groups_app.minutes_type']"}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'groups_app.user_role': {
            'Meta': {'object_name': 'user_role'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['groups_app']