from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from ejercicios.views import *
from .serialize import *
import json

from rest_framework.viewsets import ViewSet
from django.shortcuts import redirect
import re


prepare_delete_id, pu_id = None, None


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
            title = serializer.validated_data.get("title")
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
                "title" : title,
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
                    "title" : instance.title,
                    "price": instance.price,
                    "description": instance.description,
                    "color": instance.color
                })


            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task=None):
        if task:
            serializer = self.serializer_class(data=task)
        
        else:
            serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():
            id_ = serializer.validated_data.get("id_")
            title = serializer.validated_data.get("title")
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

            print(f"\n{serializer}\n")

            if message:
                return Response({
                    "alerta" : message,
                    "title" : title,
                    "price": price,
                    "description": description,
                    "color": color
                }) 
                

            else:
                return Response({"alerta": "ID_INVALIDO"})
                
        else:
            print(f"\n{serializer}\n")
            global prepare_delete_id
            prepare_delete_id = serializer.data.get("id_")

            instance = product_model_detail_view(request, prepare_delete_id, rest=True)

            return Response({
                    "alerta" : "ELIMINAR DEFINITIVAMENTE?",
                    "title" : instance.title,
                    "price": instance.price,
                    "description": instance.description,
                    "color": instance.color
                })

            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        global prepare_delete_id
        if not pk:
            return Response({"alerta": product_model_delete_view(request, prepare_delete_id, rest=True)})
        else:
            return Response({"alerta": product_model_delete_view(request, pk, rest=True)})

class TestViewset(ViewSet):
    """Regresa un listado de caracteristicas de los Viewsets"""

    serializer_class = BaseSerializer

    def list(self, request):
        content = {
            "funciones": [
                {"create": "POST"},
                {"update": "PUT"},
                "partial_update",
                "destroy",
                "list",
                "retrieve/id del producto",
                "retrieve/gen (consultar id)"
            ]
        }

        return Response(content)

    def create(self, request):
        """Creamos una instancia en la cual entramos a ProductViewSet.post"""
        product_viewset = ProductViewSet()  
        response = product_viewset.post(request)

        return Response(response.data, status=response.status_code)

    def retrieve(self, request, pk=None):
        """Maneja la consulta de un objeto por su id"""      

        return Response(pk)

    def update(self, request, pk=None):
        """Maneja la consulta de un objeto por su id"""
        product_viewset = ProductViewSet()  
        response = product_viewset.put(request)

        return Response(response.data, status=response.status_code)

    def partial_update(self, request, pk=None):
        global pu_id   
        
        """
        En partial update se necesita primero establecer en la vista menú
        partial_update/id esto para que se identifique el producto

        Despues se tendrá que accesar la opcion.
        Ejemplo:

                title:Monitor 144hz

        esto indicara a lprograma que el titulo sel producto sera cambiado.
        """

        if pu_id:
            for_instance = list(pk.keys())[1]
            task = product_model_list_view(request,rest="p_upd",pk=pu_id)

            task[for_instance] = pk[for_instance] 

            product_viewset = ProductViewSet()  
            response = product_viewset.put(request, task=task)

            return Response(response)

        return Response(pk)

    def destroy(self, request, pk=None):
        """Maneja la eliminacion de un objeto por su id"""

        product_viewset = ProductViewSet()  
        response = product_viewset.delete(request, pk)

        return Response(response.data, status=response.status_code)


class ReaderMenu(views.APIView):
    serializer_class = MenuSerializer

    def get(self, request):
        content = {
            "introduzca": [
                "create",
                "update",
                "partial_update/id del producto",
                "destroy/id del producto",
                "list",
                "retrieve/id del producto",
                "retrieve/gen (consultar id)"
            ]
        }
        return Response(content)

    def post(self, request):
        global pu_id
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():        
            task = serializer.validated_data.get("task")

            if "retrieve" in task or "partial_update" in task or "destroy" in task:
                try:
                    product = re.findall("/([\w\W ]+)", task)[0]
                
                except IndexError:
                    pass

                if product != "gen":
                    
                    if "retrieve" in task:
                        product_ = product_model_list_view(request,rest="retrieve",pk=product)
                        ret_testview = TestViewset()
                        response = ret_testview.retrieve(request, pk=product_)
                    
                    elif "destroy" in task:
                        ret_testview = TestViewset()
                        response = ret_testview.destroy(request, pk=product)
                    
                    else:
                        pu_id = product
                        product_ = product_model_list_view(request,rest="upd",pk=product)
                        
                        product_['indicaciones'] = {
                            'INSERTE' : 'Key:cambio requerido',
                            'EJEMPLO' : 'title: Un nuevo mouse'
                            }
        
                        ret_testview = TestViewset()
                        response = ret_testview.retrieve(request, pk=product_)

                else:
                    text = product_model_list_view(request,rest=True)
                    json_ = json.loads(text)
                    content = {}

                    count = 0
                    for element in json_:            
                        content[f"id: {element['pk']}"] =element['fields']['title']
                        count += 1

                    return Response(content)

                return Response(response.data, status=response.status_code)
            
            elif task == "return":
                return redirect("menu")

            else:
                try:
                    task = re.findall("([\w\W ]+):", task)[0]
                    if task in ["title", "description", "price", "color"]:
                        #product_ = product_model_list_view(request,rest="upd",pk=product)
                        try:
                            new = re.findall(":([\w\W ]+)", task)[0]
                            task = re.findall("([\w\W ]+):", task)[0]
                        except IndexError:
                            pass

                        ret_testview = TestViewset()
                        response = ret_testview.partial_update(request, pk={"action": "upd", task: new})

                        return redirect("menu")
                except IndexError:
                    return redirect(f"tv{task}")