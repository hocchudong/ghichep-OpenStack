# Tìm hiểu về Cinder.

### 1 . Cinder là gì?

- Cinder là một Block Storage service trong OpenStack . Nó được thiết kế với khả năng lưu trữ dữ liệu mà người dùng cuối có thể sử dụng bỏi Project Compute (NOVA). 
Nó có thể được sử dụng thông qua các reference implementation (LVM) hoặc các plugin driver dành cho lưu trữ.

- Có thể hiểu ngắn gọn về Cinder như sau : Cinder là ảo hóa việc quản lý các thiết bị Block Storage và cung cấp cho người dùng một API 
đáp ứng được như cầu tự phục vụ cũng như yêu cầu tiêu thụ các tài nguyên đó mà không cần có quá nhiều kiến thức về lưu trữ.

### 2. Một số hình thức lưu trữ trong OpenStack.

|             |Lưu trữ tạm thời|Block Storage|Object Storage|
|-------------|----------------|-------------|--------------|
|Hình thức sử dụng |Dùng để chạy hệ điều hành và scrath space|Thêm một persistent storage vào VM|lưu trữ các VM iamge , disk volume , snapshot VM,....|
|Hình thức truy cập|Qua một file system|Một Block device có thể là một partition, formated, mounted (giống như là : /dev/vdc)|Thông qua RESTAPI|
|Có thể truy cập từ|Trong một VM|Trong một VM|Bất kỳ đâu|
|Quản lý bỏi|NOVA|Cinder|Swift|
|Những vấn đề tồn tại|VM được kết thúc|Có thể được xóa bởi người dùng|Có thể được xóa bởi user|
|Kích cỡ được xác định bởi|Người quản trị hệ thống cấu hình cài đặt kích cỡ, tương tự như là Flavors|Dựa theo đặc điểm yêu cầu của người dùng|Số lượng lưu trữ mà máy vật lý hiện có|
|Ví dụ điển hình|10GB đĩa thứ nhất, 30GB đĩa thứ 2|1TB disk|10s of TBs of dataset storage|

### 3. Cinder Architect .

![cinder-Architect](/images/cinder-Architect.png)

- Cinder-client : Người dùng sử dụng CLI/UI (Command line interface / User interface) để tạo request.
- Cinder-api : Chấp nhận và chỉ định đường đi cho các request.
- Cinder-scheduler : Lịch trình và định tuyến đường đi cho các request tới những volumes thích hợp.
- Cinder-volume : Quản lý thiết bị Block Storage.
- Driver : Chứa các mã back-end cụ thể để có thể liên lạc với các loại lưu trữ khác nhau. 
- Storage : Các thiết bị lưu trữ từ các nhà cung cấp khác nhau.
- SQL DB : Cung cấp một phương tiện dùng để back up dữ liệu từ Swift/Celp, etc,....

### 4. Volume API .

- Xem thêm tại [đây](https://developer.openstack.org/api-ref/block-storage/)

### 5. Cinder Driver.

- Cinder driver maps các Cinder requests yêu cầu từ dòng lệnh lên external storage platform.
- Có trên 50 loại driver tuy nhiên chúng ta thường sử dụng nhất là LVM (Logical Volume Managerment).
- Để set một volume driver chúng ta dùng tham số `volume_driver` trong file `cinder.conf`

```sh
volume_driver = cinder.volume.drivers.lvm.LVMISCSIDriver
```

- LVM sẽ maps các thiết bị Block storage vật lý trên các thiết bị Block storage ảo cấp cao hơn.
- Cinder Volume được khởi tạo như Logical Volumes bởi LVM.
- Sử dụng giao thức iSCSI để kết nối các volumes tới các compute nodes.
- Không có nhà cung cấp cụ thể.

`Cinder Attach Flow` 

![cinder-attach-flow](/images/cinder-attach-flow.png)

- Cinder gọi Cinder qua APi của cinder, truyền thông tin kết nối.
  - Ví vụ :  Host name, iSCSI initiator name, FC WWPNs
- Cinder-API chuyển thông điệp đến Cinder-volume.
- Sau đó trình kiểm tra lỗi đầu vào sẽ làm việc và gọi đến volume driver.
- Volume Driver sẽ chuẩn bị các yếu tố cần thiết để cho phép kết nối.
  - Ví dụ : Cho phép máy chủ NOVA có thể truy cập vào Volume.
- Volume driver trả về thông tin kết nối, được truyền cho NOVA.
  - Ví dụ : iSCSI iqn and portal, FC WWPN.
- NOVA tạo kết nối đến storage sử dụng thông tin được trả về.
- NOVA chuyển volume device/file tới hypervisor.


### 6. Cinder Status.

|Status|Mô tả|
|------|-----|
|Creating|Volume được tạo ra|
|Available|Volume ở trạng thái sẵn sàng để attach vào một instane|
|Attaching|Volume đang được gắn vào một instane|
|In-use|Volume đã được gắn thành công vào instane|
|Deleting|Volume đã được xóa thành công|
|Error|Đã xảy ra lỗi khi tạo Volume|
|Error deleting|Xảy ra lỗi khi xóa Volume|
|Backing-up|Volume đang được back up|
|Restore_backup|Trạng thái đang restore lại trạng thái khi back up|
|Error_restoring|Có lỗi xảy ra trong quá trình restore|
|Error_extending|Có lỗi xảy ra khi mở rộng Volume|


### Cinder back up.
- Cinder có thể back up một volume.
- Một bản back up là một bản sao lưu được lưu trữ vào ổ đĩa. Bản backup này được lưu trữ vào object storage.
- Backups có thể cho phép phục hồi từ :
 <ul>
  <li>Dữ liệu volume bị hư.</li>
  <li>Storage failure.</li>
  <li>Site failure (Cung cấp giải pháp backup an toàn).</li>
 </ul>

### 7. Advanced Features.

- Snapshot :
  - Một snapshot là một bản sao của một thời điểm của dữ liệu chứa một volume.
  - Một snapshot sẽ cùng tồn tại trên storage backend như một volume đang hoạt động.
- Quota :
  - Admin sẽ đặt giới hạn cho volume, khả năng backup và snapshot tùy thuộc vào chính sách cài đặt.
- Volume transfer :
  - Chuyển một volume từ user này đến một user khác.
- Encryption :
  - Mã hóa được thực hiện bởi NOVA sử dụng dm-crypt , là một hệ thống con minh bạch mã hóa đĩa trong Linux kernel.
- Migration (Admin only):
  - Chuyển dữ liệu từ back-end hiện tại của volume đến một nơi mới.
  - Hai luồng chính phụ thuộc vào việc volume có được gắn vào hay không.

# Tham khảo.

- 2 file đính kèm trong thư mục [ref](https://github.com/datkk06/ghichep-OpenStack/tree/master/05-Cinder/ref).