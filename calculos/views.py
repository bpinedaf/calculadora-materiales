import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from materiales.models import Material
from .models import CalculoMateriales, Proyecto, CalculoMaterialDetalle
from .forms import CalculoMaterialesForm


# Factores de consumo por m² para cada tipo de estructura
FACTORES_MATERIALES = {
    'muro': {
        'blocks': 12.5,  
        'cemento': 0.5,  
        'arena': 0.05,  
        'cal': 0.02,  
        'varilla_vertical': 1.67,  
        'varilla_horizontal': 1.33,  
        'sobrecimiento': 0.1,  
        'estribos_1/4': 1.5,  
    },
    'losa_vigueta_bovedilla': {
        'viguetas': 2.5,  
        'bovedillas': 6,  
        'malla_electrosoldada': 1,  
        'capa_compresion_concreto': 0.057,  
        'cemento': 1,  
        'arena': 0.25,  
        'grava': 0.3,  
        'agua': 50,  
        'puntales': 0.35,  
        'alambre_recocido': 0.5,  
        'acero_temperatura': 1.5,  
        'cimbra_madera': 0.6,  
    },
    'cimiento_corrido_1': {
        'concreto': 0.25,
        'varilla_1/2': 6,
        'estribos_1/4': 3.5,
        'block': 12,
        'solera_U': 2.5,
        'amarres': 1.7,
    },
    'cimiento_corrido_2': {
        'concreto': 0.30,
        'varilla_5/8': 7,
        'estribos_3/8': 4,
        'block': 15,
        'solera_U': 3,
        'amarres': 2,
    },
    'zapata_1': {
        'cemento': 8,
        'arena': 0.6,
        'grava': 0.9,
        'agua': 200,
        'acero': 18,
    },
    'zapata_2': {
        'cemento': 9,
        'arena': 0.7,
        'grava': 1.0,
        'agua': 220,
        'acero': 20,
    },
    'vigas_confinamiento': {
        'concreto': 0.08,  
        'varilla_1/2': 4,  
        'estribos_1/4': 2.5,  
    },
    'escaleras': {
        'concreto': 0.2,  
        'varilla_1/2': 6,  
        'estribos_1/4': 4,  
        'cimbra_madera': 0.5,  
        'puntales': 0.2,  
    },
    'piso': {
        'piezas_piso': 1.05,  
        'mortero_adhesivo': 4,  
        'cisa': 0.2,  
        'mortero_nivelacion': 0.02,  
    },
    'cielo_falso': {
        'paneles': 1.2,  
        'perfiles': 0.6,  
        'tornillos': 20,  
        'suspensiones': 0.3,  
        'anclajes': 0.15,  
        'aislante_termico': 0.8,  
        'arriostramiento_sismico': 0.2,  
    },
    'C-A': {  
        'concreto': 0.15,  
        'varilla_1/2': 4,  
        'estribos_1/4': 3,  
        'amarres': 0.8,  
        'cimbra_madera': 0.35,  
    },
    'C-B': {  
        'concreto': 0.12,  
        'varilla_3/8': 4,  
        'estribos_1/4': 2.5,  
        'amarres': 0.7,  
        'cimbra_madera': 0.3,  
    },
    'C-C': {  
        'concreto': 0.18,  
        'varilla_1/2': 5,  
        'estribos_1/4': 3.5,  
        'amarres': 0.9,  
        'cimbra_madera': 0.4,  
    },
    'C-D': {  
        'concreto': 0.22,  
        'varilla_1/2': 8,  
        'estribos_1/4': 4,  
        'amarres': 1.2,  
        'cimbra_madera': 0.45,  
    },
}


def calcular_materiales(request):
    proyectos = Proyecto.objects.all()
    tipos_calculo = sorted(CalculoMateriales.TIPO_CALCULO_CHOICES, key=lambda x: x[1])  # Ordena alfabéticamente por nombre
    #tipos_calculo = CalculoMateriales.TIPO_CALCULO_CHOICES  # Obtener opciones dinámicamente

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
        desperdicio = float(request.POST.get('desperdicio', 5)) / 100

        # Determinar cantidad basada en el tipo de cálculo
        if tipo_calculo in ['cimiento_corrido_1', 'cimiento_corrido_2']:
            cantidad = float(request.POST.get('metros_lineales', 0))  # Metros lineales
        elif tipo_calculo in ['zapata_1', 'zapata_2']:
            cantidad = int(request.POST.get('cantidad_zapatas', 0))  # Cantidad de zapatas
        else:
            cantidad = float(request.POST.get('area', 0))

        # Crear el cálculo de materiales
        calculo = CalculoMateriales.objects.create(
            proyecto=proyecto,
            descripcion=descripcion,
            tipo_calculo=tipo_calculo,
            cantidad=cantidad,
            desperdicio=desperdicio * 100
        )

        # Guardar los materiales en la base de datos
        if tipo_calculo in FACTORES_MATERIALES:
            for material_nombre, factor in FACTORES_MATERIALES[tipo_calculo].items():
                cantidad_requerida = cantidad * factor * (1 + desperdicio)
                cantidad_pendiente = cantidad_requerida  # Al inicio, nada ha sido consumido

                material_obj = Material.objects.filter(nombre__iexact=material_nombre).first()

                if not material_obj:
                    print(f"⚠️ Material {material_nombre} NO está en la base de datos. Se registrará con precio 0.0.")
                    unidad_predeterminada = "unidad"
                    material_obj = Material.objects.create(
                        nombre=material_nombre.capitalize(),
                        unidad=unidad_predeterminada,
                        precio_unitario=0.0
                    )

                CalculoMaterialDetalle.objects.create(
                    calculo=calculo,
                    material=material_obj,
                    cantidad_requerida=cantidad_requerida,
                    cantidad_consumida=0.0,
                    cantidad_pendiente=cantidad_pendiente
                )

        return redirect('calculos:ver_calculos', proyecto.id)

    return render(request, 'calculos/calculadora.html', {'proyectos': proyectos, 'tipos_calculo': tipos_calculo})





def ver_calculos_por_proyecto(request, proyecto_id):
    proyectos = Proyecto.objects.all()
    proyecto_seleccionado = get_object_or_404(Proyecto, id=proyecto_id)
    calculos = CalculoMateriales.objects.filter(proyecto=proyecto_seleccionado)

    resumen_costos = {}
    costo_total = 0
    calculos_detallados = []

    for calculo in calculos:
        tipo = calculo.tipo_calculo
        area = calculo.area
        desperdicio = calculo.desperdicio / 100  # Convertir a decimal

        materiales_consumidos = {}
        materiales_pendientes = {}

        if tipo in FACTORES_MATERIALES:
            for material, factor in FACTORES_MATERIALES[tipo].items():
                cantidad_requerida = area * factor * (1 + desperdicio)
                cantidad_pendiente = cantidad_requerida * ((100 - calculo.avance) / 100)
                cantidad_consumida = cantidad_requerida - cantidad_pendiente

                materiales_consumidos[material] = round(cantidad_consumida, 2)
                materiales_pendientes[material] = round(cantidad_pendiente, 2)

                # Agregar al resumen de costos
                material_obj = Material.objects.filter(nombre=material).first()
                if material_obj:
                    costo_material = material_obj.precio_unitario * cantidad_requerida
                    resumen_costos[material] = resumen_costos.get(material, 0) + costo_material
                    costo_total += costo_material

        calculos_detallados.append({
            "id": calculo.id,
            "descripcion": calculo.descripcion,
            "tipo_calculo": calculo.tipo_calculo,
            "area": calculo.area,
            "desperdicio": calculo.desperdicio,
            "avance": calculo.avance,
            "materiales_consumidos": materiales_consumidos,
            "materiales_pendientes": materiales_pendientes,
        })

    return render(
        request,
        "calculos/ver_calculos.html",
        {
            "proyectos": proyectos,
            "proyecto_seleccionado": proyecto_seleccionado,
            "calculos": calculos_detallados,
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
        detalles_materiales = CalculoMaterialDetalle.objects.filter(calculo=calculo)

        for detalle in detalles_materiales:
            avance = calculo.avance  # Obtener el porcentaje de avance
            data.append([
                proyecto.nombre,  # Nombre del Proyecto
                calculo.descripcion,  # Descripción del cálculo (Ej. "Muros Planta Baja")
                calculo.tipo_calculo,  # Tipo de Cálculo (Ej. "muro")
                calculo.fecha.strftime("%d/%m/%Y"),  # Fecha de Creación del Cálculo
                detalle.material.nombre,  # Nombre del Material
                detalle.material.unidad,  # Unidad de Medida
                round(detalle.cantidad_consumida, 2),  # Cantidad Consumida
                round(detalle.cantidad_pendiente, 2),  # Cantidad Pendiente
                detalle.material.precio_unitario if detalle.material.precio_unitario > 0 else "No registrado",  # Precio Unitario
                round(detalle.cantidad_consumida * float(detalle.material.precio_unitario), 2) if detalle.material.precio_unitario > 0 else 0,  # Costo por Material
                calculo.desperdicio,  # Desperdicio Estimado (%)
                round(detalle.cantidad_requerida * float(detalle.material.precio_unitario), 2) if detalle.material.precio_unitario > 0 else 0,  # Costo Total
                avance  # % de Avance
            ])

    if not data:
        return HttpResponse("No se generaron datos para la exportación.", content_type="text/plain")

    df = pd.DataFrame(data, columns=[
        "Proyecto", "Descripción del Cálculo", "Tipo de Cálculo",
        "Fecha de Cálculo", "Material", "Unidad", "Cantidad Consumida",
        "Cantidad Pendiente", "Precio Unitario", "Costo por Material",
        "Desperdicio Estimado", "Costo Total", "Avance (%)"
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
