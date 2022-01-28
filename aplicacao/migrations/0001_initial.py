# Generated by Django 3.2.7 on 2021-10-12 15:10

import aplicacao.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contato_Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=250, verbose_name='Nome Contato')),
                ('Funcao', models.CharField(blank=True, max_length=250, null=True, verbose_name='Função Contato')),
                ('Telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('Celular', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
                ('Observacao', models.CharField(blank=True, max_length=250, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Contato_Empresa',
                'verbose_name_plural': 'Contatos Empresa',
            },
        ),
        migrations.CreateModel(
            name='Evento_Sincronizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data_Criacao_Evento', models.DateField(blank=True, null=True, verbose_name='Data Criação Evento')),
                ('Tipo_Doc_Fiscal', models.CharField(blank=True, choices=[('NFE', 'NFE'), ('NFCE', 'NFCE')], max_length=50, null=True, verbose_name='Tipo Doc')),
                ('Data_Emissao', models.DateField(blank=True, null=True, verbose_name='Data Emissão')),
                ('Num_Doc', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero Doc')),
                ('Serie_Dov', models.CharField(blank=True, max_length=50, null=True, verbose_name='Serie Doc')),
                ('Status_Doc', models.CharField(blank=True, choices=[('Enviada', 'Enviada'), ('Pendente', 'Pendente'), ('Contigencia', 'Contigencia'), ('Erro', 'Erro')], max_length=50, null=True, verbose_name='Status Doc')),
                ('Id_Tab_Orig', models.CharField(blank=True, max_length=50, null=True, verbose_name='Id Tabela Origem')),
                ('Registro_Sincronizado', models.CharField(blank=True, choices=[('Sim', 'Sim'), ('Nao', 'Nao')], max_length=50, null=True, verbose_name='Registro Sincronizado')),
                ('Empresa_Orig', models.CharField(blank=True, max_length=150, null=True, verbose_name='Empresa')),
                ('Contato_Orig', models.CharField(max_length=250, verbose_name='Nome Contato')),
                ('Telefone_Orig', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('Celular_Orig', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
            ],
            options={
                'verbose_name': 'Evento_Sincronizado',
                'verbose_name_plural': 'Eventos_Sincronizados',
            },
        ),
        migrations.CreateModel(
            name='Parametros_Gerais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tempo_Avisos_Minutos', models.IntegerField(verbose_name='Tempo de Emissão de Alertas/Aviso de Erros Identificados')),
                ('Tipo_Situ_Permitidas', models.CharField(choices=[('Enviada', 'Enviada'), ('Pendente', 'Pendente'), ('Contigencia', 'Contigencia'), ('Erro', 'Erro'), ('Todas', 'Todas')], max_length=50, verbose_name='Tipo de Sincronização  Permitida (Enviadas, Pendentes, Contigencia, Erro)')),
                ('Mod_Doc_Fisc_Permitido', models.CharField(choices=[('Nfce', 'Nfce'), ('Nfe', 'Nfe')], max_length=50, verbose_name='Modalidade Documento Fiscal (NFe, NFce) Permitidas')),
                ('Situacao_Sincronizacao', models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')], max_length=50, verbose_name='Situação - Sincronização dos Dados')),
            ],
            options={
                'verbose_name': 'Parametros_Gerais',
                'verbose_name_plural': 'Parametros_Gerais',
            },
        ),
        migrations.CreateModel(
            name='Chamado_Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Atendente', models.CharField(max_length=250, verbose_name='Nome Atendente')),
                ('Situacao_Evento', models.CharField(choices=[('Solucionado', 'Solucionado'), ('Pendente', 'Pendente'), ('Não Identificado', 'Não Identificado'), ('Empresa - Falha no Contato', 'Empresa - Falha no Contato'), ('Empresa - Retornar Contato', 'Empresa - Retornar Contato')], max_length=250, verbose_name='Situação do Evento')),
                ('Data_Retorno', models.DateField(blank=True, null=True, verbose_name='Data Contato')),
                ('Observacao', models.CharField(max_length=250, verbose_name='Observação')),
                ('fk_Evento', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='fK_Evento_Sincronizado', to='aplicacao.evento_sincronizado', verbose_name='Usuário cadastro')),
            ],
            options={
                'verbose_name': 'Chamado_Evento',
                'verbose_name_plural': 'Chamado_Eventos',
            },
        ),
        migrations.CreateModel(
            name='CustomUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nameuser', models.CharField(max_length=60, unique=True, verbose_name='Nome usuario')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('fone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Membro da equipe')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', aplicacao.models.UsuarioManager()),
            ],
        ),
    ]
