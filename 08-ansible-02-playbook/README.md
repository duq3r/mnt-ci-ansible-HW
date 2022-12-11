# Домашнее задание к занятию "08.02 Работа с Playbook"

## Подготовка к выполнению
1. Создайте свой собственный (или используйте старый) публичный репозиторий на github с произвольным именем.
2. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
3. Подготовьте хосты в соотвтествии с группами из предподготовленного playbook. 
4. Скачайте дистрибутив [java](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) и положите его в директорию `playbook/files/`. 

## Основная часть
1. Приготовьте свой собственный inventory файл `prod.yml`.
```bash
---
elasticsearch:
  hosts:
    centos:
      ansible_host: 172.30.0.2
      ansible_connection: ssh
      ansible_user: app-admin
      ansible_ssh_private_key_file: ssh_env/id_rsa_insecure
```
2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает kibana. <br>

3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.

4. Tasks должны: скачать нужной версии дистрибутив, выполнить распаковку в выбранную директорию, сгенерировать конфигурацию с параметрами.
group_vars/elasticsearch/vars.yml
```bash
---
elastic_version: "7.10.1"
elastic_home: "/opt/elastic/{{ elastic_version }}"
kibana_home: "/opt/kibana/{{ elastic_version }}"
```

site.yml
```bash
...
- name: Install Kibana
  hosts: elasticsearch
  tasks:
    - name: Get Kibana 
      get_url: 
        url: https://artifacts.elastic.co/downloads/kibana/kibana-{{ elastic_version }}-linux-x86_64.tar.gz
        dest: "/tmp/kibana-{{ elastic_version }}-linux-x86_64.tar.gz"
        mode: 0755
        timeout: 60
        force: true
        validate_certs: false
      register: get_kibana
      until: get_kibana is succeeded
      tags: kibana
    - name: Create directrory for Kibana
      become: true
      file:
        state: directory
        path: "{{ kibana_home }}"
        mode: 0755
      tags: kibana
    - name: Extract Kibana in the installation directory
      become: true
      unarchive:
        copy: false
        src: "/tmp/kibana-{{ elastic_version }}-linux-x86_64.tar.gz"
        dest: "{{ kibana_home }}"
        extra_opts: [--strip-components=1]
        creates: "{{ kibana_home }}/bin/kibana"
      tags: kibana
    - name: Set environment Kibana
      become: true
      template:
        src: templates/kibana.sh.j2
        dest: /etc/profile.d/kibana.sh
        mode: 0755
      tags: kibana

```

templates/kibana.sh.j2
```bash
# Warning: This file is Ansible Managed, manual changes will be overwritten on next playbook run.
#!/usr/bin/env bash

export KIBANA_HOME={{ kibana_home }}
export PATH=$PATH:$KIBANA_HOME/bin
```
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
Исправил ошибки
```bash
$ ansible-lint site.yml
WARNING: PATH altered to include /usr/bin
WARNING  Overriding detected file kind 'yaml' with 'playbook' for given positional argument: site.yml
WARNING  Listing 7 violation(s) that are fatal
risky-file-permissions: File permissions unset or incorrect
site.yml:9 Task/Handler: Upload .tar.gz file containing binaries from local storage

risky-file-permissions: File permissions unset or incorrect
site.yml:16 Task/Handler: Ensure installation dir exists

risky-file-permissions: File permissions unset or incorrect
site.yml:32 Task/Handler: Export environment variables

risky-file-permissions: File permissions unset or incorrect
site.yml:52 Task/Handler: Create directrory for Elasticsearch

risky-file-permissions: File permissions unset or incorrect
site.yml:68 Task/Handler: Set environment Elastic

risky-file-permissions: File permissions unset or incorrect
site.yml:88 Task/Handler: Create directrory for Kibana

risky-file-permissions: File permissions unset or incorrect
site.yml:103 Task/Handler: Set environment Kibana

You can skip specific rules or tags by adding them to your configuration file:
# .ansible-lint
warn_list:  # or 'skip_list' to silence them completely
  - experimental  # all rules tagged as experimental

Finished with 0 failure(s), 7 warning(s) on 1 files.
```
Нужно было установить права: 0644 для архивов и 0755 для папок и исполныемых файлов.
Чтобы избавиться от "Overriding detected file kind"
После исправления:
```
$ ansible-lint site.yml
WARNING: PATH altered to include /usr/bin
```

Последний варнинг происходит от того, что ansible установлен в директории пользователя командой pip3, а бинарник Питона лежит в /usr/bin`. Вроде не критично.

1. Попробуйте запустить playbook на этом окружении с флагом `--check`.
```bash
   $ ansible-playbook -i inventory/prod.yml site.yml --check

PLAY [Install Java] **********************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Set facts for Java 11 vars] ********************************************************************
ok: [centos_elk_server]

TASK [Upload .tar.gz file containing binaries from local storage] ************************************
ok: [centos_elk_server]

TASK [Ensure installation dir exists] ****************************************************************
ok: [centos_elk_server]

TASK [Extract java in the installation directory] ****************************************************
skipping: [centos_elk_server]

TASK [Export environment variables] ******************************************************************
changed: [centos_elk_server]

PLAY [Install Elasticsearch] *************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Upload tar.gz Elasticsearch from remote URL] ***************************************************
changed: [centos_elk_server]

TASK [Create directrory for Elasticsearch] ***********************************************************
ok: [centos_elk_server]

TASK [Extract Elasticsearch in the installation directory] *******************************************
skipping: [centos_elk_server]

TASK [Set environment Elastic] ***********************************************************************
changed: [centos_elk_server]

PLAY [Install Kibana] ********************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Get Kibana] ************************************************************************************
changed: [centos_elk_server]

TASK [Create directrory for Kibana] ******************************************************************
ok: [centos_elk_server]

TASK [Extract Kibana in the installation directory] **************************************************
skipping: [centos_elk_server]

TASK [Set environment Kibana] ************************************************************************
changed: [centos_elk_server]

PLAY RECAP *******************************************************************************************
centos_elk_server          : ok=13   changed=5    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
```
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
```bash
PLAY [Install Java] **********************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Set facts for Java 11 vars] ********************************************************************
ok: [centos_elk_server]

TASK [Upload .tar.gz file containing binaries from local storage] ************************************
ok: [centos_elk_server]

TASK [Ensure installation dir exists] ****************************************************************
ok: [centos_elk_server]

TASK [Extract java in the installation directory] ****************************************************
skipping: [centos_elk_server]

TASK [Export environment variables] ******************************************************************
--- before
+++ after
@@ -1,4 +1,4 @@
 {
-    "mode": "0644",
+    "mode": "0755",
     "path": "/etc/profile.d/jdk.sh"
 }

changed: [centos_elk_server]

PLAY [Install Elasticsearch] *************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Upload tar.gz Elasticsearch from remote URL] ***************************************************
changed: [centos_elk_server]

TASK [Create directrory for Elasticsearch] ***********************************************************
ok: [centos_elk_server]

TASK [Extract Elasticsearch in the installation directory] *******************************************
skipping: [centos_elk_server]

TASK [Set environment Elastic] ***********************************************************************
--- before
+++ after: /home/sergey/.ansible/tmp/ansible-local-77854lvye89t_/tmpta0g0cka/elastic.sh.j2
@@ -0,0 +1,5 @@
+# Warning: This file is Ansible Managed, manual changes will be overwritten on next playbook run.
+#!/usr/bin/env bash
+
+export ES_HOME=/opt/elastic/7.10.1
+export PATH=$PATH:$ES_HOME/bin
\ No newline at end of file

changed: [centos_elk_server]

PLAY [Install Kibana] ********************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [centos_elk_server]

TASK [Get Kibana] ************************************************************************************
ok: [centos_elk_server]

TASK [Create directrory for Kibana] ******************************************************************
ok: [centos_elk_server]

TASK [Extract Kibana in the installation directory] **************************************************
skipping: [centos_elk_server]

TASK [Set environment Kibana] ************************************************************************
--- before
+++ after
@@ -1,4 +1,4 @@
 {
-    "mode": "0644",
+    "mode": "0755",
     "path": "/etc/profile.d/kibana.sh"
 }

changed: [centos_elk_server]

PLAY RECAP *******************************************************************************************
centos_elk_server          : ok=13   changed=4    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
```
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
```bash
PLAY [Install Java] **********************************************************************************************

TASK [Gathering Facts] *******************************************************************************************
ok: [centos_elk_server]

TASK [Set facts for Java 11 vars] ********************************************************************************
ok: [centos_elk_server]

TASK [Upload .tar.gz file containing binaries from local storage] ************************************************
ok: [centos_elk_server]

TASK [Ensure installation dir exists] ****************************************************************************
ok: [centos_elk_server]

TASK [Extract java in the installation directory] ****************************************************************
skipping: [centos_elk_server]

TASK [Export environment variables] ******************************************************************************
ok: [centos_elk_server]

PLAY [Install Elasticsearch] *************************************************************************************

TASK [Gathering Facts] *******************************************************************************************
ok: [centos_elk_server]

TASK [Upload tar.gz Elasticsearch from remote URL] ***************************************************************
ok: [centos_elk_server]

TASK [Create directrory for Elasticsearch] ***********************************************************************
ok: [centos_elk_server]

TASK [Extract Elasticsearch in the installation directory] *******************************************************
skipping: [centos_elk_server]

TASK [Set environment Elastic] ***********************************************************************************
ok: [centos_elk_server]

PLAY [Install Kibana] ********************************************************************************************

TASK [Gathering Facts] *******************************************************************************************
ok: [centos_elk_server]

TASK [Get Kibana] ************************************************************************************************
ok: [centos_elk_server]

TASK [Create directrory for Kibana] ******************************************************************************
ok: [centos_elk_server]

TASK [Extract Kibana in the installation directory] **************************************************************
skipping: [centos_elk_server]

TASK [Set environment Kibana] ************************************************************************************
ok: [centos_elk_server]

PLAY RECAP *******************************************************************************************************
centos_elk_server          : ok=13   changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
```
9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
    <br>## Выполнено!.
10. Готовый playbook выложите в свой репозиторий, в ответ предоставьте ссылку на него.
 <br>## Выполнено!.

## Необязательная часть

1. Приготовьте дополнительный хост для установки logstash.
2. Пропишите данный хост в `prod.yml` в новую группу `logstash`.
3. Дополните playbook ещё одним play, который будет исполнять установку logstash только на выделенный для него хост.
4. Все переменные для нового play определите в отдельный файл `group_vars/logstash/vars.yml`.
5. Logstash конфиг должен конфигурироваться в части ссылки на elasticsearch (можно взять, например его IP из facts или определить через vars).
6. Дополните README.md, протестируйте playbook, выложите новую версию в github. В ответ предоставьте ссылку на репозиторий.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
