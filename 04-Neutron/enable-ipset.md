###Ipset kết hợp iptables trong openstack:
Neutron sử dụng iptables để tạo nên các traffic rules  nhằm thiết lập chức năng cho security group, từ đó quy định cách thức các máy ảo truyền thông trên mạng nội bộ cũng như ra ngoài mạng internet. 
Tuy nhiên, việc sử dụng iptables đơn thuần có thể gây ra 1 số vấn đề: 

- Khi 1 security group có 1 hay nhiều rules liên quan đến 1 security group khác, hiệu năng của security group sẽ bị giảm.
- Khi update 1 port vào 1 security group, thì các chain liên quan đến port này sẽ bị xóa đi và build lại, điều này ảnh hưởng đến hiệu năng của L2 agent.

Để giải quyết các vấn đề này, từ phiên bản openstack Juno, người ta đã thêm vào tính năng ipset nhằm hỗ trợ cho iptables và tối ưu các rule chain. Để tìm hiểu tác dụng của ipset trong openstack, trước tiên ta tìm hiểu cách hoạt động của ipset.

#####ipset
ipset là một "match extension" cho iptables. Khi iptables có những rules giống nhau đối với 1 tập các địa chỉ xác định, khi đó ipset lập ra 1 danh sách gồm các địa chỉ ip đó, iptables chỉ việc gọi tới danh sách này bằng cách chỉ định tên của nó mà không cần khai báo nhiều rules với từng địa chỉ ip khác nhau. 

Giả sử ta muốn chặn truy cập từ 2 địa chỉ 1.1.1.1 và 2.2.2.2, với iptables đơn thuần thì các lệnh tương ứng sẽ là:

    iptables -A INPUT -s 1.1.1.1 -j DROP  
    iptables -A INPUT -s 2.2.2.2 -j DROP  

Việc sử dụng ipset kết hợp cùng iptables sẽ thực hiện như sau:

    ipset -N myset iphash  
    ipset -A myset 1.1.1.1  
    ipset -A myset 2.2.2.2  
    iptables -A INPUT -m set --set myset src -j DROP 

Ở trên ta tạo ra 1 danh sách có tên myset bằng ipset, danh sách này bao gồm 2 địa chỉ ip 1.1.1.1 và 2.2.2.2.
Khi muốn chặn truy cập từ 2 địa chỉ này, iptables chỉ việc gọi tới myset bằng cách chỉ định **-m set --set myset**. Cờ **src** chỉ ra rằng những địa chỉ nguồn xuất hiện trong myset sẽ bị drop ở rule này.

Việc sử dụng ipset sẽ tối ưu và rút gọn các dòng lệnh iptables, khi các địa chỉ ip lên tới hàng chục hay hàng trăm thì việc dùng các danh sách thay vì khai báo từng ip bằng iptables sẽ giúp ta tiết kiệm rất nhiều thời gian.

Để xem danh sách các ipset đã được tạo, ta sử dụng lệnh:

    $sudo ipset list 

danh sách các ipset sẽ có dạng sau:

<img src="http://i.imgur.com/3xdTbYn.png">

#####ipset trong openstack

ipset được khai báo trong /etc/neutron/plugins/ml2/ml2_conf.ini trên tất cả các node:

    [securitygroup]
    ...
    enable_ipset = True
Mặc định, ipset được set bằng true kể cả khi không khai báo. Để tắt tính năng ipset, ta set nó = False.


Giả sử, ta tạo ra 3 VM a b và c có ip lần lượt là 192.168.10.14, 192.168.10.15 và 192.168.10.16. Đồng thời tạo ra 2 security group là sg1 và sg2. Gán sg1 cho VM a và b, sg2 cho VM c. Trên sg2 ta tạo 1 rule chỉ cho phép ssh từ các VM thuộc sg1.

<img src="http://i.imgur.com/uCey5ph.png">

Khi này đã xuất hiện những rule liên quan đến sg1 trên sg2, do đó những port thuộc các VM tren sg1 sẽ được add vào 1 ipset. Mỗi khi trên sg1 có sự update, thì các port mới này sẽ được tự động add vào ipset.

Kiểm tra ipset, thấy xuất hiện 1 set chứa các ip thuộc sg1 có tên NIPv43e9c683a-ad22-411f-8f8e-

<img src="http://i.imgur.com/ugYRODL.png">

Kiểm tra iptables rules, thấy xuất hiện trường match set trên rule của VM c:

<img src="http://i.imgur.com/SymOaQv.png">

Giả sử tạo thêm 1 instance d và gán nó vào sg1, thì trong ipset xuất hiện thêm ip của instance này: 

<img src ="http://i.imgur.com/ozYlvWW.png">

Tài liệu tham khảo:

[1] : http://www.linuxjournal.com/content/advanced-firewall-configurations-ipset

[2] : http://git.openstack.org/cgit/openstack/neutron-specs/tree/specs/juno/add-ipset-to-security.rst#n28

[3] : http://blog.vccloud.vn/cau-hinh-firewall-su-dung-ipset/
