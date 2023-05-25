from django.urls import path
from .views import ProductViewSet, TestViewset, ReaderMenu

urlpatterns = [
    path("", ProductViewSet.as_view()),
    path("menu", ReaderMenu.as_view(),name="menu"),

    path("tvcreate/", TestViewset.as_view({"post": "create", "get": "create"}), name="tvcreate"),
    path("tvupdate/", TestViewset.as_view({"put": "update", "get": "create"}), name="tvupdate"),
    path("tvpartial_update/", TestViewset.as_view({"patch": "partial_update", "put": "partial_update", "get": "create"}), name="tvpartial_update"),
    path("tvdestroy/", TestViewset.as_view({"delete": "destroy"}), name="tvdestroy"),
    path("tvlist/", TestViewset.as_view({"get": "list"}), name="tvlist"),
    path("tvretrieve/", TestViewset.as_view({"get": "retrieve"}), name="tvretrieve"),   
]