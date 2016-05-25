### Prevent arp spoofing trong openstack
- Từ phiên bản Liberty, openstack cung cấp 1 tính năng phòng chống tấn công giả mạo arp hay còn gọi là arp cache poisoning, nhằm đảm bảo an toàn trong truyền thông cho các máy ảo. 
- 1 cuộc tấn công giả mạo arp có thể được thực hiện ở trong mạng nội bộ bởi chính 1 VM nằm trong mạng đấy. Máy tấn công có thể gửi liên tục các bản tin arp giả mạo tới các máy nạn nhân hoặc tới gateway, nhằm thay đổi bảng arp trên các máy đó. Điều này dẫn tới việc truyền thông của các VM sẽ bị ảnh hưởng hoặc tệ hơn, là mọi thông tin đều bị attacker nghe lén và đánh cắp mà người dùng không hề phát giác được.
- Chi tiết về tấn công giả mạo arp có thể tham khảo ở đây: http://quantrimang.com/tim-hieu-ve-tan-cong-man-in-the-middle-%E2%80%93-gia-mao-arp-cache-66482

- Để ngăn chặn việc các máy ảo trong 1 vùng mạng private của 1 tenant có thể thực hiện 1 vụ tấn công arp, openstack cung cấp cơ chế prevent_arp_spoofing. Cơ chế này được khai báo trong /etc/neutron/plugins/ml2/ml2_conf.ini trên tất cả các node :

        [agent]
        ...
        prevent_arp_spoofing = True

Để kiểm tra tính năng này, ta sẽ thực hiện với 2 máy ảo trong môi trường openstack liberty như sau: 
<img src="http://i.imgur.com/LgKOIei.png">

- Máy victim chạy cirros os, có IP 192.168.10.14, MAC FA:16:3E:9F:39:18
- Gateway có IP 192.168.10.1, MAC fa:16:3e:3d:af:51
- Máy attacker chạy linux os, có IP 192.168.10.13, MAC fa:16:3e:22:0d:64 
 
Máy attacker được cài đặt tool tấn công arp có tên Dsniff. Máy này sẽ cố gắng gửi liên tục các bản tin arp giả mạo tới máy victim và gateway nhằm thay đổi arp cache: 

    $ sudo arpspoof 192.168.10.14 -t 192.168.10.1  #nói với gateway nó là máy có ip 192.168.10.14
    $ sudo arpspoof 192.168.10.1 -t 192.168.10.14  #nói với máy victim nó là gateway

<img src="http://i.imgur.com/oKG3vpW.png">

**1. Trường hợp enable tính năng prevent-arp-spoofing :**
    
 Việc gửi các bản tin giả mạo không ảnh hưởng tới arp table của máy victim và gateway do các bản tin này đã bị lọc ở mức ethernet frame.

 <img src="http://i.imgur.com/N287KDG.png">
 <img src="http://i.imgur.com/p3AEjjn.png">

 Ta thấy địa chỉ IP và MAC vẫn duy trì ở trạng thái chính xác mà không bị thay đổi. Quá trình ping giữa máy victim và gateway diễn ra bình thường. Tiến hành bắt gói tin ở máy attacker, ta không thu được các bản tin icmp nghe lén. 

**2. Trường hợp disable tính năng prevent-arp-spoofing:**

 Set giá trị prevent_arp_spoofing = False

 Sau khi gửi liên tục các bản tin giả mạo, arp cache trên máy victim và gateway đã bị thay đổi:
<img src="http://i.imgur.com/tjEq0rX.png">
<img src="http://i.imgur.com/BblacuN.png">

 Lúc này, ta thấy trên máy victim và gateway, ip của cả gateway và máy victim đều có MAC bị thay đổi theo MAC của máy attacker

Quá trình ping giữa victim với gateway hoặc với bất kì VM nào trong vùng mạng đều bị attacker nghe lén: 
 
<img src="http://i.imgur.com/jcdLAOn.png">

Tham khảo:

[1] : https://docs.oseems.com/general/operatingsystem/linux/sniff-network-traffic

[2] : http://quantrimang.com/tim-hieu-ve-tan-cong-man-in-the-middle-%E2%80%93-gia-mao-arp-cache-66482

