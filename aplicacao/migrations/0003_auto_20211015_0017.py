# Generated by Django 3.2.7 on 2021-10-15 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0002_auto_20211012_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado_evento',
            name='fk_Evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fK_Evento_Sincronizado', to='aplicacao.evento_sincronizado', verbose_name='Evento'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='parametros_gerais',
            name='Mod_Doc_Fisc_Permitido',
            field=models.CharField(choices=[('Nfce', 'Nfce'), ('Nfe', 'Nfe'), ('Todas', 'Todas')], max_length=50, verbose_name='Modalidade Documento Fiscal (NFe, NFce) Permitidas'),
        ),
    ]