# Hướng dẫn sử dụng Dashboard tạo máy ảo.
Sau khi cài đặt thành công Openstack, chúng ta bắt đầu sử dụng dashboard để tạo máy ảo. Bạn có thể tham khảo cài đặt openstack [tại đây](./install_controller.md) 

# Mục lục
- [1. Add thêm rule](#1)
- [2. Tạo network](#2)
- [3. Tạo flavor](#3)
- [4. Tạo máy ảo card mạng self-service.](#4)
- [5. Tạo một máy ảo với card mạng được gắn là provider.](#5)
- [6. Tạo máy ảo với keypair.](#6)

<a name=1></a>
## Đăng nhập vào Dashboard

  ![](../images/login.png)
  
- Đăng nhập bằng tài khoản admin

## 1. Add thêm rule
- Click tab `Project => Network => Security groups => MANAGE RULES`

  ![](../images/add_rule_1.png)
  
- Sau đó click `ADD RULE`

  ![](../images/add_rule_2.png)
  
- Chọn `Other Protocol` để mở tất cả các rule từ bên ngoài vào VMs. Bạn có thể chọn `SSH` để đăng nhập vào máy ảo thông qua ssh (chọn `Other Protocol` thì cũng đã bao gồm cả ssh rồi).

  ![](../images/add_rule_3.png)
  
<a name=2></a>
## 2. Tạo network
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
    
<a name=3></a>
## 3. Tạo flavor. 
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
  
<a name=4></a>
## 4. Tạo máy ảo card mạng self-service.

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
    
- II. Associate Floating Ip cho VM để VM có thể ra ngoài internet.
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
  
<a name=5></a>
## 5. Tạo một máy ảo với card mạng được gắn là provider.
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
  
<a name=6></a>
## 6. Tạo máy ảo với keypair.
- Keypair dùng để đăng nhập vào máy ảo thông qua ssh mà không cần sử dụng mật khẩu.
- Phần này sẽ hướng dẫn tạo máy ảo với keypair.
- Bạn có thể chọn cách tạo máy ảo bằng 1 trong 2 loại card mạng như trên. 
- Tôi xin phép hướng dẫn tạo máy ảo bằng card self-service có thêm keypair.
- Các bước ban đầu hoàn toàn giống với hướng dẫn ở trên.

  ![](../images/vm_keypair.png)
  
  ![](../images/vm_keypair_1.png)
  
  ![](../images/vm_keypair_2.png)
  
  ![](../images/vm_keypair_3.png)

  ![](../images/vm_keypair_4.png)
  
- Sau khi chọn card mạng cho máy ảo, click vào `Key Pair`

  ![](../images/vm_keypair_5.png)

- Đặt tên cho key và click `Create keypair`

  ![](../images/vm_keypair_6.png)

  ![](../images/vm_keypair_7.png)
  
- Sau khi click vào Create keypair, hệ thống sẽ thông báo cho biết sẽ tự động download một file key có đuôi `.pem`. Ở đây là `key-test.pem`. Nếu không thấy tự động download thì bạn có thể download key về theo đường dẫn. Chú ý là sau này sẽ không thể download được key này. Sau đó thì `LAUNCH INSTANCE` thôi.
- Sau khi tạo xong máy ảo theo các bước trên, ta cần phải Associate Floating Ip cho máy ảo. Bước này mình không viết lại vào đây nữa.

  ![](../images/vm_keypair_8.png)

- Ta có thể thấy, địa chỉ Floating IPs là `172.16.69.199` và Key Pair là có `key-test`.
- Kiểm tra ping đến địa chỉ `172.16.69.199` xem có kết quả không. Thực hiện trên cmd

  ![](../images/vm_keypair_9.png)

- Kết quả ping thành công.
- Bây giờ ta sẽ sử dụng cái key đã download lúc nãy để thực hiện đăng nhập vào máy ảo.
- Chúng ta sử dụng một phần mềm có tên là `puttygen` để lưu lại file có đuôi là `.ppk`
- Giao diện phần mềm như hình sau. Click vào load để load file `key-test.pem` đã tải về lúc nãy.

  ![](../images/vm_keypair_10.png)
  
- Bạn nhớ chọn `All files (*.*)` để có thể hiện ra file `key-test.pem`. Nếu không chọn sẽ không hiện thị được file pem này.

  ![](../images/vm_keypair_11.png)
  
- Sau đó `Save private key`. Sau đó bạn cứ click `yes`, ở đây là một vấn đề bảo mật trong kỹ thuật sử dụng key pair trong ssh. Tôi không giải thích ở đây.

  ![](../images/vm_keypair_12.png)
  
- Đặt tên file và lưu bình thường như các phần mềm khác. Sau khi lưu, chúng ta được một file như sau

  ![](../images/vm_keypair_13.png)
  
- Bây giờ chúng ta sẽ đăng nhập vào máy ảo thông qua ssh mà không cần sử dụng mật khẩu. Mình sử dụng một phần mềm hỗ trợ đăng nhập từ xa rất phổ biến là `MobaXterm`
- Chọn `Session => SSH` sau đó điền địa chỉ IP: 172.16.69.199, click vào `Use private key` và trỏ đến file `key-test.ppk`. 
- Sau khi điền đầy đủ thông tin, click `Ok` là xong.

  ![](../images/vm_keypair_14.png)
  
- Đăng nhập vào với tên user là `cirros` và kiểm tra ping ra internet.

  ![](../images/vm_keypair_15.png)
  
  
---
Trên đây là ghi chép lại quá trình thực hành tạo máy ảo của mình một các cơ bản nhất. Bài viết hy vọng sẽ cung cấp cho bạn một cách tạo máy ảo cơ bản. Chúc bạn thành công :)