from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _obter_fernet():
    """
    LGPD - Princípio da Segurança e Prevenção (Art. 6º, VII e VIII; Art. 46):
    lê a chave de criptografia de variável de ambiente, evitando segredos no código-fonte.
    """
    chave = settings.FERNET_KEY
    if not chave:
        raise ValueError(
            'FERNET_KEY não configurada. Defina a variável no arquivo .env.'
        )
    return Fernet(chave.encode('utf-8'))


def criptografar_texto(texto):
    """Criptografa um texto em claro usando Fernet (AES-128-CBC + HMAC-SHA256)."""
    if not texto:
        return ''
    fernet = _obter_fernet()
    return fernet.encrypt(texto.encode('utf-8')).decode('utf-8')


def descriptografar_texto(token):
    """Descriptografa um token Fernet apenas quando autorizado para exibição."""
    if not token:
        return ''
    fernet = _obter_fernet()
    try:
        return fernet.decrypt(token.encode('utf-8')).decode('utf-8')
    except InvalidToken:
        return '[Não foi possível descriptografar este conteúdo com a chave atual]'
