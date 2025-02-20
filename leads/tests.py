from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.authtoken.models import Token

from leads import models


class ApiContactTestView(TestCase):
    """Test the profile API view"""

    def setUp(self):
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username="testuser",
            password=self.password,
            email="test@gmail.com",
        )
        self.endpoint = "/api/contact/"
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_invalid_token(self):
        """Test invalid token"""

        res = self.client.get(self.endpoint, HTTP_AUTHORIZATION="Token invalid")

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            res.json(), {"status": "error", "message": "Token inválido.", "data": {}}
        )

    def test_missing_data(self):
        """Test missing data but with valid token"""

        res = self.client.post(
            self.endpoint,
            data={},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Invalid data",
                "data": {
                    "name": ["Este campo es requerido."],
                    "email": ["Este campo es requerido."],
                    "phone": ["Este campo es requerido."],
                },
            },
        )

    def test_missing_token(self):
        """Test without sending token"""

        res = self.client.get(self.endpoint)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Las credenciales de autenticación no se proveyeron.",
                "data": {},
            },
        )

    def test_valid(self):
        """Test create contact with valid data"""

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
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Check contact created in database
        contact = models.Contact.objects.all().first()
        self.assertEqual(contact.name, data["name"])
        self.assertEqual(contact.email, data["email"])
        self.assertEqual(contact.phone, data["phone"])
        self.assertEqual(contact.address, data["address"])
        data["id"] = contact.id

        self.assertEqual(
            res.json(),
            {
                "status": "success",
                "message": "Contact created",
                "data": data,
            },
        )


class ApiQuoteTestView(TestCase):
    """Test the profile API view"""

    def setUp(self):

        # Create login user and token
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username="testuser",
            password=self.password,
            email="test@gmail.com",
        )
        self.endpoint = "/api/quote/"
        self.token, _ = Token.objects.get_or_create(user=self.user)

        # Global data
        self.data = {
            "name": "test",
            "email": "test@gmail.com",
            "phone": "1234567890",
            "selectedService": "company",
            "companySector": "other",
            "companyEmployees": "+50",
            "features": ["tech", "plans"],
            "residentialType": "apartment",
            "branches": 1,
            "users": ["owner", "manager"],
            "hasWifi": True,
            "hasCameras": "yes",
            "rooms": 1,
            "targets": ["employees", "children"],
        }

        # Run commands
        call_command("apps_loaddata")

    def test_invalid_token(self):
        """Test invalid token"""

        res = self.client.get(self.endpoint, HTTP_AUTHORIZATION="Token invalid")

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            res.json(), {"status": "error", "message": "Token inválido.", "data": {}}
        )

    def test_missing_data(self):
        """Missing all data"""

        # Send no data
        res = self.client.post(
            self.endpoint,
            data={},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Invalid data",
                "data": {
                    "name": ["Este campo es requerido."],
                    "email": ["Este campo es requerido."],
                    "phone": ["Este campo es requerido."],
                },
            },
        )

    def test_missing_contact_data(self):
        """Missing company and residential data"""

        # Delete company and residential data
        self.data.pop("companySector")
        self.data.pop("companyEmployees")
        self.data.pop("features")
        self.data.pop("residentialType")

        # send only contact data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Invalid data",
                "data": {
                    "companySector": ["Este campo es requerido."],
                    "companyEmployees": ["Este campo es requerido."],
                    "features": ["Este campo es requerido."],
                },
            },
        )

    def test_missing_residential_data(self):
        """Missing residential data"""

        # Delete residential data
        self.data.pop("residentialType")

        # send only contact and company data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Invalid data",
                "data": {
                    "residentialType": ["Este campo es requerido."],
                },
            },
        )

    def test_missing_company_data(self):
        """Missing company data"""

        # Delete company data
        self.data.pop("companySector")
        self.data.pop("companyEmployees")
        self.data.pop("features")

        # send only contact and residential data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Invalid data",
                "data": {
                    "companySector": ["Este campo es requerido."],
                    "companyEmployees": ["Este campo es requerido."],
                    "features": ["Este campo es requerido."],
                },
            },
        )

    def test_missing_token(self):
        """No send token"""

        res = self.client.get(self.endpoint)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            res.json(),
            {
                "status": "error",
                "message": "Las credenciales de autenticación no se proveyeron.",
                "data": {},
            },
        )

    def test_new_contact(self):
        """Create new contact"""

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate contact created
        contact = models.Contact.objects.all().first()
        self.assertEqual(contact.name, self.data["name"])
        self.assertEqual(contact.email, self.data["email"])
        self.assertEqual(contact.phone, self.data["phone"])

    def test_update_contact(self):
        """Replace existing contact"""

        # Create user with same email
        status_new = models.Status.objects.all().first()
        contact = models.Contact.objects.create(
            status=status_new,
            name="old_name",
            email=self.data["email"],
            phone="0000000000",
        )

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate contact update
        contact = models.Contact.objects.all().first()
        self.assertEqual(contact.name, self.data["name"])
        self.assertEqual(contact.email, self.data["email"])
        self.assertEqual(contact.phone, self.data["phone"])

    def test_quote_company(self):
        """Create company quote"""

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate company quote created
        quote = models.QuoteCompany.objects.all().first()
        self.assertEqual(quote.sector.key, self.data["companySector"])
        self.assertEqual(quote.employees.key, self.data["companyEmployees"])
        self.assertEqual(quote.features.count(), 2)
        self.assertEqual(quote.branches, self.data["branches"])
        self.assertEqual(quote.users.count(), 2)
        self.assertEqual(quote.has_wifi, self.data["hasWifi"])
        self.assertEqual(quote.has_cameras, self.data["hasCameras"])

        # Valdiate response
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            res.json(),
            {
                "status": "success",
                "message": "Quote for company created",
                "data": {
                    "id": quote.id,
                    "contact_email": self.data["email"],
                },
            },
        )

    def test_quote_residential(self):
        """Create residential quote"""

        # Update data
        self.data["selectedService"] = "residential"

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate residential quote created
        quote = models.QuoteResidential.objects.all().first()
        self.assertEqual(quote.type.key, self.data["residentialType"])
        self.assertEqual(quote.features.count(), 2)
        self.assertEqual(quote.rooms, self.data["rooms"])
        self.assertEqual(quote.targets.count(), 2)
        self.assertEqual(quote.has_wifi, self.data["hasWifi"])
        self.assertEqual(quote.has_cameras, self.data["hasCameras"])

        # Valdiate response
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            res.json(),
            {
                "status": "success",
                "message": "Quote for residential created",
                "data": {
                    "id": quote.id,
                    "contact_email": self.data["email"],
                },
            },
        )

    def test_quote_company_has_cameras_no(self):
        """Validate has_cameras is no (yes skipped because it is default)"""

        # Update data
        self.data["selectedService"] = "company"
        self.data["hasCameras"] = "no"

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate company quote created
        quote = models.QuoteCompany.objects.all().first()
        self.assertEqual(quote.has_cameras, "no")

    def test_quote_residential_has_cameras_maintenance(self):
        """Validate has_cameras is maintenance"""

        # Update data
        self.data["selectedService"] = "residential"
        self.data["hasCameras"] = "maintenance"

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate residential quote created
        quote = models.QuoteResidential.objects.all().first()
        self.assertEqual(quote.has_cameras, "maintenance")

    def test_quote_residential_has_cameras_no(self):
        """Validate has_cameras is no (yes skipped because it is default)"""

        # Update data
        self.data["selectedService"] = "residential"
        self.data["hasCameras"] = "no"

        # send full data
        res = self.client.post(
            self.endpoint,
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(res.status_code, 201)

        # Validate residential quote created
        quote = models.QuoteResidential.objects.all().first()
        self.assertEqual(quote.has_cameras, "no")
