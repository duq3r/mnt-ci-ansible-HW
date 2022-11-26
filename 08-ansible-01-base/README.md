# Домашнее задание к занятию "08.01 Введение в Ansible"

## Подготовка к выполнению
1. Установите ansible версии 2.10 или выше.
2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Выполнено
'''bash
> $ ansible --version                                                                       ⬡ none 
ansible [core 2.13.5]
  config file = None
  configured module search path = ['/Users/e.madan/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /opt/homebrew/Cellar/ansible/6.5.0/libexec/lib/python3.10/site-packages/ansible
  ansible collection location = /Users/e.madan/.ansible/collections:/usr/share/ansible/collections
  executable location = /opt/homebrew/bin/ansible
  python version = 3.10.8 (main, Oct 13 2022, 09:48:40) [Clang 14.0.0 (clang-1400.0.29.102)]
  jinja version = 3.1.2
  libyaml = True
  '''

## Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.
   '''bash
   > $ ansible-playbook -i inventory/test.yml site.yml                                         ⬡ none [±master ●]

PLAY [Print os facts] *****************************************************************************************

TASK [Gathering Facts] ****************************************************************************************
[WARNING]: Platform darwin on host localhost is using the discovered Python interpreter at
/opt/homebrew/bin/python3.10, but future installation of another Python interpreter could change the meaning
of that path. See https://docs.ansible.com/ansible-core/2.13/reference_appendices/interpreter_discovery.html
for more information.
ok: [localhost]

TASK [Print OS] ***********************************************************************************************
ok: [localhost] => {
    "msg": "MacOSX"
}

TASK [Print fact] *********************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP ****************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
'''
2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
  '''bash
  > $ cat group_vars/all/examp.yml                                                            ⬡ none [±master ●]
---
  some_fact: "all default fact"
''' 
3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
 ```bash
 docker ps                                                                                 ⬡ none [±master ●]
CONTAINER ID   IMAGE                      COMMAND           CREATED        STATUS        PORTS     NAMES
4275ee63f606   pycontribs/ubuntu:latest   "sleep 6000000"   16 hours ago   Up 16 hours             ubuntu
1928cb482f30   pycontribs/centos:7        "sleep 6000000"   16 hours ago   Up 16 hours             centos7
```  
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
   ```bash
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}
   ```
5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
  ```bash
 ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}  
```
6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
7.    ```bash
 ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}  
```
8. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
```bash
$ ansible-vault encrypt group_vars/deb/examp.yml --ask-vault-password                       ⬡ none [±master ●]
New Vault password: 
Confirm New Vault password: 
Encryption successful
                                                                                                                 
e.madan@Mac ~/Documents/DevOps/my-homeworks/mnt-homeworks/08-ansible-01-base/playbook                
> $ ansible-vault decrypt group_vars/el/examp.yml --ask-vault-password                       [±master ●]
New Vault password: 
Confirm New Vault password: 
Encryption successful
```
9. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
```bash
ansible-playbook site.yml  -i ./inventory/prod.yml --ask-vault-password                 
Vault password: 
```
10. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
```bash
ansible-doc -t connection -l

Использую ssh
ansible-doc -t connection ssh
```
11. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
```bash
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: docker
  local:
    hosts:
      localhost:
        ansible_connection: local
```
12. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
```bash
ansible-playbook -i inventory/prod.yml site.yml --ask-vault-password                               ⬡ none [±master ●]
Vault password: 

PLAY [Print os facts] ****************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
[WARNING]: Platform darwin on host localhost is using the discovered Python interpreter at /opt/homebrew/bin/python3.10,
but future installation of another Python interpreter could change the meaning of that path. See
https://docs.ansible.com/ansible-core/2.13/reference_appendices/interpreter_discovery.html for more information.
ok: [localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "MacOSX"
}

TASK [Print fact] ********************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP ***************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```
13. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

## Закомичено. 

## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.
2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.
3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.
4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
6. Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
