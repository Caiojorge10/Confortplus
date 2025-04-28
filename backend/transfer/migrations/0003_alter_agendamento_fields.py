from django.db import migrations, models
from datetime import datetime

def split_datetime(apps, schema_editor):
    Agendamento = apps.get_model('transfer', 'Agendamento')
    for agendamento in Agendamento.objects.all():
        if agendamento.data_hora:
            agendamento.data = agendamento.data_hora.date()
            agendamento.hora = agendamento.data_hora.time()
            agendamento.save()

def combine_datetime(apps, schema_editor):
    Agendamento = apps.get_model('transfer', 'Agendamento')
    for agendamento in Agendamento.objects.all():
        if agendamento.data and agendamento.hora:
            agendamento.data_hora = datetime.combine(agendamento.data, agendamento.hora)
            agendamento.save()

class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0002_agendamento_quantidade_pessoas'),  # Corrigido para a migração real
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='data',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='hora',
            field=models.TimeField(null=True),
        ),
        migrations.RunPython(split_datetime, combine_datetime),
        migrations.RemoveField(
            model_name='agendamento',
            name='data_hora',
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='data',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='hora',
            field=models.TimeField(),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='forma_pagamento',
            field=models.CharField(
                choices=[
                    ('CREDITO', 'Cartão de Crédito'),
                    ('DEBITO', 'Cartão de Débito'),
                    ('BOLETO', 'Boleto'),
                    ('PIX', 'PIX'),
                    ('DINHEIRO', 'Dinheiro')
                ],
                default='PIX',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='valor_adiantamento',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10
            ),
        ),
        migrations.AlterModelOptions(
            name='agendamento',
            options={'ordering': ['-data', '-hora']},
        ),
    ] 