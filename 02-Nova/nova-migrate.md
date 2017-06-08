# Tìm hiểu về Migrate NOVA.

# 1. Các loại Migrate .

Chúng ta có các kiểu Migrate như :

- Non-live migration : Instane sẽ tắt trong khoảng thời gian chuyển sang hypervisor khác.

- Live migration : Hầu như không có thời gian chết . Rất có ích vì các instane sẽ vẫn được chạy trong quá trình di chuyển.
Các loại Live migration : 

```sh
Shared storage-based live migration : Cả 2 hypervisor đều có thể truy cập vào file share storage.

Block live migration : No shared storage is required. Incompatible with read-only devices such as CD-ROMs and Configuration Drive (config_drive).

Volume-backed live migration : Instances are backed by volumes rather than ephemeral disk, no shared storage is required, and migration is supported 
(currently only available `for libvirt` based hypervisors).
```

## 2. Một số bài lab .

### 2.1. Di chuyển Instance từ AZ (Availability Zone) này sang AZ khác (Live migration).

Chúng ta thực hiện qua 2 bước cơ bản :

```sh
- Tạo Snapshot

- Khởi động instane bằng snapshot vừa tạo trên 1 AZ khác.
```

- Kiểm tra các hypervisor sẵn có :

```sh
nova hypervisor-list

+----+---------------------+-------+---------+
| ID | Hypervisor hostname | State | Status  |
+----+---------------------+-------+---------+
| 1  | compute1            | up    | enabled |
| 2  | compute2            | up    | enabled |
+----+---------------------+-------+---------+

```

- Kiểm tra các `zone` :

```sh
nova availability-zone-list | egrep -A 10 "^\| nova"


| nova-1                | available                              |
| |- compute1           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:47:49.000000 |
| nova                  | available                              |
| |- compute2           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:47:56.000000 |
+-----------------------+----------------------------------------+

```

- Kiểm tra thông tin Instance để biết chúng nằm trong AZ nào :

```sh
nova list --field name,status,OS-EXT-STS:vm_state,OS-EXT-AZ:availability_zone,OS-EXT-SRV-ATTR:hypervisor_hostname

+--------------------------------------+------+---------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name | Status  | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+------+---------+----------------------+------------------------------+--------------------------------------+
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem | SHUTOFF | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1  | SHUTOFF | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2  | SHUTOFF | stopped              | nova-1                       | compute1                             |
+--------------------------------------+------+---------+----------------------+------------------------------+--------------------------

# Ở đây chúng ta sẽ chuyển doem từ AZ nova sang AZ nova-1
```

- Tạo một snapshot từ instane `doem` :

```sh
root@controller:~# nova image-create --poll doem doem_ss

Server snapshotting... 100% complete
Finished

```

- Kiểm tra xem đã tạo thành công chưa :

```sh
root@controller:~# openstack image list

+--------------------------------------+---------+--------+
| ID                                   | Name    | Status |
+--------------------------------------+---------+--------+
| dff59356-0821-4ce5-a6b3-9b25aad72953 | doem_ss | active |
| acc8392e-e360-4c31-92e1-9115f2d04c33 | cirros  | active |

```

- Thực hiện boot instance trên AZ khác :

```sh
root@controller:~# nova boot demo_az_1 --flavor 1 --image dff59356-0821-4ce5-a6b3-9b25aad72953 --availability-zone nova-1 \ 
--nic net-id=4c711790-7cfc-42ab-8704-88d72680531a

+--------------------------------------+------------------------------------------------+
| Property                             | Value                                          |
+--------------------------------------+------------------------------------------------+
| OS-DCF:diskConfig                    | MANUAL                                         |
| OS-EXT-AZ:availability_zone          | nova-1                                         |
| OS-EXT-SRV-ATTR:host                 | -                                              |
| OS-EXT-SRV-ATTR:hostname             | demo-az-1                                      |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | -                                              |
| OS-EXT-SRV-ATTR:instance_name        | instance-00000006                              |
| OS-EXT-SRV-ATTR:kernel_id            |                                                |
| OS-EXT-SRV-ATTR:launch_index         | 0                                              |
| OS-EXT-SRV-ATTR:ramdisk_id           |                                                |
| OS-EXT-SRV-ATTR:reservation_id       | r-26gs3csc                                     |
| OS-EXT-SRV-ATTR:root_device_name     | -                                              |
| OS-EXT-SRV-ATTR:user_data            | -                                              |
| OS-EXT-STS:power_state               | 0                                              |
| OS-EXT-STS:task_state                | scheduling                                     |
| OS-EXT-STS:vm_state                  | building                                       |
| OS-SRV-USG:launched_at               | -                                              |
| OS-SRV-USG:terminated_at             | -                                              |
| accessIPv4                           |                                                |
| accessIPv6                           |                                                |
| adminPass                            | HV86mfACLj57                                   |
| config_drive                         |                                                |
| created                              | 2017-04-21T06:56:13Z                           |
| description                          | -                                              |
| flavor                               | m1.tiny (1)                                    |
| hostId                               |                                                |
| host_status                          |                                                |
| id                                   | 33c20114-3564-4095-baec-3bdd2af1efdc           |
| image                                | doem_ss (dff59356-0821-4ce5-a6b3-9b25aad72953) |
| key_name                             | -                                              |
| locked                               | False                                          |
| metadata                             | {}                                             |
| name                                 | demo_az_1                                      |
| os-extended-volumes:volumes_attached | []                                             |
| progress                             | 0                                              |
| security_groups                      | default                                        |
| status                               | BUILD                                          |
| tenant_id                            | 242e5fe186c04adfaa3e50f4b8f50a16               |
| updated                              | 2017-04-21T06:56:13Z                           |
| user_id                              | 9ab80ad692454a0496124528ef13ee51               |
+--------------------------------------+------------------------------------------------+

```

- Kiểm tra Instance :

```sh
nova list --field name,status,OS-EXT-STS:vm_state,OS-EXT-AZ:availability_zone,OS-EXT-SRV-ATTR:hypervisor_hostname

+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name      | Status  | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+
| 33c20114-3564-4095-baec-3bdd2af1efdc | demo_az_1 | ACTIVE  | active               | nova-1                       | compute1                             |
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem      | SHUTOFF | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1       | SHUTOFF | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2       | SHUTOFF | stopped              | nova-1                       | compute1                             |
+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+

```

- Show chi tiết thông tin về Instance vừa tạo :

```sh
root@controller:~# nova show demo_az_1 | egrep "Property|AZ|hypervisor| id |image"

| Property                             | Value                                                    |
| OS-EXT-AZ:availability_zone          | nova-1                                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | compute1                                                 |
| id                                   | 33c20114-3564-4095-baec-3bdd2af1efdc                     |
| image                                | doem_ss (dff59356-0821-4ce5-a6b3-9b25aad72953)           |

```

### 2.2. Non-live migration.

Có 2 trường hợp đối với Non-live migration :

- Không kết nối với cinder volume.

- Có kết nối với cinder volume.

```sh
Trong bài lab này tôi sẽ thực hiện TH1 là không có kết nối với Cinder Volume.
```

- Điều kiện để thực hiện bài lab :

```sh
- Nova Instane phải tắt
- Không có kết nối share storage
- Khi di chuyển phảo chỉ định compute node 
```

- Kiểm tra các `zone` :

```sh
nova availability-zone-list | egrep -A 10 "^\| nova"


| nova-1                | available                              |
| |- compute1           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:47:49.000000 |
| nova                  | available                              |
| |- compute2           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:47:56.000000 |
+-----------------------+----------------------------------------+

```

- Kiểm tra thông tin Instance để biết chúng nằm trong AZ nào :

```sh
nova list --field name,status,OS-EXT-STS:vm_state,OS-EXT-AZ:availability_zone,OS-EXT-SRV-ATTR:hypervisor_hostname

+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name      | Status  | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+
| 51d72e61-6125-4885-85aa-6f331a3f03a3 | demo01    | SHUTOFF | stopped              | nova                         | compute2                             |
| 33c20114-3564-4095-baec-3bdd2af1efdc | demo_az_1 | SHUTOFF | stopped              | nova-1                       | compute1                             |
| f11f98ac-286d-469f-8915-8bbde4fb3f1c | demo_zone | ACTIVE  | active               | nova                         | compute2                             |
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem      | SHUTOFF | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1       | SHUTOFF | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2       | SHUTOFF | stopped              | nova-1                       | compute1                             |
+--------------------------------------+-----------+---------+----------------------+------------------------------+--------------------------------------+


```

- Thực hiện migration :

```sh
nova migrate --poll vm2
Server migrating... 100% complete
Finished
```

- Kiểm tra trạng thái :

```sh
nova list --field name,status,OS-EXT-STS:vm_state,OS-EXT-AZ:availability_zone,OS-EXT-SRV-ATTR:hypervisor_hostname

+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name      | Status        | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| 51d72e61-6125-4885-85aa-6f331a3f03a3 | demo01    | SHUTOFF       | stopped              | nova                         | compute2                             |
| 33c20114-3564-4095-baec-3bdd2af1efdc | demo_az_1 | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| f11f98ac-286d-469f-8915-8bbde4fb3f1c | demo_zone | ACTIVE        | active               | nova                         | compute2                             |
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem      | SHUTOFF       | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1       | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2       | VERIFY_RESIZE | resized              | nova                         | compute1                             |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+

```

- Xác nhận migration :

```sh
nova resize-confirm vm2
```

- Kiểm tra :

```sh
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name      | Status        | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| 51d72e61-6125-4885-85aa-6f331a3f03a3 | demo01    | SHUTOFF       | stopped              | nova                         | compute2                             |
| 33c20114-3564-4095-baec-3bdd2af1efdc | demo_az_1 | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| f11f98ac-286d-469f-8915-8bbde4fb3f1c | demo_zone | ACTIVE        | active               | nova                         | compute2                             |
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem      | SHUTOFF       | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1       | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2       | SHUTOFF       | stopped              | nova                         | compute1                             |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
```

- Bật máy kiểm tra :

```sh
nova start vm2
```

- Kiểm tra :

```sh
nova list --field name,status,OS-EXT-STS:vm_state,OS-EXT-AZ:availability_zone,OS-EXT-SRV-ATTR:hypervisor_hostname

+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| ID                                   | Name      | Status        | OS-EXT-STS: Vm State | OS-EXT-AZ: Availability Zone | OS-EXT-SRV-ATTR: Hypervisor Hostname |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
| 51d72e61-6125-4885-85aa-6f331a3f03a3 | demo01    | SHUTOFF       | stopped              | nova                         | compute2                             |
| 33c20114-3564-4095-baec-3bdd2af1efdc | demo_az_1 | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| f11f98ac-286d-469f-8915-8bbde4fb3f1c | demo_zone | ACTIVE        | active               | nova                         | compute2                             |
| e97d3a7c-5549-4870-af71-0eebdd7ac3d0 | doem      | SHUTOFF       | stopped              | nova                         | compute2                             |
| 2ca1209c-c2dd-451e-bf53-d9103f400ba9 | vm1       | SHUTOFF       | stopped              | nova-1                       | compute1                             |
| 6a4e53cb-0cf3-4113-9571-c42aa9f1afa4 | vm2       | ACTIVE        | active               | nova                         | compute1                             |
+--------------------------------------+-----------+---------------+----------------------+------------------------------+--------------------------------------+
```

### 2.3. Migrate an Instance with Zero Downtime: OpenStack Live Migration with KVM Hypervisor and NFS Shared Storage.

- https://www.mirantis.com/blog/tutorial-openstack-live-migration-with-kvm-hypervisor-and-nfs-shared-storage/

# Đang cập nhật.
