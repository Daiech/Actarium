# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organizations'
        db.create_table(u'organizations_organizations', (
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
        db.send_create_signal(u'organizations', ['Organizations'])

        # Adding model 'Groups'
        db.create_table(u'organizations_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_path', self.gf('libs.thumbs.ImageWithThumbsField')(name='image_path', sizes=((50, 50), (100, 100)), default='img/groups/default.jpg', max_length=100, blank=True, null=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups_org', to=orm['organizations.Organizations'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'organizations', ['Groups'])

        # Adding model 'rel_user_group'
        db.create_table(u'organizations_rel_user_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rel_user_group_id_user', to=orm['auth.User'])),
            ('id_user_invited', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rel_user_group_id_user_invited', null=True, blank=True, to=orm['auth.User'])),
            ('id_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Groups'])),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_secretary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_superadmin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_convener', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'organizations', ['rel_user_group'])


    def backwards(self, orm):
        # Deleting model 'Organizations'
        db.delete_table(u'organizations_organizations')

        # Deleting model 'Groups'
        db.delete_table(u'organizations_groups')

        # Deleting model 'rel_user_group'
        db.delete_table(u'organizations_rel_user_group')


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
        u'organizations.groups': {
            'Meta': {'object_name': 'Groups'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('libs.thumbs.ImageWithThumbsField', [], {'name': "'image_path'", 'sizes': '((50, 50), (100, 100))', 'default': "'img/groups/default.jpg'", 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups_org'", 'to': u"orm['organizations.Organizations']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'organizations.organizations': {
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
        u'organizations.rel_user_group': {
            'Meta': {'object_name': 'rel_user_group'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizations.Groups']"}),
            'id_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rel_user_group_id_user'", 'to': u"orm['auth.User']"}),
            'id_user_invited': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rel_user_group_id_user_invited'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_convener': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_secretary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superadmin': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['organizations']