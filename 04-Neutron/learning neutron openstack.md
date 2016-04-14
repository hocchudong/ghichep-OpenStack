###Overlapping network using namespace:
- Openstack là mô hình multitenancy -> m?i tenant có th? t?o riêng nhi?u private network, router, firewall, loadbalancer… Neutron có kh? nang tách bi?t các tài nguyên m?ng gi?a các tenant s? d?ng linux namespace.
- m?i network namespace có riêng cho mình routes, firewall rules, interface devices. M?i network hay router do tenant t?o ra d?u hi?n h?u du?i d?ng 1 network namespace -> cho phép các tenant t?o dc các network trùng nhau ( overlapping) nhung v?n d?c l?p mà k b? xung d?t (isolated)
- Các namespace hi?n th? du?i d?ng:
     - qdhcp- <network UUID>
     - qrouter- <router UUID>
     - qlbaas- <load balancer UUID>
- d? list các namespace dang có s? d?ng l?nh:

        #ipnetns

- xem c?u hình 1 network namespace s? d?ng l?nh:
	
         #ipnetns exec NAMESPACE command

các l?nh có th? s? d?ng ? dây nhu ip, route, iptables, telnet ho?c ping…

-------------------------------------

###ML2 plugin:

- Nh? ki?n trúc plugin, Neutron có kh? nang m? r?ng thông qua ML2 plugin
- LB và OVS là các c?u trúc nguyên kh?i, có nghia chúng ch? ho?t d?ng riêng r? mà k s? d?ng dc d?ng th?i v?i các công ngh? khác. Nh? ML2 mà các công ty có th? t? t?o ra các plugin c?a riêng mình và cho phép neutron s? d?ng chúng. ML2 tách các ch?c nang lõi c?a m?ng nhu IPAM, ID management… do dó các vendor k c?n làm l?i các ch?c nang này mà ch? c?n t?p trung phát tri?n tính nang s?n ph?m. 
- ML2 plugin tach bi?t network type và mechanism type. network type và mechanism type có kh? nang tách bi?t thông qua drivers (pluggable)
     - Type driver qu?n lý các mô hình m?ng c?a c? provider network và tenant network nhu : local, flat, vlan, gre hay vxlan…
     - Mechanism driver là 1 l?p ch?a driver c?a h?u h?t các plugin network c?a các vendor khác nhau nhu OVS, LB, HyperV, Arista, CiscoNexus…

---------------------------- 

###Enable packet forwading:

- Khi c?u hình Neutron, c?n c?u hình 3 kernel parameter v? forward gói tin:
      - Net.ipv4.ip_forward = 1
      - Net.ipv4.conf.all.rp_filter = 0
      - Net.ipv4.conf.default.rp_filter = 0

- Net.ipv4.ip_forward cho phép host v?t lý có kh? nang forward traffic t? VM ra internet . 2 tham s? sau là 1 co ch?  nh?m ngan ch?n t?n công t? ch?i d?ch v? b?ng cách ch?n các d?a ch? IP gi? m?o. Khi dc c?u hình, linux kernel s? ki?m tra t?ng packet d? d?m b?o d?a ch? IP ngu?n là có th? d?nh tuy?n ngu?c t? interface mà nó g?i traffic d?n, t?c các gói tin nh?n dc trên 1 interface t? IP dó s? có kh? nang ph?n h?i l?i -> k ph?i IP gi? m?o.
2 thông s? này du?c set v? 0, co ch? này dc tri?n khai thay b?ng iptables rules

----------------

###C?u hình neutron trong file /etc/neutron/neutron.conf:

####s? d?ng Keystone d? xác th?c :
    # crudini --set /etc/neutron/neutron.conf DEFAULT auth_strategy keystone  
    # crudini --set /etc/neutron/neutron.conf DEFAULT api_paste_config /etc/neutron/api-paste.ini 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_host controller 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_port 35357 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken auth_protocol http 66 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_tenant_name service 
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_user neutron
    # crudini --set /etc/neutron/neutron.conf keystone_authtoken admin_password neutron

####s? d?ng file /etc/neutron/api-paste.ini làm môi tru?ng d? xác th?c:
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken auth_host controller 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken auth_uri http://controller:5000 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_tenant_name service 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_user neutron 
    # crudini --set /etc/neutron/api-paste.ini filter:authtoken admin_password neutron

####C?u hình Neutron s? d?ng d?ch v? message queue
    # crudini --set /etc/neutron/neutron.conf DEFAULT rpc_backend rabbit
    # crudini --set /etc/neutron/neutron.conf DEFAULT rabbit_host = controller
    # crudini --set /etc/neutron/neutron.conf DEFAULT rabbit_password = RABBIT_PASS

####C?u hình nova s? d?ng neutron thay cho nova-network trong /etc/nova/nova.conf

    # crudini --set /etc/nova/nova.conf DEFAULT network_api_class nova.network.neutronv2.api.API 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_url http://controller:9696
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_auth_strategy keystone 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_tenant_name service 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_username neutron 68 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_password neutron 
    # crudini --set /etc/nova/nova.conf DEFAULT neutron_admin_auth_url http://controller:35357/v2.0

(nova s? d?ng firewall_driver d? c?u hình firewall cho nova-network, khi s? d?ng neutron, dòng này c?n dc c?u hình là nova.virt.firewall.NoopFirewallDriver d? nova k s? d?ng firewall_driver n?a )

####C?u hình nova s? d?ng neutron api d? tri?n khai security group:
    # crudini --set /etc/nova/nova.conf DEFAULT security_group_api neutron

####C?u hình core_plugin
Ð? thông báo cho neutron bi?t s? d?ng công ngh? nào d? t?o switch ?o, c?n khai báo trong core_plugin. M?i công ngh? có 1 driver riêng:

  - LinuxBridge: neutron.plugins.linuxbridge.lb_neutron_plugin.LinuxBridgePluginV2
  - Open vSwitch: neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2

? dây ta s? d?ng ML2 plugin d? m? r?ng kh? nang s? d?ng các công ngh? khác nhau, chi ti?t ph?n khai báo c?u hình các công ngh? du?c c?u hình trong file /etc/neutron/plugins/ml2/ml2_config.ini

####DHCP và ti?n trình Dnsmasq
Khi DHCP du?c enable, ti?n trình dnsmasq du?c kh?i ch?y bên trong m?i dhcp namespace, có nhi?m v? dóng vai trò nhu 1 dhcp server c?p ip d?ng cho các VM trong 1 tenant. 
M?i dhcp namespace du?c gán 1 port tap và n?i t?i br-int trên node network. Show dhcp namespace port b?ng câu l?nh:

    ip netns exec {dhcp-namespace-ID} ip a
ta s? th?y port tap dó.

####Quy u?c d?t tên port trong openstack:
**Trên compute node**

- Linux bridge: qbr-ID
Linux bridge n?m gi?a VM và br-int, g?m 2 port:
 - port tap g?n v?i VM: tap-ID
 - port veth pair g?n v?i br-int: qvb-ID
- Br-int :
 - port veth pair g?n v?i linux bridge: qvo-ID
 - port patch g?n v?i br-tun
 
Trên 1 network thì các port c?a các thi?t b? này có chung ID là ID c?a network dó.

**Trên network node**

- Br-int: cung c?p router ?o và DHCP cho instance. g?m các port:
 - port tap g?n v?i DHCP namespace: tap-ID
 - port qr g?n v?i router namespace: qr-ID
 
- Br-ex: cung c?p external connection. G?m port qg g?n v?i router namespace: qg-ID
