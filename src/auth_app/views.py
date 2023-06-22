from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework.response import Response
from .serialize import Register,Login, Login2
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class GoSignUp(views.APIView):
    serializer_class = Register

    def get(self, request):
        return Response({"INSTRUCCIONES": "escriba el nombre de usuario"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            
            data["response"] = "Registro Exitoso"
            data["username"] = account.username
            data["email"] = account.email
            
            token, created = Token.objects.get_or_create(user=account)            
            data["token"] = token
           

        else:
            return Response(serializer.errors)

        return Response({"NOTIFICACION":data["response"]})

class GoLogin(views.APIView):
    serializer_class = Login

    def get(self, request):
        return Response({"INSTRUCCIONES": "escriba el nombre de usuario"}) 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email_username = serializer.validated_data["email_username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=email_username, password=password)
            
            data = {}

            if user is None:
                user = authenticate(email=email_username, password=password)
            
            if user is not None:   
                data["CUENTA"] = "INFORMACIÓN DE LA CUENTA"
                data["username"] = user.username
                data["email"] = user.email
                data["password"] = password
                data["token"] = f"{Token.objects.get(user=user)}"
                
                request.session['profile_data'] = data

                return redirect("profile")

        else: 
            return Response({"ALERTA": "Credenciales Invalidas"}) 

        return Response({"ALERTA": "Credenciales Invalidas"}) 

class ProfileView(views.APIView):
    
    def get(self, request, data=None):
        data = request.session.get('profile_data') 

        if data:
            return Response(data) 
        
        return Response({
            "ALERTA": "SESIÓN NO INICIADA",
            "VISITE": "http://localhost:8000/account/login/"
        }) 
    


@api_view(["POST", "GET"])
def registration_view(request):
    if request.method == "POST":
        print("\n POST \n")      
        serializer = Login2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == "GET":

        return Response({"INSTRUCCIONES": "escriba el nombre de usuario"})
