# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrderStatus'
        db.create_table(u'customers_services_orderstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'customers_services', ['OrderStatus'])

        # Adding model 'Periods'
        db.create_table(u'customers_services_periods', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'customers_services', ['Periods'])

        # Adding model 'ServicesCategories'
        db.create_table(u'customers_services_servicescategories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['ServicesCategories'])

        # Adding model 'PaymentMethods'
        db.create_table(u'customers_services_paymentmethods', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['PaymentMethods'])

        # Adding model 'Services'
        db.create_table(u'customers_services_services', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price_per_period', self.gf('django.db.models.fields.FloatField')()),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services_period', to=orm['customers_services.Periods'])),
            ('service_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services_service_category', to=orm['customers_services.ServicesCategories'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['Services'])

        # Adding model 'CustomersServices'
        db.create_table(u'customers_services_customersservices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('date_expiration', self.gf('django.db.models.fields.DateField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['CustomersServices'])

        # Adding model 'Addresses'
        db.create_table(u'customers_services_addresses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['Addresses'])

        # Adding model 'Customers'
        db.create_table(u'customers_services_customers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['customers_services.Addresses'], unique=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['Customers'])

        # Adding model 'CustomerOrders'
        db.create_table(u'customers_services_customerorders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customerorders_status', to=orm['customers_services.OrderStatus'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customerorders_customer', to=orm['customers_services.Customers'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['CustomerOrders'])

        # Adding model 'OrderItems'
        db.create_table(u'customers_services_orderitems', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('number_of_periods', self.gf('django.db.models.fields.IntegerField')()),
            ('discount', self.gf('django.db.models.fields.IntegerField')()),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderitems_service', to=orm['customers_services.Services'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderitems_order', to=orm['customers_services.CustomerOrders'])),
            ('customer_service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderitems_customer_service', to=orm['customers_services.CustomersServices'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'customers_services', ['OrderItems'])


    def backwards(self, orm):
        # Deleting model 'OrderStatus'
        db.delete_table(u'customers_services_orderstatus')

        # Deleting model 'Periods'
        db.delete_table(u'customers_services_periods')

        # Deleting model 'ServicesCategories'
        db.delete_table(u'customers_services_servicescategories')

        # Deleting model 'PaymentMethods'
        db.delete_table(u'customers_services_paymentmethods')

        # Deleting model 'Services'
        db.delete_table(u'customers_services_services')

        # Deleting model 'CustomersServices'
        db.delete_table(u'customers_services_customersservices')

        # Deleting model 'Addresses'
        db.delete_table(u'customers_services_addresses')

        # Deleting model 'Customers'
        db.delete_table(u'customers_services_customers')

        # Deleting model 'CustomerOrders'
        db.delete_table(u'customers_services_customerorders')

        # Deleting model 'OrderItems'
        db.delete_table(u'customers_services_orderitems')


    models = {
        u'customers_services.addresses': {
            'Meta': {'object_name': 'Addresses'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'customers_services.customerorders': {
            'Meta': {'object_name': 'CustomerOrders'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customerorders_customer'", 'to': u"orm['customers_services.Customers']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customerorders_status'", 'to': u"orm['customers_services.OrderStatus']"})
        },
        u'customers_services.customers': {
            'Meta': {'object_name': 'Customers'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['customers_services.Addresses']", 'unique': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'customers_services.customersservices': {
            'Meta': {'object_name': 'CustomersServices'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_expiration': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        u'customers_services.orderitems': {
            'Meta': {'object_name': 'OrderItems'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderitems_customer_service'", 'to': u"orm['customers_services.CustomersServices']"}),
            'discount': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_of_periods': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderitems_order'", 'to': u"orm['customers_services.CustomerOrders']"}),
            'order_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderitems_service'", 'to': u"orm['customers_services.Services']"})
        },
        u'customers_services.orderstatus': {
            'Meta': {'object_name': 'OrderStatus'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'customers_services.paymentmethods': {
            'Meta': {'object_name': 'PaymentMethods'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'customers_services.periods': {
            'Meta': {'object_name': 'Periods'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'customers_services.services': {
            'Meta': {'object_name': 'Services'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_period'", 'to': u"orm['customers_services.Periods']"}),
            'price_per_period': ('django.db.models.fields.FloatField', [], {}),
            'service_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_service_category'", 'to': u"orm['customers_services.ServicesCategories']"})
        },
        u'customers_services.servicescategories': {
            'Meta': {'object_name': 'ServicesCategories'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['customers_services']