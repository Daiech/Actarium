# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'minutes_type_1.extra1'
        db.add_column(u'groups_app_minutes_type_1', 'extra1',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'minutes_type_1.extra2'
        db.add_column(u'groups_app_minutes_type_1', 'extra2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'minutes_type_1.extra3'
        db.add_column(u'groups_app_minutes_type_1', 'extra3',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'minutes_type_1.extra1'
        db.delete_column(u'groups_app_minutes_type_1', 'extra1')

        # Deleting field 'minutes_type_1.extra2'
        db.delete_column(u'groups_app_minutes_type_1', 'extra2')

        # Deleting field 'minutes_type_1.extra3'
        db.delete_column(u'groups_app_minutes_type_1', 'extra3')


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
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dni_permissions_id_group'", 'to': u"orm['organizations.Groups']"}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_id_creator'", 'to': u"orm['auth.User']"}),
            'id_extra_minutes': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minutes_id_group'", 'to': u"orm['organizations.Groups']"}),
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
            'extra1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
        u'groups_app.private_templates': {
            'Meta': {'unique_together': "(('id_template', 'id_group'),)", 'object_name': 'private_templates'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_group'", 'to': u"orm['organizations.Groups']"}),
            'id_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_templates'", 'to': u"orm['groups_app.templates']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'private_templates_id_user'", 'to': u"orm['auth.User']"})
        },
        u'groups_app.rel_group_dni': {
            'Meta': {'object_name': 'rel_group_dni'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_group_dni_id_user'", 'to': u"orm['auth.User']"}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_group_dni_id_group'", 'to': u"orm['organizations.Groups']"}),
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
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reunions_id_group'", 'to': u"orm['organizations.Groups']"}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'groups_app.rol_user_minutes': {
            'Meta': {'object_name': 'rol_user_minutes'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rol_user_minutes_id_group'", 'to': u"orm['organizations.Groups']"}),
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
            'address_css': ('django.db.models.fields.CharField', [], {'default': "'groups/minutesTemplates/empty_style.css'", 'max_length': '150'}),
            'address_css4pdf': ('django.db.models.fields.CharField', [], {'default': "'pdfmodule/default_css4pdf.css'", 'max_length': '150'}),
            'address_js': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'address_template': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'id_minutes_type'", 'to': u"orm['groups_app.minutes_type']"}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'logo'", 'sizes': '((110, 40), (130, 45), (200, 70))', 'default': "'client_logos/default/actarium-beta.png'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'organizations.groups': {
            'Meta': {'object_name': 'Groups'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'image_path'", 'sizes': '((50, 50), (100, 100))', 'default': "'icons/group_default.jpg'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups_org'", 'to': u"orm['organizations.Organizations']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'organizations.organizations': {
            'Meta': {'object_name': 'Organizations'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'image_path'", 'sizes': '((50, 50), (100, 100))', 'default': "'icons/org_default.jpg'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '120'})
        }
    }

    complete_apps = ['groups_app']