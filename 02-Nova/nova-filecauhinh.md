# Giải thích file cấu hình nova.conf

## 1. File cấu hình nova.conf 

```sh
[DEFAULT]
dhcpbridge_flagfile=/etc/nova/nova.conf
dhcpbridge=/usr/bin/nova-dhcpbridge
logdir=/var/log/nova
state_path=/var/lib/nova
lock_path=/var/lock/nova
force_dhcp_release=True
libvirt_use_virtio_for_bridges=True
verbose=True
ec2_private_dns_show_ip=True
api_paste_config=/etc/nova/api-paste.ini
enabled_apis=ec2,osapi_compute,metadata
rpc_backend = rabbit
auth_strategy = keystone
my_ip = 10.10.10.20
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver


[oslo_messaging_rabbit]
rabbit_host = 10.10.10.10
rabbit_userid = openstack
rabbit_password = Anhdat96


[keystone_authtoken]
auth_uri = http://10.10.10.10:5000
auth_url = http://10.10.10.10:35357
memcached_servers = 10.10.10.10:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = Anhdat96


[vnc]
enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://172.16.1.128:6080/vnc_auto.html


[glance]
api_servers = http://10.10.10.10:9292


[oslo_concurrency]
lock_path = /var/lib/nova/tmp


[neutron]
url = http://10.10.10.10:9696
auth_url = http://10.10.10.10:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = Anhdat96

```

## 2. Giải thích file cấu hình .

### 2.1. Khai báo về Message Queue

```sh
[DEFAULT]
...
rpc_backend = rabbit

[oslo_messaging_rabbit]
...
rabbit_host = controller
rabbit_userid = openstack
rabbit_password = RABBIT_PASS
```

- rpc_backend = rabbit : Trình điều khiển message được sử dụng mặc định là rabbitMQ.
- rabbit_host = controller : IP(host) của RabbitMQ server (node Controller)
- rabbit_userid = openstack : User để kết nối với RabbitMQ server
- rabbit_password = RABBIT_PASS : Password của RabbitMQ server

### 2.2. Khai báo về xác thực Keystone.

```sh
[DEFAULT]
...
auth_strategy = keystone

[keystone_authtoken]
...
auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = NOVA_PASS
```

- auth_strategy = keystone : Cấu hình sử dụng keystone để xác thực. Hỗ trợ noauth và deprecated
- auth_uri = http://controller:5000 : Cấu hình enpoint Identity service
- auth_url = http://controller:5000 : URL để xác thực Identity service
- memcached_servers = controller:11211 : Địa chỉ Memcache-server
- auth_type = password : Hình thức xác thực sử dụng password
- project_domain_name = default : Chỉ định project domain name openstack
- user_domain_name = default : Chỉ định user domain name openstack
- project_name = service : Chỉ định project name openstack
- username = nova : Chỉ định username của nova
- password = NOVA_PASS : Chỉ đinh pass của nova

### 2.3. IP management 

```sh
[DEFAULT]
...
my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
```

- my_ip = 192.168.11.12 : Địa chỉ IP management của Compute node

### 2.4. Cấu hình Networking .

```sh
[DEFAULT]
...
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
```

- use_neutron = True : Cấu hình xác nhận sử dụng Neutron Networking
- firewall_driver = nova.virt.firewall.NoopFirewallDriver : Mặc định Compute sử dụng một internal firewall service cho tới khi Networking cũng bao gồm một 
firewall service , chúng ta phải disable Compute firewall service bằng cách sử dụng Friver `nova.virt.firewall.NoopFirewallDriver`

### 2.5. Cấu hình VNC.

```sh
[vnc]
...
enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://controller:6080/vnc_auto.html
```
- enabled = True : Cho phép sử dụng vnc.
- vncserver_listen = 0.0.0.0 : Cấu hình địa chỉ lắng nghe của vnc server (ở đây là trên tất cả các địa chỉ).
- vncserver_proxyclient_address = $my_ip : Cấu hình proxy lắng nghe trên IP của compute node.
- novncproxy_base_url = http://controller:6080/vnc_auto.html : Cấu hình đường dẫn nơi chúng ta có thể sử dụng trình duyệt web để chúng ta có thể remote access sonsole 
VM trên node Compute.

### 2.6. Cấu hình Glane API .

```sh
[glance]
...
api_servers = http://controller:9292
```

- api_servers = http://controller:9292 : Cấu hình enpoint của Glane.

### 2.7. cấu hình lock_path :

```sh
[oslo_concurrency]
...
lock_path = /var/lib/nova/tmp
```

- Thư mục sử dụng cho các tệp khóa , mặc định là thư mục temp