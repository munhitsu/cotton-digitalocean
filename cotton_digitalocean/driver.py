from __future__ import print_function
import getpass
import time
import datetime
import dateutil.parser
import copy
import pprint
import digitalocean
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
        self.connection = digitalocean.Manager(client_id=client_id, api_key=api_key)
        assert self.connection is not None

    def status(self):
        instances = []
        droplets = self.connection.get_all_droplets()
        for droplet in droplets:
            instances.append(self.info(droplet))
        return instances

    def create(self, name=None, **kwargs):
        """
        return: aws instance object
        instance is booting so don't forget to cotton.fabextras.wait_for_shell()
        """
        zone_config = get_provider_zone_config()

        droplet = digitalocean.Droplet(
            client_id=self.connection.client_id,
            api_key=self.connection.api_key,
            name=name,
            region_id=zone_config['region_id'],
            image_id=zone_config['image_id'],
            size_id=zone_config['size_id'],
            backup_active=zone_config['backup_active'],
            private_networking=zone_config['private_networking'],
            ssh_key_ids=zone_config['ssh_key_ids'])
        droplet.create()

        print("Waiting for instance to run",)
        while droplet.ip_address is None or droplet.status != 'active':
            droplet.load()
            print(self.info(droplet))
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)
        print(" OK")

        return droplet

    def terminate(self, server):
        assert isinstance(server, digitalocean.Droplet)
        pprint.pprint(self.info(server))

        if env.force:
            sure = 'T'
        else:
            sure = prompt(red("Type 'T' to confirm termination"), default='N')

        if sure == 'T':
            server.rename('{}-terminated'.format(server.name))
            time.sleep(1) #TODO: wait for droplet to be available
            server.destroy()
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
            for droplet in self.connection.get_all_droplets():
                if droplet.name == name:
                    instances.append(droplet)
                    print("selected digital ocean droplet: {}".format(droplet.id))
        else:
            raise NotImplementedError()

        if not instances:
            print(yellow("Warning: {} not found!".format(name), bold=True))

        return instances

    def info(self, server):
        """
        returns dictionary with info about server
        """
        info_dict = dict()
        info_dict["name"] = server.name
        info_dict["ip_address"] = server.ip_address
        info_dict["private_ip_address"] = server.private_ip_address
        info_dict["backup_active"] = server.backup_active
        info_dict["status"] = server.status
        return info_dict

    def host_string(self, server):
        #TODO: where to select user/provisioning mode
        return self.info(server)["ip_address"]

