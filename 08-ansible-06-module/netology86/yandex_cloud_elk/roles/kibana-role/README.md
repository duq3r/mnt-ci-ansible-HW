Ansible-Role Kibana for CentOS 7
=========

Role installs Kibana on CentOS 7. 

Tested on CentOS 7.9.2009 (Core).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

* The version of kibana to install.
  ```yml
  kibana_version: "7.14.0"
  ```
* The URL (including port) over which Kibana will connect to Elasticsearch.
  ```yml
  kibana_elasticsearch_url: "http://localhost:9200"
  ```

Dependencies
------------

None.

Example Playbook
----------------

The simpliest example:
```yaml
- name: Install Kibana
  roles:
    - kibana-role
```

Below is more complete example with variables. It presumes to be used as a part of an ELK stack split on microservices, wehere `el-instance` is the name of Elasticsearch host.
```yaml
- name: Install Kibana
  hosts: kibana
  vars:
    - kibana_elasticsearch_url: ["http://{{ hostvars['el-instance']['ansible_facts']['default_ipv4']['address'] }}:9200/"]
    - kibana_version: "7.15.0"
  roles:
    - kibana-role
  tags: kibana
```

License
-------

MIT

Author Information
------------------

The role was created by Sergey Shadurskiy in 2022/02 as a homework during a 10-month DevOps cource on Netology online educational platform.
