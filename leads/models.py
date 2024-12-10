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
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="estado")
    name = models.CharField(max_length=100, verbose_name="nombre")
    email = models.EmailField(verbose_name="correo")
    phone = models.CharField(max_length=15, verbose_name="teléfono")
    address = models.TextField(verbose_name="dirección", blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True, verbose_name="fecha añadido")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="fecha actualizado")
    
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