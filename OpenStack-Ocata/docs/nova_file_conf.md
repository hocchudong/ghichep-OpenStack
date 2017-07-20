# File cấu hình nova

## 1. Sau đây là các dòng cấu hình cơ bản của nova trên node controller

- File cấu hình mặc định là `/etc/nova/nova.conf`

  ```sh
  [DEFAULT]
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  my_ip = 10.10.10.190
  transport_url = rabbit://openstack:Welcome123@controller
  dhcpbridge_flagfile=/etc/nova/nova.conf
  dhcpbridge=/usr/bin/nova-dhcpbridge
  force_dhcp_release=true
  state_path=/var/lib/nova
  enabled_apis=osapi_compute,metadata
  log_dir=/var/log/nova
  
  
  [api]
  auth_strategy = keystone
  
  
  [api_database]
  connection = mysql+pymysql://nova:Welcome123@controller/nova_api
  
  
  [cells]
  enable=False
  
  
  [cinder]
  os_region_name = RegionOne
  
  
  [database]
  connection = mysql+pymysql://nova:Welcome123@controller/nova
  
  
  [glance]
  api_servers = http://controller:9292
  
  
  [keystone_authtoken]
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = nova
  password = Welcome123
  
  
  [neutron]
  url = http://controller:9696
  auth_url = http://controller:35357
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  region_name = RegionOne
  project_name = service
  username = neutron
  password = Welcome123
  service_metadata_proxy = true
  metadata_proxy_shared_secret = Welcome123
  
  
  [oslo_concurrency]
  lock_path = /var/lib/nova/tmp
  
  
  [placement]
  os_region_name = RegionOne
  project_domain_name = Default
  project_name = service
  auth_type = password
  user_domain_name = Default
  auth_url = http://controller:35357/v3
  username = placement
  password = Welcome123
  
  
  [vnc]
  enabled = true
  vncserver_listen = $my_ip
  vncserver_proxyclient_address = $my_ip
  
  ```
  
- 1. Cấu hình truy cập database. Ở trong section `[api_database]` và `[database]`.

  ```sh
  [api_database]
  # ...
  connection = mysql+pymysql://nova:Welcome123@controller/nova_api

  [database]
  # ...
  connection = mysql+pymysql://nova:Welcome123@controller/nova
  ```
  
  - `Welcome123` là mật khẩu của user nova được cấp phát cho phép truy cập vào các database của dịch vụ compute.
  
- 2. Cấu hình truy cập RabbitMQ. Ở trong section [DEFAULT]
  
  ```sh
  [DEFAULT]
  # ...
  transport_url = rabbit://openstack:Welcome123@controller
  ```
  
  - `Welcome123` là mật khẩu của tài khoản `openstack` trong RabbitMQ.
  
- 3. Cấu hình truy cập đến dịch vụ Identity (keystone).

  ```sh
  [api]
  # ...
  # Cấu hình này để xác định rõ chiến lược xác thực: sử dụng keystone hoặc noathu2
  # noathu2: được thiết kế chỉ để testing, vì nó không thực sự kiểm tra cridential. Noauth2 cung cấp một cridential có tính quản trị chi khi nếu có admin được chỉ định bằng username
  # Chúng ta sử dụng keystone cho việc xác thực.
  auth_strategy = keystone

  [keystone_authtoken]
  # ...
  # Chúng ta phải cung cấp thông tin xác thực cho user nova để keystone thực hiện xác thực. NOVA_PASS là mật khẩu của user nova
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = nova
  password = Welcome123
  ```
  
- 4. Cấu hình địa chỉ ip của interface dùng để quản lý trên node controller. Dòng cấu hình này ở trong section [DEFAULT].

  ```sh
  [DEFAULT]
  # ...
  # Ở đây là địa chỉ IP của interface mà trong hệ thống dùng để quản lý.
  my_ip = 10.10.10.190
  ```
  
- 5. Enable hỗ trợ dịch vụ Networking.
  
  ```sh
  [DEFAULT]
  # ...
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  ```
  - Mặc định, Compute sử dụng một firewall driver nội bộ. Từ khi dịch vụ Networking bao gồm một firewall driver, bạn phải disable nó bằng cách sử dụng `nova.virt.firewall.NoopFirewallDriver firewall driver.`

- 6. Trong [vnc] section, cấu hình VNC proxy để sử dụng địa chỉ ip của interface quản lý của node controller.
  
  ```sh
  [vnc]
  # Virtual Network Computer (VNC) có thể được sử dụng để cung cấp remote desktop console truy cấp đến các VMs cho các tenants hoặc administrators.
  enabled = true
  
  # ...
  # Địa chỉ IP hoặc hostname mà trên đó một VM sẽ lắng nghe yêu cầu kết nối VNC trên node này (ở đây là node controller)
  vncserver_listen = $my_ip
  
  # địa chỉ IP hoặc hostname riêng tư, nội bộ của VNC console proxy.
  # VNC proxy là một thành phần openstack mà cho phép dịch vụ compute người dùng truy cấp tới các VMs của họ thông qua VNC clients.
  vncserver_proxyclient_address = $my_ip
  ```
  
- 7. Trong [glance] section, cấu hình vị trí API của dịch vụ Image.

  ```sh
  [glance]
  # ...
  api_servers = http://controller:9292
  ```
  - cung cấp endpoint api đến dịch vụ glance.
  
- 8. Trong [oslo_concurrency] section, cấu hình lock path:

  ```sh
  [oslo_concurrency]
  # ...
  lock_path = /var/lib/nova/tmp
  ```
  
- 9. Trong [placement] section, cấu hình Placement API:
  
  ```sh
  [placement]
  # ...
  os_region_name = RegionOne
  project_domain_name = Default
  project_name = service
  auth_type = password
  user_domain_name = Default
  auth_url = http://controller:35357/v3
  username = placement
  password = Welcome123
  ```
  - `Welcome123` là mật khẩu của user placement trong dịch vụ Identity.
  
- 10. Khai báo tên region của node cinder đang sử dụng.

  ```sh
  [cinder]
  os_region_name = RegionOne
  ```
## 2. Sau đây là các dòng cấu hình cơ bản của nova trên node compute

- File cấu hình `/etc/nova/nova.conf`

  ```sh
  [DEFAULT]
  transport_url = rabbit://openstack:Welcome123@controller
  my_ip = 10.10.10.191
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver

  dhcpbridge_flagfile=/etc/nova/nova.conf
  dhcpbridge=/usr/bin/nova-dhcpbridge
  force_dhcp_release=true
  state_path=/var/lib/nova
  enabled_apis=osapi_compute,metadata
  log_dir=/var/log/nova

  [api]
  auth_strategy = keystone

  [api_database]
  connection=sqlite:////var/lib/nova/nova.sqlite

  [glance]
  api_servers = http://controller:9292

  [keystone_authtoken]
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = nova
  password = Welcome123

  [neutron]
  url = http://controller:9696
  auth_url = http://controller:35357
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  region_name = RegionOne
  project_name = service
  username = neutron
  password = Welcome123

  [placement]
  os_region_name = RegionOne
  project_domain_name = Default
  project_name = service
  auth_type = password
  user_domain_name = Default
  auth_url = http://controller:35357/v3
  username = placement
  password = Welcome123

  [vnc]
  enabled = True
  vncserver_listen = 0.0.0.0
  vncserver_proxyclient_address = $my_ip
  novncproxy_base_url = http://172.16.69.190:6080/vnc_auto.html

  ```
- 1. Cấu hình truy cập RabbitMQ. Ở trong section [DEFAULT]
  
  ```sh
  [DEFAULT]
  # ...
  transport_url = rabbit://openstack:RABBIT_PASS@controller
  ```
  
  - `RABBIT_PASS` là mật khẩu của tài khoản `openstack` trong RabbitMQ. Cấu hình truy cập RabbitMQ ở trên node controller.
  
- 2. Cấu hình truy cập đến dịch vụ Identity (keystone). Cũng tương tự như trên node controller.

  ```sh
  [api]
  # ...
  auth_strategy = keystone

  [keystone_authtoken]
  # ...
  # Chúng ta phải cung cấp thông tin xác thực cho user nova để keystone thực hiện xác thực. Welcome123 là mật khẩu của user nova
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = nova
  password = Welcome123
  ```
  
- 3. Cấu hình địa chỉ ip của interface dùng để quản lý trên node controller. Dòng cấu hình này ở trong section [DEFAULT].

  ```sh
  [DEFAULT]
  # ...
  # Ở đây là địa chỉ IP của interface mà trong hệ thống dùng để quản lý.
  my_ip = 10.10.10.191
  ```
- 4. Enable hỗ trợ dịch vụ Networking.
  
  ```sh
  [DEFAULT]
  # ...
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  ```
  
- 5. Trong [vnc] section, cấu hình VNC proxy để sử dụng địa chỉ ip của interface quản lý của node controller.
  
  ```sh
  [vnc]
  # Virtual Network Computer (VNC) có thể được sử dụng để cung cấp remote desktop console truy cấp đến các VMs cho các tenants hoặc administrators.
  enabled = true
  
  # ...
  # Địa chỉ IP hoặc hostname mà trên đó một VM sẽ lắng nghe yêu cầu kết nối VNC trên node này (ở đây là node controller)
  # Thành phần server lắng nghe trên tất cả các địa chỉ IP.
  vncserver_listen = 0.0.0.0
  
  # địa chỉ IP hoặc hostname riêng tư, nội bộ của VNC console proxy.
  # VNC proxy là một thành phần openstack mà cho phép dịch vụ compute người dùng truy cấp tới các VMs của họ thông qua VNC clients.
  # Thành phần proxy chỉ lắng nghe trên địa chỉ IP của interface dùng để manage
  vncserver_proxyclient_address = $my_ip

  # Địa chỉ public của noVNC VNC console proxy
  novncproxy_base_url = http://172.16.69.190:6080/vnc_auto.html
  ```
- Còn 3 section: [glance], [glance], [placement] giống với cấu hình ở controller.