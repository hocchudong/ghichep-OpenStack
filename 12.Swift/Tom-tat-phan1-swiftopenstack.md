#Chapter 1: Sự phát triển của lưu trữ dữ liệu

- Nhu cầu về dữ liệu tăng cao như dữ liệu đa phương tiện, game, video, hình ảnh, ca nhạc...
- Phát triển SDS (Sofware-defined storage)  khiến hệ thống lưu trữ dễ dàng truy cập và mở rộng
- Yêu cầu về lưu trữ dữ liệu cần đảm bảo các yếu tố: 
  + Độ bền: đảm bảo dữ liệu không bị hỏng hoặc mất kể cả với các lý do khách quan
  + Tính sẵn sàng: dữ liệu cần luôn sẵn sàng để được sử dụng với mọi loại thiết bị với người dùng khác nhau.
  + Khả năng quản lý: dữ liệu nhiều tuy nhiên phải được quản lý dễ dàng
  + Chi phí thấp: khả năng mở rộng sẽ rất cao nên cần chi phí phần cứng hay nhân công khi mở rộng cần thấp nhất có thể.
  
 - Định lý CAP về hệ thống máy tính phân tán: chỉ đảm bảo được 2 trong 3 yếu tố: tính nhất quán, tính sẵn có, hoặc khả năng phân vùng.
 - Swift đảm bảo được tính sẵn có và khả năng phân vùng
 - So sánh về các loại storage:
https://github.com/canvietanh/ghi-chep-storage/blob/master/Block-object-filesystem.md
- Kiến trúc lưu trữ mới với SDS (đề cao khả năng chịu lỗi) gồm 4 thành phần chính:
 + Định tuyến lưu trữ: định tuyến yêu cầu tránh các node lỗi
 + Khả năng phục hồi lưu trữ: Có quy trình kiểm tra dữ liệu lỗi để khôi phục
 + Phần cứng vật lý: dùng để lưu trữ
 + Bộ điều khiển: cần quản lý tập trung với quy mô lớn
 
#Chapter 2: Swift
- Là project multi-tennant dùng lưu trữ dữ liệu phi cấu trúc như tài liệu, nội dung web, backup...
- Đặc điểm của Swift
 + Khả năng mở rộng: chỉ cần thêm các node lưu trữ
 + Đảm bảo độ bền: có các bản sao dữ liệu đảm bảo độ bền
 + Đa khu vực: Thực hiện với các khu vực địa lý khác nhau.
 + Tính đồng thời: Sử dụng nhiều server 1 lúc
 + Lưu trữ linh hoạt: như vs các dữ liệu cần nhanh thì có thể dùng ổ ssd (dựa vào chính sách lưu trữ)
 + Mã nguồn mở
 + Hệ sinh thái lớn: nhiều tool phát triển xung quan để hỗ trợ.
 + Chạy trên các phần cứng thương mạ: ko cần chuyên dụng đảm bảo chi phí thấp.
 + Thân thiện với nhà phát triển: nhiều thư viện cho các ngôn ngữ khác nhau, nhiều tính năng hỗ trợ như đặt thời gian tồn tại url, dữ liệu....
 
#Chapter 3: Kiến trúc và mô hình dữ liệu Swift
Các thông số liên kết với nhau tạo ra điểm lưu trữ:

- /account: Tài khoản vị trí lưu trữ là 1 tên khu vực lưu trữ duy nhất, nơi sẽ chứa các metadata(thông tin mô tả) về tài khoản này, cũng như nơi chứa tài khoản. Lưu ý trong Swift 1 tài khoản ko phải là 1 danh tính người dùng mà là 1 khu vực lưu trữ.

- /account/container: là vùng lưu trữ được định nghĩa phía trong account nơi mà các metadata về container và danh sách các object mà container đó lưu trữ.

- /account/container/object: vị trí lưu trữ đối tượng là nơi dữ liệu đối tượng và metadata của nó đc lưu trữ.

<img src="http://i.imgur.com/y3Tyy9j.png">

##Kiến trúc lưu trữ:
###Cluster --> Region --> Zone --> Node

- Region: chia thành các vùng vật lý khác nhau. Có thể là single-region hoặc multi-region. Với multi-region dữ liệu được sao ở nhiều điểm khác nhau. Khi lấy dữ liệu sẽ lấy ở điểm có độ trễ thấp nhất (gọi là lựa chọn quen thuộc)
- Zone: chia thành các zone như các trung tâm lưu trữ hay các rack khác nhau để cô lập lỗi
- Node: Server vật lý chạy 1 hoặc nhiều máy chủ xử lý swift.
- Chính sách lưu trữ: được cấu hình để đảm bảo lưu trữ linh hoạt và mạnh mẽ.

<img src="http://i.imgur.com/8A9XBf6.png">

###Về các tiến trình lưu trữ:

- Proxy process: Đảm bảo giao tiếp với client
- Account process: cung cấp metadata của account và danh sách container trong account đó
- Container process: cung cấp metadata của container và danh sách các object trong nó.
- Object process: Lưu trữ, truy xuất, xóa dữ liệu trên các ổ cứng

###Tiến trình thống nhất

Các tiến trình trên để đảm bảo lưu trữ. Còn có các tiến trình để đảm bảo tính thống nhất, khả năng chịu lỗi cho dữ liệu.

- Auditor(account, container, object):  Những auditor account, container, object sẽ liên tục quét trên các ỏ cứng trên các nốt lưu trữ dữ liệu để đảm bảo rằng dữ liệu không bị hệ thống làm hư hỏng. Nếu phát hiện ra dữ liệu bị hư hỏng, các auditor sẽ chuyển dữ liệu đó đến khu vực kiểm tra riêng.
- Repicator (account, container, object): Tiến trình này sẽ đảm bảo đủ các bản copy của dữ liệu mới nhất được lưu trữ trên các cluster. Các replicator account, container, object chạy ngầm với các tiến trình tương ứng. Luôn so sánh với dữ liệu ở 1 node trung tâm để có thể kiểm tra backup.
- Reaper (account): Khi reaper account thấy 1 account bị đánh dấu là xóa, nó sẽ bắt đầu gỡ bỏ hết các liên kết giữa các container và object liên quan đến account đó và sau cùng là lại bỏ bản ghi account đó. Để tránh lỗi, các reaper account sẽ được cấu hình với 1 độ trễ nhất định trước khi nó bắt đầu xóa dữ liệu. 
- Updater (container, object): chịu trách nhiệm giữ các danh sách container tới 1 kỳ hạn. Nó sẽ cập nhật số lượng các object, số lượng container và số byte được sử dụng trong metadata account.
- Expier (object): chỉ định đối tượng tự động xóa sau 1 khoảng thời gian nhằm thanh lọc dữ liệu được chỉ định.

###Định vị dữ liệu:

- Sử dụng hàm băm Rings: dùng md5 băm vị trí đối tượng, rồi chia cho số ổ lấy dư ra ổ lưu trữ
- Hàm băm cải tiến: Băm thông tin ổ (tên ổ, địa chỉ ổ...) Xếp vào 1 vòng trong (vòng rings) hàm bă dữ liệu gần với thông số, trong khoảng nào thì sẽ được lưu trong ổ đó.

<img src="http://i.imgur.com/dUZln7t.png">

- Sửa đổi hàm băm cho phù hợp: Mỗi ổ sẽ có  nhiều khoảng trong vòng rings chứ không chi 1 khoảng. Và các khoảng sẽ được cố định. Được gọi là các partion.
Thông số partion power(?).
 số (partion) trong cluster = 2^(partion power)

<img src="http://i.imgur.com/lgkmL2H.png"> 

- Replica count:(Số bản sao) thường là 3.

- Replica locks: Khóa dữ liệu khi có sự dịch chuyển ổ.

Ngoài sử dụng vòng rings thì còn sử dụng 2 thông số:

- Weight: đánh trọng số cho thiết bị, trọng số càng cao thiết bị càng được nhiều partion.
- Unique as possible: đảm bảo các bản sao được phân bố xa nhau nhất có thể.

###Tạo và cập nhật rings.
- Dựa vào file ring-builder: Các file builder riêng biệt được tạo cho các account, container và tứng chính sách lưu trữ object, nó chứa thông tin như partion power, repica count, replica lock time và vị trí của ổ trong cluster. Swift sử dụng ring-builder để cập nhật các file builder với các thông tin cập nhật  trong ổ đĩa.Lưu ý quan trọng là thông tin trong mỗi file builder này là tách biệt với các file khác. Ví dụ như có thể thêm 1 số ổ đĩa cho account và conatainer nhưng không được cho object
- Cân bằng rings: Khi các builder file được tạo hoặc cập nhật với tất cả thông tin cần thiết, rings sẽ được tạo. Tiện ích rings-builder chạy sử dụng các lệnh rebalance với builder file là tham số đầu vào. Điều này được thực hiện cho mỗi rings: accouunt, container, object. Mỗi khi rings được tạo , nó phải sao chép tới tất cả các node, thay thế cho những  rings cũ.

###Bên trong các rings:
Mỗi lần Swift xây dựng rings, 2 cấu trúc dữ liệu nội bộ quan trọng được tạo ra và truyền vào trong file builder:

- Devices list: Ring-builder chứa danh sách tất cả thiết bị mà chúng ta muốn thêm và file ring-builder. Mỗi ổ bao gồm các thông số ID, zone, trọng số, địa chỉ IP, port và tên thiết bị.

<img src="http://i.imgur.com/9nNh5Pi.png">

- Bảng tra cứu thiết bị: Bảng này chứa 1 hàng cho mỗi bản sao và cột là cho mỗi partion trong cluster, thường là có 3 hàng và hàng ngàn cột. Ring-bui;để tính toán các ổ đĩa tối ưu để đặt mỗi bản sao phân vùng trên ổ đĩa bằng cách sử dụng các trọng số và thuật toán sắp xếp unique-as-posible. Sau đó ghi lại các ổ vào trong bảng

<img src="http://i.imgur.com/TWTHthh.png">

#Chapter 4: Basic Swift
##Gửi yêu cầu
Nếu bạn gửi yêu cầu tới các Swift cluster, nó phải chứa đủ các thành phần sau:
###1. Storage URL: 
Cách yêu cầu gửi đến cluster và phải chỉ ra được vị trí trong cluster mà yêu cầu nhắm đến
- Vị trí cluster (swift.example.com/v1): Phần đầu của Storage URL là 1 endpoint trong cluster. Nó được sửu dụng bởi việc mạng sẽ định tuyến yêu cyaf tới các node có tiến trình máy chủ proxy để yêu cầu của bạn có thể được sử lý
- Vị trí lưu trữ (account/container/object): bào gồm 1 hoặc nhiều phần tạo nên sự duy nhất của vị trí dữ liệu. Các vị trí lưu trữ ccos thể là 1 trong 3 dạng tùy thuộc vào tài nnguyeen mà bạn đang có gắng gửi yêu cầu:
 + Account: /account
 + Container: /account/container
 + Object: /account/container/object
Lưu ý: Tên đối tượng có thể chứa ký tự gạch chéo (/) vì vậy việc giả lồng thư mục là hoàn toàn có thể xảy ra

###2.Thông tin xác thực
- Thông qua những thông tin xác thực ở mỗi lần gửi yêu cầu
- Thông qua xác thực token

###3.Động từ HTTP
Chúng ta sẽ xem xét kỹ những hành động khác nhau khi yều cầu giao tiếp với HTTP. Swift sử dụng các động từ chuẩn HTTP như sau:
- GET: Download object(cùng metadata), hoặc list nội dung của container hoặc account
- PUT: upload object, tạo container hoặc ghi đè metadata headers.
- POST: cập nhật metadata (account hoặc container) ghi đè metadata(đối tượng) hoặc tạo container nếu nó chưa tồn tại
- DELETE: xóa object hoặc container trống
- HEAD: Lấy thông tin header, bao gồm metadata của account, container, object

###4. Tùy chọn: dữ liệu hoặc metadata được ghi.

##Ủy quyền
Mặc dù người dùng có thể có thông tin hợp lệ để truy cập vào Swift cluster, nhưng họ có thể không được cấp phép cho những hành động mà họ gửi trong yêu cầu. Các máy chủ proxy sẽ cần xác nhận ủy quyền trước khi cho phép các yêu cầu để hoàn thành
Ví dụ: Nếu bản gửi 1 yêu cầu với thông tin hợp lệ, nhưng cố gắng thêm dữ liệu vào 1 account khác thì bạn vẫn sẽ được xác thực nhưng sẽ bị từ chối yêu cầu.
Nếu các hành động là được phép, các tiến trình máy chỉ proxy sẽ gọi đúng các node được yêu cầu, các node sẽ trả về kết quả của yêu cầu, và proxy sẽ trả về các phản hồi HTTP.

##Phản hồi
Các phản hồi từ Swift cluster sẽ chứa 2, hoặc thường là 3 các thành phần sau:
- Mã phản hồi và mô tả
- Header
- Data
Mã phản hồi và mô tả sẽ cho bạn biết biết yêu cầu của bạn được hoàn thành. Rộng ra có 5 mẫu mã phản hồi
- 1xx(thông tin): ví dụ 100 continue
- 2xx(thành công): ví dụ 200 OK hoặc 201 created
- 3xx(chuyển hướng): ví dụ 300 multiple choices hoặc 301 Moved Permanently
- 4xx(lỗi người dùng): ví dụ 400 bad request hoặc 401 là unauthorized
- 5xx(lỗi server): 500  Internal Server Error

##Sử dụng CLI
Command-Line Interfaces
Chúng ta sẽ xem xét 2 câu lệnh cURL vs Swift. Cả 2 câu lệnh đều cho phép người dùng gửi yêu cầu 1 dòng 1 lần tới các Swift Cluster. 

Sử dụng cURL (clinent for URL)
là câu lệnh phổ biến để chuyển dữ liệu đến và đi sử dụng các cấu trúc URL. Nó thường được cài đặt trước hoặc dẽ dàng được cài đặt bằng câu lệnh. cURL cung cấp chi tiết kiểm soát yêu cầy HTTP nên nó có thể xử lý tất cả các yêu cầu Swift. Vì cURL lấy các động từ HTTP 1 cách rõ ràng nên nó thường được sử dụng cung cấp ví dụ cho Swift
cURL gồm các thành phần sau:
+ curl
+ -X <method> tùy chọn chỉ ra động từ HTTP (get, post, put..)
+ thông tin xác thực
+ đường dẫn storage URL
+ Dữ liệu hoặc metadata (tùy chọn)

curl -X <HTTL-verb> [] <storage-url> <object.ext>

Chúng ta cùng xem xét 1 vài ví dụ về HTTP GET từ 1 người dùng tên Bob để xem cách cURL được sử dụng cho object, container, account. 1 cách phổ biến để sử dụng Swift là nơi mọi người dùng đều có chính xác 1 tài khoảnh. Chúng ra sẽ sử dụng mô hinhg đó ở đây, nên URL cho Bob sẽ là  http://swift.example.com/v1/AUTH_bob. Đây sẽ là những tác vụ mà Bob sẽ thực hiên thông thường trong Swift.
- Tạo conainter mới: tạo lệnh put với vị trí container mới
 curl -X PUT [...] /
 http://swift.example.com/v1/AUTH_bob/container2 
- List tất cả các container có trong account sử dụng get và chỉ ra địa chỉ account
 curl -X GET [...] /
 http://swift.example.com/v1/AUTH_bob 
- Upload đối tượng: sử dụng PUT tới vị trí của đối tượng
 curl -X PUT [...] /
 http://swift.example.com/v1/AUTH_bob/container1 -T object.jpg
- List các đối tượng trong container
 curl -X GET [...]
 http://swift.example.com/v1/AUTH_bob/container1 
- Download 1 đối tượng
 curl -X GET [...]
 http://swift.example.com/v1/AUTH_bob/container1/object.jpg 