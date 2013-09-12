#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from Actarium import settings
from groups.models import groups as Groups


class OrderStatus(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.name)
 
class Order(models.Model):
    id_order_status = models.ForeignKey(OrderStatus,  null=False, related_name='%(class)s_id_order_status')
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.id_user.username, self.id_order_status.name, self.date_added)

       
class PaymentMethod(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.name)


class Billing(models.Model):
    id_order = models.ForeignKey(Order,  null=False, related_name='%(class)s_id_order')
    id_payment_method = models.ForeignKey(PaymentMethod,  null=False, related_name='%(class)s_id_payment_method')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s (%s)" % (self.id_order, self.id_payment_method)


class PriceCustomization(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    price_month = models.CharField(max_length=150, verbose_name="price_month")
    is_active = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.price_month)
    
    
class PriceTeamSize(models.Model):
    quantity = models.CharField(max_length=10, verbose_name="quantity")
    price_month = models.CharField(max_length=150, verbose_name="price_month")
    is_active = models.BooleanField()
    is_available = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.quantity, self.price_month)
    
class Timetable (models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    time_start = models.TimeField()
    time_end = models.TimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s (%s - %s)" % (self.name, self.time_start, self.time_end)
        
class PriceAdvertising(models.Model):
    id_timetable = models.ForeignKey(Timetable,  null=False, related_name='%(class)s_id_timetable')
    price_week = models.CharField(max_length=150, verbose_name="price_week")
    is_active = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.id_timetable, self.price_week)

class OrderCustomization(models.Model):
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    months = models.CharField(max_length=10, verbose_name="months")
    id_price_customization = models.ForeignKey(PriceCustomization,  null=False, related_name='%(class)s_id_price_customization')
    id_order = models.ForeignKey(Order,  null=False, related_name='%(class)s_id_order')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s - %s" % (self.id_group.name, self.months, self.id_price_customization, self.id_order)
    
    
class OrderTeamSize(models.Model):
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    months = models.CharField(max_length=10, verbose_name="months")
    id_price_team_size = models.ForeignKey(PriceTeamSize,  null=False, related_name='%(class)s_id_price_team_size')
    id_order = models.ForeignKey(Order,  null=False, related_name='%(class)s_id_order')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s - %s" % (self.id_group.name, self.months, self.id_price_team_size, self.id_order)
    
    
class OrderAdvertising(models.Model):
    weeks = models.CharField(max_length=10, verbose_name="weeks")
    id_price_advertising = models.ForeignKey(PriceAdvertising,  null=False, related_name='%(class)s_id_price_advertising')
    id_order = models.ForeignKey(Order,  null=False, related_name='%(class)s_id_order')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.weeks, self.id_price_advertising, self.id_order)
    
class Advertising(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    description = models.TextField(blank=True)
    url= models.TextField(blank=True)
    image_path = models.CharField(max_length=150, verbose_name="image", default="img/groups/default.jpg")
    is_active = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.is_active)
    
    
class AdvertisingLogType(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.name)    

class AdvertisingLog(models.Model):
    id_advertising_log_type = models.ForeignKey(AdvertisingLogType,  null=False, related_name='%(class)s_id_advertising_log_type')
    id_advertising = models.ForeignKey(Advertising,  null=False, related_name='%(class)s_id_advertising')
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.id_user.username, self.id_group.name, self.id_advertising_log_type)

    
class ExpCustomization(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    expiration_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.id_user.username, self.id_group.name, self.expiration_date)
    
    
class ExpTeamSize(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_group = models.ForeignKey(Groups,  null=False, related_name='%(class)s_id_group')
    quantity =  models.CharField(max_length=10, verbose_name="quantity")
    expiration_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.id_user, self.id_group, self.quantity, self.expiration_date)
    
    
class ExpAdvertising(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_advertising = models.ForeignKey(Advertising,  null=False, related_name='%(class)s_id_advertising')
    expiration_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - $s - %s" % (self.id_user, self.id_advertising, self.expiration_date)
    
    
class RelCustomizationOrderExp(models.Model):
    id_order_customization = models.ForeignKey(OrderCustomization,  null=False, related_name='%(class)s_id_order_customization')
    id_exp_customization = models.ForeignKey(ExpCustomization,  null=False, related_name='%(class)s_id_exp_customization')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.id_order_customization,  self.id_exp_customization)
    
    
class RelTeamSizeOrderExp(models.Model):
    id_order_team_size = models.ForeignKey(OrderTeamSize,  null=False, related_name='%(class)s_id_order_team_size')
    id_exp_team_size = models.ForeignKey(ExpTeamSize,  null=False, related_name='%(class)s_id_exp_team_size')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.id_order_team_size,  self.id_exp_team_size)
    
    
class RelAdvertisingOrderExp(models.Model):
    id_order_advertising = models.ForeignKey(OrderAdvertising,  null=False, related_name='%(class)s_id_order_advertising')
    id_exp_advertising = models.ForeignKey(ExpAdvertising,  null=False, related_name='%(class)s_id_exp_advertising')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.id_order_advertising,  self.id_exp_advertising)
    

    

    