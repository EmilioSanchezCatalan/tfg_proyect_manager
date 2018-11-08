# Generated by Django 2.1.2 on 2018-11-08 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tfgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField()),
                ('mode', models.PositiveSmallIntegerField()),
                ('is_team', models.BooleanField()),
                ('objectives', models.TextField()),
                ('methodology', models.TextField()),
                ('docs_and_forms', models.TextField()),
                ('departament_validation', models.BooleanField()),
                ('center_validation', models.BooleanField()),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('carrers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Carrers')),
                ('itineraries', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Itineraries')),
                ('mentions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Mentions')),
                ('skills', models.ManyToManyField(to='core.Skills')),
                ('tutor1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tutor2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Tutor2')),
            ],
        ),
    ]
