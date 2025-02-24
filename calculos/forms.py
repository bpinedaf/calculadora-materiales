from django import forms
from .models import CalculoMateriales, TipoTrabajador, Trabajador

class CalculoMaterialesForm(forms.ModelForm):
    class Meta:
        model = CalculoMateriales
        fields = ["descripcion", "tipo_calculo", "area", "desperdicio"]

class TipoTrabajadorForm(forms.ModelForm):
    class Meta:
        model = TipoTrabajador
        fields = ['nombre', 'tarifa_m2', 'tarifa_ml', 'tarifa_dia']

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'tipo']
