from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from leads import models
from leads import serializers


class ContactView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        # Use serializer for data validation
        serializer = serializers.ContactSerializer(data=request.data)
        valid_data = serializer.is_valid(raise_exception=False)
        if not valid_data:
            return Response({
                "status": "error",
                "message": "Invalid data",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Create new contact
        status_new = models.Status.objects.all().first()
        contact = models.Contact(
            status=status_new,
            name=request.data['name'],
            email=request.data['email'],
            phone=request.data['phone'],
            address=request.data['address'],
        )
        contact.save()
        
        return Response({
            "status": "success",
            "message": "Contact created",
            "data": {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "address": contact.address,
            },
        }, status=status.HTTP_201_CREATED)
            
        
class Quote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        # Use serializer for data validation
        serializers_to_check = [
            serializers.ContactSerializer,
            serializers.QuoteCompanySerializer,
            serializers.QuoteResidentialSerializer,
        ]
        for serializer_to_check in serializers_to_check:
            serializer = serializer_to_check(data=request.data)
            valid_data = serializer.is_valid(raise_exception=False)
            if not valid_data:
                return Response({
                    "status": "error",
                    "message": "Invalid data",
                    "data": serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
            
        # Get or create contact
        status_new = models.Status.objects.all().first()
        current_contact = models.Contact.objects.filter(email=request.data['email'])
        if current_contact.exists():
            # Update contact data
            contact = current_contact.first()
            contact.status = status_new
            contact.name = request.data['name']
            contact.phone = request.data['phone']
        else:
            # Create new contact
            contact = models.Contact(
                status=status_new,
                name=request.data['name'],
                email=request.data['email'],
                phone=request.data['phone'],
            )
        contact.save()
        
        # Get global data
        selected_service = request.data['selectedService']
        features_keys = request.data.getlist('features')
        print(">>>>>", features_keys, request.data)
        features = []
        for feature_key in features_keys:
            print(feature_key)
            feature = models.Features.objects.get(key=feature_key)
            features.append(feature)
            
        # Create quotes
        if selected_service == 'company':
            
            # Get secondary data
            sector_key = request.data['companySector']
            employees_key = request.data['companyEmployees']
            
            sector = models.CompanySector.objects.get(key=sector_key)
            employees = models.CompanyEmployees.objects.get(key=employees_key)
                
            # Save quote
            quote = models.QuoteCompany(
                contact=contact,
                status=status_new,
                sector=sector,
                employees=employees,
            )
        else:
            # Get secondary data
            type_key = request.data['residentialType']
            type = models.ResidentialType.objects.get(key=type_key)
            
            # Save quote
            quote = models.QuoteResidential(
                contact=contact,
                status=status_new,
                type=type,
            )
            
        # Add features to quote and save
        quote.save()
        quote.features.set(features)
        
        return Response({
            "status": "success",
            "message": f"Quote for {selected_service} created",
            "data": {
                "id": quote.id,
                "contact_email": contact.email,
            },
        }, status=status.HTTP_201_CREATED)
            
        
         