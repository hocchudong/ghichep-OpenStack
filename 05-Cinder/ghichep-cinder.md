# Các ghi chép về cinder

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
 - VOLUME_NAME: Tên volime

# Ví dụ:
openstack server add volume volume01 vm01
```