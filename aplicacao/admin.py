from django.contrib import admin

# Register your models here.
from .models import Contato_Empresa, Evento_Sincronizado, Chamado_Evento, Parametros_Gerais, CustomUsuario

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm


@admin.register(Contato_Empresa)
class Contato_EmpresaAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Funcao', 'Telefone', 'Celular', 'Observacao')

@admin.register(Evento_Sincronizado)
class Evento_SincronizadoAdmin(admin.ModelAdmin):
    list_display = ('Data_Criacao_Evento', 'Tipo_Doc_Fiscal', 'Data_Emissao', 'Num_Doc', 'Serie_Dov', 'Status_Doc', 'Id_Tab_Orig', 'Registro_Sincronizado', 'Empresa_Orig', 'Contato_Orig', 'Telefone_Orig', 'Celular_Orig'
)

@admin.register(Chamado_Evento)
class Chamado_EventoAdmin(admin.ModelAdmin):
    list_display = ('fk_Evento', 'Atendente', 'Situacao_Evento', 'Data_Retorno', 'Observacao')

@admin.register(Parametros_Gerais)
class Parametros_GeraisAdmin(admin.ModelAdmin):
    list_display = ('Tempo_Avisos_Minutos', 'Tipo_Situ_Permitidas', 'Mod_Doc_Fisc_Permitido', 'Situacao_Sincronizacao')

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
