from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def apurador_required(view_func):
    """
    LGPD - Princípio da Segurança (Art. 6º, VII e Art. 46):
    restringe o acesso aos dados das denúncias apenas a usuários autenticados
    e autorizados no grupo 'Apurador' (controle de acesso baseado em papel).
    """

    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='Apurador').exists():
            raise PermissionDenied('Acesso restrito a membros do grupo Apurador.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
