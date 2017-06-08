# Cài đặt CInder , tạo volume và launch instane bằng volume đó.

====

#   MỤC LỤC.

[1. Cài đặt Cinder.](#caidat)

[2. Tạo volume và launch instane.](#instane)

===


<a name="caidat"></a>
## 1. Cài đặt Cinder trên một node riêng.

- Lưu ý : Trên mô hình phải được cài đặt sẵn OpenStack , nếu chưa có tham khảo tại [đây](https://github.com/congto/OpenStack-Mitaka-Scripts/tree/master/OPS-Mitaka-LB-Ubuntu)

### 1.1. Mô hình.

![mohinh](/images/cinder/mohinh.png)

### Phân hoạch địa chỉ IP và yêu cầu phần cứng đối với máy chủ:

![table-phanhoach](/images/cinder/mohinh-re.png)

### Trên Node Cinder thiết lập điah chỉ IP và hostname

- Dùng trình soạn thảo `vi` để mở file cấu hình interface network tiến hành thiết lập IP cho node Cinder :

```sh
vi /etc/network/interfaces
```

- Sửa lại file cấu hình như sau :

```sh
auto lo
iface lo inet loopback

# EXT NETWORK
auto eth0
iface eth0 inet static
address 172.16.1.130
netmask 255.255.255.0
gateway 172.16.1.1
dns-nameservers 8.8.8.8

# MGNT NETWORK
auto eth1
iface eth1 inet static
address 10.10.10.130
netmask 255.255.255.0

```

- Lưu lại file cấu hình và tiến hành yêu cầu phát phát lại địa chỉ IP :

```sh
ifdown -a && ifup -a
```

- Thiết lập file hosts :

```sh
vi /etc/hosts
```

- Sau đó chỉnh sửa lại file cấu hình như sau :

```sh
127.0.0.1       localhost cinder
10.10.10.10    controller
10.10.10.20   compute1
10.10.10.130 cinder
```

- Chỉnh sửa file hostname :

```sh
vi /etc/hostname
```

- Sửa lại file cấu hình thành :

```sh
cinder
```

- Reboot lại máy chủ để lấy cấu hình mới :

```sh
init 6
```

### 1.2. Cài đặt.

- Ở đây mình chỉ tiến hành cài node Cinder, mặc định là OpenStack đã có và chúng ta chỉ cài thêm dịch vụ lưu trữ Block Storage (Cinder) , nếu chưa có OpenStack có thể xem tại [đây](https://github.com/congto/OpenStack-Mitaka-Scripts/tree/master/OPS-Mitaka-LB-Ubuntu/scripts) để đồng bộ với mô hình cài node cinder .

### Trên Node Controller :

- Tạo cơ sở dữ liệu cho Cinder :

Truy cập vào cơ sở dữ liệu thông qua `root`

```sh
mysql -u root -p
```

Tạo `cinder` database :

```sh
CREATE DATABASE cinder;
```

Cấp quyền truy cập cơ sở dữ liệu :

```sh
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' \
  IDENTIFIED BY 'CINDER_DBPASS';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' \
  IDENTIFIED BY 'CINDER_DBPASS';
```

Thay đổi lại CINDER_PASS thành password mà chúng ta muốn đặt.

Thoát khỏi database :

```sh
exit;
```

- Chạy source admin-openrc để có quyền truy cập vào các lệnh CLI của quản trị viên :

```sh
. admin-openrc
```

- Tạo thông tin đăng nhập dịch vụ :

Tạo `cinder` user :

```sh
openstack user create --domain default --password-prompt cinder
User Password:
Repeat User Password:
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | e0353a670a9e496da891347c589539e9 |
| enabled   | True                             |
| id        | bb279f8ffc444637af38811a5e1f0562 |
| name      | cinder                           |
+-----------+----------------------------------+
```

Thêm role admin vào cinder user :

```sh
openstack role add --project service --user cinder admin
```

Tạo các entities cinder và cinderv2 :

```sh
openstack service create --name cinder \
  --description "OpenStack Block Storage" volume
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Block Storage          |
| enabled     | True                             |
| id          | ab3bbbef780845a1a283490d281e7fda |
| name        | cinder                           |
| type        | volume                           |
+-------------+----------------------------------+
```

```sh
openstack service create --name cinderv2 \
  --description "OpenStack Block Storage" volumev2
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Block Storage          |
| enabled     | True                             |
| id          | eb9fd245bdbc414695952e93f29fe3ac |
| name        | cinderv2                         |
| type        | volumev2                         |
+-------------+----------------------------------+
```

Tạo các enpoint cho Cinder :


```sh
openstack endpoint create --region RegionOne \
  volume public http://controller:8776/v1/%\(tenant_id\)s
  +--------------+-----------------------------------------+
  | Field        | Value                                   |
  +--------------+-----------------------------------------+
  | enabled      | True                                    |
  | id           | 03fa2c90153546c295bf30ca86b1344b        |
  | interface    | public                                  |
  | region       | RegionOne                               |
  | region_id    | RegionOne                               |
  | service_id   | ab3bbbef780845a1a283490d281e7fda        |
  | service_name | cinder                                  |
  | service_type | volume                                  |
  | url          | http://controller:8776/v1/%(tenant_id)s |
  +--------------+-----------------------------------------+

openstack endpoint create --region RegionOne \
  volume internal http://controller:8776/v1/%\(tenant_id\)s
  +--------------+-----------------------------------------+
  | Field        | Value                                   |
  +--------------+-----------------------------------------+
  | enabled      | True                                    |
  | id           | 94f684395d1b41068c70e4ecb11364b2        |
  | interface    | internal                                |
  | region       | RegionOne                               |
  | region_id    | RegionOne                               |
  | service_id   | ab3bbbef780845a1a283490d281e7fda        |
  | service_name | cinder                                  |
  | service_type | volume                                  |
  | url          | http://controller:8776/v1/%(tenant_id)s |
  +--------------+-----------------------------------------+

openstack endpoint create --region RegionOne \
  volume admin http://controller:8776/v1/%\(tenant_id\)s
  +--------------+-----------------------------------------+
  | Field        | Value                                   |
  +--------------+-----------------------------------------+
  | enabled      | True                                    |
  | id           | 4511c28a0f9840c78bacb25f10f62c98        |
  | interface    | admin                                   |
  | region       | RegionOne                               |
  | region_id    | RegionOne                               |
  | service_id   | ab3bbbef780845a1a283490d281e7fda        |
  | service_name | cinder                                  |
  | service_type | volume                                  |
  | url          | http://controller:8776/v1/%(tenant_id)s |
  +--------------+-----------------------------------------+
```

```sh
openstack endpoint create --region RegionOne \
  volumev2 public http://controller:8776/v2/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | 513e73819e14460fb904163f41ef3759        |
| interface    | public                                  |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | eb9fd245bdbc414695952e93f29fe3ac        |
| service_name | cinderv2                                |
| service_type | volumev2                                |
| url          | http://controller:8776/v2/%(tenant_id)s |
+--------------+-----------------------------------------+

openstack endpoint create --region RegionOne \
  volumev2 internal http://controller:8776/v2/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | 6436a8a23d014cfdb69c586eff146a32        |
| interface    | internal                                |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | eb9fd245bdbc414695952e93f29fe3ac        |
| service_name | cinderv2                                |
| service_type | volumev2                                |
| url          | http://controller:8776/v2/%(tenant_id)s |
+--------------+-----------------------------------------+

openstack endpoint create --region RegionOne \
  volumev2 admin http://controller:8776/v2/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | e652cf84dd334f359ae9b045a2c91d96        |
| interface    | admin                                   |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | eb9fd245bdbc414695952e93f29fe3ac        |
| service_name | cinderv2                                |
| service_type | volumev2                                |
| url          | http://controller:8776/v2/%(tenant_id)s |
+--------------+-----------------------------------------+
```

- Cài đặt và cấu hình các thành phần :

Cài đặt các gói dịch vụ :

```sh
apt-get install cinder-api cinder-scheduler
```

- Sửa file `/etc/cinder/cinder.conf` như sau :

Trong section [database] cấu hình truy cập cơ sở dữ liệu :

```sh
[database]
...
connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder
```

Thay thế CINDER_PASS bằng password mà chúng ta đã tạo ở trên.

Trong section [DEFAULT] và [oslo_messaging_rabbit] cấu hình truy cập RabbitMQ :

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

Thay thế CINDER_PASS bằng password của RabbitMQ.

Trong section [DEFAULT] và [keystone_authtoken] cấu hình dịch vụ xác thực :

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
username = cinder
password = CINDER_PASS
```

Thay thế CINDER_PASS thành password mà chúng ta đã tạo ở trên.

Trong section [DEFAULT] cấu hình `my_ip` sử dụng IP của controller node :

```sh
[DEFAULT]
...
my_ip = 10.0.0.11
```

Trong section [oslo_concurrency] cấu hình lock path :

```sh
[oslo_concurrency]
...
lock_path = /var/lib/cinder/tmp
```

- Đồng bộ dữ liệu Block Storage :

```sh
su -s /bin/sh -c "cinder-manage db sync" cinder
```

- Cuối cùng :

Khởi động lại Compute API service :

```sh
service nova-api restart
```

Khởi động lại dịch vụ Block Storage  :

```sh
service cinder-scheduler restart
service cinder-api restart
```

### Trên node compute :

- Sửa file cấu hình `/etc/nova/nova.conf` như sau :

```sh
[cinder]
os_region_name = RegionOne
```

### Trên Node Cinder .

- Thực hiện thêm repo OpenStack :

```sh
 apt-get install software-properties-common -y
 add-apt-repository cloud-archive:mitaka -y
```

- Cập nhật lại các gói phần mềm :

```sh
 apt-get -y update && apt-get -y dist-upgrade
```

- Cài đặt LVM

```sh
apt-get install lvm2
```

- Tạo Physical volume :

```sh
# pvcreate /dev/sdb
Physical volume "/dev/sdb" successfully created
```

- Tạo volume group `cinder-volumes`

```sh
# vgcreate cinder-volumes /dev/sdb
Volume group "cinder-volumes" successfully created
```

- Theo mặc định công cụ quét của LVM sẽ quét toàn bộ thư mục /dev cho các thiết bị lưu trữ khối, dó đó chúng ta cần cấu hình lại 
cấu hình mặc định này để LVm chỉ quét những ở thư mục mà chúng ta cấu hình và cho phép tạo volume trên đó :

- Mở file cấu hình `/etc/lvm/lvm.conf` :


```sh
vi /etc/lvm/lvm.conf
```

- Tìm đến dòng `filter = ` và sửa lại như sau :

```sh
filter = [ "a/sdb/", "r/.*/"]
```

- cài đặt và cấu hình các dịch vụ thành phần :

```sh
apt-get install -y cinder-volume python-mysqldb
```

- Mở file `/etc/cinder/cinder.conf` và sửa lại như sau :

Trong section [database] cấu hình truy cập cơ sở dữ liệu :

```sh
[database]
...
connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder
```

Thay thế CINDER_PASS bằng mật khẩu Cinder.

Trong section [DEFAULT] và [oslo_messaging_rabbit] cấu hình RabbitMQ :


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

Thay thế RABBIT_PASS bằng mật khẩu đã chọn cho tài khoản openstack trong RabbitMQ.

Trong section [DEFAULT] và [keystone_authtoken] cấu hình truy cập dịch vụ xác thực :

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
username = cinder
password = CINDER_PASS
```

Thay thế CINDER_DBPASS bằng mật khẩu của Cinder.

Trong section [DEFAULT] sửa lại tùy chọn `my_ip` :

```sh
[DEFAULT]
...
my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
```

Thay thế `MANAGEMENT_INTERFACE_IP_ADDRESS` bằng địa chỉ của Cinder node.

Trong section LVM , cấu hình LVM backend với LVM driver, `cinder-volumes` volume group, iCSI protocol và dịch vụ iSCSI thích hợp :

```sh
[lvm]
...
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm
```

Trong section [DEFAULT] , enable LVM back-end :

```sh
[DEFAULT]
...
enabled_backends = lvm
```

Trong section [DEFAULT] cấu hình đường dẫn của image identity service API :

```sh
[DEFAULT]
...
glance_api_servers = http://controller:9292
```

Trong section [oslo_concurrency] cấu hình lock path :

```sh
[oslo_concurrency]
...
lock_path = /var/lib/cinder/tmp
```

- Cuối cùng chúng ta restart lại dịch vụ Block Storage bao gồm :

```sh
service tgt restart
service cinder-volume restart
```

<a name="instane"></a>
## 2. Tạo volume và launch instane :

- Kiểm tra các dịch vụ để kết nối với nhau thành công hay chưa :

![cinder-service](/images/cinder/cinder-service.png)

- Đăng nhập vào OpenStack từ Dashboard :

![dashboard](/images/cinder/dashboard.png)

- Chọn Project => Compute => volumes

![volume](/images/cinder/volume.png)

- Chọn Create Volume :

![create-volume](/images/cinder/create-volume.png)

- Nhập thông tin cần thiết để tạo volume mới :

![volume-properties](/images/cinder/volume-properties.png)

- Nếu tạo volume thành công chúng ta sẽ nhận được trạng thái như sau :

![create-success](/images/cinder/create-success.png)

- Sau khi tạo Volume chúng ta vào Project => Compute => Install để tiến hành launch instane bằng volume vừa mới tạo :

![instane](/images/cinder/instane.png)

- Chọn Launch Instane để tạo một VM mới :

![launch-instane](/images/cinder/launch-instane.png)

- Tại Details chọn tên đặt cho VM :

![details](/images/cinder/details.png)

- Tại phần Source chọn `Boot Source` là volume rồi chọn Volume vừa tạo :

![source](/images/cinder/source.png)

- Tạo phần Flavors chọn tùy chọn đầu tiên :

![flavor](/images/cinder/flavor.png)

- Tại phần network chọn selservice , sau đó ấn Launch Instane để tiến hành tạo Instane mới 

- Sau khi Lauch Instane xong tiến hành Start Instane và chờ 1 lúc để thấy kết quả :

![vm](/images/cinder/vm.png)



# Tham Khảo :

- https://docs.openstack.org/mitaka/install-guide-ubuntu/cinder-storage-install.html
- http://netapp.github.io/openstack-deploy-ops-guide/icehouse/content/section_cinder-processes.html