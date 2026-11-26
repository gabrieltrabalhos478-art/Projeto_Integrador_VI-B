# DenúnciaSafe — Canal de Denúncias em Conformidade com a LGPD

Sistema web desenvolvido para o **Projeto Integrador VI-B**, voltado ao registro e acompanhamento de denúncias de vazamento de dados, práticas inadequadas de segurança e atividades suspeitas em empresas. O sistema foi projetado para ser, ele próprio, um exemplo prático de conformidade com a **Lei Geral de Proteção de Dados (Lei nº 13.709/2018 — LGPD)**.

## Tecnologias Utilizadas

- **Python 3** e **Django 5**
- **SQLite** (banco de dados local embutido)
- **cryptography (Fernet)** para criptografia simétrica em repouso
- **python-dotenv** para leitura de variáveis de ambiente a partir do `.env`

## Instalação

1. Crie e ative o ambiente virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

3. Configure a chave de criptografia no arquivo `.env` (baseado no `.env.example`):
   ```powershell
   Copy-Item .env.example .env
   python -c "from cryptography.fernet import Fernet; print('FERNET_KEY=' + Fernet.generate_key().decode())"
   ```
   Cole a chave gerada no campo `FERNET_KEY` do arquivo `.env`.

4. Aplique as migrações do banco de dados:
   ```powershell
   python manage.py migrate
   ```

5. Crie o grupo **Apurador** e um superusuário para testes:
   ```powershell
   python manage.py configurar_acessos
   python manage.py createsuperuser
   ```
   > **Dica:** Para automatizar a criação do superusuário de teste sem gravar senhas no repositório, defina `DJANGO_SUPERUSER_PASSWORD` no terminal antes de rodar `python manage.py configurar_acessos`, ou adicione o usuário criado ao grupo `Apurador` pelo `/admin/`.

## Como Rodar

Execute a verificação do projeto e inicie o servidor de desenvolvimento:

```powershell
python manage.py check
python manage.py runserver
```

Acesse no navegador:

- **Nova denúncia (pública):** `http://127.0.0.1:8000/`
- **Consultar protocolo (pública):** `http://127.0.0.1:8000/consultar/`
- **Política de Privacidade (LGPD):** `http://127.0.0.1:8000/privacidade/`
- **Login / Painel do Apurador:** `http://127.0.0.1:8000/login/` e `/painel/`
- **Trilha de Auditoria (Administrador):** `http://127.0.0.1:8000/painel/auditoria/`

## Perfis de Usuário

| Perfil | Autenticação | Permissões no Sistema |
| :--- | :--- | :--- |
| **Denunciante (Público)** | Não requer login | Pode registrar denúncias (de forma anônima ou com contato opcional), ler a Política de Privacidade e consultar apenas o status pelo número de protocolo. |
| **Apurador** | Login obrigatório + grupo `Apurador` | Acessa a lista de denúncias, visualiza detalhes descriptografados e atualiza o status (`Recebida`, `Em análise`, `Concluída`). |
| **Administrador** | Login obrigatório + `is_superuser` | Além das permissões administrativas do `/admin/`, acessa a tela de **Trilha de Auditoria** (`/painel/auditoria/`) com o histórico de visualizações e alterações. |

## Matriz de Conformidade com a LGPD

| Exigência da Lei (LGPD) | Requisito do Sistema | Implementação no Código |
| :--- | :--- | :--- |
| **Finalidade** (Art. 6º, I) e **Consentimento** (Art. 7º, I; Art. 8º) | Informar claramente o objetivo da coleta e obter aceite explícito antes do envio. | Campo obrigatório `consentimento` no `DenunciaForm` (`denuncias/forms.py`) com link direto para a Política de Privacidade (`denuncias/templates/denuncias/nova_denuncia.html`). |
| **Necessidade / Minimização** (Art. 6º, III) | Coletar apenas o essencial, permitindo anonimato total e evitando exposição na consulta pública. | Campo `contato_denunciante` opcional em `Denuncia` (`denuncias/models.py`); view `consultar_status` (`denuncias/views.py`) retorna somente protocolo, status e datas. |
| **Transparência** (Art. 6º, VI) | Explicar em linguagem clara finalidade, minimização, segurança e retenção. | Página dedicada `/privacidade/` (`denuncias/templates/denuncias/politica_privacidade.html`). |
| **Segurança e Prevenção** (Art. 6º, VII e VIII; Art. 46) | Proteger dados sensíveis em repouso e restringir o acesso ao conteúdo. | Criptografia Fernet em `descricao` e `contato_denunciante` (`denuncias/crypto.py`) com chave em `.env`; descriptografia apenas em `detalhe_denuncia` protegida pelo decorator `@apurador_required` (`denuncias/decorators.py`). |
| **Responsabilização e Prestação de Contas** (Art. 6º, X) | Registrar quem acessou ou alterou cada denúncia e quando. | Model `LogAcesso` (`denuncias/models.py`) gravado automaticamente em `detalhe_denuncia` e exibido na tela `/painel/auditoria/` para o administrador. |
