# Cài đặt node compute1 

### 1. Cài đặt môi trường
- Cập nhật các gói phần mềm
  ```sh
  apt-get update
  ```
  
### 1.1 Cài đặt card mạng cho máy
- Dùng lệnh vi để sửa file `/etc/network/interfaces` với nội dung như sau. 
  ```sh
  auto ens3
  iface ens3 inet static
          address 10.10.10.191
          netmask 255.255.255.0


  auto ens4
  iface ens4 inet static
          address 172.16.69.191
          netmask 255.255.255.0
          gateway 172.16.69.1
          dns-nameservers 8.8.8.8


  auto ens5
  iface ens5 inet static
          address 10.10.20.191
          netmask 255.255.255.0
  ```
  
- Khởi động lại card mạng sau khi thiết lập IP tĩnh.
  ```sh
  ifdown -a && ifup -a
  ```
- Đăng nhập lại máy Compute1 với quyền root và thực hiện kiểm tra kết nối.
- Kiểm tra kết nối tới gateway và internet sau khi thiết lập xong.
  - ping gateway `ping -c 4 172.16.69.1`
  ```sh
  ~# ping -c 4 172.16.69.1
  PING 172.16.69.1 (172.16.69.1) 56(84) bytes of data.
  64 bytes from 172.16.69.1: icmp_seq=1 ttl=64 time=0.250 ms
  64 bytes from 172.16.69.1: icmp_seq=2 ttl=64 time=0.308 ms
  64 bytes from 172.16.69.1: icmp_seq=3 ttl=64 time=0.343 ms
  64 bytes from 172.16.69.1: icmp_seq=4 ttl=64 time=0.321 ms

  --- 172.16.69.1 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 2998ms
  rtt min/avg/max/mdev = 0.250/0.305/0.343/0.038 ms
  ```
  - ping ra ngoài internet `ping -c 4 google.com`
  ```sh
  ~# ping -c 4 google.com
  PING google.com (172.217.24.206) 56(84) bytes of data.
  64 bytes from hkg12s13-in-f14.1e100.net (172.217.24.206): icmp_seq=1 ttl=54 time=22.5 ms
  64 bytes from hkg12s13-in-f14.1e100.net (172.217.24.206): icmp_seq=2 ttl=54 time=22.6 ms
  64 bytes from hkg12s13-in-f14.1e100.net (172.217.24.206): icmp_seq=3 ttl=54 time=22.6 ms
  64 bytes from hkg12s13-in-f14.1e100.net (172.217.24.206): icmp_seq=4 ttl=54 time=22.6 ms

  --- google.com ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3004ms
  rtt min/avg/max/mdev = 22.574/22.632/22.666/0.187 ms
  ```
 
- Cấu hình hostname.
- Dùng vi sửa file `/etc/hostname` với tên là compute1.
  ```sh
  compute1
  ``` 
- Cập nhật file `/etc/hosts` để phân giải từ IP sang hostname và ngược lại, nội dung như sau
  ```sh
  127.0.0.1       localhost       compute1
  10.10.10.191    compute1
  10.10.10.190    controller
  ```
- Khởi động lại máy, sau đó đăng nhập vào với quyền root.
  ```sh
  init 6
  ```
  
### 1.2 Cài đặt NTP.
- 1. Cài gói chrony.
  ```sh
  apt install chrony -y
  ```
- 2. Mở file `/etc/chrony/chrony.conf` bằng vi và thêm vào dòng sau:
  - commnet dòng sau:
  ```sh
  #pool 2.debian.pool.ntp.org offline iburst
  ```
  - Thêm dòng sau:
  ```sh
  server controller iburst
  ```
- 3. Restart dịch vụ NTP
  ```sh
  service chrony restart
  ```
- 4. Kiểm tra lại hoạt động của NTP bằng lệnh dưới
  ```sh
  ~# chronyc sources
  210 Number of sources = 1
  MS Name/IP address         Stratum Poll Reach LastRx Last sample
  ===============================================================================
  ^* controller                    3   6    17    23    -10ns[+6000ns] +/-  248ms
  ```
  
### 1.3 Cài đặt repos để cài OpenStack OCATA
- 1. Cài đặt gói để cài OpenStack OCATA
  ```sh
  apt-get install software-properties-common -y
  add-apt-repository cloud-archive:ocata -y
  ```
- 2. Cập nhật các gói phần mềm
  ```sh
  apt -y update && apt -y dist-upgrade
  ```
- 3. Cài đặt các gói client của OpenStack.
  ```sh
  apt install python-openstackclient -y
  ```
- 4. Khởi động lại máy chủ
  ```sh
  init 6
  ```
  
### 2. Cài đặt nova-compute1
#### 2.1 Cài đặt và cấu hình
- 1. Cài đặt
  ```sh
  apt install nova-compute -y
  ```
- Sao lưu file cấu hình của dịch vụ nova-compute trước khi chỉnh sửa.
  ```sh
  cp /etc/nova/nova.conf /etc/nova/nova.conf.orig
  ```
- 2. Cấu hình 
- Trong [DEFAULT] section:
  ```sh
  [DEFAULT]
  #..
  transport_url = rabbit://openstack:Welcome123@controller
  my_ip = 10.10.10.191
  use_neutron = True
  firewall_driver = nova.virt.firewall.NoopFirewallDriver
  ```
- Trong [api] và [keystone_authtoken], cấu hình dịch vụ identity:
  ```sh
  [api]
  # ...
  auth_strategy = keystone

  [keystone_authtoken]
  # ...
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
- Trong [vnc] section:
  ```sh
  [vnc]
  # ...
  enabled = True
  vncserver_listen = 0.0.0.0
  vncserver_proxyclient_address = $my_ip
  novncproxy_base_url = http://controller:6080/vnc_auto.html
  ```
- Trong [glance]:
  ```sh
  [glance]
  # ...
  api_servers = http://controller:9292
  ```
- Trong [oslo_concurrency]:
  ```sh
  [oslo_concurrency]
  # ...
  lock_path = /var/lib/nova/tmp
  ```
- Trong [placement], cấu hình Placement API:
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
#### 2.2 Kết thúc bước cài đặt và cấu hình nova
- 1. Xác định xem compute1 node có hỗ trợ  ảo hóa hay không
  ```sh
  egrep -c '(vmx|svm)' /proc/cpuinfo
  ```
  - Nếu lệnh này trả về một giá trị là 1 hoặc lớn hơn, thì compute node này sẽ hỗ trợ ảo hóa.
  
- 2. Restart the Compute service:
  ```sh
  service nova-compute restart
  ```
  
- Đến đây đã cài đặt và cấu hình xong nova-compute trên node compute1. Quay lại node controller để tiếp tục cài đặt. Click [vào đây để quay lại controller](./install_controller.md#con)

<a name=neutron></a>
### 3. Cài đặt và cấu hình neutron
- 1 cài đặt các thành phần
  ```sh
  apt install neutron-linuxbridge-agent -y
  ```
- 2. Cấu hình
- Sao lưu file `/etc/neutron/neutron.conf` trước khi cài đặt
  ```sh
  cp /etc/neutron/neutron.conf /etc/neutron/neutron.conf.orig
  ```
- Trong [database] section, comment hết các connection
  ```sh
  #connection = sqlite:////var/lib/neutron/neutron.sqlite
  ```
- Trong [DEFAULT] section:
  ```sh
  auth_strategy = keystone
  transport_url = rabbit://openstack:Welcome123@controller
  ```
- Trong [keystone_authtoken] section:
  ```sh
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = neutron
  password = Welcome123
  ```
- Cấu hình Linux bridge agent
- Sao lưu file `/etc/neutron/plugins/ml2/linuxbridge_agent.ini`
  ```sh
  cp /etc/neutron/plugins/ml2/linuxbridge_agent.ini /etc/neutron/plugins/ml2/linuxbridge_agent.ini.orig
  ```
- Trong [linux_bridge] section:
  ```sh
  physical_interface_mappings = provider:ens4
  ```
- Trong [vxlan] section:
  ```sh
  enable_vxlan = true
  local_ip = 10.10.10.191
  l2_population = true
  ```
- Trong [securitygroup] section:
  ```sh
  enable_security_group = true
  firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
  ```

- **Cấu hình dịch vụ compute sử dụng dịch vụ network**
- Sửa file `/etc/nova/nova.conf`
- Trong [neutron] section:
  ```sh
  url = http://controller:9696
  auth_url = http://controller:35357
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  region_name = RegionOne
  project_name = service
  username = neutron
  password = Welcome123
  ```

- Kết thúc cài đặt
- Restart nova-compute
  ```sh
  service nova-compute restart
  ```
- Restart Linux bridge agent:
  ```sh
  service neutron-linuxbridge-agent restart
  ```

- Quay lại node controller để kiểm lại cài đặt neutron [tại đây](./install_controller.md#end).