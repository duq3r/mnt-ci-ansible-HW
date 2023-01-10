# Ansible Collection - netology86.yandex_cloud_elk

Description
------------

The collection contains a simple module [my_own_module](yandex_cloud_elk/plugins/modules/my_own_module.py) that creates a file with user defined content or default content, which is "Hi, Netology!" and a single task role [netology86-role](roles/netology86-role/), that uses these module.

There are also a number of usefull plugins and roles intended to create a ELK-stack with Filebeat on Yandex Cloud Platform:
- Yandex Cloud Compute [module to create/delete instances](plugins/modules/yc_create_instance.py)
- A single task role [yc-create-instance-role](roles/yc-create-instance-role/), that uses these module to create Yandex Cloud instances
- Yandex Cloud [inventory module](plugins/inventory/yc_inventory.py)
- [Elasticsearch](roles/elastic-role), [Kibana](roles/kibana-role), [Logstash](roles/logstash-role) and [Filebeat](roles/filebeat-role) roles
- [Playbook](playbooks/playbook_with_dynamic_inventory.yml), that will create a YC instance and deploy complete ELK-stack and Filebeat on it
- [Inventory-file](yc_inventory.yml), to use playbook with

Dependencies
------------

CLI Yandex Cloud :
- [Documentation main page](https://cloud.yandex.com/en-ru/docs/cli/)
- [Getting started](https://cloud.yandex.com/en-ru/docs/cli/quickstart)

License
-------

MIT

