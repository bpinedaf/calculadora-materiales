from django.shortcuts import render, redirect, get_object_or_404
from .models import Material
from .forms import MaterialForm
from calculos.models import Proyecto  # Importa el modelo de proyectos

def lista_materiales(request):
    materiales = Material.objects.all()
    return render(request, 'calculos/lista_materiales.html', {'materiales': materiales})


def home(request):
    proyectos = Proyecto.objects.all()  # Obtiene todos los proyectos
    
    return render(request, 'materiales/home.html', {'proyectos': proyectos})


def agregar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_materiales')  # Redirige a la lista después de agregar
    else:
        form = MaterialForm()
    
    return render(request, 'calculos/agregar_material.html', {'form': form})

    

def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('lista_materiales')
    else:
        form = MaterialForm(instance=material)

    return render(request, 'calculos/editar_material.html', {'form': form, 'material': material})

def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('lista_materiales')

    return render(request, 'calculos/eliminar_material.html', {'material': material})
