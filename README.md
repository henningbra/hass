apt install docker-compose


# Certbot
`
    # Init command:     
    $ docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org
    
    # Renwew command: 
    $ docker-compose run --rm certbot renew

    # Backup files
    $  sudo zip -r haas_config_backup.zip .storage/ .cloud/ secrets.yaml

# Testing code in appdaemon

    # sudo docker-compose exec appdaemon sh
    # cd /conf
    # pytest
