## Các ghi chép về OpenStack Neutron


### Cấu hình QoS cho Neutron trong OpenStack Liberty
-----

#### Bước 1: Cấu hình
##### Trên Neutron Server

- Trong bản OpenStack Liberty thì Neutron nằm trên Controller
- Khai báo trong file `/etc/neutron/neutron.conf`
```sh
[DEFAULT]

service_plugins = router,qos

```

- Khai báo trong file `/etc/neutron/plugins/ml2/ml2_conf.ini` ở 2 section `[ml2]` và `[agent]`
```sh
[ml2]

extension_drivers = qos


[agent]

extensions = qos
```
##### Trên node COMPUTE
- Khai báo trong file `/etc/neutron/plugins/ml2/ml2_conf.ini` ở 2 section `[ml2]` và `[agent]`
```sh
[ml2]

extension_drivers = qos


[agent]

extensions = qos
```



#### Bước 2: Thực hiện test
Tạo 02 máy ảo để thực hiện test

##### Thực hiện trên Neutron Server 

- Tạo `qos-policy` có tên là `bw-limiter`
```sh
neutron qos-policy-create bw-limiter
```

- Setup bandwidth 
```sh
neutron qos-bandwidth-limit-rule-create --max-kbps 1000 --max-burst-kbps 100 bw-limiter
```

- Kiểm tra port trong neutron 
```sh
neutron port-list
```

- Áp rule vào port cần thiết lập
```sh
neutron port-update ID_PORT --qos-policy bw-limiter
```

- Bỏ rule của port vừa thiết lập
```sh
neutron port-update ID_PORT --no-qos-policy
```


- Đứng trên node compute kiểm tra port của máy ảo cần kiểm tra bằng lệnh
```sh
ovs-vsctl show | grep qvo
```

- Ghi lại port cần kiểm tra và sử dụng lệnh nload ở dưới.
- Trên node compute thực hiện theo dõi bandwidth của máy ảo bằng lệnh nload 


- Thực hiện đẩy traffic vào máy cần kiểm tra (máy này có port được áp policy)
```sh
ssh cirros@$THE_IP_ADDRESS 'dd if=/dev/zero  bs=1M count=1000000000'
```



##### Link tham khảo
1. http://www.ajo.es/post/126667247769/neutron-qos-service-plugin

2. http://m.blog.csdn.net/blog/junheart/48373483

3 http://docs.openstack.org/networking-guide/adv_config_qos.html  (Cách tạo rule)

---------------------- 

###Security group:
- Là 1 tập hợp các traffic rule được áp dụng cho các VM trong 1 tenant, dùng để kiểm soát truy cập giữa các VM và giữa VM với tài nguyên mạng bên ngoài môi trường openstack.
- 1 security khi đc gán cho 1 port hoặc VM sẽ được dịch sang các iptables rules.
- Mặc định, 1 security group được tạo ra có tên default group được gán cho tất cả các instance. default group chặn tất cả traffic tới VM và chỉ cho traffic từ VM gửi đi.
- 1 instance có thể có nhiều security group
Trước đây, openstack sử dụng nova firewall driver để triển khai các security rules, nhưng giờ đã được thay thế bởi neutron, do đó cần disable nova firewall trong file */etc/nova/nova.conf* :

        [DEFAULT]
        ...
        firewall_driver =nova.virt.firewall.NoopFirewallDriver


 và thay thế bởi neutron firewall driver trong */etc/neutron/plugins/ml2/ml2_conf.ini* trên tất cả các node:

        [securitygroup]
        ...
        enable_security_group = True    #để là true nếu dùng neutron firewall, false nếu dùng nova firewall
        firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver

 ở đây ta sử dụng firewall driver dành cho openvswitch, nếu sử dụng plugin là linux bridge, thì driver sẽ là :
**neutron.agent.linux.iptables_firewall.IptablesFirewallDriver**

- chi tiết của các neutron firewall drivers có thể tham khảo tại:
https://github.com/openstack/neutron/blob/master/neutron/agent/firewall.py
https://github.com/openstack/neutron/blob/master/neutron/agent/linux/iptables_firewall.py

 ta thấy có các driver chính đó là **IptablesFirewallDriver**, **OVSHybridIptablesFirewallDriver** dựa trên iptables và NoopFirewallDriver nếu không muốn triển khai neutron firewall

**OVSHybridIptablesFirewallDriver** là driver dành cho openvswitch plugin và được kế thừa lại từ **IptablesFirewallDriver**

- security group của neutron được khai báo ở */etc/neutron/plugins/ml2/ml2/ml2_conf.ini*  trên tất cả các node. 
 
 Khi thay đổi firewall driver ( ví dụ khai báo sai driver hoặc dùng NoopFirewallDriver) việc tạo và sửa các rule trên các security group cũng như việc gán security group cho instance không bị ảnh hưởng, nhưng các rule đó sẽ không có tác dụng đối với instance. Tất cá các traffic tới VM đều bị drop.

#####Tham khảo:
1. https://wiki.openstack.org/wiki/Neutron/blueprint_ovs-firewall-driver

2. http://docs.openstack.org/user-guide-admin/nova_cli_manage_projects_security.html
