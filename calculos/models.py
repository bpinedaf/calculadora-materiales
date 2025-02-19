from django.db import models

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class CalculoMateriales(models.Model):
    TIPO_CALCULO_CHOICES = [
        ('muro', 'Muro'),
        ('losa_fundida', 'Losa Fundida'),
        ('losa_vigueta_bovedilla', 'Losa con Vigueta y Bovedilla'),
        ('losa_acero', 'Losa de Acero'),
        ('cimentacion', 'Cimentación'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="calculos")
    descripcion = models.CharField(
        max_length=200,
        help_text="Ejemplo: Muro Perimetral, Losa Segundo Nivel, Cimentación",
        default="Sin descripción"
    )
    tipo_calculo = models.CharField(max_length=50, choices=TIPO_CALCULO_CHOICES)
    area = models.FloatField(help_text="Área en metros cuadrados")
    desperdicio = models.FloatField(default=5.0, help_text="Porcentaje de desperdicio")
    fecha = models.DateTimeField(auto_now_add=True)
    avance = models.FloatField(default=0.0, help_text="Porcentaje de avance de la obra")

    def __str__(self):
        return f"{self.proyecto.nombre} - {self.descripcion} - {self.tipo_calculo} - {self.area} m²"
