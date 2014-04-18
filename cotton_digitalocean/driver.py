from __future__ import print_function
import getpass
import time
import datetime
import dateutil.parser
import copy
import pprint
from dop.client import Client, DOPException
from dop.models import Droplet
from fabric.api import abort, env, prompt
from cotton.colors import *
from cotton.provider.driver import Provider
from cotton.config import get_config
from cotton.config import get_provider_zone_config

class DigitalOceanProvider(Provider):

    connection = None

    def __init__(self, client_id=None, api_key=None, **kwargs):
        """
        initializes connection object
        """
        self.connection = Client(client_id, api_key)
        assert self.connection is not None

    def status(self):
        instances = []
        droplets = self.connection.droplets()
        for droplet in droplets:
            instances.append(self.info(droplet))
        return instances

    def create(self, name=None, **kwargs):
        """
        return: aws instance object
        instance is booting so don't forget to cotton.fabextras.wait_for_shell()
        """
        zone_config = get_provider_zone_config()

        result = self.filter(name=name)
        if result:
            abort(red("VM name already in use"))


        size = {}
        fields = ['size_id', 'size_slug']
        for field in fields:
            if field in zone_config:
                size[field] = zone_config[field]

        image = {}
        fields = ['image_id', 'image_slug']
        for field in fields:
            if field in zone_config:
                image[field] = zone_config[field]

        region = {}
        fields = ['region_id', 'region_slug']
        for field in fields:
            if field in zone_config:
                region[field] = zone_config[field]

        droplet = self.connection.create_droplet(
            name=name,
            size=size,
            image=image,
            region=region,
            backups_enabled=zone_config['backup_active'],
            private_networking=zone_config['private_networking'],
            ssh_key_ids=map(lambda x: str(x), zone_config['ssh_key_ids'])
        )

        print("Waiting for instance to run",)
        while droplet.ip_address is None or droplet.status != 'active':
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)
            droplet = self.connection.show_droplet(droplet.droplet_id)
        print(" OK")

        return droplet

    def terminate(self, server):
        assert isinstance(server, Droplet)
        pprint.pprint(self.info(server))

        if env.force:
            sure = 'T'
        else:
            sure = prompt(red("Type 'T' to confirm termination"), default='N')

        if sure == 'T':
            self.connection.rename_droplet(server.droplet_id, '{}-terminating'.format(server.name))
#            time.sleep(1) #TODO: wait for droplet to be available
            while True:
                try:
                    self.connection.destroy_droplet(server.droplet_id)
                    break
                except:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    time.sleep(1)
                    continue
            print("Terminated")
        else:
            print("Aborting termination")

    def filter(self, **kwargs):
        """
        return: list of objects matching filter args
        typically provide should support filter 'name'='foo'
        """
        instances = []

        if 'name' in kwargs:
            name = kwargs['name']
            for droplet in self.connection.droplets():
                if droplet.name == name:
                    instances.append(droplet)
                    print("selected digital ocean droplet: {}".format(droplet.droplet_id))
        else:
            raise NotImplementedError()

        if not instances:
            print(yellow("Warning: {} not found!".format(name), bold=True))

        return instances

    def info(self, server):
        """
        returns dictionary with info about server
        """
        return server.to_json()

    def host_string(self, server):
        #TODO: where to select user/provisioning mode
        return self.info(server)["ip_address"]

