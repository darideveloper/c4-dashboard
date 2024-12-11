from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.authtoken.models import Token

from leads import models


class ApiContactTestView(TestCase):
    """ Test the profile API view """

    def setUp(self):
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser',
            password=self.password,
            email="test@gmail.com",
        )
        self.endpoint = '/api/contact/'
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_invalid_token(self):
        """ Test invalid token """

        res = self.client.get(self.endpoint, HTTP_AUTHORIZATION='Token invalid')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Token inválido.",
            "data": {}
        })

    def test_missing_data(self):
        """ Test missing data but with valid token """

        res = self.client.post(
            self.endpoint,
            data={},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Invalid data",
            "data": {
                "name": ["Este campo es requerido."],
                "email": ["Este campo es requerido."],
                "phone": ["Este campo es requerido."],
            }
        })
        
    def test_missing_token(self):
        """ Test without sending token """

        res = self.client.get(self.endpoint)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Las credenciales de autenticación no se proveyeron.",
            "data": {}
        })
        
    def test_valid(self):
        """ Test create contact with valid data """
        
        # Run command
        call_command("apps_loaddata")
        
        data = {
            "name": "Test Name",
            "email": "test@gmail.com",
            "phone": "1234567890",
            "address": "Test Address",
        }
        
        # Validtae response status
        res = self.client.post(
            self.endpoint,
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(res.status_code, 201)
        
        # Check contact created in database
        contact = models.Contact.objects.all().first()
        self.assertEqual(contact.name, data['name'])
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.phone, data['phone'])
        self.assertEqual(contact.address, data['address'])
        data['id'] = contact.id
                
        self.assertEqual(res.json(), {
            "status": "success",
            "message": "Contact created",
            "data": data,
        })