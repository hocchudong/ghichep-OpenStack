# Tìm hiểu về GlusterFS.

## 1. Tổng quan về GlusterFS.

- Thời đại bùng nổ của các dữ liệu lớn và sự tăng trưởng không ngừng nghỉ của các dịch vụ, khiến việc lưu trữ dữ liệu đơn 
thuần ở các server đơn khiến dữ liệu của bạn bị ì ạch khi truy cập và nguy hiểm khi gặp sự cố. Những dữ liệu được lưu trữ 
tập trung ở các file system đơn thuần trên đĩa cứng không có các giaỉ pháp backup định kì hoặc các gỉai pháp đảm bảo tính 
sẵn sàng cao thì khi gặp các sự cố gây mất mát dữ liệu, người quản trị viên sẽ rất lúng túng khi khôi phục dữ liệu hoặc cung 
cấp việc truy xuất dữ liệu trở lại bình thường.

- Lúc này một hệ thống file system mới được khai sinh với tên gọi GlusterFS (Cluster File System), có nhiệm vụ đảm bảo cho 
dữ liệu của bạn luôn trong trạng thái sẵn sàng và mở rộng không gian lưu trữ lên đến hàng terabytes và đồng thời phục vụ 
cho hàng ngàn máy khách (client). Hệ thống của bạn luôn được đảm bảo tính liên tục dưới "bàn tay" của GlusterFS kể cả khi 
có gặp các sự cố hoặc nhanh chóng nâng cấp không gian lưu trữ cho hệ thống của bạn mà không phải dừng toàn bộ hệ thống.

- GlusterFS cung cấp khá nhiều các mô hình (concept), ý tưởng xây dựng hệ thống lưu trữ và phân bổ dữ liệu nên chúng ta khá linh 
động trong việc gỉai các bài toán lưu trữ dữ liệu đem lại tính sẵn sàng cao cho dữ liệu của mình.

- GlusterFS chỉ cần các máy chủ storage (máy chủ lưu trữ dữ liệu có dung lượng lưu trữ lớn), và chúngđược kết nối với nhau qua mạng (network). 
Việc còn lại là triển khai các mô hình dữ liệu (concept) và chọn lựa các giao thức chia sẻ dữ liệu mà GlusterFS hỗ trợ điển hình là TCP/IP và Infiniband RDMA.

### Khi nào chúng ta nên sử dụng GlusterFS.

- Khi hệ thống của chúng ta cần duy trì tính liên tục, truy cập ổn định khi các 1 trong các server storage trong hệ thống của chúng ta 
bị down bất thường. Hoặc khi chúng ta có các dữ liệu rất lớn cần tối ưu hiệu năng tối đa trong việc truy cập và xử lý dữ liệu. Đơn gỉan là một hệ thống luôn ổn 
định trong mọi trường hợp, các việc truy xuất dữ liệu không bị gían đoạn. 

## 2. Một số định nghĩa trong GlusterFS.

|Định nghĩa|Mô tả|
|---------|------|
|Node|à một máy chủ lưu trữ (Server Storage) chạy hệ điều hành CentOS, Ubuntu,.... Chạy dịch vụ GlusterFS, chứa các Bricks|
|Bricks|Là một folder / mount point / file system trên một node để chia sẻ với các node tin cậy khác trong hệ thống (trusted storage pool) - Trên một node có thể có nhiều Brick (s). - Brick được dùng để gán (assign) vào các vùng dữ liệu (volume). - Các brick trong một volume nên có dung lượng lưu trữ (size) bằng nhau.|
|Volume|Một khối logic chứa nhiều bricks. Các cách thao tác lưu trữ và xử lí dữ liệu trên volume được định nghĩa bởi kiểu lưu trữ (concept volume). Một volume có thể chứa nhiều bricks từ các node khác nhau. Client muốn sử dụng File System thì sẽ mount volume chứ không sử dụng trực tiếp bricks.|


- Brick :

![bricks](/images/cinder/storage/bricks.png)

- Volume :

![volume](/images/cinder/storage/volume.png)

## 3. Các loại Volume trong GlusterFS.

- Khi sử dụng GlusterFS có thể tạo nhiều loại volume và mỗi loại có được những tính năng khác nhau. Dưới đây là 6 loại volume cơ bản.

### 3.1. Distributed volume:

Distributed Volume có những đặc điểm cơ bản sau:

- Dữ liệu được lưu trữ phân tán trên từng bricks, file1 nằm trong brick 1, file 2 nằm trong brick 2,...

- Vì metadata được lưu trữ trực tiếp trên từng bricks nên không cần thiết phải có một metadata server ở bên ngoài, giúp cho các tổ chức tiết kiệm được tài nguyên.

- Ưu điểm: mở rộng được dung lượng store ( dung lượng store bằng tổng dung lượng các brick)

- Nhược điểm: nếu 1 trong các brick bị lỗi, dữ liệu trên brick đó sẽ mất

![dis_volume](/images/cinder/storage/dis_volume.png)

### 3.2. Replicated volume:

- Dữ liệu sẽ được nhân bản đến những brick còn lại, trên tất cả các node và đồng bộ tất cả các nhân bản mới cập nhật.

- Đảm bảo tính nhất quán.

- Không giới hạn số lượng replicas.

- Ưu điểm: phù hợp với hệ thống yêu cầu tính sẵn sàng cao và dự phòng

- Nhược điểm: tốn tài nguyên hệ thống

![Replicated_Volume](/images/cinder/storage/Replicated_Volume.png)

### 3.3. Stripe volume:

- Dữ liệu chia thành những phần khác nhau và lưu trữ ở những brick khác nhau, ( 1 file được chia nhỏ ra trên các brick )

- Ưu điểm : phù hợp với những môi trường yêu cầu hiệu năng, đặc biệt truy cập những file lớn.

- Nhược điểm: 1 brick bị lỗi volume không thể hoạt động được.

![stripe_volume](/images/cinder/storage/stripe_volume.png)

### 3.4. Distributed replicated:

Kết hợp từ distributed và replicated

![dr_volume](/images/cinder/storage/dr_volume.png)

Với mô hình trên, hệ thống sẽ yêu cầu cần tối thiểu 3 node, vừa có thể mở rộng được dung lượng lưu trữ, vừa tăng tính dự phòng cho hệ thống. 
Tuy nhiên, nếu đồng thời bị lỗi 2 node server1 và server2 hoặc 2 node server3 và server4 thì hệ thống sẽ không hoạt động được.

### 3.5. Distributed stripe volume:

Kết hợp từ Distributed và stripe. Do đó nó có hầu hết những thuộc tính hai loại trên và khi 1 node và 1 brick delete đồng nghĩa volume cũng không thể hoạt động được nữa.

![ds_volume](/images/cinder/storage/ds_volume.png)

### 3.6. Replicated stripe volume:

Kết hợp từ replicated và stripe

![rs_volume](/images/cinder/storage/rs_volume.png)



# Tham khảo.

- https://github.com/meditechopen/mdt-technical/blob/master/TRIMQ/GlusterFS/glusterfs.md#33

- https://blog.0x1115.org/2015/08/19/glusterfs-file-server-co-tinh-san-sang-cao/