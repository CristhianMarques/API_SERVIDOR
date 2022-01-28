import django_tables2 as tables
from django_tables2.utils import A

from django_tables2 import Column, Table

from aplicacao.models import Evento_Sincronizado, Chamado_Evento



class Evento_SincronizadoTable(tables.Table):

    #id = tbl.Column(verbose_name='id',  orderable=True)
    #Data_Criacao_Evento = tables.Column() #tbl.Column(verbose_name='Data Criacao Evento')

    class Meta:
        model = Evento_Sincronizado
        #exclude = ('id',)
        #sequence = ('Data_Criacao_Evento')
        #fields = ('id', 'Data_Criacao_Evento')
        attrs = {'class': 'table table-sm', 'id': 'idtablepainel'}
        template_name = "bootstrap4-custom.html"


class Chamado_EventoTable(tables.Table):

    #id = tbl.Column(verbose_name='id',  orderable=True)
    #Data_Criacao_Evento = tables.Column() #tbl.Column(verbose_name='Data Criacao Evento')

    class Meta:
        model = Chamado_Evento
        #exclude = ('id',)
        #sequence = ('Data_Criacao_Evento')
        #fields = ('id', 'Data_Criacao_Evento')
        template_name = "bootstrap4-custom.html"

class Evento_SincronizadoTableV1(Table):
    id                  = Column(accessor='id', verbose_name='Id')
    Data_Criacao_Evento = Column(accessor='Data_Criacao_Evento', verbose_name='Data Criacao Evento')
    Empresa_Orig        = Column(accessor='Empresa_Orig', verbose_name='Empresa')
    chamado             = tables.TemplateColumn(verbose_name='',template_name='but_chamado_template.html', orderable=False)

    class Meta:
        model = Evento_Sincronizado
        attrs = {'class': 'table table-sm', 'id': 'idtablepainel'}
        exclude = ('Contato_Orig','Telefone_Orig','Celular_Orig','Registro_Sincronizado')
        ordering = ['-id']
        