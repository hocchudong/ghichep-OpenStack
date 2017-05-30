# Cấu hình openstack trong kolla
File cấu hình các service trong kolla là `/etc/kolla/globals.yaml`

Dựa vào file cấu hình này mà ansible sẽ tạo ra file config đối với các service.

Chúng ta sẽ tìm hiểu về nội dung cấu hình trong file này.


## 1. Cấu hình kolla
```sh
###################
# Kolla options
###################

# Valid options are [ centos, oraclelinux, ubuntu ]
#- kolla_base_distro: "centos"`

# Valid options are [ binary, source ]
#kolla_install_type: "binary"

# Valid option is Docker repository tag
#openstack_release: ""

# This should be a VIP, an unused IP on your network that will float between
# the hosts running keepalived for high-availability. When running an All-In-One
# without haproxy and keepalived, this should be the first IP on your
# 'network_interface' as set in the Networking section below.
- `kolla_internal_vip_address: "10.10.10.254"
```

- `kolla_base_distro: "centos"`: Image các service trong openstack dựa trên nền distro nào?
- `kolla_install_type: "binary"`: Image các service có dưới 2 dạng là binary và source. Tham khảo tại repo chứa image trên docker. https://hub.docker.com/u/kolla/
- `openstack_release`: Phiên bản image của các service. Mặc định nó sẽ lấy phiên bản mới nhất. Phiên bản mới nhất hiện tại là 4.0.0.
- `kolla_internal_vip_address: "10.10.10.254"`: Địa chỉ VIP chạy HA proxy và keepalived.

## 2. Cấu hình docker.

```sh
####################
# Docker options
####################

#docker_registry: "172.16.0.10:4000"
#docker_namespace: "companyname"
#docker_registry_username: "sam"
#docker_registry_password: "correcthorsebatterystaple"
```

- Cấu hình repository là nơi chứa image của các service openstack. Nếu không cấu hình, mặc định docker sẽ pull các image từ docker hub. https://hub.docker.com/u/kolla/

## 3. Cấu hình Network
```sh
###############################
# Neutron - Networking Options
###############################

#network_interface: "eth0"
#`neutron_external_interface: "eth1"
# Valid options are [ openvswitch, linuxbridge ]
#neutron_plugin_agent: "openvswitch"
```

- `network_interface`: interface kết nối các service trên các node.
- `neutron_external_interface`: interface kết nối ra mạng external.
- `neutron_plugin_agent`: Sử dụng giải pháp network nào? Có 2 lựa chọn là openvswitch hoặc linuxbridge.

## 4. Cấu hình OpenStack
```sh
####################
# OpenStack options
####################

# Valid options are [ novnc, spice ]
#nova_console: "novnc"
# OpenStack services can be enabled or disabled with these options
#enable_aodh: "no"
#enable_barbican: "no"
#enable_ceilometer: "no"
#enable_central_logging: "no"
#enable_ceph: "no"
#enable_ceph_rgw: "no"
#enable_chrony: "no"
#enable_cinder: "no"
#enable_cinder_backend_hnas_iscsi: "no"
#enable_cinder_backend_hnas_nfs: "no"
#enable_cinder_backend_iscsi: "no"
#enable_cinder_backend_lvm: "no"
#enable_cinder_backend_nfs: "no"
#enable_cloudkitty: "no"
#enable_collectd: "no"
#enable_congress: "no"
#enable_designate: "no"
#enable_destroy_images: "no"
#enable_etcd: "no"
#enable_freezer: "no"
#enable_gnocchi: "no"
#enable_grafana: "no"
#enable_heat: "yes"
#enable_horizon: "yes"
```

- `nova_console: "novnc": Console đến nova bằng phương pháp nào?
- `enable_horizon: "yes"``: Cấu hình sẽ cài đặt các service nào. (yes or no).

### 4.1 Cấu hình keystone
```sh
##############################
# Keystone - Identity Options
##############################

# Valid options are [ uuid, fernet ]
#`keystone_token_provider: 'uuid'`
#fernet_token_expiry: 86400
```

- `keystone_token_provider: 'uuid'`: Sử dụng dạng token nào.
- `fernet_token_expiry: 86400`: Thời gian hết hạn của token fernet.

## 4.2 Cấu hình glance
```sh
#########################
# Glance - Image Options
#########################
# Configure image backend.
#glance_backend_file: "yes"
#glance_backend_ceph: "no"
```

- Cấu hình backend chứa image là file hay ceph?

## 4.3 Cấu hình nova

```sh
#########################
# Nova - Compute Options
#########################
#nova_backend_ceph: "{{ enable_ceph }}"
```

Cấu hình nova có sử dụng ceph không?

## 4.4 Cấu hình cinder
```sh
#################################
# Cinder - Block Storage Options
#################################
# Enable / disable Cinder backends
#cinder_backend_ceph: "{{ enable_ceph }}"
#cinder_volume_group: "cinder-volumes"
#cinder_backup_driver: "nfs"
#cinder_backup_share: ""
#cinder_backup_mount_options_nfs: ""
```

Cấu hình cinder có sử dụng ceph?

#### Ngoài ra còn cấu hình các dịch vụ khác. Các bạn tham khảo file mẫu `globals.yaml` trong thư mục `file_config`.