#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ast import mod
# from asyncore import file_dispatcher
# from importlib.resources import path
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yc_create_instance

short_description: This module creates Yandex Cloud compute instance

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module creates Yandex Cloud compute instance and requires Yandex CLI to do that.
             The module will only create instance and check it's existence. It will not be fixing
             instance properties, if it's been changed manually or with a different tool.
             The presence of the instance is checked by it's name.

options:
    network_interface:
        description: VPC subnet name to tie the instance to/
        required: true
        type: str
    name:
        description: Name of the instance/
        required: false
        type: str
    hostname:
        description: Hostname of the instance/
        required: false
        type: str
    zone:
        description: Data center zone of availability/
        required: false
        type: str
    ssh_key:
        description: SSH pub key to copy for default user "yc-user". If not set, module will use default ssh pub key ~/.ssh/id_rsa.pub
        required: false
        type: str
    cores:
        description: Number of compute cores/
        required: false
        type: str
    core_fraction:
        description: Persentage of compute time guaranteed to the VM. Options 20, 50 and 100 are available.
        required: false
        type: str
    memory:
        description: RAM in gigabytes.
        required: false
        type: str
    platform:
        description: Compute platform. See the list in YC documentation.
        required: false
        type: str
    image_family:
        description: OS family for the boot image. For example "centos-7".
        required: false
        type: str
    boot_disk_size: Boot disk size in gigabytes.
        description:
        required:
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - netology-86.yandex_cloud_elk.yc_create_instance

author:
    - Sergey Shadurskiy (@run0ut)
'''

EXAMPLES = r'''
# Create completeley default instance with only required options.
- name: Testing module with default config
  host: localhost
  netology-86.yandex_cloud_elk.yc_create_instance:
    network_interface: "net-ru-central1-a"

# More custom config to create a VM.
- name: Create my fancy VM
  host: localhost
  netology-86.yandex_cloud_elk.yc_create_instance:
    network_interface: "net-ru-central1-a"
    name: "my_fancy_VM"
    cores: 8
    memory: 32
    image_family: "debian-11"
    boot_disk_size: "1000"

# fail the module
- name: Test failure of the module
  host: localhost
  netology-86.yandex_cloud_elk.yc_create_instance:
    name: "fail me"
'''

RETURN = r'''
# The module has no returns
'''

from ansible.module_utils.basic import AnsibleModule
import os
import subprocess
import json


def create_instance(args):

    # yc compute instance create --name elk-instance --create-boot-disk image-folder-id=standard-images,image-family=debian-9
    #     --name elk-instance \
    #     --hostname elk-intsance \
    #     --create-boot-disk image-family=centos-7
    #     --network-interface subnet-name=net-ru-central1-a,nat-ip-version=ipv4 \
    #     --zone ru-central1-a \
    #     --ssh-key ~/.ssh/id_rsa.pub \
    #     --cores 4 \
    #     --core-fraction 100 \
    #     --memory 4GB \
    #     --platform "standard-v1" \

    args['ssh_key'] = os.path.expanduser(args['ssh_key'])
    vars = [
        "yc", "compute", "instance", "create",
        "--name", args['name'],
        "--hostname", args['hostname'],
        "--network-interface", "subnet-name={network_interface},nat-ip-version=ipv4".format(**args),
        "--zone", args['zone'],
        "--ssh-key", args['ssh_key'],
        "--cores", args['cores'],
        "--core-fraction", args['core_fraction'],
        "--memory", "{memory}GB".format(**args),
        "--platform", "{platform}".format(**args),
        "--create-boot-disk","image-folder-id=standard-images,image-family={image_family},size={boot_disk_size}GB".format(**args)
    ]
    process = subprocess.Popen(vars, 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
    process.wait()
    # for stdout_line in iter(process.stdout.readline, ""):
    #     print(stdout_line)


def get_instance_info(args):

    # yc compute instance get --name netology86-instance --format=json
    
    vars = [
        "yc", "compute", "instance", "get", 
        "--name", args['name'], 
        "--format=json"
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


def main():
    module_args = dict(
        name=dict(type='str', required=False, default="netology86-instance"),
        hostname=dict(type='str', required=False, default="netology86-intsance"),
        network_interface=dict(type='str', required=True),
        zone=dict(type='str', required=False, default="ru-central1-a"),
        ssh_key=dict(type='str', required=False, default="~/.ssh/id_rsa.pub"),
        cores=dict(type='str', required=False, default="2"),
        core_fraction=dict(type='str', required=False, default="100"),
        memory=dict(type='str', required=False, default="4"),
        platform=dict(type='str', required=False, default="standard-v1" ),
        image_family=dict(type='str', required=False, default="centos-7" ),
        boot_disk_size=dict(type='str', required=False, default="20")
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Check if instance exists to decide if any action required
    instance_info = json.loads(get_instance_info(module.params))

    # If instance doesn't have network interface, it's most like doesn't exist
    # because YC doesn't allow you to create instances not connected to a network
    if module.check_mode:
        if not "network_interfaces" in instance_info:
            result['changed'] = True
        module.exit_json(**result)

    # Do nothing if instance exists or create one and return changed status to ansible
    if "network_interfaces" in instance_info:
        # print(instance_info['network_interfaces'][0]['primary_v4_address']['one_to_one_nat']['address'])
        pass
    else:
        create_instance(module.params)
        result['changed'] = True

    # Just in case to test what it looks like when module fails
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()