from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from leads import models
from leads.serializers import ContactSerializer


class ContactView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        # Use serializer for validation
        serializer = ContactSerializer(data=request.data)
        valid_data = serializer.is_valid(raise_exception=False)
        if not valid_data:
            return Response({
                "status": "error",
                "message": "Invalid data",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Create new contact
        state = models.Status.objects.all().first()
        contact = models.Contact(
            status=state,
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
            
        

         