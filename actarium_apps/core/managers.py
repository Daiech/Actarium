#encoding:utf-8
from django.db import models
from libs.generic_managers import GenericManager

class OrganizationServicesManager(GenericManager):

    def get_max_num_members(self):
        organization_services = self.all()
        for organization_service in  organization_services:
            service_category = organization_service.service.service_category() 
            if  service_category.pk == 1:
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
        print num_available_members
        if num_available_members >0:
            return True
        else:
            return False
        
class ActariumCustomersManager(GenericManager):
    pass