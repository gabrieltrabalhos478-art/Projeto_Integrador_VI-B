from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def apurador_required(view_func):
    """Restringe o acesso apenas a usuários autenticados do grupo 'Apurador'."""

    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='Apurador').exists():
            raise PermissionDenied('Acesso restrito a membros do grupo Apurador.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
