1. Instale o plugin do Postgres:
    ```sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git```
1. Instale o plugin do Letsencrypt
    ```sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git```
1. Crie o app:
    ```dokku apps:create app-name```
1. Crie o banco:
    ```dokku postgres:create app-name-db```
1. Faça a ligação entre o banco e o app:
    ```dokku postgres:link app-name-db app-name```
1. Adicione a SECRET_KEY do seu projeto Django:
    ```dokku config:set app-name SECRET_KEY='coloque_sua_secret_key_aqui'```
1. **Faça deploy da sua aplicação antes de continuar!**
1. Aplique as migrações:
    ```dokku run app-name python manage.py migrate```
1. Crie o superusuário:
    ```dokku run app-name python manage.py createsuperuser```
1. Adicione seu domínio:
    ```dokku domains:add app-name vitormartins.dev```
    ```dokku domains:add app-name www.vitormartins.dev```
1. Adicione um proxy (para o letsencrypt):
    ```dokku proxy:ports-add app-name http:80:5555```
1. Configure um email para o letsencrypt (será usado para te notificar quando o certificado estiver perto da validade):
    ```dokku config:set --no-restart app-name DOKKU_LETSENCRYPT_EMAIL=seu@email.com```
1. Adicione o certificado HTTPS:
    ```dokku letsencrypt app-name```
1. Para o certificado renovar automaticamente:
    ```dokku letsencrypt:cron-job --add```
    ```dokku letsencrypt:auto-renew```
1. Configurar os arquivos estáticos:
    ```dokku run app-name python manage.py collectstatic```
1. Conecte o armazenamento persistente do Dokuu com o Django:
    ```dokku storage:mount app-name /var/lib/dokku/data/storage:/vitor/static```
