#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ast import mod
from asyncore import file_dispatcher
# from importlib.resources import path
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: Path to file to create ot set content
        required: true
        type: str
    content:
        description: Content for the file.
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - netology-86.yandex_cloud_elk.my_own_module

author:
    - Sergey Shadurskiy (@run0ut)
'''

EXAMPLES = r'''
# Create a file
- name: Testing module with default content
  netology-86.yandex_cloud_elk.my_own_module:
    path: "~/file.txt

# change content of the  file and have changed true
- name: Testing module with user defined content
  netology-86.yandex_cloud_elk.my_own_module:
    path: "~/file.txt
    content: "My text"

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# The module has no returns
'''

from ansible.module_utils.basic import AnsibleModule
import os


def check_if_file_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def check_if_regular_file(path):
    if os.path.isfile(path):
        return True
    else:
        return False


def get_file_content(path):
    with open(path, 'r') as file:
        content = file.read()
    return content


def check_if_content_the_same(path, content):
    file_content = get_file_content(path)
    if file_content == content:
        return True
    else:
        return False


def create_and_fill_file_with_content(path, content):
    with open(path, 'w') as file:
        file.write(content)
    return True


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # name=dict(type='str', required=True),
        # new=dict(type='bool', required=False, default=False)
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='Hi, Netology!')
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

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        if not os.path.exists(module.params['path']):
            result['changed'] = True
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    # Assume file doesn't exist or has a different content
    # then theck if it's true
    file_doesnt_exist_of_content_differ = True
    if check_if_file_exists(module.params['path']):
        if check_if_regular_file(module.params['path']):
            if check_if_content_the_same(module.params['path'],module.params['content']):
                file_doesnt_exist_of_content_differ = False

    if file_doesnt_exist_of_content_differ:
        create_and_fill_file_with_content(module.params['path'], module.params['content'])
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['path'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()