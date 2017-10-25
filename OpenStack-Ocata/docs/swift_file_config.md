# Giải thích file cấu hình cơ bản của swift

# Mục lục
- [1. File cấu hình proxy-server.conf](#1)
- [2. File cấu hình swift.conf](#2)
- [3. File cấu hình account-server.conf](#3)
- [4. File cấu hình container-server.conf](#4)
- [5. File cấu hình object-server.conf](#5)

<a name=1></a>
## 1. File cấu hình `proxy-server.conf`

- Trong section `[DEFAULT]`
	- `bind_port = 8080` cấu hình port 8080 được sử dụng cho proxy server
	- `user = swift` tên user sử dụng swift của hệ thống
	- `swift_dir = /etc/swift` là thư mục của swift
	
- Section `[pipeline:main]` cấu hình pipeline.

- Section `[app:proxy-server]`, 	`account_autocreate = True` sẽ tự động tạo account cho user nếu account chưa tồn tại trên hệ thống.

- Section `[filter:tempauth]` cấu hình cho hệ thống xác thực có trong swift. Trong tài liệu này sử dụng hệ thống xác thực keystone nên không cần quan tâm đến section này.

- Section `[filter:authtoken]` cấu hình để sử dụng hệ thống xác thực keystone cung cấp token

	- `paste.filter_factory = keystonemiddleware.auth_token:filter_factory` khai báo truy cập keystone
	
	```sh
	auth_uri = http://controller:5000
	auth_url = http://controller:35357
	memcached_servers = controller:11211
	auth_type = password
	project_domain_name = default
	user_domain_name = default
	project_name = service
	username = swift
	password = Welcome123
	delay_auth_decision = True
	```
	- Thông tin xác thực của tài khoản admin cho swift.
	
- Section `[filter:keystoneauth]` cấu hình các role được phép tương tác với swift.
	- User phải có một role trong các role được định nghĩa trong `operator_roles`
	
	```sh
	operator_roles = admin,user
	```
	
	- ở đây có 2 role là admin và user được phép tương tác với swift.
	
- Section `[filter:cache]` cấu hình sử dụng memcache server.
	
	```sh
	memcache_servers = controller:11211
	```
	
<a name=2></a>
## 2. File cấu hình swift.conf
- Section `[swift-hash]` cung cấp dãy ký tự được sử dụng trong thuật toán băm
	
	```sh
	swift_hash_path_suffix = HASH_PATH_SUFFIX
	swift_hash_path_prefix = HASH_PATH_PREFIX
	```
	
	- Hai giá trị này phải được giữ bí mật mà không được thay đổi.
	
- Section `[storage-policy:0]` cấu hình về policy lưu trữ index 0.

	- `name = Policy-0` tên của policy
	- `default = yes` cấu hình policy có mặc định hay không
	
<a name=3></a>
## 3. File cấu hình account-server.conf
- Section `[DEFAULT]`, cấu hình địa chỉ ip, port, user, thư mục và kiểm tra mount point:

	```sh
	bind_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
	bind_port = 6202
	user = swift
	swift_dir = /etc/swift
	devices = /srv/node
	mount_check = True
	```
	
	- `MANAGEMENT_INTERFACE_IP_ADDRESS` địa chỉ ip quản lý của node cài account-server.
	- sử dụng port 6202 cho account-server
	- user là swift
	- sử dụng thư mục /etc/swift
	- thiết bị /srv/node
	
- Section `	[pipeline:main]`, cấu hình sử dụng các module phù hợp cho account-server

	```sh
	pipeline = healthcheck recon account-server
	```
	
- Section `[filter:recon]`, cấu hình thư mục cho recon cache.

	```sh
	recon_cache_path = /var/cache/swift
	```
	
<a name=4></a>
## 4. File cấu hình container-server.conf
- Section `[DEFAULT]`, cấu hình địa chỉ ip, port, user, thư mục và kiểm tra mount point:

	```sh
	bind_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
	bind_port = 6201
	user = swift
	swift_dir = /etc/swift
	devices = /srv/node
	mount_check = True
	```
	
	- `MANAGEMENT_INTERFACE_IP_ADDRESS` địa chỉ ip quản lý của node cài container-server.
	- sử dụng port 6201 cho container-server
	- user là swift
	- sử dụng thư mục /etc/swift
	- thiết bị /srv/node
	
- Section `	[pipeline:main]`, cấu hình sử dụng các module phù hợp cho container-server

	```sh
	pipeline = healthcheck recon container-server
	```
	
- Section `[filter:recon]`, cấu hình thư mục cho recon cache.

	```sh
	recon_cache_path = /var/cache/swift
	```
	

<a name=5></a>
## 5. File cấu hình object-server.conf
- Section `[DEFAULT]`, cấu hình địa chỉ ip, port, user, thư mục và kiểm tra mount point:

	```sh
	bind_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
	bind_port = 6200
	user = swift
	swift_dir = /etc/swift
	devices = /srv/node
	mount_check = True
	```
	
	- `MANAGEMENT_INTERFACE_IP_ADDRESS` địa chỉ ip quản lý của node cài object-server.
	- sử dụng port 6200 cho object-server
	- user là swift
	- sử dụng thư mục /etc/swift
	- thiết bị /srv/node
	
- Section `	[pipeline:main]`, cấu hình sử dụng các module phù hợp cho object-server

	```sh
	pipeline = healthcheck recon object-server
	```
	
- Section `[filter:recon]`, cấu hình thư mục cho recon cache.

	```sh
	recon_cache_path = /var/cache/swift
	```
	