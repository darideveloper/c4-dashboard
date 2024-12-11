from rest_framework import serializers
from leads import models


class ContactSerializer(serializers.ModelSerializer):
    """ Contact serializer """
    class Meta:
        # Fields to serialize
        model = models.Contact
        fields = ['id', 'name', 'email', 'phone', 'address']


class QuoteCompanySerializer(serializers.ModelSerializer):
    """ Quote company serializer """

    # Map frontend keys to model fields using 'source'
    companySector = serializers.CharField()
    companyEmployees = serializers.CharField()
    features = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        # Fields to serialize
        model = models.QuoteCompany
        fields = ['id', 'companySector', 'companyEmployees', 'features']
        
        
class QuoteResidentialSerializer(serializers.ModelSerializer):
    """ Quote company serializer """
    
    # Map frontend keys to model fields using 'source'
    residentialType = serializers.CharField()
    features = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        # Fields to serialize
        model = models.QuoteResidential
        fields = ['id', 'residentialType', 'features']