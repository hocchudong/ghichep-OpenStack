# Tổng quan về Keystone
Các môi trường Cloud với mô hình Infrastructure-as-a-Service cung cấp cho người dùng truy cập đến các tài nguyên quan trọng như các máy ảo, lượng lớn lưu trữ và băng thông mạng. Một tính năng quan trọng của bất kỳ một môi trường cloud là cung cấp bảo mật, kiểm soát truy cập tới những tài nguyền có trên cloud. Trong môi trường Openstack, dịch vụ keystone có trách nhiệm đảm nhận việc bảo mật, kiểm soát truy cập tới tất cả các tài nguyên của cloud. Keystone là một thành phần không thể thiếu để bảo mật cho cloud.

## Các khái niệm trong keystone
- 1. Project:
  - Trong những ngày đầu của Openstack, có một khái niệm là Tenants. Sau đó người ta sử dụng khái niệm Project để thay thế cho trực quan hơn.
  - Project là nhóm và cô lập lại các tài nguyên.
  - Keystone đăng ký các project và sẽ xác định ai nên được phép truy cập vào những project này và sử dụng tài nguyên của project thông qua role mà user được gán trên từng project.
  
- 2. Domain
  - Domain là một tập hợp các user, group và project
  - Domain sẽ giới hạn khả năng hiện thị các project và user của các tổ chức.
  - Để openstack có thể hỗ trợ các tổ chức một các rõ ràng trong việc đặt tên, người ta đã sử dụng một khái niệm Domain.
  
- 3. Region
  - Mỗi region đều triển khai hệ thống full OPS, bao gồm các API endpoint, network và các tài nguyên compute của chính nó.
  - Các Region khác nhau chia sẻ thiết lập chung dịch vụ Keystone và Horizon, để cung cấp khả năng truy cập điều khiển và giao diện web tương tác với hệ thống.
  - Khái niệm Region thì giống như là một nhóm các tài nguyên vật lý được gộp nhóm theo khu vực địa lý trong môi trường OPS. Nếu bạn có 2 trung tâm dữ liệu khác nhau, bạn nên đặt một khu vực và region A trong môi trường OPS và khu vực còn lại vào region B.
  - Khái niệm region ngày các trở nên hữu dụng nhanh chóng, đặc biệt là khi đi cùng với khái niệm cell và domain. Region được sử dung khi triển khai mô hình cloud lớn, trải dài ra trên nhiều trung tâm dữ liệu trên các vùng địa lý cách biệt khác nhau.

- 4. User và User Group
  - User Group là nhóm các user
  - Chúng ta gọi user và user group là actor
  
- 5. Roles
  - Chỉ ra vai trò của người dùng trong project hoặc trong domain,...
  - Mỗi user có thể có vai trò khác nhau đối với từng project.
  
- 6. Assignment
  - Thể hiện sự kết nối giữa một actor(user và user group) với một actor(domain, project) và một role.
  - Role assignment được cấp phát và thu hồi, và có thể được kế thừa giữa các user và group trên project của domains.
  
- 7. Target
  - Chính là project nào hoặc domain nào sẽ được gán Role cho user.
  
- 8. Token
  - Keystone là dịch vụ có trách nhiệm tạo ra token này.
  - User sẽ nhận token này khi xác thực thành công bởi keystone.
  - Token nãy cũng được ủy quyền (nó đại diện cho user). Nó chứa sự ủy quyền của user có trên cloud.
  - Một token có cả 1 ID và 1 payload. ID của token là duy nhất trên mỗi cloud, và payload chứa data về user.
  
- 9. Catalog
  - Chứa URLs và endpoints của các dịch vụ trong cloud.
  - Với catalog, người dùng và ứng dụng có thể biết ở đâu để gửi yêu cầu tạo máy ảo hoặc storage objects.
  - Dịch vụ catalog chia thành danh sách các endpoint, mỗi endpoint chi thành các admin URL, internal URL, public URL.
