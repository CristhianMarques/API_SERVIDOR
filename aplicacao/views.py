import sweetify
from django.shortcuts import render, redirect
from django.contrib import messages

from django.db import connections

from django.views import generic
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django_tables2.views import RequestConfig
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from django_tables2 import RequestConfig

from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.template import loader

from .forms import Chamado_EventoForm, Chamado_EventoFormV2, Parametros_GeraisModelForm, Contato_EmpresaModelForm, EventoFilterFormHelper
from .models import Parametros_Gerais, Contato_Empresa, Evento_Sincronizado, Chamado_Evento
from aplicacao.tables import Evento_SincronizadoTable, Evento_SincronizadoTableV1, Chamado_EventoTable
from aplicacao import tablesconfigure

from django_tables2 import RequestConfig

from aplicacao.filters import Evento_SincronizadoFilter, Chamado_EventoFilter, Evento_SincronizadoFilter1

from django_tables2 import SingleTableView

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


from datetime import date
# Create your views here.


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(PagedFilteredTableView, self).get_table()
        RequestConfig(self.request, paginate={'page': self.kwargs['page'],
                            "per_page": self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


@login_required
def index(request):
    
    return render(request, 'base.html')

@login_required(login_url='login')
def datalhechamado(request, pkchamado):
    
    dados_eventos  = []

    dados_chamados = []

    if str(request.user) != 'AnonymousUser':

        try:
            objevento = Evento_Sincronizado.objects.filter(id=pkchamado)
        except Evento_Sincronizado.DoesNotExist:
            objevento = None
        
        print('re', objevento)
        
        try:
            objlistchamado = Chamado_Evento.objects.filter(fk_Evento=pkchamado)
        except Chamado_Evento.DoesNotExist:
            objlistchamado = None

        filtro = Chamado_EventoFilter(request.GET, objlistchamado)
        table  = Chamado_EventoTable(filtro.qs)

        table.paginate(page=request.GET.get("page", 1), per_page=25)


        chamado = None

        if request.method == 'POST':
            print('gerra' )
            form = Chamado_EventoFormV2(request.POST, instance=chamado)
            form.instance.fk_Evento = objevento[0]
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
                try:
                    objlistchamado = Chamado_Evento.objects.filter(fk_Evento=pkchamado)
                except Chamado_Evento.DoesNotExist:
                    objlistchamado = None

                filtro = Chamado_EventoFilter(request.GET, objlistchamado)
                table  = Chamado_EventoTable(filtro.qs)

                table.paginate(page=request.GET.get("page", 1), per_page=25)

            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Chamado_EventoFormV2(instance=chamado)
            
        context = {
            'form': form,
            'objevento': objevento,
            'table': table,
            'pkchamado': pkchamado
        }

        #print(objevento[0].Empresa_Orig)

        #print(context)
        
        return render(request, 'datalhechamado.html', context)
    else:
        return redirect('index')
    

@login_required
def simplificado(request):

    dados_array = []

    query = """
                    SELECT 
	
                        SUM(
                            CASE 
        	                    WHEN UPPER(Status_Doc) = UPPER('Enviada') THEN 1
                            ELSE 0 END ) AS ENVIADAS,
    
                        SUM(
                            CASE 
    	                        WHEN UPPER(Status_Doc) = UPPER('Erro') THEN 1
                            ELSE 0 END ) AS ERRO,
    
                        SUM(
                            CASE 
    	                        WHEN UPPER(Status_Doc) = UPPER('Contigencia') THEN 1
                            ELSE 0 END ) AS CONTIGENCIA,
    
                        SUM(
                            CASE 
    	                        WHEN UPPER(Status_Doc) = UPPER('PENDENTE') THEN 1
                            ELSE 0 END ) AS PENDENTE
    
                    FROM aplicacao_evento_sincronizado WHERE 1 = 1
            """
    
    with connections['default'].cursor() as cursor:

        cursor.execute(query, [])

        for lista in cursor.fetchall():

            dados_array.append({
                'erros': lista[1],
                'enviadas': lista[0],
                'contigencia': lista[2],
                'pendente': lista[3]
            })
            
    context  = {'dados': dados_array}

    return render(request, 'monitoramento_simplificado.html', context)

@login_required(login_url='login')
def error404(request, ex):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/thml; charset=utf8', status=404)

@login_required(login_url='login')
def error500(request):
    print('er')
    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=500)
    

@login_required
def paineldr(request):

    queryset = Evento_Sincronizado.objects.filter(Status_Doc='Erro').order_by('-id')

    filtro = Evento_SincronizadoFilter(request.GET, queryset)
    table = Evento_SincronizadoTable(filtro.qs)

    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {
        'table': table
    }
    
    return render(request, 'monitoramento_detalhado.html', {'table': table})

@login_required
def parametro(request):
    if str(request.user) != 'AnonymousUser':

        try:
            parametro_instance = Parametros_Gerais.objects.get(id=1)
        except Parametros_Gerais.DoesNotExist:
            parametro_instance = None

        if request.method == 'POST':
            form = Parametros_GeraisModelForm(request.POST, instance=parametro_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Parametros_GeraisModelForm(instance=parametro_instance)
        
        context = {
            'form': form
        }
        
        return render(request, 'parametro_gerais.html', context)
    else:
        return redirect('index')

@login_required(login_url='login')
def Chamado(request):
    if str(request.user) != 'AnonymousUser':

        try:
            chamado = Chamado_Evento.objects.get(id=1)
        except Chamado_Evento.DoesNotExist:
            chamado = None

        if request.method == 'POST':
            form = Chamado_EventoForm(request.POST, instance=chamado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Chamado_EventoForm(instance=chamado)
        
        context = {
            'form': form
        }
        
        return render(request, 'chamado.html', context)
    else:
        return redirect('index')

@login_required(login_url='login')
def contato(request):
    if str(request.user) != 'AnonymousUser':
        
        try:
            contato_instance = Contato_Empresa.objects.get(id=1)
        except Contato_Empresa.DoesNotExist:
            contato_instance = None

        print('eu')
        if request.method == 'POST':
            form = Contato_EmpresaModelForm(request.POST, instance=contato_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Contato_EmpresaModelForm(instance=contato_instance)
        
        context = {
            'form': form
        }
        
        return render(request, 'contato_empresa.html', context)
    else:
        return redirect('index')


class FilteredSingleTableView(SingleTableMixin, FilterView):
    formhelper_class = None

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset


class ModelNameView(LoginRequiredMixin,FilteredSingleTableView):
    #print('teste')
    
    template_name = 'painel.html'
    table_class = Evento_SincronizadoTableV1
    paginate_by = 25
    filterset_class = Evento_SincronizadoFilter
    formhelper_class = EventoFilterFormHelper

class ModelNameDetalhadoView(LoginRequiredMixin,FilteredSingleTableView):
    #print('teste')
    
    template_name = 'monitoramento_detalhado.html'
    table_class = Evento_SincronizadoTableV1
    print(dir(table_class))
    paginate_by = 25
    filterset_class = Evento_SincronizadoFilter1
    
    print(dir(filterset_class))
    formhelper_class = EventoFilterFormHelper
    print(dir(formhelper_class))


    #try:
    #    objlistchamado = Evento_Sincronizado.objects.filter(Status_Doc='Erro')
    #except Evento_Sincronizado.DoesNotExist:
    #    objlistchamado = None

    #print(objlistchamado)
    

    

    #https://www.treinaweb.com.br/blog/consumindo-apis-com-python-parte-2
    #https://docs.python-requests.org/en/master/

	#https://stackoverflow.com/questions/34774138/reload-table-data-in-django-without-refreshing-the-page/34775420
	#https://stackoverflow.com/questions/35975511/how-to-auto-refresh-redirect-a-view-in-django
	#https://github.com/tjwalch/django-livereload-server