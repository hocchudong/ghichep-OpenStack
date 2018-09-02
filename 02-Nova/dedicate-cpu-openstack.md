# Dedicated CPU cho instance trong Openstack


### Mục lục
- [1. Vấn đề sử dụng](#issue)
- [2. Yêu cầu trước khi thực hiện](#require)
- [3. Cách thực hiện cấu hình](#config)
- [4. Kiểm tra kết quả](#summary)


### Nội dung

- #### <a name='issue'>1. Vấn đề sử dụng</a>
    - Dựa trên khái niệm của IBM đưa ra, `dedicated CPU` cho instance là việc một hay nhiều CPU vật lý sẽ được gán cho một instance duy nhất.
    - Việc `dedicated CPU` được sử dụng trong trường hợp instance nào đó hoạt động cần rất nhiều hiệu năng của CPU mà không thể sử dụng chung CPU với các instance khác.


- #### <a name='require'>2. Yêu cầu trước khi thực hiện</a>
    - Các node compute cần có CPU được hỗ trợ `KVM feature`. Để kiểm tra, ta sử dụng câu lệnh:
        
            egrep -c '(vmx|svm)' /proc/cpuinfo
            
        nếu kết quả trả về là một giá trị lớn hơn 0 thì có nghĩa là ta có thể thực hiện dedicated.
        
    - Ta cần phải đảm bảo `libvirt` được cấu hình sử dụng `KVM` thay vì sử dụng `QEMU`. Bằng cách thực hiện sửa hoặc thêm nội dung sau vào file `/etc/nova/nova-compute.conf`:
        
            virt_type = kvm
            
        sau đó hãy restart lại dịch vụ `nova-compute`:
        
            service nova-compute restart
            

- #### <a name='config'>3. Cách thực hiện cấu hình</a>
    - Đầu tiên, ta cần đảm bảo rằng trên các node compute sẽ cần phải không dụng đến các CPU mà ta dự định sẽ thực hiện sử dụng nó gán cho instances. Các bước thực hiện lần lượt như sau:
    
        - Kiểm tra số lượng CPU được cung cấp cho node compute:
        
                lscpu
                
            kết quả sẽ hiển thị tương tự như sau:
            
                Architecture:          x86_64
                CPU op-mode(s):        32-bit, 64-bit
                Byte Order:            Little Endian
                CPU(s):                8
                On-line CPU(s) list:   0-7
                Thread(s) per core:    1
                Core(s) per socket:    4
                Socket(s):             2
                
            theo như kết quả hiển thị trên, ta thấy node compute được cung cấp 8 CPU. Giả sử, ta sẽ thực hiện dedicated CPU với các CPU `4,5,6,7`. Ta cần thực hiện `isolate` các CPU này để đảm bảo nó không được sử dụng bởi node compute bằng cách thực hiện thêm nội dung sau vào file `/etc/default/grub`:
            
                quiet isolcpus=4-7
            
            update GRUB:
            
                grub-mkconfig -o /boot/grub2/grub.cfg    
                
            sau đó thực hiện restart lại node compute và kiểm tra kết quả việc isolate trên bằng cách xem nội dung `quiet isolcpus=4-7` đã xuất hiện trong file `/proc/cmdline` hay chưa. Nếu thành công, ta sẽ thấy tương tự như sau:
            
                BOOT_IMAGE=/vmlinu ... ro quiet isolcpus=4-7
                
            hoặc sử dụng câu lệnh:
            
                cat /proc/$$/status|tail -6
                
            kết quả sẽ hiển thị tương tự như sau:
            
                Cpus_allowed:   0f
                Cpus_allowed_list:      0-3
                    

        - Cấu hình cho `nova-compute` bằng cách thêm hoặc sửa nội dung sau trong file `/etc/nova/nova.conf`:
        
                vcpu_pin_set = "4-7"
                
            sau đó restart lại `nova-compute`
            
            
    
- #### <a name='summary'>4. Kiểm tra kết quả</a>

    - Để tạo ra một instance được `dedicated CPU`. Ta cần tạo một flavor được hỗ trợ `hw:cpu_policy` và `hw:cpu_policy`. Giả sử:
    
            openstack flavor set m1.numa \
            --property hw:cpu_policy=dedicated \
            --property hw:cpu_thread_policy=isolate
            
    - Ta tiến hành tạo mới một instance với flavor trên và kiểm tra log của node compute (`/var/log/nova/nova-compute.log`) mà thực hiện tạo instance đó. Ta sẽ thấy kết quả tương tự như sau:
    
            Computed NUMA topology CPU pinning: usable pCPUs: [[4], [5], [6], [7]], vCPUs mapping: [(0, 4)]
            
        tạo thêm một instance như trên, ta sẽ thấy log xuất hiện:
        
            Computed NUMA topology CPU pinning: usable pCPUs: [[5], [6], [7]], vCPUs mapping: [(0, 5)]
            
        Như vậy, ta đã thực hiện được việc `dedicated CPU` cho instance.
