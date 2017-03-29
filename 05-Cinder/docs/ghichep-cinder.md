# Các ghi chép về cinder

## Các chú ý về volume
- Có 2 cách sử dụng volume: (http://prntscr.com/b8a9l7)
 - Sử dụng để gắn vào máy ảo đã được tạo trước đó: `bootable =  false`
 - Sử dụng để boot máy ảo: `bootable =  true`
- File chứa trong thư mục `/var/lib/cinder/volumes` các các file quản lý volume được tạo ra, trong đó có đường dẫn tới volume.
```
root@cinder:/var/lib/cinder/volumes# cat volume-aa2f2db8-c93b-41ca-9119-d74310caa995

<target iqn.2010-10.org.openstack:volume-aa2f2db8-c93b-41ca-9119-d74310caa995>
    backing-store /dev/cinder-volumes/volume-aa2f2db8-c93b-41ca-9119-d74310caa995
    driver iscsi
    incominguser j5GJW8rYpq5cmd263oXE JCYsTBXrX26ium4F

    write-cache on
</target>
```

- Kiểm tra các volume trên LVM bằng lệnh: http://prntscr.com/b8xoz4
```sh
lvs

hoặc 

lsbkl


```

- Volume được tạo trên LVM KHÔNG sử dụng cơ chế `thin` để cấp phát dung lượng lưu trữ (tạo bao nhiêu cấp bấy nhiêu.)

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