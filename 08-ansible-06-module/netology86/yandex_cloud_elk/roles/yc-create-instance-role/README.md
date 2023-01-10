yc-create-instance-role
=========

Requirements
------------

CLI Yandex Cloud :
- [Documentation main page](https://cloud.yandex.com/en-ru/docs/cli/)
- [Getting started](https://cloud.yandex.com/en-ru/docs/cli/quickstart)

The role is supposed to be started against localhost, but no reasions could stop you from using it on any node.
The only requirement though, YC CLI has to be installed on the node against which the role is executed.
In that case, keep in mind that SSH pub key to acces YC instance would also be taken from that node. 

Role Variables
--------------

  - `network_interface`: VPC subnet name to tie the instance to/
  - `name`: Name and **hostname** of the instance.
  - `zone`: Data center zone of availability.
  - `ssh_key`: SSH pub key to copy for default user "yc-user". If not set, module will use default ssh pub key ~/.ssh/id_rsa.pub
  - `cores`: Number of compute cores.
  - `core_fraction`: Persentage of compute time guaranteed to the VM. Options 20, 50 and 100 are available.
  - `memory`: RAM in gigabytes.
  - `platform`: Compute platform. See the list in YC documentation.
  - `image_family`: OS family for the boot image. For example "centos-7".
  - `boot_disk_size`: Boot disk size in gigabytes.

Dependencies
------------

None

Example Playbook
----------------

- Create completeley default instance with only required options.

      - name: Testing module with default config
        host: localhost
        netology-86.yandex_cloud_elk.yc_create_instance:
          network_interface: "net-ru-central1-a"

- More custom config to create a VM.

      - name: Create my fancy VM
        host: localhost
        netology-86.yandex_cloud_elk.yc_create_instance:
          network_interface: "net-ru-central1-a"
          name: "my_fancy_VM"
          cores: 8
          memory: 32
          image_family: "debian-11"
          boot_disk_size: "1000"

License
-------

MIT

