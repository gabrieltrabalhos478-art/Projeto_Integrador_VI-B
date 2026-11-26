import secrets
import string
from django.db import models


def gerar_protocolo():
    """Gera um código de protocolo único e aleatório no formato DS-XXXXXXXX."""
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(secrets.choice(caracteres) for _ in range(8))
    return f'DS-{codigo}'


class Denuncia(models.Model):
    """Representa uma denúncia de incidente ou prática insegura envolvendo dados."""

    CATEGORIA_CHOICES = [
        ('vazamento', 'Vazamento de dados'),
        ('pratica_inadequada', 'Prática inadequada de segurança'),
        ('atividade_suspeita', 'Atividade suspeita'),
    ]

    STATUS_CHOICES = [
        ('recebida', 'Recebida'),
        ('em_analise', 'Em análise'),
        ('concluida', 'Concluída'),
    ]

    protocolo = models.CharField(
        'Protocolo',
        max_length=20,
        unique=True,
        editable=False,
    )
    categoria = models.CharField(
        'Categoria',
        max_length=30,
        choices=CATEGORIA_CHOICES,
    )
    empresa_envolvida = models.CharField(
        'Empresa envolvida',
        max_length=150,
    )
    data_aproximada = models.DateField(
        'Data aproximada do ocorrido',
    )
    descricao = models.TextField(
        'Descrição do ocorrido',
    )
    # Campo opcional para permitir denúncias 100% anônimas
    contato_denunciante = models.CharField(
        'Contato do denunciante (opcional)',
        max_length=255,
        blank=True,
        default='',
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='recebida',
    )
    criado_em = models.DateTimeField(
        'Data de registro',
        auto_now_add=True,
    )
    atualizado_em = models.DateTimeField(
        'Última atualização',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        # Garante que toda denúncia receba um protocolo único antes de salvar
        if not self.protocolo:
            novo_protocolo = gerar_protocolo()
            while Denuncia.objects.filter(protocolo=novo_protocolo).exists():
                novo_protocolo = gerar_protocolo()
            self.protocolo = novo_protocolo
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.protocolo} - {self.get_categoria_display()}'
