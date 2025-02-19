import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from materiales.models import Material
from .models import CalculoMateriales, Proyecto
from .forms import CalculoMaterialesForm


# Factores de consumo por m² para cada tipo de estructura
FACTORES_MATERIALES = {
    'muro': {
        'blocks': 12.5,
        'cemento': 0.5,
        'arena': 0.05,
        'cal': 0.02,
    },
    'losa_fundida': {
        'cemento': 7,
        'arena': 0.7,
        'grava': 0.7,
        'agua': 175,
    },
    'losa_vigueta_bovedilla': {
        'viguetas': 2.5,
        'bovedillas': 6,
        'cemento': 1,
        'arena': 0.05,
    },
    'losa_acero': {
        'placas_acero': 1,
        'pernos': 4,
        'cemento': 0.8,
    },
    'cimentacion': {
        'cemento': 9,
        'arena': 0.8,
        'grava': 0.8,
        'agua': 180,
    },
    'zapatas': {
        'cemento': 7,  # Sacos de cemento por m³ de concreto
        'arena': 0.5,  # m³ de arena por m³ de concreto
        'grava': 0.7,  # m³ de grava por m³ de concreto
        'agua': 180,   # Litros de agua por m³ de concreto
        'acero': 15,   # Kg de acero por m²
    },
    'repello': {
        'cemento': 3,  # Sacos de cemento por cada 10 m²
        'arena': 0.1,  # m³ de arena por m²
    },
    'piso': {
        'cemento': 3.5,  # Sacos de cemento por m²
        'arena': 0.12,
        'grava': 0.15,
    },
    'cielo_falso': {
        'paneles': 1.2,  # Paneles de gypsum por m²
        'perfiles': 0.5,  # Metros lineales de perfil metálico
        'tornillos': 20,  # Cantidad de tornillos
    },
}

def calcular_materiales(request):
    proyectos = Proyecto.objects.all()
    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto_existente')
        nuevo_proyecto_nombre = request.POST.get('nuevo_proyecto')
        descripcion = request.POST.get('descripcion')
        
        if nuevo_proyecto_nombre:
            proyecto, created = Proyecto.objects.get_or_create(nombre=nuevo_proyecto_nombre)
        elif proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        else:
            return render(request, 'calculos/error.html', {'mensaje': 'Debes seleccionar o crear un proyecto'})

        tipo_calculo = request.POST.get('tipo_calculo')
        area = float(request.POST.get('area', 0))
        desperdicio = float(request.POST.get('desperdicio', 5)) / 100

        CalculoMateriales.objects.create(
            proyecto=proyecto,
            descripcion=descripcion,
            tipo_calculo=tipo_calculo,
            area=area,
            desperdicio=desperdicio * 100
        )
        return redirect('calculos:ver_calculos', proyecto.id)
    
    return render(request, 'calculos/calculadora.html', {'proyectos': proyectos})



def ver_calculos_por_proyecto(request, proyecto_id):
    proyectos = Proyecto.objects.all()
    proyecto_seleccionado = get_object_or_404(Proyecto, id=proyecto_id)
    calculos = CalculoMateriales.objects.filter(proyecto=proyecto_seleccionado)

    resumen_costos = {}
    costo_total = 0

    for calculo in calculos:
        materiales = Material.objects.all()
        for material in materiales:
            if material.nombre not in resumen_costos:
                resumen_costos[material.nombre] = 0
            resumen_costos[material.nombre] += material.precio_unitario * calculo.area
            costo_total += material.precio_unitario * calculo.area

    return render(
        request,
        "calculos/ver_calculos.html",
        {
            "proyectos": proyectos,
            "proyecto_seleccionado": proyecto_seleccionado,
            "calculos": calculos,
            "resumen_costos": resumen_costos,
            "costo_total": costo_total,
        },
    )


def editar_calculo(request, calculo_id):
    calculo = get_object_or_404(CalculoMateriales, id=calculo_id)
    if request.method == "POST":
        form = CalculoMaterialesForm(request.POST, instance=calculo)
        if form.is_valid():
            form.save()
            return redirect("calculos:ver_calculos", calculo.proyecto.id)
    else:
        form = CalculoMaterialesForm(instance=calculo)
    return render(request, "calculos/editar_calculo.html", {"form": form, "calculo": calculo})

def eliminar_calculo(request, calculo_id):
    calculo = get_object_or_404(CalculoMateriales, id=calculo_id)
    if request.method == "POST":
        proyecto_id = calculo.proyecto.id
        calculo.delete()
        return redirect("calculos:ver_calculos", proyecto_id)
    return render(request, "calculos/eliminar_calculo.html", {"calculo": calculo})

def exportar_calculos_excel(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    calculos = CalculoMateriales.objects.filter(proyecto=proyecto)
    data = []
    for calculo in calculos:
        for material in Material.objects.all():
            data.append([
                proyecto.nombre,
                calculo.fecha_calculo.strftime("%d/%m/%Y"),
                calculo.fecha_reporte.strftime("%d/%m/%Y") if calculo.fecha_reporte else "N/A",
                material.nombre,
                material.unidad_medida,
                calculo.cantidad_consumida,
                calculo.cantidad_pendiente,
                material.precio_unitario,
                calculo.cantidad_consumida * material.precio_unitario,
                calculo.desperdicio_estimado,
                calculo.costo_total
            ])
    df = pd.DataFrame(data, columns=[
        "Proyecto", "Fecha de Cálculo", "Último Reporte",
        "Material", "Unidad", "Cantidad Consumida",
        "Cantidad Pendiente", "Precio Unitario",
        "Costo por Material", "Desperdicio Estimado", "Costo Total"
    ])
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="calculos_{proyecto.nombre}.xlsx"'
    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Cálculos")
    return response

def actualizar_avance(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith("avance_"):
                calculo_id = key.split("_")[1]
                calculo = CalculoMateriales.objects.get(id=calculo_id)
                calculo.avance = float(value)
                calculo.save()
    return redirect(request.META.get('HTTP_REFERER', 'calculos:ver_calculos'))

def ver_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'calculos/ver_proyectos.html', {'proyectos': proyectos})

def agregar_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Proyecto.objects.create(nombre=nombre)
    return redirect('calculos:ver_proyectos')

def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    return redirect('calculos:ver_proyectos')

def gestionar_materiales(request):
    materiales = Material.objects.all()
    return render(request, 'calculos/gestionar_materiales.html', {'materiales': materiales})

def home(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'calculos/home.html', {'proyectos': proyectos})
