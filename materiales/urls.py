from django.urls import path
from .views import lista_materiales, home, agregar_material, editar_material, eliminar_material

urlpatterns = [
    path('', home, name='home'),  # Página principal
    path('materiales/', lista_materiales, name='lista_materiales'),
    path('materiales/agregar/', agregar_material, name='agregar_material'),
    path('materiales/editar/<int:pk>/', editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', eliminar_material, name='eliminar_material'),


]
