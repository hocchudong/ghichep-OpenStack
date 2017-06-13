# Hướng dẫn sử dụng Dashboard tạo máy ảo.
Sau khi cài đặt thành công Openstack, chúng ta bắt đầu sử dụng dashboard để tạo máy ảo. Bạn có thể tham khảo cài đặt openstack [tại đây](./file_config_nova_in_controller.md) 


## Đăng nhập vào Dashboard

  ![](../images/login.png)
  
- Đăng nhập bằng tài khoản admin

### 1. Add thêm rule
- Click tab `Project => Network => Security groups => MANAGE RULES`

  ![](../images/add_rule_1.png)
  
- Sau đó click `ADD RULE`

  ![](../images/add_rule_2.png)
  
- Chọn `Other Protocol` để mở tất cả các rule từ bên ngoài vào VMs. Bạn có thể chọn `SSH` để đăng nhập vào máy ảo thông qua ssh (chọn `Other Protocol` thì cũng đã bao gồm cả ssh rồi).

  ![](../images/add_rule_3.png)
  
### 2. Tạo network
- I. Tạo dải mạng cho phép máy ảo ra ngoài internet.

  - Click tab `Admin => Networks => CREATE NETWORK`
  
    ![](../images/network_1.png)
    
  - Điền các thông tin như hình sau rồi SUBMIT.
  
    ![](../images/network_2.png)
    
    ```sh
    Name: provider
    Project: admin
    Provider Network Typy: Flat
    Physical Network: provider
    Admin State: UP
    Shared: checked
    External Network: checked
    ```
  
  - Tạo sub-net.
    
    ![](../images/network_3.png)
    
  - Click vào tab `Subnets => CREATE SUBNET`
  
    ![](../images/network_4.png)
    
  - Khai báo dải địa chỉ mạng. Dải địa chỉ này trùng với dải địa của node controller dùng để ra ngoài internet, là dải mà trong mô hình chúng ta dùng để provider network.
  
    ![](../images/network_5.png)
    
  - Khai báo pool ip và ip của DNS
  
    ![](../images/network_6.png)
    
- II. Tạo dải mạng cục bộ cho từng project.
  
  - Click `Project => Network => Networks => CREATE NETWORK`
  
    ![](../images/network_admin_1.png)
    
  - Đặt tên cho network => click next.
  
    ![](../images/network_admin_2.png)
    
  - Khai báo tên subnet và địa chỉ mạng của subnet.
  
    ![](../images/network_admin_3.png)
    
  - Khai báo pool ip và id của DNS
  
    ![](../images/network_admin_4.png)
    
- III. Tạo router cho project admin
  
  - `Project => Network => Routers => CREATE ROUTER`
  
    ![](../images/router_1.png)
    
  - Đặt tên và chỉ ra dải mạng ngoài cho router. Dải mạng ngoài ngoài chọn `Provider
    
    ![](../images/router_2.png)
    
  - Add interface cho router
    
    ![](../images/router_3.png)
    
  - Click tab `interfaces => ADD INTERFACE`
  
    ![](../images/router_4.png)
    
  - Chọn sub-net là self-service.
  
    ![](../images/router_5.png)
    
### 3. Tạo flavor. 
- Click `Admin => Flavors => CREATE FLAVOR`

  ![](../images/flavor_1.png)
  
- Tạo mới một flavor.

  ![](../images/flavor_2.png)
  
  ```sh
  name: m1.medium
  VCPUs: 1
  RAM: 512 MB
  DISK: 5 GB
  ```
  
### 4. Tạo máy ảo.
- I. Tạo máy ảo gắn vào card mạng self-service.
  - Click `Project => Compute => Instances => LAUNCH INSTANCE`
  
    ![](../images/vm1.png)
    
  - Đặt tên `mv69`, số lượng `1`.
  
    ![](../images/vm2.png)
    
  - Chọn images cho VM.
  
    ![](../images/vm3.png)
    
  - Chọn flavor.
  
    ![](../images/vm4.png)
    
  - Chọn network => click `LAUNCH INSTANCE`
  
    ![](../images/vm5.png)
    
  - Chờ một lát sẽ có kết quả như hình sau. Click vào máy ảo.

    ![](../images/vm6.png)
    
  - Click tab `Console => Click here to show only console`
    
    ![](../images/vm7.png)
    
  - Đăng nhập vào vm69 với user: `cirros` và password: `cubswin:)`
  
    ![](../images/vm8.png)
    
### 5. Associate Floating Ip cho VM để VM có thể ra ngoài internet.
- Chọn Associate Floating Ip.

  ![](../images/floating_1.png)
  
- Ban đầu sẽ không có địa ip nào, click vào `+` để xin cấp 1 địa chỉ ip.

  ![](../images/floating_2.png)
  
- Chọn provider, click `ALLOCATE IP`

  ![](../images/floating_3.png)
  
- Sau đó sẽ được cấp 1 IP và chọn vào `Associate`

  ![](../images/floating_4.png)
  
- Kết quả sau khi floating ip cho Vm.

  ![](../images/floating_5.png)
  
- Bạn có thể kiểm tra kết nối từ ngoài vào bằng cách ping tới địa chỉ đã được floating cho vm. Ở đây là địa chỉ `172.16.69.199`

- Bây giờ sẽ đăng nhập vào VM và kiểm tra kết nối ra ngoài internet.

  ![](../images/ping.png)
  
### 6. Tạo một máy ảo với card mạng được gắn là provider.
- Các bước tạo máy ảo theo trình tự như tạo máy ảo ở trên.

  ![](../images/vm_1.png)
  
  ![](../images/vm_2.png)
  
  ![](../images/vm_3.png)

  ![](../images/vm_4.png)
  
  - Đến bước chọn card mạng, chúng ta chọn `provider`.
  
  ![](../images/vm_5.png)
  
- Sau khi tạo xong, đăng nhập vào để kiểm tra kết nối internet.

  ![](../images/vm_6.png)
  
- Kết quả sau đây cho thấy máy đã được ngoài internet.

  ![](../images/vm_7.png)
  
- Và đây là Topology mạng trên hệ thống.

  ![](../images/topology.png)
  
---
Trên đây là ghi chép lại quá trình thực hành tạo máy ảo của mình một các cơ bản nhất. Bài viết hy vọng sẽ cung cấp cho bạn một cách tạo máy ảo cơ bản. Chúc bạn thành công :)