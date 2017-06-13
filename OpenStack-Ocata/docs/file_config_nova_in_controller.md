# File cấu hình nova

## Sau đây là các dòng cấu hình cơ bản của nova trên node controller

- File cấu hình mặc định là `/etc/nova/nova.conf`

- Cấu hình truy cập database. Ở trong section `[api_database]` và `[database]`.

  ```sh
  [api_database]
  # ...
  connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova_api

  [database]
  # ...
  connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova
  ```
  
  - `NOVA_DBPASS` là mật khẩu của user nova được cấp phát cho phép truy cập vào các database của dịch vụ compute.
  
- Cấu hình truy cập RabbitMQ. Ở trong section [DEFAULT]
  
  ```sh
  [DEFAULT]
  # ...
  transport_url = rabbit://openstack:RABBIT_PASS@controller
  ```
  
  - `RABBIT_PASS` là mật khẩu của tài khoản `openstack` trong RabbitMQ.
  
- Cấu hình truy cập đến dịch vụ Identity (keystone).

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
  password = NOVA_PASS
  ```
  
- Cấu hình địa chỉ ip của interface dùng để quản lý trên node controller. Dòng cấu hình này ở trong section [DEFAULT].

  ```sh
  [DEFAULT]
  # ...
  # Ở đây là địa chỉ IP của interface mà trong hệ thống dùng để quản lý.
  my_ip = 10.10.10.190
  ```
  
- Enable hỗ trợ dịch vụ Networking.
  
  ```sh
  [DEFAULT]
  # ...
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  ```
  - Mặc định, Compute sử dụng một firewall driver nội bộ. Từ khi dịch vụ Networking bao gồm một firewall driver, bạn phải disable nó bằng cách sử dụng `nova.virt.firewall.NoopFirewallDriver firewall driver.`

- Trong [vnc] section, cấu hình VNC proxy để sử dụng địa chỉ ip của interface quản lý của node controller.
  
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
  
- Trong [glance] section, cấu hình vị trí API của dịch vụ Image.

  ```sh
  [glance]
  # ...
  api_servers = http://controller:9292
  ```
  - cung cấp endpoint api đến dịch vụ glance.
  
- Trong [oslo_concurrency] section, cấu hình lock path:

  ```sh
  [oslo_concurrency]
  # ...
  lock_path = /var/lib/nova/tmp
  ```
  
- Trong [placement] section, cấu hình Placement API:
  
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
  password = PLACEMENT_PASS
  ```
  - `PLACEMENT_PASS` là mật khẩu của user placement trong dịch vụ Identity.
  
  
  
  
  
  
  
  
  
  
  
  