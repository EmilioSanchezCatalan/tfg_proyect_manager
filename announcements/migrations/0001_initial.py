# Generated by Django 2.1.2 on 2018-12-10 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Abierta para proponer'), (1, 'Abierta para solucitudes'), (2, 'Cerrada')], verbose_name='Estado de la convocatoria')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('centers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='core.Centers', verbose_name='Centro')),
            ],
        ),
    ]
