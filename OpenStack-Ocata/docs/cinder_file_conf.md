# File cấu hình của cinder

## File cấu hình của cinder trên node controller
- file cấu hình của cinder `/etc/cinder/cinder.conf`

  ```sh
  [DEFAULT]
  rootwrap_config = /etc/cinder/rootwrap.conf
  api_paste_confg = /etc/cinder/api-paste.ini
  iscsi_helper = tgtadm
  volume_name_template = volume-%s
  volume_group = cinder-volumes
  verbose = True
  auth_strategy = keystone
  state_path = /var/lib/cinder
  lock_path = /var/lock/cinder
  volumes_dir = /var/lib/cinder/volumes
  transport_url = rabbit://openstack:Welcome123@controller
  my_ip = 10.10.10.190
  
  [database]
  connection = mysql+pymysql://cinder:Welcome123@controller/cinder
  
  [keystone_authtoken]
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = cinder
  password = Welcome123
  
  [oslo_concurrency]
  lock_path = /var/lib/cinder/tmp
  ```
  
- Giải thích file cấu hình
- Trong [database] section, cấu hình truy cập database:

  ```sh
  [database]
  # ...
  connection = mysql+pymysql://cinder:Welcome123@controller/cinder
  ```
  
  - Welcome123 là mật khẩu của user `cinder` để truy cập vào database `cinder`
  
- Trong [DEFAULT] section, cấu hình truy cập RabbitMQ

  ```sh
  [DEFAULT]
  # ...
  transport_url = rabbit://openstack:Welcome123@controller
  ```
  
- Trong [DEFAULT] và [keystone_authtoken] sections, cấu hình truy cập dịch vụ Identity:

  ```sh
  [DEFAULT]
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
  username = cinder
  password = Welcome123
  ```
  
  - auth_strategy = keystone : Cấu hình sử dụng keystone để xác thực. 
  - auth_uri = http://controller:5000 : Cấu hình enpoint Identity service 
  - auth_url = http://controller:35357 : URL để xác thực Identity service
  - memcached_servers = controller:11211 : Địa chỉ Memcache-server
  - auth_type = password : Hình thức xác thực sử dụng password
  - project_domain_name = default : Chỉ định project domain name openstack
  - user_domain_name = default : Chỉ định user domain name openstack
  - project_name = service : Chỉ định project name openstack
  - username = cinder : Chỉ định username của cinder
  - password = Welcome123 : Chỉ đinh pass của nova
  
- Trong [DEFAULT] section, cấu hình my_ip option để sử dụng địa chỉ management interface IP của node controller:

  ```sh
  [DEFAULT]
  # ...
  my_ip = 10.10.10.190
  ```
  
- Trong [oslo_concurrency] section, cấu hình lock path:

  ```sh
  [oslo_concurrency]
  # ...
  lock_path = /var/lib/cinder/tmp
  ```

## File cấu hình của cinder trên node cinder
- file cấu hình của cinder `/etc/cinder/cinder.conf`

  ```sh
  [DEFAULT]
  rootwrap_config = /etc/cinder/rootwrap.conf
  api_paste_confg = /etc/cinder/api-paste.ini
  iscsi_helper = tgtadm
  volume_name_template = volume-%s
  volume_group = cinder-volumes
  verbose = True
  auth_strategy = keystone
  state_path = /var/lib/cinder
  lock_path = /var/lock/cinder
  volumes_dir = /var/lib/cinder/volumes

  transport_url = rabbit://openstack:Welcome123@controller
  my_ip = 10.10.10.192
  enabled_backends = lvm
  glance_api_servers = http://controller:9292

  [database]
  # ...
  connection = mysql+pymysql://cinder:Welcome123@controller/cinder

  [keystone_authtoken]
  # ...
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = cinder
  password = Welcome123

  [lvm]
  # ...
  volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
  volume_group = cinder-volumes
  iscsi_protocol = iscsi
  iscsi_helper = tgtadm

  [oslo_concurrency]
  # ...
  lock_path = /var/lib/cinder/tmp
  ```
