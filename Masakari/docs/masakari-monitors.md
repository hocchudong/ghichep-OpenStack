# Openstack Masakari Monitors

____

# Mục lục


- [1. Giới thiệu về Masakari Monitors](#about)
- [2. Các thành phần của masakari-monitors](#components)
- [3. Cài đặt và câu hình cho masakari-monitors](#config)
- [4. Kiểm tra kết quả](#check)
- [Các nội dung khác](#content-others)

____

# <a name="content">Nội dung</a>

- ### <a name="about">1. Giới thiệu về Masakari Monitors</a>
	- Là công cụ cung cấp việc monitor nova-compute host, VMs, process và gửi notifications tới masakari-api khi có failed events xảy ra.

- ### <a name="components">2. Các thành phần của masakari-monitors</a>
	- masakari-monitors bao gồm các thành phần sau:
		- masakari-hostmonitor
		- masakari-introspectiveinstance
		- masakari-instancemonitor
		- masakari-processmonitor

	- Để giám sát sử dụng `masakari-hostmonitor` ta cần phải cấu hình `pacemaker-corosync` trên host đó.
	
- ### <a name="config">3. Cài đặt và câu hình cho masakari-monitors</a>
	- Các bước thực hiện cài đặt masakari-monitors như sau:
		- Clone masakari-monitors sử dụng git:

				# git clone https://github.com/openstack/masakari-monitors

		- Install requirements:

				# pip insall -r requirements.txt
				# pip install oslo_log

		- Chạy file `setup.py` trong thư mục masakari-monitors để cài đặt masakari-monitors:

				# python setup.py install

		- Tạo ra thư mục cấu lưu file câu hình cho masakari-monitors:

				# mkdir /etc/masakarimonitors

		- Trước khi có thể generate ra file cấu hình cho masakarimonitors, cần phải cài đặt `tox` và `gcc`. Sau đó sử dụng câu lệnh sau:

				# tox -e genconfig

		- Copy file cấu hình `masakarimonitors.conf.sample` từ `etc/masakarimonitors` tới `/etc/masakarimonitors`

				cp etc/masakarimonitors/masakarimonitors.conf.sample /etc/masakarimonitors/

		- Copy file `hostmonitor.conf.sample`, `proc.list.sample`, `process_list.yaml.sample`, `processmonitor.conf.sample` từ `etc/masakarimonitors` tới `/etc/masakarimonitors`:

				cp etc/masakarimonitors/hostmonitor.conf.sample /etc/masakarimonitors/hostmonitor.conf
				cp etc/masakarimonitors/proc.list.sample /etc/masakarimonitors/proc.list
				cp etc/masakarimonitors/process_list.yaml.sample /etc/masakarimonitors/process_list.yaml
				cp etc/masakarimonitors/processmonitor.conf.sample /etc/masakarimonitors/processmonitor.conf

		- Thực hiện cấu hình các file:
			- Sửa nội dung file `hostmonitor.conf` cho options ví dụ như sau:

					#...
					DOMAIN="Default"
					ADMIN_USER="admin"
					ADMIN_PASS="Welcome123"
					PROJECT="service"
					REGION="RegionOne"
					AUTH_URL="http://10.0.0.254:5000/"

				hãy thay thế các giá trị tương ứng.

			- Sửa nội dung file `masakarimonitors.conf` ví dụ như sau:
				1. Trong `[DEFAULT]` section:

						[DEFAULT]
						#...
						publish_errors = true
						fatal_deprecations = true

				2. Trong `[api]` section:

						[api]
						#...
						region = RegionOne
						api_version = v1
						api_interface = admin
						auth_url = http://10.0.0.254:5000/
						domain_name = Default
						project_name = service
						username = masakari
						password = Welcome123

				3. Trong `[callback]` section:

						[callback]
						#...
						retry_max = 12
						retry_interval = 10

				4. Trong `[host]` section:

						[host]
						#...
						monitoring_driver = default
						monitoring_interval = 60
						api_retry_max = 12
						api_retry_interval = 10
						ipmi_timeout = 5
						ipmi_retry_max = 3
						ipmi_retry_interval = 10
						stonith_wait = 30
						tcpdump_timeout = 5
						corosync_multicast_interfaces = ens8
						corosync_multicast_ports = 5405

					trong đó `ens8` được sử dụng để liên lạc giữa các `nova-compute host` khi sử dụng `pacemaker-corosync`

				5. Trong `[introspectiveinstancemonitor]` section:

						[introspectiveinstancemonitor]
						#...
						guest_monitoring_interval = 10
						guest_monitoring_timeout = 2
						guest_monitoring_failure_threshold = 3
						qemu_guest_agent_sock_path = /var/lib/libvirt/qemu/domain-\w+-instance-\w+/\w+.sock

					trong đó `/var/lib/libvirt/qemu/domain-\w+-instance-\w+/\w+.sock` là một regexp trong python để tìm đến file *.sock cho mỗi instance trong nova-compute host.

				6. Trong `[libvirt]` section:

						[libvirt]
						#...
						connection_uri = qemu:///system

				7. Trong `[process]` section:

						[process]
						#...
						check_interval = 5
						restart_retries = 3
						api_retry_max = 12
						api_retry_interval = 10
						process_list_path = /etc/masakarimonitors/process_list.yaml

			- Sửa nội dung file `processmonitor.conf` ví dụ như sau:

					PROCESS_CHECK_INTERVAL=5
					PROCESS_REBOOT_RETRY=3
					REBOOT_INTERVAL=5
					MASAKARI_API_SEND_TIMEOUT=10
					MASAKARI_API_SEND_RETRY=12
					MASAKARI_API_SEND_DELAY=10
					LOG_LEVEL="debug"
					DOMAIN="Default"
					PROJECT="service"
					ADMIN_USER="admin"
					ADMIN_PASS="Welcome123"
					AUTH_URL="http://10.0.0.254:5000/"
					REGION="RegionOne"

				hãy thay các giá trị tương ứng.

			- Sửa file `process_list.yaml` như sau:

					-
					    # libvirt-bin
					    process_name: /usr/sbin/libvirtd
					    start_command: systemctl start libvirt-bin
					    pre_start_command:
					    post_start_command:
					    restart_command: systemctl restart libvirt-bin
					    pre_restart_command:
					    post_restart_command:
					    run_as_root: True
					-
					    # nova-compute
					    process_name: nova-compute
					    start_command: systemctl start nova
					    pre_start_command:
					    post_start_command:
					    restart_command: systemctl restart nova
					    pre_restart_command:
					    post_restart_command:
					    run_as_root: True

				bước cấu hình `systemctl restart nova` là để tiện cho việc kiểm tra kết quả.

- ### <a name="check">4. Kiểm tra kết quả</a>
	- Sau khi thực hiện cấu hình xong trên `masakarimonitors`. Ta cần phải thêm host đã cài đặt `masakarimonitors` bằng việc sử dụng câu lệnh `masakari`. Thứ tự thực hiện như sau:
		1. Tạo một segment
		2. Thêm mới một node với tên là hostname của host đã cài đặt `masakarimonitors` vào một segment đã có.

	- Để kiểm tra kết quả. Ta thử chạy câu lệnh sau (lần thứ nhất):

			# masakari-processmonitor &


		- Lần thứ 2, ta tắt service nova-compute:

				# service nova-compute stop

			chạy lệnh giám sát:

				# masakari-processmonitor &

____

# <a name="content-others">Các nội dung khác</a>
