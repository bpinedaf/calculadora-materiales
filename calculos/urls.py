
from django.urls import path
from . import views
from .views import (
    exportar_calculos_excel, actualizar_avance, ver_proyectos, 
    agregar_proyecto, eliminar_proyecto, calcular_materiales, 
    ver_calculos_por_proyecto, editar_calculo, eliminar_calculo,
    listar_tipos_trabajador, agregar_tipo_trabajador, 
    editar_tipo_trabajador, eliminar_tipo_trabajador, 
    gestionar_trabajadores, agregar_trabajador, editar_trabajador, 
    eliminar_trabajador, gestionar_materiales
)
from materiales.views import (
    lista_materiales, agregar_material, editar_material, eliminar_material
)

app_name = 'calculos'

urlpatterns = [
    # Rutas para la calculadora de materiales
    path('calculadora/', calcular_materiales, name='calcular_materiales'),
    path('ver_calculos/<int:proyecto_id>/', ver_calculos_por_proyecto, name='ver_calculos'),
    path('editar_calculo/<int:calculo_id>/', editar_calculo, name='editar_calculo'),
    path('eliminar_calculo/<int:calculo_id>/', eliminar_calculo, name='eliminar_calculo'),
    path('exportar_calculos/<int:proyecto_id>/', exportar_calculos_excel, name='exportar_calculos_excel'),
    path('actualizar_avance/', actualizar_avance, name='actualizar_avance'),

    # Rutas para la gestión de proyectos
    path('proyectos/', ver_proyectos, name='ver_proyectos'),
    path('proyectos/agregar/', agregar_proyecto, name='agregar_proyecto'),
    path('proyectos/eliminar/<int:proyecto_id>/', eliminar_proyecto, name='eliminar_proyecto'),

    # Rutas para la gestión de materiales
    path('materiales/', gestionar_materiales, name='gestionar_materiales'),
    path('materiales/lista/', lista_materiales, name='lista_materiales'),
    path('materiales/agregar/', agregar_material, name='agregar_material'),
    path('materiales/editar/<int:pk>/', editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', eliminar_material, name='eliminar_material'),

    # Rutas para la gestión de tipos de trabajador
    path('tipos-trabajador/', views.listar_tipos_trabajador, name='listar_tipos_trabajador'),
    path('tipos-trabajador/agregar/', views.agregar_tipo_trabajador, name='agregar_tipo_trabajador'),
    path('tipos-trabajador/editar/<int:tipo_id>/', views.editar_tipo_trabajador, name='editar_tipo_trabajador'),
    path('tipos-trabajador/eliminar/<int:tipo_id>/', views.eliminar_tipo_trabajador, name='eliminar_tipo_trabajador'),

    # Rutas para la gestión de trabajadores
    path('gestionar_trabajadores/', views.gestionar_trabajadores, name='gestionar_trabajadores'),
    path('trabajadores/agregar/', views.agregar_trabajador, name='agregar_trabajador'),
    path('trabajadores/editar/<int:trabajador_id>/', views.editar_trabajador, name='editar_trabajador'),
    path('trabajadores/eliminar/<int:trabajador_id>/', views.eliminar_trabajador, name='eliminar_trabajador'),
]
