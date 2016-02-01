###Role-based access control for network openstack
Trong các phiên bản openstack cũ, Neutron cung cấp cho người dùng tính năng chia sẻ tài nguyên mạng giữa các tenant. Khi 1 tài nguyên mạng được chỉ định là **shared**, thì nó sẽ được chia sẻ cho tất cả các tenant trong môi trường openstack. Điều này có nghĩa, 1 tài nguyên chỉ có thể shared cho tất cả hoặc không shared cho bất kì tenant nào (all-or-nothing). Điều này gây ra nhiều bất tiện và đôi khi, dẫn tới cả các rủi ro về bảo mật và quyền riêng tư.

Để giải quyết vấn đề này, từ phiên bản liberty, openstack cung cấp tính năng role-based access control cho network (RBAC), cho phép người dùng có thể chỉ định việc chia sẻ tài nguyên mạng với 1 nhóm tenant xác định. 

#####RBAC command
Để quản lí RBAC, neutron cung cấp 1 số api mới trong neutron client:

    rbac-create
    rbac-delete
    rbac-list
    rbac-show
    rbac-update

từ những api này ta có thể tạo nên role-based access controll table với các entries quy định việc chia sẻ tài nguyên mạng giữa các tenant thông qua  object type, target tenant, action và RBAC_OBJECT

    usage: rbac-create [-h] [-f {html,json,shell,table,value,yaml}] [-c COLUMN]
                   [--max-width <integer>] [--prefix PREFIX]
                   [--request-format {json,xml}] [--tenant-id TENANT_ID]
                   --type {network} [--target-tenant TARGET_TENANT] --action
                   {access_as_external,access_as_shared}
                   RBAC_OBJECT

- object type: kiểu tài nguyên cần chia sẻ (network, port, subnet...) Hiện tại mới chỉ support việc chia sẻ tài nguyên network.
- target tenant: là UUID của tenant được share phần tài nguyên này
- action: access_as_external hoặc access_as_shared
- RBAC_OBJECT: là UUID của phần tài nguyên muốn chia sẻ

Để tạo 1 RBAC policy, trước tiên ta tạo 3 tenant A B C với các user tương ứng là userA, userB và userC:

<img src="http://i.imgur.com/0QF7cH0.png">

<img src="http://i.imgur.com/42WTDuJ.png">

Tiếp theo, tạo 1 network có tên rbac-network với user admin: 

<img src="http://i.imgur.com/rTyJMU5.png">
 
Ở đây ta để ý trường shared network được set là false, tức là chỉ được sử dụng bởi user admin. Nếu trường này được set là true, vùng mạng này sẽ được chia sẻ cho tất cả các tenant, đây là điều mà ta không mong muốn.

Tạo 1 subnet trong vùng mạng này:

<img src="http://i.imgur.com/HS7W9Eu.png">

#####Tạo RBAC policy:

Ta sẽ gán quyền truy cập vào network rbac-net cho các user trong tenantA thông qua rbac policy. Nhưng trước tiên, ta kiểm tra sự tồn tại của rbac-net: 

- Đăng nhập với user admin, ta thấy sự xuất hiện của rbac-net: 

<img src="http://i.imgur.com/OMWzHq1.png">

- Đăng nhập bằng UserA thuộc tenantA, không thấy sự xuất hiện của dải mạng này:

<img src="http://i.imgur.com/sFwRzFn.png">

Để gán quyền truy cập rbac-net cho tenantA, ta tạo 1 rbac policy có dạng:

    $ neutron rbac-create --type network --target-tenant 07331639e3bb4ba6b2627a19da545677 --action access_as_shared 65bb7720-ef95-4430-bf7f-e719fb613a60 

trong đó target-tenant là id của tenantA, rbac-object là id của dải mạng rbac-net.

Tạo RBAC policy thành công:

<img src="http://i.imgur.com/PraDTYj.png">

neutron rbac-list sẽ show tất cả các RBAC policy đã tạo:

<img src="http://i.imgur.com/obB5cIy.png">

Kiểm tra lại trên tenantA, thấy xuất hiện dải mạng rbac-net:

<img src="http://i.imgur.com/lx7rUQN.png">

Từ đây trên tenantA có thể tạo các VM có port thuộc dải mạng này. Kiểm tra trên user admin, ta thấy trên dải mạng rbac-net xuất hiện port của VM vừa mới được tạo: 

<img src="http://i.imgur.com/RcIUOro.png">

Tương tự, ta gán tạo rbac policy cho phép tenantB sử dụng dải mạng này:

<img src="http://i.imgur.com/9Veivx2.png">

sử dụng command line, ta tạo VM bằng userB sử dụng dải mạng rbac-net:

    $ nova --os-project-name TenantB --os-username UserB --os-password secrete boot --flavor m1.tiny --image "cirros-0.3.4-x86_64-uec" --nic net-id=65bb7720-ef95-4430-bf7f-e719fb613a60 TenantB-vm1

<img src="http://i.imgur.com/87V0kPw.png">

UserC do không có quyền truy cập dải mạng này nên việc boot VM sử dụng dải rbac-net không thực hiện được:

<img src="http://i.imgur.com/lgeKrex.png">

Để xóa 1 RBAC policy, ta sử dụng lệnh 

    $ neutron rbac-delete {rbac-policy-id}
 
Nhưng trước tiên cần xóa các port gắn trên dải mạng đang được share.

Tài liệu tham khảo:

[1] : https://developer.rackspace.com/blog/A-First-Look-at-RBAC-in-the-Liberty-Release-of-Neutron/

[2] : http://docs.openstack.org/liberty/networking-guide/adv-config-network-rbac.html

[3] : http://specs.openstack.org/openstack/neutron-specs/specs/liberty/rbac-networks.html
