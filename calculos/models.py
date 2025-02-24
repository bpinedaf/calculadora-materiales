from django.db import models
from materiales.models import Material  # ✅ Agregamos la importación

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class CalculoMateriales(models.Model):
    TIPO_CALCULO_CHOICES = [
        ('cimiento_corrido_1', 'Cimiento Corrido Tipo 1'),
        ('cimiento_corrido_2', 'Cimiento Corrido Tipo 2'),
        ('zapata_1', 'Zapata Tipo 1'),
        ('zapata_2', 'Zapata Tipo 2'),
        ('muro', 'Muro'),
        ('losa_fundida', 'Losa Fundida'),
        ('losa_vigueta_bovedilla', 'Losa con Vigueta y Bovedilla'),
        ('losa_acero', 'Losa de Acero'),
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
        help_text="Ejemplo: Cimentación Principal, Zapatas de Esquina, etc.",
        default="Sin descripción"
    )
    tipo_calculo = models.CharField(max_length=50, choices=TIPO_CALCULO_CHOICES)
    cantidad = models.FloatField(help_text="Cantidad en metros lineales o unidades", null=True, blank=True)
    area = models.FloatField(help_text="Área en metros cuadrados", null=True, blank=True)
    desperdicio = models.FloatField(default=5.0, help_text="Porcentaje de desperdicio")
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.proyecto.nombre} - {self.descripcion} - {self.tipo_calculo} - {self.cantidad if self.cantidad else self.area} unidades/m²"

class CalculoMaterialDetalle(models.Model):
    calculo = models.ForeignKey(CalculoMateriales, on_delete=models.CASCADE, related_name="materiales")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # ✅ Ahora sí reconoce `Material`
    cantidad_requerida = models.FloatField()
    cantidad_consumida = models.FloatField(default=0.0)
    cantidad_pendiente = models.FloatField()

    def __str__(self):
        return f"{self.material.nombre} - Req: {self.cantidad_requerida} - Cons: {self.cantidad_consumida} - Pend: {self.cantidad_pendiente}"

class TipoTrabajador(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tarifa_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_ml = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_dia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.tipo.nombre}"