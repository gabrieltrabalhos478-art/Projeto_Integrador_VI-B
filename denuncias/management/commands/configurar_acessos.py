import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cria o grupo Apurador e, opcionalmente, um superusuário de teste via variável de ambiente.'

    def handle(self, *args, **options):
        grupo, criado = Group.objects.get_or_create(name='Apurador')
        if criado:
            self.stdout.write(self.style.SUCCESS('Grupo "Apurador" criado com sucesso.'))
        else:
            self.stdout.write('Grupo "Apurador" já existe.')

        # Nunca armazenar senhas reais no repositório: lê apenas de variável de ambiente
        senha_teste = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin_teste')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@exemplo.local')

        User = get_user_model()
        if senha_teste:
            if not User.objects.filter(username=username).exists():
                usuario = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=senha_teste,
                )
                usuario.groups.add(grupo)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Superusuário "{username}" criado e adicionado ao grupo "Apurador".'
                    )
                )
            else:
                self.stdout.write(f'Usuário "{username}" já existe.')
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Variável DJANGO_SUPERUSER_PASSWORD não definida. '
                    'Use "python manage.py createsuperuser" para criar o usuário manualmente '
                    'e adicione-o ao grupo "Apurador" no /admin/.'
                )
            )
