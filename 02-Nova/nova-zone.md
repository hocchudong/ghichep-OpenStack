# Thao tác nova zone.

## 1. Tạo mới 1 zone .

- Để làm được bài lab này chúng ta cần có thêm 1 node compute nữa, đóng vai trò là zone thứ 2.

### Các bước thực hiện :

- Đầu tiên chúng ta sẽ tạo ra 1 `zone` như sau :


```sh
nova aggregate-create datpt nova-1

+----+-----------------+-------------------+-------+----------+
| Id | Name            | Availability Zone | Hosts | Metadata |
+----+-----------------+-------------------+-------+----------+
| 2  | datpt           | nova-1            |       |          |
+----+-----------------+-------------------+-------+----------+

# trong đó : datpt là name mà chúng ta tùy chọn để đặt
#nova-1 là tên của zone đó .
```

- Kiểm tra `id` của zone vừa mới tạo :

```sh
nova aggregate-list

+----+--------+-------------------+
| Id | Name   | Availability Zone |
+----+--------+-------------------+
| 2  | datpt1 | nova-1            |
| 1  | datpt  | -                 |
+----+--------+-------------------+

# Ở đây id là 2
```

- Thêm node compute vào zone này :

```sh
nova aggregate-add-host 2 compute2

# 2 là id của zone
# compute2 là tên của host, được xác định trong file /etc/hosts
```

- Kiểm tra xem đã thành công hay chưa :

```sh
root@controller:~# nova availability-zone-list

+-----------------------+----------------------------------------+
| Name                  | Status                                 |
+-----------------------+----------------------------------------+
| internal              | available                              |
| |- controller         |                                        |
| | |- nova-conductor   | enabled :-) 2017-04-21T06:00:44.000000 |
| | |- nova-cert        | enabled :-) 2017-04-21T06:00:45.000000 |
| | |- nova-consoleauth | enabled :-) 2017-04-21T06:00:44.000000 |
| | |- nova-scheduler   | enabled :-) 2017-04-21T06:00:45.000000 |
| nova-1                | available                              |
| |- compute1           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:00:48.000000 |
| nova                  | available                              |
| |- compute2           |                                        |
| | |- nova-compute     | enabled :-) 2017-04-21T06:00:42.000000 |
+-----------------------+----------------------------------------+
```

- Boot VM vào zone nova :

```sh
nova boot doem --flavor 1 --image acc8392e-e360-4c31-92e1-9115f2d04c33 \
--nic net-id=4c711790-7cfc-42ab-8704-88d72680531a --availability-zone nova

+--------------------------------------+-----------------------------------------------+
| Property                             | Value                                         |
+--------------------------------------+-----------------------------------------------+
| OS-DCF:diskConfig                    | MANUAL                                        |
| OS-EXT-AZ:availability_zone          | nova                                          |
| OS-EXT-SRV-ATTR:host                 | -                                             |
| OS-EXT-SRV-ATTR:hostname             | doem                                          |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | -                                             |
| OS-EXT-SRV-ATTR:instance_name        | instance-00000005                             |
| OS-EXT-SRV-ATTR:kernel_id            |                                               |
| OS-EXT-SRV-ATTR:launch_index         | 0                                             |
| OS-EXT-SRV-ATTR:ramdisk_id           |                                               |
| OS-EXT-SRV-ATTR:reservation_id       | r-7k0f3oq0                                    |
| OS-EXT-SRV-ATTR:root_device_name     | -                                             |
| OS-EXT-SRV-ATTR:user_data            | -                                             |
| OS-EXT-STS:power_state               | 0                                             |
| OS-EXT-STS:task_state                | scheduling                                    |
| OS-EXT-STS:vm_state                  | building                                      |
| OS-SRV-USG:launched_at               | -                                             |
| OS-SRV-USG:terminated_at             | -                                             |
| accessIPv4                           |                                               |
| accessIPv6                           |                                               |
| adminPass                            | o6qnEcHG6Arv                                  |
| config_drive                         |                                               |
| created                              | 2017-04-21T06:25:48Z                          |
| description                          | -                                             |
| flavor                               | m1.tiny (1)                                   |
| hostId                               |                                               |
| host_status                          |                                               |
| id                                   | e97d3a7c-5549-4870-af71-0eebdd7ac3d0          |
| image                                | cirros (acc8392e-e360-4c31-92e1-9115f2d04c33) |
| key_name                             | -                                             |
| locked                               | False                                         |
| metadata                             | {}                                            |
| name                                 | doem                                          |
| os-extended-volumes:volumes_attached | []                                            |
| progress                             | 0                                             |
| security_groups                      | default                                       |
| status                               | BUILD                                         |
| tenant_id                            | 242e5fe186c04adfaa3e50f4b8f50a16              |
| updated                              | 2017-04-21T06:25:49Z                          |
| user_id                              | 9ab80ad692454a0496124528ef13ee51              |
+--------------------------------------+-----------------------------------------------+

```

- Kiểm tra trên Dashboard :

![test_boot](/images/nova/test_boot.png)