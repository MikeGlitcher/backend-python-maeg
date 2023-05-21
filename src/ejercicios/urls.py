from django.urls import path
from ejercicios import views


urlpatterns = [
    path("", views.product_model_list_view, name="list"),
    path("create", views.product_model_create_view, name="create"),
    path("<int:product_id>", views.product_model_detail_view, name="detail"),
    path("<int:product_id>/edit", views.product_model_update_view, name="edit"),
    path("<int:product_id>/del", views.product_model_delete_view, name="delete"),
]