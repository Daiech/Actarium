# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'email_admin_type'
        db.create_table(u'emailmodule_email_admin_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'emailmodule', ['email_admin_type'])

        # Adding model 'email'
        db.create_table(u'emailmodule_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('email_type', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('admin_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_id_email_type', to=orm['emailmodule.email_admin_type'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'emailmodule', ['email'])

        # Adding model 'email_group_permissions'
        db.create_table(u'emailmodule_email_group_permissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_group_permissions_id_group', to=orm['organizations.Groups'])),
            ('id_email_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_group_permissions_id_email_type', to=orm['emailmodule.email'])),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_group_permissions_id_user_from', to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'emailmodule', ['email_group_permissions'])

        # Adding model 'email_global_permissions'
        db.create_table(u'emailmodule_email_global_permissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_email_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_global_permissions_id_email_type', to=orm['emailmodule.email'])),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_global_permissions_id_user_from', to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'emailmodule', ['email_global_permissions'])


    def backwards(self, orm):
        # Deleting model 'email_admin_type'
        db.delete_table(u'emailmodule_email_admin_type')

        # Deleting model 'email'
        db.delete_table(u'emailmodule_email')

        # Deleting model 'email_group_permissions'
        db.delete_table(u'emailmodule_email_group_permissions')

        # Deleting model 'email_global_permissions'
        db.delete_table(u'emailmodule_email_global_permissions')


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
        u'emailmodule.email': {
            'Meta': {'object_name': 'email'},
            'admin_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_id_email_type'", 'to': u"orm['emailmodule.email_admin_type']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_type': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'emailmodule.email_admin_type': {
            'Meta': {'object_name': 'email_admin_type'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'emailmodule.email_global_permissions': {
            'Meta': {'object_name': 'email_global_permissions'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_email_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_global_permissions_id_email_type'", 'to': u"orm['emailmodule.email']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_global_permissions_id_user_from'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'emailmodule.email_group_permissions': {
            'Meta': {'object_name': 'email_group_permissions'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_email_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_group_permissions_id_email_type'", 'to': u"orm['emailmodule.email']"}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_group_permissions_id_group'", 'to': u"orm['organizations.Groups']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_group_permissions_id_user_from'", 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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

    complete_apps = ['emailmodule']