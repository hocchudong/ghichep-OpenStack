# Cinder multiple backends (LVM, NFS, GlusterFS)

## I. Thiết lập chung.

### 1. Mô hình.

![multiple_backends-mohinh](/images/cinder/multiple_backends-mohinh.png)

### 2. Phân hoạch địa chỉ IP và yêu cầu phần cứng đối với cụm máy chủ.

![phanhoach-multiple](/images/cinder/phanhoach-multiple.png)

## II. Cài đặt.

- Lưu ý : Trên mô hình phải được cài đặt sẵn OpenStack và Cinder, nếu chưa có tham khảo tại [đây](https://github.com/congto/OpenStack-Mitaka-Scripts/tree/master/OPS-Mitaka-LB-Ubuntu)

- Với mô hình trên LVM đã được cài đặt và thiết lập trước đó, ở bài này chỉ giới thiệu về glusterfs và nfs.

- Xem chi tiết thiết lập Cinder và LVM tại [đây](https://github.com/hocchudong/ghichep-OpenStack/blob/master/05-Cinder/docs/cinder-install.md)

### 1. Trên node Cinder.

- Cài đặt các gói `nfs-common` và `glusterfs-client` :

```sh
apt-get -y install nfs-common glusterfs-client 
```

- Dùng trình soạn thảo `vi` mở file cinder config :

```sh
vi /etc/cinder/cinder.conf 
```

- Tại đây chúng ta tiến hành các chỉnh sửa như sau :

Tại section [default] tìm và sửa dòng `enabled_backends` như sau :

```sh
enabled_backends = lvm,nfs,glusterfs
```

Thêm section nfs với nội dung như sau :

```sh
[nfs]
volume_driver = cinder.volume.drivers.nfs.NfsDriver
volume_backend_name = NFS
nfs_shares_config = /etc/cinder/nfs_shares
nfs_mount_point_base = $state_path/mnt_nfs 
```

Thêm section [glusterfs] với nội dung như sau :

```sh
[glusterfs]
volume_driver = cinder.volume.drivers.glusterfs.GlusterfsDriver
volume_backend_name = GlusterFS
glusterfs_shares_config = /etc/cinder/glusterfs_shares
glusterfs_mount_point_base = $state_path/mnt_glusterfs
```

- Dùng trình soạn thảo `vi` mở file `/etc/cinder/glusterfs_shares` :

```sh
vi /etc/cinder/glusterfs_shares
```

Thêm vào nội dung :

```sh
# create new : specify GlusterFS volumes

10.10.10.50:/testvol2

# testvol2 là trên của volume mà chúng ta sẽ tạo tạo GFS server.
```

- Dùng trình soạn thảo `vi` mở file `/etc/cinder/nfs_shares` :

```sh
vi /etc/cinder/nfs_shares 
```

Thêm vào nội dung :

```sh
10.10.10.40:/nfsshare
# /nfsshare là thư mục mà chúng ta sẽ share khi cấu hình NFS.
```

- Thực hiện phân quyền và restart lại dịch vụ :

```sh
chmod 640 /etc/cinder/nfs_shares /etc/cinder/glusterfs_shares 
chgrp cinder /etc/cinder/nfs_shares /etc/cinder/glusterfs_shares 
initctl restart cinder-volume
```

### 2. Trên node compute.

- Cài đặt các gói `nfs-common` và `glusterfs-client` :

```sh
apt-get -y install nfs-common glusterfs-client 
```

- Dùng trình soạn thảo `vi` chỉnh sửa file cấu hình nova :

```sh
vi /etc/nova/nova.conf 
```

- Tại section default thêm 2 dòng sau :

```sh
osapi_volume_listen = 0.0.0.0
volume_api_class = nova.volume.cinder.API
```

- Restart lại dịch vụ :

```sh
initctl restart nova-compute 
```

### 3. Trên Node gfs1 và gfs2 (thực hiện tương tự) :

- Dùng trình soạn thảo `vi` để mở file hosts :

```sh
vi /etc/hosts
```

- Sửa lại file host như sau :

```sh
127.0.0.1       localhost gfs1(gfs2) // Trên node gfs1 đặt là gfs1, trên node gfs2 đặt là gfs2
10.10.10.10    controller
10.10.10.20   compute1
10.10.10.130    cinder
10.10.10.50     gfs1
10.10.10.60     gfs2
10.10.10.40     nfs
10.10.10.30     gfs-client
```

- Reboot lại máy chủ để lấy cấu hình mới nhất :

```sh
init 6
```

- Thực hiện phân vùng ổ cứng :

```sh
fdisk /dev/sdb
```

![phanvung-gfs](/images/cinder/phanvung-gfs.png)

- Tải gói định dạng xfs :

```sh
apt-get install xfsprogs -y
```

- Format phân vùng vừa tạo với định dạng xfs :

```sh
mkfs.xfs /dev/sdb1
```

- Mount partition vào thư mục /mnt và tạo thư mục /mnt/brick1

```sh
mount /dev/sdb1 /mnt && mkdir -p /mnt/brick1
```

- Khai báo vào file cấu hình /etc/fstab để khi restart server, hệ thống sẽ tự động mount vào thư mục:

```sh
echo "/dev/sdb1 /mnt xfs defaults 0 0" >> /etc/fstab
```

- Cài đặt gói `glusterfs-server`

```sh
apt-get install glusterfs-server
```

### Tiếp tục thực hiện trên gfs2

-  Tạo 1 pool storage với Server gfs1:

```sh
gluster peer probe gfs1
```

- Kiểm tra trạng thái của gluster pool

```sh
gluster peer status
```


- Khởi tạo volume :

```sh
gluster  volume create testvol2 replica 2 transport tcp  gfs1:/mnt/brick1  gfs2:/mnt/brick1
```

- Start volume :


```sh
gluster volume start testvol2
```

### 4. Trên node gfs-client.

- Dùng trình soạn thảo `vi` để mở file hosts :

```sh
vi /etc/hosts
```

- Sửa lại file host như sau :

```sh
127.0.0.1       localhost gfs-client
10.10.10.10    controller
10.10.10.20   compute1
10.10.10.130    cinder
10.10.10.50     gfs1
10.10.10.60     gfs2
10.10.10.40     nfs
10.10.10.30     gfs-client
```

- Reboot lại máy chủ để lấy cấu hình mới nhất :

```sh
init 6
```

- Cài đặt gói `glusterfs-client ` :

```sh
glusterfs-client 
```

- Thực hiện mount từ thư mục tạo trên gfs server :

```sh
mount -t glusterfs 10.10.10.50:/testvol2 /mnt 
```

- Kiểm tra :

```sh
df -h 
```

![gfs-mount](/images/cinder/gfs-mount.png)

### 5. Cài đặt NFS 

#### 5.1. Cài đặt trên node nfs.

- Update các gói cài đặt :

```sh
apt-get update
```

- Chỉnh sửa file hosts:

```sh
127.0.0.1       localhost nfs
10.10.10.10    controller
10.10.10.20   compute1
10.10.10.130    cinder
10.10.10.50     gfs1
10.10.10.60     gfs2
10.10.10.40     nfs
10.10.10.30     gfs-client
10.10.10.41     nfs-client

```

- Reeboot lại máy chủ để lấy cấu hình mới nhất :

```sh
init 6
```

- Phân vùng ở cứng :

```sh
fdisk /dev/sdb
```

![phanvung-gfs](/images/cinder/phanvung-gfs.png)

- Tải gói định dạng xfs :

```sh
apt-get install xfsprogs -y
```

- Format phân vùng vừa tạo với định dạng xfs :

```sh
mkfs.xfs /dev/sdb1
```

- Mount partition vào thư mục /mnt :

```sh
mount /dev/sdb1 /mnt
```

- Tạo thư mục /mnt/nfs :

```sh
mkdir -p /mnt/nfs
```

- Cài đặt gói `nfs-kernel-server` :

```sh
apt-get -y install nfs-kernel-server
```

- Thực hiện lệnh

```sh
echo "10.10.10.0/24 /mnt/nfs 10.10.10.0/24(rw,no_root_squash)" >> /ect/exports
```

Cho phép mount thư mục /mnt/nfs đến dải 10.10.10.0/24

- Thực hiện lệnh :

```sh
echo "/dev/sdb1 /mnt xfs defaults 0 0" >> /etc/fstab
```

Để hệ thống tự động mount vào thư mục khi restart hệ thống.

- Khởi động lại NFS :

```sh
/etc/init.d/nfs-kernel-server restart
```

#### 5.2. Cài đặt trên node nfs-client (Chỉ mang mục đích thử nghiệm quá trình mount đã thành công hay chưa).

- Update các gói cài đặt :

```sh
apt-get update
```

- Chỉnh sửa file hosts:

```sh
127.0.0.1       localhost nfs-client
10.10.10.10    controller
10.10.10.20   compute1
10.10.10.130    cinder
10.10.10.50     gfs1
10.10.10.60     gfs2
10.10.10.40     nfs
10.10.10.30     gfs-client
10.10.10.41     nfs-client

```

- Reeboot lại máy chủ để lấy cấu hình mới nhất :

```sh
init 6
```

- Cài đặt gói `nfs-common` :

```sh
apt-get -y install nfs-common
```

- Tạo thư mục `/mnt/a` để mount thư mục từ nfs server về :

```sh
mkdir -p /mnt/a
```

- Thực hiện mount thư mục `mnt/nfs` về thư mục `/mnt/a` :

```sh
mount 10.10.10.40:/mnt/nfs /mnt/a
```

- Kiểm tra :

```sh
df -h
```

![nfs-mount](/images/cinder/nfs-mount.png)

#### 5.3. Cài đặt trên node Cinder.

- Thực hiện lệnh :

```sh
echo "/dev/sdb1 /mnt xfs defaults 0 0" >> /etc/fstab
```

Để hệ thống tự động mount vào thư mục khi restart hệ thống.



## II. Kiểm thử.

### Trên node controller , chúng ta thực hiện cấu hình backends :

- Kiểm tra xem các backends đã kết nối được đến Cinder hay chưa :

```sh
cinder service-list
```

![service_list_test](/images/cinder/service_list_test.png)

- Tạo volume-type cho glusterfs :

```sh
cinder type-create glusterfs
cinder type-create nfs
```

- Kiểm tra cinder type-list :

![cinder-type-list](/images/cinder/cinder-type-list.png)

- Tạo một volume có backends gfs để thử nghiệm :

```sh
cinder create --display_name disk01 10 --volume-type glusterfs
```

![create-volume-gfs](/images/cinder/create-volume-gfs.png)

- Kiểm tra tình trạng của volume :

```sh
cinder list
```

![kiemtra-gfs](/images/cinder/kiemtra-gfs.png)

- Tạo một volume có backends nfs để thử nghiệm :

```sh
cinder create --display_name disk_nfs-2 --volume-type nfs 10
```

- Kiểm tra tình trạng của Volume :

```sh
cinder list
```

![cinder_test_nfs](/images/cinder/cinder_test_nfs.png)

- Kiểm tra lại xem volume có được lưu trữ trên backends chỉ định hay không (thực hiện trên backends server ) :

![check_backends](/images/cinder/check_backends.png)

# Tham Khảo :

http://www.tecmint.com/how-to-setup-nfs-server-in-linux/