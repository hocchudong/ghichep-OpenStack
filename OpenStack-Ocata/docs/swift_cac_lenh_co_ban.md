# Các lệnh cơ bản với Swift
- Một số thao tác quản trị Swift trên Openstack

# Mục lục

- [1. Xem metadata của user](#1)
- [2. Lists các containers](#2)
- [3. Lists các objects trong container](#3)
- [4. Tạo một object](#4)
- [5. Download một object](#5)
- [6. Delete một object](#6)
- [7. Một số lệnh curl cơ bản](#7)

<a name=1></a>
## 1. Xem metadata của user
- Sử dụng lệnh `swift stat`

  ```sh
  swift stat
  ```

<a name=2></a>
## 2. Lists các containers 
- Xác định tên các containers có trong swift

  ```sh
  swift list
  ```
  
<a name=3></a>
## 3. Lists các objects trong container
- Liệt kê các object trong một container cụ thể

  ```sh
  swift list <container name>
  ```
  
<a name=4></a>
## 4. Tạo một object
- Upload 1 file lên container

  ```sh
  swift upload <container name> <file path>
  ```
  
	- hoặc lệnh
	
	```sh
	openstack object create <container name> <file path>
	```
	
  - `container name` là tên của container nơi muốn lưu object
	- `file path` là đường dẫn đến file cầu upload.
 
<a name=5></a>
## 5. Download một object
- download một object.

  ```sh
  swift download <container name> <object name>
  ```
  
	- `container name` là tên của container chứa object cần tải
	- `object name` là tên của object cần tải.
	
<a name=6></a>
## 6. Delete một object

	```sh
	openstack object delete <container name> <object name>
	```
	
# Ngoài cách sử dụng command line, chúng ta có thể sử dụng lệnh curl để tương tác với swift
<a name=7></a>
## 7. Một số lệnh curl cơ bản
- Lệnh cURL phổ biến trong giao thức HTTP.
- Lấy thông tin xác thực và URL của storage, sử dụng lệnh `swift auth`

  ```sh
  ~# swift auth
  export OS_STORAGE_URL=http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528
  export OS_AUTH_TOKEN=<token value>
  ```
  
	- chúng ta có được đường dẫn của account và giá trị token
	
- Tạo một container mới.
- Sử dụng HTTP PUT.

  ```sh
  curl -X PUT -H 'X-Auth-Token: <token>' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/<container name>
  ```
  
- Sử dụng HTTP GET để liệt kê các container giống như lệnh swift stat.

  ```sh
  $ curl -X GET -H 'X-Auth-Token: <token>' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/
  ```

- Upload file lên container

  ```sh
  $ curl -X PUT -H 'X-Auth-Token: <token>' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/<container name>/ \
	-T <file path>
  ```
  
- Lấy nội dung trong container

  ```sh
  $ curl -X GET -H 'X-Auth-Token: <token>' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/<container name>
  ```
  
- Lấy nội dung của object

  ```sh
  $ curl -X GET -H 'X-Auth-Token:<token>' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/<container name>/<object name>
  ```
 