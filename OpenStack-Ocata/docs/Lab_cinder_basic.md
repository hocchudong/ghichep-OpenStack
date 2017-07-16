# Lab cơ bản về cinder

## Mục lục

- [1. Tạo một volume mới](#1)
  - [Tạo một volume no-source](#a)
  - [Tạo một volume từ image](#b)
  - [Tạo một volume từ volume khác](#c)
  - [Tạo một volume từ một bản snapshot](#d)
- [2. Snapshot volume](#2)
- [3. Attach và detach volume cho instance](#3)
- [4. Xóa bỏ volume](#4)

<a name=1></a>
## 1. Tạo một volume mới

---

<a name=a></a>
### Tạo một volume no-source
- Với cách tạo này, một volume trống sẽ được tạo ra và volume này sẽ không có khả năng launch được instance - volume này được gọi là `non-bootable`.
- Dùng lệnh sau để tạo

  ```sh
  openstack volume create --size 1 volume-empty
  ```
  
  - **volume-empty** là tên của volume
  
- Lệnh thứ 2 cho kết quả tương tự

  ```sh
  cinder create --display-name volume-empty2 1
  ```
  
  - **volume-empty2** là tên của volume, **1** là kích thước volume
  
- List ra các volume có trong hệ thống để kiểm tra kết quả

  ```sh
  root@controller:~# cinder list
  +--------------------------------------+-----------+----------------+------+-------------+----------+--------------------------------------+
  | ID                                   | Status    | Name           | Size | Volume Type | Bootable | Attached to                          |
  +--------------------------------------+-----------+----------------+------+-------------+----------+--------------------------------------+
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | in-use    | volume2        | 5    | -           | true     | bde4a1f4-b951-401e-ad09-c98af5eeb76a |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | available | volume-empty2  | 1    | -           | false    |                                      |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | available | volume-empty   | 1    | -           | false    |                                      |
  +--------------------------------------+-----------+----------------+------+-------------+----------+--------------------------------------+
  root@controller:~# openstack volume list
  +--------------------------------------+----------------+-----------+------+------------------------------------------+
  | ID                                   | Display Name   | Status    | Size | Attached to                              |
  +--------------------------------------+----------------+-----------+------+------------------------------------------+
  | 80216bd2-0eba-42da-908d-6c5d40be748b | volume-empty2  | available |    1 |                                          |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | volume-empty   | available |    1 |                                          |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | volume2        | in-use    |    5 | Attached to instance-volume on /dev/vda  |
  +--------------------------------------+----------------+-----------+------+------------------------------------------+
  ```
  
  - Dùng lệnh `cinder list` thì ta có thể thấy được 2 volume vừa tạo có thuộc tính `Bootable` đều là `false`
  
<a name=b></a>
### Tạo một volume từ image
- Tạo volume từ image thì volume được tạo ra có thể dùng để launch instance
- Trước khi tạo volume, hãy list ra xem trong hệ thống có image nào

  ```sh
  root@controller:~# openstack image list
  +--------------------------------------+---------------+--------+
  | ID                                   | Name          | Status |
  +--------------------------------------+---------------+--------+
  | 9b989c67-57a3-4f7d-88d0-d4137aa0a7fa | cirros        | active |
  +--------------------------------------+---------------+--------+

- Tạo volume

  ```sh
  openstack volume create --size 1 --image cirros volume-from-image
  ```
  
- List ra xem kết quả có gì khác so với cách tạo trước

  ```sh
  root@controller:~# cinder list
  +--------------------------------------+-----------+-------------------+------+-------------+----------+--------------------------------------+
  | ID                                   | Status    | Name              | Size | Volume Type | Bootable | Attached to                          |
  +--------------------------------------+-----------+-------------------+------+-------------+----------+--------------------------------------+
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | available | volume-from-image | 1    | -           | true     |                                      |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | in-use    | volume2           | 5    | -           | true     | bde4a1f4-b951-401e-ad09-c98af5eeb76a |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | available | volume-empty2     | 1    | -           | false    |                                      |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | available | volume-empty      | 1    | -           | false    |                                      |
  +--------------------------------------+-----------+-------------------+------+-------------+----------+--------------------------------------+
  ```
  
  - Chúng ta có thể thấy volume `volume-from-image` có thuộc tính `bootable` là `true`
  
<a name=c></a>
### Tạo một volume từ một volume khác
- Chúng ta sẽ tạo 2 volume từ 2 kiểu volume khác nhau:

  ```sh
  Lưu ý: 
  size của volume cần tạo phải lớn hơn hoặc bằng volume gốc
  ```
  
- một volume từ một volume bootable

  ```sh
  openstack volume create --source volume-from-image --size 1 volume-from-volume2
  ```

- một volume từ một volume non-bootable

  ```sh
  openstack volume create --source volume-empty --size 2 volume-from-volume
  ```

- List ra các volume để xem chúng ta có kết quả gì

  ```sh
  root@controller:~# cinder list
  +--------------------------------------+-----------+---------------------+------+-------------+----------+--------------------------------------+
  | ID                                   | Status    | Name                | Size | Volume Type | Bootable | Attached to                          |
  +--------------------------------------+-----------+---------------------+------+-------------+----------+--------------------------------------+
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | available | volume-from-image   | 1    | -           | true     |                                      |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | in-use    | volume2             | 5    | -           | true     | bde4a1f4-b951-401e-ad09-c98af5eeb76a |
  | 4111ee2e-b2f6-4850-b212-50d5abd58930 | available | volume-from-volume2 | 1    | -           | true     |                                      |
  | 5d6328c7-a2bf-464b-8bb8-fc2a0a5305d2 | available | volume-from-volume  | 2    | -           | false    |                                      |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | available | volume-empty2       | 1    | -           | false    |                                      |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | available | volume-empty        | 1    | -           | false    |                                      |
  +--------------------------------------+-----------+---------------------+------+-------------+----------+--------------------------------------+
  ```
  
  - Chúng ta có thể thấy rằng, khi tạo mới một volume từ một volume non-bootable thì volume mới được tạo ra cũng non-bootable
  - Volume được tạo ra từ volume bootable thì volume đó cũng bootable.
  
<a name=d></a>
### Tạo một volume từ một snapshot
- Trước tiên hãy tạo 2 bản snapshot từ 2 loại volume (bootable và non-bootable)

  ```sh
  root@controller:~# openstack volume snapshot create --volume volume-empty --description "snapshot of non-bootable volume" snapshot-vl-empty
  +-------------+--------------------------------------+
  | Field       | Value                                |
  +-------------+--------------------------------------+
  | created_at  | 2017-07-16T03:08:00.688888           |
  | description | snapshot of non-bootable volume      |
  | id          | 0d7545fd-1a00-4cd3-96c5-ac9788cf845c |
  | name        | snapshot-vl-empty                    |
  | properties  |                                      |
  | size        | 1                                    |
  | status      | creating                             |
  | updated_at  | None                                 |
  | volume_id   | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 |
  +-------------+--------------------------------------+
  
  
  root@controller:~# openstack volume snapshot create --volume volume-from-image --description "snapshot of bootable volume" snapshot-vl-img
  +-------------+--------------------------------------+
  | Field       | Value                                |
  +-------------+--------------------------------------+
  | created_at  | 2017-07-16T03:08:59.715518           |
  | description | snapshot of bootable volume          |
  | id          | 4402630b-18b0-420d-b949-a085a498a193 |
  | name        | snapshot-vl-img                      |
  | properties  |                                      |
  | size        | 1                                    |
  | status      | creating                             |
  | updated_at  | None                                 |
  | volume_id   | 21b3d15b-9c95-415a-817c-1f70124123a5 |
  +-------------+--------------------------------------+
  
  
  root@controller:~# openstack volume snapshot list
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  | ID                                   | Name              | Description                     | Status    | Size |
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  | 4402630b-18b0-420d-b949-a085a498a193 | snapshot-vl-img   | snapshot of bootable volume     | available |    1 |
  | 0d7545fd-1a00-4cd3-96c5-ac9788cf845c | snapshot-vl-empty | snapshot of non-bootable volume | available |    1 |
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  ```
  
- Tạo 2 volume mới từ 2 snapshot trên

  ```sh
  root@controller:~# openstack volume create --snapshot snapshot-vl-empty --size 1 vl-from-snapshot-empty
  +---------------------+--------------------------------------+
  | Field               | Value                                |
  +---------------------+--------------------------------------+
  | attachments         | []                                   |
  | availability_zone   | nova                                 |
  | bootable            | false                                |
  | consistencygroup_id | None                                 |
  | created_at          | 2017-07-16T03:15:38.852186           |
  | description         | None                                 |
  | encrypted           | False                                |
  | id                  | 2447909e-9ccd-4cdc-b2be-082b61ecf2e0 |
  | migration_status    | None                                 |
  | multiattach         | False                                |
  | name                | vl-from-snapshot-empty               |
  | properties          |                                      |
  | replication_status  | None                                 |
  | size                | 1                                    |
  | snapshot_id         | 0d7545fd-1a00-4cd3-96c5-ac9788cf845c |
  | source_volid        | None                                 |
  | status              | creating                             |
  | type                | None                                 |
  | updated_at          | None                                 |
  | user_id             | 102f8ea368cd4451ad6fefeb15801177     |
  +---------------------+--------------------------------------+
  
  
  root@controller:~# openstack volume create --snapshot snapshot-vl-img --size 1 vl-from-snapshot-img
  +---------------------+--------------------------------------+
  | Field               | Value                                |
  +---------------------+--------------------------------------+
  | attachments         | []                                   |
  | availability_zone   | nova                                 |
  | bootable            | false                                |
  | consistencygroup_id | None                                 |
  | created_at          | 2017-07-16T03:16:09.653216           |
  | description         | None                                 |
  | encrypted           | False                                |
  | id                  | f1227040-0762-4c57-a3fd-65be01a69471 |
  | migration_status    | None                                 |
  | multiattach         | False                                |
  | name                | vl-from-snapshot-img                 |
  | properties          |                                      |
  | replication_status  | None                                 |
  | size                | 1                                    |
  | snapshot_id         | 4402630b-18b0-420d-b949-a085a498a193 |
  | source_volid        | None                                 |
  | status              | creating                             |
  | type                | None                                 |
  | updated_at          | None                                 |
  | user_id             | 102f8ea368cd4451ad6fefeb15801177     |
  +---------------------+--------------------------------------+
  ```
  
- List ra các volume để kiểm tra lại kết quả

  ```sh
  root@controller:~# cinder list
  +--------------------------------------+-----------+------------------------+------+-------------+----------+--------------------------------------+
  | ID                                   | Status    | Name                   | Size | Volume Type | Bootable | Attached to                          |
  +--------------------------------------+-----------+------------------------+------+-------------+----------+--------------------------------------+
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | available | volume-from-image      | 1    | -           | true     |                                      |
  | 2447909e-9ccd-4cdc-b2be-082b61ecf2e0 | available | vl-from-snapshot-empty | 1    | -           | false    |                                      |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | in-use    | volume2                | 5    | -           | true     | bde4a1f4-b951-401e-ad09-c98af5eeb76a |
  | 4111ee2e-b2f6-4850-b212-50d5abd58930 | available | volume-from-volume2    | 1    | -           | true     |                                      |
  | 5d6328c7-a2bf-464b-8bb8-fc2a0a5305d2 | available | volume-from-volume     | 2    | -           | false    |                                      |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | available | volume-empty2          | 1    | -           | false    |                                      |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | available | volume-empty           | 1    | -           | false    |                                      |
  | f1227040-0762-4c57-a3fd-65be01a69471 | available | vl-from-snapshot-img   | 1    | -           | true     |                                      |
  +--------------------------------------+-----------+------------------------+------+-------------+----------+--------------------------------------+
  ```
  
- Như vậy có thể tóm tắt lại kết quả tạo volume như sau:
  - Khi tạo một volume mới từ 1 bootable volume hoặc từ một snapshot của bootable volume thì volume mới đó là một bootable volume
  - Khi tạo một volume mới từ 1 non-bootable volume hoặc từ một snapshot của non-bootable volume thì volume mới đó là một non-bootable volume
  
<a name=2></a>
## 2. Snapshot volume
- Có thể tạo snapshot cho volume bằng lệnh theo như cách vừa tạo ở trên
- Có một lệnh khác có thể tạo snapshot như sau:
  
  ```sh
  cinder snapshot-create --display-name <tên snapshot> <ID của volume>
  ```
  
- List ra danh sách các snapshot của volume

  ```sh
  root@controller:~# openstack volume snapshot list
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  | ID                                   | Name              | Description                     | Status    | Size |
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  | 30d914e2-6bb0-41fb-a48d-d03ca6ea8944 | snap-cli-cinder   | None                            | available |    1 |
  | 4402630b-18b0-420d-b949-a085a498a193 | snapshot-vl-img   | snapshot of bootable volume     | available |    1 |
  | 0d7545fd-1a00-4cd3-96c5-ac9788cf845c | snapshot-vl-empty | snapshot of non-bootable volume | available |    1 |
  +--------------------------------------+-------------------+---------------------------------+-----------+------+
  ```
  
- Xóa snapshot

  ```sh
  openstack volume snapshot delete <tên snapshot>
  ```
  
<a name=3></a>
## 3. Attach và detach volume cho máy ảo
- List các VM có trong hệ thống

  ```sh
  root@controller:~# openstack server list
  +--------------------------------------+-----------------+---------+----------------------------------------------------+------------+
  | ID                                   | Name            | Status  | Networks                                           | Image Name |
  +--------------------------------------+-----------------+---------+----------------------------------------------------+------------+
  | 0af8fde5-f21a-40e0-89b6-8186f423025e | vm69            | SHUTOFF | self-service=192.168.1.104; provider=172.16.69.199 | cirros     |
  +--------------------------------------+-----------------+---------+----------------------------------------------------+------------+
  ```
  
- List ra các volume

  ```sh
  root@controller:~# openstack volume list
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | ID                                   | Display Name           | Status    | Size | Attached to                              |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | f1227040-0762-4c57-a3fd-65be01a69471 | vl-from-snapshot-img   | available |    1 |                                          |
  | 2447909e-9ccd-4cdc-b2be-082b61ecf2e0 | vl-from-snapshot-empty | available |    1 |                                          |
  | 4111ee2e-b2f6-4850-b212-50d5abd58930 | volume-from-volume2    | available |    1 |                                          |
  | 5d6328c7-a2bf-464b-8bb8-fc2a0a5305d2 | volume-from-volume     | available |    2 |                                          |
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | volume-from-image      | available |    1 |                                          |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | volume-empty2          | available |    1 |                                          |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | volume-empty           | available |    1 |                                          |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | volume2                | in-use    |    5 | Attached to instance-volume on /dev/vda  |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  ```
  
- Thực hiện add volume cho `vm69`

  ```sh
  root@controller:~# openstack server add volume vm69 volume-empty --device /dev/vdb
  ```

- Ta có thể add thêm một volume nữa cho vm69

  ```sh
  openstack server add volume vm69 volume-empty2 --device /dev/vdc
  ```
  
- Thực hiện list ra các volume để xem có gì thay đổi.

  ```sh
  root@controller:~# openstack volume list
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | ID                                   | Display Name           | Status    | Size | Attached to                              |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | f1227040-0762-4c57-a3fd-65be01a69471 | vl-from-snapshot-img   | available |    1 |                                          |
  | 2447909e-9ccd-4cdc-b2be-082b61ecf2e0 | vl-from-snapshot-empty | available |    1 |                                          |
  | 4111ee2e-b2f6-4850-b212-50d5abd58930 | volume-from-volume2    | available |    1 |                                          |
  | 5d6328c7-a2bf-464b-8bb8-fc2a0a5305d2 | volume-from-volume     | available |    2 |                                          |
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | volume-from-image      | available |    1 |                                          |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | volume-empty2          | in-use    |    1 | Attached to vm69 on /dev/vdc             |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | volume-empty           | in-use    |    1 | Attached to vm69 on /dev/vdb             |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | volume2                | in-use    |    5 | Attached to instance-volume on /dev/vda  |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  ```
  
- Ta có thể thấy 2 volume là `volume-empty` và `volume-empty2` ở trạng thái `in-use` và được attached vào vm69.

- Thực hiện detach volume ra khỏi vm69

  ```sh
  openstack server remove volume vm69 volume-empty
  ```
  
- List ra tất cả volume để xem kết quả thay đổi

  ```sh
  root@controller:~# openstack volume list
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | ID                                   | Display Name           | Status    | Size | Attached to                              |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  | f1227040-0762-4c57-a3fd-65be01a69471 | vl-from-snapshot-img   | available |    1 |                                          |
  | 2447909e-9ccd-4cdc-b2be-082b61ecf2e0 | vl-from-snapshot-empty | available |    1 |                                          |
  | 4111ee2e-b2f6-4850-b212-50d5abd58930 | volume-from-volume2    | available |    1 |                                          |
  | 5d6328c7-a2bf-464b-8bb8-fc2a0a5305d2 | volume-from-volume     | available |    2 |                                          |
  | 21b3d15b-9c95-415a-817c-1f70124123a5 | volume-from-image      | available |    1 |                                          |
  | 80216bd2-0eba-42da-908d-6c5d40be748b | volume-empty2          | in-use    |    1 | Attached to vm69 on /dev/vdc             |
  | adbf7ef4-7e5e-4dc3-a239-ca291c9ff555 | volume-empty           | available |    1 |                                          |
  | 2cb93558-a907-4188-8f63-c0d7b86daf36 | volume2                | in-use    |    5 | Attached to instance-volume on /dev/vda  |
  +--------------------------------------+------------------------+-----------+------+------------------------------------------+
  ```
  
<a name=4></a>
## 4. Thực hiện xóa volume
- Chúng ta không thể xóa một volume đang di cư, attached, thuộc vào 1 group hoặc có snapshot (migrating, attached, belong to a group or have snapshots).
- Xóa volume bằng lệnh sau:

  ```sh
  openstack volume delete <tên hoặc id của volume cần xóa>
  ```
  
---

Trên đây là một số tác vụ quản trị volume cơ bản mà mình đã thực hiện trong quá trình tìm hiểu. Bài viết còn nhiều thiếu sót mong nhận được sự góp ý của bạn đọc để bài viết được hoàn thiện thêm.
