from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: yc_inventory
    plugin_type: inventory
    short_description: Returns Ansible inventory from Yandex Cloud
    description: Returns Ansible inventory from Yandex Cloud
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['my_csv_plugin']
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError
import json
import os 
import subprocess


class InventoryModule(BaseInventoryPlugin):
    NAME = 'netology86.yandex_cloud_elk.yc_inventory'

    def get_instance_info(self):

        # yc compute instance list --format=json
        
        vars = [
            "yc", "compute", "instance", "list", "--format=json"
        ]
        process = subprocess.Popen(vars, 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
        process.wait()
        data, err = process.communicate()
        if process.returncode == 0:
            return data
        else:
            print("Error:", err)
        return "{}"


    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin toconsume'''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current
            # user
            if path.endswith(('yc.yaml','yc.yml','yc_inventory.yaml','yc_inventory.yml')):
                valid = True
        return valid


    def parse(self, inventory, loader, path, cache):
        '''Return dynamic inventory from source '''
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        instance_info = json.loads(self.get_instance_info())

        self.inventory.add_group("yacloud")

        for instance in instance_info:
            try:
                if instance['status'] == "RUNNING":
                    instance['ipv4'] = instance['network_interfaces'][0]['primary_v4_address']['one_to_one_nat']['address']
                    # If instance was created nameless, use it's id insted. YC Web Console uses the same approach
                    if not "name" in instance:
                        instance['name'] = instance['id']
                    self.inventory.add_host(instance["name"], group="yacloud")
                    self.inventory.set_variable(instance["name"], 'ansible_host', instance['ipv4'])
            except:
                # Don't add instance into inventory, if it doesn't have a publick IP address
                pass
