Ansible-Role Logstash for CentOS 7
=========

Role installs Logstash on CentOS 7. 

Tested on CentOS 7.9.2009 (Core).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

* Logstash version
  ```yml
  logstash_version: "7.14.0"
  ```
* The URL (including port) over which Logstash will send data to Elasticsearch.
  ```yml
  logstash_elasticsearch_url: "http://localhost:9200"
  ```
* JVM memory limits. Usefull to avoid oom killer.
  ```yml
  logstash_jvm_initial: "256m"
  logstash_jvm_maximum: "256m"
  ```

Dependencies
------------

None.

Example Playbook
----------------

The simpliest example:
```yaml
- name: Install Logstash
  roles:
    - logstash-role
```
Below is more complete example with variables.
```yaml
- name: Install Logstash
  hosts: el
  vars:
    - logstash_version: "7.14.0"
    - logstash_elasticsearch_url: ["http://{{ hostvars['el-instance']['ansible_facts']['default_ipv4']['address'] }}:9200/"]
    - logstash_java_opts: "-Xms256m -Xmx256m"
  roles:
    - logstash-role
  tags: logstash
```

License
-------

MIT

Author Information
------------------

The role was created by Sergey Shadurskiy in 2022/02 as a homework during a 10-month DevOps cource on Netology online educational platform.
