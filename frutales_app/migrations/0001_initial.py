# Generated by Django 3.2.9 on 2022-01-21 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AdicionalOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('nombre_adicional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frutales_app.adicional')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='productos')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('number_phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.TimeField(auto_now=True)),
                ('updated_at', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.CharField(max_length=90)),
                ('tamaño', models.CharField(max_length=80)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precio', to='frutales_app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamañoproducto', models.CharField(max_length=100)),
                ('especificaciones', models.TextField()),
                ('entrega', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=50)),
                ('finalizado', models.BooleanField(default=False)),
                ('created_at', models.TimeField(auto_now=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('globoadicional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='globos', to='frutales_app.adicionalorden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frutales_app.producto')),
                ('rosaadicional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rosas', to='frutales_app.adicionalorden')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frutales_app.usuario')),
            ],
        ),
    ]
