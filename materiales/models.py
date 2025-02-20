from django.db import models

UNIDADES_MEDIDA = [
    ('unidad', 'Unidad'),
    ('m', 'Metro'),
    ('m2', 'Metro cuadrado'),
    ('m3', 'Metro cúbico'),
    ('kg', 'Kilogramo'),
    ('ton', 'Tonelada'),
    ('litro', 'Litro'),
    ('saco', 'Saco'),
]

class Material(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad = models.CharField(max_length=20, choices=UNIDADES_MEDIDA, default='unidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_consumida = models.FloatField(default=0.0, help_text="Cantidad total de material consumido")
    cantidad_pendiente = models.FloatField(default=0.0, help_text="Cantidad total de material pendiente")

    def __str__(self):
        return f"{self.nombre} ({self.unidad}) - Q{self.precio_unitario}"
