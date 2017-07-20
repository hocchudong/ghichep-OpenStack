# Các lệnh cơ bản thường dùng trong Keystone

## 1. Lấy token
- Khai báo thông tin về cridentials của người dùng

  ```sh
  export OS_PROJECT_DOMAIN_NAME=Default
  export OS_USER_DOMAIN_NAME=Default
  export OS_PROJECT_NAME=admin
  export OS_USERNAME=admin
  export OS_PASSWORD=Welcome123
  export OS_AUTH_URL=http://controller:35357/v3
  export OS_IDENTITY_API_VERSION=3
  export OS_IMAGE_API_VERSION=2
  ```
  
  - cridential của user `admin` với mật khẩu là `Welcome123`
  
- Lệnh để lấy token

  ```sh
  openstack token issue`
  ```
  
- ví dụ:

  ```sh
  root@controller:~# openstack token issue
  +------------+-------------------------------------------------------------------------------------------------------------------------------------+
  | Field      | Value                                                                                                                               |
  +------------+-------------------------------------------------------------------------------------------------------------------------------------+
  | expires    | 2017-04-28T04:19:17+0000                                                                                                            |
  | id         | gAAAAABZArS1Qgi_MMYf6J4odgU-tU9eoBfD44Ob149egIzNrK_XpnovPkzh9xWp0wWiR4BDM-Vke76EFmk7dDoFtXIQtVksde-                                 |
  |            | 8uCJSgDJNIVAsgW_pLVR28qQ3DHIhSrcRXHGw8MLSdhMyPJjJrDYqKKhNh6iczBnLN4k9YoB3A52IZUrP9ug                                                |
  | project_id | 1667a274e14647ec8f2c0dd593e661de                                                                                                    |
  | user_id    | 3ce3ca843dc7458bb61c851d3a654b8b                                                                                                    |
  +------------+-------------------------------------------------------------------------------------------------------------------------------------+
  ```
  
## 2. Liệt kê các thông tin về users, projects, groups, roles, domains
- 1. liệt kê tất cả users

  ```sh
  openstack user list
  ```
  
- 2. Liệt kê tất cả projects

  ```sh
  openstack project list
  ```
  
- 3. Liệt kê tất cả groups

  ```sh
  openstack group list
  ```
  
- 4. Liệt kê roles

  ```sh
  openstack role list
  ```
  
- 5. Liệt kê domains

  ```sh
  openstack domain list
  ```

## 3. Tạo mới domain, project, user, role.
- 1. Tạo domain mới.

  ```sh
  openstack domain create <tên domain>
  ```
  
- Tạo project trong domain

  ```sh
  openstack project create --domain <tên domain> --description "<miêu tả về domain>" <tên project>
  ```

- Tạo user. User phải thuộc 1 domain, cần khai báo user thuộc domain nào

  ```sh
  openstack user create --domain <tên domain> --password <password> <tên user>
  ```
  
## 4. Gán role cho user, kiểm tra user có role gì.
- Gán role cho user

  ```sh
  openstack role add --project <tên project> --project-domain <tên domain> --user <tên user> --user-domain <tên domain> <tên role>
  ```
  
- Kiểm tra user có role gì

  ```sh
  openstack role list --user <tên user> --project <tên project>
  ```
  