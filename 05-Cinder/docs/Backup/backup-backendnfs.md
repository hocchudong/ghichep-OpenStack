# Backup Volume với backend NFS.

## I. Mô hình và các yêu cầu phần cứng.

### Mô hình

![mohinh_nfs_backup](/images/cinder/storage/mohinh_nfs_backup.png)

### Phân hoạch địa chỉ IP và yêu cầu phần cứng :

![ip_plan](/images/cinder/storage/ip_plan.png)

## II. Cài đặt.

### 1. Trên node NFS :

- Tạo các thư mục `backup_mount` và `cinder_backup`

```sh
mkdir -p /mnt/backup_mount
mkdir -p /mnt/cinder_backup
```

- Mở file `exports` :

```sh
vi /etc/exports
```

Thêm vào dòng sau :

```sh
10.10.10.0/24 /mnt/cinder_backup 10.10.10.0/24(rw,no_root_squash)
```

- Restart lại dịch vụ :

```sh
service nfs-kernel-server restart
```

### 2. Trên node Cinder.

-  Cài đặt các gói `sysfsutils` và `cinder-backup` :

```sh
apt-get install sysfsutils
apt-get install cinder-backup
```

- Dùng trình soạn thảo vi mở file `cinder.conf` :

```sh
vi /etc/cinder/cinder.conf
```

- Chỉnh sửa lại file `cinder.conf` như sau :

Tại section [DEFAULT] thêm vào các dòng sau :

```sh
backup_driver = cinder.backup.drivers.nfs
backup_mount_point_base = /mnt/backup_mount
backup_share = 10.10.10.40:/mnt/cinder_backup
```

- Tạo thư mục `/mnt/cinder_backup` và `/mnt/backup_mount` :

```sh
mkdir -p /mnt/cinder_backup
mkdir -p /mnt/backup_mount
```

- Phân quyền cho 2 thư mục vừa tạo :

```sh
chown cinder:cinder /mnt/cinder_backup
chown cinder:cinder /mnt/backup_mount
```

- Mount thư mục `/mnt/cinder_backup` về node cinder :

```sh
mount -t nfs 10.10.10.40:/mnt/cinder_backup /mnt/cinder_backup
```

- Restart lại các dịch vụ :

```sh
service cinder-volume restart
service cinder-backup restart
```

## III. Kiểm tra.

- Tạo một file backup bằng lệnh :

```sh
cinder backup-create disk_nfs-2 --name demo
```

Trong đó :

|Lệnh|Ý nghĩa|
|----|-------|
|cinder backup-create|Là lệnh khởi tạo mới một backup|
|disk_nfs-2|Tên volume cần backup|
|--name demo|--name : tùy chọn đặt tên cho file backup . demo : là tên file backup muốn đặt.|

Kết quả trả về của lệnh trên :

![kq_lenh](/images/cinder/storage/kq_lenh.png)

- Kiểm tra xem volume đã được tạo thành công chưa :

```sh
cinder backup-list
```

![backup_list](/images/cinder/storage/backup_list.png)

- Kiểm tra trên node NFS :

![file_backup](/images/cinder/storage/file_backup.png)


