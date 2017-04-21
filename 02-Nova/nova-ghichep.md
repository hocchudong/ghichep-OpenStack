# Ghi chép về Nova

## Các lệnh thường dùng với NOVA .

- Tạo một flavor mới :

```sh
nova flavor-create --is-public true m1.coolhardware 100 2048 20 2

+-----+-----------------+-----------+------+-----------+------+-------+-------------+-----------+
| ID  | Name            | Memory_MB | Disk | Ephemeral | Swap | VCPUs | RXTX_Factor | Is_Public |
+-----+-----------------+-----------+------+-----------+------+-------+-------------+-----------+
| 100 | m1.coolhardware | 2048      | 20   | 0         |      | 2     | 1.0         | True      |
+-----+-----------------+-----------+------+-----------+------+-------+-------------+-----------+

# set extra_specs :

nova flavor-key 100 set coolhardware=true

nova flavor-show 100

+----------------------------+--------------------------+
| Property                   | Value                    |
+----------------------------+--------------------------+
| OS-FLV-DISABLED:disabled   | False                    |
| OS-FLV-EXT-DATA:ephemeral  | 0                        |
| disk                       | 20                       |
| extra_specs                | {"coolhardware": "true"} |
| id                         | 100                      |
| name                       | m1.coolhardware          |
| os-flavor-access:is_public | True                     |
| ram                        | 2048                     |
| rxtx_factor                | 1.0                      |
| swap                       |                          |
| vcpus                      | 2                        |
+----------------------------+--------------------------+


```


# Tham Khảo :

- http://ken.pepple.info/openstack/2011/04/22/openstack-nova-architecture/
- https://blog.russellbryant.net/2013/05/21/availability-zones-and-host-aggregates-in-openstack-compute-nova/
- https://wiki.openstack.org/wiki/LiveMigrationWorkflows
- http://qiita.com/idzzy/items/98967887a0d3771a7795