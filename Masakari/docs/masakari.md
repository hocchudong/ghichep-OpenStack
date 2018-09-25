# Openstack Masakari

____

# Mục lục


- [1. Giới thiệu về Masakari](#about)
- [2. Thực hiện cài đặt và cấu hình cho Masakari](#config)
- [Các nội dung khác](#content-others)

____

# <a name="content">Nội dung</a>

- ### <a name="about">1. Giới thiệu về Masakari</a>
	- Masakari cung cấp API service và cơ chế phục hồi

		|     Mô tả       |																|
		|-----------------|-------------------------------------------------------------|
		| Official name   | [Masakari](https://launchpad.net/masakari) 				  	|
		| Source code     | https://github.com/openstack/Masakari 					  	|
		| Bug tracker     | https://bugs.launchpad.net/masakari 						|
		| Feature tracker | https://blueprints.launchpad.net/masakari 				  	|
		| Code Review     | https://review.openstack.org/#/q/project:openstack/masakari |

- ### <a name="config">2. Thực hiện cài đặt và cấu hình cho Masakari</a>
	- Yêu cầu trước khi sử dụng Masakari:
		- Nếu thực hiện sử dụng Masakari, ta cần phải cấu hình nova-compute host có thể live-migrate instances và nên sử dụng shared backend-storage để tránh mất dữ liệu.
		- Để cài đặt và sử dụng masakari, hãy thực hiện theo các bước bên dưới.

	- #### Điều kiện yêu cầu
		- Sử dụng database access clien để kết nối đến database server bằng user root:

				# mysql

		- Tạo `masakari` database:

				MariaDB [(none)]> CREATE DATABASE masakari;

		- Cấp quyền truy cập tới `masakari` database:

				MariaDB [(none)]> GRANT ALL PRIVILEGES ON masakari.* TO 'masakari'@'localhost' IDENTIFIED BY 'Welcome123';
				MariaDB [(none)]> GRANT ALL PRIVILEGES ON masakari.* TO 'masakari'@'%' IDENTIFIED BY 'Welcome123';

			Thoát khỏi database access client.

	- #### Cài đặt và cấu hình masakari
		- Clone maskari sử dụng git:

				# git clone https://github.com/openstack/masakari.git

		- Chạy `setup.py` từ thư mục masakari để cài đặt:

				# python setup.py install && pip install pymysql python-memcached
				# pip install -r requirements.txt

		- Tạo đường dẫn chưa file cấu hình cho `masakari`

				# mkdir /etc/masakari

		- Copy file cấu hình `api-paste.ini` từ thư mục `maskari/etc/` tới `/etc/masakari/`.

				# cp etc/masakari/api-paste.ini /etc/masakari/api-paste.ini

		- Copy file cấu hình `masakari.conf.sample` và `masakari.policy.yaml.sample` từ thư mục `doc/source/_static/
` tới `/etc/masakari/`:
				
				# cp doc/source/_static/masakari.conf.sample /etc/masakari/masakari.conf
				# cp doc/source/_static/masakari.policy.yaml.sample /etc/masakari/policy.yaml

		- Sửa file `/etc/masakari/masakari.conf` để thêm nội dung cấu hình như sau:
			1. Trong `[database]` section cấu hình truy cập database:

					[database]
					#...
					connection = mysql+pymysql://masakari:Welcome123@db_server_address/masakari?charset=utf8

				thay thế `db_server_address` với địa chỉ IP của database server.
			2. Trong `[DEFAUL]` section cấu hình option sau:

					[DEFAUL]
					#...
					auth_strategy = keystone
					masakari_topic = ha_engine
					nova_catalog_admin_info = compute:nova:public 
					os_region_name = RegionOne
					os_privileged_user_name = nova_username
					os_privileged_user_password = nova_password
					os_privileged_user_tenant = service
					os_privileged_user_auth_url = auth_url
					masakari_api_listen = ip_interface_lister
					publish_errors = true
					transport_url = rabbit://username:password@ip_address

				hãy thay thế các giá trị tương ứng sau:
				- `nova_username` bởi `nova-compute` username
				- `nova_password` bới `nova-compute` password
				- `auth_url` bởi endpoint xác thực trong Keystone service.(Ex: http://controller/identity)
				- `username` và `password` trong `transport_url` lần lượt là username và password tương ứng của người dùng trong message queue service (Ex: `openstack:Welcome123`) và `ip_address` là địa chỉ ip truy cập tới message queue service.
				- `ip_interface_lister` bởi địa chỉ IP sử dụng để cung cấp api-listen.

			3. Trong `[instance_failure]` section cấu hình cho option:

					[instance_failure]
					#...
					process_all_instances = true

			4. Trong `[keystone_authtoken]` cấu hình truy cập `Indentity service`:

					[keystone_authtoken]
					#...
					auth_url = auth_url
					project_domain_id = default
					user_domain_id = default
					project_name = service
					username = masakari
					password = Welcome123
					www_authenticate_uri = authenticate_uri
					region_name = RegionOne
					memcached_servers = ip_memcached_server:11211
					auth_type = password

				thay thế `auth_url` và `authenticate_uri` bởi endpoint xác thực trong Keytone service. (Ex: http://controller:5000 hoặc http://controller:35357), `ip_memcached_server` bởi địa chỉ IP cung cấp service memcached.

			5. Trong `[oslo_policy]` section, cấu hình sử dụng policy:

					[oslo_policy]
					#...
					policy_file = /etc/masakari/policy.yaml

			6. Trong `[wsgi]` section, cấu hình option api-wsgi:

					[wsgi]
					#...
					api_paste_config = /etc/masakari/api-paste.ini

				Lưu lại file vừa cấu hình.

			7. Sử dụng openstack cli để tạo user `masakari`:

					openstack user create --password-prompt masakari --password Welcome123

			8. Thêm admin role cho user masakari:

					openstack role add --project service --user masakari admin

			9. Tạo ra `masakari` service:

					openstack service create --name masakari --description "OpenStack High Availability" instance-ha

			10. Tạo các Masakari endpoint service:

					openstack endpoint create --region RegionOne masakari public http://ip_address:15868/v1/%\(tenant_id\)s
					openstack endpoint create --region RegionOne masakari admin http://ip_address:15868/v1/%\(tenant_id\)s
					openstack endpoint create --region RegionOne masakari internal http://ip_address:15868/v1/%\(tenant_id\)s

				thay thế `ip_address` bởi địa chỉ đã cấu hình cho `masakari_api_listen` trong `[DEFAUL]` section.
			11. Populate the Masakari service database:

					masakari-manage db sync

			12. Khởi chạy Masakari:

					masakari-api &
					masakari-engine &

____		

# <a name="content-others">Các nội dung khác</a>
