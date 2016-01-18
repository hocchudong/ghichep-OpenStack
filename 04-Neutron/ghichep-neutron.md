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

- **NoopFirewallDriver** : NGoài các firewall drivers dành cho linux bridge hoặc openvswitch plugin, còn 1 NoopFirewallDriver, tác dụng dùng để không cho phép người sử dụng thay đổi các security group rules, cụ thể như sau:

    -**Bước 1**: Sử dụng option **OVSHybridIptablesFirewallDriver** tạo 1 security group có tên sg1 với các rules cho phép ping và ssh traffic và gán cho các VM1 và VM2:
  
    <img src="http://i.imgur.com/FfetSk5.png">

    Lúc này ta thấy xuất hiện các rules tương ứng trong iptables:

    <img src="http://i.imgur.com/QkaVV5q.png">

   Kiểm tra kết nối: 
   
    <img src="http://i.imgur.com/H7IHM7K.png">

    -**Bước 2** : Thay đổi firewall driver thành Noop trong /etc/neutron/plugins/ml2/ml2_conf.ini trên tất cả các node và restart lại các dịch vụ của neutron:

        [securitygroup]
        ...
        firewall_driver = neutron.agent.firewall.NoopFirewallDriver

    -**Bước 3**: xóa security group sg1 và tạo 1 security group mới có tên sg2 với các rules cho phép truyền thông trên port 80:

     <img src="http://i.imgur.com/ruWhwh1.png">

    Lúc này ta thấy mọi nỗ lực thay đổi security group trên môi trường openstack đều không ảnh hưởng tới những rules ta đã tạo từ trước. Cụ thể, khi xóa security group sg1 đã tạo trước đó khỏi các VM1 và VM2 thì những iptables rules về icmp và ssh vẫn còn và việc truyền thông giữa các VM vẫn đảm bảo như trong bước 1, đồng thời những rules mới tạo ở sg2 sẽ không xuất hiện trong iptables và việc truyền thông qua port 80 sẽ không thực hiện được. 

    Điều này cho thấy Noopfirewalldriver có nhiệm vụ tạo ra những chính sách về truyền thông một cách cố định, người quản trị cloud sẽ tạo ra những traffic rules và fix cứng chúng trên từng tenant, người dùng sẽ tuân theo các rule mặc định đó mà không thể tạo mới hoặc thay đổi theo ý mình.

#####Tham khảo:
1. https://wiki.openstack.org/wiki/Neutron/blueprint_ovs-firewall-driver

2. http://docs.openstack.org/user-guide-admin/nova_cli_manage_projects_security.html