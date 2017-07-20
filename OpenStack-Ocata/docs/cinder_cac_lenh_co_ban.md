# Các lệnh cơ bản với cinder

## 1. Tạo, xóa, liệt kê, show volume
- Tạo một volume no-source

  ```sh
  openstack volume create --size <dung lượng volume> <tên volume>
  ```
  
  - dung lượng volume tính theo đơn vị GB
  
- Tạo một volume từ image

  ```sh
  openstack volume create --size <dung lượng volume> --image <tên hoặc ID của image> <tên volume>
  ```
  
- Tạo một volume từ volume khác

  ```sh
  openstack volume create --source <tên volume-source> --size <dung lượng volume> <tên volume>
  ```
  
- Tạo một volume từ một bản snapshot

  ```sh
  openstack volume create --snapshot <tên snapshot-source> --size <dung lượng volume> <tên volume>
  ```
  
- Xóa volume

  ```sh
  openstack volume delete <tên hoặc ID volume>
  ```
  
- Liệt kê các volume

  ```sh
  openstack volume list
  ```
  
- show volume

  ```sh
  openstack volume show <tên hoặc ID volume>
  ```
  
## 2. Snapshot volume
- Tạo snapshot

  ```sh
  openstack volume snapshot create --volume <tên hoặc ID của volume để snapshot> <tên snapshot>
  ```
  
- List ra danh sách các snapshot của volume

  ```sh
  openstack volume snapshot list
  ```
  
- Xóa snapshot

  ```sh 
  openstack volume snapshot delete <tên snapshot>
  ```
  
## 3. Attach và detach volume cho máy ảo
- Attach volume

  ```sh
  openstack server add volume <tên VM> <tên volume> --device <tên thiết bị add cho vm>
  ```
  
  ví dụ:
  
  ```sh
  openstack server add volume vm69 volume-empty2 --device /dev/vdb
  ```

- Detach volume

  ```sh
  openstack server remove volume <tên VM> <tên volume>
  ```