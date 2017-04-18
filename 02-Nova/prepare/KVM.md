# Lab KVM .

## I. Mô hình.

## II. Thực hiện cài đặt.

- Cài đặt KVM và các gói liên quan :

```sh
apt-get install qemu-kvm libvirt-bin -y
```

- Cài đặt Linux-Bridge :

```sh
apt-get install bridge-utils
```

- Sau khi cài đặt xong dùng lệnh `brctl` để kiểm tra :

```sh
brctl
```

![brctl](/images/nova/brctl.png)


- Tại bridge với tên `br0` :

```sh
brctl addbr br0
```

- Gán interface `eth0` vào `br0` :

```sh
brctl addif br0 eth0
```

- Kiểm tra :

```sh
brctl show
```

![brctl_show](/images/nova/brctl_show.png)

- Sửa lại file cấu hình networking :

```sh
vi /etc/network/interfaces
```

- Sửa lại như sau :

```sh
#auto eth0 
#iface eth0 inet dhcp 

auto br0 
iface br0 inet dhcp 
        bridge_ports eth0 
        bridge_stp off 
        bridge_fd 0 
        bridge_maxwait 0
```

- Xóa địa chỉ của card eth0 (card thực hiện gắn vào br0) :

```sh
ip addr del ip/netmask dev eth0
```

- Lấy lại cấu hình mới nhất cho mạng :

```sh
ifdown -a && ifup -a
```

## III Thực hiện tạo máy ảo trên KVM. 

- Tạo ra thư mục lưu trữ các images :

```sh
mkdir -p /var/lib/images
```

- Thực hiện upload file `.iso` của hệ điều hành vào thư mục đó (có thể dùng winscp hay bất cứ phần mềm chuyển file nào tương tự)

- Trên `Moba X-term` Thực hiện cấu hình X11 remote access ở chế độ full :

![moba_config](/images/nova/moba_config.png)

- Thực hiện cài đặt gói `virt-manager` :

```sh
apt-get install virt-manager
```

- Sau khi cài đặt xong trên trình ssh (Moba X-term), thực hiện lệnh :

```sh
virt-manager
```

- Sau đó thực hiện tạo máy ảo như bình thường.\

# Đang bổ sung ...