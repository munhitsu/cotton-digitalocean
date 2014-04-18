cotton-digitalocean
===================

digitalocean provider for cotton

example cotton.yaml:: 

    provider_zones:
      digitalocean_dev:
        driver: cotton_digitalocean.Driver
        client_id: your_client_id
        api_key: your_api_key
        region_id: 2
        image_id: 473123
        size_id: 66
        backup_active: False
        ssh_key_ids:
         - your_ssh_key_id
        provisioning_ssh_key: ~/.ssh/id_rsa
        provisioning_user: root
        private_networking: False



You can also use slug names instead of ids::

        region_slug: ams1
        image_slug: ubuntu-12-04-x64
        size_slug: 512mb


To list all options execute task `options`::

    from cotton_digitalocean.tasks import options
