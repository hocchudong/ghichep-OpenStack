# Một số thao tác quản trị Swift trên Openstack

## Mục lục
- [1. Một số thao tác cơ bản](#1)
- [2. Sử dụng lệnh cURL](#2)
- [3. Lab storage policy](#3)

<a name=1></a>
## 1. Một số thao tác cơ bản.
- Sử dụng lệnh `swift stat`

  ```sh
  ~# swift stat
                          Account: AUTH_b54646bf669746db8c62ec0410bd0528
                       Containers: 2
                          Objects: 3
                            Bytes: 7
  Containers in policy "policy-0": 2
     Objects in policy "policy-0": 3
       Bytes in policy "policy-0": 7
      X-Account-Project-Domain-Id: default
           X-Openstack-Request-Id: txcd2bc73d764c42edac195-00599f95bb
                      X-Timestamp: 1502474830.56432
                       X-Trans-Id: txcd2bc73d764c42edac195-00599f95bb
                     Content-Type: text/plain; charset=utf-8
                    Accept-Ranges: bytes
  ```
  
  - Hiện tại có 2 containers, 3 objects.
  
- Xác định tên các containers có trong swift

  ```sh
  ~# swift list
  container1
  container2
  ```
  
- Liệt kê các object trong một container cụ thể

  ```sh
  ~# swift list container1
  file1
  file2
  ```
  
- Upload 1 file lên container

  ```sh
  $ swift upload new_container file2
  ```
  
  - `new_container` là tên của container
  - `file2` là file cần upload, có thể thay thế bằng path của file cần up.
  
- Xem trạng thái của một object

  ```sh
  ~# swift stat container1 file1
                 Account: AUTH_b54646bf669746db8c62ec0410bd0528
               Container: container1
                  Object: file1
            Content Type: application/octet-stream
          Content Length: 0
           Last Modified: Fri, 11 Aug 2017 18:13:10 GMT
                    ETag: d41d8cd98f00b204e9800998ecf8427e
           Accept-Ranges: bytes
             X-Timestamp: 1502475189.17697
              X-Trans-Id: tx04f19caf5781452484ae1-00599f9829
  X-Openstack-Request-Id: tx04f19caf5781452484ae1-00599f9829
  ```
  
- download một object.

  ```sh
  ~# swift download container2 file1
  file1 [auth 5.006s, headers 5.860s, total 5.861s, 0.000 MB/s]
  ```
  
<a name=2></a>
## 2. Sử dụng lệnh cURL.
- Lệnh cURL phổ biến trong giao thức HTTP.
- Lấy thông tin xác thực và URL của storage, sử dụng lệnh `swift auth`

  ```sh
  ~# swift auth
  export OS_STORAGE_URL=http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528
  export OS_AUTH_TOKEN=gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY
  ```
  
- Tạo một container mới.
- Sử dụng HTTP PUT.

  ```sh
  curl -X PUT -H 'X-Auth-Token: gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/new_container
  ```
  
  - giá trị sau `X-Auth-Token` được thay thế bằng giá trị sau `OS_AUTH_TOKEN` nhận được ở trên.
  - sau url nhận được ở trên, cần thêm tên của container muốn tạo.
  
- Sử dụng HTTP GET để liệt kê các container giống như lệnh swift stat.

  ```sh
  $ curl -X GET -H 'X-Auth-Token: gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/
  
  container1
  container2
  new_container
  ```

- Upload file lên container

  ```sh
  $ curl -X PUT -H 'X-Auth-Token: gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/new_container/ -T /etc/network/interfaces
  ```
  
- Lấy nội dung trong new_container

  ```sh
  $ curl -X GET -H 'X-Auth-Token: gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/new_container 
  
  interfaces
  ```
  
- Lấy nội dung của object

  ```sh
  $ curl -X GET -H 'X-Auth-Token: gAAAAABZn573BDBO-u0adDsY-N-cImY6HhwbibF8OIG52RnTkkzM8yCYARUHF-r-8nHYUNX2t0Hm5jql9B0_hpvgOs3NXb87UKtbF1c-P2K0P-eR6038tToexRRifmE9gKE5QA2f8iM4Uqv7nbNGMLX0nRKlUdlLC1orebRmucAcIWwQVbW_yPY' \
  http://controller:8080/v1/AUTH_b54646bf669746db8c62ec0410bd0528/new_container/interfaces
  
  # This file describes the network interfaces available on your system
  # and how to activate them. For more information, see interfaces(5).

  source /etc/network/interfaces.d/*

  # The loopback network interface
  auto lo
  iface lo inet loopback

  # The primary network interface
  auto ens3
  iface ens3 inet static
          address 10.10.10.190
          netmask 255.255.255.0


  auto ens4
  iface ens4 inet static
          address 172.16.69.190
          netmask 255.255.255.0
          gateway 172.16.69.1
          dns-nameservers 8.8.8.8

  auto ens5
  iface ens5 inet static
          address 10.10.20.190
          netmask 255.255.255.0
  ```
 
<a name=3></a>
## 3. Lab storage policy

# Cấu hình policy
### Định nghĩa policy
- Mỗi policy được định nghĩa bởi một section trong file `/etc/swift/swift.conf`.
- Tên của section phải theo mẫu `[storage-policy:<N>]`. N là index của policy.
- Trong mỗi section policy chứa các option sau:
	- `name = <policy name>`: option này phải có
		- tên của policy
		- tên của policy phải là duy nhất
		- tên policy có thể thay đổi
		- tên `Policy-0` chỉ có thể được sử dụng với index 0
	- `default = [true|false]`: (optional)
		- Nếu `true` thì policy này sẽ được sử dụng khi client không chỉ rõ.
		- Giá trị mặc định là false
		- Nếu không có policy nào khai báo là policy mặc định thì policy với index 0 là policy mặc định
		- `Deprecated` policy không thể là `default` policy
	- `deprecated = [true|false]`: (optional)
		- Nếu `true` thì các containers mới được tạo ra không thể sử dụng policy này.
		- Giá trị mặc định là `false`
		
### Ví dụ:
- Trong file `/etc/swift/swift.conf`, ta khai báo thêm một policy nữa như sau:

	```sh
	[storage-policy:1]
	name = silver
	policy_type = replication
	```
	- policy có index 1
	- tên là silver

- Tiếp đến chúng ta cần tạo một object ring cho policy này.

	```sh
	cd /etc/swift
	
	swift-ring-builder object-1.builder create 10 3 1
	```
	
- Sau đó thêm các devices vào object ring này.

	```sh
	swift-ring-builder object-1.builder add \
	--region 1 --zone 1 --ip 10.10.10.100 --port 6200 --device sdb --weight 10
	
	swift-ring-builder object-1.builder add \
	--region 1 --zone 1 --ip 10.10.10.100 --port 6200 --device sdc --weight 10

	swift-ring-builder object-1.builder add \
	--region 1 --zone 1 --ip 10.10.10.101 --port 6200 --device sdb --weight 10

	swift-ring-builder object-1.builder add \
	--region 1 --zone 1 --ip 10.10.10.101 --port 6200 --device sdc --weight 10
	```
	
- Kiểm tra lại ring:

	```sh
	swift-ring-builder object-1.builder
	```
	
- Tái cân bằng ring
	
	```sh
	swift-ring-builder object.builder rebalance
	```
	
- copy file `object-1.ring.gz` đến các node mà chứa các thiết bị đã được thêm vào ring ở bước trước.

	```sh
	scp /etc/swift/object-1.ring.gz root@10.10.10.100:/etc/swift
	scp /etc/swift/object-1.ring.gz root@10.10.10.101:/etc/swift
	```
	
- Restart các services

	```sh
	service memcached restart
	service swift-proxy restart
	```
	
- Tạo một container mới với policy là có tên là silver.

	```sh
	curl -v -X PUT -H 'X-Auth-Token: <your auth token>' \
  -H 'X-Storage-Policy: silver' http://127.0.0.1:8080/v1/AUTH_07032571cca84854b4116a7be846089d/container_silver
	```
	
- Sử dụng lệnh sau để lấy metadata của container vừa tạo:

	```sh
	curl -i -X HEAD -H 'X-Auth-Token: <your auth token>' \
  http://127.0.0.1:8080/v1/AUTH_07032571cca84854b4116a7be846089d/container_silver
	Warning: Setting custom HTTP method to HEAD with -X/--request may not work the
	Warning: way you want. Consider using -I/--head instead.
	HTTP/1.1 204 No Content
	Content-Length: 0
	X-Container-Object-Count: 0
	Accept-Ranges: bytes
	X-Storage-Policy: silver
	Last-Modified: Tue, 10 Oct 2017 16:06:17 GMT
	X-Container-Bytes-Used: 0
	X-Timestamp: 1507651575.76753
	Content-Type: text/plain; charset=utf-8
	X-Trans-Id: tx80a5052350b943458fb05-0059dcf204
	X-Openstack-Request-Id: tx80a5052350b943458fb05-0059dcf204
	Date: Tue, 10 Oct 2017 16:15:00 GMT
	```
	
	- như vậy container có `X-Storage-Policy: silver`
	