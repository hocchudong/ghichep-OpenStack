# Giải thích các file cấu hình của Glance
- Glance có 2 file cấu hình:
  - File cấu hình cho glance API, đường dẫn của file: `/etc/glance/glance-api.conf`
  - File cấu hình cho glance Registry, đường dẫn của file: `/etc/glance/glance-registry.conf`
  
## 1. File cấu hình cơ bản của glance API.
- Glance-api: Chấp nhận các lời gọi đến API để phát hiện, truy xuất và lưu trữ image.

---

### File cấu hình

  ```sh
  [database]
  connection = mysql+pymysql://glance:Welcome123@controller/glance
  backend = sqlalchemy
  
  
  [glance_store]
  stores = file,http
  default_store = file
  filesystem_store_datadir = /var/lib/glance/images/

  
  [image_format]
  disk_formats = ami,ari,aki,vhd,vhdx,vmdk,raw,qcow2,vdi,iso,ploop.root-tar


  [keystone_authtoken]
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = glance
  password = Welcome123


  [paste_deploy]
  flavor = keystone

  ```

### Giải thích file cấu hình.
- Cấu hình truy cập và sử dụng database

  ```sh
  [database]
  #
  connection = mysql+pymysql://glance:Welcome123@controller/glance
  backend = sqlalchemy
  ```
  
  - connection = mysql+pymysql://glance:Welcome123@controller/glance : cung cấp thông tin truy cập đến database glance, username: `glance` password: `Welcome123`
  - backend = sqlalchemy: Khai báo back end để sử dụng cho database.
 
- Khai báo lưu trữ images 
  
  ```sh
  [glance_store]
  stores = file,http
  default_store = file
  filesystem_store_datadir = /var/lib/glance/images/
  ```
  
- Khai báo các loại định dạng image mà glance hỗ trợ.

  ```sh
  [image_format]
  disk_formats = ami,ari,aki,vhd,vhdx,vmdk,raw,qcow2,vdi,iso,ploop.root-tar
  ```
- Khai báo xác thực Keystone

  ```sh
  [keystone_authtoken]
  # ...
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = glance
  password = Welcome123

  ```
  
  - auth_uri = http://controller:5000 : Cấu hình enpoint Identity service
  - auth_url = http://controller:35357 : URL để xác thực Identity service
  - memcached_servers = controller:11211 : Địa chỉ Memcache-server
  - auth_type = password : Hình thức xác thực sử dụng password
  - project_domain_name = default : Chỉ định project domain name openstack
  - user_domain_name = default : Chỉ định user domain name openstack
  - project_name = service : Chỉ định project name openstack
  - username = glance : Chỉ định username của nova
  - password = Welcome123 : Chỉ đinh pass của nova
  
- Khai báo triển khai flavor để sử dụng trong ứng dụng pipeline trên server

  ```sh
  [paste_deploy]
  # ...
  flavor = keystone
  ```
  
## 2. File cấu hình cấu hình cơ bản của glance-registry
- Glane-registry: lưu trữ, xử lý, và lấy thông tin cho image.

---

### File cấu hình glance-registry ở trong đường dẫn `/etc/glance/glance-registry.conf`

  ```sh
  [database]
  connection = mysql+pymysql://glance:Welcome123@controller/glance
  backend = sqlalchemy
 
  [keystone_authtoken]
  auth_uri = http://controller:5000
  auth_url = http://controller:35357
  memcached_servers = controller:11211
  auth_type = password
  project_domain_name = default
  user_domain_name = default
  project_name = service
  username = glance
  password = Welcome123
  
  [paste_deploy]
  flavor = keystone
  ```

- Các thông tin khai báo trong file cấu hình cấu hình của glance-registry giống với glance-api.  
  
  
  
  
  