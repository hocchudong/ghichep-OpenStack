# Openstack Python Masakari Client

____

# Mục lục


- [1. Giới thiệu về Python Masakari Client](#about)
- [2. Cài đặt và sử dụng Python Masakari Client](#config)
- [Các nội dung khác](#content-others)

____

# <a name="content">Nội dung</a>

- ### <a name="about">1. Giới thiệu về Python Masakari Client</a>
	- Là công cụ cho phép người sử dụng thao tác và quản lý cho Masakari

- ### <a name="config">2. Cài đặt và sử dụng Python Masakari Client</a>
	- #### Cài đặt python-masakariclient
		- Clone python-masakariclient sử dụng git:

				# git clone http://github.com/openstack/python-masakariclient.git

		- Install requirements:

				# pip install -r requirements.txt

		- Chạy file `setup.py` để cài đặt `python-masakariclient`:

				# python setup.py install

		- Tạo Masakari client environment scripts:

			Tạo ra một file với tên là `masakari-openrc` với nội dung như sau:

					export OS_AUTH_PLUGIN=keystone
					export OS_AUTH_URL=auth_url
					export OS_DOMAIN_ID=default
					export OS_IDENTITY_API_VERSION=3
					export OS_IMAGE_API_VERSION=2
					export OS_PASSWORD=password
					export OS_PROJECT_DOMAIN_ID=Default
					export OS_PROJECT_NAME=service
					export OS_USER_DOMAIN_NAME=Default
					export OS_USERNAME=masakari

				thay `auth_url` bởi enpoint của Identity service.

		- Nếu thực hiện cài `python-masakariclient` trên host đã cài đặt `masakari` thì ta không cần phải cầu hình gì thêm. Ngược lại, ta cần phải thực hiện cấu hình tương tự như cấu hình cho  `masakari` đối với file `masakari.conf`. Chi tiết tại [Cấu hình masakari](masakari.md#config)

		- Để biết rõ hơn chi tiết về việc sử dụng python-masakariclient, ta sử dụng:

			# masakari --help
____

# <a name="content-others">Các nội dung khác</a>
