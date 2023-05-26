from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from .models import ProductModels
from .forms import ProductModelsForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q



def instance_repair(instance, queryset=None, title=None):
    if queryset:
        ids = ProductModels.objects.all().order_by('-id').values_list('id', flat=True)

        reference = ids[0]

        instance.id = None

        for element in ids:
            
            if element != reference:
                instance.id = reference
                break

            reference += 1
        
        if not instance.id:
            instance.id = queryset.count() + 1

    conca = ""
    for word in title.split(" "):
        try:
            conca += " " + word.capitalize()
        except Exception:
            conca += " " + word

    return [instance.id, conca.strip()]


def product_model_list_view(request, rest=False, pk=None):
    if not rest:
        query = request.GET.get("q", None)
        queryset = ProductModels.objects.all()
        if query is not None:
            queryset = queryset.filter(
                Q(title__contains=query.title()) |
                Q(price__contains=query)
                )

            if not queryset:
                queryset = ["Producto no encontrado"]

        context = {
            "products" : queryset
        }


        if request.user.is_authenticated:
            context["p_title"] = "Vista ADMIN"
            template = "list-detail.html"
            
        else:
            context["p_title"] = "Vista Publica"
            template = "search.html"
        
    
        return render(request, template, context)
    
    else:
        if rest == "retrieve":
    
            instance = get_object_or_404(ProductModels, id=pk)

            return {"product": instance.title}
        
        elif rest == "upd":
            instance = get_object_or_404(ProductModels, id=pk)

            return {
                "title": instance.title,
                "price": instance.price,
                "description": instance.description,
                "color": instance.color
            }
        elif rest == "p_upd":
            instance = get_object_or_404(ProductModels, id=pk)

            return {
                "id_" : instance.id,
                "title": instance.title,
                "price": instance.price,
                "description": instance.description,
                "color": instance.color
            }

        else:
            queryset = ProductModels.objects.all()
            serialized_data = serializers.serialize('json', queryset)
            return serialized_data

def product_model_create_view(request, rest_data=False):
    
    if not rest_data:
        form = ProductModelsForm(request.POST or None)
        queryset = ProductModels.objects.all()

        if form.is_valid():
            instance = form.save(commit=False)

            for_instance = instance_repair(instance, queryset, instance.title)

            instance.title = for_instance[1]

            instance.save()
            messages.success(request, "Producto creado con exito")
            return HttpResponseRedirect("/ejercicios/{product_id}".format(product_id=instance.id))
        
        context = {
            "form":form
        }

        template = "create.html"
        
        return render(request, template, context)
    
    else:
        form = ProductModelsForm()
        queryset = ProductModels.objects.all()

        instance = form.save(commit=False)

        for_instance = instance_repair(instance, queryset, str(rest_data[0]))

        instance.id = for_instance[0]
        instance.title = for_instance[1]

        instance.price = rest_data[1]
        instance.description = rest_data[2]
        instance.color = rest_data[3]

        instance.save()      

def product_model_detail_view(request, product_id, rest=False):
    if not rest:
        instance = get_object_or_404(ProductModels, id=product_id)
        context = {
            "product" : instance
        }

        template = "detail.html"

        return render(request, template, context)
    else:
        instance = get_object_or_404(ProductModels, id=product_id)
        
        return instance

def product_model_update_view(request, product_id=None, rest_data=None):
    if not rest_data:
        instance = get_object_or_404(ProductModels, id=product_id)
        form = ProductModelsForm(request.POST or None, instance=instance)
        queryset = ProductModels.objects.all()

        if form.is_valid():
            instance = form.save(commit=False)

            for_instance = instance_repair(instance, None, instance.title)

            instance.title = for_instance[1]

            instance.save()
            messages.success(request, "Producto actualizado con exito")
            return HttpResponseRedirect("/ejercicios/{product_id}".format(product_id=instance.id))
        
        context = {
            "form":form
        }

        template = "update.html"
        
        return render(request, template, context)

    else:
        instance = get_object_or_404(ProductModels, id=product_id)
        form = ProductModelsForm(instance=instance)
        queryset = ProductModels.objects.all()

        instance = form.save(commit=False)

        for_instance = instance_repair(instance, None, str(rest_data[1]))

        instance.title = for_instance[1]
        instance.price = rest_data[2]
        instance.description = rest_data[3]
        instance.color = rest_data[4]

        instance.save()

        return "PRODUCTO ACTUALIZADO"     

def product_model_delete_view(request, product_id, rest=False):
    instance = get_object_or_404(ProductModels, id=product_id)

    if not rest:
        if request.method == "POST":
            instance.delete()
            HttpResponseRedirect("/ejercicios/")
            messages.success(request, "Producto eliminado")
            return HttpResponseRedirect("/ejercicios/")
        
        context = {
            "product" : instance
        }

        template = "delete.html"

        return render(request, template, context)

    else:
        message = f"PRODUCTO: {instance.title} ELIMINADO DEFINITIVAMENTE"
        try:
            instance.delete()
            
            return message

        except Exception:
            return "ID INVALIDO"