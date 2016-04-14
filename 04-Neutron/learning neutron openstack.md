###Overlapping network using namespace:
- Openstack là mô hình multitenancy -> mỗi tenant có thể tạo riêng nhiều private network, router, firewall, loadbalancer… Neutron có khả năng tách biệt các tài nguyên mạng giữa các tenant sử dụng linux namespace.
- mỗi network namespace có riêng cho mình routes, firewall rules, interface devices. Mỗi network hay router do tenant tạo ra đều hiện hữu dưới dạng 1 network namespace -> cho phép các tenant tạo dc các network trùng nhau ( overlapping) nhưng vẫn độc lập mà k bị xung đột (isolated)
- Các namespace hiển thị dưới dạng:
     - qdhcp- <network UUID>
     - qrouter- <router UUID>
     - qlbaas- <load balancer UUID>
- để list các namespace đang có sử dụng lệnh:

        #ipnetns

- xem cấu hình 1 network namespace sử dụng lệnh:
	
         #ipnetns exec NAMESPACE command

các lệnh có thể sử dụng ở đây như ip, route, iptables, telnet hoặc ping…

-------------------------------------

###ML2 plugin:

- Nhờ kiến trúc plugin, Neutron có khả năng mở rộng thông qua ML2 plugin
- LB và OVS là các cấu trúc nguyên khối, có nghĩa chúng chỉ hoạt động riêng rẽ mà k sử dụng đc đồng thời với các công nghệ khác. Nhờ ML2 mà các công ty có thể tự tạo ra các plugin của riêng mình và cho phép neutron sử dụng chúng. ML2 tách các chức năng lõi của mạng như IPAM, ID management… do đó các vendor k cần làm lại các chức năng này mà chỉ cần tập trung phát triển tính năng sản phẩm. 
- ML2 plugin tach biệt network type và mechanism type. network type và mechanism type có khả năng tách biệt thông qua drivers (pluggable)
     - Type driver quản lý các mô hình mạng của cả provider network và tenant network như : local, flat, vlan, gre hay vxlan…
     - Mechanism driver là 1 lớp chứa driver của hầu hết các plugin network của các vendor khác nhau như OVS, LB, HyperV, Arista, CiscoNexus…

---------------------------- 

###Enable packet forwading:

- Khi cấu hình Neutron, cần cấu hình 3 kernel parameter về forward gói tin:
      - Net.ipv4.ip_forward = 1
      - Net.ipv4.conf.all.rp_filter = 0
      - Net.ipv4.conf.default.rp_filter = 0

- Net.ipv4.ip_forward cho phép host vật lý có khả năng forward traffic từ VM ra internet . 2 tham số sau là 1 cơ chế  nhằm ngăn chặn tấn công từ chối dịch vụ bằng cách chặn các địa chỉ IP giả mạo. Khi dc cấu hình, linux kernel sẽ kiểm tra từng packet để đảm bảo địa chỉ IP nguồn là có thể định tuyến ngược từ interface mà nó gửi traffic đến, tức các gói tin nhận dc trên 1 interface từ IP đó sẽ có khả năng phản hồi lại -> k phải IP giả mạo.
2 thông số này được set về 0, cơ chế này đc triển khai thay bằng iptables rules

----------------

###Cấu hình neutron trong file /etc/neutron/neutron.conf:

####sử dụng Keystone để xác thực :
    # crudini --set /etc/neutron/neutron.conf DEFAULT auth_strategy keystone  
    # crudini --set /etc/neutron/neutron.conf DEFAULT api_paste_config /etc/neutron/api-paste.ini 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_host controller 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_port 35357 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_protocol http 66 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_tenant_name service 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_user neutron
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_password neutron

####sử dụng file /etc/neutron/api-paste.ini làm môi trường để xác thực:
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken auth_host controller 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken auth_uri http://controller:5000 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_tenant_name service 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_user neutron 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_password neutron

####Cấu hình Neutron sử dụng dịch vụ message queue
    # crudini --set /etc/neutron/neutron.conf DEFAULT rpc_backend rabbit
    # crudini --set /etc/neutron/neutron.conf DEFAULT rabbit_host = controller
    # crudini --set /etc/neutron/neutron.conf DEFAULT rabbit_password = RABBIT_PASS

####Cấu hình nova sử dụng neutron thay cho nova-network trong /etc/nova/nova.conf

    # crudini --set /etc/nova/nova.conf DEFAULT network_api_class nova.network.neutronv2.api.API 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_url http://controller:9696
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_auth_strategy keystone 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_tenant_name service 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_username neutron 68 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_password neutron 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_auth_url http://controller:35357/v2.0

(nova sử dụng firewall_driver để cấu hình firewall cho nova-network, khi sử dụng neutron, dòng này cần dc cấu hình là nova.virt.firewall.NoopFirewallDriver để nova k sử dụng firewall_driver nữa )

####Cấu hình nova sử dụng neutron api để triển khai security group:
    # crudini --set /etc/nova/nova.conf DEFAULT security_group_api neutron

####Cấu hình core_plugin
Để thông báo cho neutron biết sử dụng công nghệ nào để tạo switch ảo, cần khai báo trong core_plugin. Mỗi công nghệ có 1 driver riêng:

  - LinuxBridge: neutron.plugins.linuxbridge.lb_neutron_plugin.LinuxBridgePluginV2
  - Open vSwitch: neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2

ở đây ta sử dụng ML2 plugin để mở rộng khả năng sử dụng các công nghệ khác nhau, chi tiết phần khai báo cấu hình các công nghệ được cấu hình trong file /etc/neutron/plugins/ml2/ml2_config.ini

####DHCP và tiến trình Dnsmasq
Khi DHCP được enable, tiến trình dnsmasq được khởi chạy bên trong mỗi dhcp namespace, có nhiệm vụ đóng vai trò như 1 dhcp server cấp ip động cho các VM trong 1 tenant. 
Mỗi dhcp namespace được gán 1 port tap và nối tới br-int trên node network. Show dhcp namespace port bằng câu lệnh:

    ip netns exec {dhcp-namespace-ID} ip a
ta sẽ thấy port tap đó.

####Quy ước đặt tên port trong openstack:
**Trên compute node**

- Linux bridge: qbr-ID
Linux bridge nằm giữa VM và br-int, gồm 2 port:
 - port tap gắn với VM: tap-ID
 - port veth pair gắn với br-int: qvb-ID
- Br-int :
 - port veth pair gắn với linux bridge: qvo-ID
 - port patch gắn với br-tun
 
Trên 1 network thì các port của các thiết bị này có chung ID là ID của network đó.

**Trên network node**

- Br-int: cung cấp router ảo và DHCP cho instance. gồm các port:
 - port tap gắn với DHCP namespace: tap-ID
 - port qr gắn với router namespace: qr-ID
 
- Br-ex: cung cấp external connection. Gồm port qg gắn với router namespace: qg-ID
