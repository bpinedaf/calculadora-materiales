from django.contrib import admin
from .models import CalculoMateriales

@admin.register(CalculoMateriales)
class CalculoMaterialesAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'tipo_calculo', 'area', 'desperdicio', 'fecha')
    search_fields = ('nombre_proyecto',)
