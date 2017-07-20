# Các lệnh cơ bản thường dùng trong Glance

-  1. Liệt kê các image trong hệ thống

  ```sh
  openstack image list
  ```
  
- 2. show thông tin chi tiết về một image

  ```sh
  openstack image show <tên hoặc ID của image>
  ```
  
- 3. Xóa image

  ```sh
  openstack image delete <tên hoặc ID của image>
  ```
  
- 4. Upload một image lên glance

  ```sh
  openstack image create "<tên image>" \
  --file <file image cần upload> \
  --disk-format qcow2 --container-format bare \
  --public
  ```  