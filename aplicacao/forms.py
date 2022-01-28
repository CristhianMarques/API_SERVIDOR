from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column,HTML

from .models import Parametros_Gerais, Contato_Empresa, Chamado_Evento

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUsuario

import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

class Parametros_GeraisModelForm(forms.ModelForm):
    
    class Meta:
        model = Parametros_Gerais
        fields = ['Tempo_Avisos_Minutos', 'Tipo_Situ_Permitidas', 'Mod_Doc_Fisc_Permitido', 'Situacao_Sincronizacao']

class Contato_EmpresaModelForm(forms.ModelForm):
    
    class Meta:
        model = Contato_Empresa
        fields = ['Nome', 'Funcao', 'Telefone', 'Celular', 'Observacao',]

class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')
        labels = {'username': 'Username'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class Chamado_EventoForm(forms.ModelForm):
    class Meta:
        model = Chamado_Evento
        fields = ('fk_Evento', 'Atendente', 'Situacao_Evento', 'Data_Retorno', 'Observacao')

class Chamado_EventoFormV2(forms.ModelForm):
    id           = forms.CharField(widget = forms.HiddenInput(), required = False)
    Data_Retorno = forms.DateField(initial=datetime.date.today)
    class Meta:
        model = Chamado_Evento
        fields = ('id', 'Atendente', 'Situacao_Evento', 'Data_Retorno', 'Observacao')
        widgets = {
        'Data_Retorno': forms.DateInput(format=('%m/%d/%Y')),
    }

class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')


class EventoFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        Row(
            Div('id', css_class='col-sm-2'), Div('Data_Criacao_Evento', css_class='col-sm-3'), Div('Empresa_Orig', css_class='col-sm-3'), Div('status', css_class='col-sm-2'),
            Div(
                Submit('submit', 'Filtrar'), style=" padding-top: 32px; padding-left: 20px;"
            ),
            
        ),
        
        
    )


        