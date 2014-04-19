from __future__ import print_function
from fabric.api import env, task
from cotton.colors import *
from cotton.api import vm_task, load_provider
from dop.client import Client


def pprinttable(data, headers=None, print=print):
    """
    prints data as a table assuming that data is a list of dictionaries (single level)
    if headers are provided then they specify sequence of columns

    example of data:
    [{'slug': u'ams1', 'name': u'Amsterdam 1', 'region_id': 2},
    {'slug': u'sfo1', 'name': u'San Francisco 1', 'region_id': 3},
    {'slug': u'nyc2', 'name': u'New York 2', 'region_id': 4},
    {'slug': u'ams2', 'name': u'Amsterdam 2', 'region_id': 5},
    {'slug': u'sgp1', 'name': u'Singapore 1', 'region_id': 6}]

    example of headers:
    ['slug', 'name']

    example output:
    -----------------------
    slug  name
    -----------------------
    ams1  Amsterdam 1
    sfo1  San Francisco 1
    nyc2  New York 2
    ams2  Amsterdam 2
    sgp1  Singapore 1

    """
    keys = set()
    formatting = dict()

    if not data:
        return

    def update_dict_with_max(dictionary, key, value):
        if key in dictionary:
            dictionary[key] = max(current_len, dictionary[key])
        else:
            dictionary[key] = current_len

    for line in data:
        keys.update(line.keys())
        for key, value in line.iteritems():
            current_len = len("{}".format(value))
            update_dict_with_max(formatting, key, current_len)

    for key in keys:
        current_len = len("{}".format(key))
        update_dict_with_max(formatting, key, current_len)

    if not headers:
        headers = keys

    formatting_string = "  ".join(map(lambda header: "{{:{}}}".format(formatting[header]), headers))
    line_len = sum([formatting[header] for header in headers]) + len(headers)*2
    print("-"*line_len)
    print(formatting_string.format(*headers))
    print("-"*line_len)
    for line in data:
        values = []
        for header in headers:
            if header in line:
                values.append(line[header])
            else:
                values.append('')

        print(formatting_string.format(*values))


@task
@load_provider
def options():
    assert isinstance(env.provider.connection, Client)
    client = env.provider.connection

    print()

    print(green("Regions"))
    regions = [region.to_json() for region in client.regions()]
    pprinttable(regions, ['slug', 'name'])
    print()

    print(green("Sizes"))
    sizes = [size.to_json() for size in client.sizes()]
    pprinttable(sizes)
    print()

    print(green("Images (public)"))
    images = [image.to_json() for image in client.images()]
    pprinttable(images)
    print()

    print(green("Images (private)"))
    images = [image.to_json() for image in client.images(filter='my_images')]
    pprinttable(images)
    print()

    print(green("SSH keys"))
    ssh_keys = [ssh_key.to_json() for ssh_key in client.ssh_keys()]
    pprinttable(ssh_keys)
    print()

