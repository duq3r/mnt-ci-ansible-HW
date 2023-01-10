************
Что нужно сделать, чтобы роль запустилась
************

Запустить докер-контейнер с ролью
============

Например:

.. code-block:: bash

    docker run --name netology85 --privileged=True -v $(pwd)/kibana-role:/opt/kibana-role -v $(pwd)/containers.conf:/etc/containers/containers.conf -w /opt/kibana-role -it netology85-tox bash

Поправить containers.conf
============

Поправить ``utsns`` с ``host`` на ``private``. 

Пример `containers.conf` с изменениями из контейнера, собранного с `этим файлом <https://github.com/netology-code/mnt-homeworks/blob/MNT-7/08-ansible-05-testing/Dockerfile>`_

.. code-block:: toml

    [containers]
    netns="host"
    userns="host"
    ipcns="host"
    #utsns="host"
    utsns="private"
    cgroupns="host"
    cgroups="disabled"
    log_driver = "k8s-file"
    [engine]
    cgroup_manager = "cgroupfs"
    events_logger="file"
    runtime="crun"
