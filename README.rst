cotton-digitalocean
===================

digitalocean provider for cotton

example cotton.yaml:

    provider_zones:
      digitalocean_dev:
        driver: cotton_digitalocean.Driver
        client_id: your_client_id
        api_key: your_api_key
        region_id: 2
        image_id: 473123
        size_id: 66
        backup_active: False
        ssh_key_ids: 107222
        provisioning_ssh_key: ~/.ssh/id_rsa
        provisioning_user: root
        private_networking: False


TODO
====
- allow to use textual names instead of ids only
- ensure that PR https://github.com/koalalorenzo/python-digitalocean/pull/28 gets merged
