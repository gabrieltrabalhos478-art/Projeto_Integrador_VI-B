from django.contrib import admin
from .models import Denuncia


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'categoria', 'empresa_envolvida', 'status', 'criado_em')
    list_filter = ('status', 'categoria')
    search_fields = ('protocolo', 'empresa_envolvida')
    readonly_fields = ('protocolo', 'criado_em', 'atualizado_em')
