from rest_framework.serializers import  ModelSerializer, ValidationError, CharField, Serializer
from django.contrib.auth.models import User


class Register(Serializer):
    username = CharField(required=True)
    email = CharField(required=True)

    password = CharField(
        style={"input_type":"password"}, required=True
    )

    password2 = CharField(
        style={"input_type":"password"}, required=True
    )
    # Verificacion de datos

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        
        if password != password2:
            raise ValidationError({"error": "password y password2 deben ser iguales"})
        
        email = self.validated_data["email"]
        
        if User.objects.filter(email=email).exists():
            raise ValidationError({"error": "Ese correo ya esta registrado"})
            
        username = self.validated_data["username"]
        
        account = User(email=email, username=username)
        account.set_password(password)
        account.save()
        
        
        return account

class Login(Serializer):
    email_username = CharField(required=True)
    password = CharField(
        style={"input_type":"password"}, required=True
    )


class Login2(ModelSerializer):
    username = CharField(required=True)
    email = CharField(required=True)

    password = CharField(
        style={"input_type":"password"}, required=True
    )

    password2 = CharField(
        style={"input_type":"password"}, required=True
    )
        
    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        
        if password != password2:
            raise ValidationError({"error": "password y password2 deben ser iguales"})
        
        email = self.validated_data["email"]
        
        if User.objects.filter(email=email).exist():
            raise ValidationError({"error": "Ese correo ya esta registrado"})
            
        username = self.validated_data["username"]
        
        account = Use(email=email, username=username)
        account.set_password(password)
        account.save()
        
        
        return account
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        
        extra_kwargs = {
            "password" : {"wirte_only": True}
        }    