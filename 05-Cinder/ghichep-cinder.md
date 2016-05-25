# Các ghi chép về cinder

## Các chú ý về volume
- Có 2 cách sử dụng volume: (http://prntscr.com/b8a9l7)
 - Sử dụng để gắn vào máy ảo đã được tạo trước đó: `bootable =  false`
 - Sử dụng để boot máy ảo: `bootable =  true`
- Khi tạo volume (chưa gắn vào máy nào) thì tại thư mục `/var/lib/cinder/volume` chưa xuất hiện volume. Khi thực hiện gắn (attach) vào VM nào đó thì mới có volume tại thư mục trên. Khi gỡ volume thì file đó sẽ biến mất trên node cinder

- Nếu tách máy Cinder thành 1 node (Cinder node) khác và không sử dụng backend thì mặc định volume được tạo ra sẽ lưu tại node cinder.

- Nếu boot máy ảo từ volume, file máy ảo sẽ nằm trên node Cinder. Node compute sẽ mount tới node cinder thông qua iscsi: http://prntscr.com/b8a7b3

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

- Gắn volume và gỡ volume khỏi máy ảo
```sh
# Cú pháp lệnh gắn volume
openstack server add volume INSTANCE_NAME VOLUME_NAME

# Cú pháp lệnh gỡ volume
openstack server remove volume INSTANCE_NAME VOLUME_NAME

# Trong đó: 
 - INSTANCE_NAME: Tên máy ảo
 - VOLUME_NAME: Tên volume

# Ví dụ:
openstack server add volume vm01 volume01 # Gắn vào máy ảo

 openstack server remove volume vm99999000 vol01-demo # Gỡ ra khỏi máy ảo.
```