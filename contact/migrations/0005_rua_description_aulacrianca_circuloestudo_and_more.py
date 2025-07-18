# Generated by Django 5.2.1 on 2025-06-25 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_delete_category_contact_rua'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rua',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='AulaCrianca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('serie', models.CharField(blank=True, max_length=100)),
                ('licao', models.CharField(blank=True, max_length=100)),
                ('dia_semana', models.CharField(blank=True, max_length=30)),
                ('data_ultima_aula', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('show', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('participantes', models.ManyToManyField(related_name='aulas_crianca', to='contact.contact')),
                ('professor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aulas_como_professor', to='contact.contact')),
                ('rua', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aulas_crianca', to='contact.rua')),
            ],
        ),
        migrations.CreateModel(
            name='CirculoEstudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('dia_semana', models.CharField(blank=True, max_length=30)),
                ('data_ultimo_encontro', models.DateField(blank=True, null=True)),
                ('livro', models.CharField(blank=True, max_length=100)),
                ('unidade', models.CharField(blank=True, max_length=100)),
                ('secao', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('show', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('participantes', models.ManyToManyField(related_name='circulos_estudo', to='contact.contact')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circulos_como_tutor', to='contact.contact')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoFamilias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_ultima_reflexao', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('show', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('participantes', models.ManyToManyField(related_name='grupos_familias', to='contact.contact')),
                ('ruas', models.ManyToManyField(related_name='grupos_familias', to='contact.rua')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoPreJovens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('livro', models.CharField(blank=True, max_length=100)),
                ('licoes', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('data_ultimo_encontro', models.DateField(blank=True, null=True)),
                ('dia_semana', models.CharField(blank=True, max_length=30)),
                ('show', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('pre_jovens', models.ManyToManyField(related_name='grupos_pre_jovens', to='contact.contact')),
                ('rua', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grupos_pre_jovens', to='contact.rua')),
            ],
        ),
    ]
