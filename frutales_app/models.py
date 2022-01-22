from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['first_name']) < 5:
            errors["first_name"] = "First name should be at least 5 characters"
        if len(postData['last_name']) < 5:
            errors["last_name"] = "Last name should be at least 5 characters"
        try:
            validate_email(postData['email'])
        except ValidationError:
            print('VALIDATION ERROR')
            errors["email"] = "please enter a valid email"
        # if EmailValidator(postData['email']):
        #     errors["first_name"] = "First name should be at least 5 characters"
        if postData['password'] != postData['confirmed_pw']:
            errors["password"] = "Passwords must be the same"
        
        
        return errors
# Create your models here.
class Usuario(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    number_phone= models.CharField(max_length = 13)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.TimeField(auto_now=True)
    updated_at =  models.TimeField(auto_now=True)

class Producto(models.Model):
    
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    # image=models.ImageField(upload_to="productos", null=True)

class Precio(models.Model):
    producto = models.ForeignKey(Producto, related_name = "precio", on_delete=models.CASCADE)
    precio = models.CharField(max_length=90)
    tamaño = models.CharField(max_length=80)

class Adicional(models.Model):
    nombre= models.CharField(max_length=50)
    precio= models.FloatField()
    
class AdicionalOrden(models.Model):
    nombre_adicional= models.ForeignKey(Adicional, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Orden(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tamañoproducto = models.CharField(max_length=100)
    rosaadicional = models.ForeignKey(AdicionalOrden, related_name="rosas" ,on_delete=models.CASCADE)
    globoadicional = models.ForeignKey(AdicionalOrden,related_name="globos",on_delete=models.CASCADE)
    especificaciones = models.TextField()
    entrega = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)
    created_at = models.TimeField(auto_now=True)
    updated_at =  models.TimeField(auto_now=True)