# Ý nghĩa cấu hình trong file /etc/cinder/cinder.conf

`rootwrap_config = /etc/cinder/rootwrap.conf`

```sh
Chỉ định đường dẫn tới tập cấu hình gốc sử dụng để chạy Cinder bao gồm :
- Danh sách các thư mục tải được lọc.
- Danh sách các file thực thi trong trường hợp bộ lọc không hoạt động.
- Nếu thư mục thực thi không được chỉ định mặc định trỏ đến biến môi trường PATH
- Cho phép đăng nhập vào syslog , mặc định là False
- Cơ sở syslog nào được sử dụng trong các giá trị : authpriv, syslog, local0, local1... mặc định là syslog
- Các message từ log :
-- INFO Chỉ ra những log thành công.
-- ERROR Chỉ ra những log không thành công.
```

`api_paste_confg = /etc/cinder/api-paste.ini`

```sh
Tập tin cấu hình API của Cinder.
```

`iscsi_helper = tgtadm`

```sh
- Chỉ ra iSCSI sử dụng , mặc định là tgtadm. Ngoài ra còn có :
-- Lioadm hỗ trợ LIO iSCSI
-- Scstadmin cho SCST
-- Iseradm cho ISER
-- Ietadm cho iSCSI
```

`volume_name_template = volume-%s`

```sh
Template mẫu sử dụng để tạo tên volume
```

`verbose = True`

```sh
Chưa làm
```

`auth_strategy = keystone`

```sh
- Cấu hình sử dụng cho xác thực.
- Hỗ trợ noauth, keystone và deprecated
```

`state_path = /var/lib/cinder`

```sh
Thư mục cấp cao nhất duy trì trạng thái của Cinder
```

`lock_path = /var/lock/cinder`

```sh
Thư mục sử dụng cho các tệp khóa , mặc định là thư mục temp
```

`volumes_dir = /var/lib/cinder/volumes`

```sh
Thư mục lưu trữ tập tin cấu hình volume
```

`rpc_backend = rabbit`

```sh
Trình điều khiển message được sử dụng mặc định là rabbitMQ. Các trình điều khiển khác bao gồm qpid và zmq
```

`my_ip = 10.10.10.130`

```sh
Là địa chỉ của host
```

`enabled_backends = lvm`

```sh
- Cấu hình backend muốn sử dụng, ở đây là LVM
- Đối với multiple backend chỉ cần dấu phẩy giữa các backend (ví dụ : enable_backends = lvm,nfs,glusterfs)
```

`glance_api_servers = http://controller:9292`

```sh
Danh sách các máy chủ API cung cấp sẵn cho Cinder
```

`rabbit_host = 10.10.10.10`

```sh
Địa chỉ trung chuyển RabbitMQ nơi một node được sử dụng
```

`rabbit_userid = openstack`

```sh
RabbitMQ userid
```

`rabbit_password = Anhdat96`

```sh
RabbitMQ password
```

`connection = mysql+pymysql://cinder:Anhdat96@controller/cinder`

```sh
Chuỗi kết nối SQLAlchemy sử dụng để kết nối với cơ sở dữ liệu
```

`auth_uri = http://10.10.10.10:5000`

```sh
Cấu hình enpoint Identity service
```

`auth_url = http://10.10.10.10:35357`

```sh
URL để xác thực Identity service
```

`memcached_servers = 10.10.10.10:11211`

```sh
Tùy chọn chỉ định danh sách các máy chủ được memcached sử dụng cho bộ nhớ đệm. Nếu không được xác định, 
tokens sẽ được thay thế quá trình cache
```

`auth_type = password`

```sh
Chỉ định hình thức xác thực
```

```sh
project_domain_name = default  // CHỉ định project domain name openstack
user_domain_name = default  // Chỉ định user domain name openstack
project_name = service  // Chỉ định project name openstack
username = cinder  // Chỉ định username của cinder
password = Anhdat96  // CHỉ định password của cinder
```

`volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver`

```sh
Chỉ định driver LVM mà sử dụng
```

`volume_group = cinder-volumes`

```sh
Chỉ định vgroup mà chúng ta tạo lúc cài đặt , cinder-volumes là tên của vgroup
```

`iscsi_protocol = iscsi`

```sh
Xác định giao thức iSCSI cho iSCSI volumes mới, được tạo ra với tgtadm hoặc lioadm. Để kích hoạt RDMA , tham số lên lên được đặt là "iser" . Hỗ trợ cho giao thức iSCSI giá trị là "iscsi" và "iser"
```
