from __future__ import print_function
from fabric.api import env, task
from cotton.colors import *
from cotton.api import vm_task, load_provider
from dop.client import Client


@task
@load_provider
def options():
    assert isinstance(env.provider.connection, Client)
    client = env.provider.connection


    print(green("Regions"))
    for region in client.regions():
        print(region.to_json())

    print(green("Sizes"))
    for size in client.sizes():
        print(size.to_json())

    print(green("Images (public):"))
    for image in client.images():
        print(image.to_json())

    print(green("Images (private):"))
    for image in client.images(filter='my_images'):
        print(image.to_json())

    print(green("SSH keys"))
    for ssh_key in client.ssh_keys():
        print(ssh_key.to_json())
