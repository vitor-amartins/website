## Configurando a instância

1. No bash da instância, execute ```sudo nano dokku-config.sh``` e coloque nele o seguinte código:

    ```bash
    #!/bin/sh

    if [ $# -ne 4 ];
        then echo "Usage:\n    sh dokku-config.sh <appname> <naked domain> <secret_key> <email_for_letsencrypt>"
        exit 1
    fi

    # Install postgres
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    # Install letsencrypt
    sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git

    # Create app
    dokku apps:create $1
    # Created database
    dokku postgres:create $1-db
    # Link database with app
    dokku postgres:link $1-db $1

    # Environmental variables
    dokku config:set $1 SECRET_KEY=$3
    dokku config:set $1 DOKKU_LETSENCRYPT_EMAIL=$4

    # Port for letsencrypt find container
    dokku proxy:ports-add $1 http:80:5555

    read -p "Now push your code to Dokku, wait for it to deploy successfully and press any key here." mainmenuinput

    # Apply migrations
    dokku run $1 python manage.py migrate

    # Add domain
    dokku domains:add $1 $2
    dokku domains:add $1 www.$2

    # HTTPS
    dokku letsencrypt $1
    dokku letsencrypt:cron-job --add
    dokku letsencrypt:auto-renew

    # Static files and storage
    dokku run $1 python manage.py collectstatic
    dokku storage:mount $1 /var/lib/dokku/data/storage:/app/static

    echo "Done! Don't forget to create the superuser! That's all folks!"
    ```

1. Agora o execute passando os 4 parâmetros correspondentes:

    ```bash
    sh dokku-config.sh <appname> <naked domain> <secret_key> <email_for_letsencrypt>
    ```