# Cài đặt nova.

## I. Mô hình và phân hoạch IP.


## II. Cài đặt.

### 1. Trên node controller.

- Truy cập vào Database để tại DB cho nova :

```sh
 mysql -uroot -pDB_PASS
```

Thay thế `DB_PASS` bằng password DB tương ứng.

- Tạo DB :

```sh
CREATE DATABASE nova_api;
CREATE DATABASE nova;

 GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'PASSWORD';
 GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'PASSWORD';
 GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'PASSWORD';
 GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'PASSWORD';

 FLUSH PRIVILEGES;

 exit;
```

Thay thế `PASSWORD` bằng mật khẩu muốn đặt.

- Khai báo biến môi trường :

```sh
source admin-openrc
```

- Tạo nova-user :

```sh
openstack user create --domain default \
--password-prompt nova
```

- Thêm role admin vào user nova :

```sh
openstack role add --project service --user nova admin
```

- Tạo nova service :

```sh
openstack service create --name nova \
  --description "OpenStack Compute" compute
```

- Tạo enpoint :

```sh
openstack endpoint create --region RegionOne \
  compute public http://controller:8774/v2.1/%\(tenant_id\)s

+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | 3c1caa473bfe4390a11e7177894bcc7b          |
| interface    | public                                    |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 060d59eac51b4594815603d75a00aba2          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller:8774/v2.1/%(tenant_id)s |
+--------------+-------------------------------------------+

$ openstack endpoint create --region RegionOne \
  compute internal http://controller:8774/v2.1/%\(tenant_id\)s

+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | e3c918de680746a586eac1f2d9bc10ab          |
| interface    | internal                                  |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 060d59eac51b4594815603d75a00aba2          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller:8774/v2.1/%(tenant_id)s |
+--------------+-------------------------------------------+

$ openstack endpoint create --region RegionOne \
  compute admin http://controller:8774/v2.1/%\(tenant_id\)s

+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | 38f7af91666a47cfb97b4dc790b94424          |
| interface    | admin                                     |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 060d59eac51b4594815603d75a00aba2          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller:8774/v2.1/%(tenant_id)s |
+--------------+-------------------------------------------+
```

- Cài đặt các gói phần mềm sau :

```sh
apt install nova-api nova-conductor nova-consoleauth \
  nova-novncproxy nova-scheduler
```

- Dùng trình soạn thảo `vi` mờ file cấu hình `/etc/nova/nova.conf` :

```sh
vi /etc/nova/nova.conf
```

- Chỉnh sửa lại file cấu hình như sau :

Tại các section [api_database] và [database] cấu hình truy cập DB :

```sh
[api_database]

connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova_api

[database]

connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova
```

Tại section [DEFAULT] cấu hình truy cập RabbitMQ :

```sh
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller
```

Tại section [DEFAULT] và [keystone_authtoken] cấu hình truy cập dịch vụ identity : 

```sh
[DEFAULT]

auth_strategy = keystone

[keystone_authtoken]

auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = NOVA_PASS
```

Tại section [DEFAULT] cấu hình `my_ip` , là địa chỉ của node controller :

```sh
[DEFAULT]

my_ip=IP_NODE_CONTROLLER
```

Tại section [DEFAULT] enable networking service :

```sh
[DEFAULT]

use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
```

Tại section [vnc] cấu hình VNC proxy để quản lý IP của controller node :

```sh
[vnc]

vncserver_listen = $my_ip
vncserver_proxyclient_address = $my_ip
```

Tại section [glance] chỉnh sửa đường dẫn của API image service :

```sh
[glance]

api_servers = http://controller:9292
```

Tại section [oslo_concurrency] cấu hình lock path :

```sh
[oslo_concurrency]

lock_path = /var/lib/nova/tmp
```

- Sync DB :

```sh
su -s /bin/sh -c "nova-manage api_db sync" nova
su -s /bin/sh -c "nova-manage db sync" nova
```

- Restart lại các dịch vụ :

```sh
service nova-api restart
service nova-consoleauth restart
service nova-scheduler restart
service nova-conductor restart
service nova-novncproxy restart
```

### 2. Trên node compute .

- Cài đặt `nova-compute` :

```sh
apt install nova-compute
```

- Dùng trình soạn thảo `vi` mở file cấu hình `/etc/nova/nova.conf` :

```sh
vi /etc/nova/nova.conf
```

- Chỉnh sửa lại file cấu hình như sau :

Tại section [DEFAULT] cấu hình truy cập RabbitMQ :

```sh
[DEFAULT]

transport_url = rabbit://openstack:RABBIT_PASS@controller
```

Tại section [DEFAULT] và [keystone_authtoken] cấu hình dịch vụ identity :

```sh
[DEFAULT]

auth_strategy = keystone

[keystone_authtoken]

auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = NOVA_PASS
```

Tại section [DEFAULT] cấu hình lựa chọn `my_ip` , là địa chỉ của node compute :

```sh
[DEFAULT]

my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
```

Tại section[DEFAULT] cấu hình cho enable networking service :

```sh
[DEFAULT]

use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
```

Tại section [vnc] cấu hình remote console access :

```sh
[vnc]

enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://controller:6080/vnc_auto.html
```

Tại section [glance] cấu hình đường dẫn image service API :

```sh
[glance]

api_servers = http://controller:9292
```

Tại section [oslo_concurrency] cấu hình lock path :

```sh
[oslo_concurrency]

lock_path = /var/lib/nova/tmp
```

- Kiểm tra xem hardware có hỗ trợ ảo hóa hay không ?

```sh
egrep -c '(vmx|svm)' /proc/cpuinfo
```

Kết quả trả về là `1` tức là có , `0` tức là không hỗ trợ .

- Mở file `/etc/nova/nova-compute.conf` và cấu hình section `[libvirt]` như sau :

```sh
[libvirt]

virt_type = qemu
```

- Restart lại dịch vụ :

```sh
service nova-compute restart
```

### 3. Kiểm tra.

- Để kiểm tra xem Nova đã cài đặt thành công hay chưa chúng ta sử dụng lệnh sau :

```sh
nova service-list
```

- Kết quả thu được :

```sh
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| Id | Binary           | Host       | Zone     | Status  | State | Updated_at                 | Disabled Reason |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| 3  | nova-cert        | controller | internal | enabled | up    | 2017-04-18T07:06:06.000000 | -               |
| 4  | nova-consoleauth | controller | internal | enabled | up    | 2017-04-18T07:06:05.000000 | -               |
| 5  | nova-scheduler   | controller | internal | enabled | up    | 2017-04-18T07:06:05.000000 | -               |
| 6  | nova-conductor   | controller | internal | enabled | up    | 2017-04-18T07:06:06.000000 | -               |
| 7  | nova-compute     | compute1   | nova     | enabled | up    | 2017-04-18T07:06:11.000000 | -               |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
```