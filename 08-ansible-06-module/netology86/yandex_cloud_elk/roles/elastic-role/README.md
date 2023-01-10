Ansible-Role Elasticsearch for CentOS 7
=========

Role installs Elasticsearch on CentOS 7. 

Tested on CentOS 7.9.2009 (Core).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

* The version of Elasticsearch to install.
  ```yml
  elasticsearch_version: "7.14.0"
  ```
* Directory to install Elasticsearch to.
  ```yml
  elasticsearch_home: "/opt/elasticsearch/{{ elasticsearch_version }}"
  ```
* Directory for Elasticsearch logs
  ```yml
  elasticsearch_logs: "/var/log/elasticsearch"
  ```

Dependencies
------------

None.

Example Playbook
----------------

The simpliest example:
```yaml
- name: Install Elasticsearch
  roles:
    - elastic-role
```

Below is more complete example with variables. It presumes to be used as a part of an ELK stack split on microservices, wehere `el-instance` is the name of Elasticsearch host.
```yaml
- name: Install Elasticsearch
  # todo: todo
```

License
-------

MIT

Author Information
------------------

The role was created by Sergey Shadurskiy in 2022/02 as a homework during a 10-month DevOps cource on Netology online educational platform.
