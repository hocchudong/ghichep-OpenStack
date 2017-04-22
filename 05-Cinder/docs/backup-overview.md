# OpenStack Backups.

## 1. Backup là gì?

- Tất cả những thứ được lữu trữ bên ngoài thực thể lưu trữ chính được gọi là backup. Điều này có nghĩa là các máy chủ khác có khả năng 
được lưu trữ ở nhiều điểm khác nữa. Chúng ta có nhiều lựa chọn cho các phương pháp backup khác nhau có sẵn trong OpenStack. Tuy nhiên trên thực 
tế chúng ta chỉ cần sao lưu dữ liệu Cinder Block Storage là đủ. Nó được cung cấp bởi cinder-backup . Nó có 2 backends chính để backup vào 
đó là : Celph và Swift. Việc lựa chọn backends nào thì tùy thuộc vào chúng ta , tuy nhiên việc sử dụng Celph là một lựa chọn thích hợp hơn Swift 
bởi vì Celph đã được tối ưu hóa để làm việc với backup.

## 2. Backup level.

- Chúng ta có ba mức độ backup như sau :

1. Bloack level : LVM snapshot.

2. Filesystem level : rsync.

3. Application level: SQL dump.

### Block Level.

- Vấn đề chính của phương pháp này là sự không nhất thống mà nó mang lại . Có thể trong một số trường hợp xấu có thể làm hư hỏng tệp tin.

|Ưu điểm|Nhược điểm|
|-------|----------|
|Nhanh chóng, không tương tác với với VM chỉ có lớp khối |Hệ thống filesystem không biết|
|Phục hồi nhanh (chỉ cần chạy một máy ảo mới)|Không thể thực hiện được trực tiếp (hạn chế trình điều khiển cinder backup)|
|Tích hợp với OpenStack cinder-backup|Trạng thái phục hồi không nhất quán|
|Không thể xâm nhập||
|Gia tăng được khối lượng sao lưu||

### File Level.

- Ví dụ : Backup PC.

|Ưu điểm|Nhược điểm|
|-------|----------|
|Kiểm soát được dữ liệu sâu nhất có thể (Có thể khôi phục một file) |Yêu cầu backup agent|
|Có nhiều không gian (dedup and hảdlinks)|Tiêu thụ băng thông lớn|

### Application level.

-  Ví dụ như backup cớ sở dữ liệu.

|Ưu điểm|Nhược điểm|
|-------|----------|
|Triggered by freeze hook script from QEMU agent|Cần sự phối hợp (Khá phức tạp với DBs và multi-master setups)|
|Có tính nhất quán||
|Autonomus (hệ thống tự quản)||



# Backup Volume với backend NFS.

## I. Mô hình và các yêu cầu phần cứng.

### Mô hình

![mohinh_nfs_backup](/images/cinder/storage/mohinh_nfs_backup.png)

### Phân hoạch địa chỉ IP và yêu cầu phần cứng :

![ip_plan](/images/cinder/storage/ip_plan.png)

## II. Cài đặt.

- Lưu ý : Trên mô hình phải được cài đặt sẵn OpenStack và Cinder, nếu chưa có tham khảo tại [đây](https://github.com/congto/OpenStack-Mitaka-Scripts/tree/master/OPS-Mitaka-LB-Ubuntu)

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





# Tham Khảo

- https://www.sebastien-han.fr/blog/2015/02/17/openstack-and-backup/
- https://www.snia.org/sites/default/files/SDCIndia/2016/Presentations/Using%20Object%20Storage%20to%20store%20and%20restore%20Cinder%20Volume%20backups.pdf