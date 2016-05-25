# Các ghi chép về cinder

## Các chú ý về volume
- Khi tạo volume (chưa gắn vào máy nào) thì tại thư mục `/var/lib/cinder/volume` chưa xuất hiện volume. Khi thực hiện gắn (attach) vào VM nào đó thì mới có volume tại thư mục trên.

- Nếu tách máy Cinder thành 1 node khác thì mặc định volume được tạo ra sẽ lưu tại máy đó.

- Nếu boot máy ảo từ volume, file chứa máy ảo sẽ nằm trên node Cinder. Node compute sẽ mount tới node cinder thông qua iscsi: http://prntscr.com/b8a7b3

## Các lệnh về volume

- Khởi động các dịch vụ của `Cinder`
```sh
# Trên Controller
service cinder-api restart
service cinder-scheduler restart

# Trên Cinder node (nếu triển khai tách node cinder)
service tgt restart
service cinder-volume restart
```

- Tạo volume
```sh
# Cú pháp đối với OpenStack Mitaka
openstack volume create --size kich_thuoc ten_volume

# Ví dụ tạo volume có kích thước 1Gb và tên là `volume01`
openstack volume create --size 1  volume01 
```

- Kiểm tra danh sách các volume
```sh
openstack volume list
```

- Gắn volume vào máy ảo
```sh
# Cú pháp lệnh
openstack server add volume INSTANCE_NAME VOLUME_NAME

# Trong đó: 
 - INSTANCE_NAME: Tên máy ảo
 - VOLUME_NAME: Tên volume

# Ví dụ:
openstack server add volume vm01 volume01
```