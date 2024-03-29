#encoding:utf-8
from django.db import models
from libs.generic_managers import GenericManager


class OrganizationServicesManager(GenericManager):

    def get_org(self):
        try:
            org= self.all()[0].organization
            return org
        except:
            return None

    def get_max_num_members(self):
        organization_services = self.all()
        for organization_service in  organization_services:
            service_category = organization_service.service.service_category() 
            if service_category and service_category.pk == 1:
                return organization_service.service.quantity
        return 0
    
    def can_add(self):
        max_num_members = self.get_max_num_members()
        org = self.all()[0].organization
        try:
            current_num_members = org.get_num_members()
        except:
            current_num_members = 0
        num_available_members = max_num_members - current_num_members
        if num_available_members > 0:
            return True
        else:
            return False

    def get_members_service_active(self):
        organization_services = self.all()
        for organization_service in  organization_services:
            service_category = organization_service.service.service_category() 
            if service_category and service_category.pk == 1:
                return organization_service.service
        return None


class ActariumCustomersManager(GenericManager):
    def get_user(self):
        try:
            obj = self.all()[0]
            return obj.user
        except:
            return None

    def get_customer(self):
        try:
            obj = self.all()[0]
            return obj.customer
        except:
            return None

class PackagesManager(GenericManager):
    pass

class ServicesRangesManager(GenericManager):

    def get_service(self,quantity):
        quantity = int(quantity)
        service_range = self.get_all_active().get(upper__gte=quantity,lower__lte=quantity)
        if service_range:
            service = service_range.service
            return service
        return None


    def get_total_price(self,quantity):
        quantity = int(quantity)
        service = self.get_service(quantity)
        if service:
            service_price = service.price_per_period
            total = service_price*quantity
            return total
        else:
            return None

    def get_total_price_formated(self,quantity):
        quantity = int(quantity)
        service = self.get_service()
        if service:
            total_price = self.get_total_price(quantity)
            if total_price:
                period = service.period.name
                total = "$%.0f / %s"%(total_price,period)
                return total
        return "Valor no determinado"

class DiscountCodesManager(GenericManager):
    pass


class LastMinutesTasksManager(GenericManager):
    def get_tasks(self):
        return self.filter(task__is_active=True)