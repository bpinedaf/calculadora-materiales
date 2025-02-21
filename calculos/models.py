from django.db import models
from materiales.models import Material  # ✅ Agregamos la importación

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
        ('zapatas', 'Zapatas'),
        ('vigas_confinamiento', 'Vigas de Confinamiento'),
        ('escaleras', 'Escaleras'),
        ('piso', 'Piso Cerámico'),
        ('cielo_falso', 'Cielo Falso'),
        ('C-A', 'Columna Tipo A'),
        ('C-B', 'Columna Tipo B'),
        ('C-C', 'Columna Tipo C'),
        ('C-D', 'Columna Tipo D'),
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

class CalculoMaterialDetalle(models.Model):
    calculo = models.ForeignKey(CalculoMateriales, on_delete=models.CASCADE, related_name="materiales")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # ✅ Ahora sí reconoce `Material`
    cantidad_requerida = models.FloatField()
    cantidad_consumida = models.FloatField(default=0.0)
    cantidad_pendiente = models.FloatField()

    def __str__(self):
        return f"{self.material.nombre} - Req: {self.cantidad_requerida} - Cons: {self.cantidad_consumida} - Pend: {self.cantidad_pendiente}"
