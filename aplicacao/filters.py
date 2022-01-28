from django import forms
from django.utils import six
from django.db.models import Q

import django_filters

from .models import Evento_Sincronizado, Chamado_Evento




###############################################################################

class FormularioFiltro(forms.Form):

    pesquisar = forms.CharField(required=False)

###############################################################################

class FiltroOpcoes:
    def __init__(self, opcoes = None):
        self.fields = getattr(opcoes, 'fields', None)

###############################################################################

class FiltroMetaclasse(type):
    def __new__(cls, name, bases, attrs):
        attrs['filtro'] = ''

        new_class = super(FiltroMetaclasse, cls).__new__(cls, name, bases, attrs)
        new_class._meta = FiltroOpcoes(getattr(new_class, 'Meta', None))

        return new_class

###############################################################################

class FiltroBase:

    def __init__(self, dados, queryset):
        #assert(queryset)

        self.dados = dados or {}
        self.queryset = queryset
    
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            if self.form.is_valid():
                termo_pesquisa = self.form.cleaned_data['pesquisar']
                if not termo_pesquisa:
                    termo_pesquisa = self.dados.get('query[pesquisar]', '')

                filtro = Q()
                for field in self.get_fields():
                    field_name = '%s__icontains' % field                    
                    filtro = filtro | Q(**{field_name: termo_pesquisa})

                self._qs = self.queryset.filter(filtro)
            else:
                self._qs = self.queryset.all()

        return self._qs

    @classmethod
    def get_fields(cls):
        return cls._meta.fields

    @property
    def form(self):
        if not hasattr(self, '_form'):
            self._form = FormularioFiltro(self.dados)

        return self._form
            
###############################################################################

class Filtro(six.with_metaclass(FiltroMetaclasse, FiltroBase)):
    pass

###############################################################################

class Evento_SincronizadoFilter(django_filters.FilterSet):

    ENVIADA     = 'Enviada'
    PENDENTE    = 'Pendente'
    CONTIGENCIA = 'Contigencia'
    ERRO        = 'Erro'
    TODAS       = 'Todas'

    SITUACAO_DOC = (
        (ENVIADA, 'Enviada'),
        (PENDENTE, 'Pendente'),
        (CONTIGENCIA, 'Contigencia'),
        (ERRO, 'Erro'),
    )
    
    Data_Criacao_Evento = django_filters.DateFilter(field_name='Data_Criacao_Evento', widget=forms.DateInput(attrs={'class': 'col-sm'}))
    id                  = django_filters.NumberFilter(field_name='id', widget=forms.NumberInput(attrs={'class': 'col-sm'}))
    Empresa_Orig        = django_filters.CharFilter(field_name='Empresa_Orig', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'col-sm'}))
    status              = django_filters.ChoiceFilter(field_name='Status_Doc', choices=SITUACAO_DOC)
    class Meta:
        model = Evento_Sincronizado
        fields = ['Data_Criacao_Evento','id', 'Empresa_Orig','status']

class Evento_SincronizadoFilter1(django_filters.FilterSet):

    ENVIADA     = 'Enviada'
    PENDENTE    = 'Pendente'
    CONTIGENCIA = 'Contigencia'
    ERRO        = 'Erro'
    TODAS       = 'Todas'

    SITUACAO_DOC = (
        (ENVIADA, 'Enviada'),
        (PENDENTE, 'Pendente'),
        (CONTIGENCIA, 'Contigencia'),
        (ERRO, 'Erro'),
    )
    
    
    status              = django_filters.CharFilter(field_name='Status_Doc', initial='Erro', lookup_expr='iexact')

   
    class Meta:
        model = Evento_Sincronizado
        fields = ['status']

        

class Chamado_EventoFilter(django_filters.FilterSet):

    SOLUCIONADO = 'Solucionado'
    PENDENTE    = 'Pendente'
    NAO_IDENTIFICADO = 'Não Identificado'
    SEM_CONTATO   = 'Empresa - Falha no Contato'
    FALHA_CONTATO   = 'Empresa - Retornar Contato'

    SITUACAO = (
        (SOLUCIONADO, 'Solucionado'),
        (PENDENTE,  'Pendente'),
        (NAO_IDENTIFICADO,  'Não Identificado'),
        (SEM_CONTATO,  'Empresa - Falha no Contato'),
        (FALHA_CONTATO,  'Empresa - Retornar Contato'),
    )

    Atendente       = django_filters.CharFilter(field_name='Atendente', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'col-sm'}))
    Situacao_Evento = django_filters.ChoiceFilter(field_name='Situação do Evento', choices=SITUACAO)
    Data_Retorno    = django_filters.DateFilter(field_name='Data Contato', widget=forms.DateInput(attrs={'class': 'col-sm'}))

    
    
    class Meta:
        model = Chamado_Evento
        fields = ['Atendente','Situacao_Evento', 'Data_Retorno']