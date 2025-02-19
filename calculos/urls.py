from django.urls import path
from . import views
from .views import exportar_calculos_excel, actualizar_avance, ver_proyectos, agregar_proyecto, eliminar_proyecto
from materiales.views import lista_materiales, agregar_material, editar_material, eliminar_material

app_name = 'calculos'

urlpatterns = [
    path('calculadora/', views.calcular_materiales, name='calcular_materiales'),
    path('ver_calculos/<int:proyecto_id>/', views.ver_calculos_por_proyecto, name='ver_calculos'),
    path('editar_calculo/<int:calculo_id>/', views.editar_calculo, name='editar_calculo'),
    path('eliminar_calculo/<int:calculo_id>/', views.eliminar_calculo, name='eliminar_calculo'),
    path('exportar_calculos/<int:proyecto_id>/', exportar_calculos_excel, name='exportar_calculos_excel'),
    path('actualizar_avance/', actualizar_avance, name='actualizar_avance'),
    path('proyectos/', ver_proyectos, name='ver_proyectos'),
    path('proyectos/agregar/', agregar_proyecto, name='agregar_proyecto'),
    path('proyectos/eliminar/<int:proyecto_id>/', eliminar_proyecto, name='eliminar_proyecto'),
    path('materiales/', views.gestionar_materiales, name='gestionar_materiales'),
    path('materiales/', lista_materiales, name='lista_materiales'),
    path('materiales/agregar/', agregar_material, name='agregar_material'),
    path('materiales/editar/<int:pk>/', editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', eliminar_material, name='eliminar_material'),
]
