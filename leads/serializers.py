from rest_framework import serializers
from leads.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """ Contact serializer """
    class Meta:
        # Fields to serialize
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'address']