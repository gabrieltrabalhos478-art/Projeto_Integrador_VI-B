from django.contrib import admin
from .models import Denuncia, LogAcesso


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'categoria', 'empresa_envolvida', 'status', 'criado_em')
    list_filter = ('status', 'categoria')
    search_fields = ('protocolo', 'empresa_envolvida')
    readonly_fields = ('protocolo', 'criado_em', 'atualizado_em')


@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'usuario', 'denuncia', 'acao', 'detalhe')
    list_filter = ('acao', 'data_hora')
    search_fields = ('usuario__username', 'denuncia__protocolo')
    readonly_fields = ('usuario', 'denuncia', 'acao', 'detalhe', 'data_hora')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
