from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .crypto import criptografar_texto, descriptografar_texto
from .decorators import apurador_required
from .forms import AlterarStatusForm, ConsultaProtocoloForm, DenunciaForm
from .models import Denuncia, LogAcesso


def nova_denuncia(request):
    """Página pública inicial com formulário de denúncia e aviso de consentimento."""
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            # Criptografa campos sensíveis em repouso antes de persistir no banco
            denuncia.descricao = criptografar_texto(denuncia.descricao)
            denuncia.contato_denunciante = criptografar_texto(denuncia.contato_denunciante)
            denuncia.save()
            return redirect('confirmacao_denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm()

    return render(request, 'denuncias/nova_denuncia.html', {'form': form})


def confirmacao_denuncia(request, protocolo):
    """Tela de confirmação exibindo o protocolo gerado para acompanhamento."""
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    return render(request, 'denuncias/confirmacao.html', {'protocolo': denuncia.protocolo})


def consultar_status(request):
    """Consulta pública de status usando apenas o protocolo (sem expor conteúdo)."""
    resultado = None
    nao_encontrado = False

    if request.method == 'POST':
        form = ConsultaProtocoloForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['protocolo'].strip().upper()
            denuncia = Denuncia.objects.filter(protocolo=codigo).first()
            if denuncia:
                # Retorna apenas metadados de andamento, sem descrição, empresa ou contato
                resultado = {
                    'protocolo': denuncia.protocolo,
                    'status_display': denuncia.get_status_display(),
                    'status_code': denuncia.status,
                    'criado_em': denuncia.criado_em,
                    'atualizado_em': denuncia.atualizado_em,
                }
            else:
                nao_encontrado = True
    else:
        form = ConsultaProtocoloForm()

    return render(
        request,
        'denuncias/consultar_status.html',
        {
            'form': form,
            'resultado': resultado,
            'nao_encontrado': nao_encontrado,
        },
    )


@apurador_required
def lista_denuncias(request):
    """Lista de denúncias para o apurador autenticado."""
    status_filtro = request.GET.get('status', '')
    denuncias = Denuncia.objects.all()
    if status_filtro:
        denuncias = denuncias.filter(status=status_filtro)

    return render(
        request,
        'denuncias/lista_denuncias.html',
        {
            'denuncias': denuncias,
            'status_filtro': status_filtro,
            'status_choices': Denuncia.STATUS_CHOICES,
        },
    )


@apurador_required
def detalhe_denuncia(request, pk):
    """Página de detalhe da denúncia com alteração de status pelo apurador."""
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if request.method == 'POST':
        form = AlterarStatusForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            LogAcesso.objects.create(
                usuario=request.user,
                denuncia=denuncia,
                acao='alteracao_status',
                detalhe=f'Status alterado para {denuncia.get_status_display()}',
            )
            messages.success(request, f'Status da denúncia {denuncia.protocolo} atualizado.')
            return redirect('detalhe_denuncia', pk=denuncia.pk)
    else:
        form = AlterarStatusForm(instance=denuncia)
        LogAcesso.objects.create(
            usuario=request.user,
            denuncia=denuncia,
            acao='visualizacao',
        )

    # Descriptografa descrição e contato apenas na exibição para o apurador autorizado
    descricao_clara = descriptografar_texto(denuncia.descricao)
    contato_claro = descriptografar_texto(denuncia.contato_denunciante)

    return render(
        request,
        'denuncias/detalhe_denuncia.html',
        {
            'denuncia': denuncia,
            'form': form,
            'descricao_clara': descricao_clara,
            'contato_claro': contato_claro,
        },
    )


@login_required
def logs_auditoria(request):
    """Tela de consulta da trilha de auditoria restrita ao administrador."""
    if not request.user.is_superuser:
        raise PermissionDenied('Acesso restrito ao administrador do sistema.')

    logs = LogAcesso.objects.select_related('usuario', 'denuncia').all()
    return render(request, 'denuncias/logs_auditoria.html', {'logs': logs})
