# Các ghi chép về cinder

## Các chú ý về volume
- Có 2 cách sử dụng volume: 
 - Sử dụng để gắn vào máy ảo đã được tạo trước đó: `bootable =  false`
 - Sử dụng để boot máy ảo: `bootable =  true`

![bootable](/images/cinder/bootable.png)

- File chứa trong thư mục `/var/lib/cinder/volumes` các các file quản lý volume được tạo ra, trong đó có đường dẫn tới volume.
```
root@cinder:/var/lib/cinder/volumes# cat volume-aa2f2db8-c93b-41ca-9119-d74310caa995

<target iqn.2010-10.org.openstack:volume-aa2f2db8-c93b-41ca-9119-d74310caa995>
    backing-store /dev/cinder-volumes/volume-aa2f2db8-c93b-41ca-9119-d74310caa995
    driver iscsi
    incominguser j5GJW8rYpq5cmd263oXE JCYsTBXrX26ium4F

    write-cache on
</target>
```

## I. Các lệnh thường dùng.

- Kiểm tra các volume trên LVM bằng lệnh: 
```sh
lvs

hoặc 

lsblk

```

![lsblk](/images/cinder/lsbsk.png)

- Volume được tạo trên LVM KHÔNG sử dụng cơ chế `thin` để cấp phát dung lượng lưu trữ (tạo bao nhiêu cấp bấy nhiêu.)

- Nếu tách máy Cinder thành 1 node (Cinder node) khác và không sử dụng backend thì mặc định volume được tạo ra sẽ lưu tại node cinder.

- Nếu boot máy ảo từ volume, file máy ảo sẽ nằm trên node Cinder. Node compute sẽ mount tới node cinder thông qua iscsi:

![img](/images/cinder/img.png)

## Các lệnh về volume

- Khởi động các dịch vụ của `Cinder`
```sh
# Trên Controller
service cinder-api restart
service cinder-scheduler restart

# Trên Cinder node (nếu triển khai tách node cinder)
service tgt restart
service cinder-volume restart
```

- Tạo volume
```sh
# Cú pháp đối với OpenStack Mitaka
openstack volume create --size kich_thuoc ten_volume

# Ví dụ tạo volume có kích thước 1Gb và tên là `volume01`
openstack volume create --size 1  volume01 
```

![create-volume-1](/images/cinder/create-volume-1.png)

- Kiểm tra danh sách các volume
```sh
openstack volume list
```

![volume-list](/images/cinder/volume-list.png)

`Gắn volume và gỡ volume khỏi máy ảo`

# Cú pháp lệnh gắn volume
openstack server add volume INSTANCE_ID VOLUME_ID

# Cú pháp lệnh gỡ volume
openstack server remove volume INSTANCE_ID VOLUME_ID

# Trong đó: 
 - INSTANCE_ID: ID của máy ảo (lấy id của máy ảo trên node compute với lệnh "openstack server list")
 - VOLUME_NAME: ID của volume (sử dụng lệnh openstack volume list để lấy id của volume)

# Ví dụ:

Lấy ID instane :

![instane_id](/images/cinder/instane_id.png)

Lấy id volume :

![volume_id](/images/cinder/volume_id.png)

Thực hiện add volume vào instane và kiểm tra :

![add_volume](/images/cinder/add_volume.png)


## Tạo Volume và launch instane từ volume đó :

### Tạo volume để launch instane :

- Lấy ID của image (vì chúng ta tạo volume có source image dùng để launch instane) :

```sh
openstack image list
```

![image_list](/images/cinder/image_list.png)

- Tạo volume có source image :

```sh
openstack volume create --image acc8392e-e360-4c31-92e1-9115f2d04c33 \
> --size 1 --availability-zone nova volume-test-1
```

Các giá trị :

|Giá trị|ý nghĩa|
|-------|-------|
|openstack volume create|Câu lệnh dùng để tạo volume mới|
|--image acc8392e-e360-4c31-92e1-9115f2d04c33|Đây là option nguồn là image với id phía sau : acc8392e-e360-4c31-92e1-9115f2d04c33|
| --size 1|Kích thước volume muốn tạo , ở đây là 1 GiB|
|--availability-zone nova|Đây là zone, thường là nova|
|volume-test-1|Tên của volume mới mà chúng ta muốn tạo|

- Sau khi tạo xong volume chúng ta sẽ nhận được kết quả trả về như sau :

![volume_create_succ](/images/cinder/volume_create_succ.png)

- Tiếp theo chúng ta tiến hành launch instane từ volume mới tạo này :

Thực hiện lấy danh sách các flavor :

```sh
openstack flavor list
```

![flavor_list](/images/cinder/flavor_list.png)

Thực hiện lấy danh sách các network :

```sh
openstack network list
```

![network_list](/images/cinder/network_list.png)

Lấy danh sách volume :

```sh
openstack volume list
```

![volume_list_instane](/images/cinder/volume_list_instane.png)

Sử dụng lệnh sau để tạo mới 1 instane :

```sh
 openstack server create --flavor 1 --volume 663fb70d-31b7-4b62-86e6-d263b2d808f4 \
  --nic net-id=4c711790-7cfc-42ab-8704-88d72680531a --security-group default vm4
```

ý nghĩa các giá trị :

|Lệnh/Tùy chọn|Ý nghĩa|
|-------------|-------|
|openstack server create|Lệnh để tạo mới một instane|
|--flavor 1|Tùy chọn flavor : chọn flavor có id là 1|
|--volume 663fb70d-31b7-4b62-86e6-d263b2d808f4|Tùy chọn volume, thực hiện launch instane với nguồn từ volume , volume đó có id là 663fb70d-31b7-4b62-86e6-d263b2d808f4|
|--nic net-id=4c711790-7cfc-42ab-8704-88d72680531a|Tùy chọn card mạng , với id của card mạng đó|
|--security-group default|Đặt sercurity group là default|
|vm4|Là tên của instane mà chúng ta muốn tạo|

Sau khi thực hiện lệnh trên với các tùy chọn đều thỏa mãn chúng ta sẽ thu được kết quả như sau :

![launch_instane_volume](/images/cinder/launch_instane_volume.png)

- Trên node compute chúng ta thực hiện kiểm tra xem instane đã được tạo thành công hay chưa :

```sh
openstack server list
```

![server_list_succ](/images/cinder/server_list_succ.png)


## II. Process Structure.

- Chúng ta có 4 quy trình tạo nên Cinder Service :

|Process|mô tả|
|---------|-----|
|Cinder-api|là một ứng dụng WSGI chấp nhận và xác nhận các yêu cầu REST (JSON hoặc XML) từ client và chuyển chúng tới các quy trình CInder khác nếu thích hợp với AMQP|
|Cinder-scheduler|Chương trình lập lịch các định back-end nào sẽ là điểm đến cho một yêu cầu tạo ra volume hoặc chuyển yêu cầu đó. Nó duy trì trạng thái không liên tục cho các back-end (Ví dụ : khả năng sẵn có , khả năng và các thông số kỹ thuật được hỗ trợ) có thể được tận dụng khi đưa ra các quyết định về vị trí . Thuật toán được sử dụng bởi chương trình lên lịch có thể được thay đổi thông qua cấu hình Cinder|
|Cinder-volume|Cinder-volume chấp nhận các yêu cầu từ các quy trình CInder khác đóng vai trò là thùng chứa hoạt động cho các trình điều khiển Cinder. Quá trình này là đa luồng và thường có một luồng thực hiện trên mỗi Cinder back-end giống như định nghĩa trong tập tin cấu hình Cinder.|
|Cinder-backup|Xử lý tương tác với các mục tiêu sao có khả năng sao lưu (Ví dụ như OpenStack Object Storage Service - Swift). Khi một máy client yêu cầu sao lưu volume được tạo ra hoặc quản lý.|


## Cinder Processes Concept Diagram:

![cinder-process-diagram](/images/cinder/cinder-process-diagram.png)

Hình bên trên mô tả quy trình tạo Volume , tiếp theo chúng ta cùng đến với quy trình tạo ra volume mới của Cinder :

![create-new-volume-diagram](/images/cinder/create-new-volume-diagram.png)

1. Client yêu cầu tạo ra Volume thông qua việc gọi REST API (Client cũng có thể sử dụng tiện ích CLI của python-client)
2. Cinder-api : Quá trình xác nhận hợp lệ yêu cầu thông tin người dùng , một khi được xác nhận một message được gửi lên hàng chờ AMQP để xử lý.
3. Cinder-volume thực hiện quá trình đưa message ra khỏi hàng đợi , gửi thông báo tới cinder-scheduler để báo cáo xác định backend cung cấp volume.
4. Cinder-scheduler thực hiện quá trình báo cáo sẽ đưa thông báo ra khỏi hàng đợi , tạo danh sách các ứng viên dựa trên trạng thái hiện tại và yêu cầu tạo volume theo tiêu chí (kích thước, vùng sẵn có, loại volume (bao gồm cả thông số kỹ thuật bổ sung)).
5. Cinder-volume thực hiện quá trình đọc message phản hồi từ cinder-scheduler từ hàng đợi. Lặp lại qua các danh sách ứng viên bằng các gọi backend driver cho đến khi thành công.
6. NetApp Cinder tạo ra volume được yêu cầu thông qua tương tác với hệ thống lưu trữ con (phụ thuộc vào cấu hình và giao thức).
7. Cinder-volume thực hiện quá trình thu thập dữ liệu và metadata volume và thông tin kết nối để trả lại thông báo đến AMQP.
8. Cinder-api thực hiện quá trình đọc message phản hồi từ hàng đợi và đáp ứng tới client.
9. Client nhận được thông tin bao gồm trạng thái của yêu cầu tạo, Volume UUID, ....


### Cinder & Nova Workflow - Volume Attach

![cinder-nova-workflow](/images/cinder/cinder-nova-workflow.png)

1. Client yêu cầu attach volume thông qua Nova REST API (Client có thể sử dụng tiện ích CLI của python-novaclient)
2. Nova-api thực hiện quá trình xác nhận yêu cầu và thông tin người dùng. Một khi đã được xác thực, gọi API Cinder để có được thông tin kết nối cho volume được xác định.
3. Cinder-api thực hiện quá trình xác nhận yêu cầu hợp lệ và thông tin người dùng hợp lệ . Một khi được xác nhận , một message sẽ được gửi đến người quản lý volume thông qua AMQP.
4. Cinder-volume tiến hành đọc message từ hàng đợi , gọi Cinder driver tương ứng với volume được gắn vào.
5. NetApp Cinder driver chuẩn bị Cinder Volume chuẩn bị cho việc attach (các bước cụ thể phụ thuộc vào giao thức lưu trữ được sử dụng).
6. Cinder-volume thưc hiện gửi thông tin phản hồi đến cinder-api thông qua hàng đợi AMQP.
7. Cinder-api thực hiện quá trình đọc message phản hồi từ cinder-volume từ hàng đợi; Truyền thông tin kết nối đến RESTful phản hồi gọi tới NOVA.
8. Nova tạo ra kết nối với bộ lưu trữ thông tin được trả về Cinder.
9. Nova truyền volume device/file tới hypervisor , sau đó gắn volume device/file vào máy ảo client như một block device thực thế hoặc ảo hóa (phụ thuộc vào giao thức lưu trữ).

## Tham Khảo :

- http://netapp.github.io/openstack-deploy-ops-guide/icehouse/content/section_cinder-processes.html