# Cài đặt CInder , tạo volume và launch instane bằng volume đó.

====

#   MỤC LỤC.

[1. Cài đặt Cinder.](#caidat)

[2. Tạo volume và launch instane.](#instane)

[3. Process Structure.](#process)


===


<a name="caidat"></a>
## 1. Cài đặt Cinder trên một node riêng.

### 1.1. Mô hình.

![mohinh](/images/cinder/mohinh.png)

- Cấu hình các máy :

```sh
- Gồm 3 máy chủ là : controller , compute và cinder.
- OS : Ubuntu server 14.04 64-bit.
- RAM : controller (4GB), compute (2GB), cinder (1GB).
- Máy gồm 2 NICs :
-- eth0 : sử dụng chế độ card NAT dùng để tải các gói cài đặt từ Internet.
-- eth1 : Sử dụng để quản trị các node trong mô hình OpenStack (dùng chế độ hostonly - vmnet1 của VMware).
- Thiết lập về ổ cứng :
-- controller : 1 HDD +20GB, 1 HDD + 40GB
-- compute : 1 HDD +20GB, 1 HDD + 80GB
-- cinder : 2 HDD (1 HDD 20GB + 1 HDD 100GB)
```

### Phân hoạch địa chỉ IP và yêu cầu phần cứng đối với máy chủ:

![table-phanhoach](table-phanhoach.png)

### Trên Node compute thiết lập điah chỉ IP và hostname

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


<a name="process"></a>
## 3. Process Structure.

- Chúng ta có 4 quy trình tạo nên Cinder Service :

|Process|mô tả|
|---------|-----|
|Cinder-api|là một ứng dụng WSGI chấp nhận và xác nhận các yêu cầu REST (JSON hoặc XML) từ client và chuyển chúng tới các quy trình CInder khác nếu thích hợp với AMQP|
|Cinder-scheduler|Chương trình lập lịch các định back-end nào sẽ là điểm đến cho một yêu cầu tạo ra volume hoặc chuyển yêu cầu đó. Nó duy trì trạng thái không liên tục cho các back-end (Ví dụ : khả năng sẵn có , khả năng và các thông số kỹ thuật được hỗ trợ) có thể được tận dụng khi đưa ra các quyết định về vị trí . Thuật toán được sử dụng bởi chương trình lên lịch có thể được thay đổi thông qua cấu hình Cinder|
|Cinder-volume|Cinder-volume chấp nhận các yêu cầu từ các quy trình CInder khác đóng vai trò là thùng chứa hoạt động cho các trình điều khiển Cinder. Quá trình này là đa luồng và thường có một luồng thực hiện trên mỗi Cinder back-end giống như định nghĩa trong tập tin cấu hình Cinder.|
|Cinder-backup|Xử lý tương tác với các mục tiêu sao có khả năng sao lưu (Ví dụ như OpenStack Object Storage Service - Swift). Khi một máy client yêu cầu sao lưu volume được tạo ra hoặc quản lý.|


### Cinder Processes Concept Diagram:

![cinder-process-diagram](/images/cinder/cinder-process-diagram.png)

Hình bên trên mô tả quy trình tạo Volume , tiếp theo chúng ta cùng đến với quy trình tạo ra volume mới của Cinder :

![create-new-volume-diagram](/images/cinder/create-new-volume-diagram.png)

1. Client yêu cầu tạo ra Volume thông qua việc gọi REST API (Client cũng có thể sử dụng tiện ích CLI của python-client)
2. Cinder-api : Quá trình xác nhận hợp lệ yêu cầu thông tin người dùng , một khi được xác nhận một message được gửi lên hàng chờ AMQP để xử lý.
3. Cinder-volume thực hiện quá trình đưa message ra khỏi hàng đợi , gửi thông báo tới cinder-scheduler để báo cáo xác định backend cung cấp volume.
4. Cinder-scheduler thực hiện quá trình báo cáo sẽ đưa thông báo ra khỏi hàng đợi , tạo danh sách các ứng viên dựa trên trạng thái hiện tại và yêu cầu tạo volume theo tiêu chí (kích thước, vùng sẵn có, loại volume (bao gồm cả thông số kỹ thuật bổ sung)).
5. Cinder-volume thực hiện quá trình đọc message phản hồi từ cinder-scheduler từ hàng đợi. Lặp lại qua các danh sách ứng viên bằng các gọi backend driver cho đến khi thành công.
6. NetApp Cinder tạo ra volume được yêu cầu thông qua tương tác với hệ thống lưu trữ con (phụ thuộc vào cấu hình và giao thức).
7. Cinder-volume thực hiện quá trình thu thập dữ liệu và metadata volume và thông tin kết nối để trả lại thông báo đến AMQP.
8. Cinder-api thực hiện quá trình đọc message phản hồi từ hàng đợi và đáp ứng tới client.
9. Client nhận được thông tin bao gồm trạng thái của yêu cầu tạo, Volume UUID, ....


### Cinder & Nova Workflow - Volume Attach

![cinder-nova-workflow](/images/cinder/cinder-nova-workflow.png)

1. Client yêu cầu attach volume thông qua Nova REST API (Client có thể sử dụng tiện ích CLI của python-novaclient)
2. Nova-api thực hiện quá trình xác nhận yêu cầu và thông tin người dùng. Một khi đã được xác thực, gọi API Cinder để có được thông tin kết nối cho volume được xác định.
3. Cinder-api thực hiện quá trình xác nhận yêu cầu hợp lệ và thông tin người dùng hợp lệ . Một khi được xác nhận , một message sẽ được gửi đến người quản lý volume thông qua AMQP.
4. Cinder-volume tiến hành đọc message từ hàng đợi , gọi Cinder driver tương ứng với volume được gắn vào.
5. NetApp Cinder driver chuẩn bị Cinder Volume chuẩn bị cho việc attach (các bước cụ thể phụ thuộc vào giao thức lưu trữ được sử dụng).
6. Cinder-volume thưc hiện gửi thông tin phản hồi đến cinder-api thông qua hàng đợi AMQP.
7. Cinder-api thực hiện quá trình đọc message phản hồi từ cinder-volume từ hàng đợi; Truyền thông tin kết nối đến RESTful phản hồi gọi tới NOVA.
8. Nova tạo ra kết nối với bộ lưu trữ thông tin được trả về Cinder.
9. Nova truyền volume device/file tới hypervisor , sau đó gắn volume device/file vào máy ảo client như một block device thực thế hoặc ảo hóa (phụ thuộc vào giao thức lưu trữ).

# Tham Khảo :

- https://docs.openstack.org/mitaka/install-guide-ubuntu/cinder-storage-install.html
- http://netapp.github.io/openstack-deploy-ops-guide/icehouse/content/section_cinder-processes.html