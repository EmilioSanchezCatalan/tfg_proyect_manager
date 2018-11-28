# Generated by Django 2.1.2 on 2018-11-27 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Carrers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Grado',
                'verbose_name_plural': 'Grados',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Centers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Centro',
                'verbose_name_plural': 'Centros',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Departaments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Itineraries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('carrers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='core.Carrers', verbose_name='Titulación')),
            ],
            options={
                'verbose_name': 'Itinerario',
                'verbose_name_plural': 'Itinerarios',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Masters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('centers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masters', to='core.Centers', verbose_name='Centro de validación')),
                ('departament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master', to='core.Departaments', verbose_name='Departamento de validación')),
                ('departaments', models.ManyToManyField(related_name='masters', to='core.Departaments', verbose_name='Departamentos que imparten')),
            ],
            options={
                'verbose_name': 'Master',
                'verbose_name_plural': 'Masters',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Mentions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('carrers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentions', to='core.Carrers', verbose_name='Titulación')),
            ],
            options={
                'verbose_name': 'Mencion',
                'verbose_name_plural': 'Menciones',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Iniciales')),
                ('text', models.TextField(verbose_name='Descripción')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('itineraries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='core.Itineraries', verbose_name='Competencias')),
            ],
            options={
                'verbose_name': 'Competencia',
                'verbose_name_plural': 'Competencias',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tutor2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre completo')),
                ('curriculum_vitae', models.FileField(blank=True, null=True, upload_to='cv', verbose_name='Curriculum')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Areas', verbose_name='Area de conocimiento')),
                ('departament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Departaments', verbose_name='Departamento')),
            ],
            options={
                'verbose_name': 'Tutor de apoyo',
                'verbose_name_plural': 'Tutores de apoyo',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='carrers',
            name='centers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrers', to='core.Centers', verbose_name='Centro de validación'),
        ),
        migrations.AddField(
            model_name='carrers',
            name='departament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrer', to='core.Departaments', verbose_name='Departamento de validación'),
        ),
        migrations.AddField(
            model_name='carrers',
            name='departaments',
            field=models.ManyToManyField(related_name='carrers', to='core.Departaments', verbose_name='Departamentos que imparten'),
        ),
        migrations.AddField(
            model_name='areas',
            name='departaments',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='core.Departaments', verbose_name='Departamento'),
        ),
    ]
