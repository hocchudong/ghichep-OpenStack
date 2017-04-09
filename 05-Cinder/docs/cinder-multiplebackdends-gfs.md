# Cinder multiple backends (LVM, NFS, GlusterFS)

## I. Thiết lập chung.

### 1. Mô hình.

![multiple_backends-mohinh](/images/cinder/multiple_backends-mohinh.png)

### 2. Phân hoạch địa chỉ IP và yêu cầu phần cứng đối với cụm máy chủ.

![phanhoach-multiple](/images/cinder/phanhoach-multiple.png)

## II. Cài đặt.

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

10.10.10.50:/datapoint
```

- Dùng trình soạn thảo `vi` mở file `/etc/cinder/nfs_shares` :

```sh
vi /etc/cinder/nfs_shares 
```

Thêm vào nội dung :

```sh
10.10.10.40:/storage 
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

### 3. Trên Node gf1 và gf2 (thực hiện tương tự) :

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

- Cài đặt gói `glusterfs-server`

```sh
apt-get install glusterfs-server
```

- Trên cả 2 node kiểm tra xem 2 node này đã được kết nối với nhau hay chưa :

```sh
gluster peer probe gfs1
gluster peer probe gfs2
gluster peer status
```

- Tạo thư mục trên cả 2 node , dùng để mount dữ liệu :

```sh
mkdir -p /mnt/gluster
```

- Khởi tạo volume :

```sh
gluster  volume create datapoint replica 2 transport tcp  gluster1:/mnt/gluster  gluster2:/mnt/gluster force
```

- Start volume :


```sh
gluster volume start datapoint
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
mount -t glusterfs 10.10.10.50:/datapoint /mnt 
```

- Kiểm tra :

```sh
df -h 
```

![gfs-mount](/images/cinder/gfs-mount.png)