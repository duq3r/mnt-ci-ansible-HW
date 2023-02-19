# Домашнее задание к занятию "10.02. Системы мониторинга" Мадан Евгений
10-monitoring-02-systems


## Обязательные задания

1. Опишите основные плюсы и минусы pull и push систем мониторинга.

### Решение

#### Push модель:

Плюсы:

- Настройка точек приёма метрик осуществляется на агентах, что позволяет настроить вывод метрик в несколько систем мониторинга и возможность реализовать репликацию;
- UDP является менее затратным способом передачи данных, вследствие чего может вырасти производительность сбора метрик;
- Работает за NAT;
- Более гибкая настройка отправки пакетов данных с метриками. На каждом клиенте можно задать нужный нам объем данных и частоту отправки.

Минусы:

- Затрудняется верификация данных в системах мониторинга. Эмулируя действия агента и можно размыть данные мониторинга ложной информацией;
- Агенты могут зафлудить сервера запросами спровоцировав DDoS;
- Протокол UDP не гарантирует доставку данных.
#### Pull модель

Плюсы:

- Легче контролировать подлинность данных. Есть гарантия опроса только тех агентов, которые настроены в системе мониторинга;
- Упрощенная отладка получения данных с агентов. Так как данные запрашиваются посредством HTTP, можно самостоятельно запрашивать эти данные, используя ПО вне системы мониторинга;
- Сервер собирает данные с агентов когда может, и если в данный момент нет свободных ресурсов - заберёт данные позже;
- Безопасность при pull-модели гораздо выше. Не требует открытия порта сервера во вне. Проще защитить трафик, т.к. часто используется HTTP/S

Минусы:

- Более высокие требования к ресурсам, особенно при использовании защищённых каналов связи;
- Не работает за NAT. Надо ставить какой-нибудь прокси.


2. Какие из ниже перечисленных систем относятся к push модели, а какие к pull? А может есть гибридные?

    - Prometheus 
    - TICK
    - Zabbix
    - VictoriaMetrics
    - Nagios

### Решение

| Система         | Модель                          |
|-----------------|---------------------------------|
| Prometheus      | Pull (Push с Pushgateway)       |
| TICK            | Push                            |
| Zabbix          | Push (Pull с Zabbix Proxy)      |
| VictoriaMetrics | Push/Pull, зависит от источника |
| Nagios          | Pull                            |



3. Склонируйте себе [репозиторий](https://github.com/influxdata/sandbox/tree/master) и запустите TICK-стэк, 
используя технологии docker и docker-compose.(по инструкции ./sandbox up )

В виде решения на это упражнение приведите выводы команд с вашего компьютера (виртуальной машины):

    - curl http://localhost:8086/ping
    - curl http://localhost:8888
    - curl http://localhost:9092/kapacitor/v1/ping

### Решение

```bash
root@ansibleserv:~/ansible/TICK-stek/sandbox# curl http://localhost:8086/ping
root@ansibleserv:~/ansible/TICK-stek/sandbox# curl http://localhost:8888
<!DOCTYPE html><html><head><link rel="stylesheet" href="/index.c708214f.css"><meta http-equiv="Content-type" content="text/html; charset=utf-8"><title>Chronograf</title><link rel="icon shortcut" href="/favicon.70d63073.ico"></head><body> <div id="react-root" data-basepath=""></div> <script type="module" src="/index.e81b88ee.js"></script><script src="/index.a6955a67.js" nomodule="" defer></script> </body></html>root@ansibleserv:~/ansible/TICK-stek/sandbox# curl http://localhost:9092/kapacitor/v1/ping
root@ansibleserv:~/ansible/TICK-stek/sandbox#
```

А также скриншот веб-интерфейса ПО chronograf (`http://localhost:8888`). 

![](pic/Chronograf.jpg)

P.S.: если при запуске некоторые контейнеры будут падать с ошибкой - проставьте им режим `Z`, например
`./data:/var/lib:Z`

4. Изучите список [telegraf inputs](https://github.com/influxdata/telegraf/tree/master/plugins/inputs).
    - Добавьте в конфигурацию telegraf плагин - [disk](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/disk):
    ```
    [[inputs.disk]]
      ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
    ```
    - Так же добавьте в конфигурацию telegraf плагин - [mem](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/mem):
    ```
    [[inputs.mem]]
    ```
    - После настройки перезапустите telegraf.
 
    - Перейдите в веб-интерфейс Chronograf (`http://localhost:8888`) и откройте вкладку `Data explorer`.
    - Нажмите на кнопку `Add a query`
    - Изучите вывод интерфейса и выберите БД `telegraf.autogen`
    - В `measurments` выберите mem->host->telegraf_container_id , а в `fields` выберите used_percent. 
    Внизу появится график утилизации оперативной памяти в контейнере telegraf.
    - Вверху вы можете увидеть запрос, аналогичный SQL-синтаксису. 
    Поэкспериментируйте с запросом, попробуйте изменить группировку и интервал наблюдений.
    - Приведите скриншот с отображением
    метрик утилизации места на диске (disk->host->telegraf_container_id) из веб-интерфейса. 

### Решение

- Утилизация памяти
![](pic/Chronograf-mem.jpg)

- Утилизация диска
![](pic/Chronograf-disc.jpg)


5. Добавьте в конфигурацию telegraf следующий плагин - [docker](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/docker):
```
[[inputs.docker]]
  endpoint = "unix:///var/run/docker.sock"
```

Дополнительно вам может потребоваться донастройка контейнера telegraf в `docker-compose.yml` дополнительного volume и 
режима privileged:
```
  telegraf:
    image: telegraf:1.4.0
    privileged: true
    volumes:
      - ./etc/telegraf.conf:/etc/telegraf/telegraf.conf:Z
      - /var/run/docker.sock:/var/run/docker.sock:Z
    links:
      - influxdb
    ports:
      - "8092:8092/udp"
      - "8094:8094"
      - "8125:8125/udp"
```

После настройки перезапустите telegraf, обновите веб интерфейс и приведите скриншотом список `measurments` в 
веб-интерфейсе базы telegraf.autogen . Там должны появиться метрики, связанные с docker.

Факультативно можете изучить какие метрики собирает telegraf после выполнения данного задания.

### Решение

Поменял в файле `docker-compose.yml` на:
```bash
  telegraf:
    # Full tag list: https://hub.docker.com/r/library/telegraf/tags/
    build:
      context: ./images/telegraf/
      dockerfile: ./${TYPE}/Dockerfile
      args:
        TELEGRAF_TAG: ${TELEGRAF_TAG}
    image: "telegraf"
    privileged: true
    user: telegraf:998
    environment:
      HOSTNAME: "telegraf-getting-started"
    # Telegraf requires network access to InfluxDB
    links:
      - influxdb
    volumes:
      # Mount for telegraf configuration
      - ./telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:Z
      # Mount for Docker API access
      - /var/run/docker.sock:/var/run/docker.sock:Z
    depends_on:
      - influxdb
    ports:
      - "8092:8092/udp"
      - "8094:8094"
      - "8125:8125/udp"
```
Плагин docker добавлять не пришлось. Параметр уже был в фале конфигурации
 

- Метрики docker появились
![](pic/Chronograf-docker.jpg)


## Дополнительное задание (со звездочкой*) - необязательно к выполнению

В веб-интерфейсе откройте вкладку `Dashboards`. Попробуйте создать свой dashboard с отображением:

    - утилизации ЦПУ
    - количества использованного RAM
    - утилизации пространства на дисках
    - количество поднятых контейнеров
    - аптайм
    - ...
    - фантазируйте)
    
    ---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---