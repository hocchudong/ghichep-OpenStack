## GHI CHÉP VỀ OPENSTACK OCATA

### Cài đặt
- [1. Hướng dẫn cài đặt core Openstack Ocata](./docs/install.md)
- [2. Hướng dẫn cài đặt node Block Storage](./docs/install_block.md)

### File cấu hình 
- [File cấu hình Keystone](./files/keystone.conf)
- File cấu hình Glance
  - [File cấu hình glance-api](./files/glance-api.conf)
  - [File cấu hình glance-registry](.files/glance-registry.conf)
- File cấu hình nova
  - [File cấu hình nova trên node controller](./files/nova.conf)
  - [File cấu hình nova trên node compute1](./files/nova1.conf)

- [File cấu hình Neutron (đang cập nhật)]
- [File cấu hình cinder](./files/cinder.conf)

### Giải thích file cấu hình
- [1. File cấu hình của Keystone](./docs/Ghi_Chep_File_Config_Keystone.md)
- [2. File cấu hình Glance (đang cập nhật)]
- [3. File cấu hình của Nova](./docs/file_config_nova.md)
- [4. File cấu hình Neutron (đang cập nhật)]

## Lab admin
---

### Lab keystone
- [1. Lab keystone cơ bản](./docs/Cach_Su_Dung_Keystone.md)
- [2. Chuyển từ fernet-token sang UUID token](./docs/Chuyen_Tu_Fernet_Sang_UUID.md)
- [3. Định nghĩa một role](./docs/Define_role.md)
- [4. Thiết lập thời gian tồn tại của token](./docs/Guide_set_Time_token.md)

### Lab glance
- [1. Một số lệnh quản trị với glance](./docs/Command_line_glance.md)
- [2. Thiết lập multiple store locations for glance images](./docs/Multi_store_locations.md)
- [3. Một số thao tác với lệnh cURL](./docs/Curl_glance.md)
- [4. Guide định nghĩa role trong glance](./docs/Guide_define_role.md)

### Lab nova
- [Lab nova cơ bản](./docs/Lab_nova_basic.md)

### Lab neutron
(đang cập nhật)
### Lab cinder
- [Lab cinder cơ bản](./docs/Lab_cinder_basic.md)

---

- [Sự khác nhau khi tạo VM từ image và volume](./docs/Launch.md)

### Lab end user (horizon)
- [Hướng dẫn tạo máy ảo trên dashboard](./docs/Tao_may_ao_voi_dashboard.md)