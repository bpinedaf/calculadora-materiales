from django import forms
from .models import CalculoMateriales

class CalculoMaterialesForm(forms.ModelForm):
    class Meta:
        model = CalculoMateriales
        fields = ["descripcion", "tipo_calculo", "area", "desperdicio"]
