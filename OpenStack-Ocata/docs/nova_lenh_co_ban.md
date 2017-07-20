# Các lệnh nova cơ bản

## Quản lý flavor
- 1. Tạo mới 1 flavor

  ```sh
  openstack flavor create --id auto --ram <dung lượng ram> --disk <dung lượng disk> --vcpu <số lượng cpu> --public <tên flavor>
  ```
  
  - dung lượng ram tính theo đơn vị MB
  - dung lượng disk tính theo đơn vị GB
  
- 2. Liệt kê flavors

  ```sh
  openstack flavor list
  ```
  
- 3. show chi tiết 1 flavor

  ```sh
  openstack flavor show <tên hoặc ID của flavor>
  ```
  
- 4. Xóa bỏ 1 flavor

  ```sh
  openstack flavor delete <name or id của flavor>
  ```
  
## Quản lý keypair
- 1. Tạo một keypair

  ```sh
  ssh-keygen -q -N ""
  Enter file in which to save the key (/root/.ssh/id_rsa): <nhập tên của keypair>
  ```
  
- ví dụ:

  ```sh
  ~# ssh-keygen -q -N ""
  Enter file in which to save the key (/root/.ssh/id_rsa): mykey
  ```
  
  - Sau khi thực hiện lệnh ssh-keygen -q -N "", nhập tên file sẽ lưu cặp key này. Ở đây tên file là mykey
- Liệt kê ra các file key mà hệ thống đã tạo

  ```sh
  ~# ls
  mykey  mykey.pub
  ```
  
  - gồm 2 key: mykey chứa private key và mykey.pub chứa public key.
  
- 2. add public key vào openstack

  ```sh
  openstack keypair create --public-key <file chứa public key> <tên key>
  ```
  
  ví dụ:
  
  ```sh
  openstack keypair create --public-key ~/mykey.pub mykey
  ```
  
- 3. List tất cả các key pair có trong openstack.

  ```sh
  openstack keypair list
  ```
  
- 4. Xóa bỏ 1 keypair

  ```sh
  openstack keypair delete <tên keypair>
  ```
  
## 3. Tạo, xóa, tắt, bật, reboot, list máy ảo.
- 1. Tạo mới VM
- tạo từ image

  ```sh
  openstack server create --flavor <tên flavor> --image <tên image> \
  --nic net-id=<id của network> --security-group <tên security group> \
  --key-name <tên keypair> <tên vm>
  ```
  
- Tạo máy ảo từ volume
  
  ```sh
  openstack server create --flavor <tên flavor> --volume <tên volume> \
  --nic net-id=<id của network> --security-group <tên security group> \
  --key-name <tên keypair> <tên vm>
  ```
  
- 2. Xóa máy ảo

  ```sh
  openstack server delete <tên VM>
  ```
  
- 3. Tắt máy ảo

  ```sh
  openstack server stop <tên VM>
  ```
  
- 4. Bật máy ảo

  ```sh
  openstack server start <tên VM>
  ```
  
- 5. reboot một VM đang chạy.
  
  ```sh
  openstack server reboot <tên VM>
  ```
  
- 6. List tất cả VM

  ```sh
  openstack server list
  ```