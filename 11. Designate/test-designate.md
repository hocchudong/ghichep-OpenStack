# Designate

##Designate cung cấp dịch vụ DNSaaS cho OpenStack.

- DNS cho openstack với single-tenant(mặc định) hoặc mutil-tenant
- Slave DNS
- Kết hợp với Nova/ Neutron tạo bản ghi tên máy <---> ip

##Cài đặt Designate:

Làm theo bước 1 và bước 2 thoe hướng dẫn ở link sau:

    https://github.com/vietstacker/devstack-note

Clone git của devstack về bằng lệnh git

Mặc định (nhánh master) trong git của devstack là source mới nhất của OpenStack.
 
Trong git của devstack chứa các phiên bản của OpenStack (Mitaka, Liberty, Kilo, Juno ...)

Trong hướng dẫn này sẽ thực hiển tải bản OpenStack Liberty

    git clone -b stable/liberty https://github.com/openstack-dev/devstack.git

Clone git của designate

    git clone -b stable/liberty https://github.com/openstack/designate.git

Thực hiện vào thư mục designate vừa clone về cà chạy file install.sh

    cd devstack
    ../designate/contrib/devstack/install.sh

Tạo file local.conf

Các shell trong devstack sẽ tham chiếu tới file local.conf để lấy giá trị các biến khi thực thi các dòng lệnh trong shell đó.

File local cần phải các các khao báo tối thiểu về password cho các dịch vụ trong OpenStack như: MySQL, RabbitMQ .... Các biến còn lại sẽ lấy giá trị mặc định.

Tùy vào tính năng cần test mà người dùng có thể khai báo trong file local.conf
Trong ví dụ này chúng tôi sử dụng dải mạng 192.168.1.0/24 cho dải EXTERNAL
Di chuyển vào thư mục devstack

    cd /devstack/

Tạo theo link sau:

    https://github.com/vietstacker/devstack-note/blob/master/file-local.conf-sample/devstack-designate-liberty.txt

chạy file

    cd /home/stack/devstack/

    ./stack.sh

##Tạo domain

Có thể dùng câu lệnh như sau:

    designate domain-create --name hocchudong.com. --email hocchudong@gmail.vn

    designate domain-list


Hoặc có thể dùng giao diện

   <img src="http://i.imgur.com/3sZE6kV.png">

   <img src="http://i.imgur.com/8GRkkHX.png">

##Tạo bản ghi cho domain

Các loại bản ghi mà Designate hỗ trợ

   <img src="http://i.imgur.com/iV7YnOs.png">

Tạo bản ghi A phân giải từ tên miền về IP (bản ghi AAA tương tự thay data là ipv6)
    
    designate record-create (id domian vừa tạo) --type A --name home.hocchudong.com. --data 172.16.10.4


hoăc sử dụng giao diện:
    
    <img src="http://i.imgur.com/EBAAWa9.png">

Tạo bản ghi bí danh CNAME

    designate record-create (id domain vừa tạo)  --type CNAME --name home.hocchudong.com. --data www.hocchudong.com.

với giao diện sẽ như sau:

   <img src="http://i.imgur.com/0kmGQew.png">

Đối với bản ghi PTR (bản ghi phân giải ngược từ ip sang tên miền)

Tạo domain và bản ghi mới hoàn toàn và bằng API theo hướng dẫn sau

    http://docs.openstack.org/developer/designate/howtos/manage-ptr-records.html

##Test Designate

Tạo máy ảo chuyển DNS về địa chỉ máy cài Designate và sử dụng lệnh Nslookup để test


##Link tham khảo

http://docs.openstack.org/developer/designate/

https://support.rc.nectar.org.au/docs/designate-commands

http://docs.openstack.org/cli-reference/content/designateclient_commands.html
