# Chạy các service trên multi node.
Kolla-ansible có hỗ trợ haproxy kết hợp keepalived để chúng ta có thể cân bằng tải các service openstack được chạy trên nhiều node khác nhau.

#### Chú ý, trong bài dưới, các node tôi cấu hình là:
- node controller:
  - con1: 172.16.69.220
  - con2: 172.16.69.235
- node compute:
  - com1: 172.16.69.211
  - com2: 172.16.69.238

# 1. Cấu hình cài đặt chạy service trền nhiều node.
Trên node điều khiển, chỉnh sửa file `vi /usr/local/share/kolla/ansible/inventory/multinode`

```sh
[control]
# These hostname must be resolvable from your deployment host
con1
con2

[network]
con1
con2

[compute]
com1
com2

[storage]
con1
con2
```

Ví dụ ở trên, các nhóm control, network và storage sẽ được chạy trên 2 node là con1 và con2.
nhóm compute sẽ được chạy trên 2 node com1 và com2.

```sh
mongodb:children]
control

[keystone:children]
control

[glance:children]
control

[nova:children]
control

[neutron:children]
network

[cinder:children]
control

[memcached:children]
control

[horizon:children]
control
```

- Ngoài ra, ở dưới sẽ có phần cấu hình các service sẽ được chạy trên từng group nào. Ví dụ ở đây là keystone, glance, memcached, horizon chạy trên nhóm control.

# 2. Vấn đề đồng bộ database trong kolla.
- Trên từng node control, container mariadb đảm nhiệm chức năng lưu trữ cơ sở dữ liệu cho openstack.
- Nếu ta khai báo chạy nhiều node control, thì cơ sở dữ liệu mariadb sẽ được cài đặt đồng bộ trên các node.
- Dưới dây là cấu hình đồng bộ cơ sở dữ liệu trong container mariadb trê node con1

```sh
[mysqld]
wsrep_cluster_address = gcomm://172.16.69.220:4567,172.16.69.235:4567
wsrep_provider_options = gmcast.listen_addr=tcp://172.16.69.220:4567;ist.recv_addr=172.16.69.220:4568
wsrep_node_address = 172.16.69.220:4567
wsrep_sst_receive_address = 172.16.69.220:4444
wsrep_provider = /usr/lib/galera/libgalera_smm.so
wsrep_cluster_name = "openstack"
wsrep_node_name = con1
wsrep_sst_method = xtrabackup-v2
wsrep_sst_auth = root:lZlYg6tRgvo2urduFP98kzBhax5m4q2X5kjTeWuA
wsrep_slave_threads = 4
max_connections = 10000
```

# 3. Cấu hình keepalived
- Đây là phần cấu hình keepalived trên node con1

```sh
vrrp_script check_alive {
    script "/check_alive.sh"
    interval 2
    fall 2
    rise 10
}

vrrp_instance kolla_internal_vip_51 {
    state BACKUP
    nopreempt
    interface eth0
    virtual_router_id 51
    priority 1
    advert_int 1
    virtual_ipaddress {
        172.16.69.249 dev eth0
    }
    authentication {
        auth_type PASS
        auth_pass lD6c7a5V4IFqAC7aToxMM6WtggRcHWQ2Cl8G5yoU
    }
    track_script {
        check_alive
    }
}
```

# 3. Haproxy xử lý request như thế nào?

- Đây là phần cấu hình haproxy trong container haproxy trên node con1.

```sh
listen mariadb
  mode tcp
  option tcplog
  option tcpka
  option mysql-check user haproxy
  bind 172.16.69.249:3306
  server con1 172.16.69.220:3306 check inter 2000 rise 2 fall 5 
  server con2 172.16.69.235:3306 check inter 2000 rise 2 fall 5 backup

listen rabbitmq_management
  bind 172.16.69.249:15672
  server con1 172.16.69.220:15672 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:15672 check inter 2000 rise 2 fall 5

listen keystone_internal
  bind 172.16.69.249:5000
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:5000 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:5000 check inter 2000 rise 2 fall 5

listen keystone_admin
  bind 172.16.69.249:35357
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:35357 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:35357 check inter 2000 rise 2 fall 5

listen glance_registry
  bind 172.16.69.249:9191
  server con1 172.16.69.220:9191 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:9191 check inter 2000 rise 2 fall 5

listen glance_api
  bind 172.16.69.249:9292
  server con1 172.16.69.220:9292 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:9292 check inter 2000 rise 2 fall 5

listen nova_api
  bind 172.16.69.249:8774
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:8774 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:8774 check inter 2000 rise 2 fall 5

listen nova_api_ec2
  bind 172.16.69.249:8773
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:8773 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:8773 check inter 2000 rise 2 fall 5

listen nova_metadata
  bind 172.16.69.249:8775
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:8775 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:8775 check inter 2000 rise 2 fall 5

listen nova_novncproxy
  bind 172.16.69.249:6080
  http-request del-header X-Forwarded-Proto
  http-request set-header X-Forwarded-Proto https if { ssl_fc }
  server con1 172.16.69.220:6080 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:6080 check inter 2000 rise 2 fall 5

listen neutron_server
  bind 172.16.69.249:9696
  server con1 172.16.69.220:9696 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:9696 check inter 2000 rise 2 fall 5

listen horizon
  bind 172.16.69.249:80
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:80 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:80 check inter 2000 rise 2 fall 5

listen heat_api
  bind 172.16.69.249:8004
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:8004 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:8004 check inter 2000 rise 2 fall 5

listen heat_api_cfn
  bind 172.16.69.249:8000
  http-request del-header X-Forwarded-Proto
  server con1 172.16.69.220:8000 check inter 2000 rise 2 fall 5
  server con2 172.16.69.235:8000 check inter 2000 rise 2 fall 5
```

- Ở phần `mariadb` ta thấy node1 con2 cấu hình backup tức là nó sẽ chạy ở chế độ `standby`. 
```sh
The Galera cluster configuration directive backup indicates that two of the three controllers are standby nodes. This ensures that only one node services write requests because OpenStack support for multi-node writes is not yet production-ready.

https://docs.openstack.org/ha-guide/controller-ha-haproxy.html
```

- Ở đây ta thấy không có phần cấu hình chỉ định thuật toán cân bằng tải. Vì vậy, mặc định haproxy sẽ chia tải theo thuật toán roundrobin.
```sh
The load balancing algorithm of a backend is set to roundrobin when no other
algorithm, mode nor option have been set. The algorithm may only be set once
for each backend.

http://cbonte.github.io/haproxy-dconv/configuration-1.4.html#4.2-balance
```


