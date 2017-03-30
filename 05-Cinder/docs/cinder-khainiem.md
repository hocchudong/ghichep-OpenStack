# Các khái niệm :

```sh
Block Storage
```

- Block Storage : hay còn được gọi là Volume storage được gắn vào các VMs dưới dạng volumes . Trong OpenStack Cinder là mã phần mềm triển khai block storage.
Các volumes này là "persistent" có nghĩa là các volume này có thể gán cho 1 instane rồi gỡ bỏ và gán cho instane khác mà vẫn giữ nguyên dữ liệu. Các loại Block 
Storage cho phép các instane truy cập trực tiếp đến phần cứng storage của thiết bị thật , việc này giúp tăng hiệu suất đọc/ghi I/O  
 (http://blogit.edu.vn/cac-loai-storage-trong-openstack/)
- Các volume có vòng đời phụ thuộc vào thời gian sống của VM.
- Tương tự như Amazon Elastic Block Store (EBS)

```sh
AMQP
```

- RabbitMQ là một message broker ( message-oriented middleware) sử dụng giao thức AMQP - Advanced Message Queue Protocol (Đây là giao thức phổ biến, thực tế rabbitmq hỗ trợ nhiều giao thức). RabbitMQ được lập trình bằng ngôn ngữ Erlang. RabbitMQ cung cấp cho lập trình viên một phương tiện trung gian để giao tiếp giữa nhiều thành phần trong một hệ thống lớn ( Ví dụ openstack).
-  RabbitMQ sẽ nhận message đến từ các thành phần khác nhau trong hệ thống, lưu trữ chúng an toàn trước khi đẩy đến đích.

```sh
iSCSI
```

- Trong hệ thống mạng máy tính, iSCSI (viết tắt của internet Small Computer System Interface) dựa trên giao thức mạng internet (IP) để kết nối các cơ sở dữ liệu.
- Nói một cách đơn giản nhất, iSCSI sẽ giúp tạo 1 ổ cứng Local trong máy tính của bạn với mọi chức năng y như 1 ổ cứng gắn trong máy tính vậy. Chỉ khác ở chỗ dung 
lượng thực tế nằm trên NAS và do NAS quản lý.

Tham khảo : http://ducquang415.com/view-45717/iscsi-la-gi-gioi-thieu-cach-map-o-cung-nas-thanh-1-o-cung-local/