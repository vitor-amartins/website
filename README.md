# Deploy de um app Django com Dokku no Digital Ocean

## Da criação do projeto Django até o deploy no Digital Ocean

#### O que você precisa antes de começar?

- Estar num ambiente virtual com o Django instalado
- Um droplet do Dokku no Digital Ocean

----

#### Preparado, jovem Padawan? Mãos à obra:

1. Crie o projeto Django

1. Na pasta que está o arquivo `settings.py`, crie uma pasta com o nome de _settings_

1. Renomeie o arquivo `settings.py` para `base.py` e coloque-o dentro da pasta _settings_

1. Dentro da pasta _settings_ crie dois arquivos: `develop.py` e `production.py` e importe tudo do arquivo `base.py` neles:

    `from .base import *`

1. Remova as seguintes variáveis do `base.py` e coloque-as no `develop.py`

    - SECRET_KEY
    - DEBUG
    - ALLOWED_HOSTS
    - DATABASES

1. No ```base.py``` defina o caminho para os arquivos estáticos e configure o _whitenoise_:

    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
    ```

    > Repare que como o descemos o diretório do arquivo em um nível, devemos retornar ao nível superior a partir de BASE_DIR

    ```python
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    ```

    - Na variável `MIDDLEWARE`:
        - Mova `'django.middleware.security.SecurityMiddleware',` para ser o primeiro item da lista
        - Adicione `'whitenoise.middleware.WhiteNoiseMiddleware',` em seguida

1. Instale as dependências do nosso projeto:
    > Você pode ignorar esse passo se no próximo você listar manualmente cada dependência. Se atente às versões de cada uma caso faça dessa forma.

    `pip install dj-database-url psycopg2 whitenoise gunicorn`

    - **dj-database-url:** Fará a conexão do banco do Dokku com a aplicação Django
    - **psycopg2:** Dependência para utilizar o PostgreSQL
    - **whitenoise:** Necessário para servir os arquivos estáticos
    - **gunicorn:** Ele que vai executar a aplicação no ambiente de produção

1. Crie o arquivo `requirements.txt` com a lista de dependências:

    `pip freeze > requirements.txt`

1. Configure o arquivo `production.py` da seguinte forma:

    ```python
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

    SECRET_KEY = os.environ['SECRET_KEY']

    ALLOWED_HOSTS = []
    ```

    > Em ALLOWED_HOSTS coloque o domínio que apontará para sua instância do Digital Ocean (adicionalmente, pode-se colocar também o IP da instância)

    > Por motivos de magia negra, mesmo se você definir `DEBUG=False`, ele executará como se estivesse ativado. Portanto, para desativar a opção de DEBUG, basta não inserí-lo no arquivo.

1. No arquivo `wsgi.py`, onde está a linha:
    > Aqui utilizo _"app_name"_ como exemplo, substitua pelo nome do seu projeto.

    ```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_name.settings')
    ```

    coloque o caminho para o arquivo `production.py`:

    ```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_name.settings.production')
    ```

1. Já no arquivo `manage.py`, onde está a linha:

    ```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_name.settings')
    ```

    substitua por:

    ```python
    SETTINGS_MODULE_PATH =  os.environ.get('SETTINGS_MODULE_PATH', 'app_name.settings.develop')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE_PATH)
    ```

1. Agora vamos criar o **Dockerfile**:
    ```dockerfile
    FROM python:3
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /server
    WORKDIR /server
    COPY requirements.txt /server/
    RUN pip install -r requirements.txt
    ENV SETTINGS_MODULE_PATH='app_name.settings.production'

    COPY . /server/
    CMD ["gunicorn", "app_name.wsgi"]
    ```

> Dessa forma, quando executarmos o projeto com o gunicorn, ele utilizará o wsgi.py, que referencia o arquivo de produção (production.py), e para o manage.py, nós definiremos uma variável de ambiente no Dokku para utilizar o production.py, enquanto que executando localmente com `python manage.py runserver` será utilizado o arquivo develop.py.

### Por aqui tá tudo certo, vamos agora preparar nossa instância

1. Acesse o IP da instância pelo navegador, você verá a tela de configuração inicial do Dokku. Substituia o hostname pelo ip da sua instância e clique em **Finish Setup**.

1. Acesse a instância utilizando SSH:

    ```bash
    ssh <ip_da_instancia> -l root
    ```

1. Instale o plugin do Postgres:

    ```bash
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    ```

1. Instale o plugin do Letsencrypt:

    ```bash
    sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
    ```

1. Crie o app:

    ```bash
    dokku apps:create app_name
    ```

1. Crie o banco:

    ```bash
    dokku postgres:create app_name-db
    ```

1. Faça a ligação entre o banco e o app:

    ```bash
    dokku postgres:link app_name-db app_name
    ```

1. Adicione as variáveis de ambiente do seu projeto Django:

    ```bash
    dokku config:set app_name SECRET_KEY='coloque_sua_secret_key_aqui'
    ```

### Vamos voltar à sua máquina agora, pois chegou a hora de dar push para o Dokku

1. Coloque seus poderes de git em ação:

    ```bash
    git init
    git remote add dokku dokku@<ip_da_instancia>:<app_name>
    git add .
    git commit -m "My first deploy on Dokku"
    git push dokku master
    ```
### Retornando à nossa instância, vamos aos procedimentos finais:

1. Aplique as migrações:

    ```bash
    dokku run app_name python manage.py migrate
    ```

1. Crie o superusuário:

    ```bash
    dokku run app_name python manage.py createsuperuser
    ```

1. Conecte o armazenamento persistente do Dokuu com o Django:

    ```bash
    dokku storage:mount app_name /var/lib/dokku/data/storage:/server/static
    ```

1. Configurar os arquivos estáticos:

    ```bash
    dokku run app_name python manage.py collectstatic
    ```

### Estamos quase lá, pra deixar tudo TOP, vamos configurar o HTTPS:

1. Adicione seu domínio:

    ```bash
    dokku domains:add app-name <seu_dominio.com.br> www.<seu_dominio.com.br>
    ```

1. Adicione um proxy:

    ```bash
    dokku proxy:ports-add app-name http:80:5555
    ```

    > É necessário para que o LetsEncrypt consiga se conectar com o app Dokku

1. Configure um email para o LetsEncrypt:

    ```bash
    dokku config:set --no-restart app-name DOKKU_LETSENCRYPT_EMAIL=<seu@email.com>
    ```

    >  Será usado para te notificar quando o certificado estiver perto da validade

1. Adicione o certificado HTTPS:

    ```bash
    dokku letsencrypt app_name
    ```

1. Para o certificado renovar automaticamente:

    ```bash
    dokku letsencrypt:cron-job --add
    ```

    ```bash
    dokku letsencrypt:auto-renew
    ```
### Parabéns! Você acaba de completar o Deploy e se tornar um Guerreiro Jedi.
