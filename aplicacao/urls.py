from django.urls import path

from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('parametro/', views.parametro, name='parametro'),
    path('contato/', views.contato, name='contato'),
    path('chamado/', views.Chamado, name='chamado'),
    path('simplificado/', views.simplificado, name='simplificado'),
    path('detalhado/', views.paineldr, name='detalhado'),
    path('painel/', views.ModelNameView.as_view(), name='painel'),
    path('atendchamado/<int:pkchamado>', views.datalhechamado, name='atendchamado'),
 
]
