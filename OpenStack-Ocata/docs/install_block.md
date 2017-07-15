# Cài đặt dịch vụ Block storage

# Mô hình cài đặt hệ thống lab openstack 

  ![](../images/layoutnet.png)
  
# IP Planning cho hệ thống.

  ![](../images/IPBlock.png)
  
---

Sau khi thực hiện cài đặt xong node controller và compute1 theo đúng như mô hình và IP Planning như trên (Có thể tham khảo cài đặt [tại đây](./install.md). ).
Hướng dẫn này thực hiện cài đặt thêm Block Storage node


# Cài đặt trên node controller
## 1. Chuẩn bị môi trường

- Chỉnh sửa file `/etc/hosts`. Khai báo thêm node block
  - thêm dòng sau vào file `/etc/hosts`
  
  ```sh
  10.10.10.192    block1
  ```
---
- Trước khi cài đặt và cấu hình Block Storage service, bạn phải tạo 1 database, service credentials, và API endpoints.  
#### 1.1 Tạo database
- 1. Đăng nhập vào MariaDB

  ```sh
  mysql -u root -pWelcome123
  ```
  
- 2. Tạo database `cinder`

  ```sh
  CREATE DATABASE cinder;
  ```
  
- 3. Cấp quyền truy cập đến `cinder` database

  ```sh
  GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'Welcome123';
  
  GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'Welcome123';
  
  FLUSH PRIVILEGES;
  exit;
  ```
  
#### 1.2 tạo credentials cho dịch vụ
- Chạy script biến môi trường: `source admin-openrc`
- 1. Tạo `cinder` user:

  ```sh
  ~# openstack user create --domain default --password Welcome123 cinder
  
  +---------------------+----------------------------------+
  | Field               | Value                            |
  +---------------------+----------------------------------+
  | domain_id           | default                          |
  | enabled             | True                             |
  | id                  | da27ad422b414bb4b9159ce5f385d1b6 |
  | name                | cinder                           |
  | options             | {}                               |
  | password_expires_at | None                             |
  +---------------------+----------------------------------+
  ```
  
- 2. Thêm `admin` role cho `cinder` user:

  ```sh
  openstack role add --project service --user cinder admin
  ```

- 3. Kiểm tra lại xem cinder user có role gì:

  ```sh
  ~# openstack role list --user cinder --project service
  Listing assignments using role list is deprecated. Use role assignment list --user <user-name> --project <project-name> --names instead.
  +----------------------------------+-------+---------+--------+
  | ID                               | Name  | Project | User   |
  +----------------------------------+-------+---------+--------+
  | ec9157c203314df69c4f3805e3fec0e7 | admin | service | cinder |
  +----------------------------------+-------+---------+--------+
  ```
  
- 4. Tạo `cinderv2` và `cinderv3` service entities:

  ```sh
  ~# openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
  
  +-------------+----------------------------------+
  | Field       | Value                            |
  +-------------+----------------------------------+
  | description | OpenStack Block Storage          |
  | enabled     | True                             |
  | id          | 9b7c43ccbf88464487910d04e9443e9d |
  | name        | cinderv2                         |
  | type        | volumev2                         |
  +-------------+----------------------------------+
  ```
  
  ```sh
  ~# openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3
  
  +-------------+----------------------------------+
  | Field       | Value                            |
  +-------------+----------------------------------+
  | description | OpenStack Block Storage          |
  | enabled     | True                             |
  | id          | 0512f93bd37c45b88c090488af093e24 |
  | name        | cinderv3                         |
  | type        | volumev3                         |
  +-------------+----------------------------------+
  ```
  
#### 1.3 Tạo Block Storage service API endpoints:
- volumev2

  ```sh
  openstack endpoint create --region RegionOne \
  volumev2 public http://controller:8776/v2/%\(project_id\)s
  
  openstack endpoint create --region RegionOne \
  volumev2 internal http://controller:8776/v2/%\(project_id\)s
  
  openstack endpoint create --region RegionOne \
  volumev2 admin http://controller:8776/v2/%\(project_id\)s
  ```
  
- volumev3

  ```sh
  openstack endpoint create --region RegionOne \
  volumev3 public http://controller:8776/v3/%\(project_id\)s
  
  openstack endpoint create --region RegionOne \
  volumev3 internal http://controller:8776/v3/%\(project_id\)s
  
  openstack endpoint create --region RegionOne \
  volumev3 admin http://controller:8776/v3/%\(project_id\)s
  ```
  
## 2. Cài đặt và cấu hình các thành phần trên node controller
- 1. Cài đặt các gói:

  ```sh
  apt install cinder-api cinder-scheduler -y
  ```
  
- Sao lưu file cấu hình `/etc/cinder/cinder.conf` của cinder trước khi cấu hình

  ```sh
  cp /etc/cinder/cinder.conf /etc/cinder/cinder.conf.orig
  ```
  
- 2. Thực hiện cấu hình cinder
- Theo như quá trình mình cài đặt thì file cấu hình của cinder chỉ có 1 section - [DEFAULT]. Những section nào không có thì chỉ việc thêm vào file cấu hình là được.

- Trong `[database]` section, cấu hình truy cập database:

  ```sh
  [database]
  # ...
  connection = mysql+pymysql://cinder:Welcome123@controller/cinder
  ```
  
- Trong `[DEFAULT]` section, cấu hình truy cập RabbitMQ

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
  
- Trong [DEFAULT] section, cấu hình `my_ip` option để sử dụng địa chỉ **management interface IP** của node controller:

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

- Điền vào database của Block Storage:

  ```sh
  su -s /bin/sh -c "cinder-manage db sync" cinder
  ```
  
- 3. Cấu hình Compute để sử dụng Block Storage:

- Sửa file `/etc/nova/nova.conf`, sửa trong section [cinder] như sau:

  ```sh
  [cinder]
  os_region_name = RegionOne
  ```
  
- 4. Kết thúc cài đặt
- Restart dịch vụ Compute API:

  ```sh
  service nova-api restart
  ```

- Restart dịch vụ Block Storage:

  ```sh
  service cinder-scheduler restart
  service apache2 restart
  ```
  
## 2. Cài đặt trên node block

#### Cài đặt môi trường

- Cập nhật các gói phần mềm

  ```sh
  apt-get update
  ```
  
- 2.1 Cài đặt card mạng cho máy

- Dùng lệnh vi để sửa file /etc/network/interfaces với nội dung như sau.

  ```sh
  
  auto ens3
  iface ens3 inet static
          address 10.10.10.192
          netmask 255.255.255.0


  auto ens4
  iface ens4 inet static
          address 172.16.69.192
          netmask 255.255.255.0
          gateway 172.16.69.1
          dns-nameservers 8.8.8.8
  ```

- 2.2 Cấu hình phân giải tên.

- Sửa file `/etc/hosts` chứa nội dung như sau:

  ```sh
  127.0.0.1       localhost       block1

  10.10.10.190    controller

  10.10.10.191    compute1

  10.10.10.192    block1
  ```


- 2.3 Cài đặt `NTP service`:

  ```sh
  apt install chrony -y
  ```

- Sửa file `/etc/chrony/chrony.conf` và comment hoặc xóa tất cả dòng có chứa `server` và thêm dòng sau:

  ```sh
  server controller iburst
  ```
  
- Restart NTP service:

  ```sh
  service chrony restart
  ```
  
- 2.4 Thêm Openstack repository

  ```sh
  apt install software-properties-common -y
  add-apt-repository cloud-archive:ocata -y
  ```
  
- 2.5 Cập nhật các gói phần mềm
  
  ```sh
  apt -y update && apt -y dist-upgrade
  ```
  
- 2.6 Cài đặt các gói client của OpenStack.

  ```sh
  apt install python-openstackclient -y
  ```

## 2.7 Cài đặt các tiện ích hỗ trợ.

- 2.7.1. Cài đặt lvm2

  ```sh
  apt install lvm2 -y
  ```
  
- 2.7.2. Tạo LVM physical volume `/dev/vdb` (Bạn có thể kiểm tra lại ổ đĩa dùng để cấp volume, ở đây trên hệ thống của mình là ổ `/dev/vdb`)

  ```sh
  ~# pvcreate /dev/vdb
  
  Physical volume "/dev/vdb" successfully created
  ```
  
- 2.7.3 Tạo LVM volume group là `cinder-volumes`

  ```sh
  ~# vgcreate cinder-volumes /dev/vdb
  
  Volume group "cinder-volumes" successfully created
  ```
  
- Sửa file `/etc/lvm/lvm.conf`. Thêm dòng filter ở dưới vào section `devices`.

  ```sh
  devices {
  ....
  filter = ["a/vdb/", "r/.*/"]

  ```
  
- 2.7.4 Cài đặt các gói

  ```sh
  apt install cinder-volume -y
  ```
  
- Sửa file `/etc/cinder/cinder.conf` để cấu hình cinder:

- Những section nào không có thì bạn thêm mới vào

- Trong [database] section, cấu hình truy cập database:

  ```sh
  [database]
  # ...
  connection = mysql+pymysql://cinder:Welcome123@controller/cinder
  ```
  
- Trogn [DEFAULT] section, cấu hình truy cập RabbitMQ:

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
  
- Trong [DEFAULT] section, cấu hình tùy chọn my_ip:
  
  ```sh
  [DEFAULT]
  # ...
  my_ip = 10.10.10.192
  ```
  
- Trong [lvm] section, cấu hình LVM back end với LVM driver, cinder-volumes volume group, iSCSI protocol, và iSCSI service:

  ```sh
  [lvm]
  # ...
  volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
  volume_group = cinder-volumes
  iscsi_protocol = iscsi
  iscsi_helper = tgtadm  
  ```
  
- Trong [DEFAULT] section, enable the LVM back end:

  ```sh
  [DEFAULT]
  # ...
  enabled_backends = lvm
  ```
  
- Trong [DEFAULT] section, cấu hình vị trí của Image service API:

  ```sh
  [DEFAULT]
  # ...
  glance_api_servers = http://controller:9292  
  ```
  
- Trong [oslo_concurrency] section, cấu hình lock path:

  ```sh
  [oslo_concurrency]
  # ...
  lock_path = /var/lib/cinder/tmp  
  ```
  
---

- Kết thúc cài đặt

Restart the Block Storage volume service:

  ```sh
  service tgt restart
  service cinder-volume restart
  ```
  
- Kiểm tra lại cài đặt. Thực hiện kiểm tra trên node controller.

  ```sh
  ~# openstack volume service list
  +------------------+------------+------+---------+-------+----------------------------+
  | Binary           | Host       | Zone | Status  | State | Updated At                 |
  +------------------+------------+------+---------+-------+----------------------------+
  | cinder-scheduler | controller | nova | enabled | up    | 2017-07-13T16:51:16.000000 |
  | cinder-volume    | block1@lvm | nova | enabled | up    | 2017-07-13T16:51:09.000000 |
  +------------------+------------+------+---------+-------+----------------------------+
  ```