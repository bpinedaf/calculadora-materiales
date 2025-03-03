# Generated by Django 5.1.6 on 2025-02-21 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculos', '0004_calculomaterialdetalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculomateriales',
            name='tipo_calculo',
            field=models.CharField(choices=[('muro', 'Muro'), ('losa_fundida', 'Losa Fundida'), ('losa_vigueta_bovedilla', 'Losa con Vigueta y Bovedilla'), ('losa_acero', 'Losa de Acero'), ('cimentacion', 'Cimentación'), ('zapatas', 'Zapatas'), ('vigas_confinamiento', 'Vigas de Confinamiento'), ('escaleras', 'Escaleras'), ('piso', 'Piso Cerámico'), ('cielo_falso', 'Cielo Falso'), ('C-A', 'Columna Tipo A'), ('C-B', 'Columna Tipo B'), ('C-C', 'Columna Tipo C'), ('C-D', 'Columna Tipo D')], max_length=50),
        ),
    ]
