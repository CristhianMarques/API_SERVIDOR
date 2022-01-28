from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


class Contato_Empresa(models.Model):
    Nome     = models.CharField(max_length=250, verbose_name='Nome Contato')
    Funcao   = models.CharField(max_length=250, verbose_name='Função Contato', blank=True, null=True)
    Telefone = models.CharField(max_length=20, verbose_name='Telefone', blank=True, null=True)
    Celular  = models.CharField(max_length=20, verbose_name='Celular', blank=True, null=True)
    Observacao = models.CharField(max_length=250, verbose_name='Observação', blank=True, null=True)

    class Meta:
        verbose_name = 'Contato_Empresa'
        verbose_name_plural = 'Contatos Empresa'

    def __str__(self):
        return self.Nome

class Evento_Sincronizado(models.Model):

    DOC_NFE  = 'NFE'
    DOC_NFCE = 'NFCE'

    TIPO_DOC = (
        (DOC_NFE, 'NFE'),
        (DOC_NFCE,'NFCE'),
    )

    ENVIADA     = 'Enviada'
    PENDENTE    = 'Pendente'
    CONTIGENCIA = 'Contigencia'
    ERRO        = 'Erro'
    TODAS       = 'Todas'

    SIM = 'Sim'
    NAO = 'Nao'

    SITUACAO = (
        (SIM, 'Sim'),
        (NAO,'Nao'),
    )

    SITUACAO_DOC = (
        (ENVIADA, 'Enviada'),
        (PENDENTE,'Pendente'),
        (CONTIGENCIA,'Contigencia'),
        (ERRO,'Erro'),
    )

    Data_Criacao_Evento = models.DateField(verbose_name='Data Criação Evento', blank=True, null=True)
    Tipo_Doc_Fiscal     = models.CharField(max_length=50, verbose_name='Tipo Doc', choices=TIPO_DOC, blank=True, null=True)
    Data_Emissao        = models.DateField(verbose_name='Data Emissão', blank=True, null=True)
    Num_Doc             = models.CharField(max_length=50, verbose_name='Numero Doc', blank=True, null=True)
    Serie_Dov           = models.CharField(max_length=50, verbose_name='Serie Doc', blank=True, null=True)
    Status_Doc          = models.CharField(max_length=50, verbose_name='Status Doc', choices=SITUACAO_DOC, blank=True, null=True)
    Id_Tab_Orig           = models.CharField(max_length=50, verbose_name='Id Tabela Origem', blank=True, null=True)
    Registro_Sincronizado = models.CharField(max_length=50, verbose_name='Registro Sincronizado', choices=SITUACAO, blank=True, null=True)
    Empresa_Orig          = models.CharField(max_length=150, verbose_name='Empresa', blank=True, null=True)
    Contato_Orig          = models.CharField(max_length=250, verbose_name='Nome Contato') 
    Telefone_Orig         = models.CharField(max_length=20, verbose_name='Telefone', blank=True, null=True)
    Celular_Orig          = models.CharField(max_length=20, verbose_name='Celular', blank=True, null=True)

    class Meta:
        verbose_name = 'Evento_Sincronizado'
        verbose_name_plural = 'Eventos_Sincronizados'
    
    def __str__(self):
        return str(self.id)

class Chamado_Evento(models.Model):

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

    fk_Evento       = models.ForeignKey(Evento_Sincronizado, models.PROTECT, related_name='fK_Evento_Sincronizado',  verbose_name='Evento')
    Atendente       = models.CharField(max_length=250, verbose_name='Nome Atendente', blank=False, null=False)
    Situacao_Evento =  models.CharField(max_length=250, verbose_name='Situação do Evento' , choices=SITUACAO, blank=False, null=False)
    Data_Retorno    = models.DateField(verbose_name='Data Contato', blank=True, null=True)
    Observacao      = models.CharField(max_length=250, verbose_name='Observação', blank=False, null=False)


    class Meta:
        verbose_name = 'Chamado_Evento'
        verbose_name_plural = 'Chamado_Eventos'

    def __str__(self):
        return self.Atendente

class Parametros_Gerais(models.Model):

    ENVIADA     = 'Enviada'
    PENDENTE    = 'Pendente'
    CONTIGENCIA = 'Contigencia'
    ERRO        = 'Erro'
    TODAS       = 'Todas'

    NFCE = 'Nfce'
    NFE =  'Nfe'

    ATIVO   = 'Ativo'
    INATIVO = 'Inativo'

    SITUACAO_DOC = (
        (ENVIADA, 'Enviada'),
        (PENDENTE,'Pendente'),
        (CONTIGENCIA,'Contigencia'),
        (ERRO,'Erro'),
        (TODAS,'Todas'),
    )

    DOC_FISCAL = (
        (NFCE, 'Nfce'),
        (NFE, 'Nfe'),
        (TODAS, 'Todas')
    )

    SITUACAO =  (
        (ATIVO, 'Ativo'),
        (INATIVO,'Inativo')
    )


    Tempo_Avisos_Minutos    = models.IntegerField(verbose_name='Tempo de Emissão de Alertas/Aviso de Erros Identificados', blank=False, null=False)
    Tipo_Situ_Permitidas    = models.CharField(max_length=50, verbose_name='Tipo de Sincronização  Permitida (Enviadas, Pendentes, Contigencia, Erro)', choices=SITUACAO_DOC, blank=False, null=False)
    Mod_Doc_Fisc_Permitido  = models.CharField(max_length=50, verbose_name='Modalidade Documento Fiscal (NFe, NFce) Permitidas', choices=DOC_FISCAL, blank=False, null=False)
    Situacao_Sincronizacao  = models.CharField(max_length=50, verbose_name='Situação - Sincronização dos Dados', choices=SITUACAO, blank=False, null=False)

    class Meta:
        verbose_name = 'Parametros_Gerais'
        verbose_name_plural = 'Parametros_Gerais'

class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(username, email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    username = models.CharField('Nome usuario', max_length=60, unique=True)
    email = models.EmailField('E-mail')
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name', 'last_name', 'fone']

    def __str__(self):
        return self.email

    objects = UsuarioManager()
