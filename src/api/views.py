from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from ejercicios.views import *
from .serialize import *
import json

prepare_delete_id = None


class ProductViewSet(views.APIView):
    serializer_class = BaseSerializer

    def get(self, request):
        text = product_model_list_view(request,rest=True)
        json_ = json.loads(text)
        content = {}

        count = 0
        for element in json_:            
            content[f"id: {element['pk']}"] =element['fields']['title']
            count += 1

        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get("product")
            price = serializer.validated_data.get("price")
            description = serializer.validated_data.get("description")
            color = serializer.validated_data.get("color")

            rest_form = [
                title,
                price,
                description,
                color,
            ]

            product_model_create_view(request, rest_form)

            message = f"Producto agregado: {title}"

            return Response({
                "alerta" : message,
                "producto" : title,
                "price": price,
                "description": description,
                "color": color
            })
                
        else:
            global prepare_delete_id   
            prepare_delete_id = serializer.data.get("id_")

            instance = product_model_detail_view(request, prepare_delete_id, rest=True)

            return Response({
                    "alerta" : "ELIMINAR DEFINITIVAMENTE?",
                    "producto" : instance.title,
                    "price": instance.price,
                    "description": instance.description,
                    "color": instance.color
                })


            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            id_ = serializer.validated_data.get("id_")
            title = serializer.validated_data.get("product")
            price = serializer.validated_data.get("price")
            description = serializer.validated_data.get("description")
            color = serializer.validated_data.get("color")
                          
            rest_form = [
                id_,
                title,
                price,
                description,
                color,
            ]

            message = product_model_update_view(request, rest_form[0], rest_form)

            if message:
                return Response({
                    "alerta" : message,
                    "producto" : title,
                    "price": price,
                    "description": description,
                    "color": color
                }) 
                

            else:
                return Response({"alerta": "ID_INVALIDO"})
                
        else:
            global prepare_delete_id
            prepare_delete_id = serializer.data.get("id_")

            instance = product_model_detail_view(request, prepare_delete_id, rest=True)

            return Response({
                    "alerta" : "ELIMINAR DEFINITIVAMENTE?",
                    "producto" : instance.title,
                    "price": instance.price,
                    "description": instance.description,
                    "color": instance.color
                })

            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        global prepare_delete_id

        return Response({"alerta": product_model_delete_view(request, prepare_delete_id, rest=True)})
