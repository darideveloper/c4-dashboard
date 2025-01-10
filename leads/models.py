from django.db import models


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.name


class Contact(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, verbose_name="estado")
    name = models.CharField(max_length=100, verbose_name="nombre")
    email = models.EmailField(verbose_name="correo")
    phone = models.CharField(max_length=15, verbose_name="teléfono")
    address = models.TextField(verbose_name="dirección", blank=True, null=True)
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha añadido")
    updated_on = models.DateTimeField(
        auto_now=True, verbose_name="fecha actualizado")

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return f"{self.name} ({self.email})"


class CompanySector(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Sector de empresa'
        verbose_name_plural = 'Sectores de empresas'

    def __str__(self):
        return self.name


class CompanyEmployees(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Empleados de empresa'
        verbose_name_plural = 'Empleados de empresas'

    def __str__(self):
        return self.key


class Features(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'

    def __str__(self):
        return self.name


class ResidentialType(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tipo de residencia'
        verbose_name_plural = 'Tipos de residencias'

    def __str__(self):
        return self.name
    
    
class MonitoringUser(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Usuario que monitorea'
        verbose_name_plural = 'Usuarios que monitorean'

    def __str__(self):
        return f"{self.name} ({self.key})"
    

class MonitoringTarget(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Objetivo de monitoreo'
        verbose_name_plural = 'Objetivos de monitoreo'

    def __str__(self):
        return self.name
    

class QuoteCompany(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, verbose_name="estado")
    sector = models.ForeignKey(
        CompanySector, on_delete=models.CASCADE, verbose_name="sector")
    employees = models.ForeignKey(
        CompanyEmployees, on_delete=models.CASCADE, verbose_name="empleados")
    branches = models.IntegerField(verbose_name="sucursales")
    users = models.ManyToManyField(MonitoringUser, verbose_name="usuarios")
    has_wifi = models.BooleanField(verbose_name="tiene wifi")
    has_cameras = models.BooleanField(verbose_name="tiene cámaras", default=False)
    features = models.ManyToManyField(Features, verbose_name="características")
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name="contacto")
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha añadido")
    updated_on = models.DateTimeField(
        auto_now=True, verbose_name="fecha actualizado")

    class Meta:
        verbose_name = 'Cotización de empresa'
        verbose_name_plural = 'Cotizaciones de empresas'

    def __str__(self):
        return f"company: {self.contact.name} - {self.sector}"


class QuoteResidential(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, verbose_name="estado")
    type = models.ForeignKey(
        ResidentialType, on_delete=models.CASCADE, verbose_name="tipo")
    rooms = models.IntegerField(verbose_name="habitaciones")
    targets = models.ManyToManyField(MonitoringTarget, verbose_name="objetivos")
    has_wifi = models.BooleanField(verbose_name="tiene wifi")
    has_cameras = models.BooleanField(verbose_name="tiene cámaras", default=False)
    features = models.ManyToManyField(Features, verbose_name="características")
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name="contacto")
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha añadido")
    updated_on = models.DateTimeField(
        auto_now=True, verbose_name="fecha actualizado")

    class Meta:
        verbose_name = 'Cotización de residencia'
        verbose_name_plural = 'Cotizaciones de residencias'

    def __str__(self):
        return f"residential: {self.contact.name} - {self.type}"
