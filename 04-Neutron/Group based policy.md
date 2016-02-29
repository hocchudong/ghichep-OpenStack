### Group based policy

1. GBP là gì:
GBP là 1 openstack API framework cung cấp 1 mô hình miêu tả các yêu cầu về ứng dụng mà không phụ thuộc vào cơ sở hạ tầng. 
GBP tạo 1 tập hợp các group với các chính sách nhằm miêu tả kết nối giữa các group đó. Hiện nay GBP chỉ tập trung vào network, nhưng trong tương lai nó sẽ mở rộng ra những dịch vụ khác.

2. Tại sao cần GBP
GBP thu thập những yêu cầu và triển khai những ứng dụng phức tạp trong openstack. Nó tạo sự kết nối giữa người phát triển ứng dụng và người quản trị hệ thống
 - Dependency mapping: GBP cho phép người dùng chỉ định mối quan hệ giữa các lớp ứng dụng, và cho phép chúng phát triển độc lập với nhau. Đồng thời giúp đơn giản hóa việc co dãn và tự động hóa tài nguyên
 - Separation of concerns: GBP tách riêng những yêu cầu bảo mật về ứng dụng (ai có thể nói chuyện vs ai) với những yêu cầu về network . Điều này cho phép các nhóm phát triển khác nhau có thể hoạt động độc lập mà vẫn hợp tác dc vs nhau.
 - Network service chaning: GBP trửu tượng hóa các dịch vụ network và cho phép người dùng miêu tả các yêu cầu về network như 1 phần của triển khai ứng dụng .
 
3. GBP hoạt động ntn:
GBP cung cấp giao diện API có thể truy cập thông qua Horizon(group-based-policy-ui), heat (group-based-policy-automation), hoặc CLI (group-based-policy-client).
Nó đóng vai trò như 1 thành phần nằm phía trên neutron. GBP cung cấp 2 cơ chế map tới cơ sở hạ tầng:
 - Neutron mapping driver: chuyển những tài nguyên GBP(các policy) thành lời gọi neutron api. 
 - Native drivers: Các policy được dịch thông qua SDN controller mà không cần dịch sang neutron api. 

4. Mô hình GBP:
 - Policy target: 1 network endpoint riêng biệt(NIC). Đây là thành phần cơ bản nhất trong mô hình GBP. Có thể map trực tiếp tới network port
 - Policy group: gồm nhiều policy target có chung thuộc tính, có thể map tới các subnet. Policy group sẽ tương tác với các rule set bằng 2 cách thức: provide hoặc consume
 - Policy Classifier: cách thức lọc traffic network thông qua các thuộc tính như port, giao thức và hướng (in, out hoặc bidirectional)
 - Policy action: quyết định đối với 1 gói tin khi thỏa mãn rule nào đấy. Có thể định nghĩa là allow, redirect, log...
 - Policy rule sets: tập hợp của nhiều policy rules. 1 policy rule bao gồm policy classifier và policy action.
 
GBP thích hợp với các ứng dụng đa tầng, khi mà mỗi tầng ứng dụng được gán bởi 1 group policy khác nhau. 
<img src="https://wiki.opendaylight.org/images/5/51/App-Policy-Overview.png">

5 . Triển khai GBP trên môi trường openstack:
 - Thêm dòng sau vào file **/etc/apt/sources.list**:

            deb http://ppa.launchpad.net/group-based-policy-drivers/ppa/ubuntu utopic main

 - Cài đặt GBP packages:

            sudo apt-get update
            sudo apt-get install group-based-policy group-based-policy-automation group-based-policy-ui python-group-based-policy-client

 - Thêm GBP plugin và driver vào **/etc/neutron/neutron.conf** trên node network và controller:

            service_plugins =group_policy,servicechain
            ...
            [group_policy]
            policy_drivers = implicit_policy, resource_mapping
            ...
            [servicechain]
            servicechain_drivers = simplechain_driver

 - Update GBP packages:

            sed -i 's/gbpautomation/group_based_policy_automation/g' /usr/lib/python2.7/dist-packages/gbpautomation/__init__.py 

 - Thêm GBP vào dashboard:
 
            ln -s /usr/lib/python2.7/dist-packages/gbpui/_*project*.py /usr/share/openstack-dashboard/openstack_dashboard/enabled

 - Tạo GBP database:
 
            gbp-db-manage --config-file /etc/neutron/neutron.conf upgrade head

 - Khởi động lại các dịch vụ:

            service neutron-server restart
            service heat-api restart
            service heat-api-cfn restart
            service heat-engine restart
            service apache2 restart

Hoàn thành cài đặt GBP trên openstack. Giờ ta có thể sử dụng GBP API thông qua giao diện dòng lệnh CLI hoặc trực tiếp trên dashboard của openstack. 

<img src="http://i.imgur.com/o1NNaBx.png">
