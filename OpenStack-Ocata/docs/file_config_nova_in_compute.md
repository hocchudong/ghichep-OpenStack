# File cấu hình nova

## Sau đây là các dòng cấu hình cơ bản của nova trên node compute

- File cấu hình `/etc/nova/nova.conf`

- Cấu hình truy cập RabbitMQ. Ở trong section [DEFAULT]
  
  ```sh
  [DEFAULT]
  # ...
  transport_url = rabbit://openstack:RABBIT_PASS@controller
  ```
  
  - `RABBIT_PASS` là mật khẩu của tài khoản `openstack` trong RabbitMQ. Cấu hình truy cập RabbitMQ ở trên node controller.
  
- Cấu hình truy cập đến dịch vụ Identity (keystone). Cũng tương tự như trên node controller.

  ```sh
  [api]
  # ...
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
  my_ip = 10.10.10.191
  ```
- Enable hỗ trợ dịch vụ Networking.
  
  ```sh
  [DEFAULT]
  # ...
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  ```
  
- Trong [vnc] section, cấu hình VNC proxy để sử dụng địa chỉ ip của interface quản lý của node controller.
  
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
  
- Trên đây là một số ghi chép về file cấu hình của nova trên node compute. Bạn có thể tham khảo thêm về ghi chép file cấu hình của nova trên node controller [tại đây](./file_config_nova_in_controller.md). 