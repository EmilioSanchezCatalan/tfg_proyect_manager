# Generated by Django 2.1.2 on 2018-11-08 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tfms', '0001_initial'),
        ('tfgs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('dni', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=150)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('tfgs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tfgs.Tfgs')),
                ('tfms', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tfms.Tfms')),
            ],
        ),
        migrations.CreateModel(
            name='Userinfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('areas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Areas')),
                ('auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('centers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Centers')),
                ('departaments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Departaments')),
            ],
        ),
    ]
