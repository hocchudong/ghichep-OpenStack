# Storage policy trong Ops Swift

## Mô tả bài toán
- Hệ thống Swift có nhiều loại thiết bị lưu trữ khác nhau (ổ đĩa quay HDD, ổ SSD, ...).
- Hãy quy hoạch thành các vùng lưu trữ khác nhau (pool storage) để phục vụ cho các mục đích lưu trữ khác nhau. Ví dụ như cần lưu các file có lượng truy cập cao thì lưu vào các thiết bị SSD, hay tùy thuộc vào lượng chi trả của khách hàng mà chọn nơi lưu trữ thích hợp.
- Để giải quyết bài toán, trong Swift cung cấp tính năng `Storage Policy`.

## Tổng quan về Storage policy
- Storage policy cho phép tổ chức lưu trữ các object vào các thiết bị khác nhau phụ thuộc vào mục đích sử dụng. Các policy được thực hiện thông qua `object ring`. Mỗi object ring là một policy.
- Storage policy sẽ xác định vị trí lưu các object bên trong container.
- Storage policy chỉ áp dụng cho các container, có nghĩa là khi một container được tạo ra sẽ được gán một policy.
- Khi một container được tạo, một tùy chọn header mới được hỗ trợ để chỉ định tên policy. Nếu không có tên được chỉ định thì policy mặc định được sử dụng (và nếu không có policy được đinh nghĩa, thì Policy-0 được coi là mặc định).
- Các policies sẽ được gán khi một container được tạo. Một khi container đã được ấn định policy thì sẽ không thể thay đổi (trừ khi nó bị xóa đi và tạo lại).
- Quan hệ giữa containers và policies là n-1 có nghĩa là nhiều container chia sẻ cùng 1 policy. Không có giới hạn về số lượng container trên một policy.

## Cấu hình một policy.
- Mỗi policy được định nghĩa bởi một section trong file `/etc/swift/swift.conf`.
- Tên của section phải theo mẫu `[storage-policy:<N>]`. N là index của policy.
- Trong mỗi section policy chứa các option sau:
	- `name = <policy name>`: option này phải có
		- tên của policy
		- tên của policy phải là duy nhất
		- tên policy có thể thay đổi
		- tên `Policy-0` chỉ có thể được sử dụng với `index 0`
	- default = [true|false]: (optional)
		- Nếu true thì policy này sẽ được sử dụng khi client không chỉ rõ.
		- Giá trị mặc định là false
		- Nếu không có policy nào khai báo là policy mặc định thì policy với index 0 là policy mặc định
	- Deprecated policy không thể là default policy
	- `deprecated = [true|false]`: (optional)
		- Nếu true thì các containers mới được tạo ra không thể sử dụng policy này.
		- Giá trị mặc định là false

- Sau khi cấu hình các policy, một object ring tương ứng phải được tạo ra mới có thể sử dụng policy đó.
- Tên object ring được đặt theo quy tắc: 
	- nếu là object ring cho `Policy-0` tên là `object.ring.gz`
	- Các policy khác đặt tên theo mẫu: `object-<index>.ring.gz`. index là thứ tự của policy, ví dụ policy có index = 1 thì tên được đặt là `object-1.ring.gz`
	
## Một số ví dụ
- Ta có một hệ thống swift như sau:

	![](../images/swift_layout.png)
	
- Mỗi node object đều có 2 ổ đĩa dùng để lưu trữ, tên là `/dev/vdb` và `/dev/vdc`.
- Địa chỉ ip của mỗi node object lần lượt là: 
	- 10.10.10.193
	- 10.10.10.194
	- 10.10.10.195
	- 10.10.10.196
	
- Chúng ta sẽ quy hoạch các pool storage như sau:
	- Với policy default gồm 4 thiết bị lưu trữ (2 ổ đĩa trên object1 và 2 ổ đĩa trên object2) trên 2 node object1 và object2.
	- Một policy có index = 1 gồm 4 thiết bị còn lại trên 2 node object3 và object4.
	
---
## Bắt đầu thực hiện cấu hình
- Lưu ý:

	```sh
	File cấu hình /etc/swift/swift.conf sẽ phải giống nhau trên tất cả các node. Có thể thực hiện chỉnh sửa trên node controller sau đó copy file cấu hình này đến các node khác trong hệ thống
	```
- File cấu hình policy là file `/etc/swift/swift.conf` ở trên node controller. Sau khi cấu hình xong, file này sẽ được copy đến tất cả các node object trên hệ thống.
- Với `Policy-0`: khi cài đặt sẽ được cấu hình mặc định. Với 2 node object1 và object2 sẽ thuộc vào zone 1. 

	```sh
	[storage-policy:0]
	name = Policy-0
	default = yes
	#policy_type = replication
	aliases = yellow, orange
	```

- Sau đó sẽ tạo object với tên `object.ring.gz` thông qua lệnh: 

	```sh
	swift-ring-builder object.builder create 10 3 1
	```
	
	- với lệnh trên, hệ thống sẽ tự động tạo một ring với tên `object.ring.gz`. Ring này sẽ có 2^10 partitions, 3 bản sao của object.
- Add các thiết bị từ 2 node object1 và object2 vào ring này bằng các lệnh sau:

	```sh
	swift-ring-builder object.builder add \
	--region 1 --zone 1 --ip 10.10.10.193 --port 6200 --device vdb --weight 15

	swift-ring-builder object.builder add \
	--region 1 --zone 1 --ip 10.10.10.193 --port 6200 --device vdc --weight 15

	swift-ring-builder object.builder add \
	--region 1 --zone 1 --ip 10.10.10.194 --port 6200 --device vdb --weight 15

	swift-ring-builder object.builder add \
	--region 1 --zone 1 --ip 10.10.10.194 --port 6200 --device vdc --weight 15
	```
	
	- ở đây các thiết bị có dung lượng 15 Gb.
	
- Kiểm tra lại ring bằng lệnh sau:

	```sh
	/etc/swift# swift-ring-builder object.builder
	object.builder, build version 5, id d201161e21954d5699d18688ffe9fa7d
	1024 partitions, 3.000000 replicas, 1 regions, 1 zones, 4 devices, 0.00 balance, 0.00 dispersion
	The minimum number of hours before a partition can be reassigned is 1 (0:00:00 remaining)
	The overload factor is 0.00% (0.000000)
	Ring file object.ring.gz is up-to-date
	Devices:   id region zone   ip address:port replication ip:port  name weight partitions balance flags meta
							0      1    1 10.10.10.193:6200   10.10.10.193:6200   vdb  15.00        768    0.00
							1      1    1 10.10.10.193:6200   10.10.10.193:6200   vdc  15.00        768    0.00
							2      1    1 10.10.10.194:6200   10.10.10.194:6200   vdb  15.00        768    0.00
							3      1    1 10.10.10.194:6200   10.10.10.194:6200   vdc  15.00        768    0.00
	```
	
- Tái cân bằng ring

	```sh
	/etc/swift# swift-ring-builder object.builder rebalance
	```
	
- Sau khi ring được tạo xong, ring này cần được copy đến các node có chứa thiết bị đã được add vào ring. Ở đây là ring `object.ring.gz` chứa các thiết bị ở trên node object1 và object2, do đó ta sẽ copy `object.ring.gz` đến thư mục `/etc/swift` trên node object1 và object2. Có nhiều cách để copy ring, dưới đây sử dụng lệnh `scp`.

	```sh
	scp /etc/swift/account.ring.gz /etc/swift/container.ring.gz /etc/swift/object.ring.gz root@10.10.10.193:/etc/swift
	scp /etc/swift/account.ring.gz /etc/swift/container.ring.gz /etc/swift/object.ring.gz root@10.10.10.194:/etc/swift
	```
---
- Với policy có index = 1 cho 2 node object3 và object4. 2 node này sẽ thuộc vào zone 2, ta cấu hình như sau:

	```sh
	[storage-policy:1]
	name = silver
	```
	
- Tạo ring `object-1.ring.gz`

	```sh
	swift-ring-builder object-1.builder create 10 3 1
	```
	
- Add các thiết bị trên 2 node object3 và object4. 

	```sh
	swift-ring-builder object-1.builder add \
	--region 1 --zone 2 --ip 10.10.10.195 --port 6200 --device vdb --weight 15

	swift-ring-builder object-1.builder add \
	--region 1 --zone 2 --ip 10.10.10.195 --port 6200 --device vdc --weight 15

	swift-ring-builder object-1.builder add \
	--region 1 --zone 2 --ip 10.10.10.196 --port 6200 --device vdb --weight 15

	swift-ring-builder object-1.builder add \
	--region 1 --zone 2 --ip 10.10.10.196 --port 6200 --device vdc --weight 15
	```
	
- Kiểm tra lại ring:

	```sh
	swift-ring-builder object-1.builder
	
	object-1.builder, build version 4, id 5106c186ea4241b2a290be0d6ce9c61a
	1024 partitions, 3.000000 replicas, 1 regions, 1 zones, 4 devices, 100.00 balance, 0.00 dispersion
	The minimum number of hours before a partition can be reassigned is 1 (0:00:00 remaining)
	The overload factor is 0.00% (0.000000)
	Ring file object-1.ring.gz not found, probably it hasn't been written yet
	Devices:   id region zone   ip address:port replication ip:port  name weight partitions balance flags meta
							0      1    2 10.10.10.195:6200   10.10.10.195:6200   vdb  15.00          0 -100.00
							1      1    2 10.10.10.195:6200   10.10.10.195:6200   vdc  15.00          0 -100.00
							2      1    2 10.10.10.196:6200   10.10.10.196:6200   vdb  15.00          0 -100.00
							3      1    2 10.10.10.196:6200   10.10.10.196:6200   vdc  15.00          0 -100.00
	```

- Tái cân bằng ring

	```sh
	swift-ring-builder object-1.builder rebalance
	```

	- Sau khi thực hiện lệnh trên, hệ thống sẽ tạo ra file `object-1.ring.gz` chính là ring tương ứng với policy có index = 1.
	
- copy file `object-1.ring.gz` đến các node mà chứa các thiết bị đã được thêm vào ring ở bước trước, ở đây là 2 node object3 và object4

	```sh
	scp /etc/swift/object-1.ring.gz root@10.10.10.195:/etc/swift
	scp /etc/swift/object-1.ring.gz root@10.10.10.196:/etc/swift
	```

- Restart các services

	```sh
	service memcached restart
	service swift-proxy restart
	```
	
- Tạo một container mới với policy là có tên là silver.

	```sh
	curl -v -X PUT -H 'X-Auth-Token: <your auth token>' \
	-H 'X-Storage-Policy: silver' http:<link xác của account>/container_silver
	```
	
	- Nếu lệnh trên báo lỗi thì reboot tất cả các server
	
- Kiểm tra lại metadata của container đã tạo.

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
	
	- `X-Storage-Policy: silver` như vậy đã cấu hình thành công